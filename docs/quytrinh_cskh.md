**QUY TRÌNH TH****Ự****C HI****Ệ****N CÔNG VI****Ệ****C CSKH**

**Áp d****ụ****ng cho các mã vi****ệ****c CS01 – CS10 t****ạ****i Octa**

Tài liệu hướng dẫn thao tác chuẩn dùng cho nhân viên thực hiện, quản lý trực tiếp, nhân sự mới và nhân sự học việc

Phiên bản: V3 | Ngày ban hành: 22/03/2026

**M****Ụ****C ĐÍCH VÀ ****CÁCH S****Ử**** D****Ụ****NG**

Tài liệu này chuyển phần mô tả hành động thành quy trình thao tác chuẩn, giúp nhân sự hiểu rõ phải làm gì, làm đến đâu là xong và khi nào phải báo cấp trên.

Mỗi mã việc gồm 6 phần thống nhất: mục tiêu, đầu vào tối thiểu, kết quả cần đạt, SLA/Gate, quy trình thực hiện và lưu ý quản lý.

Nguyên tắc sử dụng: phát sinh việc nào thì mở đúng mã việc đó; xử lý theo từng bước; cập nhật kết quả cuối và chỉ đóng việc khi đủ điều kiện nghiệm thu.

**T****Ổ****NG H****Ợ****P NHANH CS01 – CS10**

| **Mã vi****ệ****c** | **Tên vi****ệ****c** | **Lo****ạ****i vi****ệ****c** | **SLA / ****Gate chính** |
| --- | --- | --- | --- |
| CS01 | Khiếu nại thẻ không nạp được | Ticket sự vụ | SLA xử lý ban đầu 10 phút. Quá 10 phút chưa có kết quả hoặc có dấu hiệu lỗi hàng loạt phải báo ngay quản lý. |
| CS02 | Khiếu nại topup lỗi (giao dịch báo thành công nhưng khách không nhận được tiền) | Ticket sự vụ | SLA xử lý 15 phút. Nếu xác định rõ lỗi hệ thống hoặc lỗi đối tác, ưu tiên phương án khắc phục cho khách trước, sau đó xử lý đối soát nguyên nhân. |
| CS03 | Theo dõi cổng 39 / hỗn hợp | Checklist định kỳ | Kiểm tra 10–20 phút/lần. Giao dịch treo >3 phút phải xử lý hoặc thông báo NCC; tỷ lệ thất bại >10% phải cảnh báo điều chỉnh cổng. |
| CS04 | Cảnh báo tồn kho cổng 70 / Vina | Checklist định kỳ | Kiểm tra 30–60 phút/lần. Tồn kho tiệm cận ngưỡng phải cảnh báo ngay; có nguy cơ hết hàng phải đề xuất đóng cổng. |
| CS05 | Khiếu nại nạp tiền tài khoản Octa | Ticket sự vụ | SLA 5–15 phút. Phải xác định được nguyên nhân hoặc ít nhất xác định đúng đầu mối chịu trách nhiệm trong thời gian cho phép. |
| CS06 | Kiểm tra giao dịch mua hàng | Checklist định kỳ | Kiểm tra định kỳ 10–30 phút/lần; thời gian xử lý 5–30 phút tùy trường hợp; giao dịch phải được chuyển trạng thái hoặc được mở sự vụ theo dõi. |
| CS07 | Kiểm tra công cụ, dụng cụ trước ca làm việc | Checklist đầu ca | Thực hiện đầu ca; thời gian kiểm tra tối đa 10 phút. |
| CS08 | Kiểm tra điều kiện bán hàng hệ thống và theo dõi nếu cần | Checklist đầu ca | Thực hiện đầu ca; hoàn thành trong 10 phút. Nếu phát hiện thiếu nguồn hàng hoặc tài khoản API dưới ngưỡng phải cảnh báo ngay. |
| CS09 | Kiểm tra công cụ bán hàng hệ thống (web/mini app) | Checklist đầu ca/cuối ca | Thực hiện trước khi vào ca và trước khi kết thúc ca. |
| CS10 | Theo dõi kênh phản ánh khách hàng | Checklist liên tục + Ticket | Bắt chuông và tiếp nhận ngay từ lần báo đầu tiên. Phản hồi đầu tiên quá 3 phút là vi phạm. |

**CS01 – Khi****ế****u ****n****ạ****i th****ẻ**** không n****ạ****p đư****ợ****c**

| **Lo****ạ****i c****ấ****u hình Odoo** | Ticket sự vụ |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Xác định đúng tình trạng thẻ, xử lý đúng phương án và chốt kết quả cho khách hàng trong thời gian cho phép; đồng thời nhận diện sớm lỗi do khách hàng, do Octa hoặc do nhà cung cấp. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Mã/serial thẻ; thông tin khách hàng; thời điểm mua/in; nguồn phản ánh; NCC; ảnh chụp thẻ/log liên quan. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Phải chốt một kết quả cuối rõ ràng: thẻ hợp lệ / hướng dẫn nạp lại thành công / hỗ trợ nạp hộ / đổi mã / hoàn tiền / chuyển bộ phận sản xuất / chuyển kỹ thuật / báo cáo cấp trên. SLA xử lý ban đầu 10 phút. Quá 10 phút chưa có kết quả hoặc có dấu hiệu lỗi hàng loạt phải báo ngay quản lý. KPI: Số ticket đúng hạn; tỷ lệ xử lý dứt điểm lần đầu; tỷ lệ khiếu nại lặp lại. |

**Quy trình th****ự****c hi****ệ****n**

**1. Ti****ế****p nh****ậ****n và m****ở**** s****ự**** v****ụ****: **Tiếp nhận phản ánh từ chat, email, điện thoại hoặc tài liệu đính kèm. Kiểm tra đủ thông tin tối thiểu trước khi xử lý; thiếu thông tin thì yêu cầu khách bổ sung ngay.

**2. Xác minh ngu****ồ****n th****ẻ****: **Kiểm tra thẻ có phải do Octa bán ra hay không; xác định nguồn thẻ thuộc kho Octa, thẻ Octa sản xuất/chuyển PIN hay thẻ do đối tác/NCC cấp.

**3. Ki****ể****m tra tr****ạ****ng thái v****ớ****i nhà m****ạ****ng: **Tra cứu trạng thái thẻ theo serial trên hệ thống liên quan hoặc gọi tổng đài nhà mạng để xác minh thẻ đã nạp hay chưa, thời điểm nạp, trạng thái hiện tại.

**4. X****ử**** lý theo t****ừ****ng trư****ờ****ng h****ợ****p: **Nếu thẻ đã được nạp sau thời điểm khách mua thì thông báo kết quả xác minh cho khách và đóng phản ánh. Nếu thẻ chưa được sử dụng và là thẻ Octa sản xuất/chuyển PIN thì kiểm tra ảnh thẻ khách gửi: ảnh đúng thì hướng dẫn khách nạp lại hoặc xin số để hỗ trợ nạp hộ; nếu sai mã do Octa thì xử lý theo phương án được duyệt: gửi mã đúng, cấp mã mới, hỗ trợ nạp hộ hoặc hoàn tiền. Nếu thẻ do NCC cung cấp thì lập khiếu nại với bên bán, theo dõi phản hồi và báo cấp trên nếu có dấu hiệu bất thường hoặc liên quan nhiều mã.

**5. C****ậ****p nh****ậ****t k****ế****t qu****ả**** và ch****ố****t vi****ệ****c: **Ghi đầy đủ nguyên nhân, hướng xử lý, bằng chứng xác minh và kết quả cuối trên ticket. Chỉ đóng ticket khi khách đã được phản hồi rõ hoặc đã chuyển đúng bộ phận chịu trách nhiệm kèm đủ thông tin.

**Lưu ý / đi****ể****m ki****ể****m soát**

Không kết luận lỗi hàng loạt nếu chưa có xác minh từ nhà mạng/NCC hoặc chưa có ít nhất 2–3 trường hợp tương tự.

Nếu nghi ngờ lỗi do Octa sản xuất hoặc lỗi hàng loạt từ cùng NCC, phải báo quản lý ngay trước khi xử lý đơn lẻ (nguy cơ hack rất cao).

**CS02 – Khi****ế****u n****ạ****i topup l****ỗ****i (giao d****ị****ch báo thành công nhưng khách không nh****ậ****n đư****ợ****c ti****ề****n)**

| **Lo****ạ****i c****ấ****u hình Odoo** | Ticket sự vụ |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Xác minh trạng thái giao dịch topup, xử lý đúng phương án cho khách hàng và khống chế ảnh hưởng trải nghiệm khách hàng. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Mã giao dịch; số điện thoại; nhà cung cấp/cổng; thời điểm phát sinh; ảnh/log nếu có. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Chốt một kết quả cuối: thành công / thất bại / hoàn tiền / nạp bù / chờ đối tác xác nhận. SLA xử lý 15 phút. Nếu xác định rõ lỗi hệ thống hoặc lỗi đối tác, ưu tiên phương án khắc phục cho khách trước, sau đó xử lý đối soát nguyên nhân. KPI: Tỷ lệ ticket topup đúng hạn; mức độ hài lòng của end user; tỷ lệ tái phát cùng nguyên nhân. |

**Quy trình th****ự****c hi****ệ****n**

**1. Ti****ế****p nh****ậ****n ph****ả****n ánh: **Nhận thông tin từ khách hàng hoặc đại lý; kiểm tra đủ mã giao dịch, số điện thoại, thời điểm và kênh phát sinh.

**2. Ki****ể****m tra ph****ạ****m vi gia****o d****ị****ch: **Tra cứu trên hệ thống để xác định giao dịch có thuộc Octa hay không. Nếu không thuộc hệ thống Octa thì phản hồi rõ cho khách và đóng ticket.

**3. Ki****ể****m tra tr****ạ****ng thái giao d****ị****ch trên portal: **Nếu giao dịch thất bại thì thông báo rõ cho khách rằng thuê bao không được cộng tiền và đóng phản ánh. Nếu giao dịch hiển thị thành công thì chuyển sang bước xác minh với đại lý/tổng đài/NCC.

**4. Xác minh bên ngoài: **Kiểm tra giao dịch thuộc đại lý nào; đồng thời liên hệ tổng đài/nhà cung cấp để xác nhận thuê bao đã nhận tiền hay chưa.

**5. X****ử**** lý theo k****ế****t qu****ả**** xác minh: **Nếu xác minh cho thấy thuê bao đã nhận tiền thì phản hồi lại cho khách và đóng ticket. Nếu hệ thống báo thành công nhưng bên nhận xác nhận chưa nhận tiền, phải báo quản lý, gửi thông tin cho NCC đối soát và thực hiện một trong hai phương án đã được phê duyệt: hoàn tiền hoặc nạp bù.

**6. Hoàn t****ấ****t và theo dõi sau x****ử**** lý: **Sau khi hoàn tiền hoặc nạp bù, kiểm tra lại kết quả thực tế, thông báo cho khách và cập nhật ticket đầy đủ bằng chứng, thời gian xử lý, nguyên nhân gốc nếu xác định được.

**Lưu ý / đi****ể****m ki****ể****m soát**

Các trường hợp hệ thống báo thành công nhưng khách chưa nhận tiền phải được triển khai xử lý ưu tiên, theo dõi đến khi có kết quả cuối, không dừng ở mức 'đã báo đối tác'.

Nếu phát sinh nhiều giao dịch tương tự trong cùng thời điểm/cùng NCC, phải báo quản lý ngay để xử lý theo hướng sự cố hệ thống.

**CS03 – Theo dõi c****ổ****ng 39 / h****ỗ****n h****ợ****p**

| **Lo****ạ****i c****ấ****u hình Odoo** | Checklist định kỳ |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Theo dõi lưu lượng, tỷ lệ lỗi và trạng thái giao dịch tại các cổng hỗn hợp để tối ưu doanh thu, giảm treo giao dịch và cảnh báo điều chỉnh cổng kịp thời. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Tên cổng; số giao dịch treo; tỷ lệ thất bại; lưu lượng chờ nạp; phân bổ mệnh giá; nguyên nhân sơ bộ nếu có. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Checklist phải chốt rõ: bình thường / đã cảnh báo / đã mở ticket / đã chuyển vận hành / đã chuyển kỹ thuật / đã yêu cầu NCC xử lý. Kiểm tra 10–20 phút/lần. Giao dịch treo >3 phút phải xử lý hoặc thông báo NCC; tỷ lệ thất bại >10% phải cảnh báo điều chỉnh cổng. KPI: Số sự cố phát hiện đúng thời điểm; số cảnh báo đúng; không để giao dịch treo kéo dài hoặc thất bại hàng loạt mà không có cảnh báo. |

**Quy trình th****ự****c hi****ệ****n**

**1. Đăng nh****ậ****p và m****ở**** màn hình theo dõi: **Đăng nhập Gate Hỗn Hợp, mở các cổng cần giám sát trong ca và xác nhận dữ liệu đang cập nhật bình thường.

**2. Ki****ể****m t****ra t****ỷ**** l****ệ**** th****ấ****t b****ạ****i: **Theo dõi tỷ lệ giao dịch thất bại của từng cổng. Nếu vượt ngưỡng 10%, lập cảnh báo và đề xuất điều chỉnh lưu lượng hoặc đóng/mở bớt giao dịch vào cổng.

**3. Ki****ể****m tra giao d****ị****ch treo: **Lọc các giao dịch treo quá 3 phút. Liên hệ NCC để xác minh trạng thái; nếu đã có kết quả từ đối tác thì cập nhật trạng thái giao dịch, tạo ticket thông kê và để xử lý dứt điểm.

**4. Ki****ể****m tra phân b****ổ**** m****ệ****nh giá: **Đối chiếu lượng giao dịch theo từng mệnh giá 20/50/100/200/500. Nếu thiếu mệnh giá do phân luồng sai thì báo Vận hành; nếu do nguyên nhân khác thì báo Kỹ thuật kiểm tra.

**5. Ki****ể****m tra lưu lư****ợ****ng giao d****ị****ch ch****ờ**** nạp****: **Nếu lượng giao dịch chờ nạp quá thấp hoặc bất thường (ví dụ tỷ lệ thất bại rất thấp nhưng lưu lượng vào cổng không đủ) thì xác minh nguyên nhân: do nguồn mua hàng thấp, do chưa mở đủ giao dịch vào cổng hay do lỗi hệ thống; sau đó báo đúng đầu mối xử lý.

**6. Ghi nh****ậ****n và t****ạ****o s****ự**** v****ụ**** khi c****ầ****n: **Kết thúc mỗi lần kiểm tra phải ghi nhận tình trạng cổng. Nếu có giao dịch treo, thất bại bất thường hoặc luồng cổng cần điều chỉnh thì tạo ticket/sự vụ ngay trên hệ thống.

**Lưu ý / đi****ể****m ki****ể****m soát**

Checklist này không chỉ là 'xem cổng'; mục tiêu là phát hiện sớm để bảo vệ doanh thu và hạn chế treo giao dịch.

Mọi điều chỉnh cổng phải có dấu vết: đã cảnh báo ai, lúc nào, và kết quả sau cảnh báo.

**CS04 – C****ả****nh báo t****ồ****n kho c****ổ****ng 70 / Vina**

| **Lo****ạ****i c****ấ****u hình Odoo** | Checklist định kỳ |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Bảo đảm cổng 70/Vina luôn có đủ tồn kho phục vụ bán hàng; cảnh báo sớm trước khi cạn kho hoặc cần đóng cổng. |
| **Đ****ầ****u vào t****ố****i ****thi****ể****u** | Loại thẻ; số lượng tồn; ngưỡng tối thiểu; thời điểm kiểm tra. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Chốt rõ một trong các trạng thái: tồn bình thường / đã cảnh báo tiệm cận ngưỡng / đã yêu cầu chuyển cổng / đã cảnh báo đóng cổng. Kiểm tra 30–60 phút/lần. Tồn kho tiệm cận ngưỡng phải cảnh báo ngay; có nguy cơ hết hàng phải đề xuất đóng cổng. KPI: Số lần thiếu kho được xử lý trước; không để hết hàng mà không có cảnh báo. |

**Quy trình th****ự****c hi****ệ****n**

**1. Truy c****ậ****p kho th****ẻ****: **Đăng nhập Gate Topup thẻ, vào kho thẻ, chọn NCC Vina và lọc dữ liệu để hiển thị tồn kho hiện tại.

**2. So sánh v****ớ****i ngư****ỡ****ng v****ậ****n hành: **Đối chiếu tồn kho thực tế với ngưỡng tối thiểu do Vận hành quy định cho cổng 70.

**3. Phân lo****ạ****i m****ứ****c c****ả****nh báo: **Nếu tồn kho vẫn đủ an toàn thì ghi nhận bình thường. Nếu tồn kho tiệm cận ngưỡng thì cảnh báo người quản lý cổng/vận hành để chuẩn bị điều chỉnh. Nếu tồn kho có nguy cơ hết trước kỳ tiếp theo thì cảnh báo chuyển cổng hoặc đề xuất đóng cổng.

**4. Ghi nh****ậ****n k****ế****t qu****ả****: **Mở checklist hoặc cập nhật checklist đã có, ghi rõ số tồn, thời điểm, người đã nhận cảnh báo và hướng xử lý đã đề xuất.

**5. Theo dõi sau c****ả****nh báo: **Nếu đã phát cảnh báo, phải theo dõi lại trong kỳ kế tiếp để xác nhận cổng đã được điều chỉnh hoặc hàng đã được bổ sung.

**Lưu ý / đi****ể****m ki****ể****m soát**

Đây là việc phòng ngừa. Không chờ 'hết kho' mới báo.

Khi tồn kho xuống nhanh bất thường, nên đồng thời kiểm tra nguyên nhân từ sản lượng bán hoặc tốc độ đẩy cổng.

**CS05 – Khi****ế****u n****ạ****i n****ạ****p ti****ề****n tài kho****ả****n Octa**

| **Lo****ạ****i c****ấ****u hình Odoo** | Ticket sự vụ |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Xử lý kịp thời các trường hợp nạp tiền vào tài khoản Octa nhưng chưa được hệ thống ghi nhận, bảo đảm số dư khách hàng được cập nhật đúng và đúng thời gian. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Mã đại lý; mã giao dịch (nếu có); phương thức nạp; số tiền; ngân hàng chuyển; ảnh/chứng từ chuyển khoản. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Phải chốt trạng thái cuối: hệ thống đã tự động cộng tiền / chuyển Kế toán xử lý và đã hoàn tất / xác định sai thông tin nạp / khách hàng đã được phản hồi đầy đủ. SLA 5–15 phút. Phải xác định được nguyên nhân hoặc ít nhất xác định đúng đầu mối chịu trách nhiệm trong thời gian cho phép. KPI: Tỷ lệ xử lý đúng hạn; tỷ lệ phản ánh lặp lại cùng mã khách hàng; mức độ hài lòng của khách hàng. |

**Quy trình th****ự****c hi****ệ****n**

**1. Ti****ế****p nh****ậ****n ho****ặ****c phát hi****ệ****n ch****ủ**** đ****ộ****ng: **Tiếp nhận phản ánh từ chat, Tawk.to, tổng đài hoặc chủ động phát hiện giao dịch nạp tiền treo/chưa duyệt trên hệ thống.

**2. Thu th****ậ****p thông tin chu****ẩ****n: **Yêu cầu khách hàng chủ động cung cấp đúng thông tin: mã đại lý, số tiền nạp, ngân hàng chuyển, thời gian chuyển, ảnh/chứng từ giao dịch. Không cung cấp ngược thông tin hệ thống cho khách để khách xác nhận.

**3. Tra c****ứ****u trên portal: **Vào Portal > Đại lý > Quản lý nạp tiền, tra cứu theo mã đại lý và thời điểm giao dịch để xác định hệ thống đã cộng tiền hay chưa.

**4. X****ử**** lý theo k****ế****t qu****ả****: **Nếu hệ thống đã tự động cộng tiền thì thông báo lại cho khách và cập nhật ticket. Nếu hệ thống chưa cộng tiền thì chuyển đầy đủ thông tin cho Kế toán để kiểm tra, theo sát tiến độ xử lý và cập nhật lại khi tiền đã được cộng.

**5. Ki****ể****m tra hoàn t****ấ****t: **Sau khi tiền được cập nhật, kiểm tra lại số dư tài khoản thực tế, thông báo cho khách hàng và đóng ticket với kết quả cuối.

**Lưu ý / đi****ể****m ki****ể****m soát**

Nhân viên CSKH không tự ý hứa thời gian xử lý nếu chưa xác nhận với Kế toán hoặc quản lý.

Mọi ticket phải có chứng từ hoặc xác nhận tối thiểu để tránh xử lý sai tài khoản.

**CS06 – Ki****ể****m tra giao d****ị****ch mua hàng**

| **Lo****ạ****i c****ấ****u hình Odoo** | Checklist định kỳ |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Phát hiện kịp thời giao dịch mua hàng bị treo hoặc thất bại, xác định nguyên nhân và chuyển trạng thái giao dịch về kết quả cuối trong thời gian cho phép. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Mã giao dịch; nhà cung cấp; loại giao dịch (mua mã thẻ/topup); trạng thái hiện tại; thời gian trễ; nguyên nhân sơ bộ. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Mỗi giao dịch hoặc nhóm giao dịch phải chốt một kết quả rõ ràng: thành công / thất bại / chuyển kỹ thuật / báo NCC / báo hết hàng / tiếp tục theo dõi có kiểm soát. Kiểm tra định kỳ 10–30 phút/lần; thời gian xử lý 5–30 phút tùy trường hợp; giao dịch phải được chuyển trạng thái hoặc được mở sự vụ theo dõi. KPI: Tỷ lệ xử lý đúng hạn; tỷ lệ giao dịch chuyển được trạng thái; xu hướng giảm sự vụ lặp lại. |

**Quy trình th****ự****c hi****ệ****n**

**1. Ki****ể****m tra đ****ầ****u ca: **Đăng nhập Portal > Báo cáo > Lịch sử giao dịch; lọc từ cuối ca trước đến thời điểm hiện tại. Phân loại nhóm giao dịch đang xử lý quá 10 giây và nhóm giao dịch thất bại.

**2. Ki****ể****m tra đ****ị****nh k****ỳ**** trong ca: **Lặp lại thao tác kiểm tra 10–30 phút/lần; mỗi lần kiểm tra lọc từ thời điểm lần trước để không bỏ sót giao dịch mới phát sinh.

**3. X****ử**** lý**** giao d****ị****ch mua mã th****ẻ**** – tr****ạ****ng thái đang x****ử**** lý: **Nếu mua tại kho Octa thì kiểm tra kho: nếu kho còn hàng mà giao dịch vẫn treo, báo Kỹ thuật; nếu kho hết, mở phiếu báo cáo sự cố hết hàng. Nếu mua qua API thì mở phiếu báo cáo và liên hệ đối tác xử lý giao dịch treo.

**4. X****ử**** lý giao d****ị****ch mua mã th****ẻ**** – tr****ạ****ng thái th****ấ****t b****ạ****i: **Nếu mua tại kho thì kiểm tra tồn kho, báo Kỹ thuật khi cần và ghi nhận sự vụ. Nếu mua qua API thì liên hệ đối tác để đối soát/khắc phục, đồng thời mở ticket ghi nhận.

**5. X****ử**** lý giao d****ị****ch topup: **Với giao dịch topup đang xử lý: liên hệ đối tác/NCC để xử lý dứt điểm; riêng cổng 70 cần đồng thời liên hệ đối tác dịch vụ và Kỹ thuật nếu có dấu hiệu lỗi hệ thống. Với giao dịch topup thất bại do đại lý, NCC hoặc hệ thống thì mở phiếu báo cáo, ghi nhận nguyên nhân và thống kê.

**6. Ghi nh****ậ****n và theo dõi k****ế****t thúc: **Mọi giao dịch vượt ngưỡng hoặc thất bại đều phải có bản ghi/checklist/ticket, trong đó lưu đủ thông tin phát sinh, hướng xử lý và kết quả cuối.

**Lưu ý / đi****ể****m ki****ể****m soát**

Công việc này là theo dõi giao dịch vận hành, không chỉ xem báo cáo. Bất kỳ giao dịch treo nào cũng phải dẫn đến hành động cụ thể.

Khi xuất hiện nhiều giao dịch cùng lỗi trong một khoảng thời gian ngắn, phải xử lý theo hướng sự cố hệ thống thay vì từng giao dịch đơn lẻ.

**CS07 – Ki****ể****m tra công c****ụ****, d****ụ****ng c****ụ**** trư****ớ****c ca làm vi****ệ****c**

| **Lo****ạ****i c****ấ****u hình Odoo** | Checklist đầu ca |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Bảo đảm tất cả công cụ phục vụ CSKH hoạt động bình thường trước khi nhận ca, tránh phát sinh lỗi công cụ trong quá trình phục vụ khách hàng. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Danh sách công cụ phải kiểm tra; tình trạng từng công cụ; biên bản bàn giao ca trước. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Chốt rõ một trong các trạng thái: hoạt động bình thường / phát hiện lỗi và đã báo / chuyển kỹ thuật / cần theo dõi trong ca. Thực hiện đầu ca; thời gian kiểm tra tối đa 10 phút. KPI: Tỷ lệ check đúng đầu ca; không có phản ánh trong ca do lỗi công cụ đã tồn tại từ trước mà không được phát hiện. |

**Quy trình th****ự****c hi****ệ****n**

**1. Ki****ể****m tra t****ổ****ng đài: **Đăng nhập, thực hiện gọi thử hoặc nhận thử để xác nhận có thể nghe/gọi bình thường.

**2. Ki****ể****m tra kênh c****ả****nh báo n****ộ****i b****ộ****: **Vào Slack hoặc kênh cảnh báo tương đương, kiểm tra các cảnh báo gần nhất 12–24 giờ để chắc chắn hệ thống cảnh báo đang hoạt động.

**3. Ki****ể****m tra Telegram và các nhóm làm ****vi****ệ****c: **Đăng nhập, rà soát tin nhắn, nhắn thử khi cần và xác nhận các nhóm chính vẫn hoạt động bình thường.

**4. Ki****ể****m tra Zalo OA, Tawk.to và email CSKH: **Đăng nhập từng công cụ, kiểm tra trạng thái online, tin nhắn/thư mới và thực hiện test nhanh nếu cần để xác nhận công cụ nhận/gửi bình thường.

**5. Ki****ể****m tra biên b****ả****n bàn giao ca trư****ớ****c: **Đọc kỹ nội dung bàn giao, xác định các tồn đọng phải theo dõi trong ca mới.

**6. Xác nh****ậ****n nh****ậ****n ca: **Chỉ xác nhận hoàn tất checklist đầu ca khi toàn bộ công cụ hoạt động bình thường hoặc các lỗi đã được báo đúng đầu mối và có ghi nhận rõ.

**Lưu ý / đi****ể****m ki****ể****m soát**

Nếu công cụ lỗi nhưng vẫn có phương án dự phòng, phải ghi chú rõ để ca trực không bị gián đoạn.

Không nhận ca khi chưa đọc xong bàn giao và chưa biết các sự vụ tồn đọng.

**CS08 – Ki****ể****m tra đi****ề****u ki****ệ****n bán hàng h****ệ**** th****ố****ng và theo dõi n****ế****u c****ầ****n**

| **Lo****ạ****i c****ấ****u hình Odoo** | Checklist đầu ca |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Xác định tình trạng đủ điều kiện bán hàng của hệ thống: tồn kho mã thẻ, tồn tài khoản API và các nguồn mua hàng chính, từ đó cảnh báo kịp thời trước khi ảnh hưởng bán hàng. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Danh sách kho và API phải kiểm tra; số tồn; mức ngưỡng theo dõi; ảnh/log nếu có. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Chốt rõ: điều kiện bán hàng bình thường / đã mở phiếu cảnh báo / đã thông báo chuyển cổng / đã cảnh báo kinh doanh/NCC. Thực hiện đầu ca; hoàn thành trong 10 phút. Nếu phát hiện thiếu nguồn hàng hoặc tài khoản API dưới ngưỡng phải cảnh báo ngay. KPI: Không để xảy ra tình trạng hết hàng trong kho hoặc hết tài khoản API trong ca và ca kế tiếp mà không có cảnh báo. |

**Quy trình th****ự****c hi****ệ****n**

**1. Ki****ể****m tra t****ổ****ng th****ể**** h****ệ**** th****ố****ng vi****ễ****n thông: **Đăng nhập Portal, kiểm tra nhanh tất cả dịch vụ; xác nhận trong 8 giờ gần nhất không có giao dịch thất bại do hết hàng hoặc hết tài khoản mà chưa được xử lý.

**2. K****i****ể****m tra kho mã th****ẻ****: **Vào Gate mã thẻ/kho thẻ, chọn từng NCC trọng yếu và kiểm tra số lượng tồn so với ngưỡng vận hành.

**3. Ki****ể****m tra tài kho****ả****n API bên bán: **Vào Portal > Đối tác > Tài khoản đối tác, kiểm tra số dư và trạng thái từng tài khoản API quan trọng.

**4****. Ki****ể****m tra các ngu****ồ****n đ****ặ****c thù: **Kiểm tra API vé máy bay bảo đảm số dư tối thiểu theo quy định; kiểm tra tài khoản BigM bảo đảm đủ cho 10 ngày bán; kiểm tra tài khoản Link ID hoặc nguồn mua đặc thù khác bảo đảm đủ cho 7 ngày bán.

**5. Ghi nh****ậ****n và m****ở**** phi****ế****u n****ế****u c****ầ****n: **Ghi rõ các kho/API đã kiểm tra; nếu nguồn hàng hoặc tài khoản xuống dưới ngưỡng thì tạo phiếu cảnh báo và thông báo cho chuyên viên chuyển cổng, Kinh doanh hoặc đối tác theo đúng đầu mối.

**6. Theo dõi sau c****ả****nh báo: **Nếu đã mở phiếu, cần quay lại kiểm tra sau khi có thông tin bổ sung/điều chỉnh để xác nhận điều kiện bán hàng đã an toàn.

**Lưu ý / đi****ể****m ki****ể****m soát**

Mục tiêu của checklist này là bảo vệ điều kiện bán hàng đầu ca, không chờ đến khi giao dịch lỗi mới kiểm tra nguồn hàng.

Nên ưu tiên cảnh báo các nguồn có ảnh hưởng doanh thu lớn trước.

**CS09 – Ki****ể****m tra công c****ụ**** bán hàng h****ệ**** th****ố****ng (web/mini app)**

| **Lo****ạ****i c****ấ****u hình Odoo** | Checklist đầu ca/cuối ca |
| --- | --- |
| **M****ụ****c tiêu công vi****ệ****c** | Bảo đảm các web bán hàng và mini app chính của Octa hoạt động bình thường, đăng nhập được và không có lỗi bề mặt ảnh hưởng khách hàng. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Danh sách web/app phải kiểm tra; tình trạng đăng nhập; lỗi phát sinh; ảnh chụp/log sự cố nếu có. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Chốt rõ: bình thường / có lỗi / đã báo kỹ thuật / cần theo dõi tiếp. Thực hiện trước khi vào ca và trước khi kết thúc ca. KPI: Tỷ lệ check đầu ca/cuối ca đúng quy định; không có sự cố rõ ràng trên web/app bị bỏ sót trong ca. |

**Quy trình th****ự****c hi****ệ****n**

**1. Ki****ể****m tra web đ****ạ****i lý vi****ễ****n thông: **Truy cập bigtel.vn, đăng nhập và xác nhận các thao tác cơ bản hoạt động bình thường.

**2. Ki****ể****m tra website vé máy bay: **Truy cập vemaybaybigm.vn, đăng nhập và xác nhận website hoạt động bình thường.

**3. Ki****ể****m tra các mini app/Zalo app BigM: **Lần lượt mở các app BigM Shop, BigM Vé Máy Bay Giá Rẻ, BigM Quản trị bán hàng, BigM nạp tiền điện thoại, BigM nạp tài khoản game; kiểm tra khả năng truy cập, đăng nhập và hiển thị cơ bản.

**4. Ghi nh****ậ****n l****ỗ****i n****ế****u có: **Nếu phát hiện lỗi đăng nhập, lỗi hiển thị, lỗi không thao tác được hoặc lỗi ảnh hưởng bán hàng, chụp màn hình và báo Kỹ thuật ngay.

**5. Ch****ố****t checklist: **Hoàn tất checklist khi toàn bộ công cụ đã kiểm tra đủ hoặc các lỗi đã được ghi nhận và chuyển đúng đầu mối xử lý.

**Lưu ý / đi****ể****m ki****ể****m soát**

Checklist này tập trung vào khả năng hoạt động bề mặt của kênh bán hàng, không thay thế kiểm thử sâu của Kỹ thuật.

Các lỗi ảnh hưởng trực tiếp tới đăng nhập/bán hàng phải được ưu tiên báo ngay.

**CS10 – Theo dõi kênh ph****ả****n ánh khách hàng**

| **Lo****ạ****i c****ấ****u hình Odoo** | Checklist liên tục + Ticket |
| --- | --- |
| **M****ụ****c tiêu ****công vi****ệ****c** | Đảm bảo mọi phản ánh của khách hàng trên tất cả các kênh đều được tiếp nhận, phản hồi đầu tiên nhanh và được xử lý/điều phối đúng quy trình. |
| **Đ****ầ****u vào t****ố****i thi****ể****u** | Kênh tiếp nhận; nội dung phản ánh; thời điểm nhận; mức ưu tiên; ca trực; nhân viên phụ trách. |
| **K****ế****t qu****ả**** c****ầ****n đ****ạ****t / SLA / KPI** | Phải bảo đảm phản hồi đầu tiên trong 3 phút; nếu là sự vụ thì phải mở ticket và theo dõi đến khi có kết quả cuối hoặc được bàn giao đủ cho ca sau. Bắt chuông và tiếp nhận ngay từ lần báo đầu tiên. Phản hồi đầu tiên quá 3 phút là vi phạm. KPI: Thời gian phản hồi đầu tiên; số phản ánh bị trôi; số việc phải bàn giao sang ca sau; mức độ hài lòng khách hàng. |

**Quy trình th****ự****c hi****ệ****n**

**1. Theo dõi liên t****ụ****c các kênh: **Bật chuông/thông báo trên tổng đài, chat, email, Tawk.to, Zalo OA, Telegram và các kênh phản ánh khác. Mục tiêu là không bỏ lỡ phản ánh từ lần thông báo đầu tiên.

**2. Ti****ế****p nh****ậ****n và ghi nh****ậ****n thông tin: **Khi có phản ánh mới, ghi nhận ngay tối thiểu: kênh tiếp nhận, nội dung, thời điểm, nhân viên/ca trực, mức độ ưu tiên và trạng thái hiện tại.

**3. Ph****ả****n h****ồ****i đ****ầ****u tiên cho khách: **Trong vòng tối đa 3 phút, phải có phản hồi đầu tiên để khách biết Octa đã tiếp nhận thông tin, dù chưa có kết quả cuối.

**4. Phân lo****ạ****i ph****ả****n ánh: **Nếu là phản ánh đơn giản có thể giải đáp ngay thì xử lý trực tiếp. Nếu là sự vụ thuộc một quy trình khác (thẻ lỗi, topup lỗi, nạp tiền, v.v.) thì mở ticket đúng mã việc tương ứng và tiếp tục xử lý theo quy trình đó.

**5. Theo dõi đ****ế****n khi hoàn t****ấ****t: **Theo dõi tiến độ xử lý trong suốt ca trực. Nếu chưa thể hoàn tất do nguyên nhân khách quan, phải cập nhật trạng thái, nêu rõ việc đã làm và bàn giao đủ cho ca sau.

**6. Đánh giá sau ca: **Cuối ca hoặc theo yêu cầu quản lý, thống kê thời gian phản hồi đầu tiên, số phản ánh bị trôi, số việc quá thời gian và các phản ánh chưa được xử lý từ ca trước.

**Lưu ý / đi****ể****m ki****ể****m soát**

Phản hồi đầu tiên không phải là giải quyết xong, nhưng bắt buộc phải cho khách biết thông tin đã được tiếp nhận.

Không để phản ánh bị 'trôi' giữa các ca; nếu bàn giao phải bàn giao bằng bản ghi có trạng thái rõ ràng.

**NGUYÊN T****Ắ****C QU****Ả****N LÝ CHUNG KHI ÁP D****Ụ****NG**

Mọi sự vụ phải có kết quả cuối rõ ràng; không chấp nhận trạng thái 'đã xử lý' nhưng không mô tả xử lý xong như thế nào.

Các checklist đầu ca/định kỳ nếu phát hiện bất thường phải tạo sự vụ ngay, không chỉ ghi nhận rồi để đó.

Nếu vượt SLA mà chưa có kết quả cuối, nhân viên phải chủ động báo quản lý và cập nhật lý do kéo dài trên hệ thống.

Những trường hợp có nguy cơ ảnh hưởng doanh thu diện rộng, lỗi hàng loạt, lỗi nhiều giao dịch cùng nguyên nhân hoặc lỗi lặp lại nhiều lần phải escalte ngay.

Tài liệu ban hành dùng nội bộ Octa.

CEO / Người phê duyệt