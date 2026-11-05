# TISA BOT

Bộ công cụ AI Agent của **Học Viện TISA**, cài một lần là có đủ:

- **TISA BOT**: trợ lý AI chạy trên máy bạn, có bộ não, tệp tin, kênh chat, việc định kỳ.
- **Đội Quân AI**: bảng giao việc với 17 nhân sự AI trong 12 phòng ban.
- **52 kỹ năng `/ts-`**: đã phân sẵn cho từng nhân sự, dùng được cả trong Claude.

## Cài đặt

| Máy | Cách cài |
|---|---|
| **Windows 10/11** | Tải [TISA-BOT-Setup.exe](https://github.com/tieusangstudio-hash/tisa-bot/releases/download/desktop/TISA-BOT-Setup.exe), bấm đúp, bấm Next tới hết |
| **macOS 11 trở lên** | Mở Terminal, dán dòng dưới rồi Enter |

```bash
curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/get-tisa-bot.sh | bash
```

## Cài bằng Claude Code

Đã đăng nhập Claude Code thì chỉ cần dán câu này:

> Cài giúp tôi TISA BOT từ link này: https://github.com/tieusangstudio-hash/tisa-bot

### Lệnh cho Claude Code

Cài bằng đúng một lệnh dưới đây theo hệ điều hành của máy, không cần clone repo. Lệnh này tự tải bộ cài và các phần đi kèm, rồi đặt TISA BOT tự chạy khi mở máy.

Lệnh chạy 10 đến 20 phút nên cần chạy nền, không đặt giới hạn thời gian ngắn. Chạy lại an toàn, bước đã xong được bỏ qua.

- macOS: `curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/get-tisa-bot.sh | bash`
- Windows: `powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:TISA_SILENT='1'; irm https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows/get-tisa-bot.ps1 | iex"`

macOS có thể hiện hộp thoại Command Line Tools: nhắc người dùng bấm Install. Cài xong báo người dùng mở http://127.0.0.1:7777 (tài khoản admin, mật khẩu 123456), bấm Đội Quân AI ở thanh bên, và khởi động lại Claude một lần để nhận công cụ `doi-quan-ai`. Máy đã đăng nhập Claude thì không phải đăng nhập lại.

Mật khẩu `123456` chỉ để đăng nhập lần đầu, người dùng nên đổi ngay trong Cài đặt.

Hướng dẫn từng bước: [QUICKSTART.md](QUICKSTART.md). Ghi nguồn và giấy phép: [NOTICE.md](NOTICE.md).
