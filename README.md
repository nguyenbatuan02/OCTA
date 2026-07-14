# Dự án Octa — Odoo 17 Custom Modules (Bigtel)

## Tổng quan
Hệ thống quản lý phân phối thẻ nạp & dịch vụ số Bigtel.
6 module custom trong namespace `octa`, chạy trên Odoo 17 Community.

## Tài liệu nghiệp vụ (đọc khi cần hiểu yêu cầu)
Tất cả tài liệu đặt trong thư mục `docs/`:

| File | Nội dung |
|---|---|
| `docs/lead_cskh.md` | Mô tả công việc Lead CSKH & Vận hành thương mại |
| `docs/ppkd.md` | Mô tả công việc Phó phòng Kinh doanh |
| `docs/tdabg.md` | Mô tả công việc Trưởng dự án Bigtel |
| `docs/tpkd.md` | Mô tả công việc Trưởng phòng Kinh doanh |
| `docs/quytrinh_cskh.md` | Quy trình CS01–CS10 (thẻ lỗi, topup, cổng...) |
| `docs/quytrinh_vh.md` | Quy trình VH01–VH08 (mua hàng, cổng API...) |
| `docs/odoo_ppkd.md` | Yêu cầu cấu hình Odoo cho PPKD |
| `docs/odoo_tdabg.md` | Yêu cầu cấu hình Odoo cho TDABG |
| `docs/odoo_tpkd.md` | Yêu cầu cấu hình Odoo cho TPKD |

## Cấu trúc module
- `octa_base/`     — Security groups (6 cấp), audit log, approval config
- `octa_project/`  — Extend project.task: scope, dept, date_closed
- `octa_ticket/`   — Ticket CSKH (CS01-CS10) & Vận hành (VH01-VH08), bàn giao ca
- `octa_approval/` — Approval workflow 5 tầng, auto-escalation, SoD
- `octa_gateway/`  — API gateway monitoring, auto-lock ranh đỏ
- `octa_partner/`  — Extend res.partner: NCC/agent, debt limits

## Phân quyền (thấp → cao)
NV CSKH → NV Vận hành → Lead → TDABG → PPKD → TPKD

## Scope / Dept
- scope: bigtel / bigm / utv
- dept: cskh / ops

## Odoo 17 — Lưu ý kỹ thuật QUAN TRỌNG
- `stage_id.fold` (KHÔNG phải `is_closed` — field này không tồn tại)
- `view_mode = 'tree'` (KHÔNG phải `'list'`)
- `invisible` trên `<header>` KHÔNG resolve related 2 cấp (field.subfield)
  → Dùng computed Boolean field làm intermediary
- computed field `store=False` khi phụ thuộc `uid` hoặc `now()`
- `binding_view_types = 'list'` trong server action (khác với view_mode)
- Record rules trên `res.partner` cần fallback `octa_partner_type = False`

## Luồng bàn giao ca
1. Lead → List view → chọn nhiều ticket → Action "Bàn giao ca"
2. Wizard: chọn 1 NV ca sau + ca + note → Confirm
3. Tất cả ticket: `is_handover_pending=True`, `handover_to_id=NV`
4. NV ca sau nhận popup (bus.bus) → "Xác nhận nhận ca" bulk
5. Hoặc vào menu "Ticket được bàn giao cho tôi" → confirm

## Luồng approval
NV tạo → Lead duyệt → TDABG → PPKD → TPKD
Auto-escalate khi vượt hạn mức. Không self-approve.