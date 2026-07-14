*OCTA – Tài liệu cấu hình Odoo 17 | Role: Phó phòng Kinh doanh | ODOO-CFG.KD.PP-01*

**CÔNG TY CỔ PHẦN DỊCH VỤ TRỰC TUYẾN OCTA**

*Mã: ODOO-CFG.KD.PP-01  |  Lần ban hành: 01  |  Ngày: ……/……/2026*

**TÀI LIỆU YÊU CẦU CẤU HÌNH VAI TRÒ**

**PHÓ PHÒNG KINH DOANH TRÊN ODOO 17**

*Dùng làm tài liệu yêu cầu cấu hình Odoo 17 cho đội kỹ thuật / Phòng Innovation*

| **Hạng mục** | **Nội dung** |
| --- | --- |
| **Tên role** | PPKD – Phó phòng Kinh doanh |
| **Phạm vi chính** | Bigtel (trực tiếp) + Mảng Tài chính lớp thương mại (trực tiếp); BigM/Ứng tiền Viettel (tham vấn – chỉ khi có văn bản ủy quyền) |
| **Báo cáo trực tiếp** | Trưởng phòng Kinh doanh (TPKD) |
| **Tài liệu tham chiếu** | MTCV.KD.PP + MTCV.KD.TP + Quy chế Phân quyền + QT.KD.01 + Quy chế Thương mại + Quy chế Tài chính |
| **Phê duyệt trước khi deploy** | Giám đốc + Trưởng phòng Công nghệ + Trưởng phòng HCNS |

**PHẦN 1. TÓM TẮT VAI TRÒ PHÓ PHÒNG KINH DOANH TRÊN ODOO 17**

Trên Odoo 17, role "PPKD" là tầng điều phối – phê duyệt hạn mức thấp hơn TPKD, tập trung vào hai mảng được giao chính thức:

- Bigtel: vận hành thương mại hằng ngày, phê duyệt trong hạn mức Phó phòng, cảnh báo ranh đỏ.

- Mảng Tài chính (lớp thương mại): đàm phán deal gửi/vay với ngân hàng/công ty tài chính; theo dõi hiệu quả thương mại; KHÔNG quản trị vốn/thanh khoản/tài sản bảo đảm.

- BigM / Ứng tiền Viettel: chỉ xem (view-only) để tham vấn; không phê duyệt nếu chưa có văn bản ủy quyền của TPKD/Giám đốc.

**Nguyên tắc phân biệt PPKD vs TPKD trên hệ thống:**

| **Tiêu chí** | **TPKD** | **PPKD** |
| --- | --- | --- |
| **Phạm vi dữ liệu** | Toàn Phòng KD (Bigtel+BigM+UTViettel) | Bigtel + Tài chính lớp TM; BigM/UTV chỉ view |
| **Hạn mức phê duyệt** | Cao hơn (theo Quy chế Phân quyền) | Thấp hơn TPKD; phải escalate khi vượt |
| **Quyền mở/đóng cổng** | Toàn bộ Phòng KD | Chỉ Bigtel; BigM/UTV cần TPKD |
| **Quyền ký tờ trình deal TC** | Trong hạn mức TPKD | Trong hạn mức PPKD; vượt → escalate TPKD/GĐ |
| **Điều hành Phòng KD** | Đương nhiên | Chỉ khi có văn bản ủy quyền TPKD/GĐ |

**PHẦN 2. NGUYÊN TẮC CẤU HÌNH ROLE**

| **Nguyên tắc** | **Nội dung áp dụng** |
| --- | --- |
| **Tách phạm vi dữ liệu theo mảng được giao** | Bigtel: full access trong hạn mức. BigM/Ứng tiền Viettel: view-only trừ khi được ủy quyền bằng văn bản + cấu hình Odoo tương ứng. |
| **Không tự khép vòng (Segregation of Duties)** | PPKD không được tạo yêu cầu và tự phê duyệt cùng một đối tượng (NCC, giá, hoàn tiền, cấu hình...). |
| **Hạn mức thấp hơn TPKD** | Mọi workflow phê duyệt phải cấu hình hai mức: PPKD ≤ hạn mức → approve; vượt → auto-escalate TPKD. |
| **Audit log bắt buộc** | Tất cả hành động Create/Approve/Reject/Stop đều ghi log: user, timestamp, lý do, trạng thái, file đính kèm. |
| **Kiểm soát ngoại lệ qua workflow** | Mọi ngoại lệ (giá dưới sàn, công nợ vượt hạn, hoàn tiền vượt hạn mức PPKD) không được bypass, phải qua approval workflow. |
| **Ủy quyền tạm có kiểm soát** | Khi PPKD thay thế TPKD: quyền được mở rộng tạm theo văn bản ủy quyền; Phòng Công nghệ + HCNS phải được thông báo để điều chỉnh role trong Odoo. |
| **Không lấn owner phòng chức năng** | PPKD không có quyền chỉnh sửa: số liệu kế toán, cấu hình kỹ thuật lõi, hồ sơ nhân sự gốc, tài sản bảo đảm, tài khoản ngân hàng. |

**PHẦN 3. DANH SÁCH MODULE / MENU CẦN CÓ**

| **Module** | **Nghiệp vụ áp dụng** | **Mức quyền tổng quát** |
| --- | --- | --- |
| **Sales (Bigtel scope)** | Doanh thu Bigtel, đơn hàng, đại lý Bigtel, chính sách giá Bigtel, chiết khấu | Xem + Phê duyệt (trong hạn mức) |
| **Sales (BigM/UTV scope)** | Doanh thu BigM/UTV – chỉ xem tổng quan để tham vấn TPKD | Xem (view-only) |
| **CRM** | Pipeline đại lý Bigtel, theo dõi cơ hội phát triển đại lý cấp 1 | Xem + Tạo |
| **Purchase** | Hồ sơ NCC Bigtel, đề xuất NCC mới, SLA, công nợ NCC | Xem + Phê duyệt (Bigtel) |
| **Inventory (view)** | Tồn kho mã Bigtel, số dư API Bigtel | Xem (read-only) |
| **Accounting (view)** | Công nợ đại lý/KH Bigtel – không hạch toán | Xem (read-only) |
| **Helpdesk** | Ticket CSKH Bigtel, khiếu nại, hoàn tiền/nạp bù trong hạn mức Phó phòng | Xem + Phê duyệt |
| **Project / Task** | Giao việc nhóm Bigtel, yêu cầu liên phòng, deal tài chính đang đàm phán | Xem + Tạo + Assign |
| **HR (view – Bigtel)** | Danh sách nhân sự Bigtel, KPI cá nhân, đề xuất khen thưởng | Xem + Đề xuất |
| **Discuss** | Thông báo nội bộ, escalate, alert, kênh Bigtel | Toàn bộ |
| **Dashboard/Reporting** | Dashboard Bigtel + mảng TC lớp TM; view tổng KD để tham vấn | Xem + Xuất (phạm vi được giao) |
| **Approval (workflow)** | Luồng phê duyệt trong hạn mức PPKD: giá, hoàn tiền, cổng, công nợ Bigtel, deal TC | Tạo + Phê duyệt + Từ chối |

*⚠ Module BigM/Ứng tiền Viettel chỉ cấp View. Khi có văn bản ủy quyền TPKD → Phòng Công nghệ + HCNS tạm thời nâng quyền theo phạm vi ủy quyền và ghi log thay đổi.*

**PHẦN 4. MA TRẬN QUYỀN CHI TIẾT THEO NHÓM NGHIỆP VỤ**

*✓ = Có quyền | ○ = Có điều kiện | V = View-only (tham vấn) | — = Không có quyền*

*⚠ (Bigtel) = chỉ trong phạm vi Bigtel; (TC-TM) = Mảng Tài chính lớp thương mại; (Toàn KD) = khi được ủy quyền TPKD bằng văn bản*

| **Nhóm nghiệp vụ** | **Xem** | **Tạo** | **Sửa** | **Phê duyệt** | **Từ chối** | **Y/c cấu hình** | **Y/c dừng** | **Xuất BC** | **Drill-down** | **Xem log** | **Không được phép** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Kế hoạch KD & KPI Bigtel | ✓ | ✓ | ○ | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | Sửa KPI đã chốt TPKD/HĐQT |
| 2. KPI/BC BigM & Ứng tiền Viettel | V | — | — | — | — | — | — | — | — | — | Bất kỳ thao tác nếu chưa được ủy quyền |
| 3. DT/SL/Biên LN Bigtel | ✓ | — | — | — | — | — | — | ✓ | ✓ | ✓ | Sửa số đã phát sinh |
| 4. NCC, Sản phẩm Bigtel | ✓ | ✓ | ○ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | Sửa pháp lý NCC; dữ liệu KT NCC |
| 5. Đại lý/KH/Đối tác Bigtel | ✓ | ✓ | ○ | ✓ | ✓ | — | ○ | ✓ | ✓ | ✓ | Xóa KH; sửa lịch sử giao dịch |
| 6. Giá/CK/Thưởng/HT TM Bigtel | ✓ | ✓ | ○ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Tự sửa giá ngoài WF; vượt hạn mức PPKD |
| 7. Vận hành TM Bigtel | ✓ | ○ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Tự cấu hình cổng/sản phẩm trực tiếp |
| 8. CSKH, Hoàn tiền/Nạp bù Bigtel | ✓ | ○ | — | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | Cộng/trừ tiền ví KH trực tiếp |
| 9. Công nợ Bigtel | ✓ | ✓ | — | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | Sửa số liệu công nợ kế toán |
| 10. Đối soát DT/TK/API Bigtel | ✓ | — | — | ✓ | ✓ | — | ○ | ✓ | ✓ | ✓ | Chốt số kế toán thay Phòng KT |
| 11. Deal TC lớp TM (đàm phán) | ✓ | ✓ | ○ | ○ | — | — | — | ✓ | ✓ | — | Ký HĐ TC vượt thẩm quyền; quản trị vốn/TSBĐ |
| 12. BC, Dashboard, Alert Bigtel | ✓ | — | — | ✓ | — | — | — | ✓ | ✓ | ✓ | Thay đổi nguồn dữ liệu dashboard |
| 13. Nhân sự nhóm Bigtel | ✓ | ○ | — | ○ | ○ | — | — | ✓ | ✓ | — | Sửa HĐ LĐ; lương chính thức; hồ sơ gốc |
| 14. Phối hợp liên phòng (Bigtel) | ✓ | ✓ | — | — | — | — | ✓ | ✓ | ✓ | — | Tự đóng việc liên phòng khi chưa xác nhận đầu ra |

*○ = Chỉ trong Draft hoặc khi có văn bản điều chỉnh được TPKD/GĐ duyệt. V = View-only: tham vấn, không thao tác. Ô màu tím = chỉ xem để tham vấn TPKD.*

**PHẦN 5. DANH SÁCH WORKFLOW CẦN CẤU HÌNH**

*⚠ Tất cả workflow dưới đây được cấu hình với 2 mức phê duyệt: PPKD (trong hạn mức) → auto-escalate TPKD (khi vượt hạn mức PPKD). PPKD không thể bypass escalate.*

**WF-PP-01: Đề xuất NCC Bigtel mới**

- Bước 1: Nhóm Phát triển NCC tạo hồ sơ (BM.QT.KD.01.01) → Draft

- Bước 2: PPKD review & phê duyệt L1 (trong hạn mức) → Pending TC

- Bước 3: Phòng Tài chính thẩm định rủi ro → Approve/Reject

- Bước 4: Phòng Kế toán xác nhận điều kiện thanh toán → Confirm

- Bước 5: Nếu NCC trọng yếu ≥ ngưỡng TPKD: auto-escalate TPKD → Giám đốc

- Bước 6: Phòng Công nghệ cấu hình API/hệ thống → Done

*🔒 Ranh giới phân quyền: PPKD không tự tạo và tự approve cùng hồ sơ NCC. NCC vượt ngưỡng TPKD: workflow block, hiển thị nút Escalate.*

**WF-PP-02: Phê duyệt sản phẩm Bigtel mới**

- Bước 1: Trưởng dự án Bigtel tạo phiếu → Draft

- Bước 2: PPKD kiểm tra: NCC, HĐ/phụ lục, giá, SLA → Approve L1

- Bước 3: Phòng Kế toán xác nhận giá vốn → Confirm

- Bước 4: Phòng Công nghệ nhận BM.QT.KD.01.08 → cấu hình → Done

- Bước 5: PPKD nghiệm thu sản phẩm Active trên Bigtel.

*🔒 Ranh giới phân quyền: Không mở bán khi thiếu phê duyệt PPKD hoặc khi sản phẩm vượt hạn mức phê duyệt của PPKD (cần TPKD).*

**WF-PP-03: Phê duyệt giá / chiết khấu Bigtel**

- Bước 1: Trưởng dự án / Lead tạo phiếu (BM.QT.KD.01.02) → Draft

- Bước 2: Hệ thống tự động so sánh đề xuất với giá sàn và biên tối thiểu

- Bước 3: Nếu trong hạn mức PPKD: PPKD phê duyệt → Phòng KT đối chiếu → Phòng CN cấu hình

- Bước 4: Nếu vượt hạn mức PPKD: workflow auto-block, hiện nút Escalate TPKD

- Bước 5: Log lịch sử thay đổi giá được ghi tự động.

*🔒 Ranh giới phân quyền: PPKD không tự sửa giá trực tiếp trên Bigtel portal. Đề xuất **<** giá sàn: hệ thống block không cho phê duyệt.*

**WF-PP-04: Yêu cầu cấu hình bán Bigtel (BM.QT.KD.01.08)**

- Bước 1: PPKD / Trưởng dự án Bigtel tạo phiếu yêu cầu → Draft

- Bước 2: PPKD phê duyệt (xác nhận đã có phê duyệt chính sách) → Approved

- Bước 3: Phòng Công nghệ nhận và thực hiện → In Progress → Done

- Bước 4: PPKD hoặc Trưởng dự án Bigtel nghiệm thu kết quả.

*🔒 Ranh giới phân quyền: PPKD không tự cấu hình trực tiếp trên hệ thống Bigtel/BigM.*

**WF-PP-05: Mở / đóng cổng Bigtel**

- Bước 1: PPKD hoặc Trưởng dự án Bigtel tạo lệnh (kèm lý do bắt buộc) → Draft

- Bước 2: PPKD phê duyệt (trong phạm vi Bigtel) → Approved

- Bước 3: Phòng Công nghệ thực thi → Done

- Bước 4: Hệ thống ghi log: người ra lệnh, người thực thi, timestamp, lý do.

*🔒 Ranh giới phân quyền: Cổng BigM/Ứng tiền Viettel: PPKD không có quyền trừ khi được ủy quyền bằng văn bản. Lệnh đóng khẩn cấp Bigtel: cho phép đóng ngay, bổ sung phê duyệt trong 2 giờ.*

**WF-PP-06: Hoàn tiền / nạp bù Bigtel**

- Bước 1: CSKH Bigtel tạo ticket → xác minh → đề xuất hoàn/bù

- Bước 2: Lead Team CSKH phê duyệt (trong hạn mức Lead) → Done hoặc escalate PPKD

- Bước 3: PPKD phê duyệt (trong hạn mức PPKD) → Phòng KT lập chứng từ → Done

- Bước 4: Nếu vượt hạn mức PPKD: auto-escalate TPKD → GĐ (nếu vượt TPKD)

- Bước 5: Phòng Kế toán thực hiện hạch toán → Done

*🔒 Ranh giới phân quyền: PPKD không cộng/trừ tiền ví KH trực tiếp. Phiếu vượt hạn mức PPKD: nút approve bị disable, chỉ hiện nút Escalate TPKD.*

**WF-PP-07: Cấp hạn mức công nợ đại lý Bigtel**

- Bước 1: PPKD / Trưởng dự án Bigtel tạo đề xuất hạn mức → Draft

- Bước 2: Phòng Kế toán cung cấp lịch sử công nợ → Consulted

- Bước 3: Phòng Tài chính thẩm định rủi ro → Approve/Reject

- Bước 4: PPKD phê duyệt (trong hạn mức) hoặc Escalate TPKD

- Bước 5: Hệ thống cập nhật hạn mức, ghi log.

*🔒 Ranh giới phân quyền: PPKD không sửa trực tiếp hạn mức công nợ trên Odoo ngoài workflow.*

**WF-PP-08: Xử lý chênh lệch đối soát Bigtel**

- Bước 1: Phòng KT / Phòng KD phát hiện chênh lệch → tạo task

- Bước 2: PPKD phân công người xử lý trong nhóm Bigtel

- Bước 3: Bên xử lý giải trình + đính kèm bằng chứng → Submitted

- Bước 4: PPKD phê duyệt giải trình nghiệp vụ phía KD Bigtel

- Bước 5: Phòng Kế toán xác nhận số liệu → Done

*🔒 Ranh giới phân quyền: PPKD không chốt số kế toán; chỉ phê duyệt phần giải trình phía KD. Case chênh lệch lớn (trọng yếu) → auto-thông báo TPKD.*

**WF-PP-09: Báo cáo ranh đỏ Bigtel**

- Bước 1: Hệ thống phát hiện ranh đỏ → alert PPKD + Trưởng dự án Bigtel + TPKD

- Bước 2: PPKD xác nhận đã nhận → mở case xử lý (trong 30 phút)

- Bước 3: PPKD ra lệnh dừng / escalate → ghi log

- Bước 4: Phòng liên quan xử lý và cập nhật trạng thái

- Bước 5: TPKD báo cáo Giám đốc trong 24h → Closed

*🔒 Ranh giới phân quyền: Case ranh đỏ không được tự đóng bởi PPKD. Ranh đỏ trọng yếu (đại lý ≥ 40%, vay ≥ 15%, lỗi diện rộng) → TPKD/GĐ phải là người đóng case.*

**WF-PP-10: Giao việc và đánh giá KPI nhóm Bigtel**

- Bước 1: PPKD tạo phiếu giao chỉ tiêu tháng/quý cho Trưởng dự án Bigtel / Lead (theo chỉ tiêu TPKD đã giao PPKD)

- Bước 2: Trưởng dự án Bigtel / Lead ký nhận (confirm) trên Odoo

- Bước 3: Cuối kỳ: Trưởng dự án / Lead tự đánh giá KPI → submit

- Bước 4: PPKD đánh giá và đề xuất xếp loại A/B/C lên TPKD

- Bước 5: TPKD chốt xếp loại chính thức; Phòng HCNS nhận đề xuất khen thưởng/kỷ luật

*🔒 Ranh giới phân quyền: PPKD chỉ đề xuất xếp loại, không chốt xếp loại chính thức. PPKD không chỉnh sửa nguồn dữ liệu KPI (Bigtel CMS, Odoo log).*

**WF-PP-11: Ủy quyền điều hành thay TPKD (Conditional workflow)**

- Bước 1: TPKD hoặc GĐ tạo văn bản ủy quyền (phạm vi, thời hạn, các đầu việc được phép) trên Odoo

- Bước 2: Phòng Công nghệ + HCNS nhận thông báo → tạm thời nâng role PPKD theo phạm vi ủy quyền (ghi rõ thời hạn)

- Bước 3: PPKD điều hành trong phạm vi ủy quyền; tất cả thao tác được ghi log với tag [AUTHORIZED_SUBSTITUTION]

- Bước 4: Khi TPKD trở lại: PPKD lập BC bàn giao → TPKD confirm → Phòng CN + HCNS reset role PPKD về mức chuẩn

*🔒 Ranh giới phân quyền: PPKD không tự nâng quyền của mình. Khi ủy quyền hết hạn: hệ thống tự động reset role về mức chuẩn PPKD.*

**PHẦN 6. DANH SÁCH DASHBOARD CẦN CẤU HÌNH**

| **Mã DB** | **Tên Dashboard** | **Tần suất** | **Chỉ tiêu / Nội dung tối thiểu** |
| --- | --- | --- | --- |
| **DB-PP-01** | **Dashboard Bigtel ngày (realtime)** | Realtime (≤5 phút) | DT, SL, biên LN tạm tính Bigtel; tồn kho mã; số dư API; pending; lỗi cổng; ticket mới; hoàn-bù; cảnh báo ranh đỏ Bigtel. |
| **DB-PP-02** | **Dashboard Ranh đỏ Bigtel** | Realtime | 5 ranh đỏ Bigtel: màu đỏ/vàng/xanh; khi kích hoạt: timestamp + lệnh xử lý + người phụ trách. |
| **DB-PP-03** | **Dashboard NCC Bigtel** | Cập nhật ngày/tuần | Danh mục NCC Bigtel; tỷ trọng sản lượng (ngưỡng ≤50%); SLA; công nợ NCC; NCC dự phòng. |
| **DB-PP-04** | **Dashboard Đại lý/KH Bigtel** | Cập nhật hàng ngày | Đại lý active/inactive; DT theo đại lý; tỷ trọng ≤40%; tuổi nợ; hạn mức công nợ vs thực tế. |
| **DB-PP-05** | **Dashboard Công nợ Bigtel** | Cập nhật hàng ngày | Tổng công nợ Bigtel; tuổi nợ (0-30, 31-60, 61-90, >90 ngày); danh sách vượt hạn mức. |
| **DB-PP-06** | **Dashboard Cổng/API/Tồn kho Bigtel** | Realtime | Trạng thái cổng Bigtel (Active/Error/Closed); số dư API; tồn kho mã PIN theo mệnh giá; ngưỡng cảnh báo. |
| **DB-PP-07** | **Dashboard CSKH ****&**** Ticket Bigtel** | Cập nhật hàng ngày | Ticket mới/pending/đóng Bigtel; tỷ lệ SLA; tỷ lệ lần đầu; tỷ lệ tái phát; hoàn-bù theo tuần. |
| **DB-PP-08** | **Dashboard Mảng TC lớp TM** | Cập nhật tháng | Deal đang đàm phán; deal đã ký; điều kiện lãi/phí so với thị trường; tỷ trọng vay theo đối tác (ngưỡng ≤15%); thu nhập TC ròng thực/kế hoạch. |
| **DB-PP-09** | **Dashboard KPI nhân sự Bigtel** | Cập nhật tháng/quý | KPI Trưởng dự án Bigtel, Lead VHTM & CSKH, các nhóm Bigtel; tiến độ vs chỉ tiêu. |
| **DB-PP-10** | **Dashboard Tổng KD (View-only tham vấn)** | Cập nhật ngày | Toàn cảnh KD (Bigtel+BigM+UTV) – chỉ xem tổng quan để PPKD tham vấn TPKD. Không drill-down BigM/UTV. |

**PHẦN 7. DANH SÁCH CẢNH BÁO REALTIME / EMAIL / ODOO 17 NOTIFICATION**

| **Mã** | **Tên cảnh báo** | **Điều kiện kích hoạt** | **Tần suất** | **Người nhận** | **Mức** |
| --- | --- | --- | --- | --- | --- |
| **ALT-PP-01** | **Cổng Bigtel lỗi liên tiếp** | ≥ 5 GD lỗi/cổng liên tiếp | Realtime | PPKD + Trưởng dự án Bigtel + Phòng CN + TPKD | **Critical** |
| **ALT-PP-02** | **Pending Bigtel vượt SLA** | Pending > SLA | Realtime | PPKD + Lead VHTM + Phòng CN | **High** |
| **ALT-PP-03** | **Tồn kho mã Bigtel thấp** | Tồn < ngưỡng cảnh báo | 15 phút | PPKD + Trưởng dự án Bigtel + Phòng TC | **High** |
| **ALT-PP-04** | **Số dư API Bigtel thấp** | Số dư < nhu cầu 7 ngày | 15 phút | PPKD + Trưởng dự án Bigtel + Phòng TC | **High** |
| **ALT-PP-05** | **Ví Octa gần hết tiền** | Số dư < ngưỡng cảnh báo | Realtime | PPKD + Phòng TC + TPKD | **Critical** |
| **ALT-PP-06** | **Đại lý Bigtel vượt 40% doanh số SP** | Tỷ trọng ≥ 40% | Hàng ngày | PPKD + TPKD + Phòng TC | **Critical** |
| **ALT-PP-07** | **NCC Bigtel vượt 50% sản lượng/dòng SP** | Tỷ trọng ≥ 50% | Hàng tuần | PPKD + Phòng TC + TPKD | **High** |
| **ALT-PP-08** | **Công nợ Bigtel vượt hạn mức** | Công nợ > hạn mức duyệt | Hàng ngày | PPKD + Phòng KT + Phòng TC | **High** |
| **ALT-PP-09** | **Nợ quá hạn Bigtel ****>**** ngưỡng** | Tỷ lệ nợ quá hạn > X% | Hàng tuần | PPKD + Phòng KT | **Medium** |
| **ALT-PP-10** | **Khiếu nại hàng loạt Bigtel** | ≥ 3 khiếu nại/60 phút cùng kho | Realtime | PPKD + Lead CSKH Bigtel + Phòng CN + TPKD | **Critical** |
| **ALT-PP-11** | **Chênh lệch số liệu Bigtel vs KT ****>**** 24h** | Chưa giải trình > 24h | Hàng ngày | PPKD + Phòng KT + TPKD | **High** |
| **ALT-PP-12** | **Tỷ trọng vay từ 1 cty TC đạt 15%** | Tỷ trọng ≥ 15% | Hàng tháng | PPKD + Phòng TC + TPKD + GĐ + HĐQT | **Critical** |
| **ALT-PP-13** | **Phòng TC cảnh báo dừng deal** | Bất kỳ cảnh báo bằng văn bản | Ngay lập tức | PPKD + TPKD + GĐ | **Critical** |
| **ALT-PP-14** | **Báo cáo Bigtel quá hạn chưa nộp** | BC > hạn mà chưa submit | Ngày đến hạn | PPKD + TPKD | **Medium** |
| **ALT-PP-15** | **Hạn mức ủy quyền thay TPKD sắp hết** | Còn ≤ 1 ngày ủy quyền | 24h trước khi hết hạn | PPKD + TPKD + HCNS + Phòng CN | **Medium** |

**PHẦN 8. DANH SÁCH BÁO CÁO BẮT BUỘC**

| **Mã BC** | **Tên báo cáo** | **Tần suất** | **Người nhận** | **Phê duyệt** | **Trạng thái DL** | **Nguồn** |
| --- | --- | --- | --- | --- | --- | --- |
| **BC-PP-01** | **BC Bigtel ngày** | Hàng ngày (trước 9h) | TPKD; GĐ (khi được giao) | PPKD phê duyệt | Tạm tính | Bigtel CMS, log, ticket |
| **BC-PP-02** | **BC Bigtel tuần** | Thứ Hai hàng tuần | TPKD; KT/TC theo nội dung | PPKD phê duyệt | Tạm tính | Bigtel + sổ KT + TC |
| **BC-PP-03** | **BC mảng TC lớp TM tháng** | Ngày 5 tháng kế tiếp | TPKD; Phòng TC; GĐ | PPKD lập + TPKD duyệt trình GĐ | Thực tế | Phòng TC + so sánh thị trường |
| **BC-PP-04** | **BC bất thường Bigtel** | Theo phát sinh – gửi ngay | TPKD; GĐ | PPKD phê duyệt | Thực tế | Alert + nội bộ |
| **BC-PP-05** | **BC ủy quyền (khi thay TPKD)** | Theo kỳ ủy quyền; bàn giao khi TPKD trở lại | TPKD; GĐ | PPKD lập + TPKD confirm | Thực tế | Hồ sơ điều hành trong kỳ ủy quyền |
| **BC-PP-06** | **BC đối soát DT/TK/API Bigtel** | Tuần/tháng | Phòng KT; Phòng TC; TPKD | PPKD + Phòng KT xác nhận | Đã đối soát | Bigtel + Odoo + sổ KT |
| **BC-PP-07** | **BC deal TC lớp TM (tham chiếu so sánh thị trường)** | Theo phát sinh + tháng tổng hợp | TPKD; Phòng TC; GĐ | PPKD lập; Phòng TC ký ý kiến | Thực tế | Phòng TC + dữ liệu thị trường |
| **BC-PP-08** | **BC KPI nhân sự nhóm Bigtel** | Tháng/quý | TPKD; HCNS | PPKD đề xuất; TPKD chốt | Thực tế | Odoo + đánh giá nội bộ |

**PHẦN 9. PHẠM VI DỮ LIỆU ĐƯỢC XEM / THAO TÁC / KHÔNG ĐƯỢC TRUY CẬP**

**9.1. Dữ liệu được xem toàn bộ – Full Read (Bigtel + TC lớp TM)**

- Doanh thu, sản lượng, biên LN Bigtel theo ngày/tuần/tháng/quý/dự án/sản phẩm.

- Hồ sơ NCC Bigtel: điều kiện HĐ, SLA, tỷ lệ lỗi, công nợ, sản lượng, tập trung.

- Danh mục đại lý/KH Bigtel: thông tin, DT, tỷ trọng, công nợ, hạn mức.

- Trạng thái cổng Bigtel, số dư API, tồn kho mã PIN (realtime).

- Ticket CSKH Bigtel: nội dung, trạng thái, SLA, người xử lý.

- Công nợ đại lý/KH Bigtel (view Phòng Kế toán – không sửa).

- Danh mục ngân hàng/đối tác TC đang quan hệ; điều kiện deal đang đàm phán/đã ký.

- So sánh điều kiện deal TC với mặt bằng thị trường tương đương.

- Thu nhập TC ròng thực hiện vs kế hoạch (view từ Phòng TC).

- Tỷ trọng vay theo đối tác TC (ngưỡng ≤15%).

- Lịch sử phê duyệt của chính PPKD và cấp dưới trong nhóm Bigtel.

**9.2. Dữ liệu View-only tham vấn (BigM / Ứng tiền Viettel)**

*⚠ Chỉ xem tổng quan để tham vấn TPKD. Không drill-down chi tiết. Không phê duyệt bất kỳ thao tác nào nếu chưa có văn bản ủy quyền.*

- Tổng DT BigM và Ứng tiền Viettel (dashboard tổng KD – mức tổng hợp).

- Cảnh báo ranh đỏ BigM/UTV (view-only để PPKD nắm bức tranh tổng khi tham vấn TPKD).

**9.3. Dữ liệu được tạo / thao tác (Write/Action)**

- Tạo phiếu đề xuất NCC Bigtel mới, phiếu đề xuất sản phẩm Bigtel, phiếu đề xuất giá/CK.

- Phê duyệt/từ chối trong hạn mức PPKD (theo Quy chế Phân quyền cụ thể).

- Tạo lệnh yêu cầu cấu hình Bigtel (BM.QT.KD.01.08) và yêu cầu mở/đóng cổng Bigtel.

- Tạo giao chỉ tiêu KPI cho Trưởng dự án Bigtel và Lead Team Bigtel.

- Tạo/phê duyệt đề xuất hạn mức công nợ đại lý Bigtel (trong hạn mức PPKD).

- Phê duyệt hoàn tiền/nạp bù Bigtel vượt hạn mức Lead và trong hạn mức PPKD.

- Tạo task giao việc liên phòng (phạm vi Bigtel + TC lớp TM).

- Phê duyệt báo cáo Bigtel ngày/tuần/tháng trước khi gửi TPKD.

- Tạo tờ trình điều kiện thương mại deal TC trong hạn mức PPKD.

**9.4. Dữ liệu chỉ xem, không được sửa (Read-Only Strict)**

- Số liệu DT, công nợ, tồn kho Bigtel đã phát sinh và ghi nhận trên hệ thống.

- Số liệu kế toán đã hạch toán (sổ Fast/Odoo Accounting).

- Log giao dịch gốc từ Bigtel CMS và API (Phòng Công nghệ owner).

- Số dư tiền gửi, dư nợ vay thực tế (Phòng TC owner).

- Hồ sơ pháp lý NCC (giấy phép, HĐ gốc – Phòng KT/CN lưu).

- Hồ sơ nhân sự gốc, HĐLĐ (Phòng HCNS owner).

- Tổng quan dashboard BigM/UTV (chỉ đọc để tham vấn).

**9.5. Dữ liệu không được truy cập**

- Admin hệ thống Bigtel/BigM/Odoo (API key, cấu hình kỹ thuật lõi, database).

- Log kỹ thuật server (Phòng Công nghệ).

- Tài khoản ngân hàng, tài sản bảo đảm, quyết định giải ngân (Phòng Tài chính).

- Thông tin lương chính thức, HĐLĐ, bảo hiểm nhân sự (Phòng HCNS).

- Hồ sơ nhân sự các phòng khác ngoài Bigtel.

- Dashboard/BC của Phòng KSNB, Phòng Innovation khi chưa được chia sẻ.

- Chi tiết deal TC BigM/Ứng tiền Viettel (trừ khi được ủy quyền bằng văn bản).

**PHẦN 10. DANH SÁCH RANH ĐỎ PHẢI KHÓA THAO TÁC HOẶC BUỘC ESCALATE**

| **Mã RD** | **Tình huống** | **Hành động hệ thống bắt buộc** | **Người nhận/xử lý** |
| --- | --- | --- | --- |
| **RD-PP-01** | Đại lý Bigtel > 40% DT 1 SP | Khóa mở rộng đại lý đó; auto-create case escalate TPKD + GĐ + HĐQT. | PPKD + TPKD + GĐ + HĐQT |
| **RD-PP-02** | NCC Bigtel > 50% SL/dòng SP | Alert + PPKD tạo phương án đa dạng hóa trình TPKD. | PPKD + TPKD |
| **RD-PP-03** | Vay từ 1 cty TC > 15% tổng vốn vay | Alert PPKD + Phòng TC + TPKD; khóa đề xuất vay thêm từ đối tác đó; escalate HĐQT. | PPKD + Phòng TC + TPKD + HĐQT |
| **RD-PP-04** | Phòng TC cảnh báo dừng deal bằng văn bản | PPKD dừng đàm phán ngay; lưu hồ sơ; alert TPKD + GĐ. | PPKD + TPKD + GĐ |
| **RD-PP-05** | Giá Bigtel đề xuất < giá sàn | Block workflow; disable nút approve; hiện cảnh báo. | PPKD + Phòng KT + TPKD |
| **RD-PP-06** | Hoàn tiền/nạp bù vượt hạn mức PPKD | Disable nút approve; hiện nút Escalate TPKD; không cho phép bypass. | PPKD → TPKD |
| **RD-PP-07** | Công nợ Bigtel vượt hạn mức đã duyệt | Khóa cấp công nợ tiếp; alert PPKD + Phòng KT + Phòng TC. | PPKD + Phòng KT + Phòng TC |
| **RD-PP-08** | ≥ 5 GD lỗi liên tiếp tại 1 cổng Bigtel | Đóng cổng tạm thời; alert PPKD + Phòng CN + NCC + TPKD; PPKD confirm xử lý trong 30 phút. | PPKD + Phòng CN + TPKD |
| **RD-PP-09** | ≥ 3 khiếu nại/60 phút cùng kho Bigtel | Khóa kho tự động; alert PPKD + Lead CSKH + Tổ SX. | PPKD + Lead CSKH |
| **RD-PP-10** | Đại lý Bigtel vượt hạn mức công nợ | Dừng cấp công nợ; alert Phòng KT; case escalate TPKD. | PPKD + Phòng KT + TPKD |
| **RD-PP-11** | Chênh lệch Bigtel vs KT chưa giải trình > 24h | Alert leo thang TPKD; PPKD phải xử lý hoặc giải thích. | PPKD + Phòng KT + TPKD |
| **RD-PP-12** | PPKD thao tác ngoài phạm vi ủy quyền | Hệ thống block; ghi log vi phạm; alert TPKD + GĐ. | TPKD + GĐ |

**PHẦN 11. YÊU CẦU AUDIT LOG**

| **Yêu cầu** | **Nội dung chi tiết** |
| --- | --- |
| **Đối tượng ghi log** | Tất cả thao tác Create/Write/Approve/Reject/Stop trên các object Bigtel (NCC, SP, Giá/CK, Công nợ, Cổng/kho, Hoàn tiền/nạp bù, KPI, BC) và Deal TC lớp TM. Riêng thao tác trong kỳ ủy quyền thay TPKD phải tag [AUTHORIZED_SUBSTITUTION]. |
| **Trường bắt buộc trong mỗi log** | user_id │ timestamp │ action_type │ object_model │ object_id │ old_value │ new_value │ reason (bắt buộc với approve/reject/stop) │ attachment_ref │ approval_state │ scope_tag (BIGTEL/TC_TM/AUTHORIZED) |
| **Thời gian lưu trữ** | Tối thiểu 5 năm; không được xóa log. |
| **Ai được xem log** | PPKD: xem log của mình và nhóm Bigtel. TPKD: xem log PPKD + Phòng KD. Phòng KSNB/GĐ: toàn bộ. Admin kỹ thuật: xem không sửa. |
| **Ai không được sửa log** | Không ai. Phòng Công nghệ chịu trách nhiệm bảo toàn. |
| **Log đặc biệt – kỳ ủy quyền thay TPKD** | Tất cả thao tác trong kỳ ủy quyền ghi thêm: authorization_doc_id, authorized_by, valid_from, valid_to, scope_of_authority. Sau kỳ ủy quyền: TPKD có thể review toàn bộ log kỳ ủy quyền. |
| **Cảnh báo bất thường** | Pattern: nhiều approve trong thời gian ngắn, thao tác ngoài giờ, thao tác ngoài phạm vi ủy quyền → alert KSNB/GĐ/TPKD. |

**PHẦN 12. YÊU CẦU PHÂN QUYỀN KẾ THỪA CHO TRƯỞNG DỰ ÁN, LEAD TEAM BIGTEL**

| **Cấp bậc / Role** | **Quyền và giới hạn** | **Phạm vi** |
| --- | --- | --- |
| **PPKD** | Full quyền Bigtel + TC lớp TM theo MTCV. BigM/UTV: view-only tham vấn. | Bigtel + TC lớp TM |
| **Trưởng dự án Bigtel** | Xem dữ liệu Bigtel. Tạo phiếu đề xuất NCC, SP, cấu hình Bigtel. Phê duyệt hoàn tiền/nạp bù trong hạn mức Trưởng dự án. Giao việc, theo dõi KPI nhóm. Báo cáo Bigtel lên PPKD. KHÔNG phê duyệt chính sách giá trọng yếu, deal TC, mở/đóng cổng ngoài hạn mức. | Phạm vi Bigtel |
| **Lead VHTM ****&**** CSKH Bigtel** | Xem dữ liệu vận hành Bigtel. Tạo ticket CSKH, ghi nhận khiếu nại. Phê duyệt hoàn tiền/nạp bù trong hạn mức Lead (mức thấp nhất). Giao việc trong nhóm. KHÔNG phê duyệt giá, NCC mới, mở/đóng cổng. | Phạm vi nhóm Bigtel |
| **Nhóm Phát triển NCC Bigtel** | Tạo hồ sơ NCC mới (BM.QT.KD.01.01). Cập nhật thông tin NCC (draft). Xem hồ sơ NCC. KHÔNG phê duyệt NCC, KHÔNG sửa hồ sơ pháp lý. | Hồ sơ NCC Bigtel |
| **Nhóm Phát triển Đại lý Bigtel** | Tạo hồ sơ đại lý mới. Cập nhật thông tin đại lý (draft). Xem danh mục đại lý. KHÔNG phê duyệt hạn mức công nợ, KHÔNG cấu hình giá đại lý. | Hồ sơ đại lý Bigtel |
| **Tổ sản xuất Bigtel** | Quản lý tồn kho mã PIN: nhập/xuất trong hạn mức. Báo cáo tồn kho. KHÔNG cấu hình cổng, KHÔNG mở/đóng sản phẩm, KHÔNG phê duyệt hợp đồng NCC. | Kho mã Bigtel |

*⚠ Khi PPKD thay TPKD: Phòng Công nghệ + HCNS tạm thời nâng role PPKD theo văn bản ủy quyền; reset về mức chuẩn PPKD khi hết hạn ủy quyền.*

**PHẦN 13. USER STORIES CHO KỸ THUẬT**

**US-PP-01**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn xem dashboard Bigtel realtime với đầy đủ DT/SL/biên LN theo sản phẩm và cổng, và chỉ cần một click để drill-down vào NCC/đại lý gây ra sự thay đổi.

**Để: **để phát hiện bất thường doanh thu Bigtel ngay trong ngày và chỉ đạo xử lý kịp thời mà không cần gửi email hỏi Trưởng dự án.

**Điều kiện chấp nhận: **Dashboard Bigtel realtime cập nhật ≤ 5 phút; drill-down đến NCC/cổng/đại lý; số liệu khớp Bigtel CMS; PPKD chỉ xem không sửa.

**US-PP-02**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn phê duyệt phiếu hoàn tiền/nạp bù Bigtel vượt hạn mức Lead và khi phiếu vượt hạn mức PPKD, hệ thống tự hiển thị nút Escalate TPKD thay vì nút Approve.

**Để: **để không bao giờ vô tình phê duyệt vượt hạn mức và gây rủi ro tài chính.

**Điều kiện chấp nhận: **Màn hình phê duyệt hiển thị hạn mức PPKD vs giá trị yêu cầu; nếu vượt: nút Approve bị disable, chỉ hiện nút Escalate TPKD; log ghi rõ lý do escalate.

**US-PP-03**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn tạo tờ trình điều kiện thương mại deal ngân hàng trên Odoo và trả lời ý kiến của Phòng Tài chính ngay trong cùng task đó.

**Để: **để toàn bộ quá trình đàm phán deal TC được lưu vết, không bị mất thông tin qua email/Zalo.

**Điều kiện chấp nhận: **Task deal TC có các trường: lãi/phí đề xuất, so sánh thị trường, ý kiến Phòng TC, trạng thái (đàm phán/trình GĐ/đã ký/dừng); PPKD và Phòng TC đều nhận được notification khi có cập nhật mới.

**US-PP-04**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn nhận cảnh báo ngay khi tỷ trọng vay từ một công ty tài chính tiệm cận 15% và muốn xem ngay dashboard tỷ trọng vay theo từng đối tác.

**Để: **để kịp thời điều chỉnh cơ cấu nguồn vay và báo cáo TPKD trước khi chạm ranh đỏ.

**Điều kiện chấp nhận: **Alert gửi PPKD + Phòng TC + TPKD khi tỷ trọng đạt 12% (cảnh báo sớm) và 15% (ranh đỏ cứng); dashboard TC lớp TM hiển thị tỷ trọng theo từng đối tác dạng biểu đồ.

**US-PP-05**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn tạo lệnh đóng cổng Bigtel khẩn cấp ngay trên Odoo và được phép đóng ngay mà không cần chờ phê duyệt, nhưng phải bổ sung lý do trong vòng 2 giờ.

**Để: **để không để mất doanh thu hoặc phát sinh thêm giao dịch lỗi trong khi chờ quy trình phê duyệt.

**Điều kiện chấp nhận: **Lệnh đóng khẩn cấp cổng Bigtel: PPKD được phép thực thi ngay; hệ thống tạo task nhắc bổ sung lý do và phê duyệt trong 2 giờ; log ghi timestamp lệnh và timestamp phê duyệt bổ sung.

**US-PP-06**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn khi tôi được ủy quyền thay TPKD, mọi thao tác của tôi trong kỳ ủy quyền được gắn tag [AUTHORIZED_SUBSTITUTION] và có thể xuất báo cáo bàn giao theo kỳ.

**Để: **để TPKD khi trở lại có thể review đầy đủ những gì tôi đã làm thay và xác nhận chính xác.

**Điều kiện chấp nhận: **Trong kỳ ủy quyền: tất cả log của PPKD gắn tag [AUTHORIZED_SUBSTITUTION] + authorization_doc_id; PPKD có thể xuất BC bàn giao theo kỳ ủy quyền; khi hết hạn ủy quyền: role tự động reset về mức chuẩn PPKD.

**US-PP-07**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn giao chỉ tiêu KPI tháng cho Trưởng dự án Bigtel và Lead VHTM & CSKH Bigtel bằng văn bản trên Odoo và xem tiến độ thực hiện theo tuần.

**Để: **để không phải hỏi qua Zalo mỗi lần cần cập nhật KPI và có thể xuất báo cáo KPI nhóm Bigtel gửi TPKD.

**Điều kiện chấp nhận: **Phiếu giao chỉ tiêu có chữ ký điện tử xác nhận; dashboard KPI hiển thị tiến độ theo tuần; PPKD chỉ đề xuất xếp loại, không thể chốt xếp loại chính thức.

**US-PP-08**

**Vai trò: **Là Phó phòng Kinh doanh

**Muốn: **tôi muốn xem tổng quan KD (Bigtel + BigM + Ứng tiền Viettel) ở dạng tổng hợp để tham vấn TPKD, nhưng không thể thao tác bất cứ điều gì với BigM/UTV.

**Để: **để có đủ bức tranh toàn cảnh khi TPKD hỏi ý kiến, mà không bị hiểu là có quyền quyết định trên BigM/UTV.

**Điều kiện chấp nhận: **Dashboard tổng KD hiển thị số tổng hợp BigM/UTV ở mức tổng (không drill-down); mọi nút thao tác với BigM/UTV đều bị disable với thông báo 'Chưa được ủy quyền'; log ghi nhận chỉ là truy cập view.

**PHẦN 14. CHECKLIST NGHIỆM THU CẤU HÌNH ODOO 17 CHO ROLE PPKD**

**A. Phân tách phạm vi Bigtel vs BigM/UTV**

[ ] PPKD truy cập Bigtel: có đầy đủ quyền theo ma trận Phần 4.

[ ] PPKD truy cập BigM/UTV: chỉ thấy dashboard tổng hợp, không drill-down, không thao tác.

[ ] Khi có văn bản ủy quyền TPKD: Phòng CN có thể nâng quyền PPKD cho BigM/UTV và ghi log thay đổi.

**B. Hạn mức phê duyệt – auto escalate**

[ ] Mọi workflow có 2 mức: PPKD approve (trong hạn mức) → auto-escalate TPKD (khi vượt hạn mức PPKD).

[ ] Test: phiếu hoàn tiền vượt hạn mức PPKD → nút approve disable → chỉ hiện nút Escalate TPKD.

[ ] Test: đề xuất giá < giá sàn → workflow block, không cho PPKD phê duyệt.

**C. 11 Workflow (WF-PP-01 đến WF-PP-11)**

[ ] Tất cả 11 workflow đã cấu hình và test end-to-end: happy path + reject path + escalate path.

[ ] WF-PP-11 (ủy quyền thay TPKD): test nâng quyền tạm + auto reset khi hết hạn.

[ ] Không có workflow nào cho phép 1 user vừa tạo vừa tự approve trên cùng object.

[ ] Ranh đỏ cứng (Phần 10): block hoặc disable đúng như thiết kế.

**D. 10 Dashboard**

[ ] DB-PP-01 đến DB-PP-09 hoạt động đúng với data thực Bigtel và TC lớp TM.

[ ] DB-PP-10 (view tổng KD): chỉ xem tổng hợp, không drill-down BigM/UTV, không thao tác.

[ ] Dashboard realtime cập nhật ≤ 5 phút; drill-down Bigtel hoạt động đúng.

**E. 15 Cảnh báo**

[ ] 15 alert đã được cấu hình và test với data mô phỏng.

[ ] ALT-PP-15 (sắp hết hạn ủy quyền): test đúng 24h trước khi hết hạn.

[ ] Alert Critical gửi đến đúng người nhận ≤ 5 phút sau khi kích hoạt.

**F. Phân quyền dữ liệu**

[ ] PPKD không thể sửa số liệu DT, công nợ, tồn kho Bigtel đã phát sinh.

[ ] PPKD không truy cập được log kỹ thuật server, API key, cấu hình kỹ thuật lõi.

[ ] PPKD không thấy tài khoản ngân hàng, tài sản bảo đảm, quyết định giải ngân.

[ ] PPKD chỉ xem hồ sơ nhân sự Bigtel, không xem phòng khác.

**G. Audit log – đặc biệt kỳ ủy quyền**

[ ] Tất cả thao tác PPKD có log đầy đủ (user, timestamp, action, reason, attachment, scope_tag).

[ ] Thao tác trong kỳ ủy quyền gắn tag [AUTHORIZED_SUBSTITUTION] + các trường ủy quyền.

[ ] PPKD có thể xuất log Bigtel của mình; không xuất được log phòng khác.

**H. Phân quyền kế thừa nhóm Bigtel**

[ ] 5 cấp kế thừa (Phần 12) đã được cấu hình đúng phạm vi.

[ ] Trưởng dự án Bigtel và Lead VHTM & CSKH: test không có quyền phê duyệt giá trọng yếu hoặc deal TC.

**I. User stories**

[ ] 8 user story đã test với PPKD hoặc người dùng đại diện.

[ ] Mỗi user story đạt tất cả điều kiện chấp nhận.

**PHẦN 15. CÁC ĐIỂM CẦN CEO / HCNS / CÔNG NGHỆ CHỐT TRƯỚC KHI TRIỂN KHAI**

**CEO / Giám đốc cần quyết định**

- Hạn mức phê duyệt chính xác của PPKD (giá/CK Bigtel, hoàn tiền Bigtel, công nợ Bigtel, deal TC lớp TM) – cần số cụ thể để cấu hình workflow auto-escalate đúng ngưỡng.

- Xác nhận phạm vi ủy quyền PPKD thay TPKD: danh sách việc được phép quyết và danh sách việc phải xin ý kiến GĐ – để cấu hình WF-PP-11.

- Xác nhận BigM/Ứng tiền Viettel có bất kỳ tình huống nào mà PPKD cần quyền thao tác thường xuyên (không phải chỉ ủy quyền tạm) – nếu có, cần điều chỉnh ma trận quyền.

- Xác nhận ngưỡng cảnh báo sớm deal TC (ví dụ: 12% tổng vốn vay = cảnh báo vàng; 15% = ranh đỏ) – để cấu hình ALT-PP-12.

**Phòng HCNS cần xác nhận**

- Xác nhận danh sách nhân sự được cấp role PPKD / Trưởng dự án Bigtel / Lead / Nhóm NCC / Đại lý / Tổ SX trên Odoo.

- Quy trình khi có văn bản ủy quyền TPKD: ai phê duyệt cho Phòng Công nghệ nâng quyền PPKD? Bao lâu phải cập nhật hệ thống?

- Xác nhận dữ liệu nhân sự nhóm Bigtel nào PPKD được xem trên Odoo HR module (tránh xem lương chính thức/HĐLĐ).

- Phối hợp Phòng Công nghệ thiết lập cơ chế auto-reset role PPKD khi hết hạn ủy quyền.

**Phòng Công nghệ cần xác nhận kỹ thuật**

- Khả năng tích hợp Bigtel CMS → Odoo 17 (realtime hay batch?) để dashboard Bigtel hoạt động ≤ 5 phút.

- Cơ chế role tạm thời khi ủy quyền: Odoo 17 hỗ trợ time-based role natively hay cần custom module?

- Cơ chế tag [AUTHORIZED_SUBSTITUTION] trong audit log: cần custom hay có thể dùng chatter/note Odoo 17?

- Auto-escalate trong Approval module Odoo 17: cấu hình được ngưỡng theo giá trị hay cần Python override?

- Phân tách data scope Bigtel vs BigM/UTV trên cùng một record set (ví dụ: Sale Order có sản phẩm của cả hai): cần record rule hay multi-company Odoo?

- Timeline triển khai và môi trường test trước khi go-live.

**Phòng Tài chính cần xác nhận**

- Dữ liệu nào về deal TC lớp TM sẽ được lưu trên Odoo 17 và dữ liệu nào vẫn lưu trên hệ thống của Phòng TC? Cần xác định để tránh xung đột nguồn dữ liệu.

- Quy trình khi Phòng TC cảnh báo dừng deal bằng văn bản: cơ chế nào trên Odoo để PPKD nhận ngay và case được tạo tự động?

- Xác nhận ngưỡng cụ thể để cấu hình ALT-PP-03 (tồn kho mã thấp), ALT-PP-04 (số dư API thấp) vì các ngưỡng này Phòng TC phối hợp kiểm soát.

**Phòng Innovation cần chuẩn hóa**

- Chuẩn hóa nội dung và layout 10 dashboard (Phần 6) trước khi bàn giao Phòng Công nghệ build.

- Xác nhận công thức KPI và nguồn dữ liệu cho từng chỉ tiêu trong dashboard Bigtel và TC lớp TM.

- Pilot WF-PP-06 (hoàn tiền/nạp bù với auto-escalate) và WF-PP-11 (ủy quyền tạm) trước khi deploy toàn bộ.

- Nghiệm thu business logic của dashboard và workflow trước khi bàn giao vận hành.

*Hà Nội, ngày …… tháng …… năm 2026*

| **Soạn thảo** | **Kiểm tra ****&**** nghiệm thu** | **Phê duyệt triển khai** |
| --- | --- | --- |
| Trưởng phòng Innovation | Trưởng phòng Công nghệ Trưởng phòng HCNS | Giám đốc Nguyễn Trọng Thắng |

Bảo mật – Chỉ lưu hành nội bộ Octa