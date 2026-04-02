from datetime import timedelta

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
        snapshot = [
            (0, 0, {
                'sequence':       item.sequence,
                'name':           item.name,
                'done':           item.done,
                'attachment_ids': [(6, 0, item.attachment_ids.ids)],
            })
            for item in self.task_id.checklist_ids
        ]

        self.env['ticket.check.log'].create({
            'task_id':                self.task_id.id,
            'result':                 self.result,
            'note':                   self.note,
            'attachment_ids':         [(6, 0, self.attachment_ids.ids)],
            'checklist_snapshot_ids': snapshot,
        })

        if self.reset_checklist and self.task_id.ticket_type != 'continuous':
            self.task_id._reset_checklist()

        interval = {
            'gateway_39':        20,
            'gateway_70':        60,
            'txn_monitor':       30,
            'shift_tool_check':  None,  
            'shift_sales_check': None,
            'miniapp_check':     None,
            'msg_channels':      None,
        }.get(self.task_id.issue_type)

        if interval:
            self.task_id.next_check_time = (
                fields.Datetime.now() + timedelta(minutes=interval)
            )

        return {'type': 'ir.actions.act_window_close'}
    
        