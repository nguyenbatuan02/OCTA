# -*- coding: utf-8 -*-
from odoo import models, fields


class OctaApprovalEscalation(models.Model):
    """
    Lịch sử từng lần escalate của 1 phiếu phê duyệt.
    Bất biến sau khi tạo — không cho sửa/xóa.
    """
    _name = 'octa.approval.escalation'
    _description = 'Lịch sử escalate phiếu phê duyệt'
    _order = 'create_date asc'

    approval_id = fields.Many2one(
        'octa.approval', 'Phiếu phê duyệt',
        required=True, ondelete='cascade', readonly=True,
    )
    from_role = fields.Selection([
        ('lead',  'Lead'),
        ('tdabg', 'TDABG'),
        ('ppkd',  'PPKD'),
        ('tpkd',  'TPKD'),
    ], string='Từ tầng', required=True, readonly=True)

    to_role = fields.Selection([
        ('tdabg', 'TDABG'),
        ('ppkd',  'PPKD'),
        ('tpkd',  'TPKD'),
        ('gd',    'Giám đốc'),
    ], string='Lên tầng', required=True, readonly=True)

    escalated_by = fields.Many2one(
        'res.users', 'Người chuyển',
        required=True, readonly=True,
        default=lambda self: self.env.uid,
    )
    escalated_at = fields.Datetime(
        'Thời điểm', required=True,
        readonly=True, default=fields.Datetime.now,
    )
    reason = fields.Text('Lý do', required=True, readonly=True)

    def write(self, vals):
        raise models.ValidationError('Không được sửa lịch sử escalate.')

    def unlink(self):
        raise models.ValidationError('Không được xóa lịch sử escalate.')