from odoo import models, fields

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    
    # Người duyệt
    approver_id = fields.Many2one(
        'res.users',
        string='Người duyệt',
        help='Người có thẩm quyền duyệt tasks ở stage này'
    )