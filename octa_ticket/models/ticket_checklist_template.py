from odoo import models, fields

class TicketChecklistTemplate(models.Model):
    _name = 'ticket.checklist.template'
    _description = 'Checklist Template theo Issue Type'
    _order = 'issue_type, sequence'

    issue_type = fields.Selection([
        ('card_error',        'CS01 - Khiếu nại thẻ không nạp được'),
        ('topup_error',       'CS02 - Khiếu nại topup lỗi'),
        ('gateway_39',        'CS03 - Theo dõi cổng 39 / hỗn hợp'),
        ('gateway_70',        'CS04 - Cảnh báo tồn kho cổng 70 / Vina'),
        ('deposit_complaint', 'CS05 - Khiếu nại nạp tiền tài khoản Octa'),
        ('txn_monitor',       'CS06 - Kiểm tra giao dịch mua hàng'),
        ('shift_tool_check',  'CS07 - Kiểm tra công cụ đầu ca'),
        ('shift_sales_check', 'CS08 - Kiểm tra điều kiện bán hàng đầu ca'),
        ('miniapp_check',     'CS09 - Kiểm tra web / Mini App'),
        ('msg_channels',      'CS10 - Theo dõi kênh phản ánh khách hàng'),
    ], string='Loại sự cố', required=True)

    sequence = fields.Integer('Thứ tự', default=10)
    name     = fields.Char('Bước thực hiện', required=True)