# Kinh nghiệm đã làm thật (nạp dần)

Mục tiêu: lần sau làm nhanh và đúng hơn. Mỗi dòng là một điều tái dùng được. Bài học mới của cộng sự tự ghi ở bộ nhớ của Đạt Đấu Nối (mục "Bài học"); điều đáng giữ lâu thì thêm vào đây.

## Trình duyệt và tài khoản
- Trình duyệt TISA nhập từ hồ sơ Chrome thường **không giữ được đăng nhập Google** (Google hủy phiên bị chép), dù có cookie. Tin vào những gì thấy trên trang, không tin cookie. Cần Google thì nhờ anh đăng nhập một lần trong đúng hồ sơ.
- Chrome không cho biết tab thuộc hồ sơ nào: chỉ tin tab do TISA tự mở bằng đúng hồ sơ đã chọn. Mở Chrome mới hoặc hồ sơ khác là làm sai ý anh.
- Trang nền tảng thường có tab mở sẵn và đã đăng nhập: `tisa_browser_look op=tabs` trước, `switch_tab` dùng lại, không mở mới.

## Google
- Màn hình đồng ý OAuth ở chế độ **Testing**: token làm mới chỉ sống 7 ngày. Dùng lâu thì chuyển sang In production (ứng dụng nội bộ cá nhân không cần xác minh nếu chỉ chủ dùng, Google vẫn cảnh báo "chưa được xác minh": bấm Nâng cao rồi Tiếp tục).
- Phải thêm email của anh vào **người dùng thử** khi ở Testing, nếu không báo lỗi 403 access_denied.
- OAuth client cho TISA BOT chọn loại **Desktop app**. Bật đúng API (Drive, Gmail, Sheets...) trong cùng dự án trước khi đăng nhập.
- Tài khoản mới tạo Google Cloud lần đầu phải **đồng ý Điều khoản Google Cloud** (tick "I agree", để trống ô Email updates) trước khi tạo được dự án hay client.

## Cloudflare
- Đăng nhập `wrangler login` (OAuth) **không có quyền sửa DNS**. Sửa DNS thì làm trên dashboard hoặc dùng API token riêng có quyền Zone DNS Edit.
- Build web Vite/React: giữ `emptyOutDir: false` khi deploy lại để người đang mở trang không bị trắng trang do file cũ bị xóa.
- Cron mới deploy có thể chạy trễ vài phút đầu; đừng vội kết luận lỗi.
- Sau khi deploy luôn mở địa chỉ thật và kiểm một trang con, rồi mới báo xong.

## MCP
- `claude mcp list` có kiểm sức khỏe nên chậm, chạy nền. Trạng thái "Needs authentication" nghĩa là cần đăng nhập lại ở Claude Code, không phải hỏng.
- MCP của Claude Code chỉ dùng được khi TISA BOT chạy bằng engine Claude.
- Meta Ads MCP chính chủ nối bằng đăng nhập OAuth; tạo chiến dịch luôn để trạng thái tạm dừng rồi hỏi anh trước khi bật.

## Trạng thái người thật
- Hộp "Cho phép" của Google, Touch ID, màn hình khóa, OTP, CAPTCHA: không vượt. Nói đúng một việc anh cần làm rồi chờ và tự làm tiếp.

## Meta / Fanpage (hộp Kết nối Meta, 19/11/2026)
- Hộp có hai ô quyền thêm: "Nối cả Instagram của Trang" (instagram_basic, instagram_manage_messages, instagram_manage_comments) và "Đọc số liệu bài viết" (read_insights). App Meta tạo theo hướng dẫn chỉ có Messenger và 4 quyền Trang, nên **để trống hai ô khi nối lần đầu**. Tick mà app chưa có quyền thì Facebook báo "Invalid Scopes: read_insights" và từ chối cả lần đăng nhập (trang lỗi chỉ hiện cho chủ app). Nhắn tin, bình luận, đăng bài không cần hai ô này.
- Muốn dùng sau: thêm quyền vào app Meta trước, rồi ở Trang đã nối bấm **Đổi token**, tick ô, đăng nhập Facebook lại, đọc bảng kiểm tra.
- Facebook chỉ nhận địa chỉ quay về **https**. Nút Đăng nhập Facebook xám = TISA BOT đang mở bằng http mà chưa có địa chỉ https. Bật Truy cập từ xa (đường hầm) hoặc dùng tên miền riêng đã nối. Đường hầm nhanh đổi địa chỉ mỗi lần khởi động lại: dán lại Địa chỉ quay về vào Meta.
- Sau một lần đăng nhập Facebook hỏng, trang không quay về TISA BOT. Đóng tab lỗi, bỏ tick quyền thêm, bấm Đăng nhập Facebook lại (nút tự mở lại sau 45 giây).
- App chế độ Phát triển: chỉ quản trị viên, nhà phát triển, người thử nghiệm nhắn được. Chuyển Live phải hỏi anh. Sau khi nối nhớ vào Chatbot > Bot, tick kênh vào một bot và bật bot, nếu không bot im lặng.
- Nối xong luôn bấm Kiểm tra ở Trang và báo theo bảng kiểm tra, không báo xong khi chưa thấy dòng nhắn tin và bình luận xanh.
