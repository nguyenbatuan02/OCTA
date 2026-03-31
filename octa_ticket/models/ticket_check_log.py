from odoo import models, fields

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
