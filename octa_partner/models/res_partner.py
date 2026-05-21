# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    """
    Extend res.partner với các field nghiệp vụ Octa.

    Phân loại đối tác:
    - NCC (supplier_rank > 0): cung cấp mã PIN, API, thẻ cào
    - Đại lý (customer_rank > 0): phân phối sản phẩm Octa
    - Cả hai: vừa mua vừa bán (hiếm)

    Ranh đỏ tự động (cron hằng ngày):
    - NCC: tỷ trọng SL/dòng SP > 50% → is_concentration_warning = True
    - Đại lý: DT/SP > 40% → is_concentration_warning = True
    - Công nợ: current_debt > debt_limit → is_debt_overlimit = True
    """
    _inherit = 'res.partner'

    # ── Phân loại Octa ──────────────────────────────────────────────

    octa_partner_type = fields.Selection([
        ('ncc',   'Nhà cung cấp (NCC)'),
        ('agent', 'Đại lý / Khách hàng'),
        ('both',  'NCC & Đại lý'),
    ], string='Loại đối tác Octa', tracking=True, index=True)

    scope = fields.Selection([
        ('bigtel', 'Bigtel'),
        ('bigm',   'BigM'),
        ('utv',    'UTV'),
        ('all',    'Tất cả'),
    ], string='Dự án', default='bigtel', tracking=True, index=True,
        help='Dự án kinh doanh mà đối tác này thuộc về.',
    )

    # ── Phân hạng đại lý ────────────────────────────────────────────

    agent_grade = fields.Selection([
        ('A', 'Hạng A — Chiến lược'),
        ('B', 'Hạng B — Tiềm năng'),
        ('C', 'Hạng C — Thông thường'),
    ], string='Phân hạng đại lý', tracking=True,
        help=(
            'A: Đại lý chiến lược, doanh số lớn, ưu tiên chăm sóc.\n'
            'B: Đại lý tiềm năng, đang phát triển.\n'
            'C: Đại lý thông thường, doanh số thấp.'
        ),
    )
    agent_grade_updated = fields.Date(
        'Ngày cập nhật hạng', readonly=True,
        help='Tự động cập nhật khi agent_grade thay đổi.',
    )

    # ── NCC — SLA & chất lượng ──────────────────────────────────────

    ncc_sla_hours = fields.Float(
        'SLA xử lý lỗi (giờ)', digits=(5, 1),
        help='Thời gian NCC cam kết xử lý lỗi GD (giờ).',
    )
    ncc_success_rate = fields.Float(
        'Tỷ lệ thành công (%)', digits=(5, 2),
        help='Tỷ lệ GD thành công 30 ngày gần nhất. Cập nhật từ CMS.',
    )
    ncc_pending_rate = fields.Float(
        'Tỷ lệ pending (%)', digits=(5, 2),
    )
    ncc_error_rate = fields.Float(
        'Tỷ lệ lỗi (%)', digits=(5, 2),
    )
    ncc_concentration_pct = fields.Float(
        'Tỷ trọng sản lượng (%)', digits=(5, 2),
        help=(
            'NCC chiếm X% sản lượng/dòng sản phẩm.\n'
            'Ranh đỏ: > 50% → cảnh báo, phải đa nguồn.'
        ),
    )
    ncc_last_evaluated = fields.Date(
        'Ngày đánh giá gần nhất',
    )
    ncc_note = fields.Text(
        'Ghi chú đánh giá NCC',
        help='Điều kiện thương mại, lịch sử sự cố, điểm mạnh/yếu.',
    )

    # ── Công nợ ─────────────────────────────────────────────────────

    debt_limit = fields.Float(
        'Hạn mức công nợ (VNĐ)', digits=(15, 0), tracking=True,
        help=(
            'Hạn mức công nợ được phê duyệt cho đối tác này.\n'
            'Phải qua WF phê duyệt mới được thay đổi.'
        ),
    )
    debt_limit_approved_by = fields.Many2one(
        'res.users', 'Người phê duyệt hạn mức', readonly=True,
    )
    debt_limit_approved_at = fields.Datetime(
        'Ngày duyệt hạn mức', readonly=True,
    )

    current_debt = fields.Float(
        'Công nợ hiện tại (VNĐ)',
        compute='_compute_current_debt',
        digits=(15, 0),
        help='Tổng công nợ chưa thanh toán từ Accounting.',
    )
    debt_usage_pct = fields.Float(
        'Tỷ lệ sử dụng hạn mức (%)',
        compute='_compute_current_debt',
        digits=(5, 1),
    )

    # ── Ranh đỏ ─────────────────────────────────────────────────────

    is_concentration_warning = fields.Boolean(
        'Ranh đỏ tập trung', default=False, index=True,
        help=(
            'True khi:\n'
            '- NCC: ncc_concentration_pct > ngưỡng NCC (50%)\n'
            '- Đại lý: doanh số/SP > ngưỡng đại lý (40%)'
        ),
    )
    is_debt_overlimit = fields.Boolean(
        'Vượt hạn mức công nợ', default=False, index=True,
        compute='_compute_current_debt', store=True,
    )
    red_line_note = fields.Text(
        'Ghi chú ranh đỏ', readonly=True,
        help='Mô tả ranh đỏ đang kích hoạt.',
    )

    # ── Thông tin bổ sung ───────────────────────────────────────────

    contract_ref = fields.Char(
        'Số hợp đồng',
        help='Mã hợp đồng khung với NCC/đại lý.',
    )
    contract_start = fields.Date('Ngày bắt đầu HĐ')
    contract_end   = fields.Date('Ngày kết thúc HĐ')
    is_contract_expiring = fields.Boolean(
        'HĐ sắp hết hạn', compute='_compute_contract_status',
    )

    # ── Computes ────────────────────────────────────────────────────

    @api.depends('credit', 'debit', 'debt_limit')
    def _compute_current_debt(self):
        """
        Tính công nợ hiện tại từ account.move.
        Odoo native: partner.credit = tổng phải thu, partner.debit = tổng phải trả.
        Với đại lý: dùng credit (phải thu).
        Với NCC: dùng debit (phải trả).
        """
        for partner in self:
            # Dùng credit cho đại lý, debit cho NCC
            if partner.octa_partner_type == 'ncc':
                debt = partner.debit or 0.0
            else:
                debt = partner.credit or 0.0

            partner.current_debt = debt
            partner.debt_usage_pct = (
                (debt / partner.debt_limit * 100)
                if partner.debt_limit > 0 else 0.0
            )
            partner.is_debt_overlimit = (
                partner.debt_limit > 0 and debt > partner.debt_limit
            )

    @api.depends('contract_end')
    def _compute_contract_status(self):
        today = fields.Date.today()
        for partner in self:
            if partner.contract_end:
                delta = (partner.contract_end - today).days
                partner.is_contract_expiring = 0 <= delta <= 30
            else:
                partner.is_contract_expiring = False

    # ── Override write: ghi timestamp khi đổi hạng ──────────────────

    def write(self, vals):
        if 'agent_grade' in vals:
            vals['agent_grade_updated'] = fields.Date.today()
        return super().write(vals)

    # ── Cron: kiểm tra ranh đỏ hằng ngày ───────────────────────────

    @api.model
    def _cron_check_partner_red_lines(self):
        """
        Cron chạy hằng ngày:
        1. Kiểm tra công nợ vượt hạn mức → alert + ghi is_debt_overlimit
        2. Kiểm tra tập trung NCC/đại lý → alert + ghi is_concentration_warning
        3. Kiểm tra HĐ sắp hết hạn → alert
        """
        config = self.env['octa.approval.config'].sudo().search(
            [('active', '=', True)], limit=1
        )
        ncc_threshold   = config.ncc_concentration_pct   if config else 50.0
        agent_threshold = config.agent_concentration_pct if config else 40.0

        # 1. Công nợ vượt hạn mức
        overlimit = self.search([
            ('debt_limit', '>', 0),
            ('octa_partner_type', 'in', ['ncc', 'agent', 'both']),
        ]).filtered(lambda p: p.is_debt_overlimit)

        for partner in overlimit:
            if not partner.is_debt_overlimit:
                continue
            partner.red_line_note = (
                f'Công nợ {partner.current_debt:,.0f} VNĐ vượt hạn mức '
                f'{partner.debt_limit:,.0f} VNĐ '
                f'({partner.debt_usage_pct:.1f}%)'
            )
            self.env['octa.audit.log'].sudo().log_action(
                action_type='write',
                object_model='res.partner',
                object_id=partner.id,
                object_name=partner.name,
                new_value=f'is_debt_overlimit=True, debt={partner.current_debt:,.0f}',
                reason='Ranh đỏ tự động: công nợ vượt hạn mức',
                scope_tag=partner.scope if partner.scope != 'all' else 'bigtel',
            )
            self._alert_red_line(
                partner,
                f'🔴 CÔNG NỢ VƯỢT HẠN MỨC: {partner.name} — '
                f'{partner.current_debt:,.0f} / {partner.debt_limit:,.0f} VNĐ '
                f'({partner.debt_usage_pct:.1f}%)',
            )

        # 2. Tập trung NCC
        ncc_concentrated = self.search([
            ('octa_partner_type', 'in', ['ncc', 'both']),
            ('ncc_concentration_pct', '>', ncc_threshold),
        ])
        for partner in ncc_concentrated:
            partner.write({'is_concentration_warning': True})
            partner.red_line_note = (
                f'NCC chiếm {partner.ncc_concentration_pct:.1f}% '
                f'sản lượng/dòng SP (ngưỡng {ncc_threshold}%)'
            )
            self._alert_red_line(
                partner,
                f'🔴 TẬP TRUNG NCC: {partner.name} chiếm '
                f'{partner.ncc_concentration_pct:.1f}% SL/dòng SP '
                f'(ngưỡng {ncc_threshold}%). Cần đa nguồn ngay.',
            )

        # 3. HĐ sắp hết hạn (≤30 ngày)
        expiring = self.search([
            ('octa_partner_type', 'in', ['ncc', 'agent', 'both']),
            ('contract_end', '!=', False),
        ]).filtered(lambda p: p.is_contract_expiring)
        for partner in expiring:
            days_left = (partner.contract_end - fields.Date.today()).days
            self._alert_red_line(
                partner,
                f'🟡 HĐ SẮP HẾT HẠN: {partner.name} — '
                f'còn {days_left} ngày (đến {partner.contract_end})',
            )

    def _alert_red_line(self, partner, message: str):
        """Gửi alert đến TDABG/PPKD/TPKD về ranh đỏ đối tác."""
        for xml_id in [
            'octa_base.group_tdabg',
            'octa_base.group_ppkd',
            'octa_base.group_tpkd',
        ]:
            group = self.env.ref(xml_id, raise_if_not_found=False)
            if not group:
                continue
            for user in group.users:
                try:
                    self.env['bus.bus'].sudo()._sendone(
                        user.partner_id,
                        'octa_partner_alert',
                        {
                            'partner_id':   partner.id,
                            'partner_name': partner.name,
                            'message':      message,
                        },
                    )
                except Exception:
                    pass