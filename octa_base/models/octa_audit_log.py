# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError  


class OctaAuditLog(models.Model):
    """
    Audit log tập trung cho toàn bộ thao tác nghiệp vụ Octa.

    Nguyên tắc bất biến:
    - KHÔNG sửa bất kỳ trường nào sau khi tạo  → write() raise UserError
    - KHÔNG xóa                                 → unlink() raise UserError
    - Lưu trữ tối thiểu 5 năm theo quy định nội bộ Octa
    """
    _name = 'octa.audit.log'
    _description = 'Audit Log Octa'
    _order = 'log_time desc'
    _rec_name = 'action_type'

    # ── Thông tin cơ bản ───────────────────────────────────────────

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
        # ondelete='restrict': không cho xóa user nếu còn log
        # → bảo toàn audit trail khi nhân sự nghỉ việc
    )
    user_name = fields.Char(
        'Tên người thực hiện', readonly=True,
        help='Lưu tên tại thời điểm log — tránh mất dữ liệu khi user đổi tên.',
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

    # ── Đối tượng bị tác động ──────────────────────────────────────

    object_model = fields.Char(
        'Model', required=True, readonly=True,
        help='Tên technical model, ví dụ: project.task, octa.gateway',
    )
    object_id = fields.Integer(
        'ID đối tượng', required=True, readonly=True, index=True,
    )
    object_name = fields.Char(
        'Tên đối tượng', readonly=True,
        help='Lưu tên tại thời điểm log — tránh mất khi record bị đổi tên/xóa.',
    )

    old_value = fields.Text('Giá trị cũ', readonly=True)
    new_value = fields.Text('Giá trị mới', readonly=True)

    reason = fields.Text(
        'Lý do', readonly=True,
        help='Bắt buộc với action_type: approve / reject / stop / escalate / emergency.',
    )
    attachment_ref = fields.Char(
        'Tham chiếu file đính kèm', readonly=True,
        help='Tên file hoặc đường dẫn tham chiếu — không lưu binary ở đây.',
    )
    approval_state = fields.Char(
        'Trạng thái phê duyệt', readonly=True,
        help='Trạng thái workflow của đối tượng tại thời điểm log.',
    )

    # ── Phân loại đặc thù Octa ─────────────────────────────────────

    scope_tag = fields.Selection([
        ('bigtel',     'BIGTEL'),
        ('tc_tm',      'TC_TM — Tài chính lớp thương mại'),
        ('authorized', 'AUTHORIZED — Kỳ ủy quyền PPKD'),
        ('bigm',       'BIGM'),
        ('utv',        'UTV — Ứng tiền Viettel'),
        ('system',     'SYSTEM — Hệ thống'),
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
        help='True khi là lệnh đóng cổng/kho khẩn cấp — cần bổ sung phê duyệt trong 2h.',
        index=True,
    )

    authorization_doc_id = fields.Char(
        'Mã văn bản ủy quyền', readonly=True,
        help='Điền khi scope_tag=AUTHORIZED — kỳ PPKD thay TPKD có văn bản.',
    )

    # FIX: ip_address và session_id — tự lấy trong log_action(), không cần truyền thủ công
    ip_address = fields.Char('IP Address', readonly=True)
    session_id = fields.Char('Session ID', readonly=True)

    # ── Block sửa/xóa ──────────────────────────────────────────────

    def write(self, vals):
        """
        FIX: đổi ValidationError → UserError.

        ValidationError dành cho constraint violation (giá trị field không hợp lệ).
        UserError dành cho business rule bị vi phạm (hành động không được phép).
        Odoo xử lý 2 exception này khác nhau trong transaction rollback và UI dialog.
        """
        raise UserError(
            'Không được sửa audit log sau khi đã ghi.\n'
            'Mọi thay đổi nghiệp vụ phải tạo bản ghi log mới.'
        )

    def unlink(self):
        """
        FIX: đổi ValidationError → UserError (cùng lý do).
        ACL (ir.model.access.csv) là lớp bảo vệ đầu tiên (perm_unlink=0).
        Method này là lớp bảo vệ thứ hai — defense in depth.
        """
        raise UserError(
            'Không được xóa audit log.\n'
            'Dữ liệu phải được lưu trữ tối thiểu 5 năm theo quy định Octa.\n'
            'Liên hệ Phòng Công nghệ nếu cần xử lý dữ liệu đặc biệt.'
        )

    # ── Helper public API ───────────────────────────────────────────

    @api.model
    def log_action(
        self,
        action_type: str,
        object_model: str,
        object_id: int,
        object_name: str = '',
        old_value=None,
        new_value=None,
        reason: str = '',
        attachment_ref: str = '',
        approval_state: str = '',
        scope_tag: str = 'bigtel',
        escalation_level: str | bool = False,
        emergency: bool = False,
        authorization_doc_id: str = '',
    ) -> None:
        """
        Tạo 1 bản ghi audit log. Gọi từ bất kỳ model nào trong hệ thống.

        Dùng sudo() nội bộ để:
        - NV CSKH/Ops (không có quyền create audit log) vẫn ghi được log hành động của mình
        - ACL layer (perm_create=0 với group thấp) không bị bypass — sudo() chỉ dùng trong method này

        FIX mới: tự lấy ip_address và session_id từ request context nếu có.
        Không raise nếu không lấy được (cron, shell, test context không có request).

        Ví dụ:
            self.env['octa.audit.log'].log_action(
                action_type='approve',
                object_model='project.task',
                object_id=self.id,
                object_name=self.name,
                reason='Duyệt hoàn tiền 500k — SOP CS02',
                scope_tag='bigtel',
                escalation_level='L1',
            )
        """
        user = self.env.user

        ip_addr = ''
        sess_id = ''
        try:
            from odoo.http import request as http_request
            if http_request and http_request.httprequest:
                ip_addr = (
                    http_request.httprequest.environ.get('HTTP_X_FORWARDED_FOR', '')
                    or http_request.httprequest.remote_addr
                    or ''
                )
                # Lấy IP đầu tiên nếu có nhiều IP (reverse proxy chain)
                ip_addr = ip_addr.split(',')[0].strip()
                sess_id = getattr(http_request.session, 'sid', '') or ''
        except Exception:
            # Không raise — log không được block nghiệp vụ chính
            pass

        # sudo() để bypass ACL khi ghi log
        # create() bị override bởi write() block? Không — chỉ write() sau khi tạo bị block
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
            'reason':               reason or '',
            'attachment_ref':       attachment_ref or '',
            'approval_state':       approval_state or '',
            'scope_tag':            scope_tag or 'bigtel',
            'escalation_level':     escalation_level or False,
            'emergency':            bool(emergency),
            'authorization_doc_id': authorization_doc_id or '',
            'ip_address':           ip_addr,
            'session_id':           sess_id,
        })