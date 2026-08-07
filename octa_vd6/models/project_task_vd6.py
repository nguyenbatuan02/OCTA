# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

from .vd6_common import (
    VD6_TH, VD6_PHUONG_AN, VD6_NGUON, VD6_GD_STATUS, VD6_LOAI_TICKET,
)

VD6_APPROVER_LABELS = {
    'cskh_lead': 'Trưởng nhóm CSKH',
    'tda':       'Trưởng dự án',
    'tpkd_ktt':  'TPKD / Kế toán trưởng',
    'bgd':       'Ban Giám đốc',
}


class ProjectTaskType(models.Model):
    """Đánh dấu 8 stage riêng của luồng Vòng đời 6."""
    _inherit = 'project.task.type'

    is_vd6_stage = fields.Boolean('Stage Vòng đời 6', default=False, index=True)
    vd6_code = fields.Char(
        'Mã trạng thái VĐ6', index=True,
        help='MOI_TAO / DANG_XAC_MINH / ... / DA_DONG / TU_CHOI',
    )


class ProjectTask(models.Model):
    """Mở rộng ticket cho nghiệp vụ Vòng đời 6 (hoàn/hủy/điều chỉnh GD).

    Ticket VĐ6 dùng chung project.task với ticket CS/VH, phân biệt bằng
    is_vd6=True và source='api'. Trạng thái ticket = stage (vd6_code).
    """
    _inherit = 'project.task'

    is_vd6 = fields.Boolean('Ticket Vòng đời 6', default=False, index=True)
    vd6_ma_ticket = fields.Char(
        'Mã ticket VĐ6', index=True, copy=False,
        help='Định danh trả về cho Portal (TK-xxxxxx).',
    )

    vd6_loai_th = fields.Selection(VD6_TH, string='Tình huống (TH)', tracking=True)
    vd6_loai_ticket = fields.Selection(
        VD6_LOAI_TICKET, string='Loại ticket VĐ6',
        default='TICKET_KHACH', tracking=True,
    )
    vd6_ma_gd_goc = fields.Char('Mã giao dịch gốc', index=True, tracking=True)
    vd6_trang_thai_gd_goc = fields.Selection(
        VD6_GD_STATUS, string='Trạng thái GD gốc', tracking=True,
    )
    vd6_so_tien = fields.Float(
        'Số tiền / giá trị', digits=(15, 0), tracking=True,
        help='Giá trị ảnh hưởng — quyết định cấp duyệt.',
    )
    vd6_nguon_phat_hien = fields.Selection(VD6_NGUON, string='Nguồn phát hiện')
    vd6_phuong_an_de_xuat = fields.Selection(
        VD6_PHUONG_AN, string='Phương án đề xuất', tracking=True,
    )
    vd6_phuong_an_da_duyet = fields.Boolean('Phương án đã duyệt', tracking=True)
    vd6_ma_pa_thuc_hien = fields.Char('Mã phương án đã thực hiện', tracking=True)

    vd6_request_id = fields.Char(
        'Request ID (Portal)', index=True, copy=False,
        help='UUID Portal gửi khi tạo — dùng chống trùng (idempotency).',
    )
    vd6_ticket_khach_lien_ket = fields.Char('Ticket khách liên kết (đã đóng)')
    vd6_ticket_noi_bo_lien_ket = fields.Char('Ticket nội bộ liên kết (TH5/6/7)')
    vd6_reject_reason = fields.Char('Lý do từ chối', copy=False)

    # Người (từ Portal là chuỗi tài khoản; nội bộ có thể là user Odoo)
    vd6_nguoi_tao_portal = fields.Char('Người tạo (Portal)')
    vd6_nguoi_xu_ly_portal = fields.Char('Người xử lý (Portal)')

    # ── Suy diễn ────────────────────────────────────────────────────
    vd6_status = fields.Char(
        'Trạng thái VĐ6', compute='_compute_vd6_status', store=True,
        help='Mã trạng thái = vd6_code của stage hiện tại.',
    )
    vd6_approver_role = fields.Selection([
        ('cskh_lead', 'Trưởng nhóm CSKH'),
        ('tda',       'Trưởng dự án'),
        ('tpkd_ktt',  'TPKD / Kế toán trưởng'),
        ('bgd',       'Ban Giám đốc'),
    ], string='Cấp duyệt (theo số tiền)', compute='_compute_vd6_approver', store=True)
    vd6_team_summary = fields.Char(
        'Nhóm phụ trách', compute='_compute_vd6_team_summary',
    )

    @api.depends('stage_id', 'stage_id.vd6_code')
    def _compute_vd6_status(self):
        for t in self:
            t.vd6_status = t.stage_id.vd6_code if t.is_vd6 else False

    @api.depends('vd6_so_tien', 'is_vd6')
    def _compute_vd6_approver(self):
        Config = self.env['octa.approval.config'].sudo()
        for t in self:
            if t.is_vd6 and t.vd6_so_tien:
                try:
                    t.vd6_approver_role = Config.get_vd6_approver_role(t.vd6_so_tien)
                except Exception:
                    t.vd6_approver_role = False
            else:
                t.vd6_approver_role = False

    @api.depends('vd6_loai_th')
    def _compute_vd6_team_summary(self):
        Rule = self.env['octa.vd6.assign.rule'].sudo()
        for t in self:
            if not t.vd6_loai_th:
                t.vd6_team_summary = False
                continue
            rules = Rule.search([('loai_th', '=', t.vd6_loai_th)])
            parts = ['%s (%s)' % (r.team_id.code, r.role) for r in rules]
            t.vd6_team_summary = ', '.join(parts) or False

    # ── Helpers ─────────────────────────────────────────────────────

    @api.model
    def _vd6_stage(self, code):
        """Trả về project.task.type theo vd6_code."""
        stage = self.env['project.task.type'].sudo().search(
            [('vd6_code', '=', code), ('is_vd6_stage', '=', True)], limit=1)
        if not stage:
            raise UserError('Chưa cấu hình stage VĐ6 mã "%s".' % code)
        return stage

    def get_vd6_teams(self):
        """Trả list nhóm phụ trách [{team_code, team_name, role}] theo tình huống."""
        self.ensure_one()
        rules = self.env['octa.vd6.assign.rule'].sudo().search(
            [('loai_th', '=', self.vd6_loai_th)])
        return [{
            'team_code': r.team_id.code,
            'team_name': r.team_id.name,
            'role': r.role,
        } for r in rules]

    # ── Ràng buộc quyền duyệt theo số tiền ──────────────────────────

    # role duyệt → group được phép (cấp cao hơn cũng duyệt được nhờ implied_ids)
    _VD6_APPROVE_GROUPS = {
        'cskh_lead': ['octa_base.group_lead'],
        'tda':       ['octa_base.group_tdabg'],
        'tpkd_ktt':  ['octa_base.group_tpkd', 'octa_base.group_ktt', 'octa_base.group_gd'],
        'bgd':       ['octa_base.group_gd'],
    }

    def _vd6_check_approver(self):
        self.ensure_one()
        role = self.vd6_approver_role
        groups = self._VD6_APPROVE_GROUPS.get(role, [])
        if not any(self.env.user.has_group(g) for g in groups):
            raise UserError(
                'Số tiền %s VNĐ cần cấp "%s" phê duyệt.\n'
                'Bạn không đủ thẩm quyền cho ticket này.'
                % ('{:,.0f}'.format(self.vd6_so_tien or 0),
                   VD6_APPROVER_LABELS.get(role, role))
            )

    def _vd6_move(self, code, extra=None):
        """Chuyển stage VĐ6 + ghi audit."""
        self.ensure_one()
        vals = {'stage_id': self._vd6_stage(code).id}
        if extra:
            vals.update(extra)
        self.write(vals)
        self.env['octa.audit.log'].log_action(
            action_type='write', object_model=self._name,
            object_id=self.id, object_name=self.vd6_ma_ticket or self.name,
            new_value='→ %s' % code, reason='VĐ6 chuyển trạng thái',
            scope_tag='bigtel')

    # ── Nút thao tác vòng đời ────────────────────────────────────────

    def action_vd6_verify(self):
        for t in self:
            t._vd6_move('DANG_XAC_MINH')

    def action_vd6_propose(self):
        for t in self:
            if not t.vd6_phuong_an_de_xuat:
                raise UserError('Phải chọn "Phương án đề xuất" trước khi trình duyệt.')
            t._vd6_move('CHO_PHE_DUYET')

    def action_vd6_approve(self):
        for t in self:
            t._vd6_check_approver()
            t._vd6_move('DA_DUYET', {'vd6_phuong_an_da_duyet': True})
            if t.env.user not in t.user_ids:
                t.write({'user_ids': [(4, t.env.user.id)]})

    def action_vd6_reject(self):
        for t in self:
            t._vd6_move('TU_CHOI', {'result_final': 'failed'})

    def action_vd6_to_reconcile(self):
        for t in self:
            t._vd6_move('CHO_DOI_SOAT')

    def action_vd6_reconciled(self):
        for t in self:
            if not (t.env.user.has_group('octa_base.group_ktt')
                    or t.env.user.has_group('octa_base.group_gd')):
                raise UserError('Chỉ Kế toán trưởng mới xác nhận đối soát khớp.')
            t._vd6_move('DA_DOI_SOAT')

    def action_vd6_reconcile_fail(self):
        for t in self:
            t._vd6_move('DA_DUYET')  # quay lại thực hiện

    def action_vd6_close(self):
        for t in self:
            if not t.result_final:
                raise UserError('Phải chọn "Kết quả cuối" trước khi đóng ticket.')
            t._vd6_move('DA_DONG')

    def _vd6_create_internal_ticket(self):
        """TH5/6/7: tự sinh ticket trách nhiệm nội bộ, độc lập, ẩn với khách."""
        self.ensure_one()
        if self.vd6_loai_th not in ('TH5', 'TH6', 'TH7'):
            return False
        Task = self.env['project.task'].sudo()
        internal = Task.create({
            'name': 'Nội bộ · %s · %s' % (self.vd6_loai_th, self.vd6_ma_gd_goc),
            'project_id': self.project_id.id,
            'stage_id': Task._vd6_stage('MOI_TAO').id,
            'is_vd6': True, 'source': 'api', 'dept': 'cskh',
            'vd6_loai_ticket': 'TICKET_NOI_BO',
            'vd6_loai_th': self.vd6_loai_th,
            'vd6_ma_gd_goc': self.vd6_ma_gd_goc,
            'vd6_so_tien': self.vd6_so_tien,
            'vd6_ticket_khach_lien_ket': self.vd6_ma_ticket,
            'description': 'Ticket trách nhiệm nội bộ (%s) — độc lập, không '
                           'hiển thị cho khách.' % self.vd6_loai_th,
        })
        internal.vd6_ma_ticket = 'TKNB-%06d' % internal.id
        self.write({'vd6_ticket_noi_bo_lien_ket': internal.vd6_ma_ticket})
        return internal
