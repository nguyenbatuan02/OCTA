# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError

from .octa_report_catalog import ROLE_LABELS, FREQ_LABELS


class OctaReport(models.Model):
    """
    Báo cáo CSKH / Vận hành / Lead / TDABG.

    Loại báo cáo lấy từ octa.report.catalog (nhiều loại mỗi bộ phận).
    Hạn nộp tự tính theo tần suất của catalog.
    Workflow: draft → submitted → approved.
    """
    _name = 'octa.report'
    _description = 'Báo cáo Octa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'period_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char('Tiêu đề', required=True, tracking=True, default='Báo cáo mới')
    catalog_id = fields.Many2one(
        'octa.report.catalog', 'Loại báo cáo', required=True,
        ondelete='restrict', tracking=True, index=True,
    )
    owner_role = fields.Selection(
        related='catalog_id.owner_role', store=True, index=True, string='Bộ phận/vai trò',
    )
    frequency = fields.Selection(
        related='catalog_id.frequency', store=True, string='Tần suất',
    )
    recipients = fields.Char(related='catalog_id.recipients', string='Người nhận')
    scope = fields.Selection(related='catalog_id.scope', store=True, string='Phạm vi')

    author_id = fields.Many2one(
        'res.users', 'Người lập', required=True, tracking=True,
        default=lambda self: self.env.uid, index=True,
    )
    shift = fields.Selection([
        ('morning', 'Ca sáng'), ('afternoon', 'Ca chiều'), ('night', 'Ca tối'),
    ], string='Ca', tracking=True)
    period_date = fields.Date(
        'Ngày/kỳ báo cáo', required=True, index=True,
        default=fields.Date.context_today,
    )

    state = fields.Selection([
        ('draft', 'Nháp'), ('submitted', 'Đã nộp'), ('approved', 'Đã duyệt'),
    ], string='Trạng thái', default='draft', required=True, tracking=True, index=True)
    submitted_at = fields.Datetime('Thời điểm nộp', readonly=True, copy=False)
    approver_id  = fields.Many2one('res.users', 'Người duyệt', readonly=True, copy=False)
    approved_at  = fields.Datetime('Thời điểm duyệt', readonly=True, copy=False)

    deadline   = fields.Datetime('Hạn nộp', compute='_compute_deadline', store=True)
    is_overdue = fields.Boolean('Quá hạn', compute='_compute_is_overdue', store=True)

    kpi_id = fields.Many2one('octa.kpi', 'KPI liên kết', ondelete='set null')

    # ── Nội dung ────────────────────────────────────────────────────
    summary        = fields.Text('Tóm tắt / đầu việc trong kỳ', tracking=True)
    incidents      = fields.Text('Sự cố / ticket nổi bật')
    gate_actions   = fields.Text('Mở / đóng cổng trong kỳ')
    refund_actions = fields.Text('Hoàn tiền / nạp bù trong kỳ')
    handover_note  = fields.Text('Bàn giao / tồn đọng chuyển kỳ sau')
    proposals      = fields.Text('Đề xuất')

    sla_ontime_pct  = fields.Float('SLA đúng hạn (%)', digits=(5, 1))
    fcr_pct         = fields.Float('FCR (%)', digits=(5, 1))
    repeat_pct      = fields.Float('Tái phát (%)', digits=(5, 1))
    pending_overdue = fields.Integer('Pending quá hạn')

    # ── Compute ─────────────────────────────────────────────────────

    @api.depends('catalog_id', 'period_date', 'create_date')
    def _compute_deadline(self):
        for r in self:
            if r.catalog_id and r.period_date:
                r.deadline = r.catalog_id.compute_deadline(r.period_date, r.create_date)
            else:
                r.deadline = False

    @api.depends('deadline', 'state', 'submitted_at')
    def _compute_is_overdue(self):
        now = fields.Datetime.now()
        for r in self:
            if not r.deadline:
                r.is_overdue = False
            elif r.state == 'draft':
                r.is_overdue = now > r.deadline
            else:
                r.is_overdue = bool(r.submitted_at and r.submitted_at > r.deadline)

    @api.onchange('catalog_id')
    def _onchange_catalog(self):
        if self.catalog_id and (not self.name or self.name == 'Báo cáo mới'):
            self.name = '%s — %s' % (self.catalog_id.name, self.period_date or '')

    # ── Workflow ────────────────────────────────────────────────────

    def action_submit(self):
        for r in self:
            if r.state != 'draft':
                raise UserError('Chỉ nộp được báo cáo ở trạng thái Nháp.')
            if not r.summary:
                raise UserError('Phải nhập "Tóm tắt / đầu việc trong kỳ" trước khi nộp.')
            r.write({'state': 'submitted', 'submitted_at': fields.Datetime.now()})
            r._notify_approver()
            r._log('write', 'Nộp báo cáo %s' % r.name)
        return True

    def action_approve(self):
        for r in self:
            if r.state != 'submitted':
                raise UserError('Chỉ duyệt được báo cáo đã nộp.')
            if r.author_id.id == self.env.uid:
                raise UserError('Không được tự duyệt báo cáo của chính mình (SoD).')
            r.write({
                'state': 'approved',
                'approver_id': self.env.uid,
                'approved_at': fields.Datetime.now(),
            })
            r._log('approve', 'Duyệt báo cáo %s' % r.name)
        return True

    def action_reset_draft(self):
        for r in self:
            if r.state == 'approved':
                raise UserError('Báo cáo đã duyệt không thể trả về Nháp.')
            r.write({'state': 'draft', 'submitted_at': False})
        return True

    def action_fill_from_kpi(self):
        """Lấy số liệu SLA/FCR/tái phát từ KPI cùng người & kỳ (nếu module KPI có)."""
        if 'octa.kpi' not in self.env:
            raise UserError('Module KPI chưa được cài đặt.')
        for r in self:
            kpi = r.kpi_id or self.env['octa.kpi'].sudo().search([
                ('user_id', '=', r.author_id.id),
                ('date_from', '<=', r.period_date),
                ('date_to', '>=', r.period_date),
            ], limit=1)
            if kpi:
                r.write({
                    'kpi_id': kpi.id,
                    'sla_ontime_pct': kpi.sla_ontime_pct,
                    'fcr_pct': kpi.fcr_pct,
                    'repeat_pct': kpi.repeat_pct,
                    'pending_overdue': kpi.pending_overdue,
                })
        return True

    # ── Helpers ─────────────────────────────────────────────────────

    def _notify_approver(self):
        self.ensure_one()
        group = self.env.ref('octa_base.group_tdabg', raise_if_not_found=False)
        if not group:
            return
        for user in group.users.filtered(lambda u: u.active and u.id != self.author_id.id):
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=user.id,
                summary='Duyệt báo cáo: %s' % self.name,
            )

    def _log(self, action_type, reason):
        self.ensure_one()
        self.env['octa.audit.log'].log_action(
            action_type=action_type,
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            reason=reason,
            scope_tag=self.scope or 'bigtel',
        )

    # ── Cron nhắc hạn nộp ───────────────────────────────────────────

    @api.model
    def _cron_report_reminder(self):
        now = fields.Datetime.now()
        soon = now + timedelta(hours=1)
        drafts = self.sudo().search([('state', '=', 'draft'), ('deadline', '!=', False)])
        bus = self.env['bus.bus']
        for r in drafts:
            if r.deadline > soon:
                continue
            level = 'overdue' if r.deadline < now else 'warning'
            bus._sendone(
                r.author_id.partner_id,
                'octa_report_reminder',
                {
                    'report_id': r.id,
                    'name': r.name,
                    'deadline': r.deadline.strftime('%H:%M %d/%m'),
                    'level': level,
                },
            )

    # ══════════════════════════════════════════════════════════════
    #  API cho OWL dashboard
    # ══════════════════════════════════════════════════════════════

    @api.model
    def get_report_dashboard(self):
        """Số liệu tổng quan cho dashboard báo cáo (theo record rule của user)."""
        reports = self.search([])
        roles = []
        for role in ('cskh', 'ops', 'lead', 'tdabg'):
            grp = reports.filtered(lambda r: r.owner_role == role)
            if not grp:
                continue
            roles.append({
                'role':      role,
                'label':     ROLE_LABELS.get(role, role),
                'total':     len(grp),
                'draft':     len(grp.filtered(lambda r: r.state == 'draft')),
                'submitted': len(grp.filtered(lambda r: r.state == 'submitted')),
                'approved':  len(grp.filtered(lambda r: r.state == 'approved')),
                'overdue':   len(grp.filtered(lambda r: r.is_overdue)),
            })

        catalog = self.env['octa.report.catalog'].search([('active', '=', True)])
        catalog_data = [{
            'id':            c.id,
            'code':          c.code,
            'name':          c.name,
            'owner_role':    c.owner_role,
            'role_label':    ROLE_LABELS.get(c.owner_role, c.owner_role),
            'frequency':     c.frequency,
            'freq_label':    FREQ_LABELS.get(c.frequency, c.frequency),
            'deadline_note': c.deadline_note or '',
        } for c in catalog]

        return {
            'summary': {
                'total':     len(reports),
                'draft':     len(reports.filtered(lambda r: r.state == 'draft')),
                'submitted': len(reports.filtered(lambda r: r.state == 'submitted')),
                'overdue':   len(reports.filtered(lambda r: r.is_overdue)),
            },
            'roles':   roles,
            'catalog': catalog_data,
        }

    @api.model
    def get_report_list(self, state_filter='all'):
        domain = []
        if state_filter in ('draft', 'submitted', 'approved'):
            domain = [('state', '=', state_filter)]
        elif state_filter == 'overdue':
            domain = [('is_overdue', '=', True)]
        reports = self.search(domain, limit=100)
        return [{
            'id':          r.id,
            'name':        r.name,
            'catalog':     r.catalog_id.name,
            'role_label':  ROLE_LABELS.get(r.owner_role, ''),
            'freq_label':  FREQ_LABELS.get(r.frequency, ''),
            'period_date': fields.Date.to_string(r.period_date) if r.period_date else '',
            'deadline':    fields.Datetime.to_string(r.deadline) if r.deadline else '',
            'state':       r.state,
            'is_overdue':  r.is_overdue,
            'author':      r.author_id.name,
        } for r in reports]

    @api.model
    def create_from_catalog(self, catalog_id):
        """Tạo nhanh 1 báo cáo nháp từ 1 loại catalog → mở form."""
        cat = self.env['octa.report.catalog'].browse(catalog_id)
        rec = self.create({
            'catalog_id': cat.id,
            'name': '%s — %s' % (cat.name, fields.Date.context_today(self)),
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'octa.report',
            'res_id': rec.id,
            'views': [[False, 'form']],
            'target': 'current',
        }
