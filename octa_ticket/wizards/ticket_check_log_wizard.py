from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError

# Interval next_check_time sau khi ghi nhận (phút)
INTERVAL_MAP = {
    'gateway_39': 20, 'gateway_70': 60, 'txn_monitor': 30,
    'vh02_gate_check': 30, 'vh04_revenue_check': 480,
    'vh05_production_check': 60, 'vh08_report_daily': 480,
}

# Gợi ý issue_type VH khi CSKH cảnh báo
ESCALATE_SUGGEST = {
    'gateway_39':   'vh02_gate_incident',
    'gateway_70':   'vh02_gate_incident',
    'card_error':   'vh05_production_incident',
    'txn_monitor':  'vh02_gate_incident',
    'msg_channels': 'vh07_flight',
}

# Issue types cho từng bộ phận khi mở sự vụ
# Issue types cho từng bộ phận khi mở sự vụ
CSKH_INCIDENT_TYPES = [
    ('card_error',        'CS01 - Khiếu nại thẻ không nạp được'),
    ('topup_error',       'CS02 - Khiếu nại topup lỗi'),
    ('deposit_complaint', 'CS05 - Khiếu nại nạp tiền tài khoản Octa'),
    ('txn_monitor',       'CS06 - Kiểm tra giao dịch mua hàng'),
]

VH_INCIDENT_TYPES = [
    ('vh02_gate_incident',       'VH02 - Sự vụ điều phối / chuyển luồng cổng'),
    ('vh04_revenue_incident',    'VH04 - Sự vụ cảnh báo / đôn đốc doanh thu'),
    ('vh05_production_incident', 'VH05 - Sự vụ phát sinh sản xuất / lỗi lô'),
    ('vh06_advance',             'VH06 - Dịch vụ ứng tiền Viettel'),
    ('vh07_flight',              'VH07 - Vận hành vé máy bay'),
    ('vh08_report_incident',     'VH08 - Sự vụ số liệu / báo cáo đột xuất'),
]

VH_ESCALATE_TYPES = [
    ('vh02_gate_incident',       'VH02 - Sự vụ điều phối / chuyển luồng cổng'),
    ('vh04_revenue_incident',    'VH04 - Sự vụ cảnh báo / đôn đốc doanh thu'),
    ('vh05_production_incident', 'VH05 - Sự vụ phát sinh sản xuất / lỗi lô'),
    ('vh06_advance',             'VH06 - Dịch vụ ứng tiền Viettel'),
    ('vh07_flight',              'VH07 - Vận hành vé máy bay'),
    ('vh08_report_incident',     'VH08 - Sự vụ số liệu / báo cáo đột xuất'),
    ('vh01_purchase_plan',       'VH01 - Lập kế hoạch / đề xuất mua hàng'),
    ('vh03_contract',            'VH03 - Hợp đồng / hồ sơ / chính sách'),
]


class TicketCheckLogWizard(models.TransientModel):
    _name = 'ticket.check.log.wizard'
    _description = 'Wizard ghi nhận lần kiểm tra'

    task_id = fields.Many2one('project.task', string='Ticket', required=True)

    # ── Kết quả kiểm tra ──────────────────────────────────────

    result = fields.Selection([
        ('normal',   'Bình thường'),
        ('warning',  'Cảnh báo → Tạo ticket Vận hành'),
        ('incident', 'Mở sự vụ → Tạo ticket sự vụ cùng bộ phận'),
    ], string='Kết quả', required=True, default='normal')

    note           = fields.Text('Ghi chú / Chi tiết')
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'wizard_check_log_attachment_rel',
        'wizard_id', 'attachment_id',
        string='Bằng chứng đính kèm'
    )
    reset_checklist = fields.Boolean('Reset checklist sau khi ghi nhận', default=True)

    # ── Warning: tạo ticket VH ─────────────────────────────────

    linked_issue_type = fields.Selection(
        VH_ESCALATE_TYPES,
        string='Loại đầu việc Vận hành',
    )
    linked_ticket_name = fields.Char(
        string='Tiêu đề ticket Vận hành',
        help='Để trống sẽ tự sinh từ tên ticket gốc',
    )

    # ── Incident: tạo ticket sự vụ cùng bộ phận ───────────────

    incident_issue_type_cskh = fields.Selection(
        CSKH_INCIDENT_TYPES,
        string='Loại sự vụ CSKH',
    )
    incident_issue_type_ops = fields.Selection(
        VH_INCIDENT_TYPES,
        string='Loại sự vụ Vận hành',
    )
    incident_ticket_name = fields.Char(
        string='Tiêu đề ticket sự vụ',
        help='Để trống sẽ tự sinh',
    )

    # ── Onchange ─────────────────────────────────────────────

    @api.onchange('result')
    def _onchange_result(self):
        if self.result == 'warning' and self.task_id:
            # Gợi ý loại VH dựa vào issue_type CSKH
            suggested = ESCALATE_SUGGEST.get(self.task_id.issue_type_cskh or '')
            if suggested:
                self.linked_issue_type = suggested
            if not self.linked_ticket_name and self.task_id.name:
                self.linked_ticket_name = f'[VH] Từ {self.task_id.name}'

        elif self.result == 'incident' and self.task_id:
            if self.task_id.dept == 'cskh' and not self.incident_issue_type_cskh:
                # Chỉ gợi ý nếu issue_type hiện tại là incident type
                cskh_incident_keys = {k for k, _ in CSKH_INCIDENT_TYPES}
                current = self.task_id.issue_type_cskh or ''
                self.incident_issue_type_cskh = current if current in cskh_incident_keys else False
            elif self.task_id.dept == 'ops' and not self.incident_issue_type_ops:
                # Map từ periodic → incident tương ứng
                map_to_incident = {
                    'vh02_gate_check':       'vh02_gate_incident',
                    'vh04_revenue_check':    'vh04_revenue_incident',
                    'vh05_production_check': 'vh05_production_incident',
                    'vh08_report_daily':     'vh08_report_incident',
                }
                ops_type = self.task_id.issue_type_ops or ''
                self.incident_issue_type_ops = map_to_incident.get(ops_type, ops_type) or False
            if not self.incident_ticket_name and self.task_id.name:
                self.incident_ticket_name = f'[SỰ VỤ] Từ {self.task_id.name}'

    # ── Confirm ──────────────────────────────────────────────

    def action_confirm(self):
        self.ensure_one()
        task = self.task_id

        # 1. Snapshot checklist
        snapshot = [
            (0, 0, {
                'sequence':       item.sequence,
                'name':           item.name,
                'done':           item.done,
                'attachment_ids': [(6, 0, item.attachment_ids.ids)],
            })
            for item in task.checklist_ids
        ]

        # 2. Tạo check log — result lưu key gốc (normal/warning/incident)
        self.env['ticket.check.log'].create({
            'task_id':                task.id,
            'result':                 self.result,
            'note':                   self.note,
            'attachment_ids':         [(6, 0, self.attachment_ids.ids)],
            'checklist_snapshot_ids': snapshot,
        })

        # 3. Reset checklist
        if self.reset_checklist and task.ticket_type != 'continuous':
            task._reset_checklist()

        # 4. Cập nhật next_check_time
        issue_type = task.issue_type_cskh or task.issue_type_ops
        interval = INTERVAL_MAP.get(issue_type)
        if interval:
            task.next_check_time = fields.Datetime.now() + timedelta(minutes=interval)

        # 5. Tạo ticket theo result
        if self.result == 'warning':
            self._create_warning_ticket(task)
        elif self.result == 'incident':
            self._create_incident_ticket(task)

        return {'type': 'ir.actions.act_window_close'}

    def _create_warning_ticket(self, task):
        """Tạo ticket VH khi cảnh báo."""
        if not self.linked_issue_type:
            raise UserError('Vui lòng chọn loại đầu việc Vận hành.')

        ticket_name = self.linked_ticket_name or f'[VH] Xử lý từ {task.name}'
        vh_note = (
            f'Ticket phối hợp từ CSKH: {task.name}\n'
            f'Kết quả kiểm tra: Cảnh báo\n'
            f'Ghi chú: {self.note or "(không có)"}'
        )

        vh_ticket = self.env['project.task'].create({
            'name':           ticket_name,
            'issue_type_ops': self.linked_issue_type,
            'project_id':     task.project_id.id,
            'vh_note':        vh_note,
        })

        # Link 2 chiều + chờ VH xử lý
        task.write({'linked_ticket_id': vh_ticket.id, 'wait_for_linked': True})
        vh_ticket.write({'linked_ticket_id': task.id})

    def _create_incident_ticket(self, task):
        """Tạo ticket sự vụ cùng bộ phận."""
        dept = task.dept
        if dept == 'cskh':
            if not self.incident_issue_type_cskh:
                raise UserError('Vui lòng chọn loại sự vụ CSKH.')
            new_ticket = self.env['project.task'].create({
                'name':             self.incident_ticket_name or f'[SỰ VỤ] Từ {task.name}',
                'issue_type_cskh':  self.incident_issue_type_cskh,
                'project_id':       task.project_id.id,
                'customer_info':    task.customer_info,
                'source_complaint': task.source_complaint,
                'gateway_name':     task.gateway_name,
                'ncc':              task.ncc,
            })
        elif dept == 'ops':
            if not self.incident_issue_type_ops:
                raise UserError('Vui lòng chọn loại sự vụ Vận hành.')
            new_ticket = self.env['project.task'].create({
                'name':            self.incident_ticket_name or f'[SỰ VỤ] Từ {task.name}',
                'issue_type_ops':  self.incident_issue_type_ops,
                'project_id':      task.project_id.id,
                'vh_note':         f'Sự vụ phát sinh từ checklist: {task.name}\nGhi chú: {self.note or ""}',
                'gateway_name':    task.gateway_name,
            })
        else:
            return

        # Link ticket gốc với ticket sự vụ mới
        task.write({'linked_ticket_id': new_ticket.id})