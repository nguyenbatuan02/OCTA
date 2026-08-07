# -*- coding: utf-8 -*-
"""Hằng số & model danh mục dùng chung cho Vòng đời 6."""
from odoo import models, fields

# ── Danh mục enum (đồng bộ với đặc tả API VĐ6) ──────────────────────

VD6_TH = [
    ('TH1', 'TH1 — Thẻ lỗi, khách muốn hoàn tiền'),
    ('TH2', 'TH2 — Thẻ lỗi, khách nhận lại mã đúng'),
    ('TH3', 'TH3 — Topup báo OK nhưng khách không nhận'),
    ('TH4', 'TH4 — GD treo, NCC cập nhật được'),
    ('TH5', 'TH5 — GD treo, NCC không cập nhật được'),
    ('TH6', 'TH6 — Cập nhật sai: thất bại→thực tế thành công'),
    ('TH7', 'TH7 — Cập nhật sai: thành công→thực tế thất bại'),
    ('TH8', 'TH8 — GD đã ghi nhận nhưng phát hiện sai'),
]

VD6_PHUONG_AN = [
    ('HOAN_TIEN', 'Hoàn tiền'),
    ('HOAN_MA', 'Hoàn mã'),
    ('NAP_BU', 'Nạp bù'),
    ('CAP_NHAT_TRANG_THAI_GIAO_DICH', 'Cập nhật trạng thái giao dịch'),
    ('HE_THONG_TU_XU_LY', 'Hệ thống tự xử lý'),
]

VD6_NGUON = [
    ('KHIEU_NAI_KH', 'Khiếu nại của khách hàng'),
    ('CANH_BAO_HE_THONG', 'Cảnh báo hệ thống'),
    ('PHAT_HIEN_DOI_SOAT', 'Phát hiện qua đối soát'),
]

VD6_GD_STATUS = [
    ('0', 'Thất bại'),
    ('2', 'Đang xử lý'),
    ('3', 'Thành công'),
]

VD6_LOAI_TICKET = [
    ('TICKET_KHACH', 'Ticket khách'),
    ('TICKET_NOI_BO', 'Ticket trách nhiệm nội bộ'),
]

# Mã stage (= trạng thái ticket VĐ6). Trùng vd6_code trên project.task.type.
VD6_STAGE_CODES = [
    'MOI_TAO', 'DANG_XAC_MINH', 'CHO_PHE_DUYET', 'DA_DUYET',
    'CHO_DOI_SOAT', 'DA_DOI_SOAT', 'DA_DONG', 'TU_CHOI',
]


class Vd6Team(models.Model):
    _name = 'octa.vd6.team'
    _description = 'Nhóm phụ trách Vòng đời 6'
    _order = 'code'

    code = fields.Char('Mã nhóm', required=True, index=True)   # CSKH, VHTM, CN, KT
    name = fields.Char('Tên nhóm', required=True)

    _sql_constraints = [('uniq_code', 'unique(code)', 'Mã nhóm phải duy nhất.')]


class Vd6AssignRule(models.Model):
    """Bảng ánh xạ Tình huống → nhóm phụ trách (OWNER/SUPPORT)."""
    _name = 'octa.vd6.assign.rule'
    _description = 'Quy tắc phân công nhóm theo tình huống VĐ6'
    _order = 'loai_th, role'

    loai_th = fields.Selection(VD6_TH, string='Tình huống', required=True, index=True)
    team_id = fields.Many2one('octa.vd6.team', 'Nhóm', required=True, ondelete='cascade')
    role = fields.Selection([
        ('OWNER', 'Chủ trì'),
        ('SUPPORT', 'Phối hợp'),
    ], string='Vai trò', required=True, default='OWNER')
