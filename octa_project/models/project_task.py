from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    # Người liên quan
    related_user_ids = fields.Many2many(
        'res.users',
        'project_task_related_user_rel',
        'task_id',
        'user_id',
        string='Người liên quan'
    )
    
    # Người giám sát
    supervisor_ids = fields.Many2many(
        'res.users',
        'project_task_supervisor_rel',
        'task_id',
        'supervisor_id',
        string='Người giám sát'
    )