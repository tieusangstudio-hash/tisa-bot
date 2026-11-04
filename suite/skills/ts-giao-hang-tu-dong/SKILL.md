---
name: ts-giao-hang-tu-dong
description: "Gọi bằng /ts-giao-hang-tu-dong. Cài để khách trả tiền xong là tự nhận sản phẩm số (ebook, khóa học, file, link truy cập) trong vài giây qua trang cảm ơn, email (Resend) hoặc Telegram, kèm báo chủ shop; soạn email giao hàng đúng giọng thương hiệu và chuỗi chăm sóc sau mua. Có so sánh cách giao, checklist thử và bảo trì hằng tháng. Từ khóa: giao hàng tự động, gửi sản phẩm sau thanh toán, gửi ebook tự động, email giao khóa học, Resend, giao file tự động, trang cảm ơn."
---

# /ts-giao-hang-tu-dong — Khách trả tiền xong là tự nhận sản phẩm

> Khách chuyển khoản → vài giây sau tự nhận link/tài liệu/khóa học qua trang cảm ơn và email, bạn nhận tin báo
> "đã giao". Không phải thức khuya gửi tay từng đơn. AI lo phần kỹ thuật, bạn chỉ chuẩn bị sản phẩm và bấm vài nút.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Bán sản phẩm số: ebook, khóa học video, mẫu thiết kế, file Excel, mã kích hoạt, vé sự kiện online.
- Đang gửi sản phẩm bằng tay sau khi kiểm tra chuyển khoản, muốn tự động.
- Muốn khách nhận email giao hàng chuyên nghiệp (từ tên miền riêng, không vào thư rác).
- Muốn có chuỗi tin chăm sóc sau mua (hướng dẫn dùng, xin đánh giá, giới thiệu sản phẩm tiếp theo).
- Hệ thống giao hàng đang chạy bỗng lỗi, cần kiểm tra.

**Không dùng khi:** chưa cài nhận tiền → `/ts-cai-thanh-toan`; chỉ cần báo đơn cho chủ shop → `/ts-bao-don-telegram`;
viết chuỗi email nuôi dưỡng dài ngày → `/ts-email-cham-soc`; hàng vật lý cần vận chuyển → skill này không phù hợp.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `giao-hang-tu-dong`, `cai-thanh-toan`, `bao-don-telegram` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Dùng gì từ hồ sơ:** danh mục sản phẩm, giá, gói (`02`) → bảng "gói → sản phẩm giao"; khách là ai, hay vướng gì khi bắt đầu
(`03`) → nội dung hướng dẫn trong email; giọng văn, xưng hô, màu nút (`04`) → email và trang cảm ơn; Zalo/hotline, email,
giờ hỗ trợ (`05`) → dòng hỗ trợ cuối email. Cấu hình thanh toán và bot đã cài: lấy từ `04-ket-qua/…-cai-thanh-toan-…`, `…-bao-don-telegram-…`.

## Quy trình AI thực hiện

### Bước 1 — Hỏi rõ (1–2 lượt)
Theo `references/_chung/clarification-gate.md`. Chỉ hỏi phần còn thiếu:
1. Sản phẩm giao là gì, dạng gì? (file PDF, link video/Drive, khóa học trên nền tảng, mã kích hoạt, nhóm kín)
2. Đã cài nhận tiền tự xác nhận (`/ts-cai-thanh-toan`) chưa? Trang đang ở Vercel hay LadiPage/Canva/WordPress?
3. Giao qua đâu? A. Trang cảm ơn hiện link · B. Email · C. Telegram · D. Kết hợp (khuyên: A + B).
4. Có tên miền riêng chưa (vd `tiembanhmay.vn`)? — cần để gửi email không vào thư rác.
5. Sản phẩm có cần chống chia sẻ link không? (giá cao → nên dùng nền tảng có tài khoản học viên)

### Bước 2 — Chọn cách giao
| Cách | Cài đặt | Chi phí | Hợp với | Lưu ý |
|---|---|---|---|---|
| Trang cảm ơn hiện link | 15 phút | Miễn phí | Mọi sản phẩm số | Khách đóng trang là mất → luôn kèm email |
| **Email (Resend)** | 30 phút | Có gói miễn phí giới hạn | Ebook, file, link khóa học | Cần tên miền đã xác minh; file lớn → gửi link |
| Telegram bot | 45 phút | Miễn phí | Cộng đồng, nhóm kín, khách quen Telegram | Khách phải bấm Start bot trước |
| Nền tảng khóa học có tài khoản | Tùy nền tảng | Theo nền tảng | Khóa học giá cao | Chống chia sẻ tốt nhất |
| Link Google Drive chia sẻ | 5 phút | Miễn phí | Tài liệu giá thấp | Dễ bị chia sẻ lại |

So sánh chi tiết (link có hạn, trang bảo vệ, Drive, Notion…): `references/digital-product-delivery-methods.md`.
Giá/gói Resend và giới hạn gửi: kiểm tra trên trang Resend tại thời điểm cài, không nói theo trí nhớ.
Đọc `references/official-docs-index.md` trước khi đưa bước thật — tài liệu chính thức mới nhất được ưu tiên.

### Bước 3 — Lập bảng "gói → sản phẩm" & soạn nội dung giao (CỔNG DUYỆT 1)
- Bảng: mã gói · tên · giá (khớp QR) · link/tệp giao · hướng dẫn 1–2 câu. Link phải **ổn định, không hết hạn**, đã thử mở
  bằng trình duyệt ẩn danh (Drive: chế độ "Bất kỳ ai có đường liên kết" chỉ xem; hoặc chia sẻ theo email khách).
- Email giao hàng (giọng theo `04-thuong-hieu-noi-dung.md`): tiêu đề rõ ("Sản phẩm của bạn đã sẵn sàng: …") · cảm ơn ·
  mã đơn · **nút mở sản phẩm** · việc đầu tiên nên làm · liên hệ hỗ trợ · gửi từ địa chỉ tên miền riêng.
  Mẫu email/Telegram và chuỗi chăm sóc 6 tin trong 14 ngày: `references/post-purchase-engagement-sequence.md`.
- Trang cảm ơn: "Thanh toán thành công" · nút mở sản phẩm · "Email đã gửi tới …, kiểm tra cả mục Quảng cáo/Spam" · Zalo hỗ trợ.
> "Gõ **duyệt** bảng sản phẩm và nội dung email để mình cài."

### Bước 4 — Cài đặt (AI làm phần kỹ thuật)
**Trang trên Vercel (khuyên dùng):**
1. Thêm ô **Email** (bắt buộc) và **Tên** vào trang thanh toán (mẫu ở `/ts-cai-thanh-toan`).
2. Chép `templates/api/giao-hang.js` thành `api/giao-hang.js`, điền bảng `SAN_PHAM` và `LIEN_HE_HO_TRO`.
3. Khi trang thấy "đã thanh toán": gọi `POST /api/giao-hang` với `{ ma, goi, email, ten }` → hiện link + hướng dẫn trả về
   trên trang cảm ơn. Hàm tự kiểm tra lại với SePay (đủ tiền mới giao), gửi email Resend, báo Telegram "đã giao".
4. Học viên đặt biến môi trường trên Vercel (**Settings → Environment Variables**): `SEPAY_API_TOKEN`, `SEPAY_ACCOUNT_NUMBER`,
   `RESEND_API_KEY`, `EMAIL_GUI` (vd `Tiệm bánh Mây <don@tiembanhmay.vn>`), tùy chọn `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
   → đưa trang lên lại bằng `/ts-dua-web-len-mang`.
5. Xác minh tên miền gửi email ở Resend (SPF/DKIM/DMARC): `references/resend-deliverability.md` +
   `references/_chung/dns-basics-for-nontech.md`. Chi tiết gửi bằng Resend: `references/resend-email-delivery.md`.

**Trang trên LadiPage/Canva/WordPress:** dùng tính năng gửi email sau đơn/tích hợp có sẵn của nền tảng, hoặc dựng thêm 1 trang
thanh toán trên Vercel theo cách trên rồi trỏ nút "Mua" sang trang đó.

**Cần chặt hơn** (chống gửi trùng, ghi sổ giao hàng, thử lại khi lỗi, link có hạn): kiến trúc webhook + cơ sở dữ liệu trong
`references/automated-delivery-workflow.md` — đọc khung "Cập nhật đối chiếu" ở đầu file trước khi dùng code.

### Bước 5 — Thử thật từ đầu đến cuối (bắt buộc)
- [ ] Tạo gói thử giá 2.000đ → mua bằng email của bạn → trả tiền → trang cảm ơn hiện link trong ≤ 30 giây.
- [ ] Email đến **Hộp thư chính** (không phải Spam/Quảng cáo), nút mở đúng sản phẩm, hiển thị tốt trên điện thoại.
- [ ] Telegram báo "đã giao" (nếu cài). · [ ] Mở link sản phẩm bằng trình duyệt ẩn danh → vào được.
- [ ] Thử mã đơn chưa trả tiền → không nhận được sản phẩm.
- [ ] Không còn `[CẦN BỔ SUNG]`, không có khóa API trong file trang.

### Bước 6 — Bàn giao & bảo trì (CỔNG DUYỆT 2)
Trình: sơ đồ luồng đã cài · bảng gói → sản phẩm · email mẫu · kết quả thử · lịch kiểm tra hằng tháng.
Bảo trì (`references/post-launch-operations.md`): mỗi tháng mua thử 1 đơn nhỏ; kiểm tra email còn vào hộp thư chính; link sản phẩm
còn mở được; khóa API không bị tắt. Lỗi thanh toán/báo đơn → `/ts-cai-thanh-toan`, `/ts-bao-don-telegram`; trang lỗi → `/ts-dua-web-len-mang`.
> "Gõ **duyệt** để lưu cấu hình giao hàng vào Bộ Não."

| Lỗi | Cách sửa |
|---|---|
| Trả tiền rồi nhưng không nhận | Thanh toán chưa được xác nhận (kiểm tra `/ts-cai-thanh-toan`) → rồi mới đến bước giao |
| Email không đến / vào Spam | Tên miền chưa xác minh trên Resend; `EMAIL_GUI` không thuộc tên miền đã xác minh |
| Giao nhầm sản phẩm | Sai mã gói trong bảng `SAN_PHAM` hoặc giá không khớp QR |
| Link không mở được | Drive chưa mở quyền xem; dùng link ổn định, không hết hạn |

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** sản phẩm đã tải lên chỗ ổn định (Google Drive, nền tảng khóa học…) và link mở thử được; tên miền riêng (nếu muốn
gửi email); đã cài `/ts-cai-thanh-toan` trên trang Vercel.

**1. Tạo tài khoản Resend & khóa API (10 phút)**
- Vào `https://resend.com` → **Sign up** → đăng ký bằng email hoặc Google → xác nhận email.
- Vào mục **Domains** → **Add Domain** → nhập tên miền (vd `tiembanhmay.vn`) → Resend hiện danh sách bản ghi DNS.
- Mở trang quản lý tên miền nơi bạn mua (Mắt Bão, PA Việt Nam, Nhân Hòa, Tenten…) → mục **DNS / Quản lý DNS** → **Thêm bản ghi**
  → chép **đúng từng dòng** Resend đưa (loại TXT/MX/CNAME, tên, giá trị) → Lưu. Quay lại Resend bấm **Verify** (chờ vài phút đến vài giờ).
- Vào **API Keys** → **Create API Key** → đặt tên `giao-hang` → quyền **Sending access** → **Create** → sao chép khóa
  (chỉ hiện 1 lần). **Không dán vào chat với AI.**

**2. Đặt khóa vào Vercel:** dự án → **Settings → Environment Variables** → **Add** → Key `RESEND_API_KEY`, Value dán khóa → **Save**.
Thêm `EMAIL_GUI` (vd `Tiệm bánh Mây <don@tiembanhmay.vn>`) và các khóa AI liệt kê (`SEPAY_API_TOKEN`…) giống vậy.

**3. Gửi AI danh sách sản phẩm:** tên gói, giá, link sản phẩm, 1–2 câu hướng dẫn dùng. Đọc email mẫu AI soạn, sửa bằng lời
("thân mật hơn", "thêm câu hỏi về cách tải"), gõ **duyệt**.

**4. Cho AI cài và đưa trang lên lại:** bấm **Cho phép** khi AI xin chạy lệnh (macOS: Terminal, Windows: PowerShell — AI tự mở/hướng dẫn).

**5. Mua thử 2.000đ** bằng email của bạn → kiểm tra trang cảm ơn, hộp thư (cả Spam), Telegram. Chụp màn hình gửi AI.

**6. Gõ "duyệt"** để lưu. Đặt nhắc lịch mỗi tháng mua thử 1 đơn nhỏ.

## Câu lệnh mẫu
- `/ts-giao-hang-tu-dong khóa học Bánh mì tại nhà 690k, trả tiền xong gửi link Drive video qua email và hiện trên trang cảm ơn.`
- `/ts-giao-hang-tu-dong bán 3 ebook 99k, 149k, 199k — mỗi gói giao đúng file PDF, gửi từ email don@tiembanhmay.vn.`
- `/ts-giao-hang-tu-dong spa Hồng bán voucher online, trả tiền xong gửi mã voucher qua email và báo nhóm lễ tân Telegram.`
- `/ts-giao-hang-tu-dong khách kêu không nhận được email sản phẩm, kiểm tra giúp tôi.`

## Kết quả nhận được
- Khuyến nghị cách giao + sơ đồ luồng: trả tiền → xác nhận → giao → báo chủ shop.
- Bảng "gói → sản phẩm giao" đã duyệt.
- Email giao hàng + trang cảm ơn đúng giọng thương hiệu; (tùy chọn) chuỗi chăm sóc sau mua.
- File `api/giao-hang.js` đã cấu hình + danh sách biến môi trường cần đặt.
- Kết quả thử thật, bảng xử lý lỗi, lịch bảo trì hằng tháng.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-giao-hang-tu-dong-<chu-de-khong-dau>/`.
2. Lưu cấu hình giao hàng thành `ket-qua.md` (cách giao, bảng gói → sản phẩm → link, địa chỉ gửi email, tên miền đã xác minh,
   **tên** các biến môi trường đã đặt, link trang thanh toán/cảm ơn, ngày thử thành công, lịch bảo trì), mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-giao-hang-tu-dong
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `email-giao-hang.md`, `trang-cam-on.html`, `giao-hang.js` (không chứa khóa),
   `chuoi-cham-soc-sau-mua.md`. **Tuyệt đối không lưu** khóa API Resend/SePay, token bot, mật khẩu.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-giao-hang-tu-dong · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu bảng gói/giá/link giao khác với `01-ho-so/02-san-pham-dich-vu.md`, đề xuất cập nhật mục sản phẩm (thêm dòng "Cách giao") và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Khóa API, token chỉ nằm ở biến môi trường trên máy chủ; không xin dán vào chat, không ghi vào trang, không lưu Bộ Não.
- Chỉ giao khi đã xác nhận **đủ tiền** với SePay; mã đơn ngẫu nhiên ≥ 8 ký tự để không bị đoán.
- Bản mẫu không có cơ sở dữ liệu: người biết mã đơn đã trả có thể mở lại link → sản phẩm giá cao nên dùng nền tảng có tài khoản.
- Email giao hàng là email giao dịch; muốn gửi quảng cáo/chuỗi chăm sóc phải có sự đồng ý của khách và nút hủy nhận.
- Bật giao hàng thật (gửi email cho khách thật) là hành động gửi tin → trình bản thử và chờ người dùng nói "duyệt".
- Luôn ghi liên hệ hỗ trợ trong email; giữ đúng chính sách hoàn tiền đã công bố.

## Skill liên quan
- Trước: `/ts-cai-thanh-toan` · `/ts-gan-ma-qr` · `/ts-bao-don-telegram` · `/ts-dua-web-len-mang`
- Sau: `/ts-email-cham-soc` · `/ts-phan-tich-doanh-thu` · `/ts-cham-soc-khach-zalo`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
