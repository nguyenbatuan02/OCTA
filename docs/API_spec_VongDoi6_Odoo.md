# ĐẶC TẢ API TÍCH HỢP PORTAL ↔ ODOO — VÒNG ĐỜI 6
### Nghiệp vụ Hoàn / Hủy / Điều chỉnh giao dịch

| | |
|---|---|
| **Bên cung cấp API (server)** | Đội Odoo — CÔNG TY CP DỊCH VỤ TRỰC TUYẾN OCTA |
| **Bên tích hợp (client)** | Phòng Công nghệ — Hệ thống Portal |
| **Phiên bản** | Draft v0.1 — *gửi Phòng Công nghệ xác nhận* |
| **Ngày** | 04/2026 |
| **Căn cứ** | "Đặc tả yêu cầu API tích hợp Portal – Odoo v1.0"; "Tài liệu thiết kế nâng cấp Portal – Vòng đời 6" |

> Tài liệu này chốt lại **những quyết định kỹ thuật mà bản yêu cầu để đội Odoo tự đề xuất** (endpoint, method, auth, định dạng, mã lỗi, máy trạng thái, ánh xạ nhóm/hạn mức). Các mục đánh dấu 🔶 **cần Phòng Công nghệ xác nhận** trước khi lock spec để code.

---

## 1. Quy ước chung

### 1.1 Base URL & môi trường
| Môi trường | Base URL (🔶 xác nhận) |
|---|---|
| UAT | `https://uat-odoo.octa.vn/api/octa/v1` |
| Production | `https://odoo.octa.vn/api/octa/v1` |

- Giao thức: **HTTPS bắt buộc**. Định dạng: **JSON** (`Content-Type: application/json; charset=utf-8`).
- Ngôn ngữ thông báo lỗi: **tiếng Việt**.

### 1.2 Xác thực & bảo mật
- Header bắt buộc mỗi request:
  - `X-Api-Key: <khóa bí mật cấp riêng cho Portal>` 🔶
  - `X-Request-Id: <UUID>` — trùng giá trị `request_id` trong body (dùng cho idempotency).
- Chỉ IP của Portal được whitelist gọi API (IP allowlist). 🔶
- Khóa API cấp riêng theo môi trường (UAT/Prod), không dùng chung.

### 1.3 Định dạng response chuẩn (envelope)
Mọi API trả về cùng khung:
```json
{
  "success": true,
  "data": { },
  "error": null
}
```
Khi lỗi:
```json
{
  "success": false,
  "data": null,
  "error": { "code": "TICKET_CLOSED", "message": "Ticket đã đóng, không thể cập nhật lại." }
}
```
- HTTP status: `200` cho mọi kết quả nghiệp vụ hợp lệ (kể cả `duoc_phep=false` của API-3 — đó là kết quả nghiệp vụ, không phải lỗi hệ thống). `4xx/5xx` chỉ dùng cho lỗi kỹ thuật (sai auth, sai định dạng, lỗi server).

### 1.4 Idempotency (chống trùng)
- Mọi API **ghi dữ liệu** (API-1, API-4, API-5) bắt buộc có `request_id`.
- Odoo lưu `request_id` đã xử lý. Nếu nhận lại `request_id` cũ → **trả về kết quả đã lưu, không tạo/ghi lần 2**.
- API-2, API-3 là read-only → không cần idempotency.

### 1.5 Bảng mã lỗi (🔶 xác nhận/bổ sung)
| code | HTTP | Ý nghĩa |
|---|---|---|
| `VALIDATION_ERROR` | 200 | Thiếu/sai trường bắt buộc (kèm chi tiết trường). |
| `INVALID_TH` | 200 | `loai_th` không thuộc TH1–TH8. |
| `TICKET_NOT_FOUND` | 200 | Không tìm thấy ticket theo `ma_gd_goc`/`ma_ticket`. |
| `NO_OPEN_TICKET` | 200 | Không có ticket khách đang mở cho giao dịch. |
| `NOT_APPROVED` | 200 | Ticket chưa ở trạng thái `DA_DUYET`. |
| `PLAN_MISMATCH` | 200 | Phương án gửi lên không khớp phương án đã duyệt. |
| `TICKET_CLOSED` | 200 | Ticket đã `DA_DONG`/`TU_CHOI`. |
| `DUPLICATE_REQUEST` | 200 | `request_id` đã xử lý — trả kết quả cũ (success vẫn = true). |
| `UNAUTHORIZED` | 401 | Sai/thiếu `X-Api-Key`. |
| `INTERNAL_ERROR` | 500 | Lỗi hệ thống Odoo. |

---

## 2. Danh mục enum (đồng bộ 2 hệ thống)

**loai_th**: `TH1 TH2 TH3 TH4 TH5 TH6 TH7 TH8`

**loai_ticket**: `TICKET_KHACH` (chỉ tạo qua API-1) · `TICKET_NOI_BO` (Odoo tự sinh TH5/6/7, không qua API, ẩn với khách)

**trang_thai** (máy trạng thái — mục 5):
`MOI_TAO · DANG_XAC_MINH · CHO_PHE_DUYET · DA_DUYET · CHO_DOI_SOAT · DA_DOI_SOAT · DA_DONG · TU_CHOI`

**phuong_an** (`phuong_an_de_xuat` / `phuong_an_du_kien` / `phuong_an_da_thuc_hien`):
`HOAN_TIEN · HOAN_MA · NAP_BU · CAP_NHAT_TRANG_THAI_GIAO_DICH · HE_THONG_TU_XU_LY`

**trang_thai_gd_goc**: `2` = Đang xử lý · `3` = Thành công · `0` = Thất bại

**nguon_phat_hien**: `KHIEU_NAI_KH · CANH_BAO_HE_THONG · PHAT_HIEN_DOI_SOAT` 🔶 *(bản yêu cầu ghi bằng tiếng Việt; đề xuất mã hoá enum như trên — cần xác nhận)*

**role nhóm** (trong `nhom_phu_trach`): `OWNER` (chủ trì) · `SUPPORT` (phối hợp)

---

## 3. Đặc tả từng API

### API-1 — Tạo ticket khách — `POST /tickets`
**Request**
| Trường | Kiểu | BB | Mô tả |
|---|---|---|---|
| request_id | string(uuid) | ✓ | Chống trùng |
| ma_gd_goc | string | ✓ | Mã giao dịch gốc |
| trang_thai_gd_goc | enum | ✓ | 0/2/3 |
| so_tien_gia_tri | number | ✓ | Giá trị ảnh hưởng — quyết định cấp duyệt |
| loai_th | enum | ✓ | TH1–TH8 |
| mo_ta_su_vu | string | ✓ | Nội dung sự vụ |
| nguon_phat_hien | enum | ✓ | |
| phuong_an_de_xuat | enum | ✓ | |
| nguoi_tao | string | ✓ | Tài khoản CSKH trên Portal |

**Response `data`**: `success, ma_ticket, trang_thai(=MOI_TAO), thoi_gian_tao, loai_th, nhom_phu_trach[], phuong_an_de_xuat, ticket_khach_lien_ket(nullable)`

**Quy tắc Odoo**
1. Thiếu `ma_gd_goc`/`loai_th` hoặc `loai_th` ngoài TH1–TH8 → `VALIDATION_ERROR`/`INVALID_TH`.
2. `request_id` đã có → trả `ma_ticket` cũ (`DUPLICATE_REQUEST`, success=true).
3. Luôn gắn `loai_ticket=TICKET_KHACH`.
4. 1 `ma_gd_goc` được có nhiều ticket khác thời điểm; **chỉ chặn trùng theo `request_id`**, không chặn theo `ma_gd_goc`.
5. Nếu GD đã có ticket khách **đã đóng** trước đó → ghi mã đó vào `ticket_khach_lien_ket`.
6. Tự phân công `nhom_phu_trach` theo `loai_th` (bảng mục 4).

**Sample**
```json
// Request
{ "request_id":"7b2f...","ma_gd_goc":"GD00012345","trang_thai_gd_goc":3,
  "so_tien_gia_tri":250000,"loai_th":"TH1","mo_ta_su_vu":"Thẻ 100k không nạp được",
  "nguon_phat_hien":"KHIEU_NAI_KH","phuong_an_de_xuat":"HOAN_TIEN","nguoi_tao":"cskh01" }
// Response
{ "success":true,"data":{ "ma_ticket":"TK-2026-000123","trang_thai":"MOI_TAO",
  "thoi_gian_tao":"2026-04-10T09:12:00+07:00","loai_th":"TH1",
  "nhom_phu_trach":[{"team_code":"CSKH","team_name":"CSKH","role":"OWNER"},
                    {"team_code":"KT","team_name":"Kế toán","role":"SUPPORT"}],
  "phuong_an_de_xuat":"HOAN_TIEN","ticket_khach_lien_ket":null },"error":null }
```

### API-2 — Lấy ticket theo giao dịch — `GET /tickets?ma_gd_goc=...`
**Request**: query `ma_gd_goc` (✓).
**Response `data`**: `array` bản ghi ticket, mỗi bản ghi gồm đủ **các trường mục 5.5 của bản yêu cầu** (ma_ticket, trang_thai, phuong_an_de_xuat, phuong_an_da_duyet, người tạo/xác minh/xử lý/duyệt, ticket liên kết, các mốc thời gian, ket_qua_cuoi…).
**Quy tắc**: chưa có ticket → trả mảng rỗng `[]` (không phải lỗi). Sắp xếp `thoi_gian_tao` giảm dần.

### API-3 — Kiểm tra điều kiện thực hiện — `POST /tickets/check-condition`
**Request**: `ma_gd_goc`(✓), `phuong_an_du_kien`(✓).
**Response `data`**: `duoc_phep(bool), ma_ticket_lien_quan, phuong_an_de_xuat, phuong_an_da_duyet, nguoi_duyet, ly_do_tu_choi`.
**Quy tắc**: tìm ticket khách đang mở (chưa DA_DONG/TU_CHOI) theo `ma_gd_goc`; `duoc_phep=true` khi ticket ở `DA_DUYET` **và** `phuong_an_de_xuat == phuong_an_du_kien`. Ngược lại `duoc_phep=false` kèm `ly_do_tu_choi` (dùng mã lỗi `NO_OPEN_TICKET`/`NOT_APPROVED`/`PLAN_MISMATCH`/`TICKET_CLOSED` trong `ly_do_tu_choi`).

### API-4 — Cập nhật kết quả thực hiện — `POST /tickets/execution-result`
**Request**: `request_id`(✓), `ma_ticket`(✓), `ma_gd_goc`(✓), `trang_thai_gd_goc`(✓), `phuong_an_da_thuc_hien`(✓), `ma_phuong_an_da_thuc_hien`(có thể null), `nguoi_xu_ly`(✓), `thoi_gian_thuc_hien`(✓).
**Response `data`**: `success, ma_ticket, thoi_gian_cap_nhat, error_message`.
**Quy tắc**: chỉ nhận khi ticket đang `DA_DUYET`; nếu `DA_DONG`/`TU_CHOI` → `TICKET_CLOSED`. `phuong_an_da_thuc_hien` phải khớp phương án đã duyệt (lệch → `PLAN_MISMATCH`). `request_id` trùng → trả kết quả cũ. **API này chỉ ghi thông tin thực hiện**; việc chuyển trạng thái ticket do người dùng thao tác trên Odoo (upload bằng chứng + xác nhận).

### API-5 — Đóng ticket (riêng TH4) — `POST /tickets/close`
**Request**: `request_id`(✓), `loai_th`(✓, thực tế luôn TH4), `ma_gd_goc`(✓).
**Response `data`**: `success, ma_ticket, thoi_gian_cap_nhat`.
**Quy tắc**: chỉ đóng khi ticket thuộc **TH4** và đang khác `DA_DONG`/`TU_CHOI`. `request_id` trùng → trả kết quả cũ.

---

## 4. Ánh xạ nhóm phụ trách theo tình huống — 🔶 ĐỀ XUẤT, cần xác nhận
Team codes: `CSKH · VHTM · CN` (Công nghệ) · `KT` (Kế toán).

| TH | Mô tả | OWNER | SUPPORT |
|---|---|---|---|
| TH1 | Thẻ lỗi → hoàn tiền | CSKH | KT |
| TH2 | Thẻ lỗi → hoàn mã | CSKH | VHTM (khiếu nại NCC) |
| TH3 | Topup lỗi → hoàn/nạp bù | CSKH | CN, KT |
| TH4 | GD treo, NCC cập nhật được (tự xử lý) | VHTM | CN |
| TH5 | GD treo, NCC không cập nhật | CSKH | VHTM, CN |
| TH6 | Cập nhật sai (thất bại→thành công) | CSKH | KT *(+ ticket nội bộ)* |
| TH7 | Cập nhật sai (thành công→thất bại) | CSKH | KT *(+ ticket nội bộ)* |
| TH8 | Điều chỉnh GD đã ghi nhận | CSKH | KT |

---

## 5. Máy trạng thái ticket (state machine)

```
                 API-1
        (Portal) ─────▶ [MOI_TAO]
                           │ Odoo tự phân công nhóm theo loai_th
                           ▼
                     [DANG_XAC_MINH] ──(từ chối)──▶ [TU_CHOI] (đóng, có lý do)
                           │ upload bằng chứng + đề xuất phương án
                           ▼
                     [CHO_PHE_DUYET] ──(từ chối)──▶ [TU_CHOI]
                           │ cấp có thẩm quyền duyệt (theo hạn mức mục 6)
                           ▼
                       [DA_DUYET] ◀───────────┐
                           │                  │ (đối soát KHÔNG khớp → quay lại)
             Portal: API-3 (kiểm tra) → thực hiện phương án → API-4 (ghi kết quả)
             + người dùng upload bằng chứng & xác nhận trên Odoo
                           ▼                  │
                     [CHO_DOI_SOAT]           │
                           │ Kế toán đối soát │
                           ├──(không khớp)────┘
                           │ (khớp)
                           ▼
                     [DA_DOI_SOAT]
                           │ đóng ticket (có ket_qua_cuoi)
                           ▼
                       [DA_DONG]
```
**Ghi chú:**
- **TH4**: sau `MOI_TAO`, Portal tự khớp trạng thái GD rồi gọi **API-5** → ticket `DA_DONG` (bỏ qua các bước xác minh/duyệt/đối soát).
- **TH2**: thực hiện ngoài Portal → không gọi API-3/API-4; cập nhật bằng chứng trực tiếp trên Odoo.
- Bước đối soát có thể lặp lại (`CHO_DOI_SOAT`↔`DA_DUYET`); Odoo **lưu vết đầy đủ** mỗi lần chuyển trạng thái (người, thời điểm, kết quả).
- **Ticket nội bộ** (TH5/6/7): Odoo tự sinh `TICKET_NOI_BO`, vòng đời độc lập, không qua API, không hiển thị cho khách; liên kết 2 chiều qua `ticket_noi_bo_lien_ket`.

---

## 6. Ánh xạ hạn mức phê duyệt (theo `so_tien_gia_tri`)
| Khoảng giá trị | Cấp tự duyệt | Vượt → trình |
|---|---|---|
| ≤ 500.000đ | Trưởng nhóm CSKH | Trưởng dự án |
| ≤ 3.000.000đ | Trưởng dự án | TP KD / KTT |
| ≤ 10.000.000đ | TP KD (hoặc KTT với vấn đề số liệu) | Ban Giám đốc |
| > 10.000.000đ | Ban Giám đốc | – |

→ Odoo tự xác định cấp duyệt từ `so_tien_gia_tri`; ticket `CHO_PHE_DUYET` hiển thị ở dashboard cấp duyệt tương ứng; mỗi Duyệt/Từ chối ghi audit log.

---

## 7. Bảng SLA (giám sát nội bộ Odoo)
| Bước | SLA mục tiêu | Escalate |
|---|---|---|
| Tạo ticket | ≤ 15' từ khi phát hiện | Lead CSKH |
| Xác minh dữ liệu gốc | ≤ 4h | Trưởng nhóm CSKH |
| Đề xuất phương án | ≤ 1h | Lead CSKH |
| Phê duyệt | 4h (Lead/TP CSKH) · 24h (TP KD/KTT) · 48h (BGĐ) | Cấp cao hơn 1 bậc |
| Thực hiện phương án | ≤ 2h sau duyệt | Lead CSKH + KT |
| Đối soát | ≤ 24h | KTT |
| Đóng ticket | ≤ 2h sau đối soát khớp | Lead CSKH |

**End-to-end**: TH1/TH2/TH3 ≤ 24h · TH4–TH8 ≤ 48h.

---

## 8. Yêu cầu môi trường UAT & bàn giao
- **UAT** tách biệt production; cấp `X-Api-Key` UAT + whitelist IP Portal UAT.
- Đội Odoo bàn giao: **(1)** tài liệu này bản chốt, **(2)** Postman Collection đủ 5 API + 8 kịch bản TH, **(3)** bộ sample request/response thành công & lỗi, **(4)** sơ đồ máy trạng thái đã triển khai.
- Hai bên cùng test đủ **8 tình huống TH1–TH8** trên UAT trước khi go-live.

---

## 9. Danh sách điểm cần Phòng Công nghệ xác nhận (checklist 🔶)
1. Base URL UAT/Prod & cơ chế auth (`X-Api-Key` + IP allowlist) có phù hợp hạ tầng Portal?
2. Mã hoá enum `nguon_phat_hien` (tiếng Việt → mã) như mục 2.
3. Định dạng envelope response & bảng mã lỗi mục 1.5.
4. Ánh xạ `nhom_phu_trach` theo TH (mục 4).
5. Kiểu/độ dài `ma_ticket`, `ma_gd_goc`, `request_id` (giới hạn ký tự).
6. Múi giờ & định dạng datetime (đề xuất ISO-8601 `+07:00`).
7. API-2 dùng `GET` (query) hay `POST` (body) — theo chuẩn Portal.

---
*— Hết —*
