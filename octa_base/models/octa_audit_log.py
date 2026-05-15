# -*- coding: utf-8 -*-
from odoo import models, fields, api


class OctaAuditLog(models.Model):
    """
    Audit log tập trung cho toàn bộ thao tác nghiệp vụ Octa.
    """
    _name = 'octa.audit.log'
    _description = 'Audit Log Octa'
    _order = 'log_time desc'
    _rec_name = 'action_type'

    # Không cho sửa/xóa bất kỳ trường nào sau khi tạo
    # → override write/unlink để block

    log_time = fields.Datetime(
        'Thời điểm', required=True,
        default=fields.Datetime.now, readonly=True,
        index=True,
    )
    user_id = fields.Many2one(
        'res.users', 'Người thực hiện',
        required=True, readonly=True,
        default=lambda self: self.env.uid,
        ondelete='restrict',
    )
    user_name = fields.Char(
        'Tên người thực hiện', readonly=True,
        help='Lưu tên tại thời điểm log, tránh mất dữ liệu khi đổi tên user.',
    )
    action_type = fields.Selection([
        ('create',    'Tạo mới'),
        ('write',     'Chỉnh sửa'),
        ('approve',   'Phê duyệt'),
        ('reject',    'Từ chối'),
        ('escalate',  'Leo thang'),
        ('stop',      'Dừng / Đóng'),
        ('emergency', 'Lệnh khẩn cấp'),
        ('login',     'Đăng nhập'),
        ('export',    'Xuất dữ liệu'),
    ], string='Hành động', required=True, readonly=True, index=True)

    object_model = fields.Char(
        'Model', required=True, readonly=True,
        help='Tên technical model, ví dụ: project.task, octa.gateway',
    )
    object_id = fields.Integer(
        'ID đối tượng', required=True, readonly=True, index=True,
    )
    object_name = fields.Char(
        'Tên đối tượng', readonly=True,
        help='Lưu tên tại thời điểm log.',
    )

    old_value = fields.Text('Giá trị cũ', readonly=True)
    new_value = fields.Text('Giá trị mới', readonly=True)

    reason = fields.Text(
        'Lý do', readonly=True,
        help='Bắt buộc với approve/reject/stop/escalate/emergency.',
    )
    attachment_ref = fields.Char(
        'Tham chiếu file đính kèm', readonly=True,
    )
    approval_state = fields.Char(
        'Trạng thái phê duyệt', readonly=True,
        help='Trạng thái workflow tại thời điểm log.',
    )

    # ── Phân loại đặc thù Octa ─────────────────────────────────────

    scope_tag = fields.Selection([
        ('bigtel',      'BIGTEL'),
        ('tc_tm',       'TC_TM — Tài chính lớp thương mại'),
        ('authorized',  'AUTHORIZED — Kỳ ủy quyền'),
        ('bigm',        'BIGM'),
        ('utv',         'UTV — Ứng tiền Viettel'),
        ('system',      'SYSTEM — Hệ thống'),
    ], string='Scope', readonly=True, index=True)

    escalation_level = fields.Selection([
        ('L1', 'L1 — Lead'),
        ('L2', 'L2 — TDABG'),
        ('L3', 'L3 — PPKD'),
        ('L4', 'L4 — TPKD'),
        ('L5', 'L5 — GĐ/HĐQT'),
    ], string='Tầng escalate', readonly=True)

    emergency = fields.Boolean(
        'Lệnh khẩn cấp', default=False, readonly=True,
        help='True khi là lệnh đóng cổng/kho khẩn cấp.',
        index=True,
    )

    authorization_doc_id = fields.Char(
        'Mã văn bản ủy quyền', readonly=True,
        help='Điền khi scope_tag=AUTHORIZED — kỳ PPKD thay TPKD.',
    )

    ip_address = fields.Char('IP Address', readonly=True)
    session_id  = fields.Char('Session ID', readonly=True)

    # ── Block sửa/xóa ──────────────────────────────────────────────

    def write(self, vals):
        raise models.ValidationError(
            'Không được sửa audit log sau khi đã ghi.\n'
            'Mọi thay đổi phải tạo bản ghi log mới.'
        )

    def unlink(self):
        raise models.ValidationError(
            'Không được xóa audit log.\n'
            'Dữ liệu phải được lưu trữ tối thiểu 5 năm theo quy định.'
        )

    # ── Helper: tạo log từ module khác ─────────────────────────────

    @api.model
    def log_action(
        self,
        action_type,
        object_model,
        object_id,
        object_name='',
        old_value=None,
        new_value=None,
        reason='',
        attachment_ref='',
        approval_state='',
        scope_tag='bigtel',
        escalation_level=False,
        emergency=False,
        authorization_doc_id='',
    ):
        """
        Tạo 1 bản ghi audit log. Gọi từ bất kỳ model nào.

        Ví dụ:
            self.env['octa.audit.log'].log_action(
                action_type='approve',
                object_model='project.task',
                object_id=self.id,
                object_name=self.name,
                reason='Duyệt hoàn tiền 500k — đúng SOP CS02',
                scope_tag='bigtel',
                escalation_level='L1',
            )
        """
        user = self.env.user
        self.sudo().create({
            'log_time':             fields.Datetime.now(),
            'user_id':              user.id,
            'user_name':            user.name,
            'action_type':          action_type,
            'object_model':         object_model,
            'object_id':            object_id,
            'object_name':          object_name or '',
            'old_value':            str(old_value) if old_value is not None else False,
            'new_value':            str(new_value) if new_value is not None else False,
            'reason':               reason,
            'attachment_ref':       attachment_ref,
            'approval_state':       approval_state,
            'scope_tag':            scope_tag,
            'escalation_level':     escalation_level,
            'emergency':            emergency,
            'authorization_doc_id': authorization_doc_id,
        })
