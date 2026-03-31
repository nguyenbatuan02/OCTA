from odoo import models, fields, api
from odoo.exceptions import UserError

class TicketCheckLogWizard(models.TransientModel):
    _name = 'ticket.check.log.wizard'
    _description = 'Wizard ghi nhận lần kiểm tra'

    task_id = fields.Many2one('project.task', string='Ticket', required=True)
    result  = fields.Selection([
        ('normal',   'Bình thường'),
        ('warning',  'Cảnh báo'),
        ('incident', 'Mở sự vụ'),
        ('escalate', 'Báo cấp trên'),
    ], string='Kết quả', required=True, default='normal')
    note = fields.Text('Ghi chú / Chi tiết')
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'wizard_check_log_attachment_rel',
        'wizard_id', 'attachment_id',
        string='Bằng chứng đính kèm'
    )
    reset_checklist = fields.Boolean('Reset checklist sau khi ghi nhận', default=True)

    def action_confirm(self):
        self.ensure_one()
        if not self.task_id:
            raise UserError('Không tìm thấy ticket.')

        # Tạo check log
        self.env['ticket.check.log'].create({
            'task_id':        self.task_id.id,
            'result':         self.result,
            'note':           self.note,
            'attachment_ids': [(6, 0, self.attachment_ids.ids)],
        })

        # Reset checklist nếu chọn
        if self.reset_checklist:
            self.task_id._reset_checklist()

        return {'type': 'ir.actions.act_window_close'}