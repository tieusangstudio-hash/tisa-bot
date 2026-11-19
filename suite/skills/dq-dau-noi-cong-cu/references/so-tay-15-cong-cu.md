# Sổ tay 15 thẻ kết nối của TISA BOT

Tự tạo từ hướng dẫn trong app (cập nhật 2026-11-19). Giao diện nền tảng đổi thì làm theo ý nghĩa nhãn trên màn hình.

## Nguyên tắc chung
- Làm bằng ĐÚNG trình duyệt TISA BOT đang chạy (đầu việc tisa_browser_look op=profiles, nói tên). TRƯỚC KHI mở web: tisa_browser_look op=tabs; nền tảng đã có tab mở sẵn (đã đăng nhập) thì switch_tab dùng luôn, không mở Chrome mới, không bắt anh đăng nhập lại. Chưa có tab thì mở tab mới trong cùng trình duyệt (hoi_mo tự chuyển sang tab có sẵn nếu có). Trang đổi thì look lại trước khi bấm tiếp.
- Việc trong TISA BOT (mở thẻ, chọn ô, bấm Kết nối/Lưu) làm bằng tisa_browser_do op=ui_tisa (lenh=mo_the ten=<tên thẻ> | chon_o truong=<nhãn ô> | bam nhan=<chữ nút> | xem). Không mở TISA BOT trong trình duyệt, không bắt anh đăng nhập lại TISA BOT.
- Mã, token, khóa bí mật: KHÔNG đọc ra chat, KHÔNG ghi vào tệp hay bộ nhớ. Chuyển thẳng từ trang nền tảng sang ô của TISA BOT bằng tisa_browser_do op=dan_vao_tisa tu_tab=<mã tab> tu_id=<số khối chứa mã> (ô hiện chấm tròn).
- Chỉ dừng nhờ anh (một câu ngắn, nói rõ bấm gì ở đâu, rồi wait_user) khi thật sự không làm thay được: đăng nhập, mật khẩu, mã xác thực 2 lớp, OTP, CAPTCHA, quét QR bằng điện thoại, thanh toán hoặc thẻ, bấm Cho phép/Đồng ý ở màn hình xin quyền. Anh xong thì làm tiếp ngay.
- Chỉ xin quyền tối thiểu. Không xóa tệp. Không đổi gì khác trong tài khoản của anh ngoài việc cần để kết nối.
- Kẹt cùng một chỗ 3 lần: dừng, chụp màn hình, nói đúng chỗ kẹt và việc anh cần làm. Xong thì bấm Kiểm tra/Lưu và đọc kết quả ở phần Thông báo, rồi báo anh một câu: đã nối được chưa, nối vào tài khoản nào.

## Meta Ads (Facebook và Instagram, chỉ đọc)

**Mục tiêu:** nối thẻ Meta Ads để TISA BOT xem tài khoản quảng cáo, chiến dịch, hiệu suất (chỉ đọc, không tạo, không sửa, không tiêu tiền)

**Cần lấy:** App ID (ID ứng dụng); App Secret (Khóa bí mật của ứng dụng)

**Trang web:** https://developers.facebook.com/apps/, https://business.facebook.com/

**Từ khóa khớp:** meta ads

**Các bước:**
1. Mở https://developers.facebook.com/apps/ (chưa đăng nhập Facebook thì dừng cho anh đăng nhập). Dùng đúng tài khoản Facebook là Quản trị viên của tài khoản quảng cáo/Trang cần nối.
2. Đã có sẵn một app Meta (ví dụ app anh tạo cho Messenger hay Trang)? Dùng lại, vì một app dùng chung cho mọi thẻ Meta. Chưa có: bấm "Tạo ứng dụng" (Create app), đặt tên (ví dụ TISA BOT + tên shop), nhập email, chọn trường hợp sử dụng "Khác" (Other), chọn loại "Doanh nghiệp" (Business), bấm tạo. Meta hỏi lại mật khẩu thì dừng cho anh nhập. Loại Business mới tạo được token; loại Consumer thì không.
3. Nhìn CỘT TRÁI của trang app: thấy mục "Sản phẩm" là giao diện CŨ, thấy "Trường hợp sử dụng" là giao diện MỚI. Hai bản đi khác đường ở bước sau.
4. Giữ app ở chế độ Phát triển (Development) và anh là Quản trị viên của app. Bỏ qua "Xác minh doanh nghiệp" và "Xét duyệt ứng dụng": chỉ cần khi app phục vụ doanh nghiệp KHÁC, anh tự dùng cho tài khoản của mình thì không cần và chỉ mất thêm nhiều ngày chờ.
5. Đăng nhập bằng Facebook, bản CŨ: Sản phẩm > Thêm sản phẩm > "Đăng nhập bằng Facebook" bản THƯỜNG (không phải bản dành cho doanh nghiệp) > Cài đặt. Bản MỚI: Trường hợp sử dụng > mở mục có "Đăng nhập bằng Facebook" > Tùy chỉnh > Cài đặt (thường có sẵn).
6. Ô "URI chuyển hướng OAuth hợp lệ": TISA BOT chạy trên máy cá nhân (localhost) thì BỎ QUA. Chạy trên VPS hoặc tên miền riêng thì dùng ui_tisa lenh=xem để lấy địa chỉ trong hộp TISA, dán NGUYÊN VĂN vào ô đó rồi Lưu; thêm tên miền (không có https://, không có dấu /) vào ô "Miền ứng dụng" ở Cài đặt ứng dụng > Thông tin cơ bản rồi Lưu thay đổi.
7. Bảng báo "Invalid Scopes: ads_read, business_management": bấm OK và đi tiếp, cảnh báo đó chỉ hiện cho người tạo app. Chỉ khi nối xong mà không thấy tài khoản quảng cáo nào mới thêm quyền: Thêm trường hợp sử dụng > quảng cáo (Marketing API) > Tùy chỉnh > tab Quyền, thêm ads_read.
8. Cài đặt ứng dụng > Thông tin cơ bản: lấy ID ứng dụng và Khóa bí mật (bấm Hiện; Meta có thể bắt nhập lại mật khẩu thì dừng cho anh). Dán thẳng vào hai ô "App ID (Facebook)" và "App Secret (Facebook)" của thẻ Meta Ads bằng ui_tisa + dan_vao_tisa.
9. Bấm "Lưu & mở trang đăng nhập": cửa sổ Facebook hiện ra. Anh đăng nhập và bấm Tiếp tục, TICK đúng tài khoản quảng cáo cho TISA BOT, bấm Cho phép (AI không bấm thay). Xong anh nói, em kiểm tra thẻ đã nối được.
10. Token sống khoảng 60 ngày, TISA BOT tự gia hạn; hết hẳn thì bấm Kết nối lại trên thẻ.

**Luu y:**
- Đây là thẻ chỉ đọc. Muốn bật, tắt, đổi ngân sách thì dùng lệnh trong chat với tài khoản nối bằng API ở trang Quảng Cáo.

## Facebook Trang (đăng bài, bình luận)

**Mục tiêu:** nối thẻ Facebook Trang để TISA BOT đăng bài lên Fanpage, sửa bài, đọc và trả lời bình luận

**Cần lấy:** App ID; App Secret; chọn đúng các Trang cho phép

**Trang web:** https://developers.facebook.com/apps/

**Từ khóa khớp:** facebook trang, facebook pages, fanpage tisa

**Các bước:**
1. Mở https://developers.facebook.com/apps/ (chưa đăng nhập Facebook thì dừng cho anh đăng nhập). Dùng đúng tài khoản Facebook là Quản trị viên của tài khoản quảng cáo/Trang cần nối.
2. Đã có sẵn một app Meta (ví dụ app anh tạo cho Messenger hay Trang)? Dùng lại, vì một app dùng chung cho mọi thẻ Meta. Chưa có: bấm "Tạo ứng dụng" (Create app), đặt tên (ví dụ TISA BOT + tên shop), nhập email, chọn trường hợp sử dụng "Khác" (Other), chọn loại "Doanh nghiệp" (Business), bấm tạo. Meta hỏi lại mật khẩu thì dừng cho anh nhập. Loại Business mới tạo được token; loại Consumer thì không.
3. Mở phần Đăng nhập bằng Facebook như thẻ Meta Ads (bản CŨ: Sản phẩm; bản MỚI: Trường hợp sử dụng > Tùy chỉnh).
4. Bảng "Invalid Scopes: pages_show_list, pages_read_engagement...": bấm OK, đi tiếp. Chỉ khi nối xong mà không thấy Trang hoặc không đăng được: Thêm trường hợp sử dụng > "Quản lý mọi thứ trên Trang của bạn" > Tùy chỉnh > tab Quyền, thêm các quyền đăng và quản lý bài.
5. TISA BOT trên máy cá nhân (localhost) thì bỏ qua ô URI chuyển hướng; trên VPS hoặc tên miền riêng thì dán địa chỉ chuyển hướng lấy từ hộp TISA vào ô đó và tên miền vào "Miền ứng dụng" (xem bước tương tự ở thẻ Meta Ads).
6. Giữ app ở chế độ Phát triển, anh là Quản trị viên của app và của các Trang cần quản lý: tự cấp được quyền, không cần App Review.
7. Cài đặt ứng dụng > Thông tin cơ bản: lấy ID ứng dụng và Khóa bí mật, dán thẳng vào hai ô của thẻ Facebook Trang rồi bấm "Lưu & mở trang đăng nhập".
8. Cửa sổ Facebook hiện ra: anh đăng nhập, TICK các Trang muốn cho TISA BOT quản lý, bấm Cho phép. Thêm Trang sau này: bấm "Kết nối lại" trên thẻ, tick THÊM Trang mới và GIỮ NGUYÊN các Trang cũ (bỏ tick là mất quyền Trang đó).
9. Đăng và sửa bài là việc thật nên thẻ này chỉ chạy ở mức Toàn quyền. Token khoảng 60 ngày, TISA BOT tự gia hạn.

**Luu y:**
- Muốn bot tự trực tin nhắn và bình luận của khách: dùng thẻ Kết nối Meta (Messenger), không phải thẻ này.

## Kết nối Meta (Fanpage, Messenger, Instagram, Threads)

**Mục tiêu:** nối Fanpage Facebook (kèm Instagram, Threads) để bot trả lời tin nhắn, bình luận và TISA BOT đăng bài

**Cần lấy:** Địa chỉ quay về và link chính sách (lấy từ hộp Kết nối Meta của TISA BOT); App ID; App Secret

**Trang web:** https://developers.facebook.com/apps/

**Từ khóa khớp:** kết nối meta, messenger, fanpage facebook kèm instagram

**Các bước:**
1. Mở hộp Kết nối Meta của TISA BOT (ui_tisa lenh=mo_the ten="Kết nối Meta"), ui_tisa lenh=xem để đọc "Địa chỉ quay về" và "Link chính sách quyền riêng tư" (hai địa chỉ công khai của máy này).
2. KIỂM HTTPS NGAY: Facebook chỉ nhận địa chỉ quay về dạng https. Hộp báo "cần địa chỉ HTTPS" hoặc nút Đăng nhập Facebook xám (không bấm được) nghĩa là TISA BOT đang mở bằng http (127.0.0.1, localhost, IP mạng nội bộ) và máy chưa có địa chỉ https. Cài đặt > Truy cập từ xa: bật đường hầm (hoặc nối tên miền riêng đã có), chờ có địa chỉ https rồi mở lại hộp Kết nối Meta. Bản TISA BOT mới tự dùng địa chỉ https của đường hầm đang chạy kể cả khi trang mở bằng http. Địa chỉ quay về dán vào Meta phải là địa chỉ https đó; đường hầm nhanh (trycloudflare) đổi địa chỉ khi khởi động lại thì phải dán lại.
3. Mở https://developers.facebook.com/apps/ (đăng nhập Facebook bằng tài khoản Quản trị viên Fanpage; chưa đăng nhập thì dừng cho anh). Đã có app dùng cho Fanpage này thì dùng lại và báo tên app. Chưa có: Tạo ứng dụng, tên = tên Fanpage + chữ Bot, email của anh, trường hợp sử dụng "Tương tác với khách hàng trên Messenger from Meta" (Engage with customers on Messenger from Meta), chọn Business portfolio đang quản lý Fanpage (không có thì chọn chưa kết nối), bấm Tạo. Meta hỏi mật khẩu thì dừng cho anh.
4. Trường hợp sử dụng (Use cases): đảm bảo có Messenger. Dòng "Quản lý mọi thứ trên Trang" > Tùy chỉnh, thêm 4 quyền: pages_read_engagement, pages_read_user_content, pages_manage_engagement, pages_manage_posts. Hộp hỏi ảnh hưởng trường hợp khác thì bấm Add. Kiểm tra các quyền đều "Sẵn sàng thử nghiệm" (Ready for testing).
5. Facebook Login (hoặc Facebook Login for Business) > Cài đặt: bật "Đăng nhập OAuth ứng dụng khách" và "Đăng nhập OAuth trên web"; dán Địa chỉ quay về vào "URI chuyển hướng OAuth hợp lệ", bấm Lưu thay đổi. Chưa có mục này thì thêm Facebook Login trước.
6. Cài đặt ứng dụng > Thông tin cơ bản: dán Link chính sách vào "URL chính sách quyền riêng tư" và "Hướng dẫn xóa dữ liệu người dùng" (User data deletion), chọn Hạng mục phù hợp với shop, Lưu thay đổi.
7. Lấy ID ứng dụng và Khóa bí mật (bấm Hiện, có thể cần nhập lại mật khẩu: dừng cho anh), dán thẳng vào hai ô App ID và App Secret của hộp Kết nối Meta bằng dan_vao_tisa. KHÔNG đọc App Secret ra chat.
8. Hai ô quyền thêm trong hộp ("Nối cả Instagram của Trang", "Đọc số liệu bài viết") ĐỂ TRỐNG, trừ khi anh muốn dùng và app Meta đã thêm quyền đó (xem ghi chú bên dưới). Tick mà app chưa có quyền thì Facebook báo "Invalid Scopes: read_insights" (hoặc instagram_*) và từ chối cả lần đăng nhập. Nối Fanpage để nhắn tin, bình luận và đăng bài không cần hai ô này. Rồi bấm "Đăng nhập Facebook" trong hộp Kết nối Meta: anh chọn Fanpage và bấm đồng ý tất cả quyền (AI không bấm đồng ý thay).
9. Hỏi anh có muốn bật chế độ Live để khách thật nhắn được không. Anh đồng ý rõ ràng thì mới gạt Live; không thì để chế độ Phát triển (chỉ quản trị viên, người thử nghiệm nhắn được).

**Luu y:**
- Kết nối Instagram: tài khoản Instagram phải là Business/Creator và liên kết với đúng Fanpage trong Cài đặt Trang. Threads thêm bằng nút + Threads trên thẻ sau khi nối Fanpage.
- Thêm Instagram sau khi đã nối Fanpage: trong app Meta thêm trường hợp sử dụng Instagram với đủ 3 quyền instagram_basic, instagram_manage_messages, instagram_manage_comments (cùng chỗ Trường hợp sử dụng > Tùy chỉnh), xác nhận hiện "Sẵn sàng thử nghiệm". Rồi ở Trang đã nối bấm "Đổi token", tick "Nối cả Instagram của Trang", Đăng nhập Facebook lại. Bảng kiểm tra của Trang báo đã có quyền chưa.
- Số liệu bài viết (lượt tiếp cận, lượt lưu): thêm quyền read_insights vào app (cùng chỗ thêm 4 quyền Trang; không thấy thì tìm trong mục Quyền và tính năng của app), rồi ở Trang đã nối bấm "Đổi token", tick "Đọc số liệu bài viết", Đăng nhập Facebook lại. Bảng kiểm tra có dòng "Đọc số liệu bài viết".
- Chỉ làm bước thêm quyền khi anh MUỐN dùng tính năng đó. Không thêm hay tick "cho đủ": cả lần đăng nhập hỏng chỉ vì một quyền app chưa có.
- Lỗi hay gặp: (1) "Invalid Scopes" trên trang Facebook: bỏ tick hai ô quyền thêm, mở lại trang đăng nhập, bấm lại; (2) Facebook báo URL bị chặn: chưa dán Địa chỉ quay về vào "URI chuyển hướng OAuth hợp lệ" của Facebook Login, hoặc địa chỉ https đã đổi; (3) nút Đăng nhập Facebook xám: xem bước KIỂM HTTPS; (4) app còn chế độ Phát triển: chỉ quản trị viên, nhà phát triển, người thử nghiệm của app nhắn được, muốn khách thật nhắn thì Live (hỏi anh trước); (5) App secret sai: lấy lại ở Cài đặt ứng dụng > Thông tin cơ bản của ĐÚNG app; (6) bot im lặng sau khi nối: vào Chatbot > Bot, tick kênh vừa nối vào một bot và bật bot; Trang bấm Kiểm tra rồi Sửa tự động.
- Làm xong bấm Kiểm tra ở Trang vừa nối và đọc bảng kiểm tra từng dòng; chỉ báo xong khi dòng nhắn tin và bình luận xanh. Dòng vàng nào còn thiếu thì nói đúng thiếu gì.

## Cloudflare

**Mục tiêu:** nối Cloudflare để TISA BOT quản lý DNS, Workers, Pages, KV, R2, D1, đưa trang web lên mạng

**Cần lấy:** API token (Cloudflare); Account ID (chỉ khi token thấy nhiều tài khoản)

**Trang web:** https://dash.cloudflare.com/profile/api-tokens, https://dash.cloudflare.com/

**Từ khóa khớp:** cloudflare

**Các bước:**
1. Thẻ có hai cách: "dán API token" (quyền do token quyết định, dùng chung được với gói Cloudflare Deploy/Wrangler) hoặc "Cloudflare (đăng nhập web)" (một chạm, không tạo token). Mặc định chọn API token. Anh chỉ muốn thử nhanh thì dùng đăng nhập web: mở thẻ Cloudflare (đăng nhập web), bấm Đăng nhập Cloudflare, anh đăng nhập và đồng ý.
2. Mở https://dash.cloudflare.com/profile/api-tokens (anh đăng nhập Cloudflare nếu cần). Bấm "Create Token" > "Create Custom Token" > Get started, đặt tên TISA BOT.
3. Permissions (mỗi quyền một dòng, bấm Add more): Account > Workers Scripts > Edit; Account > Cloudflare Pages > Edit; Account > Workers KV Storage > Edit; Account > Workers R2 Storage > Edit; Account > D1 > Edit; Zone > DNS > Edit; Zone > Zone > Read; Account > Account Settings > Read. Anh chỉ muốn xem thì chọn Read cho các mục đó. Không bật quyền nào ngoài nhu cầu.
4. Account Resources: Include > tài khoản của anh. Zone Resources: Include > All zones, hoặc đúng các tên miền cần quản lý. KHÔNG bật lọc theo IP (Client IP Address Filtering): MCP của Cloudflare chưa nhận token có lọc IP.
5. Bấm Continue to summary > Create Token. Token CHỈ HIỆN MỘT LẦN: dán thẳng vào ô "API token (Cloudflare)" của thẻ bằng dan_vao_tisa (tu_id = số khối chứa token), không đọc ra chat.
6. Account ID để trống nếu token chỉ thấy một tài khoản. Cần thì lấy ở trang chủ dash.cloudflare.com (cột phải hoặc trong menu ba chấm cạnh tên tài khoản > Copy account ID).
7. Bấm Kết nối trong thẻ, đợi đèn xanh, bấm Kiểm tra.

**Luu y:**
- Token tạo một lần dùng lại được cho dịch vụ khác nên báo anh cất token ở nơi an toàn. Thiếu quyền mảng nào thì đúng mảng đó báo lỗi: quay lại sửa token (Edit) thêm quyền, không cần tạo mới.

## Composio

**Mục tiêu:** nối cổng Composio để TISA BOT dùng hơn 500 ứng dụng (Gmail, Notion, Sheets, GitHub, Linear, Slack...) qua một khóa

**Cần lấy:** Consumer key dạng ck_... (KHÔNG phải Project API key ak_...)

**Trang web:** https://dashboard.composio.dev/, https://composio.dev/

**Từ khóa khớp:** composio

**Các bước:**
1. Mở https://composio.dev, đăng nhập hoặc đăng ký tài khoản Composio (anh tự làm bước đăng nhập, đăng ký, xác minh email).
2. Vào mục kết nối cho AI: "Connect my agent" (Composio For You), hoặc trang Install/AI Clients của dashboard, chọn một MCP client bất kỳ (ví dụ Claude Code hoặc Cursor). Trang hiện câu lệnh cấu hình kèm khóa dạng ck_... gắn vào header x-consumer-api-key.
3. Lấy ĐÚNG khóa ck_ (consumer key): dán thẳng vào ô "API key (Composio)" của thẻ bằng dan_vao_tisa. Không dùng Project API key ak_ hay MCP server tạo trong Platform (không dùng được cho đường này).
4. Bấm Kết nối trong thẻ rồi Kiểm tra. Đã có thẻ Composio cũ thì dùng "Kết nối lại" để thay khóa.
5. Kết nối ứng dụng cụ thể (Gmail, Notion...) ở Composio For You > Connect Apps: mỗi app anh tự đăng nhập và bấm Cho phép. Khóa ck_ không tự cập nhật khi anh kết nối thêm app, TISA BOT tìm tool và mở link đăng nhập từng app khi cần.

**Luu y:**
- Tạo lại (regenerate) khóa thì khóa cũ chết, thẻ phải nhập khóa mới.

## Zalo Agent MCP

**Mục tiêu:** nối Zalo cá nhân để TISA BOT đọc tin, tìm cuộc chat, gửi tin bằng tài khoản Zalo

**Cần lấy:** quét mã QR bằng app Zalo trên điện thoại

**Từ khóa khớp:** zalo

**Các bước:**
1. Kiểm tra máy có Node.js 20 trở lên (không có thì nói anh cài từ nodejs.org, hoặc tự chạy lệnh cài nếu máy cho phép và anh đồng ý).
2. Thẻ Zalo Agent MCP: bấm Kết nối bằng ui_tisa. Mã QR hiện ra trong hộp.
3. Chụp màn hình để thấy mã QR, nói anh: "Anh mở Zalo trên điện thoại, quét mã QR đang hiện trong TISA BOT rồi bấm Đăng nhập trên điện thoại". wait_user.
4. Anh quét xong, đọc lại thẻ: đèn xanh là nối được. Gói tool Zalo đi kèm hiện ngay sau khi đăng nhập thì cài luôn.

**Luu y:**
- Nếu Zalo hỏi xác minh thêm trên điện thoại thì anh tự bấm. Mỗi lần quét chỉ đăng nhập một tài khoản Zalo.

## Botcake

**Mục tiêu:** nối chatbot Botcake để xem khách, tag, flow và gửi tin

**Cần lấy:** Page ID (trang Facebook gắn với Botcake); API Key của page (access token)

**Trang web:** https://botcake.io/

**Từ khóa khớp:** botcake

**Các bước:**
1. Mở https://botcake.io và đăng nhập (anh tự đăng nhập). Chọn đúng page cần nối.
2. Vào Cấu hình (Setting) > Tích hợp > Public API (có thể ghi là API Access Token) > Tạo API Key. Lưu ý: làm mới hoặc xóa key sẽ làm các kết nối cũ ngừng chạy.
3. Lấy Page ID: là dãy số của Fanpage Facebook gắn với Botcake (thường hiện trong đường dẫn hoặc phần thông tin page). Điền vào ô Page ID của thẻ.
4. Dán API key thẳng vào ô "API Key của page" bằng dan_vao_tisa. Bấm Kết nối rồi Kiểm tra.

**Luu y:**
- Mỗi page có một key riêng. Nhiều page thì nối từng page bằng nút + Thêm tài khoản.

## Google (Gmail, Lịch, Drive, Docs, Sheets, Tasks, Analytics, Ads, Search Console, Tag Manager, Merchant Center)

**Mục tiêu:** nối dịch vụ Google bằng OAuth client của chính anh (làm một lần, dùng lại cho mọi dịch vụ Google khác bằng nút "Dùng lại key")

**Cần lấy:** OAuth Client ID; OAuth Client Secret; email Google của anh

**Trang web:** https://console.cloud.google.com/

**Từ khóa khớp:** google, gmail, workspace, tag manager, merchant, analytics, search console

**Các bước:**
1. Trước hết ui_tisa lenh=mo_the để xem thẻ cần ô nào. Dịch vụ OAuth (Gmail, Lịch, Drive, Docs, Tasks, Analytics, Ads): cần Client ID và Client Secret. Google Sheets và Search Console: cần tệp Service account JSON (xem lưu ý). Google Keep, NotebookLM có cách riêng.
2. Mở https://console.cloud.google.com (anh đăng nhập Google nếu cần; Google có thể xác minh 2 lớp: dừng cho anh). Đã có project dùng cho Google khác thì dùng lại; chưa có: bấm chọn project > New Project, đặt tên TISA BOT > Create.
3. APIs & Services > Library: tìm và bấm Enable cho từng API đúng dịch vụ cần nối: Gmail API, Google Calendar API, Google Drive API, Google Docs API, Google Sheets API, Google Tasks API, Google Analytics Data API và Analytics Admin API (cho GA4), Google Ads API (cho Ads), Search Console API, Tag Manager API, Content API for Shopping (Merchant Center). Quên bật API nào thì đúng nhóm tool đó báo lỗi.
4. APIs & Services > Google Auth Platform (màn hình đồng ý OAuth cũ): Get started > tên ứng dụng TISA BOT, email hỗ trợ là email anh > Audience chọn External > email liên hệ > Create. Tab Audience > Test users > Add users: thêm CHÍNH email Google của anh (bỏ bước này thì Google chặn ngay lúc đăng nhập).
5. Mẹo quan trọng: ở chế độ Testing, quyền đăng nhập hết hạn sau 7 ngày. Anh dùng cá nhân thì vào tab Audience bấm Publish app (chuyển In production), không cần nộp xác minh; lúc đăng nhập Google hiện "ứng dụng chưa được xác minh" thì bấm Nâng cao > Tiếp tục (Go to ... unsafe) vì đây là app của chính anh.
6. Google Auth Platform > Clients (hoặc APIs & Services > Credentials) > Create client / Create credentials > OAuth client ID. Loại ứng dụng: thẻ Gmail và Lịch chọn "Web application" và dán Redirect URI lấy từ thẻ TISA vào "Authorized redirect URIs" (copy bằng ui_tisa lenh=xem); thẻ Google Workspace chọn "Desktop app" (không cần redirect). Bấm Create.
7. Hộp hiện Client ID và Client Secret CHỈ HIỆN MỘT LẦN: bấm Download JSON, hoặc dán từng giá trị thẳng vào ô "OAuth Client ID" và "OAuth Client Secret" bằng dan_vao_tisa. Thẻ Google có ô kéo thả JSON thì cũng được. Điền email Google của anh vào ô email nếu có.
8. Bấm Kết nối (hoặc Lưu và mở đăng nhập). Trình duyệt mở cửa sổ Google: anh chọn tài khoản, bấm Tiếp tục, TICK HẾT các ô quyền (bỏ ô nào là đúng nhóm tool đó không chạy), Cho phép (AI không bấm thay). Quay lại thẻ, đèn xanh là nối được.
9. Dịch vụ thứ hai trở đi (Lịch, Drive, Analytics...): mở thẻ, bấm "Dùng lại key" chọn key đã tạo, khỏi làm lại các bước tạo client.

**Luu y:**
- Google Ads cần thêm Developer token: trong tài khoản Google Ads quản lý (MCC) vào Tools and settings > API Center xin Developer token (có thể phải chờ Google duyệt), cộng với Login customer ID (10 số, ở góc trên bên phải Google Ads).
- Google Sheets, Search Console: tạo Service account (IAM & Admin > Service Accounts > Create > Keys > Add key > JSON), tải JSON. Sheets: chia sẻ bảng tính hoặc thư mục cho email của service account. Search Console: thêm email service account làm người dùng của property ở Settings > Users and permissions.
- Google Keep không có API chính thức: dùng Mật khẩu ứng dụng (app password) của tài khoản Google bật 2 lớp; cẩn thận, nhờ anh tự quyết định.
- Máy không có màn hình (VPS) không đăng nhập Google được bằng cửa sổ trình duyệt của máy chủ: dùng thẻ Lịch hoặc Gmail riêng.

## Google NotebookLM

**Mục tiêu:** nối NotebookLM (chưa có API chính thức nên mượn PHIÊN đăng nhập trình duyệt)

**Cần lấy:** phiên đăng nhập Google của trình duyệt đã chọn (storage_state)

**Trang web:** https://notebooklm.google.com/

**Từ khóa khớp:** notebooklm

**Các bước:**
1. Mở https://notebooklm.google.com bằng trình duyệt đã chọn cho AI. Chưa đăng nhập Google thì dừng cho anh đăng nhập MỘT LẦN ngay trong trình duyệt TISA này (phiên chép từ Chrome thường bị Google hủy).
2. ui_tisa lenh=mo_the ten="Google NotebookLM" để con trỏ ở ô phiên đăng nhập.
3. tisa_browser_do op=dan_vao_tisa kieu=phien_trinh_duyet mien=google.com (cần anh duyệt trừ khi đang Toàn quyền): dán phiên vào ô, ô hiện chấm tròn. TUYỆT ĐỐI không chạy lệnh "notebooklm login" hay mở trình duyệt khác.
4. Bấm Kết nối rồi Kiểm tra; thử liệt kê notebook để chắc đã nối.

**Luu y:**
- Chuỗi phiên tương đương đang đăng nhập Google, không giới hạn phạm vi: chỉ làm trên máy anh tin tưởng.

## TikTok (quảng cáo)

**Mục tiêu:** lấy ADVERTISER ID và ACCESS TOKEN của TikTok API for Business để dán vào TISA BOT

**Cần lấy:** Advertiser ID; Access Token (mã dài hạn)

**Trang web:** https://business-api.tiktok.com/portal, https://ads.tiktok.com/

**Từ khóa khớp:** tiktok

**Các bước:**
1. Mở https://business-api.tiktok.com/portal, đăng nhập bằng tài khoản TikTok For Business là quản trị nhà quảng cáo (anh tự đăng nhập, mã xác thực).
2. My Apps > Create New App (Tạo ứng dụng): tên TISA BOT, mô tả ngắn, Advertiser redirect URL ghi https://localhost, chọn quyền Ads Management và Reporting (đọc báo cáo), gửi duyệt.
3. TikTok duyệt ứng dụng mất vài giờ đến vài ngày, không ai rút ngắn được: báo anh rồi dừng, anh quay lại nói khi đã duyệt.
4. Khi đã duyệt: trong trang ứng dụng mở "Advertiser authorization URL", anh đăng nhập và bấm Confirm cho phép các tài khoản nhà quảng cáo; trang chuyển về https://localhost kèm auth_code trong thanh địa chỉ (trang lỗi không sao).
5. Đổi auth_code lấy Access Token: dùng mục "Get access token" của trang ứng dụng (cần App ID và Secret của ứng dụng), kết quả có access_token và danh sách advertiser_id. KHÔNG đọc token ra chat.
6. Dán Advertiser ID và Access Token thẳng vào các ô của thẻ TikTok trong TISA BOT bằng dan_vao_tisa rồi bấm Lưu và kiểm tra.

**Luu y:**
- Chưa duyệt app thì chỉ có sandbox (dữ liệu thử). Dùng thật phải qua duyệt của TikTok.

## Zernio

**Mục tiêu:** nối Zernio (đăng bài nhiều mạng xã hội) bằng API key

**Cần lấy:** API key (Zernio)

**Trang web:** https://github.com/tieusangstudio-hash/tisa-store/blob/main/huong-dan/zernio.md

**Từ khóa khớp:** zernio

**Các bước:**
1. Mở trang hướng dẫn kèm theo (đường dẫn ở mục trang) và đọc đúng các bước lấy API key trên trang Zernio; đăng nhập Zernio thì dừng cho anh.
2. Lấy API key, dán thẳng vào ô của thẻ bằng dan_vao_tisa, bấm Kết nối rồi Kiểm tra.

## Substack

**Mục tiêu:** nối Substack để soạn và đăng bài, newsletter

**Cần lấy:** Publication URL; Session token (cookie substack.sid); User ID

**Trang web:** https://substack.com/

**Từ khóa khớp:** substack

**Các bước:**
1. Mở trang Substack của anh trong trình duyệt đã chọn (đăng nhập thì dừng cho anh).
2. Publication URL: địa chỉ trang, dạng https://tencuaban.substack.com. Điền vào ô.
3. Session token là cookie substack.sid: không có đường chép kín an toàn, nên nhờ anh tự lấy: F12 > Application > Cookies > substack.com > substack.sid, sao chép Value và tự dán vào ô (đừng dán vào chat).
4. User ID là dãy số: lấy theo trang Hướng dẫn của thẻ (có trợ lý lấy nhanh). Bấm Kết nối rồi Kiểm tra.

**Luu y:**
- Cookie phiên tương đương đang đăng nhập Substack: giữ kín.

## CRM của tôi (Web CRM TISA)

**Mục tiêu:** nối CRM của anh để TISA BOT xem và thêm khách

**Cần lấy:** địa chỉ CRM (crm_url); API key của CRM

**Từ khóa khớp:** crm của tôi, crm

**Các bước:**
1. Mở trang Quản lý web của TISA BOT, thẻ Web CRM: lấy địa chỉ CRM đang chạy (localhost hoặc địa chỉ công khai nếu đã đưa lên mạng).
2. API key CRM nằm trong cài đặt của CRM (đăng nhập CRM bằng tài khoản chủ; mật khẩu anh tự nhập). Dán thẳng vào ô của thẻ bằng dan_vao_tisa.
3. Bấm Kết nối rồi Kiểm tra.

## GitHub

**Mục tiêu:** nối GitHub để TISA BOT đọc kho mã, issue, pull request (và ghi nếu anh cho phép)

**Cần lấy:** Personal access token (nếu thẻ hỏi), hoặc đăng nhập GitHub khi thẻ mở cửa sổ

**Trang web:** https://github.com/settings/personal-access-tokens

**Từ khóa khớp:** github

**Các bước:**
1. ui_tisa lenh=mo_the ten="GitHub" để xem thẻ cần gì: nếu có nút đăng nhập GitHub thì bấm, anh đăng nhập và bấm Authorize (AI không bấm thay).
2. Thẻ cần token: mở https://github.com/settings/personal-access-tokens (anh đăng nhập GitHub, có thể có mã xác thực 2 lớp: dừng cho anh) > Generate new token (Fine-grained).
3. Đặt tên TISA BOT, hạn dùng (Expiration) 90 ngày hoặc theo ý anh, Repository access chọn đúng các kho cần dùng (hoặc All repositories nếu anh muốn). Permissions chỉ cấp tối thiểu: chỉ xem thì Contents, Issues, Pull requests ở mức Read-only; muốn TISA BOT sửa và đăng thì thêm Read and write đúng mục đó.
4. Bấm Generate token. Token CHỈ HIỆN MỘT LẦN: dán thẳng vào ô của thẻ bằng dan_vao_tisa, không đọc ra chat. Bấm Kết nối rồi Kiểm tra.

**Luu y:**
- Token hết hạn thì tạo lại và dùng Kết nối lại trên thẻ.

## API tuỳ chỉnh (API key)

**Mục tiêu:** nối một dịch vụ bất kỳ có API và API key

**Cần lấy:** địa chỉ API gốc (base_url); API key; kiểu gửi key (auth_style); đường dẫn tài liệu (docs_url)

**Từ khóa khớp:** api tuỳ chỉnh, api tùy chỉnh, custom

**Các bước:**
1. Hỏi anh dịch vụ nào (một câu), tìm tài liệu API chính thức bằng tisa_web_search và tisa_web_fetch: lấy base URL, cách gửi key (header Authorization Bearer, x-api-key hoặc query).
2. Mở trang quản lý của dịch vụ trong trình duyệt đã chọn để tạo API key (đăng nhập thì dừng cho anh), dán thẳng vào ô bằng dan_vao_tisa, điền các ô còn lại, Kết nối và Kiểm tra.

## topview

Topview chưa có hướng dẫn riêng: ui_tisa lenh=mo_the để xem ô cần điền, tìm tài liệu chính thức của Topview (tisa_web_search), lấy khóa ở trang quản trị của họ rồi dán kín.
