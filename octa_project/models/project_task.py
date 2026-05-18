# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProjectTask(models.Model):
    """
    Extend project.task với các field dùng chung toàn hệ thống Octa.

    Phân tầng rõ ràng:
    - octa_project (file này): field scope, dept, date_closed,
      related_user_ids, supervisor_ids — dùng bởi mọi module
    - octa_ticket: field nghiệp vụ ticket (checklist, SLA, issue_type,
      wizard, cron) — chỉ dùng trong context ticket CSKH/VH
    """
    _inherit = 'project.task'

    scope = fields.Selection([
        ('bigtel', 'Bigtel'),
        ('bigm',   'BigM'),
        ('utv',    'UTV — Ứng tiền Viettel'),
    ], string='Dự án', index=True, default='bigtel',
        help=(
            'Phân loại task theo dự án kinh doanh.\n'
            'Record rules dùng field này để lọc phạm vi truy cập:\n'
            '- TDABG chỉ thấy scope=bigtel\n'
            '- PPKD thấy tất cả\n'
            '- TPKD thấy tất cả'
        ),
    )

    dept = fields.Selection([
        ('cskh', 'CSKH — Chăm sóc khách hàng'),
        ('ops',  'Vận hành thương mại'),
    ], string='Bộ phận', index=True,
        help=(
            'Phân loại task theo bộ phận thực hiện.\n'
            'Record rules dùng field này:\n'
            '- NV CSKH chỉ thấy dept=cskh\n'
            '- NV Vận hành chỉ thấy dept=ops\n'
            '- Lead trở lên thấy cả 2'
        ),
    )

    # ── Thời điểm đóng — dùng chung ────────────────────────────────
    date_closed = fields.Datetime(
        'Thời điểm đóng', readonly=True, index=True,
        help=(
            'Tự động ghi khi task chuyển sang stage fold=True.\n'
            'Tự động xóa khi task mở lại (reopen).'
        ),
    )

    # ── Người liên quan ─────────────────────────────────────────────
    related_user_ids = fields.Many2many(
        'res.users',
        'project_task_related_user_rel',
        'task_id', 'user_id',
        string='Người liên quan',
        help='Những người cần được thông báo nhưng không phải người thực hiện.',
    )

    # ── Người giám sát ──────────────────────────────────────────────
    supervisor_ids = fields.Many2many(
        'res.users',
        'project_task_supervisor_rel',
        'task_id', 'supervisor_id',
        string='Người giám sát',
        help='Người có quyền nghiệm thu và đóng task.',
    )

    # ── Override write ───────────────────────────────────────────────

    def write(self, vals):
        res = super().write(vals)

        if 'stage_id' in vals:
            for task in self:
                if task.stage_id.fold and not task.date_closed:
                    super(ProjectTask, task).write(
                        {'date_closed': fields.Datetime.now()}
                    )
                elif not task.stage_id.fold and task.date_closed:
                    super(ProjectTask, task).write(
                        {'date_closed': False}
                    )

                if task.stage_id.approver_id:
                    approver = task.stage_id.approver_id
                    if approver not in task.user_ids:
                        super(ProjectTask, task).write(
                            {'user_ids': [(4, approver.id)]}
                        )

        return res