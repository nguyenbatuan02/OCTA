*OCTA – Tài liệu yêu cầu cấu hình Odoo | Role: Trưởng phòng Kinh doanh | ODOO-CFG.KD.TP-01*

**CÔNG TY CỔ PHẦN DỊCH VỤ TRỰC TUYẾN OCTA**

**Mã: ODOO-CFG.KD.TP-01  |  Lần ban hành: 01  |  Ngày: ……/……/2026**

**TÀI LIỆU YÊU CẦU CẤU HÌNH VAI TRÒ**

**TRƯỞNG PHÒNG KINH DOANH TRÊN ODOO**

*Dùng làm tài liệu yêu cầu cấu hình Odoo cho đội kỹ thuật / Phòng Innovation*

| **Hạng mục** | **Nội dung** |
| --- | --- |
| **Tên role** | TPKD – Trưởng phòng Kinh doanh |
| **Module chính** | Sales, CRM, Purchase, Accounting (view), Inventory, Helpdesk, Project, HR, Discuss |
| **Đơn vị áp dụng** | Phòng Kinh doanh – bao gồm Bigtel, BigM, Ứng tiền Viettel |
| **Tuyến báo cáo** | Giám đốc / Tổng Giám đốc Công ty |
| **Soạn thảo** | Phòng Innovation & Transformation phối hợp Phòng HCNS |
| **Phê duyệt trước khi deploy** | Giám đốc + Trưởng phòng Công nghệ + Trưởng phòng HCNS |

**PHẦN 1. TÓM TẮT VAI TRÒ TRƯỞNG PHÒNG KINH DOANH TRÊN ODOO**

Trên Odoo, role "TPKD" là tầng giám sát – điều phối – phê duyệt cấp phòng, không phải tầng tác nghiệp trực tiếp. TPKD cần:

- Nhìn thấy toàn bộ dữ liệu kinh doanh của Phòng (doanh thu, sản lượng, biên LN, tồn kho, API, công nợ, CSKH, KPI nhân sự) theo thời gian thực và định kỳ.

- Thao tác phê duyệt: đề xuất NCC/sản phẩm mới, chính sách giá/chiết khấu, hoàn tiền/nạp bù vượt hạn mức Trưởng dự án, hạn mức công nợ, mở/đóng cổng/kho.

- Yêu cầu: Phòng Công nghệ cấu hình hệ thống; Phòng Kế toán đối soát; Phòng Tài chính thẩm định.

- Nhận cảnh báo realtime: ranh đỏ thương mại, lỗi cổng, vượt ngưỡng tập trung NCC/đại lý, công nợ quá hạn, pending vượt SLA.

- Báo cáo: ký duyệt và phát hành báo cáo điều hành KD ngày/tuần/tháng/quý lên BGĐ và HĐQT.

- KHÔNG có quyền: sửa số liệu kế toán/doanh thu đã phát sinh; tự cấu hình hệ thống; thao tác trực tiếp ví/tài khoản khách hàng; ký hợp đồng tài chính vượt thẩm quyền; admin hệ thống; truy cập log kỹ thuật lõi.

*⚠ Nguyên tắc cốt lõi: không một cá nhân nào (kể cả TPKD) được nắm trọn chuỗi: đề xuất – phê duyệt – cấu hình – bán – ghi nhận – đối soát – báo cáo.*

**PHẦN 2. NGUYÊN TẮC CẤU HÌNH ROLE**

| **Nguyên tắc** | **Nội dung áp dụng** |
| --- | --- |
| **Tách biệt chức năng (Segregation of Duties)** | TPKD không được phép thực hiện đồng thời 2 trong chuỗi: tạo giao dịch – phê duyệt – ghi nhận – đối soát – báo cáo số liệu chính thức. |
| **Phân quyền tối thiểu cần thiết (Least Privilege)** | Chỉ cấp quyền đúng với những gì MTCV ghi, không cấp thêm "cho tiện". |
| **Audit log bắt buộc (Non-repudiation)** | Mọi thao tác tạo/phê duyệt/từ chối/dừng/escalate đều phải ghi log: user, timestamp, lý do, trạng thái, file đính kèm. |
| **Không tự khép vòng (No self-closing loop)** | TPKD không được tự tạo yêu cầu và tự phê duyệt yêu cầu đó trên cùng một đối tượng. |
| **Kiểm soát ngoại lệ qua workflow** | Mọi ngoại lệ (giá dưới sàn, công nợ vượt hạn, hoàn tiền vượt hạn mức) phải qua workflow phê duyệt, không cho bypass. |
| **Phân cấp kế thừa rõ ràng** | Phó phòng kế thừa một phần quyền TPKD (xem phần 12); Trưởng dự án và Lead Team có role thấp hơn. |
| **Cảnh báo thay vì khoá cứng khi có thể** | Với ngưỡng cảnh báo mềm: hệ thống cảnh báo cho TPKD và phòng liên quan; với ranh đỏ cứng: khoá workflow, buộc escalate. |

**PHẦN 3. DANH SÁCH MODULE / MENU CẦN CÓ**

| **Module** | **Nghiệp vụ áp dụng** | **Mức quyền tổng quát** |
| --- | --- | --- |
| **Sales** | Doanh thu, đơn hàng, đại lý, khách hàng, báo giá, chính sách giá, chiết khấu | Xem + Phê duyệt |
| **CRM** | Pipeline đại lý/khách hàng, theo dõi cơ hội, hoạt động bán hàng BigM | Xem + Tạo |
| **Purchase** | Hồ sơ NCC, đề xuất NCC mới, đơn mua API/mã, SLA NCC, công nợ NCC | Xem + Phê duyệt |
| **Inventory (view)** | Tồn kho mã PIN, số dư API, nhập/xuất kho – chỉ xem và yêu cầu | Xem |
| **Accounting (view)** | Công nợ đại lý/khách hàng, đối soát số liệu – không hạch toán | Xem (read-only) |
| **Helpdesk** | Ticket CSKH Phòng KD, khiếu nại, hoàn tiền/nạp bù, SLA | Xem + Phê duyệt |
| **Project / Task** | Giao việc liên phòng, theo dõi tiến độ xử lý yêu cầu cấu hình, đối soát | Xem + Tạo + Assign |
| **HR (view)** | Danh sách nhân sự Phòng KD, KPI cá nhân, đề xuất khen thưởng/kỷ luật | Xem + Đề xuất |
| **Discuss** | Thông báo nội bộ, escalate, alert, kênh phòng KD | Toàn bộ |
| **Dashboard / Reporting** | Dashboard điều hành tùy chỉnh, báo cáo KPI, ranh đỏ, drill-down | Xem + Xuất |
| **Document (optional)** | Hồ sơ NCC, hợp đồng đại lý, phiếu trình được phê duyệt | Xem + Upload |
| **Approval (workflow)** | Luồng phê duyệt: giá, chiết khấu, hoàn tiền, công nợ, mở/đóng cổng | Tạo + Phê duyệt + Từ chối |

**PHẦN 4. MA TRẬN QUYỀN CHI TIẾT THEO NHÓM NGHIỆP VỤ**

*✓ = Có quyền | ○ = Có điều kiện / cần phê duyệt thêm | — = Không có quyền*

| **Nhóm nghiệp vụ** | **Xem** | **Tạo** | **Sửa** | **Phê duyệt** | **Từ chối** | **Y/c cấu hình** | **Y/c dừng** | **Xuất BC** | **Drill-down** | **Xem log** | **Không được phép** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Kế hoạch KD & KPI | ✓ | ✓ | ○ | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | Sửa KPI đã chốt HĐQT |
| 2. Doanh thu / sản lượng / biên LN | ✓ | — | — | — | — | — | — | ✓ | ✓ | ✓ | Sửa số đã phát sinh |
| 3. Sản phẩm, NCC | ✓ | ✓ | ○ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | Sửa pháp lý NCC; dữ liệu KT NCC |
| 4. Đại lý, KH, đối tác | ✓ | ✓ | ○ | ✓ | ✓ | — | ○ | ✓ | ✓ | ✓ | Xóa KH; sửa lịch sử giao dịch |
| 5. Giá, CK, thưởng, hỗ trợ TM | ✓ | ✓ | ○ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Tự sửa giá trên hệ thống ngoài WF |
| 6. Vận hành thương mại | ✓ | ○ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Tự cấu hình cổng/sản phẩm trực tiếp |
| 7. CSKH, khiếu nại, hoàn tiền | ✓ | ○ | — | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | Cộng/trừ tiền ví KH trực tiếp |
| 8. Công nợ kinh doanh | ✓ | ✓ | — | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | Sửa số liệu công nợ kế toán |
| 9. Đối soát: DT/TK/API/Ví | ✓ | — | — | ✓ | ✓ | — | ○ | ✓ | ✓ | ✓ | Chốt số kế toán thay Phòng KT |
| 10. Báo cáo / Dashboard / Alert | ✓ | — | — | ✓ | — | — | — | ✓ | ✓ | ✓ | Thay đổi nguồn dữ liệu dashboard |
| 11. Nhân sự Phòng KD | ✓ | ○ | — | ○ | ○ | — | — | ✓ | ✓ | — | Sửa HĐ LĐ, lương chính thức; hồ sơ gốc |
| 12. Phối hợp liên phòng | ✓ | ✓ | — | — | — | — | ✓ | ✓ | ✓ | — | Tự đóng việc liên phòng khi chưa có xác nhận đầu ra |
| 13. Quan hệ Ngân hàng/ĐTTC | ✓ | ✓ | — | ○ | — | — | — | ✓ | ✓ | — | Ký HĐ tài chính; quản trị tài sản bảo đảm; mở TK ngân hàng |

*○ = Chỉ được sửa khi đang ở trạng thái Draft và chưa phê duyệt, hoặc khi có yêu cầu điều chỉnh được Giám đốc phê duyệt.*

**PHẦN 5. DANH SÁCH WORKFLOW CẦN CẤU HÌNH**

**WF-KD-01: Đề xuất NCC / đối tác mới**

- Bước 1: Trưởng dự án / Nhóm NCC tạo hồ sơ (BM.QT.KD.01.01) → Draft

- Bước 2: TPKD review & phê duyệt sơ bộ (quyền Approve L1) → Pending Tài chính

- Bước 3: Phòng Tài chính thẩm định rủi ro → Approve/Reject

- Bước 4: Phòng Kế toán xác nhận điều kiện thanh toán → Confirm

- Bước 5: Giám đốc phê duyệt cuối (nếu NCC trọng yếu ≥ ngưỡng) → Done

- Bước 6: Phòng Công nghệ nhận yêu cầu cấu hình API/hệ thống → In Progress → Done

*⚠ Ranh giới phân quyền: TPKD không được phép tự tạo và tự approve cùng một hồ sơ NCC.*

**WF-KD-02: Phê duyệt sản phẩm / dịch vụ mới**

- Bước 1: Trưởng dự án tạo phiếu đề xuất sản phẩm → Draft

- Bước 2: TPKD kiểm tra: có NCC, HĐ/phụ lục, giá, SLA → Approve L1

- Bước 3: Phòng Kế toán xác nhận giá vốn → Confirm

- Bước 4: Phòng Công nghệ nhận BM.QT.KD.01.08 → cấu hình → Done

- Bước 5: TPKD chốt sản phẩm Active trên hệ thống.

*⚠ Ranh giới phân quyền: Không được mở bán khi thiếu hồ sơ NCC hoặc thiếu phê duyệt TPKD.*

**WF-KD-03: Phê duyệt giá / chiết khấu / thưởng / hỗ trợ TM**

- Bước 1: Trưởng dự án / Nhóm KD tạo phiếu đề xuất (BM.QT.KD.01.02) → Draft

- Bước 2: TPKD so sánh với giá sàn + biên tối thiểu → Approve (trong hạn mức) hoặc Escalate lên GĐ

- Bước 3: Phòng Kế toán đối chiếu giá vốn → Confirm

- Bước 4: Phòng Công nghệ nhận yêu cầu cấu hình giá → Done

- Bước 5: Log lịch sử thay đổi giá được lưu tự động.

*⚠ Ranh giới phân quyền: TPKD không được tự sửa giá trực tiếp trên portal mà không qua WF này.*

**WF-KD-04: Yêu cầu cấu hình bán (BM.QT.KD.01.08)**

- Bước 1: TPKD / Trưởng dự án tạo phiếu yêu cầu cấu hình → Draft

- Bước 2: TPKD phê duyệt phiếu (xác nhận đã có phê duyệt chính sách) → Approved

- Bước 3: Phòng Công nghệ nhận và thực hiện cấu hình → In Progress

- Bước 4: Phòng Công nghệ xác nhận hoàn thành → Done

- Bước 5: TPKD hoặc Trưởng dự án nghiệm thu kết quả cấu hình.

*⚠ Ranh giới phân quyền: TPKD không có quyền tự cấu hình trực tiếp trên hệ thống Bigtel/BigM.*

**WF-KD-05: Mở / đóng cổng / kho mã**

- Bước 1: TPKD hoặc Trưởng dự án tạo lệnh mở/đóng → Draft (kèm lý do bắt buộc)

- Bước 2: TPKD phê duyệt → Approved

- Bước 3: Phòng Công nghệ thực thi → Done

- Bước 4: Hệ thống ghi log: người ra lệnh, người thực thi, timestamp, lý do.

*⚠ Ranh giới phân quyền: Lệnh đóng khẩn cấp: TPKD được yêu cầu đóng ngay và bổ sung phê duyệt trong 2 giờ.*

**WF-KD-06: Hoàn tiền / nạp bù**

- Bước 1: CSKH tạo ticket → xác minh → đề xuất hoàn/bù

- Bước 2: Trưởng dự án phê duyệt (trong hạn mức Trưởng dự án) → Done

- Bước 3: Nếu vượt hạn mức: escalate lên TPKD → TPKD phê duyệt

- Bước 4: Nếu vượt hạn mức TPKD: escalate lên Giám đốc → phê duyệt → Phòng Kế toán lập chứng từ

- Bước 5: Phòng Kế toán thực hiện hạch toán và xuất chứng từ → Done

*⚠ Ranh giới phân quyền: TPKD không được tự cộng/trừ tiền ví khách hàng; mọi thao tác phải qua Phòng Kế toán sau khi có phê duyệt.*

**WF-KD-07: Cấp hạn mức công nợ đại lý / khách hàng**

- Bước 1: TPKD / Trưởng dự án tạo đề xuất hạn mức → Draft

- Bước 2: Phòng Kế toán cung cấp lịch sử công nợ → Consulted

- Bước 3: Phòng Tài chính thẩm định rủi ro → Approve/Reject

- Bước 4: TPKD phê duyệt cuối (trong hạn mức) hoặc Escalate lên GĐ

- Bước 5: Hệ thống cập nhật hạn mức, log thay đổi.

*⚠ Ranh giới phân quyền: TPKD không được sửa hạn mức công nợ trực tiếp trên Odoo mà không qua WF.*

**WF-KD-08: Xử lý chênh lệch đối soát**

- Bước 1: Phòng Kế toán hoặc Phòng KD phát hiện chênh lệch → Tạo task

- Bước 2: TPKD phân công người xử lý (Trưởng dự án / chuyên viên KD)

- Bước 3: Bên xử lý giải trình + đính kèm bằng chứng → Submitted

- Bước 4: TPKD phê duyệt giải trình nghiệp vụ phía KD

- Bước 5: Phòng Kế toán xác nhận số liệu → Done

*⚠ Ranh giới phân quyền: TPKD không được chốt số kế toán; chỉ phê duyệt phần giải trình của Phòng KD.*

**WF-KD-09: Báo cáo ranh đỏ**

- Bước 1: Hệ thống tự động phát hiện ranh đỏ → alert gửi TPKD + phòng liên quan

- Bước 2: TPKD xác nhận đã nhận → mở case xử lý (within 30 phút)

- Bước 3: TPKD ra lệnh dừng / escalate → ghi log

- Bước 4: Phòng liên quan xử lý và cập nhật trạng thái

- Bước 5: TPKD báo cáo Giám đốc trong 24h → Closed

*⚠ Ranh giới phân quyền: Case ranh đỏ không được tự đóng bởi TPKD; phải có xác nhận từ Giám đốc hoặc phòng chức năng liên quan.*

**WF-KD-10: Giao việc và đánh giá KPI**

- Bước 1: TPKD tạo phiếu giao chỉ tiêu tháng/quý cho Trưởng dự án / Lead (bằng văn bản trên Odoo)

- Bước 2: Trưởng dự án / Lead ký nhận (confirm) trên Odoo

- Bước 3: Cuối kỳ: Trưởng dự án tự đánh giá KPI → submit

- Bước 4: TPKD đánh giá và chốt xếp loại A/B/C

- Bước 5: Phòng HCNS nhận đề xuất khen thưởng / kỷ luật → xử lý theo quy chế

*⚠ Ranh giới phân quyền: TPKD không được chỉnh sửa số liệu KPI nguồn (Bigtel CMS, Odoo log) khi đánh giá.*

**PHẦN 6. DANH SÁCH DASHBOARD CẦN CẤU HÌNH**

| **Mã DB** | **Tên Dashboard** | **Tần suất cập nhật** | **Chỉ tiêu / Nội dung tối thiểu** |
| --- | --- | --- | --- |
| **DB-KD-01** | **Dashboard Điều hành KD ngày** | Realtime / end-of-day | Doanh thu, sản lượng, biên LN tạm tính theo dự án và sản phẩm; tồn kho/API; pending; lỗi cổng; số ticket mới/tồn; hoàn-bù trong ngày; cảnh báo ranh đỏ. |
| **DB-KD-02** | **Dashboard Ranh đỏ** | Realtime | Panel trạng thái 9 ranh đỏ; màu đỏ/vàng/xanh; khi kích hoạt: hiển thị timestamp + lệnh đang thực hiện. |
| **DB-KD-03** | **Dashboard NCC** | Cập nhật hàng ngày/tuần | Danh mục NCC đang hoạt động; tỷ trọng sản lượng theo NCC; SLA thực hiện; công nợ; ngưỡng tập trung ≤50%. |
| **DB-KD-04** | **Dashboard Đại lý / KH** | Cập nhật hàng ngày | Đại lý active/inactive; doanh thu theo đại lý; tỷ trọng ≤40%; tuổi nợ bình quân; hạn mức công nợ vs thực tế. |
| **DB-KD-05** | **Dashboard Công nợ** | Cập nhật hàng ngày | Tổng công nợ; phân loại theo tuổi nợ (0–30, 31–60, 61–90, >90 ngày); danh sách vượt hạn mức; xu hướng theo tháng. |
| **DB-KD-06** | **Dashboard Cổng / API / Tồn kho** | Realtime | Trạng thái từng cổng (Active/Error/Closed); số dư API theo đối tác; tồn kho mã PIN theo mệnh giá; ngưỡng cảnh báo thiếu. |
| **DB-KD-07** | **Dashboard CSKH ****&**** Ticket** | Cập nhật hàng ngày | Số ticket mới/pending/đã đóng; tỷ lệ SLA; tỷ lệ giải quyết lần đầu; tỷ lệ tái phát; hoàn-bù theo tuần. |
| **DB-KD-08** | **Dashboard KPI Nhân sự Phòng KD** | Cập nhật tháng/quý | KPI từng nhân sự, Trưởng dự án, Lead Team; tiến độ so với chỉ tiêu; xếp loại A/B/C. |
| **DB-KD-09** | **Dashboard Tài chính thương mại (view)** | Cập nhật tháng | Thu nhập tài chính ròng từ quan hệ ngân hàng; tỷ trọng vay theo đối tác (ngưỡng ≤15%); hiệu quả thực/kế hoạch. |

**PHẦN 7. DANH SÁCH CẢNH BÁO REALTIME / EMAIL / ODOO NOTIFICATION**

| **Mã** | **Tên cảnh báo** | **Điều kiện kích hoạt** | **Tần suất check** | **Người nhận** | **Mức độ** |
| --- | --- | --- | --- | --- | --- |
| **ALT-01** | **Cổng lỗi liên tiếp** | ≥ 5 giao dịch lỗi/cổng liên tiếp | Realtime | TPKD + Trưởng dự án + Phòng CN | **Critical** |
| **ALT-02** | **Pending vượt SLA** | Pending > SLA định nghĩa | Realtime | TPKD + Lead VHTM + Phòng CN | **High** |
| **ALT-03** | **Tồn kho mã thấp** | Tồn < ngưỡng cảnh báo (≤ X ngày) | 15 phút/lần | TPKD + Trưởng dự án Bigtel + Phòng TC | **High** |
| **ALT-04** | **Số dư API thấp** | Số dư < nhu cầu 7 ngày | 15 phút/lần | TPKD + Trưởng dự án + Phòng TC | **High** |
| **ALT-05** | **Ví Octa gần hết tiền** | Số dư < ngưỡng cảnh báo | Realtime | TPKD + Phòng TC | **Critical** |
| **ALT-06** | **Đại lý vượt 40% doanh số SP** | Tỷ trọng đại lý ≥ 40% | Hàng ngày | TPKD + Phòng TC + GĐ | **Critical** |
| **ALT-07** | **NCC vượt 50% sản lượng/dòng SP** | Tỷ trọng NCC ≥ 50% | Hàng tuần | TPKD + Phòng TC | **High** |
| **ALT-08** | **Công nợ vượt hạn mức** | Công nợ thực tế > hạn mức duyệt | Hàng ngày | TPKD + Phòng KT + Phòng TC | **High** |
| **ALT-09** | **Nợ quá hạn ****>**** ngưỡng** | Nợ quá hạn / tổng nợ > X% | Hàng tuần | TPKD + Phòng KT | **Medium** |
| **ALT-10** | **Khiếu nại hàng loạt** | ≥ 3 khiếu nại/60 phút cùng kho | Realtime | TPKD + Lead CSKH + Phòng CN | **Critical** |
| **ALT-11** | **Chênh lệch số liệu KD vs KT ****>**** 24h** | Chênh lệch chưa giải trình > 24h | Hàng ngày | TPKD + Phòng KT + GĐ | **High** |
| **ALT-12** | **Vay từ 1 cty TC ≥ 15% tổng vốn** | Tỷ trọng vay ≥ 15% | Hàng tháng | TPKD + Phòng TC + GĐ + HĐQT | **Critical** |
| **ALT-13** | **Lỗi hệ thống diện rộng** | Đa cổng / đa khách bị ảnh hưởng | Realtime | TPKD + Phòng CN + GĐ | **Critical** |
| **ALT-14** | **Nghi ngờ gian lận / bất thường** | Pattern giao dịch bất thường | Realtime | TPKD + Phòng TC + GĐ | **Critical** |
| **ALT-15** | **Báo cáo quá hạn chưa nộp** | BC > hạn mà chưa submit | Ngày đến hạn | TPKD + GĐ | **Medium** |

**PHẦN 8. DANH SÁCH BÁO CÁO BẮT BUỘC**

| **Mã BC** | **Tên báo cáo** | **Tần suất** | **Người nhận** | **Người phê duyệt** | **Trạng thái dữ liệu** | **Nguồn dữ liệu** |
| --- | --- | --- | --- | --- | --- | --- |
| **BC-KD-01** | **BC điều hành KD ngày** | Hàng ngày (trước 9h) | GĐ, Phó GĐ | TPKD phê duyệt | Tạm tính | Bigtel CMS, log, ticket |
| **BC-KD-02** | **BC điều hành KD tuần** | Thứ Hai hàng tuần | GĐ, HĐQT (định kỳ), TC, KT | TPKD phê duyệt | Tạm tính | Bigtel + sổ KT + TC |
| **BC-KD-03** | **BC điều hành KD tháng** | Ngày 5 tháng kế tiếp | GĐ, HĐQT, phòng phối hợp | TPKD phê duyệt | Đã đối soát | Bigtel + KT + ticket |
| **BC-KD-04** | **BC điều hành KD quý** | Ngày 10 quý kế tiếp | HĐQT (qua GĐ) | TPKD phê duyệt + GĐ trình | Đã chốt | Tổng hợp BC tháng |
| **BC-KD-05** | **BC bất thường** | Theo phát sinh – gửi ngay | GĐ/CEO, HĐQT (nếu TY) | TPKD phê duyệt | Thực tế | Alert + báo cáo Phòng KD |
| **BC-KD-06** | **BC đối soát DT/CN/TK/API** | Tuần/tháng | Phòng KT, TC, GĐ | TPKD + Phòng KT xác nhận | Đã đối soát | Bigtel + Odoo + sổ KT |
| **BC-KD-07** | **BC danh mục NCC, đại lý, KH** | Tháng/quý | GĐ, Phòng TC | TPKD phê duyệt | Đã đối soát | Bigtel + Phòng KT |
| **BC-KD-08** | **BC nhân sự Phòng KD** | Tháng/quý | HCNS, GĐ | TPKD phê duyệt | Thực tế | HCNS + đánh giá nội bộ |
| **BC-KD-09** | **BC KPI / kết quả kinh doanh** | Tháng/quý | GĐ, HĐQT | TPKD phê duyệt | Đã chốt (KPI) | Odoo + Bigtel + HCNS |
| **BC-KD-10** | **BC ranh đỏ và xử lý** | Theo phát sinh + tháng tổng hợp | GĐ, HĐQT (nếu TY) | TPKD phê duyệt | Thực tế | Alert log + xử lý case |

**PHẦN 9. PHẠM VI DỮ LIỆU ĐƯỢC XEM / THAO TÁC / KHÔNG ĐƯỢC TRUY CẬP**

**9.1. Dữ liệu được xem toàn bộ (Full Read)**

- Doanh thu, sản lượng, biên lợi nhuận theo dự án / sản phẩm / ngày / tuần / tháng / quý.

- Hồ sơ NCC: tên, điều kiện HĐ, SLA, tỷ lệ lỗi, công nợ, sản lượng, mức tập trung.

- Danh mục đại lý / khách hàng: thông tin cơ bản, doanh thu, tỷ trọng, công nợ, hạn mức.

- Trạng thái cổng, API, tồn kho mã PIN theo thời gian thực.

- Ticket CSKH thuộc Phòng KD: nội dung, trạng thái, SLA, người xử lý.

- Công nợ đại lý / khách hàng theo số liệu phối hợp với Phòng Kế toán (view only).

- Báo cáo đối soát (trạng thái chênh lệch, danh sách chưa giải trình).

- Lịch sử phê duyệt: chính sách giá, chiết khấu, hoàn tiền, công nợ, mở/đóng cổng.

- Dashboard KPI nhân sự Phòng KD.

- Log các thao tác phê duyệt của chính TPKD và cấp dưới trong Phòng KD.

**9.2. Dữ liệu được tạo / thao tác (Write/Action)**

- Tạo phiếu đề xuất NCC mới, phiếu đề xuất sản phẩm, phiếu đề xuất chính sách giá / chiết khấu.

- Phê duyệt / từ chối các phiếu trong phạm vi hạn mức TPKD.

- Tạo lệnh yêu cầu cấu hình (BM.QT.KD.01.08) và yêu cầu mở / đóng cổng / kho.

- Tạo giao chỉ tiêu KPI cho Trưởng dự án và Lead Team.

- Tạo / phê duyệt đề xuất hạn mức công nợ đại lý / khách hàng.

- Phê duyệt hoàn tiền / nạp bù vượt hạn mức Trưởng dự án và trong hạn mức TPKD.

- Giao việc liên phòng (tạo task, assign người xử lý).

- Phê duyệt báo cáo điều hành KD ngày / tuần / tháng / quý trước khi gửi BGĐ.

- Xuất báo cáo định kỳ và báo cáo bất thường.

**9.3. Dữ liệu chỉ xem, không được sửa (Read-Only Strict)**

- Số liệu doanh thu, công nợ, tồn kho đã phát sinh và đã ghi nhận trên hệ thống.

- Số liệu kế toán đã hạch toán (sổ Fast / Odoo Accounting).

- Log giao dịch gốc từ Bigtel CMS và API của Phòng Công nghệ.

- Hồ sơ pháp lý NCC (giấy phép, hợp đồng gốc – lưu ở Phòng Kế toán / Công nghệ).

- Hồ sơ nhân sự gốc, hợp đồng lao động (Phòng HCNS quản lý).

- Dữ liệu tài chính lõi: vốn, dòng tiền, tài sản bảo đảm (Phòng Tài chính owner).

**9.4. Dữ liệu không được truy cập**

- Admin hệ thống Bigtel / BigM / Odoo (API key, cấu hình kỹ thuật lõi, database).

- Log kỹ thuật server (chỉ Phòng Công nghệ).

- Thông tin lương chính thức, bảo hiểm, HĐLĐ của nhân sự ngoài Phòng KD (Phòng HCNS).

- Tài khoản ngân hàng, số dư tài khoản thanh toán của Công ty (Phòng Tài chính).

- Dashboard / báo cáo của Phòng KSNB, Phòng Innovation (khi chưa được chia sẻ).

- Thông tin phê duyệt của HĐQT trừ khi được Giám đốc chia sẻ chính thức.

**PHẦN 10. DANH SÁCH RANH ĐỎ PHẢI KHÓA THAO TÁC HOẶC BUỘC ESCALATE**

| **Mã RD** | **Tình huống ranh đỏ** | **Hành động hệ thống bắt buộc** | **Người nhận / Xử lý** |
| --- | --- | --- | --- |
| **RD-01** | Đại lý chiếm > 40% doanh số 1 sản phẩm | Khóa mở rộng đại lý đó; bắt buộc tạo case escalate lên GĐ + HĐQT trong Odoo. | TPKD + GĐ + HĐQT |
| **RD-02** | NCC chiếm > 50% sản lượng/dòng sản phẩm | Alert + buộc TPKD tạo phương án đa dạng hóa trình GĐ. | TPKD + GĐ |
| **RD-03** | Vay từ 1 cty tài chính > 15% tổng vốn vay | Khóa yêu cầu vay thêm từ đối tác đó; bắt buộc escalate lên HĐQT. | TPKD + Phòng TC + HĐQT |
| **RD-04** | Bán dưới giá sàn chưa được phê duyệt | Hệ thống block giao dịch; cảnh báo TPKD + Phòng KT; không cho phép cấu hình. | TPKD + Phòng KT + GĐ |
| **RD-05** | Hoàn tiền/nạp bù vượt hạn mức TPKD chưa trình GĐ | Khóa phiếu; buộc escalate Giám đốc. | TPKD → GĐ |
| **RD-06** | Công nợ KH/đại lý vượt hạn mức đã duyệt | Khóa cấp công nợ tiếp; alert TPKD + Phòng KT + Phòng TC. | TPKD + Phòng KT + Phòng TC |
| **RD-07** | ≥ 5 giao dịch lỗi liên tiếp tại 1 cổng | Khóa cổng tạm thời tự động; alert TPKD + Phòng CN + NCC; TPKD phải confirm xử lý trong 30 phút. | TPKD + Phòng CN |
| **RD-08** | ≥ 3 khiếu nại/60 phút cùng kho thẻ | Khóa kho tự động; alert TPKD + Lead CSKH + Tổ sản xuất. | TPKD + Lead CSKH |
| **RD-09** | Ví Octa xuống dưới ngưỡng cảnh báo | Dừng bán tự động; alert TPKD + Phòng TC. | TPKD + Phòng TC |
| **RD-10** | Chênh lệch số liệu KD vs KT chưa giải trình > 24h | Alert leo thang lên GĐ nếu không được giải trình; TPKD phải xử lý hoặc giải thích. | TPKD + Phòng KT + GĐ |
| **RD-11** | Phát hiện gian lận / bất thường nghiêm trọng | Dừng giao dịch liên quan; cô lập rủi ro; alert GĐ + Phòng TC + TPKD ngay lập tức. | TPKD + GĐ + Phòng TC |
| **RD-12** | Lỗi hệ thống diện rộng (đa cổng / đa KH) | Dừng bán toàn cục; alert GĐ + Phòng CN; TPKD và GĐ cùng quyết định. | TPKD + Phòng CN + GĐ |

**PHẦN 11. YÊU CẦU AUDIT LOG**

| **Yêu cầu** | **Nội dung chi tiết** |
| --- | --- |
| **Đối tượng ghi log** | Tất cả thao tác Tạo / Sửa / Phê duyệt / Từ chối / Dừng / Escalate trên các object: NCC, Sản phẩm, Giá/CK, Công nợ, Cổng/kho, Hoàn tiền, KPI, Báo cáo, Ranh đỏ. |
| **Trường bắt buộc trong mỗi log** | user_id │ timestamp │ action_type │ object_model │ object_id │ old_value │ new_value │ reason (bắt buộc với approve/reject/stop) │ attachment_ref │ approval_state |
| **Thời gian lưu trữ** | Tối thiểu 5 năm; không được xóa log khi chưa có phê duyệt từ Giám đốc + Phòng Công nghệ. |
| **Ai được xem log** | TPKD: xem log của chính mình và log Phòng KD. Phòng KSNB/GĐ: xem toàn bộ. Admin kỹ thuật: xem nhưng không được sửa. |
| **Ai không được sửa log** | Không ai được sửa hoặc xóa log sau khi đã ghi. Phòng Công nghệ chịu trách nhiệm bảo toàn log. |
| **Cơ chế export log** | TPKD được xuất log của Phòng KD (format CSV/PDF) trong phạm vi thời gian xác định; không được export log của phòng khác. |
| **Cảnh báo bất thường trong log** | Nếu phát hiện pattern bất thường (nhiều thao tác trong thời gian ngắn, approve liên tiếp bởi 1 user, thao tác ngoài giờ), hệ thống gửi alert cho KSNB/GĐ. |

**PHẦN 12. YÊU CẦU PHÂN QUYỀN KẾ THỪA CHO PHÓ PHÒNG, TRƯỞNG DỰ ÁN, LEAD TEAM**

| **Role / Cấp bậc** | **Quyền kế thừa từ TPKD và giới hạn** | **Phạm vi** |
| --- | --- | --- |
| **TPKD** | Full quyền theo MTCV đã xác định ở các phần trên. | Toàn Phòng KD |
| **Phó phòng KD** | Xem tất cả dữ liệu Phòng KD. Phê duyệt thay TPKD khi TPKD ủy quyền bằng văn bản (ghi rõ phạm vi). Tạo phiếu đề xuất, giao việc, theo dõi KPI. KHÔNG được phê duyệt vượt hạn mức TPKD. KHÔNG có quyền phê duyệt chính sách trọng yếu nếu TPKD không ủy quyền cụ thể. | Toàn Phòng KD (khi được ủy quyền) |
| **Trưởng dự án (Bigtel / BigM / Ứng tiền)** | Xem dữ liệu dự án mình phụ trách. Tạo phiếu đề xuất NCC, sản phẩm, cấu hình trong dự án. Phê duyệt hoàn tiền / nạp bù trong hạn mức Trưởng dự án (theo ma trận). Giao việc, theo dõi KPI nhân sự dự án. Báo cáo dự án lên TPKD. KHÔNG được xem dữ liệu dự án khác (trừ khi TPKD cho phép). | Phạm vi dự án mình phụ trách |
| **Lead Team (VHTM, CSKH, NCC, Đại lý, Tổ SX)** | Xem dữ liệu nhóm mình phụ trách. Tạo ticket CSKH, ghi nhận khiếu nại. Phê duyệt hoàn tiền / nạp bù trong hạn mức Lead (mức thấp nhất). Giao việc trong nhóm, theo dõi tiến độ. KHÔNG có quyền phê duyệt chính sách giá, NCC mới, mở/đóng cổng. | Phạm vi nhóm mình phụ trách |

*⚠ Nguyên tắc ủy quyền: Ủy quyền phải bằng văn bản (ghi rõ phạm vi, thời hạn, giới hạn); người được ủy quyền không được ủy quyền tiếp; Phòng HCNS + Phòng Công nghệ được thông báo để điều chỉnh quyền hệ thống tương ứng.*

**PHẦN 13. USER STORIES CHO KỸ THUẬT**

**US-01**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn xem dashboard doanh thu realtime theo từng dự án (Bigtel/BigM/Ứng tiền) và từng sản phẩm, với khả năng drill-down đến cổng/NCC/đại lý/kênh bán.

**Để: **để phát hiện ngay khi doanh thu bất thường và ra lệnh xử lý kịp thời.

**Điều kiện chấp nhận: **Dashboard hoạt động realtime, cập nhật ≤5 phút; drill-down đến cấp sản phẩm/cổng/NCC; số liệu trùng khớp Bigtel CMS; TPKD có quyền xem nhưng không sửa số liệu.

**US-02**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn nhận cảnh báo ngay khi một đại lý chiếm > 40% doanh số của bất kỳ sản phẩm nào.

**Để: **để kịp thời tái cơ cấu danh mục và báo cáo GĐ/HĐQT theo đúng ranh đỏ quy định.

**Điều kiện chấp nhận: **Alert gửi tới TPKD qua Odoo notification + email trong vòng 5 phút sau khi vượt ngưỡng; case escalate tự động được tạo; TPKD phải confirm xử lý trong 24h.

**US-03**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn phê duyệt phiếu đề xuất giá/chiết khấu/thưởng trên Odoo, với thông tin so sánh giá sàn và biên lợi nhuận tối thiểu hiển thị ngay trên màn hình phê duyệt.

**Để: **để quyết định phê duyệt đúng đắn mà không cần tra cứu thêm tài liệu.

**Điều kiện chấp nhận: **Màn hình phê duyệt hiển thị: giá đề xuất vs giá sàn vs biên tối thiểu; nếu giá đề xuất < giá sàn, hệ thống tự block và không cho phê duyệt.

**US-04**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn tạo yêu cầu mở/đóng cổng trên Odoo và có thể theo dõi trạng thái xử lý của Phòng Công nghệ.

**Để: **để đảm bảo mọi lệnh mở/đóng cổng đều có hồ sơ, log, người thực hiện và không bị mất.

**Điều kiện chấp nhận: **Phiếu yêu cầu mở/đóng cổng có các trường: cổng, lý do, thời điểm hiệu lực, người yêu cầu, người thực hiện; trạng thái: Draft → Approved (TPKD) → In Progress (Phòng CN) → Done; log timestamp đầy đủ.

**US-05**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn phê duyệt hoàn tiền/nạp bù vượt hạn mức Trưởng dự án và nhìn thấy ngay trên màn hình xem kết quả có vượt hạn mức TPKD không.

**Để: **để kiểm soát chi phí hoàn-bù và biết khi nào cần escalate lên GĐ.

**Điều kiện chấp nhận: **Màn hình phê duyệt hiển thị: hạn mức TPKD vs giá trị hoàn-bù yêu cầu; nếu vượt hạn mức TPKD, nút phê duyệt bị disable và chỉ hiện nút escalate lên GĐ.

**US-06**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn xem báo cáo đối soát doanh thu vs kế toán và phân công người xử lý chênh lệch chưa giải trình.

**Để: **để đảm bảo số liệu KD trùng khớp với Phòng Kế toán và mọi chênh lệch đều được giải quyết trước kỳ chốt.

**Điều kiện chấp nhận: **Bảng đối soát hiển thị: chênh lệch, ngày phát sinh, trạng thái (open/giải trình/done), người được giao; TPKD có thể giao xử lý nhưng không thể tự đóng case khi Phòng KT chưa xác nhận.

**US-07**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn giao chỉ tiêu KPI tháng/quý cho Trưởng dự án và Lead Team bằng văn bản trên Odoo, và xem tiến độ thực hiện KPI theo thời gian thực.

**Để: **để quản lý hiệu suất đội ngũ có hệ thống, có log, và có thể xuất báo cáo KPI.

**Điều kiện chấp nhận: **Phiếu giao chỉ tiêu có chữ ký điện tử xác nhận của cả TPKD và Trưởng dự án; dashboard KPI hiển thị tiến độ thực/chỉ tiêu theo từng người; TPKD không thể sửa dữ liệu nguồn KPI.

**US-08**

**Vai trò: **Là Trưởng phòng Kinh doanh

**Muốn: **tôi muốn xuất báo cáo điều hành KD tháng theo template chuẩn và ký duyệt trực tiếp trên Odoo trước khi gửi BGĐ.

**Để: **để đảm bảo báo cáo đúng format, đúng nguồn dữ liệu và có audit trail.

**Điều kiện chấp nhận: **Template báo cáo có sẵn trên Odoo; sau khi TPKD ký duyệt, hệ thống tự gửi đến danh sách người nhận; log: người lập, người kiểm tra, người phê duyệt, timestamp.

**PHẦN 14. CHECKLIST NGHIỆM THU CẤU HÌNH ODOO CHO ROLE TPKD**

**A. Module ****&**** Menu**

[ ] Tất cả 12 module/menu trong Phần 3 đã được cấp đúng quyền (xem / tạo / phê duyệt / từ chối / xuất) theo ma trận Phần 4.

[ ] Không có module nào cấp quyền sửa/xóa dữ liệu kế toán, dữ liệu kỹ thuật lõi hoặc hồ sơ nhân sự gốc.

[ ] Menu ẩn các mục không thuộc phạm vi TPKD (admin, API key, cấu hình kỹ thuật).

**B. Workflow**

[ ] 10 workflow trong Phần 5 đã được cấu hình đầy đủ trên Odoo (Approval module hoặc custom workflow).

[ ] Mỗi workflow đã test end-to-end: happy path + reject path + escalate path.

[ ] Không có workflow nào cho phép 1 user vừa tạo vừa tự approve trên cùng object.

[ ] Ranh đỏ cứng (Phần 10) đã được cấu hình: khoá thao tác hoặc disable nút khi vi phạm.

**C. Dashboard**

[ ] 9 dashboard trong Phần 6 đã được build và hiển thị đúng với data thực.

[ ] Dashboard realtime (DB-KD-01, DB-KD-02, DB-KD-06) cập nhật ≤ 5 phút.

[ ] Drill-down hoạt động: từ tổng → dự án → sản phẩm → cổng/NCC/đại lý.

[ ] Dashboard ranh đỏ (DB-KD-02) hiển thị đúng 9 panel trạng thái và đổi màu khi kích hoạt.

**D. Cảnh báo / Alert**

[ ] 15 alert trong Phần 7 đã được cấu hình và test với data mô phỏng.

[ ] Alert Critical gửi đến đúng người nhận trong ≤ 5 phút sau khi kích hoạt.

[ ] Alert Medium/High không gây nhiễu; test không bị bỏ qua vì quá nhiều alert không liên quan.

**E. Báo cáo**

[ ] 10 template báo cáo trong Phần 8 đã được cấu hình; TPKD có thể xuất và ký duyệt.

[ ] Báo cáo tự động gửi đến đúng danh sách người nhận sau khi TPKD ký duyệt.

[ ] Báo cáo hiển thị đúng: trạng thái dữ liệu (tạm tính / đã đối soát / đã chốt), người lập, người kiểm tra, người phê duyệt, timestamp.

**F. Phân quyền dữ liệu**

[ ] TPKD không thể sửa số liệu doanh thu / công nợ / tồn kho đã phát sinh.

[ ] TPKD không có quyền truy cập module Accounting ở mức edit/delete.

[ ] TPKD không thấy log kỹ thuật server, API key, cấu hình kỹ thuật lõi.

[ ] TPKD chỉ xem hồ sơ nhân sự Phòng KD, không xem hồ sơ nhân sự các phòng khác.

**G. Audit Log**

[ ] Tất cả thao tác Create/Write/Approve/Reject/Stop của TPKD đều có log đầy đủ (7 trường bắt buộc).

[ ] Không có cơ chế nào cho phép xóa hoặc sửa log.

[ ] TPKD có thể xuất log của Phòng KD; không xuất được log của phòng khác.

**H. Phân quyền kế thừa**

[ ] Role Phó phòng đã được cấu hình với quyền kế thừa theo Phần 12.

[ ] Role Trưởng dự án và Lead Team đã được cấu hình giới hạn đúng phạm vi dự án/nhóm.

[ ] Ủy quyền tạm thời (khi TPKD vắng) có cơ chế ghi log và thời hạn rõ ràng.

**I. User Stories**

[ ] 8 user story trong Phần 13 đã được test với người dùng thực (TPKD hoặc Phó phòng).

[ ] Mỗi user story đạt tất cả điều kiện chấp nhận.

**PHẦN 15. CÁC ĐIỂM CẦN CEO / HCNS / CÔNG NGHỆ CHỐT TRƯỚC KHI TRIỂN KHAI**

**CEO / Giám đốc cần quyết định**

- Hạn mức phê duyệt chính xác của TPKD (giá/CK, hoàn tiền, công nợ) theo ma trận Quy chế Phân quyền – cần có số cụ thể để cấu hình workflow.

- Các sản phẩm / NCC / đại lý nào được phân loại "trọng yếu" – để cấu hình ngưỡng phê duyệt GĐ/HĐQT bắt buộc.

- Ngưỡng cảnh báo cụ thể (% tồn kho thấp, số dư API, số ngày tồn) – để cấu hình alert.

- Ai là người thay thế TPKD (ủy quyền) khi TPKD vắng – cần cấu hình role ủy quyền tạm.

- Xác nhận danh sách người nhận báo cáo điều hành (ngày/tuần/tháng/quý) trước khi cấu hình auto-send.

**Phòng HCNS cần xác nhận**

- Xác nhận danh sách nhân sự Phòng KD được cấp role TPKD / Phó phòng / Trưởng dự án / Lead Team trên Odoo.

- Quy trình ủy quyền tạm thời khi TPKD vắng: hình thức văn bản, kênh ghi nhận, người phê duyệt ủy quyền.

- Phối hợp với Phòng Công nghệ để thu hồi / chỉnh quyền Odoo khi có thay đổi nhân sự.

- Xác nhận dữ liệu nhân sự nào (Phòng KD) được TPKD xem trên Odoo HR module.

**Phòng Công nghệ cần xác nhận kỹ thuật**

- Khả năng tích hợp dữ liệu Bigtel CMS → Odoo (realtime hay batch? API hay file import?) để dashboard hoạt động đúng.

- Cấu hình Approval module của Odoo có đủ để handle 10 workflow trong Phần 5 không, hay cần custom module?

- Cơ chế lưu audit log: dùng Odoo built-in chatter/log hay cần custom audit log module?

- Cơ chế block ranh đỏ: dùng Odoo domain/record rules hay cần Python override?

- Xác nhận các bảng dữ liệu (model) nào trên Odoo tương ứng với các đối tượng trong ma trận quyền (Phần 4).

- Timeline triển khai và môi trường test trước khi go-live.

**Phòng Innovation cần chuẩn hóa**

- Chuẩn hóa nội dung và layout 9 dashboard trước khi bàn giao cho Phòng Công nghệ build.

- Xác nhận công thức tính KPI và nguồn dữ liệu cho từng chỉ tiêu trong dashboard.

- Pilot 1-2 workflow cấu hình trước khi triển khai toàn bộ 10 workflow.

- Nghiệm thu business logic của dashboard và workflow trước khi bàn giao vận hành.

*Hà Nội, ngày …… tháng …… năm 2026*

| **Soạn thảo** | **Kiểm tra ****&**** nghiệm thu** | **Phê duyệt triển khai** |
| --- | --- | --- |
| Trưởng phòng Innovation | Trưởng phòng Công nghệ Trưởng phòng HCNS | Giám đốc Nguyễn Trọng Thắng |

Bảo mật – Chỉ lưu hành nội bộ Octa