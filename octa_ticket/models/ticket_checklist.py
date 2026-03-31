from odoo import models, fields

class TicketChecklist(models.Model):
    _name = 'ticket.checklist'
    _description = 'Checklist xử lý ticket'
    _order = 'sequence, id'

    task_id  = fields.Many2one('project.task', string='Ticket', ondelete='cascade')
    sequence = fields.Integer('Thứ tự', default=10)
    name     = fields.Char('Bước thực hiện', required=True)
    done     = fields.Boolean('Hoàn thành', default=False)

    attachment_ids = fields.Many2many(
        'ir.attachment',
        'ticket_checklist_attachment_rel',
        'checklist_id', 'attachment_id',
        string='Tài liệu đính kèm'
    )
    manager_comment = fields.Text('Nhận xét quản lý')
    manager_score   = fields.Selection([
        ('1', '1 - Kém'),
        ('2', '2 - Trung bình'),
        ('3', '3 - Khá'),
        ('4', '4 - Tốt'),
        ('5', '5 - Xuất sắc'),
    ], string='Điểm đánh giá')