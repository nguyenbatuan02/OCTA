from odoo import models, fields, api
from datetime import timedelta

SLA_MINUTES = {
    'card_error':        10,
    'topup_error':       15,
    'gateway_39':        20,
    'gateway_70':        60,
    'deposit_complaint': 15,
    'txn_monitor':       30,
    'shift_tool_check':  10,
    'shift_sales_check': 10,
    'miniapp_check':     10,
    'msg_channels':       3,
}

TICKET_TYPE_MAP = {
    'card_error':        'incident',
    'topup_error':       'incident',
    'deposit_complaint': 'incident',
    'gateway_39':        'periodic',
    'gateway_70':        'periodic',
    'txn_monitor':       'periodic',
    'shift_tool_check':  'shift',
    'shift_sales_check': 'shift',
    'miniapp_check':     'shift',
    'msg_channels':      'continuous',
}

FIELD_VISIBILITY = {
    'card_error':        ['customer_info','buy_datetime','source_complaint','ncc','card_code','network'],
    'topup_error':       ['transaction_id','phone','network','source_complaint'],
    'gateway_39':        ['gateway_name'],
    'gateway_70':        ['gateway_name'],
    'deposit_complaint': ['customer_info','phone','amount','bank_name','buy_datetime'],
    'txn_monitor':       ['transaction_id','ncc','gateway_name'],
    'shift_tool_check':  [],
    'shift_sales_check': [],
    'miniapp_check':     [],
    'msg_channels':      ['source_complaint','customer_info'],
}


class ProjectTask(models.Model):
    _inherit = 'project.task'

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
    ], string='Loại sự cố', tracking=True)

    ticket_type = fields.Selection([
        ('incident',   'Ticket sự vụ'),
        ('periodic',   'Checklist định kỳ'),
        ('shift',      'Checklist đầu ca'),
        ('continuous', 'Liên tục'),
    ], string='Loại ticket', tracking=True)

    source = fields.Selection([
        ('manual', 'Nhập tay'),
        ('api',    'API'),
        ('excel',  'Excel'),
    ], string='Nguồn', default='manual', tracking=True)

    sla_deadline   = fields.Datetime('SLA Deadline', tracking=True)
    is_overdue_sla = fields.Boolean('Quá SLA', compute='_compute_overdue_sla', store=True)

    date_closed = fields.Datetime('Thời gian đóng', readonly=True, tracking=True)

    customer_info    = fields.Char('Thông tin khách hàng', tracking=True)
    source_complaint = fields.Selection([
        ('chat',     'Chat'),
        ('email',    'Email'),
        ('hotline',  'Tổng đài'),
        ('zalo',     'Zalo'),
        ('telegram', 'Telegram'),
        ('tawkto',   'Tawk.to'),
        ('walk_in',  'Trực tiếp'),
    ], string='Nguồn phản ánh', tracking=True)
    buy_datetime = fields.Datetime('Thời điểm mua / in thẻ', tracking=True)
    ncc          = fields.Char('Nhà cung cấp (NCC)', tracking=True)

    #  CS01 
    card_code = fields.Char('Mã / Serial thẻ', tracking=True)
    network   = fields.Selection([
        ('viettel', 'Viettel'),
        ('vina',    'Vinaphone'),
        ('mobi',    'Mobifone'),
    ], string='Nhà mạng', tracking=True)

    #  CS02
    transaction_id = fields.Char('Transaction ID', tracking=True)
    phone          = fields.Char('Số điện thoại', tracking=True)

    #  CS05
    amount    = fields.Float('Số tiền nạp', digits=(15, 0), tracking=True)
    bank_name = fields.Char('Ngân hàng chuyển', tracking=True)

    #  CS03, CS04, CS06
    gateway_name = fields.Char('Tên cổng', tracking=True)

    #  Checklist
    checklist_ids = fields.One2many(
        'ticket.checklist', 'task_id', string='Checklist xử lý'
    )
    checklist_progress = fields.Integer(
        'Tiến độ checklist (%)', compute='_compute_checklist_progress', store=True
    )

    #  Check log (định kỳ)
    check_log_ids  = fields.One2many(
        'ticket.check.log', 'task_id', string='Lịch sử kiểm tra'
    )
    check_log_count = fields.Integer(
        'Số lần kiểm tra', compute='_compute_check_log_count', store=True
    )
    next_check_time = fields.Datetime('Lần check tiếp theo', tracking=True)

    is_check_warning = fields.Boolean('Sắp đến hạn check', compute='_compute_check_status')
    is_check_overdue = fields.Boolean('Quá hạn check', compute='_compute_check_status')

    def _compute_check_status(self):
        now = fields.Datetime.now()
        warn_before = timedelta(minutes=5)
        for t in self:
            if not t.next_check_time or t.stage_id.fold:
                t.is_check_warning = False
                t.is_check_overdue = False
                continue
            t.is_check_overdue = t.next_check_time < now
            t.is_check_warning = (
                not t.is_check_overdue
                and t.next_check_time - warn_before <= now
            )

    def _compute_overdue_sla(self):
        now = fields.Datetime.now()
        for t in self:
            t.is_overdue_sla = bool(
                t.sla_deadline and t.sla_deadline < now and not t.stage_id.fold
            )

    @api.depends('checklist_ids.done')
    def _compute_checklist_progress(self):
        for t in self:
            items = t.checklist_ids
            t.checklist_progress = (
                int(len(items.filtered('done')) / len(items) * 100) if items else 0
            )

    @api.depends('check_log_ids')
    def _compute_check_log_count(self):
        for t in self:
            t.check_log_count = len(t.check_log_ids)

    @api.onchange('issue_type')
    def _onchange_issue_type(self):
        if not self.issue_type:
            self.sla_deadline  = False
            self.next_check_time = False
            self.ticket_type   = False
            self.checklist_ids = [(5, 0, 0)]
            return

        # Set ticket_type
        self.ticket_type = TICKET_TYPE_MAP.get(self.issue_type)
        minutes = SLA_MINUTES.get(self.issue_type)
        # Set SLA
        minutes = SLA_MINUTES.get(self.issue_type)
        if self.ticket_type == 'incident':
            self.sla_deadline    = fields.Datetime.now() + timedelta(minutes=minutes)
            self.next_check_time = False
        else:
            self.sla_deadline    = False   # ← None, không có deadline đóng
            self.next_check_time = fields.Datetime.now() + timedelta(minutes=minutes)
        templates = self.env['ticket.checklist.template'].search(
            [('issue_type', '=', self.issue_type)], order='sequence'
        )
        self.checklist_ids = [(5, 0, 0)]
        self.checklist_ids = [
            (0, 0, {'sequence': t.sequence, 'name': t.name, 'done': False})
            for t in templates
        ]

    def action_log_check(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ghi nhận lần kiểm tra',
            'res_model': 'ticket.check.log.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_task_id': self.id},
        }

    def _reset_checklist(self):
        self.checklist_ids.write({'done': False})

    @api.model
    def create(self, vals):
        task = super().create(vals)
        if task.issue_type:
            task.ticket_type = TICKET_TYPE_MAP.get(task.issue_type)
            minutes = SLA_MINUTES.get(task.issue_type, 0)
            if task.ticket_type == 'incident':
                task.sla_deadline = fields.Datetime.now() + timedelta(minutes=minutes)
            else:
                task.sla_deadline    = False
                task.next_check_time = fields.Datetime.now() + timedelta(minutes=minutes)
            task._generate_checklist()
        return task

    def write(self, vals):
        res = super().write(vals)
        if 'issue_type' in vals:
            for task in self:
                task.ticket_type = TICKET_TYPE_MAP.get(task.issue_type)
                task.checklist_ids.unlink()
                if task.issue_type:
                    task._generate_checklist()
        if 'stage_id' in vals:
            for task in self:
                if task.stage_id.fold and not task.date_closed:
                    task.date_closed = fields.Datetime.now()
                elif not task.stage_id.fold:
                    task.date_closed = False
        return res

    def _generate_checklist(self):
        templates = self.env['ticket.checklist.template'].search(
            [('issue_type', '=', self.issue_type)], order='sequence'
        )
        for t in templates:
            self.env['ticket.checklist'].create({
                'task_id':  self.id,
                'sequence': t.sequence,
                'name':     t.name,
            })

    @api.model
    def _cron_send_check_warning(self):
        now = fields.Datetime.now()
        warn_at = now + timedelta(minutes=5)

        # Sắp đến hạn (trong 5 phút tới)
        warning_tasks = self.search([
            ('ticket_type', '=', 'periodic'),
            ('next_check_time', '>=', now),
            ('next_check_time', '<=', warn_at),
            ('stage_id.fold', '=', False),
        ])

        # Quá hạn
        overdue_tasks = self.search([
            ('ticket_type', '=', 'periodic'),
            ('next_check_time', '<', now),
            ('stage_id.fold', '=', False),
        ])

        bus = self.env['bus.bus']

        for task in warning_tasks:
            for user in task.user_ids:
                bus._sendone(
                    user.partner_id,
                    'octa_check_warning',
                    {
                        'task_id':    task.id,
                        'task_name':  task.name,
                        'check_time': task.next_check_time.strftime('%H:%M'),
                        'level':      'warning',
                    }
                )

        for task in overdue_tasks:
            for user in task.user_ids:
                bus._sendone(
                    user.partner_id,
                    'octa_check_warning',
                    {
                        'task_id':    task.id,
                        'task_name':  task.name,
                        'check_time': task.next_check_time.strftime('%H:%M'),
                        'level':      'overdue',
                    }
                )