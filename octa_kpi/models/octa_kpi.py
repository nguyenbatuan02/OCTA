# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta, time
from odoo import models, fields, api


def _period_range(period_type: str, ref: date):
    """Trả (date_from, date_to) là date cho kỳ chứa ngày ref."""
    if period_type == 'day':
        return ref, ref
    if period_type == 'week':
        start = ref - timedelta(days=ref.weekday())
        return start, start + timedelta(days=6)
    # month
    start = ref.replace(day=1)
    if start.month == 12:
        nxt = start.replace(year=start.year + 1, month=1)
    else:
        nxt = start.replace(month=start.month + 1)
    return start, nxt - timedelta(days=1)


class OctaKpi(models.Model):
    """
    Bản ghi KPI theo nhân viên / kỳ (ngày–tuần–tháng).

    Các chỉ số được tính từ project.task (ticket CSKH/VH) và octa.report
    qua action_recompute() hoặc cron _cron_generate_monthly().
    Lưu snapshot để đối chiếu lịch sử và xếp loại A/B/C.

    Ngưỡng KPI (theo lead_cskh.md — Quy chế Thương mại):
        - SLA đúng hạn ≥ 95%
        - FCR (giải quyết lần đầu) ≥ 85%
        - Tỷ lệ tái phát ≤ 5%
    """
    _name = 'octa.kpi'
    _description = 'KPI CSKH & Vận hành'
    _order = 'date_to desc, dept, user_id'

    # Ngưỡng chuẩn — có thể chỉnh khi cần
    SLA_TARGET = 95.0
    FCR_TARGET = 85.0
    REPEAT_LIMIT = 5.0

    user_id = fields.Many2one(
        'res.users', 'Nhân viên', required=True, ondelete='cascade', index=True,
    )
    dept = fields.Selection([
        ('cskh', 'CSKH — Chăm sóc khách hàng'),
        ('ops',  'Vận hành thương mại'),
    ], string='Bộ phận', required=True, index=True)
    period_type = fields.Selection([
        ('day',   'Ngày'),
        ('week',  'Tuần'),
        ('month', 'Tháng'),
    ], string='Kỳ', required=True, default='month', index=True)
    date_from = fields.Date('Từ ngày', required=True, index=True)
    date_to   = fields.Date('Đến ngày', required=True, index=True)

    # ── Sản lượng ───────────────────────────────────────────────────
    ticket_total  = fields.Integer('Tổng ticket', readonly=True)
    ticket_closed = fields.Integer('Đã đóng', readonly=True)
    ticket_open   = fields.Integer('Đang mở', readonly=True)

    # ── SLA / chất lượng ────────────────────────────────────────────
    sla_total       = fields.Integer('Ticket sự vụ đã đóng', readonly=True)
    sla_ontime      = fields.Integer('Đóng đúng SLA', readonly=True)
    sla_ontime_pct  = fields.Float('SLA đúng hạn (%)', readonly=True, digits=(5, 1))
    fcr_count       = fields.Integer('Giải quyết lần đầu', readonly=True)
    fcr_pct         = fields.Float('FCR (%)', readonly=True, digits=(5, 1))
    repeat_count    = fields.Integer('Tái phát', readonly=True)
    repeat_pct      = fields.Float('Tỷ lệ tái phát (%)', readonly=True, digits=(5, 1))
    pending_overdue = fields.Integer('Pending quá hạn', readonly=True)
    avg_score       = fields.Float('Điểm TB checklist', readonly=True, digits=(3, 1))

    # ── Báo cáo ─────────────────────────────────────────────────────
    report_total      = fields.Integer('Báo cáo phải nộp', readonly=True)
    report_ontime     = fields.Integer('Nộp đúng hạn', readonly=True)
    report_ontime_pct = fields.Float('BC đúng hạn (%)', readonly=True, digits=(5, 1))

    # ── Xếp loại ────────────────────────────────────────────────────
    grade = fields.Selection([
        ('a', 'A — Xuất sắc'),
        ('b', 'B — Đạt'),
        ('c', 'C — Cần cải thiện'),
    ], string='Xếp loại', readonly=True, index=True)
    grade_note = fields.Char('Ghi chú xếp loại', readonly=True)

    computed_at = fields.Datetime('Tính lúc', readonly=True)

    _sql_constraints = [
        ('uniq_kpi_period',
         'unique(user_id, dept, period_type, date_from, date_to)',
         'Đã tồn tại KPI cho nhân viên này trong kỳ này.'),
    ]

    def name_get(self):
        labels = {'day': 'Ngày', 'week': 'Tuần', 'month': 'Tháng'}
        res = []
        for r in self:
            res.append((r.id, '%s — %s %s→%s' % (
                r.user_id.name or '?',
                labels.get(r.period_type, ''),
                r.date_from or '', r.date_to or '',
            )))
        return res

    # ── Tính toán ───────────────────────────────────────────────────

    @api.model
    def _compute_metrics(self, user, dept, date_from, date_to):
        """
        Tính toàn bộ chỉ số cho 1 nhân viên trong khoảng [date_from, date_to].
        Trả về dict vals sẵn sàng ghi vào record.
        """
        Task = self.env['project.task'].sudo()
        dt_from = datetime.combine(date_from, time.min)
        dt_to   = datetime.combine(date_to, time.max)

        base = [
            ('user_ids', 'in', [user.id]),
            ('dept', '=', dept),
            ('create_date', '>=', dt_from),
            ('create_date', '<=', dt_to),
        ]
        tasks = Task.search(base)
        closed = tasks.filtered(lambda t: t.stage_id.fold)
        opened = tasks - closed

        incidents_closed = closed.filtered(lambda t: t.ticket_type == 'incident')
        sla_total = len(incidents_closed)
        sla_ontime = len(incidents_closed.filtered(
            lambda t: t.sla_deadline and t.date_closed
            and t.date_closed <= t.sla_deadline
        ))
        fcr_count = len(incidents_closed.filtered(lambda t: t.is_fcr))
        repeat_count = len(tasks.filtered(lambda t: t.is_repeat))

        # Pending quá hạn: ticket đang mở đã quá SLA hoặc quá giờ check
        now = fields.Datetime.now()
        pending_overdue = len(opened.filtered(
            lambda t: (t.sla_deadline and t.sla_deadline < now)
            or (t.next_check_time and t.next_check_time < now)
        ))

        # Điểm TB checklist (manager_score > 0)
        scores = tasks.mapped('checklist_ids').filtered(
            lambda c: c.manager_score
        ).mapped('manager_score')
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        # Báo cáo đúng hạn
        Report = self.env['octa.report'].sudo()
        reports = Report.search([
            ('author_id', '=', user.id),
            ('period_date', '>=', date_from),
            ('period_date', '<=', date_to),
        ])
        report_total = len(reports)
        report_ontime = len(reports.filtered(
            lambda r: r.state in ('submitted', 'approved') and not r.is_overdue
        ))

        def pct(part, whole):
            return round(part / whole * 100, 1) if whole else 0.0

        sla_pct    = pct(sla_ontime, sla_total)
        fcr_pct    = pct(fcr_count, sla_total)
        repeat_pct = pct(repeat_count, len(tasks))
        report_pct = pct(report_ontime, report_total)

        grade, grade_note = self._grade(sla_pct, fcr_pct, repeat_pct, sla_total)

        return {
            'ticket_total':      len(tasks),
            'ticket_closed':     len(closed),
            'ticket_open':       len(opened),
            'sla_total':         sla_total,
            'sla_ontime':        sla_ontime,
            'sla_ontime_pct':    sla_pct,
            'fcr_count':         fcr_count,
            'fcr_pct':           fcr_pct,
            'repeat_count':      repeat_count,
            'repeat_pct':        repeat_pct,
            'pending_overdue':   pending_overdue,
            'avg_score':         avg_score,
            'report_total':      report_total,
            'report_ontime':     report_ontime,
            'report_ontime_pct': report_pct,
            'grade':             grade,
            'grade_note':        grade_note,
            'computed_at':       fields.Datetime.now(),
        }

    @api.model
    def _grade(self, sla_pct, fcr_pct, repeat_pct, sla_total):
        """Xếp loại A/B/C theo ngưỡng chuẩn. Không đủ dữ liệu → chưa xếp."""
        if sla_total == 0:
            return False, 'Chưa đủ dữ liệu ticket sự vụ để xếp loại.'
        if (sla_pct >= self.SLA_TARGET and fcr_pct >= self.FCR_TARGET
                and repeat_pct <= self.REPEAT_LIMIT):
            return 'a', 'Đạt cả 3 ngưỡng: SLA≥95%, FCR≥85%, tái phát≤5%.'
        if sla_pct < 85.0 or repeat_pct > 15.0:
            return 'c', 'SLA<85% hoặc tái phát>15%.'
        return 'b', 'Đạt cơ bản, chưa đạt mức xuất sắc.'

    def action_recompute(self):
        """Nút tính lại KPI cho các bản ghi đang chọn."""
        for r in self:
            r.write(r._compute_metrics(r.user_id, r.dept, r.date_from, r.date_to))
        return True

    # ── Sinh KPI hàng loạt ──────────────────────────────────────────

    @api.model
    def generate_for_period(self, period_type, ref_date=None):
        """
        Sinh / cập nhật KPI cho tất cả nhân viên CSKH & Ops trong kỳ chứa ref_date.
        Gọi từ cron hoặc nút. Trả về recordset các KPI.
        """
        ref_date = ref_date or fields.Date.context_today(self)
        date_from, date_to = _period_range(period_type, ref_date)

        group_dept = [
            ('octa_base.group_octa_cskh', 'cskh'),
            ('octa_base.group_octa_ops',  'ops'),
        ]
        result = self.browse()
        for xml_id, dept in group_dept:
            group = self.env.ref(xml_id, raise_if_not_found=False)
            if not group:
                continue
            for user in group.users.filtered('active'):
                vals = self._compute_metrics(user, dept, date_from, date_to)
                existing = self.search([
                    ('user_id', '=', user.id),
                    ('dept', '=', dept),
                    ('period_type', '=', period_type),
                    ('date_from', '=', date_from),
                    ('date_to', '=', date_to),
                ], limit=1)
                if existing:
                    existing.write(vals)
                    result |= existing
                else:
                    result |= self.create(dict(vals,
                        user_id=user.id, dept=dept, period_type=period_type,
                        date_from=date_from, date_to=date_to,
                    ))
        return result

    @api.model
    def _cron_generate_monthly(self):
        """Cron đầu tháng: chốt KPI tháng trước cho toàn bộ nhân viên."""
        today = fields.Date.context_today(self)
        last_month_end = today.replace(day=1) - timedelta(days=1)
        self.generate_for_period('month', last_month_end)

    @api.model
    def _cron_generate_daily(self):
        """Cron mỗi sáng: chốt KPI ngày hôm trước."""
        yesterday = fields.Date.context_today(self) - timedelta(days=1)
        self.generate_for_period('day', yesterday)
