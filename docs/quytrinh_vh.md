**QUY TRÌNH THỰC HIỆN CÔNG VIỆC VẬN HÀNH THƯƠNG MẠI**

**Áp dụng cho các mã việc VH01 – VH08 tại Octa**

Tài liệu hướng dẫn thao tác chuẩn dùng cho nhân viên thực hiện, quản lý trực tiếp, nhân sự mới, nhân sự học việc và làm căn cứ cấu hình Odoo

Phiên bản: V1 | Ngày ban hành: 04/04/2026

**MỤC ĐÍCH VÀ CÁCH SỬ DỤNG**

Tài liệu này chuyển phần mô tả hành động thành quy trình thao tác chuẩn, giúp nhân sự hiểu rõ phải làm gì, làm đến đâu là xong và khi nào phải báo cấp trên.

Mỗi mã việc gồm 6 phần thống nhất: mục tiêu, đầu vào tối thiểu, kết quả cần đạt, SLA/Gate, quy trình thực hiện và lưu ý quản lý.

Nguyên tắc sử dụng: phát sinh việc nào thì mở đúng mã việc đó; xử lý theo từng bước; cập nhật kết quả cuối và chỉ đóng việc khi đủ điều kiện nghiệm thu.

Tài liệu đồng thời là đầu bài cho đối tác phát triển Odoo: cần hiểu đúng bản chất từng đầu việc để cấu hình workflow, checklist, ticket, phê duyệt, báo cáo và KPI hiệu quả.

**TỔNG HỢP NHANH VH01 – VH08**

| **Mã việc** | **Tên việc** | **Loại việc** | **SLA / Gate chính** |
| --- | --- | --- | --- |
| VH01 | Lập kế hoạch/đề xuất mua hàng dự kiến (mã thẻ, thẻ cào, API “nạp tiền tài khoản mua hàng qua API”) | Ticket sự vụ | Lập kế hoạch mua hàng theo tuần/tháng/ngày; đề xuất ngày phải hoàn thành trước 9:00 sáng; không để xảy ra thiếu hàng gây đứt doanh thu hoặc thừa hàng vượt mốc quy định. |
| VH02 | Điều phối luồng giao dịch (đóng/mở/chuyển gate mua hàng API hoặc kho mã thẻ của công ty) | Checklist định kỳ + Ticket sự vụ | Đảm bảo tính sẵn sàng của các cổng và cổng backup; kích hoạt điều hướng luồng giao dịch ngay khi cổng chính lỗi, hết số dư hoặc hết hàng. |
| VH03 | Xây dựng, quản lý hợp đồng (hồ sơ khách hàng), chính sách và chất lượng | Ticket sự vụ | Hồ sơ/hợp đồng/chính sách phải đầy đủ, đúng mẫu, đúng thời điểm áp dụng; thay đổi phải được cập nhật và lưu vết kịp thời. |
| VH04 | Thúc đẩy doanh thu & chăm sóc khách hàng lớn | Checklist định kỳ + Ticket sự vụ | Cập nhật kế hoạch và doanh số thực hiện của đại lý/đối tác trọng yếu; cảnh báo sớm khi lệch cam kết hoặc có thay đổi bất thường. |
| VH05 | Điều phối bộ phận sản xuất (chuyển đổi thẻ cào sang mã thẻ dạng PIN) | Checklist định kỳ + Ticket sự vụ | Sản xuất đúng kế hoạch nhập hàng; hàng lên kho kịp thời; không để gián đoạn nguồn hàng do chậm sản xuất hoặc lỗi đọc mã. |
| VH06 | Dịch vụ ứng tiền (ứng tiền tài khoản Viettel) | Ticket sự vụ | Báo cáo đối soát đúng hạn, đúng số liệu; cập nhật kịch bản/chính sách kịp thời; duy trì dịch vụ vận hành ổn định. |
| VH07 | Vận hành vé máy bay | Ticket sự vụ | Mỗi giao dịch hoặc nhóm giao dịch phải có trạng thái cuối rõ ràng; số dư quỹ xuất vé luôn an toàn; xử lý phát sinh đúng hạn. |
| VH08 | Báo cáo vận hành thương mại | Checklist định kỳ + Ticket sự vụ | Dashboard ngày phải sẵn sàng trước 9:00 sáng; báo cáo phân tích tuần/tháng/quý hoàn thành đúng thời hạn cam kết. |

**VH01 – Lập kế hoạch/ đề xuất mua hàng dự kiến**

| **Loại cấu hình Odoo** | Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Bảo đảm nguồn hàng mã thẻ, thẻ cào và tài khoản API luôn đủ cho kế hoạch bán hàng; hạn chế thiếu hàng gây đứt doanh thu và hạn chế thừa hàng gây ứ đọng vốn hoặc tăng rủi ro tồn kho. |
| **Đầu vào tối thiểu** | Tồn kho đầu kỳ; số dư tài khoản API; sản lượng chạy ngày hôm trước; dữ liệu cùng kỳ tháng trước; lượng hàng chạy đầu ngày; đơn hàng đã gửi/chưa nhận; kế hoạch bán hàng; chỉ đạo PKD; ngưỡng tồn tối thiểu/tối đa. |
| **Kết quả cần đạt / SLA / KPI** | Phải có đề xuất mua hàng/ngày rõ số lượng, thời điểm, loại hàng và nguồn mua; đơn hàng được gửi trước 9:00 sáng hoặc theo hạn chốt được giao; các ticket bổ sung trong ngày phải có lý do rõ ràng. KPI: số đề xuất đúng hạn; chênh lệch giữa dự kiến và thực tế; số lần thiếu hàng/thừa hàng vượt ngưỡng. |

**Quy trình thực hiện**

1. Thu thập dữ liệu đầu ngày: Đăng nhập Gate Kho, Gate Topup, Portal đối tác/API và các màn hình cần thiết để lấy tồn kho hiện tại, số dư API, hàng đang chạy đầu ngày, lịch sử chạy ngày hôm trước và cùng kỳ tháng trước.

2. Kiểm tra tồn đặc thù theo nguồn: Với mã pin Viettel, phải kiểm tra riêng lượng thẻ cào chưa làm, thẻ đã cào chưa chụp, thẻ đã nhập kho và hàng đang chờ sản xuất. Với mã pin Vina hoặc nguồn NCC khác, kiểm tra tồn thực tế, đơn đang đặt và khả năng rút hàng. Với API, kiểm tra số dư từng cổng đang dùng.

3. Dự báo lượng chạy trong ngày: Căn cứ dữ liệu lịch sử, tốc độ chạy đầu ngày, biến động doanh số gần nhất, các chương trình bán hàng hoặc chỉ đạo kinh doanh để ước lượng nhu cầu trong ngày/ca.

4. Lập đề xuất mua hàng: Xác định số lượng cần nhập thêm cho từng nguồn hàng; tách rõ đề xuất cho hàng thẻ vật lý, mã thẻ, topup và nạp tiền API; nêu rõ mức tồn sau nhập dự kiến và lý do nếu cần mua bổ sung đột biến.

5. Gửi đề xuất và xin xác nhận: Chuyển ticket/kế hoạch cho Tài chính để chốt phương án vốn và cho Kế toán/đầu mối NCC để triển khai đơn mua theo đúng luồng nội bộ.

6. Theo dõi nhận hàng/nhận tiền: Với đơn mã pin Viettel, theo dõi bộ phận sản xuất nhận hàng và kiểm tra số lượng thực nhận so với đơn. Với Vina/NCC khác, theo dõi việc nâng tiền vào tài khoản NCC và thao tác rút hàng. Với API, kiểm tra NCC đã nâng đúng số tiền trên cổng tương ứng.

7. Giám sát sau đặt hàng: Trong ngày, tiếp tục theo dõi lượng giao dịch thực tế; nếu có biến động mạnh so với dự kiến thì mở ticket bổ sung, điều chỉnh hoặc cảnh báo ngay để không thiếu hàng.

8. Chốt ticket cuối ngày: Cập nhật kết quả thực hiện gồm: số lượng đề xuất, số lượng mua thực tế, chênh lệch, nguyên nhân chênh lệch và các điểm cần rút kinh nghiệm cho kỳ sau.

**Lưu ý / điểm kiểm soát**

Mọi ticket phải có xác nhận hoặc dấu vết phối hợp từ Tài chính và Kế toán theo đúng luồng mua hàng.

Không gửi đề xuất chỉ dựa trên cảm tính; phải có căn cứ dữ liệu tối thiểu và mức tồn mục tiêu.

Nếu phát sinh rủi ro thiếu hàng nhưng chưa chốt được nguồn vốn hoặc NCC, phải cảnh báo ngay quản lý thay vì chờ đến khi đứt doanh thu.

**VH02 – Điều phối luồng giao dịch**

| **Loại cấu hình Odoo** | Checklist định kỳ + Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Tối ưu phân bổ lưu lượng giao dịch giữa các cổng API/kho hàng dựa trên độ ổn định, kế hoạch phòng, tốc độ xử lý, mức tồn, số dư và cam kết thương mại; đồng thời bảo đảm luôn có phương án backup khi cổng chính gặp sự cố. |
| **Đầu vào tối thiểu** | Tên cổng chính/cổng backup; tên sản phẩm chạy; số dư các cổng; tồn kho từng nguồn; tỷ lệ thành công/thất bại; tốc độ xử lý; trạng thái NCC; chỉ đạo PKD. |
| **Kết quả cần đạt / SLA / KPI** | Cổng chính và cổng dự phòng luôn trong trạng thái sẵn sàng; luồng giao dịch được điều hướng đúng thời điểm khi cổng chính lỗi, hết số dư hoặc hết hàng; mọi điều chỉnh có dấu vết và kết quả sau điều chỉnh. KPI: tỷ lệ cổng ổn định; số lần điều phối kịp thời; tỷ lệ giao dịch thành công sau điều phối. |

**Quy trình thực hiện**

1. Mở màn hình theo dõi cổng: Truy cập các cổng đang vận hành trong ca và xác nhận dữ liệu đang cập nhật bình thường.

2. Kiểm tra sức khỏe cổng: Theo dõi tốc độ xử lý, tỷ lệ thất bại, tỷ lệ giao dịch treo, số dư API, tồn kho thương mại và cảnh báo từ NCC/đối tác.

3. So sánh cổng chính với cổng backup: Đánh giá cổng nào đang có mức ưu tiên cao hơn, tốc độ tốt hơn, ổn định hơn và còn đủ năng lực xử lý cho khối lượng giao dịch hiện tại.

4. Thực hiện đóng/mở/chuyển cổng: Khi cổng chính lỗi, hết số dư, hết hàng, tỷ lệ thất bại tăng hoặc có chỉ đạo thương mại, phải thực hiện điều phối ngay theo quy tắc đã được phê duyệt.

5. Ghi nhận lý do điều phối: Cập nhật trong checklist/ticket lý do đóng/mở/chuyển cổng, thời điểm thực hiện, cổng thay thế và người đã được thông báo.

6. Theo dõi kết quả sau điều phối: Kiểm tra lại tỷ lệ giao dịch, trạng thái thất bại/treo và doanh số sau khi chuyển luồng để xác nhận điều phối đạt mục tiêu.

7. Mở ticket sự vụ khi cần: Nếu sự cố không chỉ là điều phối thông thường mà có dấu hiệu lỗi hệ thống, lỗi NCC hoặc đứt doanh thu diện rộng, phải mở ticket sự vụ và phối hợp Kỹ thuật/NCC xử lý.

8. Chốt ca hoặc kỳ kiểm tra: Kết thúc mỗi kỳ theo dõi phải chốt tình trạng cổng: bình thường / đã điều phối / đang lỗi / đã mở ticket / đang chờ NCC.

**Lưu ý / điểm kiểm soát**

Không điều phối cổng chỉ theo cảm giác; mọi thay đổi phải có căn cứ từ số dư, tốc độ, tồn kho, lỗi giao dịch hoặc chỉ đạo rõ ràng.

Khi đóng/mở/chuyển cổng phải thông tin cho các đầu mối liên quan theo quy định để tránh phát sinh hiểu nhầm trong vận hành và CSKH.

Nếu nhiều cổng cùng phát sinh lỗi trong một khoảng thời gian ngắn, phải xử lý theo hướng sự cố hệ thống thay vì điều chỉnh đơn lẻ.

**VH03 – Xây dựng, quản lý hợp đồng (hồ sơ khách hàng), chính sách và chất lượng**

| **Loại cấu hình Odoo** | Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Bảo đảm hồ sơ khách hàng/đối tác, hợp đồng, phụ lục và chính sách thương mại được cập nhật đầy đủ, đúng mẫu, đúng thời điểm áp dụng; đồng thời duy trì chất lượng thông tin để giảm tranh chấp và sai lệch khi triển khai. |
| **Đầu vào tối thiểu** | Thông tin khách hàng/đối tác; mẫu hợp đồng/phụ lục; nội dung chính sách đã được phê duyệt; thời gian hiệu lực; đối tượng áp dụng; tài liệu chất lượng hoặc phản ánh cần cập nhật. |
| **Kết quả cần đạt / SLA / KPI** | Hồ sơ/ CCCD/hợp đồng/chính sách đầy đủ, đúng mẫu, lưu vết rõ; thay đổi chính sách được cập nhật kịp thời, truyền thông đúng đối tượng và có dấu vết xác nhận. KPI: tỷ lệ hồ sơ hoàn tất đúng hạn; số sai sót do dùng sai mẫu/sai chính sách; tỷ lệ cập nhật đúng thời điểm. |

**Quy trình thực hiện**

1. Tiếp nhận yêu cầu: Nhận đề xuất từ Kinh doanh, CSKH, lãnh đạo hoặc đối tác liên quan đến hồ sơ khách hàng, hợp đồng, phụ lục, chính sách giá/chiết khấu hoặc yêu cầu cập nhật chất lượng.

2. Kiểm tra tính đầy đủ của đầu vào: Xác minh thông tin khách hàng/đối tác, mẫu biểu, nội dung phê duyệt, thời gian hiệu lực, người có thẩm quyền và phạm vi áp dụng.

3. Soạn thảo/cập nhật tài liệu: Lập hoặc chỉnh sửa hợp đồng, phụ lục, biên bản, chính sách hoặc thông báo theo mẫu chuẩn của công ty; bảo đảm ngôn ngữ rõ, không gây hiểu sai và phù hợp phạm vi phê duyệt.

4. Phối hợp liên phòng khi cần: Nếu hồ sơ liên quan CSKH, HCNS, Kế toán, Tài chính hoặc Kỹ thuật thì phải chuyển đúng đầu mối để bổ sung phần việc chuyên môn hoặc xác nhận thông tin trước khi ban hành.

5. Gửi khách hàng/đối tác hoặc triển khai nội bộ: Gửi tài liệu tới đúng đối tượng; hướng dẫn các bước ký/nhận/xác nhận; nếu là chính sách mới thì thực hiện đăng tải/gửi mail/thông báo theo danh sách áp dụng.

6. Lưu trữ và theo dõi phản hồi: Lưu bằng chứng gửi đi, phản hồi nhận lại, thời gian hiệu lực và các ý kiến phát sinh; cập nhật ticket đến khi hoàn tất.

7. Kiểm tra sau triển khai: Nếu phát sinh khiếu nại về hồ sơ/chính sách/chất lượng, phải truy lại tài liệu đã ban hành và đánh giá nguyên nhân để điều chỉnh hoặc chuẩn hóa lại.

8. Chốt ticket: Chỉ đóng khi hồ sơ/chính sách đã được cập nhật, lưu trữ và không còn vướng đầu việc đang chờ.

**Lưu ý / điểm kiểm soát**

Không được áp dụng chính sách, mẫu hợp đồng hoặc thông báo khi chưa có phê duyệt hợp lệ.

Mọi thay đổi chính sách ảnh hưởng khách hàng/đối tác phải có dấu vết về thời gian thông báo và phạm vi người nhận.

VH03 là đầu mối vận hành hồ sơ/chính sách trên góc độ thương mại, không thay thế Kế toán ở phần hóa đơn/chứng từ thuế và không thay HCNS ở phần hồ sơ nhân sự.

**VH04 – Thúc đẩy doanh thu ****&**** chăm sóc khách hàng lớn**

| **Loại cấu hình Odoo** | Checklist định kỳ + Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Nắm chắc kế hoạch doanh số của nhóm khách hàng/đại lý/đối tác trọng yếu, hỗ trợ và đôn đốc đúng thời điểm để bảo đảm hoàn thành doanh số cam kết và phát hiện sớm dấu hiệu suy giảm doanh thu. |
| **Đầu vào tối thiểu** | Danh sách khách hàng/đại lý trọng yếu; doanh số tháng trước; doanh số cùng kỳ; doanh số thực hiện theo tuần/ngày; doanh số cam kết; kế hoạch tháng; thông tin phát sinh bất thường. |
| **Kết quả cần đạt / SLA / KPI** | Có cập nhật doanh số và kế hoạch chạy của từng đối tác; có nhắc việc/đôn đốc đúng thời điểm; có cảnh báo sớm khi doanh số lệch kế hoạch hoặc có biến động bất thường. KPI: tỷ lệ cập nhật đúng hạn; tỷ lệ khách trọng yếu được theo dõi; tỷ lệ hoàn thành doanh số theo nhóm. |

**Quy trình thực hiện**

1. Truy cập dữ liệu doanh số: Đăng nhập portal hoặc báo cáo nội bộ để kiểm tra doanh số các tháng trước, doanh số hiện tại và tình trạng phát sinh của từng đại lý/đối tác trọng yếu.

2. Xác định nhóm cần theo dõi: Lọc nhóm đối tác có doanh số lớn, có cam kết sản lượng, có xu hướng giảm mạnh hoặc có dấu hiệu rủi ro cần ưu tiên chăm sóc.

3. Liên hệ và cập nhật kế hoạch chạy: Trao đổi với đầu mối đại lý/đối tác về doanh số dự kiến trong tháng/tuần, nhu cầu hàng, khó khăn phát sinh hoặc thay đổi vận hành có thể ảnh hưởng doanh số.

4. So sánh kế hoạch với thực tế: Hàng tuần hoặc theo chu kỳ quản lý, đối chiếu doanh số thực tế với mục tiêu/cam kết; xác định mức lệch và nguyên nhân sơ bộ.

5. Hỗ trợ và đôn đốc: Nếu đối tác lệch kế hoạch, chủ động nhắc việc, hỗ trợ phối hợp nguồn hàng, cổng, chính sách hoặc xử lý phát sinh để kéo lại doanh số.

6. Cảnh báo bất thường: Khi phát hiện đại lý giảm sâu, ngưng giao dịch, thay đổi nhu cầu, có khiếu nại lặp lại hoặc có nguy cơ không đạt cam kết, phải mở ticket/cảnh báo cho quản lý và đầu mối liên quan.

7. Ghi nhận kết quả chăm sóc: Mỗi lần theo dõi phải cập nhật tình trạng doanh số, thông tin đã trao đổi, hành động đã thực hiện và kết quả tạm thời.

8. Chốt kỳ theo dõi: Cuối tuần/tháng, tổng hợp kết quả theo từng đối tác trọng yếu, nêu rõ đối tác nào đạt/không đạt, nguyên nhân và hành động tiếp theo.

**Lưu ý / điểm kiểm soát**

Mục tiêu của checklist này là upsell doanh số và bảo vệ doanh thu, không chỉ là gọi điện hỏi thăm.

Báo cáo phải có đủ: doanh số cam kết, doanh số thực hiện, chênh lệch và cảnh báo theo từng đối tác/đại lý.

Nếu thông tin từ đối tác ảnh hưởng trực tiếp tới kế hoạch nguồn hàng, cổng hoặc dòng tiền thì phải chuyển đầu mối liên quan ngay, không giữ thông tin cục bộ.

**VH05 – Điều phối bộ phận sản xuất**

| **Loại cấu hình Odoo** | Checklist định kỳ + Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Điều phối hoạt động sản xuất thẻ cào thành mã PIN theo đúng kế hoạch nhập hàng, bảo đảm hàng lên kho kịp thời, đúng số lượng, đúng chất lượng và không gây gián đoạn nguồn hàng bán. |
| **Đầu vào tối thiểu** | Kế hoạch nhập hàng; danh sách lô thẻ cần sản xuất; số lượng ảnh thẻ/ thẻ vật lý nhận về; tiến độ tồn đọng; năng lực xử lý của ca; danh sách thẻ chưa đọc tự động; tiêu chuẩn nhập kho. |
| **Kết quả cần đạt / SLA / KPI** | Hàng được sản xuất và nhập kho đúng kế hoạch; thẻ chưa đọc tự động được rà soát và phối hợp kỹ thuật xử lý; lỗi sản xuất và thẻ lỗi được tách riêng và báo cáo rõ. KPI: sản lượng/ca; tỷ lệ hoàn thành kế hoạch sản xuất; tỷ lệ đọc mã thành công; số thẻ lỗi còn tồn. |

**Quy trình thực hiện**

1. Nhận kế hoạch và phân công ca: Căn cứ kế hoạch nhập hàng từ VH01 hoặc chỉ đạo PKD, phân công rõ người nhận thẻ cào, người scan, người kiểm tra lại, người nhập kho và người tổng hợp báo cáo.

2. Kiểm tra đầu vào sản xuất: Xác nhận số lượng thẻ nhận được, tình trạng hàng, mức độ ưu tiên từng lô và thời hạn cần lên kho.

3. Điều phối sản xuất theo mức ưu tiên: Sắp xếp lô hàng cần làm trước theo kế hoạch bán hàng, mức tồn kho hiện tại và chỉ đạo kinh doanh; không để đội sản xuất làm dàn trải khi một lô đang cấp bách.

4. Theo dõi quá trình scan và đọc mã: Giám sát tiến độ phần mềm đọc mã, số lượng đã xử lý, số lượng lỗi, số lượng chưa đọc được tự động và thời gian hoàn thành dự kiến.

5. Kiểm soát thẻ chưa đọc tự động: Tách riêng danh sách thẻ lỗi/không đọc được; tổ chức kiểm tra lại thủ công; xác minh mã đúng trước khi cho nhập kho.

6. Khai báo nhập kho: Sau khi mã được xác nhận, thực hiện hoặc xác nhận thao tác nhập kho vào hệ thống; đối chiếu số lượng đã sản xuất với số lượng dự kiến và số lượng đã lên kho.

7. Báo cáo sản xuất và lỗi: Cuối ca hoặc khi có phát sinh bất thường, tổng hợp sản lượng, tồn đọng, tỷ lệ thành công, số thẻ lỗi, nguyên nhân sơ bộ và nhu cầu hỗ trợ thêm nếu có.

8. Mở ticket sự vụ khi phát sinh rủi ro: Nếu sản xuất chậm, lỗi hàng loạt, phần mềm đọc mã lỗi, thiếu nhân lực hoặc có nguy cơ đứt nguồn hàng, phải mở ticket và báo quản lý ngay.

**Lưu ý / điểm kiểm soát**

VH05 là đầu mối điều phối sản xuất, không chỉ là theo dõi sản lượng cuối ngày.

Không nhập kho các mã chưa được xác minh rõ hoặc các thẻ lỗi chưa phân loại nguyên nhân.

Mọi chênh lệch giữa số lượng nhận – số lượng sản xuất – số lượng nhập kho phải được ghi nhận và giải trình.

**VH06 – Dịch vụ ứng tiền**

| **Loại cấu hình Odoo** | Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Duy trì dịch vụ ứng tiền Viettel vận hành ổn định, đúng quy trình phối hợp với đối tác/kỹ thuật; bảo đảm báo cáo đối soát chính xác, cập nhật kịch bản vận hành kịp thời và xử lý nhanh các phát sinh liên quan. |
| **Đầu vào tối thiểu** | Lịch làm việc/đầu mối Viettel; dữ liệu CMS; mẫu báo cáo; yêu cầu từ Kỹ thuật; thay đổi chính sách/kịch bản ứng tiền; các phản ánh phát sinh liên quan dịch vụ. |
| **Kết quả cần đạt / SLA / KPI** | Báo cáo đối soát được trích xuất và gửi đúng hạn; thay đổi chính sách/kịch bản được cập nhật và chuyển đúng đầu mối; mọi ticket có trạng thái cuối rõ ràng. KPI: tỷ lệ báo cáo đúng hạn; tỷ lệ dữ liệu chính xác; thời gian cập nhật kịch bản; số phát sinh được xử lý đúng hạn. |

**Quy trình thực hiện**

1. Chủ động làm việc với đầu mối Viettel: Trong tuần đầu của kỳ mới hoặc theo lịch quy định, liên hệ đầu mối hỗ trợ Viettel để chốt lịch làm việc, lịch báo cáo hoặc các nội dung cần phối hợp.

2. Truy cập hệ thống CMS: Đăng nhập đúng tài khoản, trích xuất dữ liệu báo cáo theo kỳ, kiểm tra định dạng và số liệu tổng thể trước khi gửi đi.

3. Gửi dữ liệu cho đầu mối kỹ thuật/vận hành liên quan: Chuyển file báo cáo hoặc dữ liệu cần thiết cho Kỹ thuật theo đúng form, đúng thời hạn; bảo đảm có xác nhận đã nhận dữ liệu.

4. Theo dõi và xử lý thay đổi: Nếu có thay đổi chính sách, kịch bản vận hành, chỉ số kiểm soát hoặc yêu cầu mới từ Viettel/công ty, phải cập nhật nội dung và chuyển đến các đầu mối triển khai đúng thời điểm.

5. Ghi nhận các phản ánh/phát sinh: Với các lỗi hoặc khiếu nại liên quan ứng tiền, mở ticket và mô tả rõ tình trạng, phạm vi ảnh hưởng, dữ liệu đã trích xuất và đầu mối đang xử lý.

6. Theo dõi đến khi có xác nhận cuối: Không đóng ticket khi chỉ mới gửi báo cáo; phải theo dõi đến khi Kỹ thuật/đầu mối liên quan xác nhận dữ liệu đã dùng được hoặc phát sinh đã xử lý xong.

7. Báo cáo lại quản lý khi có bất thường: Nếu dữ liệu CMS thiếu, lệch, trích xuất chậm hoặc chính sách thay đổi ảnh hưởng vận hành, phải báo ngay quản lý thay vì chờ đủ kỳ báo cáo.

8. Lưu vết hồ sơ xử lý: Lưu file báo cáo, thời gian gửi, người nhận, xác nhận phản hồi và các thay đổi đã cập nhật để phục vụ đối soát sau này.

**Lưu ý / điểm kiểm soát**

Mọi ticket phải có báo cáo hoặc dữ liệu được Kỹ thuật/đầu mối nhận và xác nhận theo quy định.

VH06 không phải chỉ là gửi báo cáo; mục tiêu là duy trì được dịch vụ, bám thay đổi và bảo đảm luồng phối hợp không đứt đoạn.

Nếu thay đổi chính sách/kịch bản ứng tiền có ảnh hưởng khách hàng hoặc vận hành hệ thống, phải mở luồng phối hợp với phụ trách Kinh doanh/Kỹ thuật ngay.

**VH07 – Vận hành vé máy bay**

| **Loại cấu hình Odoo** | Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Vận hành ổn định dịch vụ vé máy bay trên BigM, xử lý đúng các phát sinh xuất/hoàn/đổi/hủy vé, hỗ trợ khách hàng đúng thời hạn và duy trì số dư quỹ xuất vé an toàn. |
| **Đầu vào tối thiểu** | Yêu cầu từ CSKH/đại lý; mã giao dịch/đơn vé; loại yêu cầu (xuất/hoàn/đổi/hủy); thông tin đối tác/NCC; số dư quỹ; log hoặc email thay đổi từ NCC. |
| **Kết quả cần đạt / SLA / KPI** | Mỗi giao dịch hoặc nhóm giao dịch phải có trạng thái cuối rõ ràng: thành công / thất bại / chuyển kỹ thuật / báo NCC / tiếp tục theo dõi có kiểm soát. Theo dõi số dư quỹ xuất vé không âm và đề xuất nạp thêm khi số dư ≤20 triệu VNĐ. KPI: tỷ lệ ticket đúng hạn; tỷ lệ giao dịch chốt trạng thái cuối; tỷ lệ phát sinh được xử lý ngay từ lần đầu. |

**Quy trình thực hiện**

1. Tiếp nhận yêu cầu vận hành: Nhận thông tin từ CSKH, đại lý hoặc hệ thống về yêu cầu xuất vé, đổi vé, hoàn vé, hủy vé hoặc khiếu nại liên quan giao dịch vé máy bay.

2. Kiểm tra thông tin giao dịch và phạm vi xử lý: Xác định loại yêu cầu, mã đơn, trạng thái hiện tại, hãng bay/NCC liên quan và kiểm tra đây có phải phát sinh thuộc Octa/BigM hay không.

3. Thực hiện nghiệp vụ theo đúng quyền hạn: Xử lý xuất/hoàn/đổi/hủy vé theo quy định nghiệp vụ đã được hướng dẫn; nếu phát sinh lỗi ngoài nghiệp vụ chuẩn thì chuyển Kỹ thuật hoặc NCC đúng đầu mối.

4. Kiểm tra lịch sử và phản hồi từ NCC: Sau khi thao tác, rà soát lại toàn bộ lịch sử xử lý; nếu NCC gửi email hoặc cập nhật thay đổi chuyến bay thì phải chuyển/gửi lại thông tin cho khách hàng hoặc CSKH ngay.

5. Theo dõi số dư quỹ xuất vé: Truy cập trang quản trị vé máy bay, kiểm tra số dư quỹ; nếu quỹ ≤20 triệu VNĐ thì lập đề xuất nạp thêm và theo dõi đến khi số dư được bổ sung an toàn.

6. Cập nhật ticket và thông tin cho CSKH: Ghi rõ việc đã làm, kết quả hiện tại, các bước còn chờ, tài liệu/bằng chứng liên quan và thông tin cần CSKH phản hồi cho khách.

7. Mở ticket sự cố diện rộng khi cần: Nếu xuất hiện nhiều giao dịch cùng lỗi hoặc NCC/hệ thống phát sinh lỗi diện rộng, phải xử lý theo hướng sự cố hệ thống thay vì từng ticket đơn lẻ.

8. Chốt ticket: Chỉ đóng khi giao dịch đã về trạng thái cuối hoặc đã được bàn giao đầy đủ cho đầu mối xử lý tiếp theo với bằng chứng rõ ràng.

**Lưu ý / điểm kiểm soát**

VH07 là công việc vận hành giao dịch thực tế, không chỉ kiểm tra báo cáo.

Số dư quỹ là điểm kiểm soát trọng yếu; không để quỹ âm hoặc xuống thấp mà không có đề xuất nạp thêm.

Mọi thay đổi chuyến bay hoặc phản hồi từ NCC phải được truyền lại cho khách hàng/CSKH kịp thời để tránh khiếu nại vượt cấp.

**VH08 – Báo cáo vận hành thương mại**

| **Loại cấu hình Odoo** | Checklist định kỳ + Ticket sự vụ |
| --- | --- |
| **Mục tiêu công việc** | Cung cấp báo cáo vận hành thương mại đúng hạn, đúng số liệu, đủ lớp nhìn điều hành để lãnh đạo và các đầu mối liên quan có căn cứ ra quyết định trong ngày và theo kỳ. |
| **Đầu vào tối thiểu** | Dữ liệu portal/hệ thống; dữ liệu kho/API/cổng; báo cáo sản xuất; số liệu doanh số; sự cố vận hành; mẫu dashboard và mẫu báo cáo phân tích đã thống nhất. |
| **Kết quả cần đạt / SLA / KPI** | Dashboard ngày sẵn sàng trước 9:00 sáng; báo cáo phân tích tuần/tháng/quý hoàn thành đúng thời hạn; số liệu có thể đối chiếu và giải thích được. KPI: tỷ lệ báo cáo đúng hạn; tỷ lệ sai số liệu; số cảnh báo được nêu kịp thời trong báo cáo. |

**Quy trình thực hiện**

1. Xác định chu kỳ báo cáo cần làm: Tách rõ báo cáo ngày, báo cáo tuần, báo cáo tháng/quý và báo cáo đột xuất theo yêu cầu quản lý.

2. Trích xuất dữ liệu nguồn: Lấy dữ liệu từ portal, kho hàng, tài khoản API, cổng giao dịch, sản xuất, doanh số, vé máy bay, ứng tiền và các nguồn liên quan theo từng mẫu báo cáo.

3. Kiểm tra và chuẩn hóa số liệu: So khớp số tổng, kiểm tra dữ liệu thiếu, loại trừ trùng lặp và xác nhận các chỉ tiêu trọng yếu trước khi tổng hợp.

4. Tổng hợp dashboard ngày: Cập nhật các chỉ số vận hành chính (nguồn hàng, cổng, sự cố, doanh số, cảnh báo) và hoàn tất dashboard trước 9:00 sáng.

5. Thực hiện báo cáo phân tích: Với báo cáo tuần/tháng/quý, bổ sung phân tích nguyên nhân, xu hướng, rủi ro, điểm bất thường, tác động doanh thu và đề xuất hành động tiếp theo.

6. Gửi và lưu vết báo cáo: Gửi đúng nhóm nhận, đúng thời hạn; lưu file báo cáo, thời gian phát hành và bản dữ liệu nguồn để có thể đối chiếu khi cần.

7. Mở ticket nếu số liệu có vấn đề: Nếu phát hiện chênh lệch dữ liệu, thiếu dữ liệu hoặc có sự cố ảnh hưởng chất lượng báo cáo, phải mở ticket và theo dõi xử lý thay vì tự ước lượng.

8. Cập nhật bài học và chuẩn hóa mẫu: Khi lãnh đạo yêu cầu thêm chỉ tiêu hoặc có điểm chưa hợp lý trong cách trình bày, phải cập nhật mẫu để các kỳ sau dùng thống nhất.

**Lưu ý / điểm kiểm soát**

Báo cáo vận hành không chỉ là tổng hợp số; phải làm rõ vấn đề, cảnh báo và gợi ý hành động.

Mọi số liệu trọng yếu phải truy ra được nguồn gốc nếu quản lý yêu cầu kiểm tra lại.

Nếu báo cáo ngày chưa sẵn sàng trước 9:00 sáng phải báo lý do và thời điểm hoàn thành dự kiến ngay, không để lãnh đạo chờ không thông tin.

**NGUYÊN TẮC QUẢN LÝ CHUNG KHI ÁP DỤNG**

Mọi sự vụ phải có kết quả cuối rõ ràng; không chấp nhận trạng thái “đã xử lý” nhưng không mô tả xử lý xong như thế nào.

Các checklist đầu ca/định kỳ nếu phát hiện bất thường phải tạo sự vụ ngay, không chỉ ghi nhận rồi để đó.

Nếu vượt SLA mà chưa có kết quả cuối, nhân viên phải chủ động báo quản lý và cập nhật lý do kéo dài trên hệ thống.

Những trường hợp có nguy cơ ảnh hưởng doanh thu diện rộng, lỗi hàng loạt, lỗi lặp lại hoặc làm đứt nguồn hàng phải escalte ngay.

Với Odoo, mỗi mã việc nên có trạng thái chuẩn, đầu vào tối thiểu, bằng chứng xử lý, owner, deadline và khả năng mở ticket ngay từ checklist.

Tài liệu này được dùng cho vận hành nội bộ và là căn cứ mô tả nghiệp vụ để đối tác cấu hình Odoo cho đúng thực tế công việc của Octa.

Tài liệu ban hành dùng nội bộ Octa.

**CEO / Người phê duyệt**