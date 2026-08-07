# ĐẶC TẢ API ODOO CUNG CẤP CHO PORTAL
## Nghiệp vụ Hoàn / Hủy / Điều chỉnh giao dịch — Vòng đời 6

| | |
|---|---|
| Bên cung cấp API (server) | Đội Odoo — CÔNG TY CP DỊCH VỤ TRỰC TUYẾN OCTA |
| Bên tích hợp (client) | Phòng Công nghệ — Hệ thống Portal |
| Phiên bản | v1.0 |
| Ngày | 04/2026 |

Tài liệu đặc tả **5 API** Odoo cung cấp để Portal tích hợp. Portal là bên gọi (client), Odoo là bên cung cấp (server).

---

## 1. Quy ước chung

**Base URL**
| Môi trường | URL |
|---|---|
| UAT | `https://uat-odoo.octa.vn/api/octa/v1` |
| Production | `https://odoo.octa.vn/api/octa/v1` |

**Header bắt buộc**
| Header | Mô tả |
|---|---|
| `Content-Type` | `application/json; charset=utf-8` |
| `X-Api-Key` | Khóa bí mật cấp riêng cho Portal theo môi trường |
| `X-Request-Id` | UUID, trùng `request_id` trong body (API ghi dữ liệu) |

**Định dạng response** — mọi API dùng chung khung:
```json
{ "success": true, "data": { }, "error": null }
```
Khi lỗi:
```json
{ "success": false, "data": null,
  "error": { "code": "TICKET_CLOSED", "message": "Ticket đã đóng, không thể cập nhật lại." } }
```
HTTP `200` cho mọi kết quả nghiệp vụ hợp lệ (kể cả `duoc_phep=false`); `401/500` cho lỗi kỹ thuật.

**Chống trùng (idempotency)**: API-1, API-4, API-5 bắt buộc có `request_id`. Gọi lại cùng `request_id` → Odoo trả kết quả đã lưu, không tạo/ghi lần 2.

**Datetime**: ISO-8601 kèm múi giờ, ví dụ `2026-04-10T09:12:00+07:00`.

---

## 2. Danh mục enum

| Nhóm | Giá trị |
|---|---|
| loai_th | `TH1 TH2 TH3 TH4 TH5 TH6 TH7 TH8` |
| loai_ticket | `TICKET_KHACH` · `TICKET_NOI_BO` |
| trang_thai | `MOI_TAO · DANG_XAC_MINH · CHO_PHE_DUYET · DA_DUYET · CHO_DOI_SOAT · DA_DOI_SOAT · DA_DONG · TU_CHOI` |
| phuong_an | `HOAN_TIEN · HOAN_MA · NAP_BU · CAP_NHAT_TRANG_THAI_GIAO_DICH · HE_THONG_TU_XU_LY` |
| trang_thai_gd_goc | `0` Thất bại · `2` Đang xử lý · `3` Thành công |
| nguon_phat_hien | `KHIEU_NAI_KH · CANH_BAO_HE_THONG · PHAT_HIEN_DOI_SOAT` |
| role (nhom_phu_trach) | `OWNER` · `SUPPORT` |

---

## 3. API-1 — Tạo ticket khách
`POST /tickets`

**Request**
| Trường | Kiểu | BB | Mô tả |
|---|---|---|---|
| request_id | string(uuid) | Có | Chống trùng |
| ma_gd_goc | string | Có | Mã giao dịch gốc |
| trang_thai_gd_goc | enum | Có | 0 / 2 / 3 |
| so_tien_gia_tri | number | Có | Giá trị ảnh hưởng — quyết định cấp duyệt |
| loai_th | enum | Có | TH1–TH8 |
| mo_ta_su_vu | string | Có | Nội dung sự vụ |
| nguon_phat_hien | enum | Có | |
| phuong_an_de_xuat | enum | Có | |
| nguoi_tao | string | Có | Tài khoản CSKH trên Portal |

**Response `data`**
| Trường | Kiểu | Mô tả |
|---|---|---|
| ma_ticket | string | Mã ticket Odoo vừa sinh |
| trang_thai | enum | Mặc định `MOI_TAO` |
| thoi_gian_tao | datetime | |
| loai_th | enum | |
| nhom_phu_trach | array | Mỗi phần tử: `team_code`, `team_name`, `role` |
| phuong_an_de_xuat | enum | |
| ticket_khach_lien_ket | string/null | Mã ticket khách đã đóng trước đó (nếu có) |

**Quy tắc**: thiếu `ma_gd_goc`/`loai_th` hoặc `loai_th` ngoài TH1–TH8 → lỗi. `request_id` trùng → trả `ma_ticket` cũ. Luôn gắn `TICKET_KHACH`. 1 giao dịch được có nhiều ticket khác thời điểm. Odoo tự phân công `nhom_phu_trach` theo `loai_th`.

**Sample**
```json
// Request
{ "request_id":"7b2f1c40-...","ma_gd_goc":"GD00012345","trang_thai_gd_goc":3,
  "so_tien_gia_tri":250000,"loai_th":"TH1","mo_ta_su_vu":"Thẻ 100k không nạp được",
  "nguon_phat_hien":"KHIEU_NAI_KH","phuong_an_de_xuat":"HOAN_TIEN","nguoi_tao":"cskh01" }
// Response
{ "success":true,"error":null,"data":{
  "ma_ticket":"TK-2026-000123","trang_thai":"MOI_TAO",
  "thoi_gian_tao":"2026-04-10T09:12:00+07:00","loai_th":"TH1",
  "nhom_phu_trach":[{"team_code":"CSKH","team_name":"CSKH","role":"OWNER"},
                    {"team_code":"KT","team_name":"Kế toán","role":"SUPPORT"}],
  "phuong_an_de_xuat":"HOAN_TIEN","ticket_khach_lien_ket":null } }
```

---

## 4. API-2 — Lấy ticket theo giao dịch
`GET /tickets?ma_gd_goc={ma_gd_goc}`

**Request**: query `ma_gd_goc` (Có).

**Response `data`**: mảng ticket, mỗi bản ghi gồm: `ma_ticket, ma_gd_goc, trang_thai_gd_goc, so_tien_gia_tri, loai_ticket, loai_th, nguon_phat_hien, mo_ta_su_vu, trang_thai, nhom_phu_trach, phuong_an_de_xuat, phuong_an_da_duyet, nguoi_tao, nguoi_xac_minh, nguoi_xu_ly, nguoi_duyet, ticket_noi_bo_lien_ket, ticket_khach_lien_ket, ma_phuong_an_da_thuc_hien, thoi_gian_tao, thoi_gian_de_xuat, thoi_gian_duyet, thoi_gian_xac_nhan_doi_soat_khop, thoi_gian_dong, ket_qua_cuoi`.

**Quy tắc**: chưa có ticket → trả `[]`. Sắp xếp `thoi_gian_tao` giảm dần.

**Sample response**
```json
{ "success":true,"error":null,"data":[
  { "ma_ticket":"TK-2026-000123","ma_gd_goc":"GD00012345","loai_ticket":"TICKET_KHACH",
    "loai_th":"TH1","trang_thai":"DA_DUYET","phuong_an_de_xuat":"HOAN_TIEN",
    "phuong_an_da_duyet":true,"nguoi_duyet":"lead_cskh","thoi_gian_tao":"2026-04-10T09:12:00+07:00",
    "ket_qua_cuoi":null } ] }
```

---

## 5. API-3 — Kiểm tra điều kiện thực hiện phương án
`POST /tickets/check-condition`

**Request**
| Trường | Kiểu | BB | Mô tả |
|---|---|---|---|
| ma_gd_goc | string | Có | Mã giao dịch gốc |
| phuong_an_du_kien | enum | Có | Phương án Portal muốn thực hiện |

**Response `data`**
| Trường | Kiểu | Mô tả |
|---|---|---|
| duoc_phep | boolean | true = được tạo GD xử lý; false = chặn |
| ma_ticket_lien_quan | string | Ticket căn cứ (khi `duoc_phep=true`) |
| phuong_an_de_xuat | enum | Phải trùng `phuong_an_du_kien` |
| phuong_an_da_duyet | boolean | |
| nguoi_duyet | string | |
| ly_do_tu_choi | string | Bắt buộc khi `duoc_phep=false` |

**Quy tắc**: tìm ticket khách đang mở theo `ma_gd_goc`; `duoc_phep=true` khi ticket ở `DA_DUYET` và phương án khớp. Ngược lại `false` + `ly_do_tu_choi` rõ ràng (đây là kết quả nghiệp vụ, không phải lỗi).

**Sample**
```json
// Request
{ "ma_gd_goc":"GD00012345","phuong_an_du_kien":"HOAN_TIEN" }
// Response (được phép)
{ "success":true,"error":null,"data":{
  "duoc_phep":true,"ma_ticket_lien_quan":"TK-2026-000123",
  "phuong_an_de_xuat":"HOAN_TIEN","phuong_an_da_duyet":true,"nguoi_duyet":"lead_cskh",
  "ly_do_tu_choi":null } }
// Response (bị chặn)
{ "success":true,"error":null,"data":{
  "duoc_phep":false,"ma_ticket_lien_quan":null,"phuong_an_de_xuat":null,
  "phuong_an_da_duyet":false,"nguoi_duyet":null,
  "ly_do_tu_choi":"Phương án chưa được phê duyệt." } }
```

---

## 6. API-4 — Cập nhật kết quả thực hiện phương án
`POST /tickets/execution-result`

**Request**
| Trường | Kiểu | BB | Mô tả |
|---|---|---|---|
| request_id | string(uuid) | Có | Chống ghi trùng |
| ma_ticket | string | Có | Lấy từ API-3 |
| ma_gd_goc | string | Có | Đối chiếu chéo |
| trang_thai_gd_goc | enum | Có | |
| phuong_an_da_thuc_hien | enum | Có | Phải khớp phương án đã duyệt |
| ma_phuong_an_da_thuc_hien | string | Không | Mã yêu cầu nạp tiền / GD nạp bù; null nếu cập nhật trạng thái |
| nguoi_xu_ly | string | Có | |
| thoi_gian_thuc_hien | datetime | Có | |

**Response `data`**: `success, ma_ticket, thoi_gian_cap_nhat, error_message`.

**Quy tắc**: chỉ nhận khi ticket đang `DA_DUYET`; đã đóng → `TICKET_CLOSED`. Phương án lệch → `PLAN_MISMATCH`. `request_id` trùng → trả kết quả cũ. API chỉ ghi thông tin thực hiện; việc chuyển trạng thái ticket do người dùng thao tác trên Odoo.

**Sample**
```json
// Request
{ "request_id":"9a1e-...","ma_ticket":"TK-2026-000123","ma_gd_goc":"GD00012345",
  "trang_thai_gd_goc":3,"phuong_an_da_thuc_hien":"HOAN_TIEN",
  "ma_phuong_an_da_thuc_hien":"NAPTIEN-778899","nguoi_xu_ly":"cskh01",
  "thoi_gian_thuc_hien":"2026-04-10T11:30:00+07:00" }
// Response
{ "success":true,"error":null,"data":{
  "ma_ticket":"TK-2026-000123","thoi_gian_cap_nhat":"2026-04-10T11:30:05+07:00",
  "error_message":null } }
```

---

## 7. API-5 — Đóng ticket (riêng TH4)
`POST /tickets/close`

**Request**
| Trường | Kiểu | BB | Mô tả |
|---|---|---|---|
| request_id | string(uuid) | Có | Chống ghi trùng |
| loai_th | enum | Có | Thực tế luôn `TH4` |
| ma_gd_goc | string | Có | Đối chiếu chéo |

**Response `data`**: `success, ma_ticket, thoi_gian_cap_nhat`.

**Quy tắc**: chỉ đóng khi ticket thuộc `TH4` và đang khác `DA_DONG`/`TU_CHOI`. `request_id` trùng → trả kết quả cũ.

**Sample**
```json
// Request
{ "request_id":"c3d5-...","loai_th":"TH4","ma_gd_goc":"GD00067890" }
// Response
{ "success":true,"error":null,"data":{
  "ma_ticket":"TK-2026-000200","thoi_gian_cap_nhat":"2026-04-10T14:05:00+07:00" } }
```

---

## 8. Máy trạng thái ticket

```
API-1 ─▶ MOI_TAO ─▶ DANG_XAC_MINH ─▶ CHO_PHE_DUYET ─▶ DA_DUYET
                          │                 │              │
                       TU_CHOI           TU_CHOI    API-3 → thực hiện → API-4
                                                          │
                                                    CHO_DOI_SOAT ⇄ (không khớp) DA_DUYET
                                                          │ (khớp)
                                                    DA_DOI_SOAT ─▶ DA_DONG
```
- **TH4**: sau `MOI_TAO`, Portal tự khớp trạng thái GD → gọi **API-5** → `DA_DONG`.
- **TH2**: thực hiện ngoài Portal, không gọi API-3/API-4; cập nhật trực tiếp trên Odoo.
- Bước đối soát có thể lặp lại; Odoo lưu vết đầy đủ mỗi lần chuyển trạng thái.

---

## 9. Bảng mã lỗi

| code | Ý nghĩa |
|---|---|
| VALIDATION_ERROR | Thiếu/sai trường bắt buộc |
| INVALID_TH | `loai_th` ngoài TH1–TH8 |
| TICKET_NOT_FOUND | Không tìm thấy ticket |
| NO_OPEN_TICKET | Không có ticket khách đang mở |
| NOT_APPROVED | Ticket chưa `DA_DUYET` |
| PLAN_MISMATCH | Phương án không khớp phương án đã duyệt |
| TICKET_CLOSED | Ticket đã `DA_DONG`/`TU_CHOI` |
| DUPLICATE_REQUEST | `request_id` đã xử lý (trả kết quả cũ) |
| UNAUTHORIZED | Sai/thiếu `X-Api-Key` |
| INTERNAL_ERROR | Lỗi hệ thống Odoo |

---
*— Hết —*
