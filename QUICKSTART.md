# Cài TISA BOT từng bước

Cần: máy Windows 10/11 hoặc macOS 11 trở lên, mạng ổn định, tài khoản Claude (gói trả phí). Thời gian: 10 đến 20 phút, chủ yếu là chờ tải.

## 1. Cài

**Windows:** tải [TISA-BOT-Setup.exe](https://github.com/tieusangstudio-hash/tisa-bot/releases/download/desktop/TISA-BOT-Setup.exe), bấm đúp. Nếu Windows hiện "Windows protected your PC", bấm **More info** rồi **Run anyway**. Bấm Next tới hết, một cửa sổ đen hiện tiến trình cài, đừng tắt.

**macOS:** mở ứng dụng **Terminal**, dán dòng này rồi Enter:

```bash
curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/get-tisa-bot.sh | bash
```

macOS có thể hỏi cài Command Line Tools (bấm **Install**) và mật khẩu máy Mac một lần.

Xong sẽ có biểu tượng **TISA BOT** trên Desktop (Windows) hoặc Applications (macOS), máy khởi động là TISA BOT tự chạy.

## 2. Đăng nhập TISA BOT

Sau khi cài, TISA BOT chạy ngay trên máy bạn, chỉ máy này mở được, chưa cần tên miền:

| Công cụ | Địa chỉ |
|---|---|
| TISA BOT | <http://127.0.0.1:7777> |
| Đội Quân AI | <http://127.0.0.1:7788> (mở trên chính máy này thì tự vào) |

Tài khoản mặc định: tên đăng nhập **admin**, mật khẩu **123456**.

**Đổi mật khẩu trước khi gắn tên miền hoặc bật truy cập từ xa.** Mật khẩu mặc định ai cũng biết, mà TISA BOT có toàn quyền trên máy của bạn.

## 3. Đăng nhập Claude

Vào trang **Models**, bấm đăng nhập Claude rồi cho phép trên trình duyệt.

Từ lúc này mọi kết nối bạn đã bật trong Claude (Google Drive, Gmail, Meta Ads...) và các MCP đã thêm vào Claude Code đều tự có trong TISA BOT và Đội Quân AI, không phải kết nối lại.

## 4. Mở Đội Quân AI

Bấm **Đội Quân AI** ở chân thanh bên trái, hoặc mở <http://127.0.0.1:7788> (mở từ chính máy này thì tự đăng nhập). Gõ thử một việc rồi bấm **Giao việc**. Trạng thái góc dưới phải hiện **TISA BOT đã nối**.

## 5. Dùng trong Claude

Trong Claude Code hoặc tab Code của Claude Desktop, gõ `/ts-` để thấy 52 kỹ năng. Nhờ Claude giao việc cho đội bằng câu tự nhiên, ví dụ "giao cho đội làm kế hoạch nội dung tuần này": Claude dùng công cụ `doi-quan-ai`. Khởi động lại Claude một lần sau khi cài để nó nhận công cụ.

## Khi có bản mới

Biểu tượng chuông báo có bản mới. Vào **Cài đặt > Cập nhật**, bấm **Cập nhật**. TISA BOT, bảng và kỹ năng cùng lên bản mới; bộ não, dữ liệu và những kỹ năng bạn đã tự sửa được giữ nguyên. Cập nhật lỗi thì app tự quay về bản cũ.

## Gặp trục trặc

- Xem tình trạng cài: tệp `.doi-quan-ai/setup-status.json` trong thư mục người dùng.
- Nhật ký: thư mục `.doi-quan-ai/logs/` trong thư mục người dùng.
- Chạy lại bộ cài bao nhiêu lần cũng được, bước đã xong sẽ tự bỏ qua.
