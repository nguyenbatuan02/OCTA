# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class TicketHandoverWizard(models.TransientModel):
    """
    Wizard bàn giao ca — Lead chọn nhiều ticket từ list view,
    chọn 1 NV ca sau nhận toàn bộ.

    Flow:
        Lead chọn nhiều ticket trên list → Action "Bàn giao ca"
        → Wizard mở với task_ids đã pre-fill từ context
        → Lead chọn handover_to_id (NV ca sau), điền note
        → Confirm → tất cả ticket: is_handover_pending=True,
          handover_to_id=NV, handover_by_id=Lead, handover_at=now
        → Gửi notification cho NV ca sau
    """
    _name = 'ticket.handover.wizard'
    _description = 'Wizard Bàn giao ca'

    # ── Danh sách ticket được chọn ────────────────────────────────
    task_ids = fields.Many2many(
        'project.task',
        'ticket_handover_wizard_task_rel',
        'wizard_id', 'task_id',
        string='Tickets bàn giao',
        required=True,
    )

    # ── NV ca sau nhận toàn bộ ────────────────────────────────────
    handover_to_id = fields.Many2one(
        'res.users',
        string='Bàn giao cho',
        required=True,
        domain="[('share', '=', False)]",
        help='Nhân viên ca sau nhận toàn bộ ticket được chọn.',
    )

    shift = fields.Selection([
        ('morning',   'Ca sáng (08:00–17:00)'),
        ('afternoon', 'Ca chiều (17:00–20:00)'),
        ('night',     'Ca tối (20:00–08:00)'),
    ], string='Ca bàn giao', required=True,
        help='Ca làm việc đang được bàn giao.',
    )

    handover_note = fields.Text(
        'Nội dung bàn giao',
        help='Tóm tắt tình hình và việc NV ca sau cần tiếp tục.',
    )

    # Computed summary để hiện trên wizard
    task_count = fields.Integer(
        'Số ticket',
        compute='_compute_task_count',
    )
    task_summary = fields.Html(
        'Danh sách ticket',
        compute='_compute_task_summary',
    )

    # ── Default get — pre-fill task_ids từ active_ids ─────────────

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # active_ids được truyền từ server action (list view selection)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids and 'task_ids' in fields_list:
            # Lọc: chỉ lấy ticket chưa đóng và chưa pending
            valid_tasks = self.env['project.task'].browse(active_ids).filtered(
                lambda t: not t.stage_id.fold and not t.is_handover_pending
            )
            if not valid_tasks:
                raise UserError(
                    'Tất cả ticket đã chọn đều đã đóng hoặc đang chờ bàn giao.\n'
                    'Vui lòng chọn lại.'
                )
            skipped = len(active_ids) - len(valid_tasks)
            if skipped:
                # Warning nhẹ — vẫn tiếp tục với ticket hợp lệ
                pass
            res['task_ids'] = [fields.Command.set(valid_tasks.ids)]
        return res

    @api.depends('task_ids')
    def _compute_task_count(self):
        for wiz in self:
            wiz.task_count = len(wiz.task_ids)

    @api.depends('task_ids')
    def _compute_task_summary(self):
        for wiz in self:
            if not wiz.task_ids:
                wiz.task_summary = '<em>Chưa có ticket nào.</em>'
                continue
            rows = ''.join(
                f'<tr>'
                f'<td style="padding:4px 8px">{t.name}</td>'
                f'<td style="padding:4px 8px;color:#6c757d">'
                f'{dict(t._fields["dept"].selection).get(t.dept, "") if t.dept else ""}</td>'
                f'<td style="padding:4px 8px;color:#6c757d">'
                f'{t.stage_id.name if t.stage_id else ""}</td>'
                f'</tr>'
                for t in wiz.task_ids
            )
            wiz.task_summary = (
                f'<table class="table table-sm table-bordered mb-0">'
                f'<thead><tr>'
                f'<th style="padding:4px 8px">Ticket</th>'
                f'<th style="padding:4px 8px">Bộ phận</th>'
                f'<th style="padding:4px 8px">Trạng thái</th>'
                f'</tr></thead>'
                f'<tbody>{rows}</tbody>'
                f'</table>'
            )

    # ── Validate ──────────────────────────────────────────────────

    @api.constrains('handover_to_id')
    def _check_handover_to(self):
        for wiz in self:
            if wiz.handover_to_id == self.env.user:
                raise ValidationError(
                    'Không thể bàn giao cho chính mình.\n'
                    'Vui lòng chọn nhân viên ca sau.'
                )

    # ── Confirm ───────────────────────────────────────────────────

    def action_confirm(self):
        """
        Ghi nhận bàn giao cho tất cả task_ids.

        Mỗi ticket:
        - is_handover_pending = True
        - handover_to_id = NV được chọn
        - handover_by_id = Lead đang login
        - handover_at = now
        - shift = ca được chọn
        - handover_note = note chung
        - user_ids: thêm NV ca sau để họ thấy ticket trong record rule

        Sau đó:
        - Gửi bus notification cho NV ca sau (hiện popup)
        - Post chatter trên từng ticket
        """
        self.ensure_one()
        if not self.task_ids:
            raise UserError('Không có ticket nào để bàn giao.')

        now = fields.Datetime.now()
        by_user = self.env.user
        to_user = self.handover_to_id
        shift_label = dict(
            self._fields['shift'].selection
        ).get(self.shift, self.shift)

        for task in self.task_ids:
            task.write({
                'is_handover_pending': True,
                'handover_to_id':      to_user.id,
                'handover_by_id':      by_user.id,
                'handover_at':         now,
                'shift':               self.shift,
                'handover_note':       self.handover_note or '',
                # Thêm NV ca sau vào user_ids để record rule cho phép họ thấy ticket
                'user_ids': [fields.Command.link(to_user.id)],
            })

            task.message_post(
                body=(
                    '<b>📋 Bàn giao ca — %s</b><br/>'
                    'Từ: <b>%s</b> → Cho: <b>%s</b><br/>'
                    'Thời điểm: %s<br/>'
                    '%s'
                ) % (
                    shift_label,
                    by_user.name,
                    to_user.name,
                    now.strftime('%H:%M %d/%m/%Y'),
                    ('<br/>📝 ' + self.handover_note) if self.handover_note else '',
                ),
                subtype_xmlid='mail.mt_note',
            )

        # Gửi bus notification → trigger popup phía NV ca sau
        pending_count = len(self.task_ids)
        self.env['bus.bus']._sendone(
            to_user.partner_id,
            'octa_handover_notification',
            {
                'type':          'handover',
                'count':         pending_count,
                'from_user':     by_user.name,
                'shift':         shift_label,
                'task_ids':      self.task_ids.ids,
                'message':       (
                    f'Bạn được {by_user.name} bàn giao '
                    f'{pending_count} ticket ({shift_label}).'
                ),
            },
        )

        # Audit log
        self.env['octa.audit.log'].log_action(
            action_type='write',
            object_model='project.task',
            object_id=self.task_ids[0].id if len(self.task_ids) == 1 else 0,
            object_name=(
                self.task_ids[0].name
                if len(self.task_ids) == 1
                else f'{pending_count} tickets'
            ),
            new_value=(
                f'Bàn giao cho {to_user.name}, ca {shift_label}'
            ),
            reason='Bàn giao ca cuối ca',
            scope_tag='bigtel',
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title':   '✅ Bàn giao thành công',
                'message': (
                    f'Đã bàn giao {pending_count} ticket cho '
                    f'{to_user.name} ({shift_label}).'
                ),
                'type':   'success',
                'sticky': False,
            },
        }