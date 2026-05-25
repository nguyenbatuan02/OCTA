# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class TicketHandoverWizard(models.TransientModel):
    """
    Wizard bàn giao ca — Lead chọn NV ca sau và ghi nội dung bàn giao.

    Flow:
        Lead mở wizard từ form ticket (nút 'Bàn giao ca')
        → Chọn NV ca sau + điền nội dung bàn giao
        → Xác nhận → ticket ghi nhận bàn giao + log
        → NV ca sau bấm 'Xác nhận nhận bàn giao' trên form ticket
    """
    _name = 'ticket.handover.wizard'
    _description = 'Wizard bàn giao ca'

    task_id = fields.Many2one(
        'project.task', 'Ticket', required=True, readonly=True,
    )
    task_name      = fields.Char(related='task_id.name', readonly=True)
    task_dept      = fields.Selection(related='task_id.dept', readonly=True)
    # FIX: bỏ task_issue — issue_type là computed field, Odoo không cho related vào đây
    sla_deadline   = fields.Datetime(related='task_id.sla_deadline', readonly=True)
    checklist_progress = fields.Integer(
        related='task_id.checklist_progress', readonly=True,
    )

    shift = fields.Selection([
        ('morning',   'Ca sáng (08:00–17:00)'),
        ('afternoon', 'Ca chiều (17:00–20:00)'),
        ('night',     'Ca tối (20:00–08:00)'),
    ], string='Ca hiện tại', required=True)

    handover_to_id = fields.Many2one(
        'res.users',
        string='Bàn giao cho *',
        required=True,
        help='NV ca sau sẽ tiếp nhận ticket này.',
    )
    handover_note = fields.Text(
        'Nội dung bàn giao *',
        required=True,
        placeholder=(
            'Mô tả:\n'
            '1. Trạng thái hiện tại (đã làm gì, kết quả ra sao)\n'
            '2. Việc cần làm tiếp theo\n'
            '3. Lưu ý đặc biệt (nếu có)'
        ),
    )

    def action_confirm(self):
        """Xác nhận bàn giao — ghi nhận vào ticket và audit log."""
        self.ensure_one()
        task = self.task_id
        user = self.env.user
        now = fields.Datetime.now()

        # Cập nhật ticket
        task.write({
            'shift':               self.shift,
            'handover_note':       self.handover_note,
            'handover_to_id':      self.handover_to_id.id,
            'handover_by_id':      user.id,
            'handover_at':         now,
            'is_handover_pending': True,
        })

        # Ghi chatter — visible cho tất cả follower
        task.message_post(
            body=(
                '<b>Bàn giao ca</b><br/>'
                'Người bàn giao: <b>%s</b><br/>'
                'Bàn giao cho: <b>%s</b><br/>'
                'Thời điểm: %s<br/>'
                'Nội dung: %s'
            ) % (
                user.name,
                self.handover_to_id.name,
                now.strftime('%H:%M %d/%m/%Y'),
                self.handover_note,
            ),
        )

        # Audit log
        self.env['octa.audit.log'].log_action(
            action_type='write',
            object_model='project.task',
            object_id=task.id,
            object_name=task.name,
            old_value='handover_pending=False',
            new_value='handover_to=%s' % self.handover_to_id.name,
            reason=self.handover_note,
            scope_tag=task.scope or 'bigtel',
        )

        # Notify NV ca sau qua bus
        try:
            self.env['bus.bus'].sudo()._sendone(
                self.handover_to_id.partner_id,
                'octa_handover_notify',
                {
                    'task_id':   task.id,
                    'task_name': task.name,
                    'from_user': user.name,
                    'note':      self.handover_note[:100] + '...' if len(self.handover_note) > 100 else self.handover_note,
                },
            )
        except Exception:
            pass

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Da ban giao ca',
                'message': 'Ticket da duoc ban giao cho %s.' % self.handover_to_id.name,
                'type': 'success',
                'sticky': False,
            },
        }