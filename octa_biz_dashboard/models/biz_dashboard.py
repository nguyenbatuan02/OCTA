# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta, time
from odoo import models, fields, api


class OctaBizDashboard(models.Model):
    """
    Dashboard điều hành Octa — gom các trục lõi từ dữ liệu sẵn có:
    Vận hành, Ranh đỏ, NCC, Đại lý, Cổng/API/Tồn kho, Công nợ, CSKH & Ticket, KPI.

    1 component tham số hóa theo scope:
        - Lead / TDABG → chỉ Bigtel
        - PPKD / TPKD  → tất cả (Bigtel + BigM + UTV)

    Backend dùng sudo() + lọc scope theo role để tránh AccessError khi
    role thấp không có quyền đọc trực tiếp octa.gateway / res.partner.
    Phần Doanh thu/SL và Tài chính thương mại KHÔNG có ở đây vì hệ thống
    chưa có model doanh thu/deal (DB-01, DB-08, DB-PP-08, DB-KD-09).
    """
    _name = 'octa.biz.dashboard'
    _description = 'Dashboard điều hành Octa'

    name = fields.Char(default='Biz Dashboard')

    # ── Scope theo role ─────────────────────────────────────────────

    @api.model
    def _allowed_scopes(self):
        role = self.env['octa.approval.config'].sudo().get_role_for_user()
        if role in ('ppkd', 'tpkd'):
            return ['bigtel', 'bigm', 'utv']
        return ['bigtel']

    @api.model
    def _month_range(self):
        today = fields.Date.context_today(self)
        start = today.replace(day=1)
        return start, today

    # ── API cho OWL ─────────────────────────────────────────────────

    # Danh sách dashboard theo từng vị trí (đúng mã DB trong tài liệu).
    # key = section render trong OWL; available=False → placeholder "chưa có dữ liệu".
    _MENU_BY_ROLE = {
        'tdabg': [
            ('DB-BT-01', 'Vận hành Bigtel ngày', 'ops', True),
            ('DB-BT-02', 'Ranh đỏ Bigtel', 'red', True),
            ('DB-BT-03', 'NCC Bigtel', 'ncc', True),
            ('DB-BT-04', 'Đại lý Bigtel', 'agent', True),
            ('DB-BT-05', 'Cổng / API / Tồn kho', 'gateway', True),
            ('DB-BT-06', 'Công nợ Bigtel', 'debt', True),
            ('DB-BT-07', 'CSKH & Ticket', 'ticket', True),
            ('DB-BT-08', 'Doanh thu theo cơ cấu SP', 'revenue', False),
            ('DB-BT-09', 'KPI nhóm Bigtel', 'kpi', True),
        ],
        'ppkd': [
            ('DB-PP-01', 'Bigtel ngày (realtime)', 'ops', True),
            ('DB-PP-02', 'Ranh đỏ Bigtel', 'red', True),
            ('DB-PP-03', 'NCC Bigtel', 'ncc', True),
            ('DB-PP-04', 'Đại lý / KH Bigtel', 'agent', True),
            ('DB-PP-05', 'Công nợ Bigtel', 'debt', True),
            ('DB-PP-06', 'Cổng / API / Tồn kho', 'gateway', True),
            ('DB-PP-07', 'CSKH & Ticket', 'ticket', True),
            ('DB-PP-08', 'Mảng TC lớp TM', 'finance', False),
            ('DB-PP-09', 'KPI nhân sự Bigtel', 'kpi', True),
            ('DB-PP-10', 'Tổng KD (view-only)', 'total_kd', False),
        ],
        'tpkd': [
            ('DB-KD-01', 'Điều hành KD ngày', 'ops', True),
            ('DB-KD-02', 'Ranh đỏ', 'red', True),
            ('DB-KD-03', 'NCC', 'ncc', True),
            ('DB-KD-04', 'Đại lý / KH', 'agent', True),
            ('DB-KD-05', 'Công nợ', 'debt', True),
            ('DB-KD-06', 'Cổng / API / Tồn kho', 'gateway', True),
            ('DB-KD-07', 'CSKH & Ticket', 'ticket', True),
            ('DB-KD-08', 'KPI Nhân sự Phòng KD', 'kpi', True),
            ('DB-KD-09', 'Tài chính thương mại', 'finance', False),
        ],
        'lead': [
            ('', 'Vận hành tổng quan', 'ops', True),
            ('', 'Ranh đỏ', 'red', True),
            ('', 'Cổng / API / Tồn kho', 'gateway', True),
            ('', 'CSKH & Ticket', 'ticket', True),
            ('', 'KPI nhóm', 'kpi', True),
        ],
    }

    @api.model
    def _menu_for_role(self, role):
        menu = self._MENU_BY_ROLE.get(role) or self._MENU_BY_ROLE['lead']
        return [{'code': c, 'name': n, 'key': k, 'available': a}
                for (c, n, k, a) in menu]

    @api.model
    def get_biz_dashboard(self):
        scopes = self._allowed_scopes()
        role = self.env['octa.approval.config'].sudo().get_role_for_user()
        if role not in self._MENU_BY_ROLE:
            role = 'lead'
        return {
            'role': role,
            'menu': self._menu_for_role(role),
            'scope_label': 'Toàn KD (Bigtel + BigM + UTV)'
                           if len(scopes) > 1 else 'Bigtel',
            'ops':      self._section_ops(scopes),
            'red_lines': self._section_red_lines(scopes),
            'gateways': self._section_gateways(scopes),
            'ncc':      self._section_ncc(scopes),
            'agents':   self._section_agents(scopes),
            'debt':     self._section_debt(scopes),
            'ticket':   self._section_ticket(scopes),
            'kpi':      self._section_kpi(),
        }

    # ── Vận hành tổng quan ──────────────────────────────────────────

    @api.model
    def _section_ops(self, scopes):
        Task = self.env['project.task'].sudo()
        Gate = self.env['octa.gateway'].sudo()
        today = fields.Date.context_today(self)
        dt_from = datetime.combine(today, time.min)
        now = fields.Datetime.now()

        tdomain = [('scope', 'in', scopes), ('dept', 'in', ['cskh', 'ops'])]
        new_today = Task.search_count(tdomain + [('create_date', '>=', dt_from)])
        open_tasks = Task.search(tdomain + [('stage_id.fold', '=', False)])
        pending_overdue = len(open_tasks.filtered(
            lambda t: (t.sla_deadline and t.sla_deadline < now)
            or (t.next_check_time and t.next_check_time < now)
        ))
        handover_pending = Task.search_count(
            tdomain + [('is_handover_pending', '=', True)]
        )
        gates = Gate.search([('scope', 'in', scopes)])
        return {
            'new_today':        new_today,
            'open':             len(open_tasks),
            'pending_overdue':  pending_overdue,
            'handover_pending': handover_pending,
            'gate_locked':      len(gates.filtered(lambda g: g.state == 'locked')),
            'gate_error':       len(gates.filtered(lambda g: g.state in ('warning', 'closed'))),
        }

    # ── Ranh đỏ ─────────────────────────────────────────────────────

    @api.model
    def _section_red_lines(self, scopes):
        Gate = self.env['octa.gateway'].sudo()
        Partner = self.env['res.partner'].sudo()
        items = []
        for g in Gate.search([('scope', 'in', scopes), ('state', '=', 'locked')]):
            items.append({
                'type': 'gateway', 'level': 'red',
                'name': 'Cổng khóa tự động: %s' % g.name,
                'detail': '%d lỗi liên tiếp' % g.error_count,
                'time': fields.Datetime.to_string(g.auto_locked_at) if g.auto_locked_at else '',
            })
        pdomain = [('scope', 'in', scopes + ['all'])]
        for p in Partner.search(pdomain + [('is_debt_overlimit', '=', True)]):
            items.append({
                'type': 'debt', 'level': 'red',
                'name': 'Công nợ vượt hạn mức: %s' % p.name,
                'detail': '%.0f / %.0f VNĐ' % (p.current_debt, p.debt_limit),
                'time': '',
            })
        for p in Partner.search(pdomain + [('is_concentration_warning', '=', True)]):
            items.append({
                'type': 'concentration', 'level': 'amber',
                'name': 'Tập trung NCC: %s' % p.name,
                'detail': '%.1f%% sản lượng' % p.ncc_concentration_pct,
                'time': '',
            })
        for p in Partner.search(pdomain + [('is_contract_expiring', '=', True)]):
            items.append({
                'type': 'contract', 'level': 'amber',
                'name': 'HĐ sắp hết hạn: %s' % p.name,
                'detail': 'Đến %s' % (p.contract_end or ''),
                'time': '',
            })
        return {'count': len(items), 'items': items}

    # ── Cổng / API / Tồn kho ────────────────────────────────────────

    @api.model
    def _section_gateways(self, scopes):
        Gate = self.env['octa.gateway'].sudo()
        rows = []
        for g in Gate.search([('scope', 'in', scopes)], order='state desc, name'):
            rows.append({
                'id': g.id, 'name': g.name, 'code': g.code or '',
                'state': g.state,
                'success_rate': round(g.success_rate, 1),
                'api_balance': g.api_balance,
                'balance_low': g.is_balance_low,
                'error_count': g.error_count,
            })
        return {'count': len(rows), 'rows': rows}

    # ── NCC ─────────────────────────────────────────────────────────

    @api.model
    def _section_ncc(self, scopes):
        Partner = self.env['res.partner'].sudo()
        rows = []
        domain = [('octa_partner_type', 'in', ['ncc', 'both']),
                  ('scope', 'in', scopes + ['all'])]
        for p in Partner.search(domain, order='ncc_concentration_pct desc'):
            rows.append({
                'id': p.id, 'name': p.name,
                'success_rate': round(p.ncc_success_rate, 1),
                'error_rate': round(p.ncc_error_rate, 1),
                'concentration': round(p.ncc_concentration_pct, 1),
                'debt': p.current_debt,
                'warn': p.is_concentration_warning,
            })
        return {'count': len(rows), 'rows': rows}

    # ── Đại lý ──────────────────────────────────────────────────────

    @api.model
    def _section_agents(self, scopes):
        Partner = self.env['res.partner'].sudo()
        rows = []
        domain = [('octa_partner_type', 'in', ['agent', 'both']),
                  ('scope', 'in', scopes + ['all'])]
        grade_lbl = {'a': 'A', 'b': 'B', 'c': 'C'}
        for p in Partner.search(domain, order='current_debt desc'):
            rows.append({
                'id': p.id, 'name': p.name,
                'grade': grade_lbl.get(p.agent_grade, '—'),
                'debt': p.current_debt,
                'debt_limit': p.debt_limit,
                'usage': round(p.debt_usage_pct, 1),
                'overlimit': p.is_debt_overlimit,
            })
        return {'count': len(rows), 'rows': rows}

    # ── Công nợ ─────────────────────────────────────────────────────

    @api.model
    def _section_debt(self, scopes):
        Partner = self.env['res.partner'].sudo()
        domain = [('scope', 'in', scopes + ['all'])]
        ncc = Partner.search(domain + [('octa_partner_type', 'in', ['ncc', 'both'])])
        agent = Partner.search(domain + [('octa_partner_type', 'in', ['agent', 'both'])])
        overlimit = Partner.search(domain + [('is_debt_overlimit', '=', True)])
        return {
            'payable':   sum(ncc.mapped('current_debt')),     # phải trả NCC
            'receivable': sum(agent.mapped('current_debt')),  # phải thu đại lý
            'overlimit_count': len(overlimit),
            'overlimit': [{'name': p.name, 'debt': p.current_debt,
                           'limit': p.debt_limit} for p in overlimit],
        }

    # ── CSKH & Ticket ───────────────────────────────────────────────

    @api.model
    def _section_ticket(self, scopes):
        Task = self.env['project.task'].sudo()
        start, today = self._month_range()
        dt_from = datetime.combine(start, time.min)
        dt_to = datetime.combine(today, time.max)
        base = [('scope', 'in', scopes), ('dept', 'in', ['cskh', 'ops']),
                ('create_date', '>=', dt_from), ('create_date', '<=', dt_to)]
        tasks = Task.search(base)
        closed = tasks.filtered(lambda t: t.stage_id.fold)
        opened = tasks - closed
        inc_closed = closed.filtered(lambda t: t.ticket_type == 'incident')

        def pct(a, b):
            return round(a / b * 100, 1) if b else 0.0

        sla_ontime = len(inc_closed.filtered(
            lambda t: t.sla_deadline and t.date_closed and t.date_closed <= t.sla_deadline))
        fcr = len(inc_closed.filtered(lambda t: t.is_fcr))
        repeat = len(tasks.filtered(lambda t: t.is_repeat))
        return {
            'new': len(tasks), 'open': len(opened), 'closed': len(closed),
            'sla_pct': pct(sla_ontime, len(inc_closed)),
            'fcr_pct': pct(fcr, len(inc_closed)),
            'repeat_pct': pct(repeat, len(tasks)),
        }

    # ── KPI nhóm ────────────────────────────────────────────────────

    @api.model
    def _section_kpi(self):
        if 'octa.kpi' not in self.env:
            return {'available': False}
        Kpi = self.env['octa.kpi'].sudo()
        start, _ = self._month_range()
        kpis = Kpi.search([('period_type', '=', 'month'), ('date_from', '=', start)])
        dist = {'a': 0, 'b': 0, 'c': 0, 'none': 0}
        rows = []
        for k in kpis:
            dist[k.grade or 'none'] += 1
            rows.append({
                'user': k.user_id.name, 'dept': k.dept,
                'sla': k.sla_ontime_pct, 'fcr': k.fcr_pct,
                'repeat': k.repeat_pct, 'grade': (k.grade or '—').upper(),
            })
        return {'available': True, 'dist': dist, 'rows': rows,
                'total': len(kpis)}
