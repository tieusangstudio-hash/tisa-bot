# Cấu trúc trang bán hàng, trang lead và checklist hỏi chủ (nghiên cứu cho "Quản Trị WEB")

Ngày: 19/11/2026. Nguồn: https://connectivewebdesign.com/blog/storybrand-framework (StoryBrand, bên thứ ba); https://storybrand.com/building-a-storybrand-book/ (trang sách, không liệt kê 7 phần); https://dansilvestre.com/?p=4025 (tóm tắt DotCom Secrets của Brunson); kết quả tìm kiếm về squeeze page, value ladder, Perfect Webinar (thrivethemes.com, supplygem.com, marketingprofs.com); các bản tóm tắt $100M Offers (supersummary.com, readingraphics.com...); các bản tóm tắt 5 mức nhận thức của Schwartz (selzee.com, shortform.com, optimizesmart.com); các bản tóm tắt Halbert (Boron Letters, michelfortin.com); https://amis.misa.vn/35769/cau-truc-landing-page/ (cấu trúc landing tiếng Việt); https://datareportal.com/reports/digital-2026-vietnam; https://vneconomy.vn/nhung-diem-moi-trong-luat-bao-ve-du-lieu-ca-nhan-tu-112026.htm; https://web.dev/articles/vitals; https://web.dev/articles/inp; https://web.dev/articles/optimize-lcp; https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events/; https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/customer-information-parameters; https://developers.facebook.com/docs/meta-pixel/reference; https://developers.google.com/analytics/devguides/collection/ga4/reference/events; https://ads.tiktok.com/help/article/event-deduplication; https://developers.cloudflare.com/workers/static-assets/; https://developers.cloudflare.com/zaraz/; https://developers.google.com/search/docs/appearance/snippet; https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials; repo README trong tệp 01.

Lưu ý nguồn: sách gốc (Brunson, Hormozi, Schwartz, Halbert, Miller) tôi không đọc trực tiếp, chỉ đọc bản tóm tắt bên thứ ba, nên các ý gắn nhãn "(tóm tắt)" là gián tiếp. Về Phạm Thành Long: tìm kiếm không ra tài liệu công khai nào về cấu trúc trang bán hàng của ông, nên không ghi gì thay ông. Phần tiếng Việt dùng bài của MISA AMIS. Ví dụ câu chữ bên dưới do tôi tự soạn, chỗ có [ngoặc vuông] là chỗ phải thay bằng thông tin thật của chủ.

## 1. Các khung, tóm tắt bằng lời mình

| Khung | Ý chính dùng cho trang | Ghi chú nguồn |
|---|---|---|
| PAS (Vấn đề, Khuấy động, Giải pháp) | Nêu nỗi đau cụ thể, làm khách thấy hậu quả nếu để nguyên, rồi mới đưa giải pháp | Gắn với Dan Kennedy (README rymac-skills); AIDA, PASTOR cũng được nhắc trong README copy-thief |
| AIDA | Chú ý, Quan tâm, Mong muốn, Hành động: trật tự đọc của một trang | Quen thuộc, dùng làm khung kiểm tra nhanh |
| StoryBrand (Donald Miller) | Khách là nhân vật chính, thương hiệu là người dẫn đường. Trang gồm: hero rõ trong vài giây, vấn đề và hậu quả nếu không hành động, bằng chứng người dẫn đường, kế hoạch 3 bước, lời kêu gọi trực tiếp (mua, gọi) và lời kêu gọi chuyển tiếp (tải tài liệu) cho người chưa sẵn sàng | (tóm tắt) Connective Web Design liệt kê 8 khối; nguồn khác nói 9-10 khối, không thống nhất |
| Brunson: Value Ladder, squeeze page, Star-Story-Solution | Xây thang giá trị từ rẻ đến đắt; trang thu lead có một mục tiêu, không gì gây xao nhãng; tiêu đề mở bằng sản phẩm, mong muốn hoặc vấn đề tùy khách đã biết đến đâu; kịch bản bán: Nhân vật, Câu chuyện, Giải pháp kèm quà, giá, bảo đảm, nút | (tóm tắt) Perfect Webinar (mở đầu, nội dung, chốt) là dạng webinar, không phải trang |
| Hormozi: Value Equation, Grand Slam Offer | Giá trị tăng khi tăng kết quả mơ ước và độ tin chắc đạt được; giảm thời gian chờ và công sức khách bỏ ra. Gói quà tặng, bảo đảm, tên gói nêu kết quả. Khan hiếm là số lượng, cấp bách là thời gian; cả hai phải thật | (tóm tắt) tóm tắt nói công thức không phải toán chặt; chưa đối chiếu sách |
| Halbert, Kennedy: tiêu đề, P.S. | Tiêu đề quyết định có đọc tiếp không; P.S. cuối thư nhắc lại lợi ích, giá, hạn | Một tóm tắt Boron Letters nói tiêu đề được đọc nhiều hơn thân bài khoảng 5 lần (cần xác minh). Tuyên bố "P.S. là phần được đọc nhiều thứ hai" lưu hành nhưng không tìm thấy nguồn gốc (cần xác minh) |
| Schwartz: 5 mức nhận thức | Chưa biết có vấn đề; biết vấn đề; biết có loại giải pháp; biết sản phẩm; sẵn sàng mua chỉ cần biết ưu đãi. Khách càng biết nhiều, trang càng ngắn | (tóm tắt) xem mục 2b để gắn với kênh kéo khách |

Cách dùng khi dựng: chẩn đoán mức nhận thức của khách trước, rồi chọn độ dài và cách mở trang (mục 2b).

## 2a. Các khối của một trang bán hàng, theo thứ tự

Ví dụ: dịch vụ [dọn dẹp nhà sau xây] và khóa học [quay video bằng điện thoại]. Không có con số trong ví dụ là số thật.

| # | Khối | Mục đích | Ví dụ câu chữ | Lỗi thường gặp |
|---|---|---|---|---|
| 1 | Thanh đầu (logo, nút gọi/Zalo) | Cho khách biết đây là ai, có đường liên hệ ngay; bỏ menu dài trên trang bán | "[Tên thương hiệu] | Gọi 09xx xxx xxx" | Menu 7 mục kéo khách đi chỗ khác (AMIS và GetResponse khuyên bỏ điều hướng trên trang bán) |
| 2 | Hero: tiêu đề, dòng phụ, nút, hình thật | Trong vài giây khách hiểu: bán gì, cho ai, lợi gì, bấm đâu | "Dọn xong nhà mới trong 1 ngày, bàn giao sạch để dọn vào ở" / "Dành cho chủ nhà sắp nhận nhà. Báo giá qua Zalo trong 15 phút." / [Nhận báo giá qua Zalo] | Tiêu đề kể về mình ("Công ty uy tín số 1"), ảnh minh họa chung chung, hai nút cạnh tranh nhau |
| 3 | Chứng cứ nhanh dưới hero | Một dòng tin cậy ngay: số khách thật, đánh giá, báo chí, giấy phép | "[Số thật] căn đã bàn giao. Xem ảnh trước-sau." | Con số bịa, logo của nơi chưa từng làm việc cùng |
| 4 | Vấn đề (P) | Gọi đúng nỗi đau bằng lời khách tự nói | "Nhận nhà xong, bụi xi măng còn dày, thợ dọn hẹn rồi lại hủy." | Nỗi đau chung chung; liệt kê tính năng thay vì nỗi đau |
| 5 | Hậu quả nếu để nguyên (A, Stakes) | Cho khách thấy cái giá của việc chờ, không dọa | "Mỗi tuần trễ là thêm tiền thuê trọ và lùi ngày dọn vào." | Dọa quá lố; dùng nỗi sợ sai sự thật |
| 6 | Giải pháp và cơ chế riêng (S, Guide) | Thương hiệu là người dẫn đường, nói vì sao cách này hiệu quả | "Đội 4 người, quy trình 3 lớp, có biên bản bàn giao." | Giới thiệu công ty dài thay vì cách giải quyết |
| 7 | Lợi ích, kết quả | Đổi tính năng thành kết quả khách nhận (AMIS gọi đây là phần quan trọng nhất) | "Dọn vào ở ngay, không phải lau lại." | Chỉ nêu tính năng ("máy hút bụi công nghiệp") |
| 8 | Quy trình 3 bước (Plan) | Giảm cảm giác khó và mơ hồ | "1. Gửi ảnh qua Zalo. 2. Nhận báo giá. 3. Hẹn ngày, bàn giao." | Quá nhiều bước, bước đầu đòi quá nhiều |
| 9 | Ưu đãi và gói giá trị | Liệt kê khách nhận gì, quà tặng đi kèm, giá trị từng phần | "Gói gồm: dọn sàn, kính, bếp; tặng [quà thật]." | Quà không liên quan; "giá trị 5 triệu" tự bịa |
| 10 | Bằng chứng xã hội chi tiết | Lời kể và ảnh/video thật của khách có tên, có bối cảnh | "Chị [Tên], [quận]: [lời kể thật]." + ảnh trước-sau | Lời chứng thực viết hộ, ảnh kho; xem mục 2c |
| 11 | Bảo đảm | Hạ rủi ro: hoàn tiền, làm lại, hủy trước giờ hẹn | "Chưa hài lòng, chúng tôi dọn lại miễn phí trong 48 giờ." | Bảo đảm mơ hồ hoặc khó đòi, rồi thực tế không giữ |
| 12 | Giá, khan hiếm trung thực, so sánh | Nêu giá rõ, lý do giá, hạn thật nếu có | "Từ [giá thật]/căn. Còn [số thật] lịch trong tháng này." | Đồng hồ đếm ngược giả tự reset; "chỉ còn 3 suất" bịa |
| 13 | Hỏi đáp (xử lý phản đối) | Trả lời các nỗi ngại: giá, uy tín, thời gian, thanh toán | "Có thể chuyển khoản sau khi nghiệm thu không?" | Câu hỏi tự bịa ra để quảng cáo |
| 14 | CTA cuối, P.S., chân trang | Nhắc lại lợi ích và hành động; thông tin pháp lý, chính sách, liên hệ | "P.S. Hạn ưu đãi đến [ngày thật]. Nhắn Zalo [số] ngay hôm nay." | Quên chân trang pháp lý và chính sách dữ liệu |

Quy tắc xuyên suốt: một mục tiêu duy nhất cho cả trang (một loại nút chính, lặp 3-5 lần); mỗi cuộn màn hình có một ý; kiểm lại bằng khung mức nhận thức.

## 2b. Landing lead và sales page dài

| Tiêu chí | Landing lead (thu SĐT/Zalo) | Sales page dài (bán thẳng) |
|---|---|---|
| Mục tiêu | Lấy tên và SĐT, rồi tư vấn tiếp | Khách ra quyết định mua ngay trên trang |
| Phù hợp | Dịch vụ cần báo giá, bất động sản, khóa học giá cao, traffic từ quảng cáo | Sản phẩm giá thấp-vừa, khách đã quen, có sẵn thanh toán |
| Độ dài | Ngắn: 1-3 màn hình (hero, 3 lợi ích, bằng chứng, form) | Dài: đủ 14 khối ở mục 2a |
| Điều hướng | Không | Không hoặc tối giản |
| Hành động | Điền form, bấm gọi, Zalo | Chọn gói, thanh toán (COD, chuyển khoản QR) |
| Mức nhận thức hợp | Biết vấn đề, hoặc đã nghe tên (retarget) | Chưa biết hoặc biết vấn đề thì cần dài |
| Thang giá trị Brunson | Mồi: quà miễn phí, báo giá miễn phí | Bậc kế tiếp: sản phẩm chính |

Gợi ý chọn: traffic lạnh từ Facebook/TikTok vào dịch vụ cần tư vấn thì làm lead ngắn, kèm quà hoặc báo giá; muốn bán trực tiếp sản phẩm lạ thì cần dài. Nên khớp thông điệp quảng cáo với tiêu đề trang (rymac-skills và copy-thief đều nhấn). Chỉ đưa nhiều mục tiêu khi có lý do: mỗi nút thêm là một lối thoát.

## 2c. Form lead, nút nổi, bằng chứng, bảo đảm, khan hiếm

Form tối ưu (tổng hợp thực hành; chỉ phần nhãn là có nguồn):
- Tối đa 2-3 ô: tên gọi, SĐT/Zalo, và tùy chọn "nhu cầu" (danh sách chọn). Chỉ hỏi email khi có tài liệu gửi qua email.
- Nhãn đặt trên ô nhập, không dùng chữ mờ thay nhãn (NN/g, qua tóm tắt: placeholder thay nhãn làm tăng lỗi và thời gian điền).
- Ô SĐT: bàn phím số (type tel), tự nhận 0xxx và +84, báo lỗi bằng tiếng Việt cụ thể.
- Nút ghi rõ việc sắp xảy ra ("Nhận báo giá qua Zalo"), không ghi "Gửi".
- Ô đồng ý xử lý dữ liệu, mặc định chưa tích, kèm mục đích và liên kết chính sách (xem mục 2d).
- Chặn gửi trùng, chặn spam bằng ô ẩn thay vì bắt giải mã; có thông báo thành công và chuyển tới trang cảm ơn.

Nút nổi gọi/Zalo/Messenger: luôn thấy trên điện thoại; nút gọi dùng tel:; Zalo có thể dùng liên kết Zalo hoặc widget Zalo OA (cần tài khoản OA xác minh, theo các hướng dẫn bên thứ ba; trang developers.zalo.me chưa đọc được, cần xác minh mã hiện hành); Messenger dùng m.me/[Page]. Thử trên máy thật, vì trình duyệt trong ứng dụng Facebook/TikTok đôi khi xử lý liên kết tel/Zalo khác trình duyệt thường (cần xác minh). Tránh che nút của trang.

Bằng chứng xã hội: đánh giá có tên, ảnh/video thật, số liệu có thể kiểm. Quy tắc nền: không tạo lời chứng thực. Skill skill-copy-pagina-vendas và solo-founder dặn không bịa; FTC Mỹ (14/08/2024) cấm lời chứng thực từ người không tồn tại kể cả do AI tạo (luật Việt Nam về quảng cáo sai sự thật: cần xác minh trước khi nêu điều khoản). Khi chưa có bằng chứng: kể câu chuyện người sáng lập, quy trình minh bạch, bảo đảm, kênh nói chuyện trực tiếp.

Bảo đảm hoàn tiền: viết đủ điều kiện, thời hạn, cách đòi; chỉ hứa nếu chủ thật sự thực hiện. Hormozi chia bảo đảm vô điều kiện, có điều kiện và theo cột mốc (tóm tắt).

Khan hiếm trung thực: chỉ dùng khi có giới hạn thật (số suất, ngày hạn, số thợ); ghi cách đếm và ngày hết hạn thật; không đồng hồ reset, không "còn 3 suất" bịa. Khan hiếm là số lượng, cấp bách là thời gian (tóm tắt).

## 2d. Đặc thù thị trường Việt Nam

| Chủ đề | Điều rút ra | Nguồn, độ chắc |
|---|---|---|
| Quy mô | 85,6 triệu người dùng internet (10/2025), 79,0 triệu danh tính mạng xã hội, 137 triệu kết nối di động | DataReportal Digital 2026 Vietnam (đã đọc) |
| Mobile | Thiết kế mobile trước. Tỷ lệ truy cập web từ điện thoại: DataReportal trang này không nêu, cần xác minh; vẫn coi điện thoại là chính | cần xác minh |
| Tốc độ mạng | Tốc độ tải xuống di động trung vị 152 Mbps (Ookla, cuối 2025), nghĩa là "3G chậm" không còn là mặc định. Nhưng vùng xa, trong nhà, thiết bị rẻ vẫn chậm: giữ trang nhẹ | DataReportal (đã đọc); phần còn lại là khuyến nghị |
| Zalo | Kênh nhắn tin chính: ưu tiên nút Zalo cạnh nút gọi. Con số 78,3 triệu người dùng/tháng do VNG nêu qua bài thứ ba | cần xác minh |
| COD, QR | COD còn lớn (một bài cho 67% giao dịch mua online năm 2024 theo báo cáo PCMI; số khác nhau tùy nguồn), QR tăng nhanh (hơn 4,5 triệu điểm chấp nhận QR đầu 2025). Cho khách chọn COD hoặc chuyển khoản QR; trang bán giá thấp nên có COD | cần xác minh (bài thứ ba, số lệch nhau) |
| VietQR | Tạo mã QR theo số tiền và nội dung; nội dung ngắn (tối đa 19 ký tự, không dấu theo một tài liệu API); đối soát tự động qua dịch vụ như SePay (mẫu ags-salepages dùng SePay) | cần xác minh với tài liệu chính thức |
| Nguồn khách | Facebook, TikTok là kênh chính: dùng Pixel, tham số UTM, trang khớp quảng cáo | thực hành |
| Dữ liệu cá nhân | Luật Bảo vệ dữ liệu cá nhân 2025 (số 91/2025/QH15) có hiệu lực từ 01/01/2026; theo một bài tổng hợp, Nghị định 356/2025/NĐ-CP thay Nghị định 13/2023. Số điện thoại là dữ liệu cá nhân: form phải nêu mục đích, có đồng ý rõ ràng, có chính sách, có cách rút lại. Chi tiết điều khoản và mức phạt (bài báo nêu tới 3 tỷ đồng hoặc 5% doanh thu, nguồn khác nhau): cần xác minh với văn bản chính thức hoặc luật sư | Nguồn: vneconomy.vn và các bài pháp lý (bên thứ ba) |
| Quảng cáo | Không khẳng định sai kết quả, giá, khan hiếm; nội dung cần khớp chính sách quảng cáo Meta/TikTok | thực hành, cần xác minh chính sách hiện hành |

## 2e. Đo lường

Chuẩn bị trước khi bật quảng cáo: tài khoản Meta Business, Pixel ID, tài khoản TikTok Ads và Pixel, GA4 property, tên miền có HTTPS, trang cảm ơn riêng, bảng ghi lead (Google Sheets, CRM), người nhận thông báo (Zalo/Telegram).

| Hành động của khách | Meta | TikTok (cần xác minh tên) | GA4 |
|---|---|---|---|
| Xem trang | PageView, ViewContent | PageView, ViewContent | page_view (tự động) |
| Gửi form lead | Lead | SubmitForm hoặc tương đương | generate_lead (value, currency, lead_source) |
| Bấm gọi/Zalo/Messenger | Contact | tên sự kiện cần xác minh | không có "contact"; gần nhất là working_lead; có thể dùng sự kiện tùy chỉnh |
| Đặt lịch | Schedule | cần xác minh | sự kiện tùy chỉnh |
| Bắt đầu thanh toán | InitiateCheckout | InitiateCheckout | begin_checkout |
| Mua hàng | Purchase (value và currency bắt buộc) | Purchase hoặc CompletePayment (cần xác minh) | purchase (transaction_id, value, currency, items) |

Các điểm cần nhớ:
- Meta: Lead là đăng ký xong; Contact là liên hệ qua điện thoại, tin nhắn, chat (theo tài liệu Pixel).
- Conversions API và chống đếm trùng: Pixel (eventID) và API (event_id) phải trùng, cùng tên sự kiện; Meta giữ sự kiện tới trước và loại trùng trong 48 giờ.
- Tham số khớp người dùng: email và SĐT phải băm; fbp, fbc, IP, user agent không băm.
- TikTok: gửi cùng event_id ở Pixel và Events API; trùng thì gộp khi cách nhau hơn 5 phút và trong 48 giờ; không có event_id thì dùng cookie _ttp để đoán (help center TikTok).
- UTM: gắn utm_source, utm_medium, utm_campaign, utm_content vào link quảng cáo; trang lưu UTM cùng lead để biết lead đến từ đâu.
- Kích hoạt Lead trên trang cảm ơn hoặc sau khi form thành công, không phải khi bấm nút (tránh đếm form lỗi).
- Cloudflare: Zaraz đưa thẻ bên thứ ba ra rìa để trang nhanh hơn (tài liệu Zaraz); trang tổng quan không nói rõ có hỗ trợ Meta Conversions API (cần xác minh trang công cụ cụ thể). Mẫu Worker tự viết có trong repo arbragaa/server-side-tracking-cloudflare (tệp 01).
- Quyền riêng tư: chỉ gửi dữ liệu băm lên nền tảng quảng cáo, không ghi dữ liệu cá nhân thô nếu không cần; có thông báo trên trang.

## 2f. Tốc độ, SEO cơ bản, trang cảm ơn

Core Web Vitals (web.dev, đo ở bách phân vị 75, tách mobile/desktop): LCP tốt khi không quá 2,5 giây; INP tốt khi không quá 200 ms; CLS tốt khi không quá 0,1.

Tốc độ thực dụng:
- Ảnh hero: nhập trong HTML, đặt fetchpriority="high", không tải lười ảnh hero (web.dev optimize-lcp); dùng AVIF/WebP, đúng kích thước.
- Ảnh khác: loading="lazy", ghi width và height để không giật bố cục.
- Font: tối đa 2 kiểu; kiểu có dấu tiếng Việt (subset vietnamese); tránh tải 6 trọng lượng.
- Hạn chế script bên thứ ba; Pixel tải bất đồng bộ; không chặn hiển thị đầu trang.
- Thân trang HTML tĩnh phục vụ qua CDN (Cloudflare Workers static assets) giúp giảm thời gian chờ máy chủ, phần lớn thời gian LCP.

SEO cơ bản (trang bán hàng chủ yếu sống bằng traffic quảng cáo, SEO là phụ):
- Mỗi trang một thẻ title và một meta description riêng, ngắn, đủ thông tin (giá, giờ làm...), không nhồi từ khóa; Google có thể tự viết lại đoạn mô tả (tài liệu Google).
- Thẻ OG (og:title, og:description, og:image) và ảnh chia sẻ 1200x630 để link trên Facebook/Zalo đẹp (thực hành chung, chưa đọc lại tài liệu ngày 19/11).
- Một H1, các tiêu đề con theo thứ tự; alt cho ảnh; chữ không nằm hết trong ảnh.
- Trang cảm ơn thêm noindex.

Trang cảm ơn: xác nhận đã nhận thông tin; hẹn thời gian liên hệ; nút kết nối Zalo hoặc nhóm; tặng tài liệu hoặc video (nếu hứa); chỗ kích hoạt sự kiện Lead; không bán thêm quá gắt; có link về chính sách dữ liệu.

## 3. Checklist hỏi chủ trước khi dựng trang

Hỏi từng nhóm, không đổ hết một lần. Câu nào chủ chưa trả lời thì ghi "chưa có", không tự bịa.

1. Mục tiêu và loại trang: thu số điện thoại/Zalo, bán trực tiếp, đặt lịch hay xem nhà? Một mục tiêu chính là gì?
2. Sản phẩm/dịch vụ: bán gì, kết quả khách nhận được, khác đối thủ ở đâu, ai cũng làm được hay chỉ vùng nào?
3. Giá và ưu đãi: giá chính thức, có giảm không, quà tặng, điều kiện, hạn thật (ngày cụ thể), số suất thật.
4. Khách mục tiêu: ai, bao nhiêu tuổi, ở đâu, đang gặp nỗi đau nào, họ đã biết vấn đề hay biết sản phẩm chưa (mức nhận thức)?
5. Bằng chứng thật: đánh giá có tên, ảnh/video trước-sau, số khách đã phục vụ, giấy phép, báo chí. Ghi rõ cái nào chưa có.
6. Bảo đảm: có hoàn tiền, làm lại, hủy được không; điều kiện thế nào; chủ có chịu thực hiện không?
7. Hình thức liên hệ: số gọi, Zalo (cá nhân hay OA), Messenger, form; ai trả lời; giờ làm việc; bao lâu phản hồi?
8. Thanh toán (nếu bán): COD, chuyển khoản QR, ví; tài khoản nhận tiền; ai đối soát; chính sách đổi trả.
9. Kênh kéo khách: Facebook, TikTok, Google, giới thiệu? Khách lạnh hay đã biết mình? Sẽ có quảng cáo khớp thông điệp nào?
10. Đo lường: đã có Pixel Meta/TikTok, GA4, tên miền chưa? Lead lưu ở đâu, ai nhận thông báo?
11. Thương hiệu: logo, màu, font, ảnh thật, giọng văn; trang tham khảo thích; điều cấm (không dùng màu gì, không nói gì).
12. Pháp lý: tên pháp nhân, địa chỉ, mã số thuế, chính sách bảo mật và đổi trả; có thu dữ liệu cá nhân nên cần ô đồng ý.
13. Tên miền và nơi đặt: đã có tên miền chưa, ai quản trị DNS, có dùng Cloudflare không?
14. Duyệt: ai duyệt nội dung và hành động bên ngoài (đăng, chạy quảng cáo, gửi tin, thanh toán) trước khi chạy.

Quy tắc cho cộng sự: thiếu thông tin thì hỏi, không bịa lời chứng thực, số liệu, đồng hồ đếm ngược, giá; không chép nguyên văn tài liệu có bản quyền; hành động bên ngoài (đăng, quảng cáo, gửi tin, thanh toán) cần chủ duyệt.
