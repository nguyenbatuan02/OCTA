# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class OctaApprovalConfig(models.Model):
    """
    Cấu hình hạn mức phê duyệt và ngưỡng ranh đỏ — Singleton.

    Chỉ 1 bản ghi được active tại 1 thời điểm (_check_single_active).
    Toàn bộ module khác đọc config qua get_active() — không hardcode số.

    Thứ bậc phê duyệt hoàn tiền/nạp bù:
        Lead → TDABG → PPKD → TPKD → GĐ
    Mỗi tầng có hạn mức riêng; vượt tầng nào → tự động escalate lên tầng trên.
    """
    _name = 'octa.approval.config'
    _description = 'Cấu hình hạn mức phê duyệt Octa'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'effective_date desc'

    # ── Thông tin chung ─────────────────────────────────────────────

    name = fields.Char(
        'Tên phiên bản', required=True,
        default='Hạn mức phê duyệt 2026',
        tracking=True,
    )
    active = fields.Boolean(
        'Đang áp dụng', default=True, tracking=True,
        help='Chỉ 1 bản ghi được active tại một thời điểm.',
    )
    effective_date = fields.Date(
        'Ngày hiệu lực', required=True,
        default=fields.Date.today, tracking=True,
    )
    approved_by = fields.Many2one(
        'res.users', 'Phê duyệt bởi',
        default=lambda self: self.env.uid,
        tracking=True,
    )
    note = fields.Text('Ghi chú / căn cứ', tracking=True)

    # ── Hạn mức hoàn tiền / nạp bù (VNĐ) ──────────────────────────

    limit_lead = fields.Float(
        'Lead CSKH & VH (VNĐ)', required=True, default=0,
        digits=(15, 0), tracking=True,
        help='Hoàn tiền/nạp bù ≤ giá trị này: Lead tự duyệt được.',
    )
    limit_tdabg = fields.Float(
        'Trưởng dự án Bigtel (VNĐ)', required=True, default=0,
        digits=(15, 0), tracking=True,
        help='Vượt hạn mức Lead → TDABG duyệt.',
    )
    limit_ppkd = fields.Float(
        'Phó phòng Kinh doanh (VNĐ)', required=True, default=0,
        digits=(15, 0), tracking=True,
        help='Vượt hạn mức TDABG → PPKD duyệt.',
    )
    limit_tpkd = fields.Float(
        'Trưởng phòng Kinh doanh (VNĐ)', required=True, default=0,
        digits=(15, 0), tracking=True,
        help='Vượt hạn mức PPKD → TPKD duyệt. Vượt TPKD → escalate GĐ.',
    )

    # ── Hạn mức công nợ đại lý (VNĐ) ──────────────────────────────

    debt_limit_tdabg = fields.Float(
        'Công nợ đại lý — TDABG duyệt (VNĐ)', default=0,
        digits=(15, 0), tracking=True,
    )
    debt_limit_ppkd = fields.Float(
        'Công nợ đại lý — PPKD duyệt (VNĐ)', default=0,
        digits=(15, 0), tracking=True,
    )
    debt_limit_tpkd = fields.Float(
        'Công nợ đại lý — TPKD duyệt (VNĐ)', default=0,
        digits=(15, 0), tracking=True,
    )

    # ── Hạn mức đề xuất NCC mới (giá trị HĐ VNĐ) ──────────────────

    ncc_limit_tdabg = fields.Float(
        'NCC mới — TDABG duyệt (VNĐ)', default=0,
        digits=(15, 0), tracking=True,
    )
    ncc_limit_ppkd = fields.Float(
        'NCC mới — PPKD duyệt (VNĐ)', default=0,
        digits=(15, 0), tracking=True,
    )

    # ── Ngưỡng ranh đỏ vận hành ────────────────────────────────────

    gateway_error_threshold = fields.Integer(
        'Lỗi cổng liên tiếp → tự đóng', default=5,
        tracking=True,
        help='≥ X GD lỗi liên tiếp/cổng → hệ thống tự đóng cổng + alert TDABG.',
    )
    complaint_burst_count = fields.Integer(
        'Khiếu nại hàng loạt → khoá kho', default=3,
        tracking=True,
        help='≥ X khiếu nại trong cửa sổ thời gian → khoá kho tự động.',
    )
    complaint_burst_minutes = fields.Integer(
        'Cửa sổ thời gian khiếu nại (phút)', default=60,
        tracking=True,
    )
    emergency_approval_hours = fields.Integer(
        'Hạn bổ sung phê duyệt lệnh khẩn (giờ)', default=2,
        tracking=True,
        help='Sau lệnh đóng cổng khẩn cấp, TDABG/PPKD/TPKD bổ sung phê duyệt trong X giờ.',
    )
    emergency_report_hours = fields.Integer(
        'Hạn báo cáo cấp trên sau lệnh khẩn (giờ)', default=1,
        tracking=True,
        help='Sau lệnh đóng cổng khẩn cấp, phải báo PPKD/TPKD trong X giờ.',
    )

    # ── Ngưỡng ranh đỏ tập trung ───────────────────────────────────

    agent_concentration_pct = fields.Float(
        'Tập trung đại lý (%)', default=40.0,
        tracking=True,
        help='Đại lý chiếm > X% DT 1 sản phẩm → ranh đỏ, alert TPKD + GĐ.',
    )
    ncc_concentration_pct = fields.Float(
        'Tập trung NCC (%)', default=50.0,
        tracking=True,
        help='NCC chiếm > X% SL/dòng sản phẩm → ranh đỏ.',
    )
    finance_concentration_pct = fields.Float(
        'Vay 1 cty tài chính (%)', default=15.0,
        tracking=True,
        help='Vay từ 1 cty TC ≥ X% tổng vốn vay → ranh đỏ, alert HĐQT.',
    )
    finance_warning_pct = fields.Float(
        'Cảnh báo sớm vay TC (%)', default=12.0,
        tracking=True,
        help='Cảnh báo vàng khi tỷ trọng vay đạt X% (trước ranh đỏ 15%).',
    )

    # ── Ngưỡng ranh đỏ tồn kho & tài chính ────────────────────────

    stock_warning_days = fields.Integer(
        'Cảnh báo tồn kho (ngày nhu cầu)', default=7,
        tracking=True,
        help='Tồn kho < X ngày nhu cầu → alert High.',
    )
    reconciliation_lag_hours = fields.Integer(
        'Chênh lệch chưa giải trình (giờ)', default=24,
        tracking=True,
        help='Chênh lệch CMS vs KT chưa giải trình > X giờ → alert leo thang.',
    )
    flight_fund_warning = fields.Float(
        'Cảnh báo quỹ vé máy bay (VNĐ)', default=20_000_000,
        digits=(15, 0), tracking=True,
        help='Quỹ xuất vé ≤ X VNĐ → đề xuất nạp thêm (VH07).',
    )

    # ── Constraints ─────────────────────────────────────────────────

    @api.constrains('limit_lead', 'limit_tdabg', 'limit_ppkd', 'limit_tpkd')
    def _check_limit_hierarchy(self):
        """
        Hạn mức phải tăng dần theo thứ bậc: Lead ≤ TDABG ≤ PPKD ≤ TPKD.
        ValidationError đúng ở đây vì đây là constraint trên giá trị field.
        """
        for rec in self:
            if not (rec.limit_lead <= rec.limit_tdabg
                    <= rec.limit_ppkd <= rec.limit_tpkd):
                raise ValidationError(
                    'Hạn mức phải tăng dần theo thứ bậc:\n'
                    'Lead ≤ TDABG ≤ PPKD ≤ TPKD\n\n'
                    f'Hiện tại:\n'
                    f'  Lead   = {rec.limit_lead:>15,.0f} VNĐ\n'
                    f'  TDABG  = {rec.limit_tdabg:>15,.0f} VNĐ\n'
                    f'  PPKD   = {rec.limit_ppkd:>15,.0f} VNĐ\n'
                    f'  TPKD   = {rec.limit_tpkd:>15,.0f} VNĐ'
                )

    @api.constrains('finance_warning_pct', 'finance_concentration_pct')
    def _check_finance_pct(self):
        """Ngưỡng cảnh báo sớm phải thấp hơn ngưỡng ranh đỏ."""
        for rec in self:
            if rec.finance_warning_pct >= rec.finance_concentration_pct:
                raise ValidationError(
                    f'Cảnh báo sớm ({rec.finance_warning_pct}%) phải '
                    f'thấp hơn ranh đỏ ({rec.finance_concentration_pct}%).'
                )

    @api.constrains('active')
    def _check_single_active(self):
        """Singleton: chỉ 1 bản ghi active tại một thời điểm."""
        for rec in self:
            if rec.active:
                others = self.search([
                    ('active', '=', True),
                    ('id', '!=', rec.id),
                ])
                if others:
                    raise ValidationError(
                        'Chỉ được có 1 cấu hình đang áp dụng.\n'
                        f'Vui lòng tắt bản ghi "{others[0].name}" trước.'
                    )

    # ── Helper methods ───────────────────────────────────────────────

    @api.model
    def get_active(self):
        """
        Đọc config đang active. Gọi từ bất kỳ module nào:

            config = self.env['octa.approval.config'].get_active()
            if amount > config.limit_tdabg:
                # escalate lên PPKD

        Raise UserError (không phải ValidationError) vì đây là
        lỗi vận hành (chưa setup), không phải lỗi giá trị field.
        """
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            raise UserError(
                'Chưa có cấu hình hạn mức phê duyệt đang áp dụng.\n'
                'Vào menu: Octa → Cấu hình → Hạn mức phê duyệt để thiết lập.'
            )
        return config

    @api.model
    def get_limit_for_role(self, role_key: str) -> float:
        """
        Trả hạn mức hoàn tiền theo role key.
        role_key: 'lead' | 'tdabg' | 'ppkd' | 'tpkd'

        Trả 0 nếu role_key không hợp lệ (không raise — caller tự xử lý).
        """
        config = self.get_active()
        return {
            'lead':  config.limit_lead,
            'tdabg': config.limit_tdabg,
            'ppkd':  config.limit_ppkd,
            'tpkd':  config.limit_tpkd,
        }.get(role_key, 0)

    @api.model
    def get_escalate_role(self, current_role: str) -> str:
        """
        Trả role cần escalate lên khi vượt hạn mức current_role.
        Dùng trong octa_approval và octa_ticket.

            next_role = config.get_escalate_role('tdabg')  # → 'ppkd'
            next_role = config.get_escalate_role('tpkd')   # → 'gd'
            next_role = config.get_escalate_role('gd')     # → 'gd' (cùi)
        """
        chain = ['lead', 'tdabg', 'ppkd', 'tpkd', 'gd']
        try:
            idx = chain.index(current_role)
            return chain[idx + 1]
        except (ValueError, IndexError):
            return 'gd'

    @api.model
    def get_role_for_user(self, user=None) -> str:
        """
        Xác định role cao nhất của user trong thứ bậc Octa.
        Trả về key: 'tpkd' | 'ppkd' | 'tdabg' | 'lead' | 'ops' | 'cskh' | 'unknown'

        Kiểm tra từ cao xuống thấp vì user thuộc group cao
        cũng thuộc group thấp hơn qua implied_ids.

        Dùng trong octa_approval để tự động xác định tầng:
            role = self.env['octa.approval.config'].get_role_for_user()
            limit = self.env['octa.approval.config'].get_limit_for_role(role)
        """
        if user is None:
            user = self.env.user

        group_map = [
            ('tpkd',  'octa_base.group_tpkd'),
            ('ppkd',  'octa_base.group_ppkd'),
            ('tdabg', 'octa_base.group_tdabg'),
            ('lead',  'octa_base.group_lead'),
            ('ops',   'octa_base.group_octa_ops'),
            ('cskh',  'octa_base.group_octa_cskh'),
        ]
        for role_key, xml_id in group_map:
            group = self.env.ref(xml_id, raise_if_not_found=False)
            if group and user in group.users:
                return role_key
        return 'unknown'

    @api.model
    def can_approve(self, amount: float, role_key: str) -> bool:
        """
        Kiểm tra role có đủ quyền approve số tiền amount không.

        Dùng để disable/enable nút Phê duyệt trên form:
            config = self.env['octa.approval.config'].get_active()
            if not config.can_approve(self.refund_amount, 'tdabg'):
                # Show nút Escalate, disable nút Duyệt

        amount: số tiền cần phê duyệt (VNĐ)
        role_key: 'lead' | 'tdabg' | 'ppkd' | 'tpkd'
        """
        limit = self.get_limit_for_role(role_key)
        # limit = 0 nghĩa là chưa config → không cho duyệt
        if limit == 0:
            return False
        return amount <= limit
    
    # ── Nút Kích hoạt / Huỷ kích hoạt ──────────────────────────────

    def action_activate(self):
        """
        Nút Kích hoạt trên form.
        Tự động huỷ kích hoạt bản ghi đang active trước đó.
        Constraint _check_single_active sẽ bắt lỗi nếu có bug.
        """
        # Huỷ active tất cả bản ghi khác trước
        others = self.search([('active', '=', True), ('id', '!=', self.id)])
        if others:
            # Dùng write trực tiếp lên super để bypass tracking tạm thời
            others.write({'active': False})

        self.write({'active': True})

        # Ghi audit log
        self.env['octa.audit.log'].log_action(
            action_type='write',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            new_value='active = True',
            reason=f'Kích hoạt cấu hình hạn mức: {self.name}',
            scope_tag='system',
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Đã kích hoạt',
                'message': f'"{self.name}" đang được áp dụng.',
                'type': 'success',
                'sticky': False,
            },
        }

    def action_deactivate(self):
        """
        Nút Huỷ kích hoạt trên form.
        Cảnh báo: sau khi huỷ, hệ thống không có config active
        → get_active() sẽ raise UserError cho đến khi kích hoạt lại.
        """
        self.write({'active': False})

        self.env['octa.audit.log'].log_action(
            action_type='write',
            object_model=self._name,
            object_id=self.id,
            object_name=self.name,
            old_value='active = True',
            new_value='active = False',
            reason=f'Huỷ kích hoạt cấu hình: {self.name}',
            scope_tag='system',
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Đã huỷ kích hoạt',
                'message': 'Không còn cấu hình nào đang áp dụng. '
                           'Hãy kích hoạt 1 bản ghi trước khi vận hành.',
                'type': 'warning',
                'sticky': True,
            },
        }