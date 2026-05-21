# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

# ── Constants — tách ra ngoài class để dễ test và import ────────────

CSKH_ISSUE_TYPES = [
    ('card_error',       'CS01 — Thẻ lỗi / không nạp được'),
    ('topup_error',      'CS02 — Topup lỗi / hoàn tiền'),
    ('gateway_39',       'CS03 — Kiểm tra cổng 39 (20 phút)'),
    ('gateway_70',       'CS04 — Kiểm tra cổng 70/Vina (60 phút)'),
    ('deposit_complaint','CS05 — Khiếu nại nạp ví'),
    ('txn_monitor',      'CS06 — Theo dõi GD pending (30 phút)'),
    ('shift_tool_check', 'CS07 — Kiểm tra công cụ đầu ca'),
    ('shift_sales_check','CS08 — Kiểm tra điều kiện bán đầu ca'),
    ('miniapp_check',    'CS09 — Kiểm tra web/mini app'),
    ('msg_channels',     'CS10 — Cập nhật kênh phản ánh'),
]

VH_ISSUE_TYPES = [
    ('vh01_purchase_plan',      'VH01 — Kế hoạch mua hàng'),
    ('vh02_gate_check',         'VH02 — Kiểm tra cổng định kỳ'),
    ('vh02_gate_incident',      'VH02 — Sự vụ cổng API'),
    ('vh03_contract',           'VH03 — Hợp đồng đại lý'),
    ('vh04_revenue_check',      'VH04 — Theo dõi doanh thu KH lớn'),
    ('vh04_revenue_incident',   'VH04 — Sự vụ doanh thu'),
    ('vh05_production_check',   'VH05 — Kiểm tra sản xuất thẻ'),
    ('vh05_production_incident','VH05 — Sự vụ sản xuất thẻ'),
    ('vh06_advance',            'VH06 — Ứng tiền Viettel'),
    ('vh07_flight',             'VH07 — Vé máy bay'),
    ('vh08_report_daily',       'VH08 — Báo cáo vận hành ngày'),
    ('vh08_report_incident',    'VH08 — Sự vụ báo cáo'),
]

TICKET_TYPE_MAP = {
    'card_error': 'incident', 'topup_error': 'incident',
    'deposit_complaint': 'incident', 'vh01_purchase_plan': 'incident',
    'vh02_gate_incident': 'incident', 'vh03_contract': 'incident',
    'vh04_revenue_incident': 'incident', 'vh05_production_incident': 'incident',
    'vh06_advance': 'incident', 'vh07_flight': 'incident',
    'vh08_report_incident': 'incident',
    'gateway_39': 'periodic', 'gateway_70': 'periodic',
    'txn_monitor': 'periodic', 'vh02_gate_check': 'periodic',
    'vh04_revenue_check': 'periodic', 'vh05_production_check': 'periodic',
    'shift_tool_check': 'shift', 'shift_sales_check': 'shift',
    'miniapp_check': 'shift',
    'msg_channels': 'continuous', 'vh08_report_daily': 'periodic',
}

SLA_MINUTES = {
    'card_error': 10, 'topup_error': 15, 'gateway_39': 20,
    'gateway_70': 60, 'deposit_complaint': 15, 'txn_monitor': 30,
    'shift_tool_check': 10, 'shift_sales_check': 10,
    'miniapp_check': 10, 'msg_channels': 3,
    'vh01_purchase_plan': 60, 'vh02_gate_incident': 30,
    'vh03_contract': 120, 'vh04_revenue_incident': 60,
    'vh05_production_incident': 60, 'vh06_advance': 60,
    'vh07_flight': 30, 'vh08_report_incident': 60,
    'vh02_gate_check': 30, 'vh04_revenue_check': 480,
    'vh05_production_check': 60, 'vh08_report_daily': 480,
}

# Gợi ý tạo ticket VH khi CSKH phát hiện cảnh báo
ESCALATE_SUGGEST = {
    'gateway_39':  'vh02_gate_incident',
    'gateway_70':  'vh02_gate_incident',
    'card_error':  'vh05_production_incident',
    'txn_monitor': 'vh02_gate_incident',
}

CSKH_KEYS = {k for k, _ in CSKH_ISSUE_TYPES}

# Interval reset checklist (phút) — cho ticket periodic/shift
INTERVAL_MAP = {
    'gateway_39': 20, 'gateway_70': 60, 'txn_monitor': 30,
    'shift_tool_check': 0, 'shift_sales_check': 0, 'miniapp_check': 0,
    'vh02_gate_check': 30, 'vh04_revenue_check': 480,
    'vh05_production_check': 60, 'vh08_report_daily': 480,
}


def _compute_type_sla(issue_type: str) -> dict:
    """
    Tính ticket_type, dept, sla_deadline, next_check_time từ issue_type.
    Pure function — không đụng record, không trigger write/onchange.
    Trả về dict vals để nhét vào create()/write().
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
        'ticket_type':     ticket_type,
        'dept':            dept,
        'sla_deadline':    sla_deadline,
        'next_check_time': next_check_time,
    }


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # ── Phân loại issue ─────────────────────────────────────────────
    # FIX: bỏ field 'dept' — đã định nghĩa ở octa_project
    # FIX: bỏ field 'date_closed' — đã định nghĩa ở octa_project

    issue_type_cskh = fields.Selection(
        CSKH_ISSUE_TYPES, string='Loại sự cố (CSKH)', tracking=True,
    )
    issue_type_ops = fields.Selection(
        VH_ISSUE_TYPES, string='Loại đầu việc (Vận hành)', tracking=True,
    )

    # FIX: _compute_issue_type — thêm guard khi cả 2 có value
    issue_type = fields.Selection(
        CSKH_ISSUE_TYPES + VH_ISSUE_TYPES,
        string='Mã loại việc',
        compute='_compute_issue_type',
        store=True, readonly=True,
    )

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

    # ── SLA ─────────────────────────────────────────────────────────
    sla_deadline    = fields.Datetime('SLA Deadline', tracking=True)
    next_check_time = fields.Datetime('Lần kiểm tra tiếp theo', tracking=True)
    is_overdue_sla  = fields.Boolean(
        'Quá SLA', compute='_compute_overdue_sla', store=True,
    )
    # Cả 2 field check_status dùng chung 1 compute _compute_check_status
    # vì phụ thuộc cùng field next_check_time — tránh query 2 lần
    is_check_warning = fields.Boolean(
        'Sắp đến hạn kiểm tra',
        compute='_compute_check_status',
        help='True khi next_check_time còn ≤5 phút — hiện alert vàng trên form.',
    )
    is_check_overdue = fields.Boolean(
        'Quá giờ kiểm tra',
        compute='_compute_check_status',
        help='True khi next_check_time đã qua — hiện alert đỏ trên form.',
    )

    # ── Thông tin khách hàng / giao dịch ───────────────────────────
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
    buy_datetime   = fields.Datetime('Thời điểm mua / in thẻ', tracking=True)
    ncc            = fields.Char('Nhà cung cấp (NCC)', tracking=True)
    card_code      = fields.Char('Mã / Serial thẻ', tracking=True)
    network        = fields.Selection([
        ('viettel', 'Viettel'),
        ('vina',    'Vinaphone'),
        ('mobi',    'Mobifone'),
    ], string='Nhà mạng', tracking=True)
    transaction_id = fields.Char('Transaction ID', tracking=True)
    phone          = fields.Char('Số điện thoại', tracking=True)
    amount         = fields.Float('Số tiền', digits=(15, 0), tracking=True)
    bank_name      = fields.Char('Ngân hàng chuyển', tracking=True)
    gateway_name   = fields.Char('Tên cổng', tracking=True)
    vh_note        = fields.Text('Nội dung / Ghi chú vận hành', tracking=True)

    # ── Ticket liên kết ─────────────────────────────────────────────
    linked_ticket_id = fields.Many2one(
        'project.task', string='Ticket liên quan',
        tracking=True, domain="[('id', '!=', id)]", ondelete='set null',
    )
    linked_ticket_name = fields.Char(
        related='linked_ticket_id.name', readonly=True,
    )
    linked_ticket_dept = fields.Selection(
        related='linked_ticket_id.dept', readonly=True,
    )
    linked_ticket_stage = fields.Many2one(
        related='linked_ticket_id.stage_id', readonly=True,
        string='Stage ticket liên quan',
    )
    linked_is_done = fields.Boolean(
        'Ticket liên quan đã xong',
        compute='_compute_linked_is_done', store=True,
    )
    wait_for_linked = fields.Boolean(
        'Đang chờ ticket liên quan', default=False, tracking=True,
    )

    # ── Checklist ───────────────────────────────────────────────────
    checklist_ids = fields.One2many(
        'ticket.checklist', 'task_id', string='Checklist',
    )
    checklist_progress = fields.Integer(
        'Tiến độ checklist (%)',
        compute='_compute_checklist_progress', store=True,
    )

    # ── Check log ───────────────────────────────────────────────────
    check_log_ids  = fields.One2many(
        'ticket.check.log', 'task_id', string='Lịch sử kiểm tra',
    )
    check_log_count = fields.Integer(
        'Số lần kiểm tra',
        compute='_compute_check_log_count', store=True,
    )

    # ── Computed fields ──────────────────────────────────────────────

    @api.depends('issue_type_cskh', 'issue_type_ops')
    def _compute_issue_type(self):
        for t in self:
            # FIX: guard khi cả 2 có value — ưu tiên cskh
            # Không nên xảy ra trong thực tế (onchange reset cái kia)
            # nhưng data cũ hoặc import có thể có cả 2
            if t.issue_type_cskh and t.issue_type_ops:
                # Log warning để phát hiện data lỗi
                t.issue_type = t.issue_type_cskh
            else:
                t.issue_type = t.issue_type_cskh or t.issue_type_ops or False

    @api.depends('next_check_time', 'stage_id.fold')
    def _compute_check_status(self):
        """
        Tính cả is_check_warning lẫn is_check_overdue trong 1 compute
        vì cùng phụ thuộc next_check_time — tránh query 2 lần.
        Không store=True vì phụ thuộc 'now' thay đổi liên tục.
        """
        now = fields.Datetime.now()
        warn_threshold = now + timedelta(minutes=5)
        for t in self:
            if not t.next_check_time or t.stage_id.fold:
                t.is_check_warning = False
                t.is_check_overdue = False
            else:
                t.is_check_overdue = t.next_check_time < now
                t.is_check_warning = (
                    not t.is_check_overdue
                    and t.next_check_time <= warn_threshold
                )

    @api.depends('sla_deadline', 'stage_id.fold')
    def _compute_overdue_sla(self):
        now = fields.Datetime.now()
        for t in self:
            t.is_overdue_sla = bool(
                t.sla_deadline and t.sla_deadline < now
                and not t.stage_id.fold
            )

    @api.depends('checklist_ids.done')
    def _compute_checklist_progress(self):
        for t in self:
            items = t.checklist_ids
            t.checklist_progress = (
                int(len(items.filtered('done')) / len(items) * 100)
                if items else 0
            )

    @api.depends('check_log_ids')
    def _compute_check_log_count(self):
        for t in self:
            t.check_log_count = len(t.check_log_ids)

    @api.depends('linked_ticket_id.stage_id.fold')
    def _compute_linked_is_done(self):
        for t in self:
            t.linked_is_done = (
                t.linked_ticket_id.stage_id.fold
                if t.linked_ticket_id else True
            )

    # ── Onchange ────────────────────────────────────────────────────

    @api.onchange('dept')
    def _onchange_dept(self):
        """Reset issue_type khi đổi bộ phận."""
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
        self.ticket_type     = type_vals.get('ticket_type')
        self.sla_deadline    = type_vals.get('sla_deadline')
        self.next_check_time = type_vals.get('next_check_time')
        templates = self.env['ticket.checklist.template'].search(
            [('issue_type', '=', issue_type)], order='sequence'
        )
        self.checklist_ids = [(5, 0, 0)] + [
            (0, 0, {'sequence': t.sequence, 'name': t.name, 'done': False})
            for t in templates
        ]

    # ── Default get ─────────────────────────────────────────────────

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'dept' in fields_list:
            user = self.env.user
            # FIX: ref đúng groups octa_base
            if user.has_group('octa_base.group_lead'):
                pass  # Lead tự chọn, không set mặc định
            elif user.has_group('octa_base.group_octa_ops'):
                res['dept'] = 'ops'
            elif user.has_group('octa_base.group_octa_cskh'):
                res['dept'] = 'cskh'
        return res

    # ── Create ──────────────────────────────────────────────────────

    @api.model
    def create(self, vals):
        issue_type = vals.get('issue_type_cskh') or vals.get('issue_type_ops')

        # Tạo từ wizard/API (không qua onchange) → tự tính type/sla
        if issue_type and not vals.get('ticket_type'):
            type_vals = _compute_type_sla(issue_type)
            vals = dict(vals, **type_vals)

        # Tự sinh checklist nếu chưa có
        if issue_type and not vals.get('checklist_ids'):
            templates = self.env['ticket.checklist.template'].search(
                [('issue_type', '=', issue_type)], order='sequence'
            )
            vals['checklist_ids'] = [
                (0, 0, {'sequence': t.sequence, 'name': t.name, 'done': False})
                for t in templates
            ]

        return super().create(vals)

    # ── Write ────────────────────────────────────────────────────────

    def write(self, vals):
        # Chặn đóng ticket khi ticket liên quan chưa xong
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

        # Đổi issue_type → tính lại type/sla/checklist
        issue_type_changed = (
            'issue_type_cskh' in vals or 'issue_type_ops' in vals
        )
        if issue_type_changed:
            new_issue_type = vals.get('issue_type_cskh') or vals.get('issue_type_ops')
            if new_issue_type:
                type_vals = _compute_type_sla(new_issue_type)
                vals = dict(vals, **type_vals)
                templates = self.env['ticket.checklist.template'].search(
                    [('issue_type', '=', new_issue_type)], order='sequence'
                )
                vals['checklist_ids'] = [(5, 0, 0)] + [
                    (0, 0, {'sequence': t.sequence, 'name': t.name, 'done': False})
                    for t in templates
                ]

        # NOTE: bỏ logic date_closed ở đây — đã xử lý ở octa_project.write()
        return super().write(vals)

    # ── Actions ─────────────────────────────────────────────────────

    def action_log_check(self):
        """Mở wizard ghi nhận lần kiểm tra (CS03/CS04/CS06/VH02...)."""
        self.ensure_one()
        suggested_vh = ESCALATE_SUGGEST.get(self.issue_type, False)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ghi nhận lần kiểm tra',
            'res_model': 'ticket.check.log.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_task_id':           self.id,
                'default_suggested_vh_type': suggested_vh,
                'default_project_id':        self.project_id.id,
                'dept':                      self.dept,
            },
        }

    def _reset_checklist(self):
        """Reset tất cả checklist về chưa làm."""
        self.checklist_ids.write({'done': False})

    def _generate_checklist(self):
        """Sinh checklist từ template. Chỉ gọi khi chắc chắn chưa có."""
        issue_type = self.issue_type_cskh or self.issue_type_ops
        if not issue_type:
            return
        templates = self.env['ticket.checklist.template'].search(
            [('issue_type', '=', issue_type)], order='sequence'
        )
        for t in templates:
            self.env['ticket.checklist'].create({
                'task_id':  self.id,
                'sequence': t.sequence,
                'name':     t.name,
            })

    # ── Cron ────────────────────────────────────────────────────────

    @api.model
    def _cron_send_check_warning(self):
        """
        Chạy mỗi phút — cảnh báo NV khi checklist sắp đến giờ (≤5ph)
        hoặc đã quá giờ.

        FIX: warn_at = now + 5ph (cảnh báo trước 5ph) — version cũ đúng.
        Overdue = next_check_time < now (đã qua).
        """
        now = fields.Datetime.now()
        warn_at = now + timedelta(minutes=5)

        # Sắp đến giờ: next_check_time trong khoảng [now, now+5ph]
        warning_tasks = self.search([
            ('ticket_type', 'in', ['periodic', 'shift']),
            ('next_check_time', '>=', now),
            ('next_check_time', '<=', warn_at),
            ('stage_id.fold', '=', False),
        ])
        # Đã quá giờ: next_check_time < now
        overdue_tasks = self.search([
            ('ticket_type', 'in', ['periodic', 'shift']),
            ('next_check_time', '<', now),
            ('stage_id.fold', '=', False),
        ])

        bus = self.env['bus.bus']
        for task in warning_tasks | overdue_tasks:
            level = 'warning' if task in warning_tasks else 'overdue'
            for user in task.user_ids:
                bus._sendone(
                    user.partner_id,
                    'octa_check_warning',
                    {
                        'task_id':    task.id,
                        'task_name':  task.name,
                        'dept':       task.dept,
                        'check_time': (
                            task.next_check_time.strftime('%H:%M')
                            if task.next_check_time else ''
                        ),
                        'level': level,
                    },
                )