# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class OctaGatewayCommandWizard(models.TransientModel):
    """
    Wizard ra lệnh mở/đóng cổng — 2 bước:
    1. Chọn lệnh (open/close)
    2. Nhập lý do
    3. Tick emergency nếu là lệnh khẩn
    """
    _name = 'octa.gateway.command.wizard'
    _description = 'Wizard lệnh cổng API'

    gateway_id = fields.Many2one(
        'octa.gateway', 'Cổng', required=True, readonly=True,
    )
    gateway_state = fields.Selection(related='gateway_id.state', readonly=True)
    scope = fields.Selection(related='gateway_id.scope', readonly=True)

    command = fields.Selection([
        ('open',  '🟢 Mở cổng'),
        ('close', '⚫ Đóng cổng'),
    ], string='Loại lệnh', required=True)

    reason = fields.Text(
        'Lý do *', required=True,
        placeholder='Bắt buộc nhập lý do đầy đủ...',
    )
    emergency = fields.Boolean(
        'Lệnh khẩn cấp',
        help=(
            'Tích nếu cần thực hiện ngay không chờ phê duyệt.\n'
            'Bắt buộc bổ sung phê duyệt trong 2 giờ sau khi ra lệnh.'
        ),
    )

    @api.onchange('gateway_state')
    def _onchange_gateway_state(self):
        """Gợi ý lệnh dựa theo trạng thái hiện tại."""
        if self.gateway_state in ('closed', 'locked'):
            self.command = 'open'
        else:
            self.command = 'close'

    def action_execute(self):
        """Thực hiện lệnh."""
        self.ensure_one()
        if not self.reason or not self.reason.strip():
            raise UserError('Bắt buộc nhập lý do.')

        gw = self.gateway_id

        # Kiểm tra quyền
        user = self.env.user
        can_command = (
            user.has_group('octa_base.group_lead')
            or user.has_group('octa_base.group_tdabg')
            or user.has_group('octa_base.group_ppkd')
            or user.has_group('octa_base.group_tpkd')
        )
        if not can_command:
            raise UserError(
                'Chỉ Lead trở lên mới có thể ra lệnh mở/đóng cổng.'
            )

        # Tạo và thực hiện lệnh
        cmd = self.env['octa.gateway.command'].create({
            'gateway_id': gw.id,
            'command':    self.command,
            'reason':     self.reason.strip(),
            'emergency':  self.emergency,
            'issued_by':  self.env.uid,
            'scope':      gw.scope,
        })
        cmd.action_confirm()

        # Nếu lệnh khẩn → nhắc TDABG bổ sung phê duyệt
        if self.emergency:
            config = self.env['octa.approval.config'].sudo().search(
                [('active', '=', True)], limit=1
            )
            hours = config.emergency_approval_hours if config else 2

            # Tạo activity nhắc TDABG
            group = self.env.ref('octa_base.group_tdabg', raise_if_not_found=False)
            if group:
                for u in group.users:
                    if u == self.env.user:
                        continue
                    try:
                        cmd.activity_schedule(
                            'mail.mail_activity_data_todo',
                            user_id=u.id,
                            summary=f'Bổ sung phê duyệt lệnh khẩn: {gw.name}',
                            note=(
                                f'Lệnh khẩn <b>{cmd.name}</b> cần phê duyệt bổ sung '
                                f'trong <b>{hours} giờ</b>.<br/>'
                                f'Cổng: {gw.name}<br/>'
                                f'Người ra lệnh: {self.env.user.name}<br/>'
                                f'Lý do: {self.reason}'
                            ),
                        )
                    except Exception:
                        pass

        # Thông báo kết quả
        action_label = 'MỞ' if self.command == 'open' else 'ĐÓNG'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': f'Đã {action_label} cổng',
                'message': f'{gw.name} — {self.reason}',
                'type': 'success' if self.command == 'open' else 'warning',
                'sticky': False,
            },
        }


class OctaGatewaySupplementalWizard(models.TransientModel):
    """Wizard phê duyệt bổ sung cho lệnh khẩn cấp."""
    _name = 'octa.gateway.supplemental.wizard'
    _description = 'Phê duyệt bổ sung lệnh khẩn'

    command_id = fields.Many2one(
        'octa.gateway.command', 'Lệnh khẩn', required=True, readonly=True,
    )
    gateway_name = fields.Char(related='command_id.gateway_id.name', readonly=True)
    original_reason = fields.Text(related='command_id.reason', readonly=True)
    reason = fields.Text('Lý do phê duyệt bổ sung *', required=True)

    def action_approve(self):
        self.ensure_one()
        if not self.reason or not self.reason.strip():
            raise UserError('Bắt buộc nhập lý do phê duyệt bổ sung.')
        self.command_id._do_supplemental_approve(self.reason.strip())
        return {'type': 'ir.actions.act_window_close'}