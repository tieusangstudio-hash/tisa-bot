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
