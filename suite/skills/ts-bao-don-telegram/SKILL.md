---
name: ts-bao-don-telegram
description: "Gọi bằng /ts-bao-don-telegram. Cài để có đơn, có tiền vào, có khách để lại thông tin là điện thoại báo ngay qua Telegram: tạo bot bằng BotFather, lấy Chat ID, nối với SePay (không cần code) hoặc qua webhook trên trang Vercel; tùy chọn gửi email xác nhận cho khách bằng Resend. Có mẫu tin nhắn tiếng Việt. Từ khóa: báo đơn Telegram, thông báo có tiền vào, bot Telegram, BotFather, chat ID, webhook SePay, báo lead, email xác nhận đơn."
---

# /ts-bao-don-telegram — Có đơn là báo về Telegram

> Khách chuyển khoản hoặc để lại thông tin → điện thoại bạn "ting" một tin Telegram ghi rõ số tiền, nội dung,
> mã đơn. Không phải ngồi mở app ngân hàng kiểm tra. AI làm phần kỹ thuật, bạn chỉ tạo bot và bấm vài nút.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Đã cài nhận tiền qua SePay, muốn **có tiền vào là báo ngay** về điện thoại (hoặc nhóm nhân viên).
- Có form đăng ký/để lại số điện thoại trên trang, muốn **có lead là báo**.
- Muốn cả nhóm bán hàng cùng thấy đơn mới trong 1 nhóm Telegram.
- Muốn khách nhận **email xác nhận đơn** tự động (Resend).
- Bot đang chạy thì im lặng, cần tìm lỗi.

**Không dùng khi:** chưa cài nhận tiền → `/ts-cai-thanh-toan`; muốn tự **gửi sản phẩm** cho khách sau khi trả tiền →
`/ts-giao-hang-tu-dong`; muốn nhắn tin chăm sóc khách qua Zalo → `/ts-cham-soc-khach-zalo`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Hỏi rõ (1 lượt)
Theo `references/_chung/clarification-gate.md`:
1. Báo khi nào? A. Có tiền vào tài khoản (SePay) · B. Khách điền form trên trang · C. Cả hai.
2. Báo cho ai? A. Chỉ mình tôi (chat riêng) · B. Một nhóm Telegram (nhân viên cùng xem).
3. Đã có tài khoản SePay đã liên kết ngân hàng chưa? Trang đã ở trên Vercel chưa (link)?
4. Có muốn gửi email xác nhận cho khách không? (cần Resend + tên miền riêng — có thể làm sau)
5. Máy dùng macOS hay Windows? Đã cài Telegram trên điện thoại chưa?

### Bước 2 — Chọn cách nối
| Cách | Khi nào | Cần code? | Ghi chú |
|---|---|---|---|
| **A. SePay → Telegram có sẵn** | Chỉ cần báo có tiền vào | Không | Nhanh nhất. Menu **Tích hợp Telegram** trên my.sepay.vn, bot của SePay gửi vào nhóm |
| **B. Bot riêng + webhook trên Vercel** | Muốn tin nhắn theo mẫu riêng, ghép thêm việc (giao hàng, ghi sổ) | AI viết sẵn | Dùng `templates/api/sepay-webhook.js` |
| **C. Form → Telegram** | Báo lead từ form | AI viết sẵn | Form gửi về hàm API trên Vercel hoặc dịch vụ form có tích hợp Telegram |

Mặc định đề xuất **A** cho người mới; cần tùy biến mới dùng **B**. Kiến trúc chi tiết, chống trùng, thử lại:
`references/webhook-to-notification-pipeline.md`. Tài liệu chính thức (đọc trước khi làm thật — giao diện có thể đổi):
`references/official-docs-index.md`, SePay: `https://docs.sepay.vn/tich-hop-telegram.html`, `https://docs.sepay.vn/tich-hop-webhooks.html`.

### Bước 3 — Tạo bot & lấy Chat ID (cách B, C; cách A chỉ cần nhóm)
- Học viên tạo bot bằng **@BotFather** (các bước ở mục Hướng dẫn). Token dạng `123456789:ABCdef…` là **bí mật** —
  **không** để học viên dán vào chat; hướng dẫn đặt vào biến môi trường hoặc ô Environment Variables trên Vercel.
- Lấy Chat ID: học viên nhắn 1 tin cho bot (hoặc trong nhóm có bot), rồi chạy
  `scripts/thu_telegram.py tim-chat-id` (lệnh ở Bước 5). Chat cá nhân là số dương; **nhóm là số âm, thường bắt đầu `-100`**.
  Cách khác: mở `https://web.telegram.org`, vào nhóm, xem số trên thanh địa chỉ; hoặc dùng @userinfobot cho ID cá nhân.
- Nhóm: thêm bot vào nhóm (… → **Add Members** → tìm tên bot). Bot không nhận được tin trong nhóm → đặt bot làm quản trị viên.

### Bước 4 — Nối nguồn báo
**Cách A — SePay có sẵn:** my.sepay.vn → **Tích hợp Telegram** → làm theo 4 bước của SePay: (1) Kết nối — tạo nhóm,
thêm bot của SePay theo hướng dẫn trên màn hình, nhập ID nhóm, bấm kiểm tra kết nối · (2) Chọn tài khoản ngân hàng,
**Sự kiện = Có tiền vào**, điều kiện lọc (nếu cần) · (3) Sửa mẫu "Nội dung chat Telegram" · (4) Thử bằng giao dịch nhỏ.

**Cách B — webhook riêng trên Vercel:**
1. Chép `templates/api/sepay-webhook.js` vào thư mục trang thành `api/sepay-webhook.js` (cạnh `index.html`).
2. Vercel → Project → **Settings → Environment Variables**, thêm: `SEPAY_WEBHOOK_APIKEY` (chuỗi bí mật ngẫu nhiên, AI tạo
   giúp), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` → đưa trang lên lại bằng `/ts-dua-web-len-mang`.
3. my.sepay.vn → **Webhooks** → **+ Thêm webhook**: đặt tên · sự kiện **Có tiền vào** · URL
   `https://<ten-trang>.vercel.app/api/sepay-webhook` · chọn tài khoản ngân hàng · bảo mật **API Key** (dán đúng
   `SEPAY_WEBHOOK_APIKEY`) → **Thêm**. SePay gửi header `Authorization: Apikey <khóa>`.
4. Quy tắc SePay: webhook coi là thành công khi trả **HTTP 200/201 + JSON `{"success": true}` trong 30 giây**; lỗi sẽ
   gửi lại tối đa 7 lần → file mẫu đã xử lý. Muốn chặt hơn có thể chọn HMAC-SHA256 (xem tài liệu SePay).

**Cách C — form:** form trên trang gửi `POST` về một hàm API trên Vercel (giống cách B) để gửi Telegram; token để trong
biến môi trường, **không bao giờ đặt token trong file HTML**.

### Bước 5 — Soạn tin nhắn & thử
- Mẫu tin tiếng Việt (đơn mới, đã thanh toán, chờ thanh toán, đã giao, tổng kết ngày, lead mới):
  `references/notification-message-templates.md`. Tin ngắn, dòng đầu có biểu tượng + loại sự kiện, số tiền in đậm.
- Gửi tin thử (học viên tự chạy hoặc AI chạy khi có quyền; token đặt bằng biến môi trường):
```
macOS (Terminal):
  export TELEGRAM_BOT_TOKEN="dán-token"
  python3 scripts/thu_telegram.py tim-chat-id
  export TELEGRAM_CHAT_ID="số-vừa-tìm"
  python3 scripts/thu_telegram.py gui-thu

Windows (PowerShell):
  $env:TELEGRAM_BOT_TOKEN="dán-token"
  py scripts\thu_telegram.py tim-chat-id
  $env:TELEGRAM_CHAT_ID="số-vừa-tìm"
  py scripts\thu_telegram.py gui-thu
```
- Thử thật: chuyển khoản **2.000đ** vào tài khoản đã liên kết SePay → tin báo đến trong vài giây.
  SePay → **Giao dịch** cho xem lịch sử gửi; webhook có thống kê gửi thành công/thất bại.

### Bước 6 — (Tùy chọn) Email xác nhận cho khách bằng Resend
Telegram báo **chủ shop**; Resend gửi email cho **khách**. Cần: tài khoản Resend, khóa API (đặt ở biến môi trường
`RESEND_API_KEY`), **tên miền riêng đã xác minh** (để không vào thư rác), form thu email khách. Mẫu email + các bước:
`references/resend-email-confirmation.md`; xác minh tên miền (SPF/DKIM/DMARC): `references/resend-deliverability.md`
và `references/_chung/dns-basics-for-nontech.md`.

### Bước 7 — Báo kết quả (CỔNG DUYỆT)
Trình: cách đã nối · nơi nhận (cá nhân/nhóm, tên nhóm) · ảnh chụp tin thử đã đến · mẫu tin đang dùng · việc còn lại.
> "Tin thử đã đến điện thoại chưa? Gõ **duyệt** để lưu cấu hình vào Bộ Não."

**Lỗi thường gặp:**
| Hiện tượng | Cách sửa |
|---|---|
| Lỗi 401 | Token sai/đã thu hồi → @BotFather → `/mybots` → chọn bot → **API Token** (hoặc `/revoke` để cấp mới) |
| Lỗi 400 "chat not found" | Sai Chat ID hoặc chưa nhắn cho bot lần nào; nhóm phải có dấu `-` |
| Lỗi 403 | Bot bị chặn hoặc bị xóa khỏi nhóm → thêm lại |
| Có tiền mà không báo | Webhook sai URL/khóa, trang chưa đưa lên lại sau khi thêm biến → xem nhật ký trên SePay và Vercel (Logs) |
| Báo 2 lần | SePay gửi lại do không nhận `{"success": true}` kịp → kiểm tra hàm trả về đúng và nhanh |
| Email vào thư rác | Tên miền chưa xác minh trên Resend |

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** điện thoại có app Telegram (tải trên App Store / CH Play, đăng ký bằng số điện thoại), tài khoản SePay đã
liên kết ngân hàng (chưa có → chạy `/ts-cai-thanh-toan` trước).

**1. Tạo bot (3 phút)**
- Trong Telegram, bấm ô tìm kiếm → gõ `BotFather` → chọn tài khoản **@BotFather** có dấu tích xanh → bấm **Start**.
- Gõ `/newbot` → gửi.
- BotFather hỏi tên hiển thị → gõ vd `Báo đơn Tiệm Mây` → gửi.
- BotFather hỏi username → gõ tên **không dấu, kết thúc bằng `bot`**, vd `tiemmay_baodon_bot` (trùng thì thêm số).
- BotFather trả về tin có dòng token dạng `123456789:ABC...` → bấm giữ để **sao chép**, cất vào ghi chú riêng tư.
  **Không dán token vào khung chat với AI.**

**2. Tạo nhóm nhận báo (nếu muốn nhân viên cùng xem)**
- Telegram → biểu tượng bút chì/**New Group** → đặt tên vd `Đơn hàng Tiệm Mây` → thêm nhân viên.
- Mở nhóm → bấm tên nhóm → **Add Members** → tìm username bot vừa tạo → thêm. Nhắn 1 tin bất kỳ trong nhóm.
- Chỉ báo cho riêng bạn: mở chat với bot → bấm **Start** → nhắn "xin chào".

**3. Đưa token cho AI một cách an toàn**
- Cách B: vào Vercel → dự án → **Settings → Environment Variables** → bấm **Add** → Key `TELEGRAM_BOT_TOKEN`, Value dán token →
  **Save**. AI sẽ chỉ bạn thêm `TELEGRAM_CHAT_ID` và `SEPAY_WEBHOOK_APIKEY` y như vậy.
- Chạy lệnh thử: mở **Terminal** (macOS: Cmd+Space gõ "Terminal") hoặc **PowerShell** (Windows: bấm Start gõ "PowerShell"),
  dán từng dòng AI đưa (ở Bước 5), thay `dán-token` bằng token của bạn.

**4. Nối với SePay**
- Không cần code (cách A): đăng nhập `my.sepay.vn` → menu **Tích hợp Telegram** → làm theo 4 bước trên màn hình.
- Cách B: `my.sepay.vn` → **Webhooks** → **+ Thêm webhook** → điền đúng URL và khóa AI đưa → bấm **Thêm**.

**5. Thử:** chuyển khoản 2.000đ vào tài khoản của bạn với nội dung AI đưa → điện thoại báo trong vài giây. Chụp màn hình gửi AI.

**6. Gõ "duyệt"** để lưu cấu hình (không lưu token) vào Bộ Não.

## Câu lệnh mẫu
- `/ts-bao-don-telegram có tiền vào tài khoản SePay thì báo vào nhóm Telegram 'Đơn hàng' của shop, không cần code.`
- `/ts-bao-don-telegram trang khóa học trên Vercel, có người đăng ký học thử thì báo Telegram cho tôi kèm số điện thoại.`
- `/ts-bao-don-telegram spa Hồng muốn khách chuyển cọc là nhắn nhóm lễ tân, và gửi email xác nhận cho khách.`
- `/ts-bao-don-telegram bot báo đơn hôm qua tự nhiên im lặng, kiểm tra giúp tôi.`

## Kết quả nhận được
- Bot Telegram đã tạo + nơi nhận (cá nhân/nhóm) + Chat ID đã kiểm tra.
- Kết nối SePay → Telegram (cách A) hoặc file `api/sepay-webhook.js` + danh sách biến môi trường cần đặt (cách B).
- Mẫu tin nhắn tiếng Việt đã chọn, tin thử đã đến điện thoại.
- (Tùy chọn) email xác nhận cho khách qua Resend.
- Bảng xử lý lỗi để tự kiểm tra lần sau.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-bao-don-telegram-<chu-de-khong-dau>/`.
2. Lưu cấu hình đã cài thành `ket-qua.md` (cách nối A/B/C, tên bot `@…`, tên nhóm và Chat ID, tên webhook và URL trên SePay,
   tên các biến môi trường đã đặt — **chỉ tên, không giá trị**, mẫu tin đang dùng, ngày thử thành công), mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-bao-don-telegram
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `mau-tin-nhan.md`, `sepay-webhook.js` đã dùng (không chứa token).
   **Tuyệt đối không lưu** token bot, khóa webhook, khóa API Resend, mật khẩu.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-bao-don-telegram · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Token bot, khóa webhook, khóa API là bí mật** — không xin dán vào chat, không ghi vào file HTML, không lưu Bộ Não,
  không chụp màn hình gửi người khác. Lộ token → @BotFather `/revoke` lấy token mới, cập nhật lại Vercel.
- Webhook luôn có kiểm tra khóa (API Key hoặc HMAC) để người lạ không gửi "báo đơn giả".
- Tin báo Telegram **chỉ là thông báo** — trước khi giao hàng giá trị lớn, đối chiếu lại số dư trong app ngân hàng.
- Nhóm báo đơn có số điện thoại, tên khách → chỉ thêm người cần thiết; nhân viên nghỉ việc thì xóa khỏi nhóm.
- Gửi email cho khách: chỉ email giao dịch (xác nhận đơn), không gửi quảng cáo khi khách chưa đồng ý.

## Skill liên quan
- Trước: `/ts-cai-thanh-toan` · `/ts-gan-ma-qr` · `/ts-dua-web-len-mang`
- Sau: `/ts-giao-hang-tu-dong` · `/ts-phan-tich-doanh-thu` · `/ts-cham-soc-khach-zalo`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
