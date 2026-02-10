from odoo import models, fields, api
from datetime import date, timedelta


class OctaDashboard(models.Model):
    _name = 'octa.dashboard'
    _description = 'OCTA Dashboard'

    name = fields.Char(default='Dashboard')

    @api.model
    def get_dashboard_data(self):
        uid = self.env.uid
        today = date.today()
        Task = self.env['project.task'].sudo()

        # Tôi làm
        my = Task.search([('user_ids', 'in', [uid])])
        my_done = my.filtered(lambda t: t.stage_id.fold)

        # Tôi giao
        assigned = Task.search([('create_uid', '=', uid)])
        assigned_done = assigned.filtered(lambda t: t.stage_id.fold)

        # Tôi giám sát
        sup = Task.search([('supervisor_ids', 'in', [uid])])
        sup_done = sup.filtered(lambda t: t.stage_id.fold)

        # Tôi liên quan
        rel = Task.search([('related_user_ids', 'in', [uid])])
        rel_done = rel.filtered(lambda t: t.stage_id.fold)

        # Đang thực hiện (tôi làm + chưa fold)
        in_progress = my.filtered(lambda t: not t.stage_id.fold)

        # Xử lý hôm nay
        today_tasks = Task.search([
            ('user_ids', 'in', [uid]),
            ('date_deadline', '=', fields.Date.to_string(today)),
            ('stage_id.fold', '=', False),
        ])

        # Xử lý trong tuần
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_tasks = Task.search([
            ('user_ids', 'in', [uid]),
            ('date_deadline', '>=', fields.Date.to_string(week_start)),
            ('date_deadline', '<=', fields.Date.to_string(week_end)),
            ('stage_id.fold', '=', False),
        ])

        # Quá hạn
        overdue = Task.search([
            ('user_ids', 'in', [uid]),
            ('date_deadline', '<', fields.Date.to_string(today)),
            ('stage_id.fold', '=', False),
        ])

        return {
            'my_tasks': {'total': len(my), 'not_done': len(my) - len(my_done), 'done': len(my_done)},
            'assigned': {'total': len(assigned), 'not_done': len(assigned) - len(assigned_done), 'done': len(assigned_done)},
            'supervisor': {'total': len(sup), 'not_done': len(sup) - len(sup_done), 'done': len(sup_done)},
            'related': {'total': len(rel), 'not_done': len(rel) - len(rel_done), 'done': len(rel_done)},
            'in_progress': len(in_progress),
            'today': len(today_tasks),
            'week': len(week_tasks),
            'overdue': len(overdue),
        }

    @api.model
    def get_task_list(self, tab='my_tasks'):
        uid = self.env.uid
        today = date.today()
        domain = []

        if tab == 'my_tasks':
            domain = [('user_ids', 'in', [uid])]
        elif tab == 'assigned':
            domain = [('create_uid', '=', uid)]
        elif tab == 'supervisor':
            domain = [('supervisor_ids', 'in', [uid])]
        elif tab == 'related':
            domain = [('related_user_ids', 'in', [uid])]

        tasks = self.env['project.task'].sudo().search(domain, order='date_deadline asc, id desc')

        result = []
        for t in tasks:
            deadline = t.date_deadline
            if deadline and hasattr(deadline, 'date'):
                deadline = deadline.date()
            result.append({
                'id': t.id,
                'name': t.name,
                'stage_name': t.stage_id.name or '',
                'progress': 100 if t.stage_id.fold else 0,
                'user_names': ', '.join(t.user_ids.mapped('name')),
                'date_deadline': fields.Date.to_string(deadline) if deadline else '',
                'is_overdue': bool(deadline and deadline < today and not t.stage_id.fold),
            })
        return result