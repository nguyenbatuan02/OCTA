from odoo import models, fields


class TicketChecklistTemplate(models.Model):
    _name = 'ticket.checklist.template'
    _description = 'Checklist Template theo Issue Type'
    _order = 'issue_type, sequence'

    issue_type = fields.Selection([
        # CSKH
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
        # Vận hành
        ('vh01_purchase_plan',       'VH01 - Lập kế hoạch / đề xuất mua hàng'),
        ('vh02_gate_check',          'VH02 - Kiểm tra định kỳ trạng thái cổng'),
        ('vh02_gate_incident',       'VH02 - Sự vụ điều phối / chuyển luồng cổng'),
        ('vh03_contract',            'VH03 - Hợp đồng / hồ sơ / chính sách'),
        ('vh04_revenue_check',       'VH04 - Theo dõi định kỳ doanh thu KH lớn'),
        ('vh04_revenue_incident',    'VH04 - Sự vụ cảnh báo / đôn đốc doanh thu'),
        ('vh05_production_check',    'VH05 - Theo dõi định kỳ sản xuất thẻ cào'),
        ('vh05_production_incident', 'VH05 - Sự vụ phát sinh sản xuất / lỗi lô'),
        ('vh06_advance',             'VH06 - Dịch vụ ứng tiền Viettel'),
        ('vh07_flight',              'VH07 - Vận hành vé máy bay'),
        ('vh08_report_daily',        'VH08 - Dashboard / báo cáo ngày'),
        ('vh08_report_incident',     'VH08 - Sự vụ số liệu / báo cáo đột xuất'),
    ], string='Loại sự cố / đầu việc', required=True)

    sequence = fields.Integer('Thứ tự', default=10)
    name     = fields.Char('Bước thực hiện', required=True)