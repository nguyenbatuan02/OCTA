# CẨM NANG TEST HỆ THỐNG OCTA
## Hướng dẫn từng bước — ai làm, bấm gì, kết quả ra sao

| | |
|---|---|
| Địa chỉ hệ thống | `http://localhost:8069` |
| Ngày | 04/2026 |
| Mục đích | Để người test đăng nhập và chạy thử từng luồng nghiệp vụ |

---

## A. Đăng nhập & tài khoản test

Vào `http://localhost:8069`, nhập **Tài khoản** và **Mật khẩu** bên dưới.
**Mật khẩu tất cả tài khoản: `octa@123`** (mk = mật khẩu).

| Tài khoản | Mật khẩu | Vai trò | Dùng để test |
|---|---|---|---|
| `cskh1` | octa@123 | Nhân viên CSKH | Tạo & xử lý ticket, nộp báo cáo |
| `vh1` | octa@123 | Nhân viên Vận hành | Xử lý việc vận hành |
| `lead1` | octa@123 | Lead (Trưởng nhóm) | Duyệt tiền ≤ 500.000đ, bàn giao ca |
| `tdabg1` | octa@123 | Trưởng dự án | Duyệt tiền ≤ 3.000.000đ |
| `ppkd1` | octa@123 | Phó phòng KD | Xem, hỗ trợ |
| `tpkd1` | octa@123 | Trưởng phòng KD | Duyệt tiền ≤ 10.000.000đ |
| `ktt1` | octa@123 | Kế toán trưởng | Đối soát Vòng đời 6 |
| `gd1` | octa@123 | Ban Giám đốc | Duyệt tiền > 10.000.000đ |

*Mẹo: mở nhiều trình duyệt / cửa sổ ẩn danh để đăng nhập nhiều vai cùng lúc.*

---

## LUỒNG 1 — Xử lý ticket khách hàng (thẻ lỗi)

**Mục tiêu:** khách báo thẻ lỗi, nhân viên CSKH tiếp nhận và xử lý.

**Bước 1 — Nhân viên CSKH tạo ticket.**
Đăng nhập `cskh1` → menu **Octa Ticket → Chăm sóc khách hàng** → bấm **Mới**.
- *Tên:* "Khách báo thẻ 100k không nạp được"
- *Bộ phận:* CSKH
- *Loại sự cố:* **CS01 — Thẻ lỗi / không nạp được**
→ Hệ thống **tự sinh danh sách checklist các bước cần làm** và đặt hạn xử lý (SLA).

**Bước 2 — Nhân viên làm theo checklist.**
Tick ✔ từng bước trong mục *Checklist* khi hoàn thành (kiểm tra thông tin, xác minh nguồn thẻ, tra nhà mạng...).

**Bước 3 — Ghi nhận đã phản hồi khách.**
Bấm nút **💬 Đã phản hồi KH** (hệ thống ghi lại thời gian phản hồi để chấm điểm).

**Bước 4 — Chốt kết quả & đóng.**
Chọn *Kết quả cuối* = "Đã hoàn tiền" (hoặc phù hợp) → kéo trạng thái ticket sang **Đã đóng**.
✅ *Kết quả mong đợi:* ticket đóng thành công. Nếu chưa chọn Kết quả cuối, hệ thống **chặn** và nhắc chọn.

---

## LUỒNG 2 — Bàn giao ca

**Mục tiêu:** hết ca, giao ticket đang dở cho người ca sau.

**Bước 1 — Người giao (Lead).**
Đăng nhập `lead1` → mở 1 ticket đang xử lý → bấm **📋 Bàn giao ca** →
chọn *Bàn giao cho* = `cskh1`, ghi *Nội dung bàn giao* → Xác nhận.

**Bước 2 — Người nhận (ca sau).**
Đăng nhập `cskh1` → vào **Octa Ticket → Bàn giao ca → Ticket được bàn giao cho tôi** → mở ticket → bấm **✅ Xác nhận nhận bàn giao**.
✅ *Kết quả:* ticket chuyển trách nhiệm sang `cskh1`, có ghi nhật ký bàn giao.

---

## LUỒNG 3 — Phê duyệt hoàn tiền (nội bộ)

**Mục tiêu:** nhân viên đề xuất hoàn tiền, cấp trên duyệt theo hạn mức.

**Bước 1 — Nhân viên tạo phiếu.**
Đăng nhập `cskh1` → menu **Phiếu phê duyệt Octa → Phiếu của tôi** → **Mới** →
*Loại phiếu:* Hoàn tiền/Nạp bù · *Số tiền:* 300.000 → bấm **Gửi duyệt**.

**Bước 2 — Cấp trên duyệt.**
Đăng nhập `lead1` → **Phiếu phê duyệt Octa → Chờ tôi duyệt** → mở phiếu → **Phê duyệt** (hoặc Từ chối, nhập lý do).
✅ *Kết quả:* phiếu chuyển "Đã duyệt".

**Thử vượt hạn mức:** tạo phiếu **5.000.000đ** → `lead1` sẽ **không duyệt được**, chỉ hiện nút **Escalate** (chuyển lên Trưởng dự án). Đăng nhập `tdabg1` duyệt tiếp.

---

## LUỒNG 4 — Vòng đời 6: Hoàn/Hủy/Điều chỉnh giao dịch (Portal ↔ Odoo)

**Đây là luồng tích hợp với Portal.** Portal tạo ticket qua API, nhân viên Octa xử lý trên Odoo.

> **Chuẩn bị (Phòng Công nghệ):** các lệnh `curl` chạy ở cửa sổ Terminal. Khóa API: `CHANGE_ME_UAT_KEY`.

**Bước 1 — Portal tạo ticket (API-1).** Phòng CN chạy:
```
curl -s -X POST http://localhost:8069/api/octa/v1/tickets \
 -H "X-Api-Key: CHANGE_ME_UAT_KEY" -H "Content-Type: application/json" -d '{
  "request_id":"demo-1","ma_gd_goc":"GD-DEMO-01","trang_thai_gd_goc":3,
  "so_tien_gia_tri":250000,"loai_th":"TH1","mo_ta_su_vu":"The 100k loi",
  "nguon_phat_hien":"KHIEU_NAI_KH","phuong_an_de_xuat":"HOAN_TIEN","nguoi_tao":"cskh01"}'
```
→ Trả về mã ticket, ví dụ **TK-000050**. Ticket xuất hiện trong Odoo.

**Bước 2 — Nhân viên nhận & xác minh.**
Đăng nhập `cskh1` → **Octa Ticket → Vòng đời 6 (Hoàn/Hủy/Điều chỉnh)** → mở ticket TK-000050 → bấm **① Nhận & xác minh**.

**Bước 3 — Đề xuất phương án.**
Vẫn `cskh1` → kiểm tra *Phương án đề xuất* = Hoàn tiền → bấm **② Trình duyệt phương án**.

**Bước 4 — Cấp có thẩm quyền duyệt.**
Ticket 250.000đ → cấp duyệt là **Trưởng nhóm CSKH**. Đăng nhập `lead1` → mở ticket → bấm **③ Phê duyệt**.
*(Nếu số tiền lớn hơn, xem bảng "cấp duyệt" bên dưới — cấp thấp bấm sẽ bị chặn.)*

**Bước 5 — Portal kiểm tra & báo kết quả (API-3, API-4).** Phòng CN chạy:
```
# Kiểm tra đã được phép chưa (phải trả duoc_phep: true)
curl -s -X POST http://localhost:8069/api/octa/v1/tickets/check-condition \
 -H "X-Api-Key: CHANGE_ME_UAT_KEY" -H "Content-Type: application/json" \
 -d '{"ma_gd_goc":"GD-DEMO-01","phuong_an_du_kien":"HOAN_TIEN"}'

# Báo đã hoàn tiền xong (thay TK-000050 bằng mã thật)
curl -s -X POST http://localhost:8069/api/octa/v1/tickets/execution-result \
 -H "X-Api-Key: CHANGE_ME_UAT_KEY" -H "Content-Type: application/json" -d '{
  "request_id":"exec-1","ma_ticket":"TK-000050","ma_gd_goc":"GD-DEMO-01",
  "trang_thai_gd_goc":3,"phuong_an_da_thuc_hien":"HOAN_TIEN",
  "ma_phuong_an_da_thuc_hien":"NAP-123","nguoi_xu_ly":"cskh01",
  "thoi_gian_thuc_hien":"2026-04-10T10:00:00+07:00"}'
```

**Bước 6 — Nhân viên gửi đối soát.**
`cskh1` → mở ticket → bấm **④ Gửi đối soát**.

**Bước 7 — Kế toán đối soát.**
Đăng nhập `ktt1` → mở ticket → bấm **⑤ Đối soát khớp**.
*(Chỉ Kế toán trưởng bấm được; người khác bị chặn.)*

**Bước 8 — Đóng ticket.**
`cskh1` (hoặc `lead1`) → chọn *Kết quả cuối* → bấm **⑥ Đóng ticket**.
✅ *Kết quả:* ticket về "Đã đóng".

### Bảng cấp duyệt theo số tiền (Bước 4)
| Số tiền hoàn/bù | Ai duyệt | Tài khoản |
|---|---|---|
| ≤ 500.000đ | Trưởng nhóm CSKH | `lead1` |
| ≤ 3.000.000đ | Trưởng dự án | `tdabg1` |
| ≤ 10.000.000đ | TPKD / Kế toán trưởng | `tpkd1` / `ktt1` |
| > 10.000.000đ | Ban Giám đốc | `gd1` |

### Các biến thể để test thêm
- **Số tiền lớn:** đổi `so_tien_gia_tri` thành `8000000` khi tạo (Bước 1) → chỉ `tpkd1` duyệt được, `lead1`/`tdabg1` bị chặn.
- **TH4 (giao dịch treo, tự đóng):** tạo ticket `"loai_th":"TH4"` rồi Portal chạy:
```
curl -s -X POST http://localhost:8069/api/octa/v1/tickets/close \
 -H "X-Api-Key: CHANGE_ME_UAT_KEY" -H "Content-Type: application/json" \
 -d '{"request_id":"close-1","loai_th":"TH4","ma_gd_goc":"GD-DEMO-01"}'
```
→ Ticket **tự đóng**, không cần nhân viên thao tác.
- **TH5/TH6/TH7:** tạo ticket các loại này → hệ thống tự sinh thêm **1 ticket nội bộ** (xem ở bộ lọc "Ticket nội bộ").
- **Chống tạo trùng:** chạy lại y hệt lệnh Bước 1 (cùng `request_id`) → trả về đúng ticket cũ, **không tạo thêm**.

---

## LUỒNG 5 — Nộp & duyệt báo cáo

**Bước 1 — Nhân viên nộp báo cáo.**
Đăng nhập `cskh1` → menu **Báo cáo Octa → Bảng báo cáo** → chọn loại "Báo cáo ngày CSKH" bấm **Tạo** → nhập *Tóm tắt đầu việc trong ca* → bấm **Nộp báo cáo**.
→ Hệ thống **tự tính hạn nộp** (báo cáo ngày: trước 9:30 hôm sau).

**Bước 2 — Cấp trên duyệt.**
Đăng nhập `tdabg1` → **Báo cáo Octa → Báo cáo chờ duyệt** → mở → **Duyệt**.
✅ *Kết quả:* báo cáo "Đã duyệt". Nếu nộp trễ hạn, báo cáo hiện cảnh báo đỏ "Quá hạn".

---

## LUỒNG 6 — Xem KPI & Bảng điều hành

**Bước 1 — Sinh KPI.**
Đăng nhập `lead1` → menu **KPI → Sinh KPI tháng** (hệ thống tính SLA đúng hạn %, giải quyết lần đầu %, tỷ lệ tái phát, xếp loại A/B/C cho từng nhân viên).

**Bước 2 — Xem KPI.**
`lead1` → **KPI → KPI của tôi** → xem điểm & xếp loại.

**Bước 3 — Bảng điều hành.**
`lead1` (hoặc `tdabg1`, `tpkd1`) → menu **Điều hành Octa → Bảng điều hành** →
chọn từng mục ở thanh bên trái: Ranh đỏ · Cổng/API · NCC · Đại lý · Công nợ · CSKH & Ticket · KPI nhóm.
✅ *Kết quả:* mỗi vai trò thấy phạm vi dữ liệu tương ứng.

---

## B. Bảng tự đánh giá sau khi test

| Luồng | Test đạt? | Ghi chú |
|---|---|---|
| 1. Xử lý ticket khách hàng | ☐ | |
| 2. Bàn giao ca | ☐ | |
| 3. Phê duyệt hoàn tiền + escalate | ☐ | |
| 4. Vòng đời 6 (Portal API) | ☐ | |
| 5. Nộp & duyệt báo cáo | ☐ | |
| 6. KPI & bảng điều hành | ☐ | |

---

## C. Lưu ý cho Phòng Công nghệ
- Các lệnh `curl` chạy ở **cửa sổ Terminal riêng** (khác cửa sổ đang chạy hệ thống).
- Khóa API demo là `CHANGE_ME_UAT_KEY` — sẽ đổi khóa thật + giới hạn IP khi lên môi trường chính thức.
- Chi tiết kỹ thuật 5 API xem file **Dac_ta_API_Odoo_VongDoi6.docx**.

---
*Mọi thao tác đều được hệ thống ghi nhật ký (ai làm, lúc nào) để tra soát.*
