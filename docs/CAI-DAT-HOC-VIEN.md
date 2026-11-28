# Cài TISA BOT + 53 skill trên máy học viên (hướng dẫn cho Claude Code)

Trang này dành cho Claude Code. Nhân viên chỉ dán vào Claude Code đúng một câu:

> Cài TISA BOT và 53 skill trên máy này theo đúng hướng dẫn tại https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/docs/CAI-DAT-HOC-VIEN.md

Claude Code tự nhận ra máy Mac hay Windows, tự chạy, tự xử lý lỗi, chỉ nhờ người dùng ở những chỗ hệ điều hành bắt buộc người thật bấm.

## 1. Nhận ra máy

Chạy `uname -s`. Ra `Darwin` là **macOS**. Ra `MINGW…`, `MSYS…`, `CYGWIN…` hoặc lệnh không có là **Windows**.

## 2. Chạy đúng MỘT lệnh

Lệnh chạy 10 đến 20 phút: chạy NỀN, không đặt giới hạn thời gian ngắn, theo dõi đầu ra tới khi xong. Chạy lại bao nhiêu lần cũng an toàn, bước đã xong được bỏ qua, dữ liệu cũ giữ nguyên.

- **macOS:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/cai-tisa-bot-day-du.sh | bash
  ```
- **Windows:**
  ```bash
  powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows/cai-tisa-bot-day-du.ps1 | iex"
  ```

Lệnh tự làm 4 bước: cài TISA BOT (Git, Python, Node, Claude CLI, tự chạy cùng máy), chép 53 skill vào `~/.claude/skills`, kết nối Claude (máy đã đăng nhập Claude Code thì dùng chung), chờ TISA BOT lên (chưa lên thì tự chạy lại và in nhật ký).

## 3. Những chỗ phải nhờ người dùng bấm (hệ điều hành không cho phần mềm tự bấm)

Khi đầu ra tới các chỗ này, nói ngắn gọn bằng tiếng Việt cho người dùng biết phải bấm gì, rồi chờ tiếp:

| Thấy gì | Nói với người dùng |
|---|---|
| macOS: dòng "Command Line Tools" | "Máy vừa hiện hộp Cài Command Line Tools, anh/chị bấm **Install** (Cài đặt) rồi chờ 5 đến 15 phút." |
| Windows: hộp "Bạn có muốn cho phép ứng dụng này thay đổi thiết bị?" | "Bấm **Yes** (Có) trên hộp Windows vừa hiện." |
| "Trinh duyet se mo trang dang nhap Claude" | "Trình duyệt vừa mở trang Claude, anh/chị đăng nhập rồi bấm **Authorize**." |

Không tự gõ mật khẩu, không tự bấm thay các hộp đó, không tắt tính năng bảo mật nào của máy.

## 4. Gặp lỗi thì tự xử lý

Đọc dòng `[LOI]` hoặc `[!]` trong đầu ra rồi sửa và chạy lại đúng lệnh ở bước 2:

- **Mạng chập chờn, tải lỗi:** chờ 30 giây, chạy lại, tối đa 3 lần.
- **"Thu muc ~/TISABot da co file nhung khong phai ban TISA BOT":** KHÔNG xóa. Hỏi người dùng có được đổi tên thư mục đó thành `TISABot-cu` không; đồng ý thì đổi tên rồi chạy lại.
- **TISA BOT chưa lên:** đọc 25 dòng nhật ký lệnh đã in, sửa theo lỗi (thiếu thư viện thì chạy lại lệnh cài; cổng 7777 bận thì báo người dùng tiến trình nào đang giữ cổng).
- **Lỗi khác:** đọc kỹ, tự tìm cách sửa trên máy; chỉ hỏi người dùng khi cách sửa có thể làm mất dữ liệu.

## 5. Kiểm tra trước khi báo xong

1. Mở được `http://127.0.0.1:7777` (macOS: `curl -fsS -o /dev/null http://127.0.0.1:7777/`; Windows: `curl.exe` hoặc `Invoke-WebRequest`).
2. Có đủ skill: đếm thư mục `ts-*` trong `~/.claude/skills` (Windows: `%USERPROFILE%\.claude\skills`), phải từ 53 trở lên.
3. Claude đã kết nối: `claude auth status --json` có `"loggedIn": true`.

Mục nào chưa đạt thì sửa tiếp theo bước 4, đừng báo xong.

## 6. Báo cho người dùng (tiếng Việt, ngắn gọn)

- **Link đăng nhập:** `http://127.0.0.1:7777` (hoặc `http://localhost:7777`). TISA BOT chỉ mở cho chính máy này; muốn dùng từ máy khác hay điện thoại thì vào trang **Truy cập từ xa** trong TISA BOT.
- **Tài khoản:** lấy đúng tên và mật khẩu ở khung cuối của lệnh (mặc định `admin` / `123456`). Nhắc đổi mật khẩu ở trang **Tài khoản**.
- Số skill đã cài, và Claude đã kết nối hay chưa.
- Nhắc: vào trang **Models**, bấm **"Chuyển sang token dài hạn"** (dùng 1 năm, tắt mở máy không bị văng kết nối Claude).
- Lần đầu TISA BOT muốn điều khiển máy, macOS sẽ hỏi quyền Trợ năng và Ghi màn hình: bấm **Cho phép** / bật công tắc là xong, TISA BOT tự hướng dẫn từng bước.

## 7. Đề nghị khởi động lại máy

Hỏi: "Khởi động lại máy một lần để TISA BOT tự chạy cùng máy và Claude Code nhận đủ skill nhé?" Người dùng đồng ý thì nhắc lưu việc đang dở, rồi chạy:

- macOS: `osascript -e 'tell application "System Events" to restart'`
- Windows: `shutdown /r /t 30`

Người dùng chưa muốn thì dặn: lần sau mở máy TISA BOT tự chạy, mở lại Claude Code là thấy skill (gõ `/ts-`).
