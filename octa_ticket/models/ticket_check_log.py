from odoo import models, fields, api

class TicketCheckLog(models.Model):
    _name = 'ticket.check.log'
    _description = 'Lịch sử lần kiểm tra định kỳ'
    _order = 'check_time desc'

    task_id    = fields.Many2one('project.task', string='Ticket', ondelete='cascade')
    check_time = fields.Datetime('Thời điểm kiểm tra', default=fields.Datetime.now, readonly=True)
    checked_by = fields.Many2one('res.users', string='Người kiểm tra',
                                  default=lambda self: self.env.uid, readonly=True)
    result = fields.Selection([
        ('normal',   'Bình thường'),
        ('warning',  'Cảnh báo'),
        ('incident', 'Mở sự vụ'),
        ('escalate', 'Báo cấp trên'),
    ], string='Kết quả', required=True)
    note           = fields.Text('Ghi chú / Chi tiết')
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'ticket_check_log_attachment_rel',
        'log_id', 'attachment_id',
        string='Bằng chứng đính kèm'
    )
    checklist_snapshot_ids = fields.One2many(
        'ticket.check.log.item', 'log_id',
        string='Chi tiết checklist'
    )
    # Tổng điểm trung bình tự tính
    avg_score = fields.Float(
        'Điểm TB', compute='_compute_avg_score', store=True
    )

    @api.depends('checklist_snapshot_ids.manager_score')
    def _compute_avg_score(self):
        for log in self:
            scores = log.checklist_snapshot_ids.filtered(
                lambda i: i.manager_score
            ).mapped('manager_score')
            log.avg_score = (
                sum(int(s) for s in scores) / len(scores)
                if scores else 0.0
            )

