# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class OctaGatewayCommand(models.Model):
    """
    Lịch sử lệnh mở/đóng cổng API.
    Bất biến sau khi state=done — không cho sửa/xóa.

    Mỗi lệnh phải có:
    - Người ra lệnh (issued_by)
    - Lý do (reason) — bắt buộc
    - Timestamp
    - Trạng thái (draft/done/cancelled)
    - emergency=True nếu là lệnh khẩn (cần bổ sung phê duyệt trong 2h)
    """
    _name = 'octa.gateway.command'
    _description = 'Lệnh mở/đóng cổng API'
    _inherit = ['mail.thread']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(
        'Mã lệnh', readonly=True, copy=False, default='New',
    )
    gateway_id = fields.Many2one(
        'octa.gateway', 'Cổng', required=True,
        ondelete='cascade', tracking=True,
    )
    scope = fields.Selection([
        ('bigtel', 'Bigtel'), ('bigm', 'BigM'), ('utv', 'UTV'),
    ], related='gateway_id.scope', store=True, readonly=True)

    command = fields.Selection([
        ('open',  '🟢 Mở cổng'),
        ('close', '⚫ Đóng cổng'),
        ('lock',  '🔴 Khóa khẩn (Auto)'),
    ], string='Loại lệnh', required=True, tracking=True)

    state = fields.Selection([
        ('draft',     'Nháp'),
        ('done',      'Đã thực hiện'),
        ('cancelled', 'Đã huỷ'),
    ], default='draft', required=True, tracking=True)

    issued_by = fields.Many2one(
        'res.users', 'Người ra lệnh',
        required=True, default=lambda self: self.env.uid,
        tracking=True,
    )
    issued_at = fields.Datetime(
        'Thời điểm ra lệnh',
        default=fields.Datetime.now, readonly=True,
    )
    reason = fields.Text(
        'Lý do', required=True, tracking=True,
    )
    emergency = fields.Boolean(
        'Lệnh khẩn cấp', default=False, tracking=True,
        help='Lệnh khẩn: thực hiện ngay, bổ sung phê duyệt trong 2h.',
    )

    # Phê duyệt bổ sung cho lệnh khẩn
    supplemental_approved_by = fields.Many2one(
        'res.users', 'Phê duyệt bổ sung', readonly=True, tracking=True,
    )
    supplemental_approved_at = fields.Datetime(
        'Thời điểm phê duyệt bổ sung', readonly=True,
    )
    supplemental_reason = fields.Text(
        'Lý do phê duyệt bổ sung', readonly=True,
    )

    # Trạng thái phê duyệt bổ sung
    supplemental_state = fields.Selection([
        ('pending',  'Chờ phê duyệt bổ sung'),
        ('approved', 'Đã phê duyệt bổ sung'),
        ('overdue',  'Quá hạn'),
    ], string='Phê duyệt bổ sung', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = (
                self.env['ir.sequence'].next_by_code('octa.gateway.command')
                or 'New'
            )
        if vals.get('emergency'):
            vals['supplemental_state'] = 'pending'
        return super().create(vals)

    def action_confirm(self):
        """Xác nhận thực hiện lệnh — cập nhật trạng thái cổng."""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError('Chỉ xác nhận được lệnh đang ở trạng thái Nháp.')

        gw = self.gateway_id
        if self.command == 'open':
            gw.write({'state': 'active', 'error_count': 0})
            # Xóa pending approval nếu có
            if gw.pending_approval_command_id == self:
                gw.write({
                    'pending_approval_command_id': False,
                    'emergency_deadline': False,
                })
        elif self.command == 'close':
            gw.write({'state': 'closed'})
        elif self.command == 'lock':
            gw.write({'state': 'locked'})

        self.write({'state': 'done'})

        # Audit log
        self.env['octa.audit.log'].log_action(
            action_type='stop' if self.command in ('close', 'lock') else 'write',
            object_model='octa.gateway',
            object_id=gw.id,
            object_name=gw.name,
            new_value=f'command={self.command}, emergency={self.emergency}',
            reason=self.reason,
            scope_tag=self.scope,
            emergency=self.emergency,
        )

    def action_supplemental_approve(self):
        """Phê duyệt bổ sung cho lệnh khẩn."""
        self.ensure_one()
        if not self.emergency:
            raise UserError('Chỉ phê duyệt bổ sung cho lệnh khẩn cấp.')
        if self.supplemental_state == 'approved':
            raise UserError('Lệnh này đã được phê duyệt bổ sung rồi.')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Phê duyệt bổ sung lệnh khẩn',
            'res_model': 'octa.gateway.supplemental.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_command_id': self.id},
        }

    def _do_supplemental_approve(self, reason: str):
        """Gọi từ wizard."""
        self.write({
            'supplemental_state':       'approved',
            'supplemental_approved_by': self.env.uid,
            'supplemental_approved_at': fields.Datetime.now(),
            'supplemental_reason':      reason,
        })
        # Xóa deadline khẩn trên cổng
        gw = self.gateway_id
        if gw.pending_approval_command_id == self:
            gw.write({
                'pending_approval_command_id': False,
                'emergency_deadline': False,
            })

        self.env['octa.audit.log'].log_action(
            action_type='approve',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            reason=reason,
            scope_tag=self.scope,
            emergency=True,
        )
        self.message_post(
            body=(
                f'✅ <b>Phê duyệt bổ sung hoàn tất</b><br/>'
                f'Người duyệt: {self.env.user.name}<br/>'
                f'Lý do: {reason}'
            ),
            subtype_xmlid='mail.mt_note',
        )