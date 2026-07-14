*OCTA – Tài liệu cấu hình Odoo 17 | Role: Trưởng dự án Bigtel | ODOO-CFG.KD.TDABG-01*

**CÔNG TY CỔ PHẦN DỊCH VỤ TRỰC TUYẾN OCTA**

*Mã: ODOO-CFG.KD.TDABG-01  |  Lần ban hành: 01  |  Ngày: ……/……/2026*

**TÀI LIỆU YÊU CẦU CẤU HÌNH VAI TRÒ**

**TRƯỞNG DỰ ÁN BIGTEL TRÊN ODOO 17**

*Dùng làm tài liệu yêu cầu cấu hình Odoo 17 cho đội kỹ thuật / Phòng Innovation*

| **Hạng mục** | **Nội dung** |
| --- | --- |
| **Tên role** | TDABG – Trưởng dự án Bigtel |
| **Phạm vi dữ liệu** | Chỉ Bigtel (toàn chuỗi 9 bước QT.KD.01). Không truy cập BigM/Ứng tiền Viettel. |
| **Báo cáo trực tiếp** | Phó phòng KD phụ trách Bigtel (tác nghiệp hằng ngày) + Trưởng phòng KD (kết quả, phê duyệt vượt hạn mức) |
| **Quản lý trực tiếp** | Lead Phát triển NCC; Lead Phát triển Đại lý; Lead VHTM & CSKH Bigtel; Tổ sản xuất |
| **Phê duyệt trước khi deploy** | Giám đốc + Trưởng phòng KD + Trưởng phòng Công nghệ + Trưởng phòng HCNS |

**PHẦN 1. TÓM TẮT VAI TRÒ TRƯỞNG DỰ ÁN BIGTEL TRÊN ODOO 17**

Trên Odoo 17, role "TDABG" là tầng thực thi – điều phối – phê duyệt hạn mức thấp nhất trong chuỗi KD → PPKD → TDABG, tập trung toàn bộ vào dự án Bigtel:

- Phạm vi dữ liệu: chỉ Bigtel. Không có bất kỳ quyền truy cập nào vào BigM, Ứng tiền Viettel.

- Chức năng chính: điều hành toàn bộ chuỗi 9 bước QT.KD.01 trong phạm vi Bigtel; phê duyệt trong hạn mức TDABG; cảnh báo và escalate PPKD/TPKD khi vượt hạn mức.

- Thao tác được phép: tạo phiếu đề xuất NCC, sản phẩm, giá/chiết khấu, cấu hình, mở/đóng cổng, giao việc nhóm, phê duyệt hoàn tiền/nạp bù trong hạn mức TDABG.

- Không được phép: cấu hình hệ thống Bigtel trực tiếp; ký hợp đồng NCC/đại lý vượt phân quyền; phê duyệt vượt hạn mức TDABG; truy cập tài chính vốn/thanh khoản/TSBĐ.

**Tầng phân quyền 3 cấp trong Bigtel:**

| **TPKD** | **PPKD** | **TDABG** |
| --- | --- | --- |
| Toàn Phòng KD | Bigtel + TC lớp TM | Chỉ Bigtel |
| Hạn mức cao nhất | Hạn mức giữa | Hạn mức thấp nhất |
| Phê duyệt chính sách lớn | Phê duyệt Bigtel trong phạm vi | Phê duyệt tác nghiệp trong hạn mức TDABG |
| Deal TC, quan hệ ngân hàng | Escalate vượt PPKD → TPKD | Escalate vượt TDABG → PPKD |

**PHẦN 2. NGUYÊN TẮC CẤU HÌNH ROLE**

| **Nguyên tắc** | **Nội dung áp dụng** |
| --- | --- |
| **Phạm vi dữ liệu chỉ Bigtel** | Record rules Odoo 17 phải lọc toàn bộ object (Sale Order, Purchase Order, Product, Partner, Ticket, Task, Inventory...) chỉ hiển thị dữ liệu thuộc Bigtel. BigM/UTV: không có menu, không có dữ liệu. |
| **3 tầng escalate rõ ràng** | Workflow phê duyệt phải cấu hình: TDABG approve (≤ hạn mức TDABG) → auto-escalate PPKD (≤ hạn mức PPKD) → auto-escalate TPKD. TDABG không thể bypass escalate. |
| **Không nắm trọn chuỗi QT.KD.01** | TDABG không được vừa là người đề xuất NCC vừa là người phê duyệt cuối. Vừa tạo phiếu cấu hình vừa confirm kết quả: cần thêm xác nhận của Phòng CN hoặc PPKD. |
| **Audit log bắt buộc** | Mọi thao tác Create/Approve/Reject/Stop/Escalate ghi đầy đủ log: user, timestamp, action, reason, attachment, scope = BIGTEL. |
| **Stop authority trong Bigtel** | TDABG có quyền ra lệnh dừng bán/đóng cổng/khóa kho ngay lập tức trong Bigtel khi chạm ranh đỏ; phải báo PPKD/TPKD trong vòng 1 giờ và bổ sung phê duyệt trong 2 giờ. |
| **Không tự cấu hình hệ thống** | Mọi thay đổi cấu hình Bigtel (giá, sản phẩm, cổng, API) phải qua phiếu yêu cầu kỹ thuật (BM.QT.KD.01.08) được TDABG phê duyệt rồi Phòng CN thực hiện. |
| **Ranh đỏ tự động khóa** | 5 lỗi liên tiếp/cổng → hệ thống tự đóng cổng + alert; 3 khiếu nại/60 phút/kho → hệ thống tự khóa kho + alert. TDABG nhận alert và phải xử lý trong 30 phút. |

**PHẦN 3. DANH SÁCH MODULE / MENU CẦN CÓ**

| **Module** | **Nghiệp vụ áp dụng** | **Mức quyền** |
| --- | --- | --- |
| **Sales (Bigtel)** | Doanh thu, sản lượng, đơn hàng, đại lý, chính sách giá Bigtel, chiết khấu | Xem + Tạo + Phê duyệt (hạn mức TDABG) |
| **CRM (Bigtel)** | Pipeline đại lý Bigtel, phát triển đại lý mới | Xem + Tạo |
| **Purchase (Bigtel)** | Hồ sơ NCC Bigtel, đề xuất NCC, SLA, công nợ NCC | Xem + Tạo phiếu đề xuất |
| **Inventory (Bigtel)** | Tồn kho mã PIN Bigtel, số dư API, nhập/xuất kho Bigtel | Xem + Tạo yêu cầu nhập/xuất |
| **Accounting (view)** | Công nợ NCC/đại lý Bigtel, đối soát doanh thu – không hạch toán | Xem (read-only) |
| **Helpdesk (Bigtel)** | Ticket CSKH Bigtel (CS01–CS15), hoàn tiền/nạp bù trong hạn mức TDABG | Xem + Phê duyệt (hạn mức TDABG) |
| **Project / Task** | Giao việc Lead các nhóm Bigtel, yêu cầu liên phòng Bigtel | Xem + Tạo + Assign |
| **HR (view – Bigtel)** | Danh sách nhân sự 4 nhóm Bigtel, KPI nhóm, đề xuất khen thưởng | Xem + Đề xuất |
| **Discuss** | Thông báo, alert, channel Bigtel, escalate lên PPKD/TPKD | Toàn bộ |
| **Dashboard/Reporting (Bigtel)** | Dashboard vận hành Bigtel: DT, SL, success/pending/error, tồn kho, CN, ticket | Xem + Xuất |
| **Approval (Bigtel workflow)** | Luồng phê duyệt hạn mức TDABG: NCC, giá, hoàn tiền, cổng, công nợ | Tạo + Phê duyệt + Từ chối + Escalate |

*⚠ Tất cả module trên chỉ hiển thị dữ liệu Bigtel. Record rule Odoo 17 lọc theo tag/project_id = BIGTEL. Không có menu nào dẫn đến dữ liệu BigM/UTV.*

**PHẦN 4. MA TRẬN QUYỀN CHI TIẾT THEO NHÓM NGHIỆP VỤ**

*✓ = Có quyền | ○ = Có điều kiện / cần phê duyệt | E = Escalate bắt buộc | — = Không có quyền*

| **Nhóm nghiệp vụ** | **Xem** | **Tạo** | **Sửa** | **Phê duyệt** | **Từ chối** | **Y/c cấu hình** | **Y/c dừng** | **Xuất BC** | **Drill-down** | **Xem log** | **Không được phép** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Kế hoạch KD & KPI Bigtel | ✓ | ✓ | ○ | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | Sửa KPI đã chốt PPKD/TPKD; xem KPI BigM/UTV |
| 2. DT/SL/Biên LN Bigtel | ✓ | — | — | — | — | — | — | ✓ | ✓ | ✓ | Sửa số đã phát sinh; xem DT BigM/UTV |
| 3. NCC Bigtel (đề xuất) | ✓ | ✓ | ○ | ○ | ○ | — | ○ | ✓ | ✓ | ✓ | Phê duyệt NCC vượt hạn mức TDABG; sửa pháp lý NCC |
| 4. Sản phẩm Bigtel (đề xuất mới) | ✓ | ✓ | ○ | ○ | ○ | — | — | ✓ | ✓ | ✓ | Mở bán khi chưa đủ phê duyệt; cấu hình trực tiếp |
| 5. Đại lý/KH Bigtel | ✓ | ✓ | ○ | ○ | ○ | — | ○ | ✓ | ✓ | ✓ | Xóa đại lý; sửa lịch sử GD; phê duyệt hạn mức vượt mức TDABG |
| 6. Giá/CK/Thưởng Bigtel | ✓ | ✓ | ○ | ○ | ○ | ✓ | ✓ | ✓ | ✓ | ✓ | Tự sửa giá ngoài WF; bán dưới giá sàn; vượt hạn mức TDABG |
| 7. Vận hành TM – Mở/đóng cổng | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Tự cấu hình trực tiếp; lệnh mở/đóng không có log |
| 8. CSKH/Hoàn tiền/Nạp bù Bigtel | ✓ | ○ | — | ○ | ○ | — | ✓ | ✓ | ✓ | ✓ | Cộng/trừ tiền ví KH trực tiếp; vượt hạn mức TDABG |
| 9. Công nợ NCC/đại lý Bigtel | ✓ | ✓ | — | ○ | ○ | — | ✓ | ✓ | ✓ | ✓ | Sửa số liệu công nợ KT; phê duyệt hạn mức vượt TDABG |
| 10. Đối soát DT/TK/API Bigtel | ✓ | — | — | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | Chốt số KT thay Phòng KT; sửa số liệu đã chốt |
| 11. BC, Dashboard, Alert Bigtel | ✓ | — | — | ✓ | — | — | — | ✓ | ✓ | ✓ | Thay đổi nguồn dữ liệu dashboard; xem dashboard BigM/UTV |
| 12. Nhân sự 4 nhóm Bigtel | ✓ | ○ | — | ○ | ○ | — | — | ✓ | ✓ | — | HĐ LĐ, lương chính thức, hồ sơ gốc; nhân sự phòng khác |
| 13. Phối hợp liên phòng Bigtel | ✓ | ✓ | — | — | — | — | ○ | ✓ | ✓ | — | Tự đóng task liên phòng khi chưa có xác nhận đầu ra |

*○ = Chỉ trong hạn mức TDABG theo Quy chế Phân quyền. Vượt hạn mức: hệ thống tự block và hiển thị nút Escalate PPKD.*

**PHẦN 5. DANH SÁCH WORKFLOW CẦN CẤU HÌNH**

*⚠ Tất cả workflow dưới đây được cấu hình 3 tầng: TDABG approve (≤ hạn mức) → PPKD approve (≤ hạn mức PPKD) → TPKD approve (nếu vượt PPKD). TDABG không thể bypass.*

**WF-BT-01: Đề xuất NCC Bigtel mới**

- Bước 1: Lead Phát triển NCC tạo hồ sơ BM.QT.KD.01.01 → Draft

- Bước 2: TDABG review hồ sơ → phê duyệt L1 (trong hạn mức TDABG)

- Bước 3: Phòng Tài chính thẩm định rủi ro, điều kiện đặt cọc/ký quỹ → Consulted

- Bước 4: Nếu trong hạn mức PPKD: PPKD phê duyệt L2. Nếu vượt: TPKD/GĐ phê duyệt cuối

- Bước 5: Phòng Kế toán xác nhận điều kiện thanh toán → Confirm

- Bước 6: Phòng Công nghệ kết nối API/cấu hình NCC → Done

*🔒 Ranh giới phân quyền: TDABG không tự tạo và tự approve cùng hồ sơ NCC. NCC vượt hạn mức TDABG: nút approve disable, hiện nút Escalate PPKD.*

**WF-BT-02: Phê duyệt sản phẩm Bigtel mới**

- Bước 1: TDABG hoặc Lead tạo phiếu đề xuất sản phẩm → Draft

- Bước 2: TDABG kiểm tra: NCC đã có, HĐ/phụ lục, giá, SLA → Approve L1

- Bước 3: PPKD phê duyệt L2 (nếu sản phẩm trọng yếu theo định nghĩa hạn mức)

- Bước 4: Phòng Kế toán xác nhận giá vốn → Confirm

- Bước 5: Phòng Công nghệ nhận BM.QT.KD.01.08 → cấu hình → TDABG nghiệm thu → Done

*🔒 Ranh giới phân quyền: Không mở bán khi chưa đủ phê duyệt TDABG (+ PPKD nếu cần). Phòng CN không cấu hình khi chưa có phiếu yêu cầu được phê duyệt.*

**WF-BT-03: Phê duyệt giá / chiết khấu Bigtel**

- Bước 1: TDABG hoặc Lead tạo phiếu đề xuất giá/CK (BM.QT.KD.01.02) → Draft

- Bước 2: Hệ thống tự so sánh với giá sàn và biên tối thiểu; block nếu < giá sàn

- Bước 3: TDABG phê duyệt (trong hạn mức TDABG) → Phòng KT đối chiếu giá vốn

- Bước 4: Phòng Công nghệ nhận yêu cầu cấu hình giá → Done

- Bước 5: Log lịch sử thay đổi giá ghi tự động.

*🔒 Ranh giới phân quyền: Đề xuất **<** giá sàn: block, không cho phê duyệt. Vượt hạn mức TDABG: auto-escalate PPKD.*

**WF-BT-04: Yêu cầu cấu hình bán Bigtel (BM.QT.KD.01.08)**

- Bước 1: TDABG tạo phiếu yêu cầu cấu hình (ghi rõ: sản phẩm, mệnh giá, giá, cổng, kho, thời điểm) → Draft

- Bước 2: TDABG phê duyệt (xác nhận đã có phê duyệt chính sách liên quan) → Approved

- Bước 3: Phòng Công nghệ nhận và thực hiện → In Progress → Done

- Bước 4: TDABG hoặc Lead VHTM nghiệm thu kết quả cấu hình trước khi mở bán.

*🔒 Ranh giới phân quyền: TDABG không tự cấu hình trực tiếp trên hệ thống. Mọi thay đổi cấu hình phải qua ticket có phê duyệt TDABG.*

**WF-BT-05: Mở / đóng cổng / kho Bigtel**

- Bước 1: TDABG hoặc Lead VHTM tạo lệnh mở/đóng (kèm lý do bắt buộc) → Draft

- Bước 2: TDABG phê duyệt → Approved

- Bước 3: Phòng Công nghệ thực thi → Done

- Bước 4: Hệ thống ghi log: người ra lệnh, người thực thi, timestamp, lý do.

- Bước 5: Lệnh đóng khẩn cấp (ranh đỏ): TDABG ra lệnh ngay → Phòng CN thực hiện → TDABG bổ sung phê duyệt trong 2 giờ, báo PPKD/TPKD trong 1 giờ.

*🔒 Ranh giới phân quyền: Lệnh không có lý do: hệ thống block. Lệnh khẩn cấp không có phê duyệt bổ sung trong 2 giờ: auto-alert PPKD.*

**WF-BT-06: Hoàn tiền / nạp bù Bigtel**

- Bước 1: CSKH tạo ticket → xác minh giao dịch → đề xuất hoàn/bù

- Bước 2: Lead CSKH phê duyệt (trong hạn mức Lead) → Done hoặc escalate TDABG

- Bước 3: TDABG phê duyệt (trong hạn mức TDABG) → Phòng KT lập chứng từ → Done

- Bước 4: Vượt hạn mức TDABG: nút approve disable → auto-escalate PPKD → TPKD → GĐ

- Bước 5: Phòng Kế toán hạch toán → ghi nhận → Done

*🔒 Ranh giới phân quyền: TDABG không cộng/trừ tiền ví KH trực tiếp. Hoàn tiền vượt hạn mức TDABG: block và escalate bắt buộc.*

**WF-BT-07: Cấp hạn mức công nợ đại lý / NCC Bigtel**

- Bước 1: TDABG hoặc Lead Đại lý tạo đề xuất hạn mức công nợ → Draft

- Bước 2: Phòng Kế toán cung cấp lịch sử công nợ → Consulted

- Bước 3: TDABG phê duyệt (trong hạn mức TDABG); vượt → escalate PPKD

- Bước 4: Phòng Tài chính thẩm định rủi ro (nếu hạn mức lớn) → Approve/Reject

- Bước 5: Hệ thống cập nhật hạn mức, ghi log.

*🔒 Ranh giới phân quyền: TDABG không sửa trực tiếp hạn mức công nợ ngoài workflow.*

**WF-BT-08: Xử lý chênh lệch đối soát Bigtel**

- Bước 1: Phòng KT hoặc TDABG phát hiện chênh lệch → tạo task

- Bước 2: TDABG phân công Lead xử lý trong nhóm Bigtel

- Bước 3: Lead xử lý, giải trình + đính kèm bằng chứng → Submitted

- Bước 4: TDABG phê duyệt giải trình nghiệp vụ phía Bigtel

- Bước 5: Phòng Kế toán xác nhận số liệu → Done

*🔒 Ranh giới phân quyền: TDABG không chốt số KT thay Phòng KT. Case chênh lệch lớn (vượt ngưỡng trọng yếu): auto-thông báo PPKD/TPKD.*

**WF-BT-09: Báo cáo ranh đỏ Bigtel**

- Bước 1: Hệ thống tự phát hiện ranh đỏ → alert TDABG + Lead liên quan + PPKD + TPKD

- Bước 2: TDABG xác nhận đã nhận → ra lệnh xử lý (trong 30 phút với Critical)

- Bước 3: TDABG ghi nhận hành động đã thực hiện, lý do, kết quả dự kiến

- Bước 4: TDABG báo cáo PPKD/TPKD trong 1 giờ

- Bước 5: PPKD hoặc TPKD đóng case sau khi xác nhận đã xử lý xong

*🔒 Ranh giới phân quyền: Case ranh đỏ Critical: TDABG không tự đóng case. PPKD/TPKD là người đóng case sau khi xác nhận.*

**WF-BT-10: Giao việc và đánh giá KPI nhóm Bigtel**

- Bước 1: TDABG tạo phiếu giao chỉ tiêu tháng/quý cho 4 Lead nhóm Bigtel (theo chỉ tiêu PPKD/TPKD đã giao TDABG)

- Bước 2: Lead ký nhận (confirm) trên Odoo 17

- Bước 3: Cuối kỳ: Lead tự đánh giá KPI → submit lên TDABG

- Bước 4: TDABG đánh giá, cho điểm, đề xuất xếp loại A/B/C lên PPKD

- Bước 5: PPKD chốt xếp loại; Phòng HCNS nhận đề xuất khen thưởng/kỷ luật

*🔒 Ranh giới phân quyền: TDABG chỉ đề xuất xếp loại, không chốt chính thức. TDABG không chỉnh sửa nguồn dữ liệu KPI (CMS Bigtel, log API).*

**PHẦN 6. DANH SÁCH DASHBOARD CẦN CẤU HÌNH**

| **Mã** | **Tên Dashboard** | **Tần suất** | **Chỉ tiêu / Nội dung tối thiểu** |
| --- | --- | --- | --- |
| **DB-BT-01** | **Dashboard Vận hành Bigtel ngày (realtime)** | Realtime (≤3 phút) | DT mệnh giá, DT Octa thực hưởng, SL, biên LN tạm tính theo SP/NCC/cổng; success/pending/error rate; tồn kho mã; số dư API; ticket mới; hoàn-bù; cảnh báo ranh đỏ. |
| **DB-BT-02** | **Dashboard Ranh đỏ Bigtel** | Realtime | 10 ranh đỏ Bigtel: màu đỏ/vàng/xanh; timestamp kích hoạt; hành động đã thực hiện; người phụ trách; trạng thái xử lý. |
| **DB-BT-03** | **Dashboard NCC Bigtel** | Ngày/tuần | Danh mục NCC đang hoạt động; tỷ trọng SL (≤50%); success/pending/error từng NCC; SLA; công nợ NCC; NCC dự phòng. |
| **DB-BT-04** | **Dashboard Đại lý Bigtel** | Ngày | Đại lý active/inactive; DT/SL/biên LN theo đại lý; tỷ trọng ≤40%; tuổi nợ; hạn mức công nợ vs thực tế; tỷ lệ đại lý hoạt động. |
| **DB-BT-05** | **Dashboard Cổng/API/Tồn kho** | Realtime | Trạng thái từng cổng (Active/Error/Closed); success/pending/error từng cổng; số dư API theo NCC; tồn kho mã theo mệnh giá/loại; ngưỡng cảnh báo/an toàn/đóng kho tự động. |
| **DB-BT-06** | **Dashboard Công nợ Bigtel** | Ngày | Công nợ NCC (phải trả); công nợ đại lý (phải thu); tuổi nợ 0-30/31-60/61-90/>90 ngày; danh sách vượt hạn mức. |
| **DB-BT-07** | **Dashboard CSKH ****&**** Ticket Bigtel** | Ngày | Ticket CS01-CS15: mới/pending/đóng; SLA%; FCR%; tỷ lệ tái phát; hoàn-bù theo ngày/tuần; ticket báo cáo PPKD. |
| **DB-BT-08** | **Dashboard Doanh thu theo cơ cấu SP** | Tuần/tháng | Cơ cấu DT theo Topup/API, Mã PIN, Dịch vụ số khác; so sánh vs định hướng BGĐ phê duyệt; xu hướng tháng; biên LN từng nhóm. |
| **DB-BT-09** | **Dashboard KPI nhóm Bigtel** | Tháng/quý | KPI 4 Lead nhóm và từng nhân viên Bigtel; tiến độ vs chỉ tiêu; xếp loại A/B/C. |

**PHẦN 7. DANH SÁCH CẢNH BÁO REALTIME / EMAIL / ODOO 17 NOTIFICATION**

| **Mã** | **Tên cảnh báo** | **Điều kiện kích hoạt** | **Tần suất** | **Người nhận** | **Mức** |
| --- | --- | --- | --- | --- | --- |
| **ALT-BT-01** | **≥ 5 GD lỗi liên tiếp/cổng** | Hệ thống tự đóng cổng + alert | Realtime | TDABG + Lead VHTM + Phòng CN + PPKD | **Critical** |
| **ALT-BT-02** | **≥ 3 khiếu nại/60 phút/kho** | Hệ thống tự khóa kho + alert | Realtime | TDABG + Lead CSKH + Tổ SX + PPKD | **Critical** |
| **ALT-BT-03** | **Pending vượt SLA** | Pending > SLA định nghĩa | Realtime | TDABG + Lead VHTM + Phòng CN | **High** |
| **ALT-BT-04** | **Tồn kho mã ****<**** mức cảnh báo** | Tồn kho mệnh giá X < ngưỡng | 10 phút | TDABG + Lead PT NCC + Phòng TC | **High** |
| **ALT-BT-05** | **Tồn kho mã ****<**** mức đóng kho** | Tồn kho < ngưỡng đóng kho tự động | Realtime | TDABG + Lead PT NCC + Phòng TC + PPKD | **Critical** |
| **ALT-BT-06** | **Số dư API ****<**** nhu cầu 7 ngày** | Số dư API/NCC < 7 ngày nhu cầu | 10 phút | TDABG + Lead PT NCC + Phòng TC | **High** |
| **ALT-BT-07** | **Đại lý Bigtel ****>**** 40% DT 1 SP** | Tỷ trọng đại lý vượt ngưỡng | Hàng ngày | TDABG + Lead PT Đại lý + PPKD | **Critical** |
| **ALT-BT-08** | **NCC Bigtel ****>**** 50% SL/dòng SP** | Tỷ trọng NCC vượt ngưỡng | Hàng tuần | TDABG + Lead PT NCC + PPKD | **High** |
| **ALT-BT-09** | **Công nợ đại lý vượt hạn mức** | Công nợ > hạn mức đã duyệt | Hàng ngày | TDABG + Lead PT Đại lý + Phòng KT | **High** |
| **ALT-BT-10** | **Nợ quá hạn ****>**** ngưỡng** | Tuổi nợ > ngưỡng cảnh báo | Hàng tuần | TDABG + Phòng KT | **Medium** |
| **ALT-BT-11** | **Chênh lệch CMS vs KT ****>**** 24h** | Chưa giải trình > 24 giờ | Hàng ngày | TDABG + Phòng KT + PPKD | **High** |
| **ALT-BT-12** | **Hoàn tiền/nạp bù vượt hạn mức TDABG** | Yêu cầu > hạn mức TDABG | Theo phát sinh | TDABG (block) + PPKD nhận escalate | **High** |
| **ALT-BT-13** | **Cổng/hệ thống Bigtel lỗi diện rộng** | Đa cổng / đa KH bị ảnh hưởng | Realtime | TDABG + Phòng CN + PPKD + TPKD + GĐ | **Critical** |
| **ALT-BT-14** | **Nghi ngờ gian lận** | Pattern GD bất thường | Realtime | TDABG + PPKD + TPKD + GĐ | **Critical** |
| **ALT-BT-15** | **Báo cáo Bigtel quá hạn** | BC > hạn mà chưa submit | Ngày đến hạn | TDABG + PPKD | **Medium** |

**PHẦN 8. DANH SÁCH BÁO CÁO BẮT BUỘC**

| **Mã BC** | **Tên báo cáo** | **Tần suất** | **Người nhận** | **Phê duyệt** | **Trạng thái DL** | **Nguồn** |
| --- | --- | --- | --- | --- | --- | --- |
| **BC-BT-01** | **BC vận hành Bigtel ngày** | Hằng ngày (trước 9:30) | PPKD; TPKD | TDABG phê duyệt | Tạm tính | CMS Bigtel, log API, ticket |
| **BC-BT-02** | **BC Bigtel tuần** | Thứ Hai (trước 10:00) | PPKD; TPKD; KT/TC theo nội dung | TDABG phê duyệt | Tạm tính | CMS + KT + log + ticket |
| **BC-BT-03** | **BC Bigtel tháng (kèm đối soát)** | Ngày làm việc thứ 5 tháng kế tiếp | PPKD; TPKD; BGĐ | TDABG phê duyệt + Phòng KT xác nhận | Đã đối soát | CMS + KT + TC + HCNS |
| **BC-BT-04** | **BC Bigtel quý/năm** | Theo lịch tổng kết Phòng KD | PPKD; TPKD; BGĐ; HCNS | TDABG + PPKD duyệt | Đã chốt | Tổng hợp BC tháng |
| **BC-BT-05** | **BC đột xuất (ranh đỏ, sự cố)** | Trong 1 giờ kể từ khi phát hiện | PPKD; TPKD; BGĐ; Phòng CN/KT liên quan | TDABG phê duyệt | Thực tế | Alert log + điều tra thực địa |
| **BC-BT-06** | **BC đối soát DT/CN/TK Bigtel** | Tuần/tháng | Phòng KT; PPKD; TPKD | TDABG + Phòng KT xác nhận | Đã đối soát | CMS Bigtel + sổ KT |
| **BC-BT-07** | **BC NCC Bigtel (đánh giá định kỳ)** | Tháng/quý | PPKD; TPKD; Phòng TC | TDABG phê duyệt | Thực tế | Log API, SLA, công nợ NCC |
| **BC-BT-08** | **BC KPI 4 nhóm Bigtel** | Tháng/quý | PPKD; HCNS | TDABG đề xuất; PPKD chốt | Thực tế | CMS Bigtel + đánh giá nội bộ |

**PHẦN 9. PHẠM VI DỮ LIỆU ĐƯỢC XEM / THAO TÁC / KHÔNG ĐƯỢC TRUY CẬP**

**9.1. Dữ liệu được xem toàn bộ – Full Read (chỉ Bigtel)**

- DT mệnh giá, DT Octa thực hưởng, SL, biên LN Bigtel theo ngày/tuần/tháng/SP/NCC/cổng/đại lý.

- Hồ sơ NCC Bigtel: điều kiện HĐ, SLA, success/pending/error từng NCC, công nợ, tỷ trọng.

- Danh mục đại lý Bigtel: phân hạng, DT, tỷ trọng ≤40%, công nợ, hạn mức.

- Trạng thái cổng Bigtel, số dư API từng NCC, tồn kho mã PIN (realtime).

- Ticket CSKH Bigtel (CS01–CS15): nội dung, trạng thái, SLA, người xử lý.

- Công nợ NCC/đại lý Bigtel (view Phòng KT – không sửa).

- Log mở/đóng cổng/kho Bigtel (do chính TDABG và Lead tạo).

- Biên bản đối soát Bigtel đã ký.

- Dashboard vận hành Bigtel (9 dashboard tại Phần 6).

**9.2. Dữ liệu được tạo / thao tác (Write/Action)**

- Tạo phiếu đề xuất NCC Bigtel mới (BM.QT.KD.01.01).

- Tạo phiếu đề xuất sản phẩm Bigtel mới.

- Tạo phiếu đề xuất giá/chiết khấu Bigtel (BM.QT.KD.01.02).

- Tạo phiếu yêu cầu cấu hình Bigtel (BM.QT.KD.01.08).

- Tạo/phê duyệt lệnh mở/đóng cổng/kho Bigtel (trong hạn mức TDABG).

- Phê duyệt hoàn tiền/nạp bù Bigtel (trong hạn mức TDABG).

- Tạo phiếu giao chỉ tiêu KPI cho 4 Lead nhóm Bigtel.

- Tạo task giao việc liên phòng (phạm vi Bigtel).

- Phê duyệt giải trình đối soát nghiệp vụ phía Bigtel.

- Phê duyệt BC vận hành Bigtel ngày/tuần/tháng trước khi gửi PPKD.

**9.3. Dữ liệu chỉ xem, không được sửa (Read-Only Strict)**

- Số liệu DT, công nợ, tồn kho Bigtel đã phát sinh và ghi nhận trên hệ thống.

- Số liệu kế toán đã hạch toán (sổ Fast/Odoo Accounting).

- Log giao dịch gốc từ Bigtel CMS và API (Phòng CN owner).

- Hồ sơ pháp lý NCC (giấy phép, HĐ gốc – lưu tại Phòng KT/Pháp chế).

- Hồ sơ nhân sự gốc, HĐLĐ, lương chính thức 4 nhóm Bigtel (Phòng HCNS owner).

- Dữ liệu tài chính vốn/thanh khoản/TSBĐ (Phòng TC owner).

**9.4. Dữ liệu không được truy cập**

- Admin hệ thống Bigtel/BigM/Odoo (API key, cấu hình kỹ thuật lõi, database).

- Log kỹ thuật server (Phòng CN).

- Bất kỳ dữ liệu nào thuộc BigM, Ứng tiền Viettel.

- Tài khoản ngân hàng, TSBĐ, quyết định giải ngân (Phòng TC).

- Thông tin deal tài chính lớp thương mại (Phòng TC + PPKD/TPKD owner).

- Dashboard/BC của Phòng KSNB, Phòng Innovation khi chưa được chia sẻ.

**PHẦN 10. DANH SÁCH RANH ĐỎ PHẢI KHÓA THAO TÁC HOẶC BUỘC ESCALATE**

| **Mã RD** | **Tình huống** | **Hành động hệ thống / TDABG bắt buộc** | **Người nhận/xử lý** |
| --- | --- | --- | --- |
| **RD-BT-01** | ≥ 5 GD lỗi liên tiếp/cổng Bigtel | Hệ thống TỰ ĐỘNG đóng cổng; alert TDABG + Phòng CN + PPKD. TDABG confirm xử lý trong 30 phút; báo PPKD trong 1 giờ. | TDABG + Phòng CN + PPKD |
| **RD-BT-02** | ≥ 3 khiếu nại/60 phút/kho | Hệ thống TỰ ĐỘNG khóa kho; alert TDABG + Lead CSKH + Tổ SX. TDABG rà soát lô + phối hợp NCC. | TDABG + Lead CSKH + Tổ SX |
| **RD-BT-03** | Đại lý Bigtel > 40% DT 1 SP | Alert TDABG + PPKD; block mở rộng hạn mức đại lý đó; TDABG đề xuất tái cơ cấu trình PPKD. | TDABG + PPKD + TPKD |
| **RD-BT-04** | NCC > 50% SL/dòng SP Bigtel | Alert TDABG + PPKD; TDABG lập kế hoạch đa nguồn trình PPKD trong tuần. | TDABG + PPKD |
| **RD-BT-05** | Công nợ đại lý/NCC vượt hạn mức | Hệ thống block cấp công nợ tiếp; alert TDABG + Phòng KT + Phòng TC; TDABG dừng cấp hàng/đóng cổng đại lý. | TDABG + Phòng KT + Phòng TC + PPKD |
| **RD-BT-06** | Giá đề xuất < giá sàn | Block workflow; disable nút approve; hiển thị cảnh báo rõ ràng. TDABG phải điều chỉnh giá hoặc escalate. | TDABG + Phòng KT |
| **RD-BT-07** | Hoàn tiền/nạp bù vượt hạn mức TDABG | Disable nút approve TDABG; hiện nút Escalate PPKD bắt buộc; không cho bypass. | TDABG → PPKD |
| **RD-BT-08** | Chênh lệch CMS vs KT chưa giải trình > 24h | Alert leo thang PPKD; TDABG phải xử lý hoặc giải thích bằng văn bản. | TDABG + Phòng KT + PPKD |
| **RD-BT-09** | Lỗi hệ thống Bigtel diện rộng (đa cổng) | Alert TDABG + PPKD + TPKD + GĐ + Phòng CN; TDABG phối hợp Phòng CN xử lý ngay. | TDABG + Phòng CN + PPKD + TPKD + GĐ |
| **RD-BT-10** | Nghi ngờ gian lận/lạm dụng cổng/kho | Khóa tài khoản liên quan; alert TDABG + PPKD + TPKD + GĐ; TDABG lập biên bản ngay; KHÔNG tự xử lý. | TDABG + PPKD + TPKD + GĐ + HCNS |
| **RD-BT-11** | KH cuối có nguy cơ truyền thông xấu | Alert TDABG + PPKD + GĐ; TDABG báo ngay, không tự phát ngôn. | TDABG + PPKD + GĐ |
| **RD-BT-12** | Tồn kho < mức đóng kho tự động | Hệ thống tự đóng kho; alert TDABG + Lead PT NCC + Phòng TC. TDABG đề xuất nhập hàng khẩn. | TDABG + Lead PT NCC + Phòng TC + PPKD |

**PHẦN 11. YÊU CẦU AUDIT LOG**

| **Yêu cầu** | **Nội dung chi tiết** |
| --- | --- |
| **Đối tượng ghi log** | Tất cả thao tác Create/Write/Approve/Reject/Stop/Escalate trên object Bigtel: NCC, SP, Giá/CK, Đại lý, Cổng/kho, Hoàn tiền/nạp bù, Công nợ, Đối soát, KPI, BC. Đặc biệt: lệnh mở/đóng cổng phải ghi log ngay tại thời điểm ra lệnh, không chờ phê duyệt. |
| **Trường bắt buộc trong mỗi log** | user_id │ timestamp │ action_type │ object_model │ object_id │ old_value │ new_value │ reason (bắt buộc với approve/reject/stop/escalate) │ attachment_ref │ approval_state │ scope_tag = BIGTEL │ escalation_level (L1/L2/L3) |
| **Log đặc biệt – lệnh dừng khẩn cấp** | Lệnh đóng cổng/khóa kho khẩn cấp: ghi log ngay tại thời điểm ra lệnh; trường emergency=True; thời hạn bổ sung phê duyệt = 2 giờ; nếu quá hạn: auto-alert PPKD. |
| **Thời gian lưu trữ** | Tối thiểu 5 năm; không ai được xóa hoặc sửa log sau khi đã ghi. |
| **Ai được xem log** | TDABG: log của mình và 4 nhóm Bigtel. PPKD/TPKD: log TDABG + nhóm Bigtel. GĐ/KSNB: toàn bộ. Admin kỹ thuật: xem không sửa. |
| **Cảnh báo bất thường** | Pattern bất thường: nhiều approve trong thời gian ngắn; thao tác ngoài giờ; approve liên tiếp bởi 1 user; thao tác ngoài phạm vi Bigtel → alert KSNB/PPKD/TPKD. |
| **Export log** | TDABG được xuất log Bigtel của mình và nhóm (format CSV/PDF, trong khoảng thời gian xác định). Không xuất log phòng khác. |

**PHẦN 12. YÊU CẦU PHÂN QUYỀN KẾ THỪA CHO 4 NHÓM BIGTEL**

| **Cấp bậc / Role** | **Quyền và giới hạn** | **Phạm vi** |
| --- | --- | --- |
| **TDABG** | Full quyền Bigtel theo MTCV và ma trận Phần 4. Không truy cập BigM/UTV. Hạn mức thấp hơn PPKD – escalate khi vượt. | Toàn bộ Bigtel |
| **Lead Phát triển NCC** | Tạo hồ sơ NCC mới (BM.QT.KD.01.01); cập nhật thông tin NCC (draft); xem hồ sơ NCC. Không phê duyệt NCC, không sửa pháp lý NCC, không ký HĐ. | Hồ sơ NCC Bigtel |
| **Lead Phát triển Đại lý** | Tạo hồ sơ đại lý mới; cập nhật thông tin đại lý (draft); xem danh mục đại lý; xem DT/tỷ trọng. Không phê duyệt hạn mức công nợ lớn, không cấu hình giá đại lý. | Hồ sơ đại lý Bigtel |
| **Lead VHTM ****&**** CSKH Bigtel** | Xem dashboard vận hành Bigtel; tạo ticket CSKH; ghi nhận khiếu nại; phê duyệt hoàn tiền/nạp bù trong hạn mức Lead (mức thấp nhất); báo cáo TDABG. Không mở/đóng cổng nếu không có phê duyệt TDABG. | Vận hành Bigtel hằng ngày |
| **Tổ sản xuất (thẻ vật lý)** | Nhập/xuất kho thẻ vật lý trong hạn mức; báo cáo tồn kho; ghi nhận sự cố kho. Không cấu hình hệ thống, không phê duyệt đơn mua NCC, không tiếp cận dữ liệu tài chính. | Kho thẻ vật lý Bigtel |

*⚠ Nguyên tắc: Lead các nhóm không được kết nối ngang với các phòng chức năng (TC, KT, CN, HCNS) mà không có sự đồng ý của TDABG. TDABG là đầu mối duy nhất của Bigtel khi làm việc với các phòng.*

**PHẦN 13. USER STORIES CHO KỸ THUẬT**

**US-BT-01**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn xem dashboard vận hành Bigtel realtime (cập nhật ≤ 3 phút) với success/pending/error rate từng cổng, và click thẳng vào cổng lỗi để xem chi tiết GD bị ảnh hưởng.

**Để: **để phát hiện lỗi cổng ngay trong giờ và ra lệnh đóng cổng kịp thời mà không cần gọi điện cho Phòng CN hỏi log.

**Điều kiện chấp nhận: **Dashboard Bigtel realtime ≤ 3 phút; drill-down cổng → từng GD lỗi; TDABG chỉ xem không sửa; khi ≥ 5 lỗi liên tiếp: hệ thống tự đóng và hiển thị banner cảnh báo đỏ trên dashboard.

**US-BT-02**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn ra lệnh đóng cổng Bigtel khẩn cấp ngay trên Odoo (chỉ cần 2 click) và Phòng CN nhận được ngay lập tức, sau đó tôi bổ sung lý do đầy đủ trong 2 giờ.

**Để: **để không mất thêm GD lỗi trong thời gian chờ hoàn thành thủ tục phê duyệt.

**Điều kiện chấp nhận: **Lệnh đóng cổng khẩn cấp: 2 click (chọn cổng + lý do sơ bộ); Phòng CN nhận notification ngay; log ghi emergency=True + timestamp; task nhắc TDABG bổ sung phê duyệt đầy đủ trong 2 giờ; nếu quá 2 giờ: auto-alert PPKD.

**US-BT-03**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn phê duyệt phiếu hoàn tiền/nạp bù Bigtel và khi giá trị vượt hạn mức của tôi, hệ thống tự hiển thị rõ hạn mức TDABG và giá trị yêu cầu, không cho tôi approve mà chỉ cho escalate PPKD.

**Để: **để không bao giờ vô tình phê duyệt vượt hạn mức và phát sinh rủi ro tài chính.

**Điều kiện chấp nhận: **Màn hình phê duyệt hiển thị: hạn mức TDABG, giá trị yêu cầu, chênh lệch; nếu vượt: nút Approve disable, chỉ hiện nút Escalate PPKD; log ghi lý do escalate.

**US-BT-04**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn nhận cảnh báo ngay khi tồn kho mã PIN của bất kỳ mệnh giá nào xuống dưới mức an toàn, với thông tin cụ thể: mệnh giá, tồn hiện tại, mức an toàn, nhu cầu dự kiến 7 ngày.

**Để: **để kịp thời đề xuất Lead PT NCC bổ sung hàng trước khi hết kho và gián đoạn bán hàng.

**Điều kiện chấp nhận: **Alert gửi TDABG + Lead PT NCC trong ≤ 10 phút sau khi chạm ngưỡng; nội dung alert: mệnh giá, tồn hiện tại, mức an toàn, % còn lại, nhu cầu dự kiến 7 ngày; TDABG click vào alert → vào thẳng màn hình tồn kho để xác nhận.

**US-BT-05**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn giao chỉ tiêu KPI tháng cho 4 Lead nhóm Bigtel bằng phiếu điện tử trên Odoo, Lead ký nhận trực tiếp trên hệ thống, và theo dõi tiến độ thực hiện KPI theo tuần.

**Để: **để không còn quản lý KPI qua file Excel/Zalo và có đầy đủ hồ sơ bằng chứng khi đánh giá cuối kỳ.

**Điều kiện chấp nhận: **Phiếu giao chỉ tiêu có chữ ký điện tử xác nhận của TDABG và Lead; dashboard KPI nhóm cập nhật theo tuần; TDABG chỉ đề xuất xếp loại, PPKD chốt chính thức; không thể chỉnh sửa nguồn dữ liệu KPI.

**US-BT-06**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn yêu cầu Phòng Công nghệ cấu hình sản phẩm/giá/cổng Bigtel qua phiếu điện tử (BM.QT.KD.01.08) và theo dõi được trạng thái xử lý: Draft → Approved → In Progress → Done → Nghiệm thu.

**Để: **để không có yêu cầu cấu hình nào bị mất, không có thay đổi cấu hình nào không có log và không có thay đổi nào mà tôi không biết.

**Điều kiện chấp nhận: **Phiếu yêu cầu cấu hình có đầy đủ trường: SP/giá/cổng cụ thể, lý do, tham chiếu phê duyệt chính sách; workflow 5 trạng thái; TDABG nhận notification khi Phòng CN hoàn thành; TDABG nghiệm thu và confirm Done.

**US-BT-07**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn xem BC đối soát DT Bigtel vs Phòng KT hằng tháng và phân công Lead giải trình từng dòng chênh lệch ngay trên Odoo, với deadline xử lý rõ ràng.

**Để: **để chênh lệch đối soát không bị bỏ sót, mọi giải trình đều có bằng chứng, và đối soát hoàn thành đúng hạn ngày làm việc thứ 5.

**Điều kiện chấp nhận: **Bảng đối soát hiển thị: chênh lệch, ngày phát sinh, trạng thái (open/giải trình/done), người được giao, deadline; TDABG phê duyệt giải trình Bigtel; Phòng KT xác nhận → Done. TDABG không thể chốt số KT.

**US-BT-08**

**Vai trò: **Là Trưởng dự án Bigtel

**Muốn: **tôi muốn nhận một alert tổng hợp end-of-day mỗi ngày lúc 20:00 tóm tắt: DT ngày, số GD lỗi, ticket chưa đóng, ranh đỏ nào đã kích hoạt, việc tồn đọng cần xử lý sáng hôm sau.

**Để: **để không bỏ sót bất kỳ vấn đề nào qua đêm và có thể chuẩn bị BC vận hành Bigtel ngày trước 9:30 kịp thời.

**Điều kiện chấp nhận: **Alert end-of-day lúc 20:00 hàng ngày gửi TDABG: tóm tắt 5 mục (DT ngày, lỗi, ticket, ranh đỏ, việc tồn đọng); click vào từng mục → đi thẳng đến màn hình liên quan.

**PHẦN 14. CHECKLIST NGHIỆM THU CẤU HÌNH ODOO 17 CHO ROLE TDABG**

**A. Phạm vi dữ liệu Bigtel only**

[ ] Record rules Odoo 17 lọc đúng: TDABG và 4 nhóm Lead chỉ thấy dữ liệu Bigtel.

[ ] Test: TDABG đăng nhập → không thấy bất kỳ dữ liệu nào của BigM/Ứng tiền Viettel.

[ ] Test: TDABG không thấy menu, không có link nào dẫn đến dữ liệu BigM/UTV.

**B. 10 Workflow (WF-BT-01 đến WF-BT-10)**

[ ] Tất cả 10 workflow đã cấu hình và test end-to-end: happy path + reject + escalate.

[ ] Test 3-tầng escalate: TDABG approve (hạn mức TDABG) → auto-escalate PPKD → auto-escalate TPKD.

[ ] Test WF-BT-05 lệnh đóng khẩn cấp: TDABG ra lệnh ngay, task nhắc bổ sung phê duyệt trong 2 giờ.

[ ] Không có workflow nào cho TDABG vừa tạo vừa tự approve trên cùng object.

[ ] Block giá < giá sàn: test đề xuất giá dưới sàn → button approve disable.

**C. 9 Dashboard**

[ ] DB-BT-01 (realtime): cập nhật ≤ 3 phút; success/pending/error từng cổng hiển thị đúng.

[ ] DB-BT-02 (ranh đỏ): 12 ranh đỏ hiển thị màu đúng; khi kích hoạt: timestamp + người xử lý.

[ ] DB-BT-05 (cổng/API/tồn kho): hiển thị đúng realtime; drill-down cổng → từng GD lỗi.

[ ] Khi ≥ 5 lỗi liên tiếp/cổng: dashboard hiển thị banner cảnh báo đỏ; cổng chuyển trạng thái Closed.

**D. 15 Cảnh báo**

[ ] 15 alert đã cấu hình và test với data mô phỏng.

[ ] ALT-BT-01 (≥5 lỗi/cổng) và ALT-BT-02 (≥3 khiếu nại/kho): hệ thống tự động đóng + alert ≤ 1 phút.

[ ] ALT-BT-08 (US-BT-08): alert end-of-day lúc 20:00 gửi đúng nội dung 5 mục.

**E. Ranh đỏ tự động**

[ ] ≥ 5 lỗi/cổng: hệ thống TỰ ĐỘNG đóng cổng (không cần TDABG ra lệnh trước).

[ ] ≥ 3 khiếu nại/60 phút/kho: hệ thống TỰ ĐỘNG khóa kho.

[ ] Tồn kho < mức đóng kho: hệ thống TỰ ĐỘNG đóng kho.

[ ] Hoàn tiền vượt hạn mức TDABG: nút approve disable, chỉ hiện nút Escalate PPKD.

**F. Phân quyền dữ liệu**

[ ] TDABG không sửa được số liệu DT, công nợ, tồn kho đã phát sinh.

[ ] TDABG không truy cập log kỹ thuật server, API key, cấu hình kỹ thuật lõi.

[ ] TDABG không thấy dữ liệu tài chính vốn/TSBĐ của Phòng TC.

[ ] TDABG không thấy HĐ LĐ, lương chính thức, hồ sơ gốc nhân sự Bigtel.

**G. Audit log**

[ ] Mọi thao tác TDABG và 4 Lead nhóm có log đầy đủ (user, timestamp, action, reason, attachment, scope=BIGTEL).

[ ] Log lệnh đóng cổng khẩn cấp có trường emergency=True + timestamp lệnh + timestamp phê duyệt bổ sung.

[ ] TDABG xuất được log Bigtel của mình và nhóm; không xuất được log phòng khác/BigM/UTV.

**H. Phân quyền 5 cấp trong Bigtel**

[ ] 5 role trong Bigtel (TDABG, Lead NCC, Lead ĐL, Lead VHTM/CSKH, Tổ SX) đã cấu hình đúng phạm vi.

[ ] Lead VHTM không mở/đóng cổng nếu không có phê duyệt TDABG.

[ ] Tổ sản xuất không truy cập dữ liệu tài chính, không cấu hình hệ thống.

**I. User stories**

[ ] 8 user story đã test với TDABG hoặc người đại diện.

[ ] Mỗi user story đạt tất cả điều kiện chấp nhận.

**PHẦN 15. CÁC ĐIỂM CẦN CEO / HCNS / CÔNG NGHỆ CHỐT TRƯỚC KHI TRIỂN KHAI**

**CEO / Giám đốc cần quyết định**

- Hạn mức phê duyệt chính xác của TDABG: hoàn tiền/nạp bù (giá trị VNĐ), hạn mức công nợ đại lý/NCC, hạn mức giá/CK, hạn mức NCC mới → cần con số cụ thể để cấu hình auto-escalate đúng ngưỡng.

- Xác nhận ngưỡng cảnh báo tồn kho: mức cảnh báo (alert vàng), mức đóng kho tự động (alert đỏ) → cần giá trị cụ thể theo từng mệnh giá/loại sản phẩm.

- Xác nhận ngưỡng success/error rate: ngưỡng cảnh báo và ngưỡng đóng cổng tự động theo từng nhóm sản phẩm.

- Xác nhận thời hạn bổ sung phê duyệt sau lệnh đóng cổng khẩn cấp (hiện đề xuất 2 giờ) – có thể điều chỉnh theo thực tế vận hành.

**Phòng HCNS cần xác nhận**

- Danh sách nhân sự được cấp role TDABG / Lead PT NCC / Lead PT ĐL / Lead VHTM-CSKH / Tổ SX trên Odoo 17.

- Xác nhận: Lead các nhóm có được liên hệ trực tiếp phòng chức năng (TC, KT, CN, HCNS) không? MTCV quy định TDABG là đầu mối duy nhất → cần cấu hình permission tương ứng.

- Quy trình khi TDABG nghỉ dài ngày: ai được ủy quyền thay? Phòng CN cập nhật quyền như thế nào?

- Xác nhận dữ liệu nhân sự nào của 4 nhóm Bigtel TDABG được xem trên HR module (tránh xem lương/HĐLĐ).

**Phòng Công nghệ cần xác nhận kỹ thuật**

- Cơ chế tự động đóng cổng/kho khi chạm ngưỡng (≥5 lỗi/cổng, ≥3 khiếu nại/kho, tồn kho < ngưỡng): Odoo 17 hỗ trợ native hay cần custom module? Cần tích hợp với Bigtel CMS như thế nào?

- Tích hợp Bigtel CMS → Odoo 17: dữ liệu DT, SL, success/pending/error, tồn kho, API được sync realtime hay batch (≤3 phút)?

- Record rules Odoo 17 lọc dữ liệu Bigtel vs BigM/UTV: cần multi-company Odoo hay custom domain/record rule?

- Cơ chế lệnh đóng cổng khẩn cấp 2 click: Odoo 17 hỗ trợ wizard đơn giản hay cần custom button?

- Alert end-of-day 20:00 (US-BT-08): cần Odoo scheduled action hay external cron?

- Timeline triển khai và môi trường UAT/test trước khi go-live.

**Phòng Kế toán cần xác nhận**

- Quy trình đối soát DT Bigtel: dữ liệu nào sẽ push tự động từ Bigtel CMS → Odoo Accounting? Dữ liệu nào vẫn nhập tay?

- Ngưỡng chênh lệch 'trọng yếu' (triggering auto-alert leo thang PPKD) là bao nhiêu? Ví dụ: > 0.1% DT tháng hoặc > X triệu VNĐ.

- Quy trình chốt số KT hằng tháng: Phòng KT cần xác nhận trên Odoo workflow hay vẫn qua email/biên bản?

**Phòng Innovation cần chuẩn hóa**

- Chuẩn hóa 9 dashboard (Phần 6) trước khi bàn giao Phòng CN build: layout, KPI, nguồn dữ liệu, công thức tính.

- Thiết kế UX cho lệnh đóng cổng khẩn cấp 2 click và màn hình phê duyệt hoàn tiền có hiển thị hạn mức.

- Pilot WF-BT-05 (lệnh đóng khẩn cấp) và WF-BT-06 (hoàn tiền với auto-escalate) trước khi deploy toàn bộ.

- Ma trận RACI QT.KD.01 (9 bước) cần được mapping vào Odoo workflow: ai R, ai A, ai C, ai I – thiết kế notification đúng đối tượng.

*Hà Nội, ngày …… tháng …… năm 2026*

| **Soạn thảo** | **Kiểm tra ****&**** nghiệm thu** | **Phê duyệt triển khai** |
| --- | --- | --- |
| Trưởng phòng Innovation | Trưởng phòng Công nghệ Trưởng phòng HCNS | Giám đốc Nguyễn Trọng Thắng |

Bảo mật – Chỉ lưu hành nội bộ Octa