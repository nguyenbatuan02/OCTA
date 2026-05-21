# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class OctaApprovalActionWizard(models.TransientModel):
    _name = 'octa.approval.action.wizard'
    _description = 'Wizard hành động phê duyệt'

    approval_id = fields.Many2one(
        'octa.approval', 'Phiếu phê duyệt',
        required=True, readonly=True,
    )
    action = fields.Selection([
        ('approve',  'Phê duyệt'),
        ('reject',   'Từ chối'),
        ('escalate', 'Chuyển tầng'),
    ], required=True, readonly=True)

    reason = fields.Text(
        'Lý do',
        help='Bắt buộc với mọi hành động.',
    )

    # Hiển thị thông tin tham khảo trên wizard
    amount         = fields.Float(related='approval_id.amount',       readonly=True, digits=(15, 0))
    limit_display  = fields.Float(related='approval_id.limit_display', readonly=True, digits=(15, 0))
    amount_vs_limit= fields.Float(related='approval_id.amount_vs_limit', readonly=True, digits=(15, 0))
    approval_type  = fields.Selection(related='approval_id.approval_type', readonly=True)
    current_role   = fields.Selection(related='approval_id.current_approver_role', readonly=True)

    @api.constrains('reason')
    def _check_reason_required(self):
        for rec in self:
            if not rec.reason or not rec.reason.strip():
                raise UserError('Bắt buộc nhập lý do.')

    def action_confirm(self):
        """Thực hiện hành động đã chọn."""
        self.ensure_one()
        if not self.reason or not self.reason.strip():
            raise UserError('Bắt buộc nhập lý do trước khi xác nhận.')

        approval = self.approval_id
        reason = self.reason.strip()

        if self.action == 'approve':
            approval._do_approve(reason)
        elif self.action == 'reject':
            approval._do_reject(reason)
        elif self.action == 'escalate':
            approval._do_escalate(reason)

        return {'type': 'ir.actions.act_window_close'}