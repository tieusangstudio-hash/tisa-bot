# TISA BOT

Bộ công cụ AI Agent của **Học Viện TISA**, cài một lần là có đủ:

- **TISA BOT**: trợ lý AI chạy trên máy bạn, có bộ não, tệp tin, kênh chat, việc định kỳ.
- **Kỹ năng `/ts-`**: cài sẵn cho TISA BOT và Claude Code (gõ `/ts-` để thấy).

## Cài đặt

| Máy | Cách cài |
|---|---|
| **Windows 10/11** | Tải [TISA-BOT-Setup.exe](https://github.com/tieusangstudio-hash/tisa-bot/releases/download/desktop/TISA-BOT-Setup.exe), bấm đúp, bấm Next tới hết |
| **macOS 11 trở lên** | Mở Terminal, dán dòng dưới rồi Enter |

```bash
curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/get-tisa-bot.sh | bash
```

## Cài bằng Claude Code

Đã đăng nhập Claude Code thì chỉ cần dán đúng một câu (Mac hay Windows đều được, Claude tự nhận ra máy):

> Cài TISA BOT và 53 skill trên máy này theo đúng hướng dẫn tại https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/docs/CAI-DAT-HOC-VIEN.md

Claude Code tự cài TISA BOT, 53 skill, kết nối Claude, tự xử lý lỗi, kiểm tra lại rồi báo link đăng nhập, tài khoản và đề nghị khởi động lại máy. Xem [docs/CAI-DAT-HOC-VIEN.md](docs/CAI-DAT-HOC-VIEN.md).

### Lệnh cho Claude Code

Cài bằng đúng một lệnh dưới đây theo hệ điều hành của máy, không cần clone repo. Lệnh này tự tải bộ cài và các phần đi kèm, rồi đặt TISA BOT tự chạy khi mở máy.

Lệnh chạy 10 đến 20 phút nên cần chạy nền, không đặt giới hạn thời gian ngắn. Chạy lại an toàn, bước đã xong được bỏ qua.

- macOS: `curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/cai-tisa-bot-day-du.sh | bash`
- Windows: `powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows/cai-tisa-bot-day-du.ps1 | iex"`

Hai lệnh trên cài TISA BOT rồi cài luôn 53 skill của kho [tisa-skills](https://github.com/tieusangstudio-hash/tisa-skills) vào `~/.claude/skills`, cuối cùng in link đăng nhập và tài khoản. Chỉ cần TISA BOT (không cần skill) thì dùng `get-tisa-bot.sh` / `get-tisa-bot.ps1` cùng thư mục.

macOS có thể hiện hộp thoại Command Line Tools: nhắc người dùng bấm Install. Cài xong báo người dùng mở http://127.0.0.1:7777 (tài khoản admin, mật khẩu 123456), và mở lại Claude Code một lần để thấy các lệnh `/ts-`. Máy đã đăng nhập Claude thì không phải đăng nhập lại. Nhắc người dùng vào trang Models, bấm "Chuyển sang token dài hạn" (dùng 1 năm) để tắt mở máy không bị văng kết nối Claude, và khởi động lại máy một lần.

Mật khẩu `123456` chỉ để đăng nhập lần đầu, người dùng nên đổi ngay trong Cài đặt.

Hướng dẫn từng bước: [QUICKSTART.md](QUICKSTART.md). Ghi nguồn và giấy phép: [NOTICE.md](NOTICE.md).
