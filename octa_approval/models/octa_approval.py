# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


# ── Loại phiếu ─────────────────────────────────────────────────────
APPROVAL_TYPE = [
    ('refund',  'Hoàn tiền / Nạp bù'),
    ('gateway', 'Mở / Đóng cổng'),
    ('ncc',     'Đề xuất NCC mới'),
    ('price',   'Phê duyệt giá / Chiết khấu'),
    ('debt',    'Cấp hạn mức công nợ'),
    ('other',   'Khác'),
]

# Loại phiếu dùng hạn mức tiền để escalate
AMOUNT_BASED_TYPES = {'refund', 'debt'}

# Map role → chuỗi hiển thị
ROLE_LABELS = {
    'lead':  'Lead CSKH & Vận hành',
    'tdabg': 'Trưởng dự án Bigtel',
    'ppkd':  'Phó phòng Kinh doanh',
    'tpkd':  'Trưởng phòng Kinh doanh',
    'gd':    'Giám đốc',
}


class OctaApproval(models.Model):
    """
    Phiếu phê duyệt tập trung Octa.

    State machine:
        draft → pending → approved
                        ↘ rejected
                        ↘ (escalated → pending tầng trên)

    Nguyên tắc cứng:
    1. SoD: requester_id != người duyệt hiện tại
    2. Vượt hạn mức: can_approve=False → chỉ hiện nút Escalate
    3. Mọi thao tác ghi octa.audit.log
    4. Escalate đúng thứ tự tầng, không bypass
    """
    _name = 'octa.approval'
    _description = 'Phiếu phê duyệt Octa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    # ── Thông tin cơ bản ────────────────────────────────────────────

    name = fields.Char(
        'Mã phiếu', readonly=True, copy=False, default='New',
    )
    approval_type = fields.Selection(
        APPROVAL_TYPE, string='Loại phiếu',
        required=True, tracking=True,
    )
    scope = fields.Selection([
        ('bigtel', 'Bigtel'),
        ('bigm',   'BigM'),
        ('utv',    'UTV'),
    ], string='Phạm vi', required=True, default='bigtel', tracking=True)

    state = fields.Selection([
        ('draft',     'Nháp'),
        ('pending',   'Chờ duyệt'),
        ('approved',  'Đã duyệt'),
        ('rejected',  'Từ chối'),
        ('cancelled', 'Huỷ'),
    ], string='Trạng thái', default='draft', required=True,
       tracking=True, copy=False)

    # ── Người liên quan ─────────────────────────────────────────────

    requester_id = fields.Many2one(
        'res.users', 'Người đề xuất',
        required=True, tracking=True,
        default=lambda self: self.env.uid,
    )
    current_approver_role = fields.Selection([
        ('lead',  'Lead'),
        ('tdabg', 'TDABG'),
        ('ppkd',  'PPKD'),
        ('tpkd',  'TPKD'),
        ('gd',    'Giám đốc'),
    ], string='Tầng duyệt hiện tại', tracking=True)

    approved_by_id = fields.Many2one(
        'res.users', 'Người đã duyệt', readonly=True, tracking=True,
    )
    approved_at    = fields.Datetime('Thời điểm duyệt', readonly=True)
    rejected_by_id = fields.Many2one(
        'res.users', 'Người từ chối', readonly=True, tracking=True,
    )
    rejected_at    = fields.Datetime('Thời điểm từ chối', readonly=True)

    # ── Nội dung ────────────────────────────────────────────────────

    description = fields.Text(
        'Nội dung / Lý do đề xuất', required=True, tracking=True,
    )
    amount = fields.Float(
        'Số tiền (VNĐ)', digits=(15, 0), tracking=True,
        help='Bắt buộc với loại: Hoàn tiền, Công nợ.',
    )
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'octa_approval_attachment_rel',
        'approval_id', 'attachment_id',
        string='Tài liệu đính kèm',
    )

    # ── Lý do các hành động ─────────────────────────────────────────

    approve_reason  = fields.Text('Lý do phê duyệt',   readonly=True, tracking=True)
    reject_reason   = fields.Text('Lý do từ chối',     tracking=True)
    escalate_reason = fields.Text('Lý do chuyển tầng', readonly=True, tracking=True)

    # ── Lịch sử escalate ────────────────────────────────────────────

    escalation_history_ids = fields.One2many(
        'octa.approval.escalation', 'approval_id',
        string='Lịch sử chuyển tầng', readonly=True,
    )

    # ── Link ticket gốc ─────────────────────────────────────────────

    ticket_id   = fields.Many2one(
        'project.task', 'Ticket liên quan',
        tracking=True, ondelete='set null',
    )
    ticket_name = fields.Char(related='ticket_id.name', readonly=True)

    # ── Computed: kiểm soát UI ──────────────────────────────────────
    # FIX: store=False → không cache, recompute mỗi lần user mở form
    # Bắt buộc vì can_approve phụ thuộc env.user (không khai báo được trong depends)

    can_approve = fields.Boolean(
        'Có thể duyệt',
        compute='_compute_can_approve',
        store=False,
        help='False → disable nút Duyệt.',
    )
    can_escalate = fields.Boolean(
        'Có thể escalate',
        compute='_compute_can_approve',
        store=False,
    )
    limit_display = fields.Float(
        'Hạn mức tầng hiện tại (VNĐ)',
        compute='_compute_limit_display',
        store=False,
        digits=(15, 0),
    )
    amount_vs_limit = fields.Float(
        'Chênh lệch so với hạn mức (VNĐ)',
        compute='_compute_limit_display',
        store=False,
        digits=(15, 0),
        help='Dương = vượt hạn mức → phải escalate.',
    )

    # ── Computes ────────────────────────────────────────────────────

    @api.depends('amount', 'current_approver_role', 'approval_type',
                 'state', 'requester_id')
    def _compute_can_approve(self):
        # sudo() vì NV CSKH/Ops không có ACL đọc octa.approval.config
        config = self.env['octa.approval.config'].sudo().search(
            [('active', '=', True)], limit=1
        )
        user = self.env.user
        user_role = self.env['octa.approval.config'].sudo().get_role_for_user(user)

        for rec in self:
            if rec.state != 'pending':
                rec.can_approve = rec.can_escalate = False
                continue

            # SoD: so sánh bằng id để tránh False positive
            if rec.requester_id.id == user.id:
                rec.can_approve = rec.can_escalate = False
                continue

            # Phải đúng tầng
            if user_role != rec.current_approver_role:
                rec.can_approve = rec.can_escalate = False
                continue

            # Loại phiếu không dựa hạn mức tiền → approve trực tiếp
            if rec.approval_type not in AMOUNT_BASED_TYPES or not config:
                rec.can_approve = True
                rec.can_escalate = False
                continue

            # Kiểm tra hạn mức tiền
            limit = config.sudo().get_limit_for_role(user_role)
            within = (limit > 0) and (rec.amount <= limit)
            rec.can_approve  = within
            rec.can_escalate = not within

    @api.depends('amount', 'current_approver_role')
    def _compute_limit_display(self):
        config = self.env['octa.approval.config'].sudo().search(
            [('active', '=', True)], limit=1
        )
        for rec in self:
            if not config or not rec.current_approver_role:
                rec.limit_display = rec.amount_vs_limit = 0
                continue
            limit = config.sudo().get_limit_for_role(rec.current_approver_role)
            rec.limit_display   = limit
            rec.amount_vs_limit = rec.amount - limit

    # ── Constraints ─────────────────────────────────────────────────

    @api.constrains('amount', 'approval_type')
    def _check_amount_required(self):
        for rec in self:
            if rec.approval_type in AMOUNT_BASED_TYPES and rec.amount <= 0:
                raise ValidationError(
                    f'Loại phiếu "{dict(APPROVAL_TYPE).get(rec.approval_type)}" '
                    'bắt buộc nhập Số tiền > 0.'
                )

    # ── Create ──────────────────────────────────────────────────────

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = (
                self.env['ir.sequence'].next_by_code('octa.approval') or 'New'
            )
        rec = super().create(vals)
        self.env['octa.audit.log'].log_action(
            action_type='create',
            object_model=self._name,
            object_id=rec.id,
            object_name=rec.name,
            new_value=f'type={rec.approval_type}, amount={rec.amount:,.0f}',
            scope_tag=rec.scope,
        )
        return rec

    # ── Actions ─────────────────────────────────────────────────────

    def action_submit(self):
        """Draft → Pending. Xác định tầng duyệt đầu tiên."""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError('Chỉ nộp được phiếu đang ở trạng thái Nháp.')
        if not self.description:
            raise UserError('Bắt buộc nhập Nội dung / Lý do đề xuất.')

        first_role = self._get_first_approver_role()
        self.write({'state': 'pending', 'current_approver_role': first_role})
        self._notify_approver(first_role)
        self.env['octa.audit.log'].log_action(
            action_type='write',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            old_value='draft',
            new_value=f'pending → {first_role}',
            scope_tag=self.scope,
        )

    def action_approve(self):
        """Mở wizard xác nhận phê duyệt."""
        self.ensure_one()
        if not self.can_approve:
            raise UserError(
                'Bạn không thể phê duyệt phiếu này.\n'
                'Kiểm tra: đúng tầng duyệt, số tiền ≤ hạn mức, '
                'và bạn không phải người tạo phiếu.'
            )
        return self._open_action_wizard('approve')

    def action_reject(self):
        """Mở wizard xác nhận từ chối."""
        self.ensure_one()
        if self.state != 'pending':
            raise UserError('Chỉ từ chối được phiếu đang chờ duyệt.')
        user_role = self.env['octa.approval.config'].sudo().get_role_for_user()
        if user_role != self.current_approver_role:
            raise UserError('Bạn không phải người duyệt tầng này.')
        if self.requester_id.id == self.env.uid:
            raise UserError('Không thể từ chối phiếu do chính mình tạo.')
        return self._open_action_wizard('reject')

    def action_escalate(self):
        """Mở wizard chuyển tầng."""
        self.ensure_one()
        if not self.can_escalate:
            raise UserError(
                'Không thể chuyển tầng.\n'
                'Chỉ chuyển khi số tiền vượt hạn mức tầng hiện tại.'
            )
        return self._open_action_wizard('escalate')

    def action_cancel(self):
        """Huỷ phiếu."""
        self.ensure_one()
        if self.state in ('approved', 'rejected'):
            raise UserError('Không thể huỷ phiếu đã duyệt hoặc từ chối.')
        user = self.env.user
        if self.requester_id.id != user.id and not user.has_group('octa_base.group_lead'):
            raise UserError('Chỉ người tạo hoặc Lead trở lên mới huỷ được.')
        self.write({'state': 'cancelled'})
        self.env['octa.audit.log'].log_action(
            action_type='stop',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            scope_tag=self.scope,
        )

    # ── Internal methods ─────────────────────────────────────────────

    def _open_action_wizard(self, action: str) -> dict:
        return {
            'type': 'ir.actions.act_window',
            'name': {
                'approve':  'Xác nhận phê duyệt',
                'reject':   'Xác nhận từ chối',
                'escalate': 'Chuyển lên tầng trên',
            }.get(action, 'Hành động'),
            'res_model': 'octa.approval.action.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_approval_id': self.id,
                'default_action': action,
            },
        }

    def _get_first_approver_role(self) -> str:
        """
        FIX: dùng dict map thay vì chain index — rõ ràng và không lỗi.

        Nguyên tắc SoD: người duyệt phải ở tầng CAO HƠN người tạo.
            unknown/cskh/ops → lead   (NV tạo → Lead duyệt)
            lead             → tdabg  (Lead tạo → TDABG duyệt, SoD)
            tdabg            → ppkd
            ppkd             → tpkd
            tpkd             → gd
        """
        requester_role = self.env['octa.approval.config'].sudo().get_role_for_user(
            self.requester_id
        )
        role_map = {
            'unknown': 'lead',
            'cskh':    'lead',
            'ops':     'lead',
            'lead':    'tdabg',
            'tdabg':   'ppkd',
            'ppkd':    'tpkd',
            'tpkd':    'gd',
        }
        return role_map.get(requester_role, 'lead')

    def _do_approve(self, reason: str):
        """Thực hiện approve — gọi từ wizard."""
        self.write({
            'state':                 'approved',
            'approved_by_id':        self.env.uid,
            'approved_at':           fields.Datetime.now(),
            'approve_reason':        reason,
            'current_approver_role': False,
        })
        if self.ticket_id:
            self.ticket_id.message_post(
                body=(
                    f'✅ Phiếu <b>{self.name}</b> đã được phê duyệt.<br/>'
                    f'Số tiền: {self.amount:,.0f} VNĐ<br/>'
                    f'Người duyệt: {self.env.user.name}<br/>'
                    f'Lý do: {reason}'
                ),
            )
        self.env['octa.audit.log'].log_action(
            action_type='approve',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            reason=reason,
            scope_tag=self.scope,
        )

    def _do_reject(self, reason: str):
        """Thực hiện reject — gọi từ wizard."""
        if not reason:
            raise UserError('Bắt buộc nhập lý do từ chối.')
        self.write({
            'state':                 'rejected',
            'rejected_by_id':        self.env.uid,
            'rejected_at':           fields.Datetime.now(),
            'reject_reason':         reason,
            'current_approver_role': False,
        })
        if self.ticket_id:
            self.ticket_id.message_post(
                body=f'❌ Phiếu <b>{self.name}</b> bị từ chối.<br/>Lý do: {reason}',
            )
        self.env['octa.audit.log'].log_action(
            action_type='reject',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            reason=reason,
            scope_tag=self.scope,
        )

    def _do_escalate(self, reason: str):
        """Thực hiện escalate — gọi từ wizard."""
        if not reason:
            raise UserError('Bắt buộc nhập lý do chuyển tầng.')
        config = self.env['octa.approval.config'].sudo().get_active()
        next_role = config.get_escalate_role(self.current_approver_role)
        if next_role == self.current_approver_role:
            raise UserError('Đã ở tầng cao nhất (Giám đốc). Liên hệ trực tiếp.')

        self.env['octa.approval.escalation'].create({
            'approval_id':  self.id,
            'from_role':    self.current_approver_role,
            'to_role':      next_role,
            'escalated_by': self.env.uid,
            'reason':       reason,
        })
        self.write({
            'state':                 'pending',
            'current_approver_role': next_role,
            'escalate_reason':       reason,
        })
        self._notify_approver(next_role)

        role_chain = ['lead', 'tdabg', 'ppkd', 'tpkd', 'gd']
        level = f'L{role_chain.index(next_role) + 1}' if next_role in role_chain else 'L5'
        self.env['octa.audit.log'].log_action(
            action_type='escalate',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            new_value=f'→ {ROLE_LABELS.get(next_role, next_role)}',
            reason=reason,
            scope_tag=self.scope,
            escalation_level=level,
        )

    def _notify_approver(self, role: str):
        """Ghi thông báo vào chatter — không gửi email."""
        group_map = {
            'lead':  'octa_base.group_lead',
            'tdabg': 'octa_base.group_tdabg',
            'ppkd':  'octa_base.group_ppkd',
            'tpkd':  'octa_base.group_tpkd',
        }
        xml_id = group_map.get(role)
        if not xml_id:
            return
        group = self.env.ref(xml_id, raise_if_not_found=False)
        if not group:
            return

        notify_users = group.users.filtered(
            lambda u: u.id != self.requester_id.id and u.active
        )
        if not notify_users:
            return

        for user in notify_users:
            try:
                self.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=user.id,
                    summary=f'Cần duyệt: {self.name}',
                    note=(
                        f'Phiếu <b>{self.name}</b> cần phê duyệt tầng '
                        f'<b>{ROLE_LABELS.get(role, role)}</b>.<br/>'
                        f'Loại: {dict(APPROVAL_TYPE).get(self.approval_type, "")}<br/>'
                        f'Số tiền: {self.amount:,.0f} VNĐ<br/>'
                        f'Người đề xuất: {self.requester_id.name}'
                    ),
                )
            except Exception:
                pass

        # Ghi vào chatter, không gửi email (mt_note)
        self.message_post(
            body=(
                f'📋 Chờ duyệt tầng: <b>{ROLE_LABELS.get(role, role)}</b><br/>'
                f'Người được thông báo: {", ".join(notify_users.mapped("name"))}'
            ),
            subtype_xmlid='mail.mt_note',
        )