# Lấy khóa YouTube API miễn phí (từng bước, khoảng 10 phút)

Dùng cho `/ts-nghien-cuu-youtube`. Khóa API (API key) là một chuỗi ký tự giúp script hỏi YouTube
số liệu thật (view, số người đăng ký, like, bình luận). **Miễn phí**, không cần thẻ thanh toán cho
mức dùng này. Hạn mức: 10.000 đơn vị/ngày ≈ 90 từ khóa/ngày.

> Giao diện Google có thể thay đổi tên nút một chút theo thời gian. Nếu không thấy đúng chữ,
> tìm nút có ý nghĩa tương tự hoặc gõ tên vào ô tìm kiếm trên cùng của trang.

## Chuẩn bị
- Một tài khoản Gmail (nên dùng Gmail công việc, không dùng Gmail chứa dữ liệu quan trọng).
- Máy tính có trình duyệt Chrome/Edge/Safari.

## Các bước

**Bước 1 — Mở Google Cloud Console**
Vào `https://console.cloud.google.com` → đăng nhập Gmail → nếu hiện bảng điều khoản, tick đồng ý → bấm **Agree and continue** (Đồng ý và tiếp tục).

**Bước 2 — Tạo dự án mới**
- Bấm ô chọn dự án ở góc trên bên trái (cạnh chữ "Google Cloud").
- Bấm **New Project** (Dự án mới).
- Đặt tên, ví dụ `nghien-cuu-youtube` → bấm **Create** (Tạo). Chờ 10–20 giây.
- Bấm lại ô chọn dự án, chọn đúng dự án vừa tạo.

**Bước 3 — Bật YouTube Data API v3**
- Ở ô tìm kiếm trên cùng, gõ `YouTube Data API v3` → chọn kết quả có biểu tượng API.
- Bấm nút **Enable** (Bật). Chờ trang tải xong.

**Bước 4 — Tạo khóa API**
- Bấm menu ☰ góc trái → **APIs & Services** (API và dịch vụ) → **Credentials** (Thông tin xác thực).
- Bấm **+ Create credentials** (Tạo thông tin xác thực) → chọn **API key** (Khóa API).
- Một bảng hiện ra chứa khóa (dạng `AIza...` dài khoảng 39 ký tự) → bấm biểu tượng sao chép.

**Bước 5 — Giới hạn khóa (an toàn, nên làm)**
- Trong danh sách khóa, bấm tên khóa vừa tạo (hoặc **Edit API key**).
- Mục **API restrictions** (Giới hạn API) → chọn **Restrict key** (Giới hạn khóa) → tick **YouTube Data API v3** → bấm **Save** (Lưu).
- Như vậy nếu lộ khóa, người khác cũng chỉ dùng được cho YouTube, không dùng được dịch vụ tính tiền khác.

**Bước 6 — Đưa khóa cho script dùng** (chọn 1 cách)

*Cách dễ nhất:* khi AI hỏi, **không dán khóa vào khung chat**. Thay vào đó, tự gõ lệnh trên máy mình:

macOS (ứng dụng Terminal):
```bash
export YOUTUBE_API_KEY="dán-khóa-vào-đây"
python3 scripts/yt_tim_video.py --q "từ khóa của bạn" --min-views 10000
```

Windows (Command Prompt):
```bat
set YOUTUBE_API_KEY=dán-khóa-vào-đây
py scripts\yt_tim_video.py --q "từ khóa của bạn" --min-views 10000
```

Windows (PowerShell):
```powershell
$env:YOUTUBE_API_KEY="dán-khóa-vào-đây"
py scripts\yt_tim_video.py --q "từ khóa của bạn" --min-views 10000
```

Lệnh `export`/`set` chỉ có tác dụng trong cửa sổ đang mở. Đóng cửa sổ thì phải gõ lại.

*Nếu dùng AI có quyền chạy lệnh trên máy bạn (Claude Code, Cowork, Codex…):* bạn đặt biến môi trường
như trên trước khi mở AI, hoặc lưu khóa vào một file `.env` trong thư mục làm việc và chỉ nói với AI
"khóa nằm trong file .env". Không dán khóa vào chat.

## Lỗi thường gặp

| Thông báo | Nguyên nhân | Cách sửa |
|---|---|---|
| Khóa API không đúng | Chép thiếu/thừa ký tự | Sao chép lại bằng nút sao chép |
| Khóa bị từ chối (403) | Chưa bật YouTube Data API v3, hoặc chọn sai dự án | Làm lại Bước 3 với đúng dự án |
| Đã hết hạn mức | Dùng quá 10.000 đơn vị/ngày | Chờ tới khoảng 14h–15h chiều (giờ Việt Nam) hôm sau, hoặc dùng `--tu-file` với dữ liệu đã lưu |
| Không kết nối được mạng | Mất mạng, mạng công ty chặn | Kiểm tra Internet, thử mạng khác |

## An toàn
- Khóa API giống chìa khóa nhà: **không đăng lên mạng, không gửi vào nhóm, không dán vào khung chat AI.**
- Nghi bị lộ → vào **Credentials**, bấm khóa đó → **Regenerate key** (tạo lại) hoặc xóa, rồi tạo khóa mới.
- Không bao giờ lưu khóa vào Bộ Não Thứ 2.

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
