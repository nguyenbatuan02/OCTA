# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class OctaGateway(models.Model):
    """
    Cổng API Bigtel — quản lý trạng thái, đếm lỗi, ranh đỏ tự động.

    State machine:
        active → warning → locked (auto khi ≥ threshold lỗi)
        locked → active  (khi TDABG/PPKD mở lại thủ công sau phê duyệt)
        active/warning → closed (lệnh thủ công có phê duyệt)
        closed → active  (lệnh thủ công mở lại)

    Ranh đỏ cứng: error_count ≥ gateway_error_threshold → cron tự lock
    """
    _name = 'octa.gateway'
    _description = 'Cổng API Bigtel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    _rec_name = 'name'

    # ── Thông tin ───────────────────────────────────────────────────

    name = fields.Char('Tên cổng', required=True, tracking=True)
    code = fields.Char('Mã cổng', required=True, copy=False)
    sequence = fields.Integer('Thứ tự', default=10)
    scope = fields.Selection([
        ('bigtel', 'Bigtel'),
        ('bigm', 'BigM'),
        ('utv', 'UTV'),
    ], required=True, default='bigtel', tracking=True)

    ncc_id = fields.Many2one(
        'res.partner', 'Nhà cung cấp',
        domain="[('supplier_rank', '>', 0)]", tracking=True,
    )
    network = fields.Selection([
        ('viettel', 'Viettel'), ('vina', 'Vinaphone'),
        ('mobi', 'Mobifone'), ('other', 'Khác'),
    ], string='Nhà mạng', tracking=True)
    gateway_type = fields.Selection([
        ('topup', 'Nạp tiền'), ('card', 'Thẻ cào'),
        ('api', 'API số dư'), ('flight', 'Vé máy bay'), ('other', 'Khác'),
    ], string='Loại cổng', required=True, default='topup', tracking=True)

    # ── Trạng thái ─────────────────────────────────────────────────

    state = fields.Selection([
        ('active',  '✅ Hoạt động'),
        ('warning', '🟡 Cảnh báo'),
        ('closed',  '⚫ Đã đóng'),
        ('locked',  '🔴 Khóa tự động'),
    ], default='active', required=True, tracking=True, index=True)

    is_backup = fields.Boolean('Cổng backup', default=False, tracking=True)
    backup_gateway_id = fields.Many2one(
        'octa.gateway', 'Cổng backup',
        domain="[('is_backup', '=', True), ('id', '!=', id)]",
    )

    # ── Số liệu vận hành ────────────────────────────────────────────

    api_balance = fields.Float(
        'Số dư API (VNĐ)', digits=(15, 0), tracking=True,
    )
    api_balance_threshold = fields.Float(
        'Ngưỡng cảnh báo số dư (VNĐ)', digits=(15, 0),
        help='Khi số dư ≤ ngưỡng → cảnh báo vàng.',
    )
    success_rate = fields.Float('Tỷ lệ thành công (%)', digits=(5, 2))

    # ── Đếm lỗi (ranh đỏ) ──────────────────────────────────────────

    error_count = fields.Integer(
        'Số lỗi liên tiếp', default=0, tracking=True,
        help='Cron kiểm tra: ≥ ngưỡng → auto-lock.',
    )
    last_error_time = fields.Datetime('Thời điểm lỗi gần nhất', readonly=True)
    auto_locked_at  = fields.Datetime('Thời điểm bị khóa tự động', readonly=True)
    emergency_deadline = fields.Datetime(
        'Hạn bổ sung phê duyệt', readonly=True,
        help='Deadline 2h sau lệnh khẩn — TDABG phải bổ sung phê duyệt.',
    )
    pending_approval_command_id = fields.Many2one(
        'octa.gateway.command', 'Lệnh khẩn chờ phê duyệt', readonly=True,
    )

    # ── Lịch sử lệnh ────────────────────────────────────────────────

    command_ids = fields.One2many(
        'octa.gateway.command', 'gateway_id', string='Lịch sử lệnh',
    )
    command_count = fields.Integer(compute='_compute_command_count')

    is_balance_low = fields.Boolean(compute='_compute_balance_warning')

    @api.depends('command_ids')
    def _compute_command_count(self):
        for rec in self:
            rec.command_count = len(rec.command_ids)

    @api.depends('api_balance', 'api_balance_threshold')
    def _compute_balance_warning(self):
        for rec in self:
            rec.is_balance_low = (
                rec.api_balance_threshold > 0
                and rec.api_balance <= rec.api_balance_threshold
            )

    # ── Action mở wizard lệnh ───────────────────────────────────────

    def action_open_command_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Lệnh cổng: {self.name}',
            'res_model': 'octa.gateway.command.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_gateway_id': self.id,
                'default_scope': self.scope,
            },
        }

    def action_view_commands(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Lịch sử lệnh — {self.name}',
            'res_model': 'octa.gateway.command',
            'view_mode': 'list,form',
            'domain': [('gateway_id', '=', self.id)],
        }

    # ── Internal: auto-lock khi chạm ranh đỏ ───────────────────────

    def _auto_lock(self, reason: str = ''):
        self.ensure_one()
        now = fields.Datetime.now()
        config = self.env['octa.approval.config'].sudo().search(
            [('active', '=', True)], limit=1
        )
        hours = config.emergency_approval_hours if config else 2
        deadline = fields.Datetime.add(now, hours=hours)

        self.write({
            'state': 'locked',
            'auto_locked_at': now,
            'emergency_deadline': deadline,
        })

        # Tạo lệnh khẩn tự động
        root = self.env.ref('base.user_root')
        cmd = self.env['octa.gateway.command'].sudo().create({
            'gateway_id': self.id,
            'command':    'lock',
            'reason':     reason or f'Auto-lock: {self.error_count} lỗi liên tiếp',
            'emergency':  True,
            'issued_by':  root.id,
            'scope':      self.scope,
            'state':      'done',
        })
        self.pending_approval_command_id = cmd

        # Audit log
        self.env['octa.audit.log'].sudo().log_action(
            action_type='emergency',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            reason=reason or f'Auto-lock: {self.error_count} lỗi liên tiếp',
            scope_tag=self.scope,
            emergency=True,
        )

        # Chatter
        self.message_post(
            body=(
                f'🔴 <b>CỔNG BỊ KHÓA TỰ ĐỘNG</b><br/>'
                f'Lý do: {reason or f"{self.error_count} lỗi liên tiếp"}<br/>'
                f'Thời điểm: {now.strftime("%H:%M %d/%m/%Y")}<br/>'
                f'⏰ Hạn bổ sung phê duyệt: {deadline.strftime("%H:%M %d/%m/%Y")}'
            ),
            subtype_xmlid='mail.mt_note',
        )

        # Alert managers
        self._alert_managers(
            f'🔴 CỔNG {self.name} KHÓA TỰ ĐỘNG — {self.error_count} lỗi. '
            f'Bổ sung phê duyệt trước {deadline.strftime("%H:%M")}.'
        )

        # Kích hoạt backup nếu có
        if self.backup_gateway_id and self.backup_gateway_id.state == 'closed':
            self.backup_gateway_id.write({'state': 'active'})

    def _alert_managers(self, message: str):
        """Gửi alert bus qua TDABG/PPKD/TPKD."""
        for xml_id in [
            'octa_base.group_tdabg',
            'octa_base.group_ppkd',
            'octa_base.group_tpkd',
        ]:
            group = self.env.ref(xml_id, raise_if_not_found=False)
            if not group:
                continue
            for user in group.users:
                try:
                    self.env['bus.bus'].sudo()._sendone(
                        user.partner_id,
                        'octa_gateway_alert',
                        {
                            'gateway_id':   self.id,
                            'gateway_name': self.name,
                            'state':        self.state,
                            'message':      message,
                            'error_count':  self.error_count,
                        },
                    )
                except Exception:
                    pass

    # ── Cron ────────────────────────────────────────────────────────

    @api.model
    def _cron_check_gateway_red_lines(self):
        """
        Cron mỗi phút:
        1. Cổng error_count ≥ ngưỡng → auto-lock
        2. Lệnh khẩn quá hạn phê duyệt → alert leo thang
        3. Số dư API thấp → cảnh báo vàng
        """
        config = self.env['octa.approval.config'].sudo().search(
            [('active', '=', True)], limit=1
        )
        threshold   = config.gateway_error_threshold if config else 5
        emg_hours   = config.emergency_approval_hours if config else 2

        # 1. Auto-lock
        to_lock = self.search([
            ('state', 'in', ['active', 'warning']),
            ('error_count', '>=', threshold),
        ])
        for gw in to_lock:
            gw._auto_lock(
                f'Auto-lock: {gw.error_count} lỗi liên tiếp (ngưỡng={threshold})'
            )

        # 2. Quá hạn bổ sung phê duyệt
        now = fields.Datetime.now()
        overdue = self.search([
            ('state', '=', 'locked'),
            ('emergency_deadline', '!=', False),
            ('emergency_deadline', '<', now),
            ('pending_approval_command_id', '!=', False),
        ])
        for gw in overdue:
            gw._alert_managers(
                f'⚠️ QUÁ HẠN phê duyệt lệnh khẩn: {gw.name} '
                f'({emg_hours}h chưa được duyệt!)'
            )
            gw.message_post(
                body=(
                    f'⚠️ <b>QUÁ HẠN bổ sung phê duyệt</b> — '
                    f'Alert leo thang PPKD/TPKD.'
                ),
                subtype_xmlid='mail.mt_note',
            )

        # 3. Số dư API thấp
        low_bal = self.search([
            ('state', '=', 'active'),
            ('api_balance_threshold', '>', 0),
        ]).filtered(lambda g: g.api_balance <= g.api_balance_threshold)
        for gw in low_bal:
            gw.write({'state': 'warning'})
            gw._alert_managers(
                f'🟡 SỐ DƯ THẤP: {gw.name} — '
                f'{gw.api_balance:,.0f} ≤ ngưỡng {gw.api_balance_threshold:,.0f} VNĐ'
            )