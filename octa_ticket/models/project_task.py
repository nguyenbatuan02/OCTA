from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

CSKH_ISSUE_TYPES = [
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
]

VH_ISSUE_TYPES = [
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
]

TICKET_TYPE_MAP = {
    'card_error': 'incident', 'topup_error': 'incident',
    'deposit_complaint': 'incident', 'gateway_39': 'periodic',
    'gateway_70': 'periodic', 'txn_monitor': 'periodic',
    'shift_tool_check': 'shift', 'shift_sales_check': 'shift',
    'miniapp_check': 'shift', 'msg_channels': 'continuous',
    'vh01_purchase_plan': 'incident', 'vh03_contract': 'incident',
    'vh06_advance': 'incident', 'vh07_flight': 'incident',
    'vh02_gate_check': 'periodic', 'vh04_revenue_check': 'periodic',
    'vh05_production_check': 'periodic', 'vh08_report_daily': 'periodic',
    'vh02_gate_incident': 'incident', 'vh04_revenue_incident': 'incident',
    'vh05_production_incident': 'incident', 'vh08_report_incident': 'incident',
}

SLA_MINUTES = {
    'card_error': 10, 'topup_error': 15, 'gateway_39': 20, 'gateway_70': 60,
    'deposit_complaint': 15, 'txn_monitor': 30, 'shift_tool_check': 10,
    'shift_sales_check': 10, 'miniapp_check': 10, 'msg_channels': 3,
    'vh01_purchase_plan': 60, 'vh02_gate_incident': 30, 'vh03_contract': 120,
    'vh04_revenue_incident': 60, 'vh05_production_incident': 60,
    'vh06_advance': 60, 'vh07_flight': 30, 'vh08_report_incident': 60,
    'vh02_gate_check': 30, 'vh04_revenue_check': 480,
    'vh05_production_check': 60, 'vh08_report_daily': 480,
}

ESCALATE_SUGGEST = {
    'gateway_39': 'vh02_gate_incident', 'gateway_70': 'vh02_gate_incident',
    'card_error': 'vh05_production_incident', 'txn_monitor': 'vh02_gate_incident',
    'msg_channels': 'vh07_flight',
}

CSKH_KEYS = {k for k, _ in CSKH_ISSUE_TYPES}


def _compute_type_sla(issue_type):
    """Tính ticket_type, dept, sla_deadline, next_check_time từ issue_type.
    Trả về dict vals — không đụng vào record, không trigger write/onchange.
    """
    if not issue_type:
        return {}
    ticket_type = TICKET_TYPE_MAP.get(issue_type)
    dept = 'cskh' if issue_type in CSKH_KEYS else 'ops'
    minutes = SLA_MINUTES.get(issue_type, 0)
    now = fields.Datetime.now()
    if ticket_type == 'incident':
        sla_deadline    = now + timedelta(minutes=minutes) if minutes else False
        next_check_time = False
    else:
        sla_deadline    = False
        next_check_time = now + timedelta(minutes=minutes) if minutes else False
    return {
        'ticket_type':    ticket_type,
        'dept':           dept,
        'sla_deadline':   sla_deadline,
        'next_check_time': next_check_time,
    }


class ProjectTask(models.Model):
    _inherit = 'project.task'

    dept = fields.Selection([
        ('cskh', 'Chăm sóc khách hàng'),
        ('ops',  'Vận hành thương mại'),
    ], string='Bộ phận', tracking=True)

    issue_type_cskh = fields.Selection(
        CSKH_ISSUE_TYPES, string='Loại sự cố (CSKH)', tracking=True,
    )
    issue_type_ops = fields.Selection(
        VH_ISSUE_TYPES, string='Loại đầu việc (Vận hành)', tracking=True,
    )
    issue_type = fields.Selection(
        CSKH_ISSUE_TYPES + VH_ISSUE_TYPES,
        string='Mã loại việc',
        compute='_compute_issue_type',
        store=True, readonly=True,
    )

    ticket_type = fields.Selection([
        ('incident', 'Ticket sự vụ'), ('periodic', 'Checklist định kỳ'),
        ('shift', 'Checklist đầu ca'), ('continuous', 'Liên tục'),
    ], string='Loại ticket', tracking=True)

    source = fields.Selection([
        ('manual', 'Nhập tay'), ('api', 'API'), ('excel', 'Excel'),
    ], string='Nguồn', default='manual', tracking=True)

    sla_deadline   = fields.Datetime('SLA Deadline', tracking=True)
    is_overdue_sla = fields.Boolean('Quá SLA', compute='_compute_overdue_sla', store=True)
    date_closed    = fields.Datetime('Thời gian đóng', readonly=True, tracking=True)

    customer_info    = fields.Char('Thông tin khách hàng', tracking=True)
    source_complaint = fields.Selection([
        ('chat', 'Chat'), ('email', 'Email'), ('hotline', 'Tổng đài'),
        ('zalo', 'Zalo'), ('telegram', 'Telegram'),
        ('tawkto', 'Tawk.to'), ('walk_in', 'Trực tiếp'),
    ], string='Nguồn phản ánh', tracking=True)
    buy_datetime   = fields.Datetime('Thời điểm mua / in thẻ', tracking=True)
    ncc            = fields.Char('Nhà cung cấp (NCC)', tracking=True)
    card_code      = fields.Char('Mã / Serial thẻ', tracking=True)
    network        = fields.Selection([
        ('viettel', 'Viettel'), ('vina', 'Vinaphone'), ('mobi', 'Mobifone'),
    ], string='Nhà mạng', tracking=True)
    transaction_id = fields.Char('Transaction ID', tracking=True)
    phone          = fields.Char('Số điện thoại', tracking=True)
    amount         = fields.Float('Số tiền', digits=(15, 0), tracking=True)
    bank_name      = fields.Char('Ngân hàng chuyển', tracking=True)
    gateway_name   = fields.Char('Tên cổng', tracking=True)
    vh_note        = fields.Text('Nội dung / Ghi chú vận hành', tracking=True)

    linked_ticket_id = fields.Many2one(
        'project.task', string='Ticket liên quan (bộ phận khác)',
        tracking=True, domain="[('id', '!=', id)]", ondelete='set null',
    )
    linked_ticket_name  = fields.Char(related='linked_ticket_id.name', readonly=True)
    linked_ticket_dept  = fields.Selection(related='linked_ticket_id.dept', readonly=True)
    linked_ticket_stage = fields.Many2one(related='linked_ticket_id.stage_id', readonly=True)
    linked_is_done = fields.Boolean(
        'Ticket liên quan đã xong', compute='_compute_linked_is_done', store=True,
    )
    wait_for_linked = fields.Boolean('Chờ bộ phận khác xử lý', default=False, tracking=True)

    checklist_ids = fields.One2many('ticket.checklist', 'task_id', string='Checklist xử lý')
    checklist_progress = fields.Integer(
        'Tiến độ (%)', compute='_compute_checklist_progress', store=True
    )
    check_log_ids   = fields.One2many('ticket.check.log', 'task_id', string='Lịch sử kiểm tra')
    check_log_count = fields.Integer(
        'Số lần kiểm tra', compute='_compute_check_log_count', store=True
    )
    next_check_time  = fields.Datetime('Lần check tiếp theo', tracking=True)
    is_check_warning = fields.Boolean('Sắp đến hạn check', compute='_compute_check_status')
    is_check_overdue = fields.Boolean('Quá hạn check', compute='_compute_check_status')

    # ── Computes ────────────────────────────────────────────────

    @api.depends('issue_type_cskh', 'issue_type_ops')
    def _compute_issue_type(self):
        for t in self:
            t.issue_type = t.issue_type_cskh or t.issue_type_ops or False

    def _compute_check_status(self):
        now, warn = fields.Datetime.now(), timedelta(minutes=5)
        for t in self:
            if not t.next_check_time or t.stage_id.fold:
                t.is_check_warning = t.is_check_overdue = False
                continue
            t.is_check_overdue = t.next_check_time < now
            t.is_check_warning = not t.is_check_overdue and t.next_check_time - warn <= now

    @api.depends('sla_deadline', 'stage_id.fold')
    def _compute_overdue_sla(self):
        now = fields.Datetime.now()
        for t in self:
            t.is_overdue_sla = bool(t.sla_deadline and t.sla_deadline < now and not t.stage_id.fold)

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

    @api.depends('linked_ticket_id.stage_id.fold')
    def _compute_linked_is_done(self):
        for t in self:
            t.linked_is_done = t.linked_ticket_id.stage_id.fold if t.linked_ticket_id else True

    # ── Onchange ────────────────────────────────────────────────

   

    @api.onchange('dept')
    def _onchange_dept(self):
        self.issue_type_cskh = False
        self.issue_type_ops  = False
        self.ticket_type     = False
        self.sla_deadline    = False
        self.next_check_time = False
        self.checklist_ids   = [(5, 0, 0)]

    @api.onchange('issue_type_cskh')
    def _onchange_issue_type_cskh(self):
        self._apply_issue_type(self.issue_type_cskh)

    @api.onchange('issue_type_ops')
    def _onchange_issue_type_ops(self):
        self._apply_issue_type(self.issue_type_ops)

    def _apply_issue_type(self, issue_type):
        """Chỉ chạy trong onchange — set fields trên UI cache, không chạm DB."""
        if not issue_type:
            self.ticket_type     = False
            self.sla_deadline    = False
            self.next_check_time = False
            self.checklist_ids   = [(5, 0, 0)]
            return
        type_vals = _compute_type_sla(issue_type)
        self.ticket_type     = type_vals['ticket_type']
        self.sla_deadline    = type_vals['sla_deadline']
        self.next_check_time = type_vals['next_check_time']
        templates = self.env['ticket.checklist.template'].search(
            [('issue_type', '=', issue_type)], order='sequence'
        )
        self.checklist_ids = [(5, 0, 0)]
        self.checklist_ids = [
            (0, 0, {'sequence': t.sequence, 'name': t.name, 'done': False})
            for t in templates
        ]

    # ── Actions ─────────────────────────────────────────────────

    def action_log_check(self):
        self.ensure_one()
        suggested_vh = ESCALATE_SUGGEST.get(self.issue_type, False)
        return {
            'type': 'ir.actions.act_window', 'name': 'Ghi nhận lần kiểm tra',
            'res_model': 'ticket.check.log.wizard', 'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_task_id':           self.id,
                'default_suggested_vh_type': suggested_vh,
                'default_project_id':        self.project_id.id,
                'dept':                      self.dept,
            },
        }

    def _reset_checklist(self):
        self.checklist_ids.write({'done': False})

    def _generate_checklist(self):
        """Sinh checklist từ template vào DB. Chỉ gọi khi chắc chắn chưa có."""
        issue_type = self.issue_type_cskh or self.issue_type_ops
        if not issue_type:
            return
        templates = self.env['ticket.checklist.template'].search(
            [('issue_type', '=', issue_type)], order='sequence'
        )
        for t in templates:
            self.env['ticket.checklist'].create({
                'task_id': self.id, 'sequence': t.sequence, 'name': t.name,
            })

    # ── Create ──────────────────────────────────────────────────
    # Chiến lược:
    # - Từ UI form: _onchange đã set ticket_type, dept, sla, checklist_ids vào vals
    #   → super().create(vals) tạo hết trong 1 lần → KHÔNG làm gì thêm
    # - Từ wizard/API: không có ticket_type/dept/checklist trong vals
    #   → tự tính và thêm vào vals TRƯỚC khi gọi super()
    #   → super().create() tạo hết trong 1 lần → KHÔNG làm gì thêm

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'dept' in fields_list:
            user = self.env.user
            if user.has_group('octa_ticket.group_octa_manager'):
                pass  # manager không set mặc định, tự chọn
            elif user.has_group('octa_ticket.group_octa_ops'):
                res['dept'] = 'ops'
            elif user.has_group('octa_ticket.group_octa_cskh'):
                res['dept'] = 'cskh'
        return res

    @api.model
    def create(self, vals):
        issue_type = vals.get('issue_type_cskh') or vals.get('issue_type_ops')

        # Nếu chưa có ticket_type (tạo từ wizard/API) → tính và nhét vào vals
        if issue_type and not vals.get('ticket_type'):
            type_vals = _compute_type_sla(issue_type)
            vals = dict(vals, **type_vals)

        # Nếu chưa có checklist (tạo từ wizard/API) → tạo checklist items và nhét vào vals
        if issue_type and not vals.get('checklist_ids'):
            templates = self.env['ticket.checklist.template'].search(
                [('issue_type', '=', issue_type)], order='sequence'
            )
            vals['checklist_ids'] = [
                (0, 0, {'sequence': t.sequence, 'name': t.name, 'done': False})
                for t in templates
            ]

        return super().create(vals)

    # ── Write ────────────────────────────────────────────────────

    def write(self, vals):
        # Chặn đóng khi linked chưa xong
        if 'stage_id' in vals:
            new_stage = self.env['project.task.type'].browse(vals['stage_id'])
            if new_stage.fold:
                for task in self:
                    if task.wait_for_linked and not task.linked_is_done:
                        raise ValidationError(
                            f'Không thể đóng "{task.name}".\n'
                            f'Ticket liên quan "{task.linked_ticket_id.name}" '
                            f'chưa hoàn thành.'
                        )

        # Khi user edit đổi issue_type trên record đã lưu
        # → xóa checklist cũ, tính lại type/sla, thêm vào vals
        issue_type_changed = 'issue_type_cskh' in vals or 'issue_type_ops' in vals
        if issue_type_changed:
            new_issue_type = vals.get('issue_type_cskh') or vals.get('issue_type_ops')
            if new_issue_type:
                type_vals = _compute_type_sla(new_issue_type)
                vals = dict(vals, **type_vals)
                # Tạo checklist items mới trong vals
                templates = self.env['ticket.checklist.template'].search(
                    [('issue_type', '=', new_issue_type)], order='sequence'
                )
                vals['checklist_ids'] = [(5, 0, 0)] + [
                    (0, 0, {'sequence': t.sequence, 'name': t.name, 'done': False})
                    for t in templates
                ]

        res = super().write(vals)

        # date_closed
        if 'stage_id' in vals:
            for task in self:
                if task.stage_id.fold and not task.date_closed:
                    task.date_closed = fields.Datetime.now()
                elif not task.stage_id.fold:
                    task.date_closed = False

        return res

    # ── Cron ────────────────────────────────────────────────────

    @api.model
    def _cron_send_check_warning(self):
        now, warn_at = fields.Datetime.now(), fields.Datetime.now() + timedelta(minutes=5)
        warning_tasks = self.search([
            ('ticket_type', 'in', ['periodic', 'shift']),
            ('next_check_time', '>=', now),
            ('next_check_time', '<=', warn_at),
            ('stage_id.fold', '=', False),
        ])
        overdue_tasks = self.search([
            ('ticket_type', 'in', ['periodic', 'shift']),
            ('next_check_time', '<', now),
            ('stage_id.fold', '=', False),
        ])
        bus = self.env['bus.bus']
        for task in warning_tasks + overdue_tasks:
            for user in task.user_ids:
                bus._sendone(user.partner_id, 'octa_check_warning', {
                    'task_id':    task.id,
                    'task_name':  task.name,
                    'dept':       task.dept,
                    'check_time': task.next_check_time.strftime('%H:%M'),
                    'level':      'warning' if task in warning_tasks else 'overdue',
                })