from odoo import models, fields

class TicketCheckLogItem(models.Model):
    _name = 'ticket.check.log.item'
    _description = 'Chi tiết checklist trong log'
    _order = 'sequence'

    log_id   = fields.Many2one('ticket.check.log', ondelete='cascade')
    sequence = fields.Integer()
    name     = fields.Char('Bước thực hiện', readonly=True)
    done     = fields.Boolean('Hoàn thành', readonly=True)

    attachment_ids = fields.Many2many(
        'ir.attachment',
        'log_item_attachment_rel',
        'item_id', 'attachment_id',
        string='Tài liệu đính kèm',
        readonly=True  
    )
    manager_comment = fields.Text('Nhận xét quản lý')
    manager_score   = fields.Selection([
        ('1', '1 - Kém'),
        ('2', '2 - Trung bình'),
        ('3', '3 - Khá'),
        ('4', '4 - Tốt'),
        ('5', '5 - Xuất sắc'),
    ], string='Điểm')