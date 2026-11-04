---
name: ts-cai-thanh-toan
description: "Gọi bằng /ts-cai-thanh-toan. Cài hệ thống nhận tiền chuyển khoản qua mã VietQR với SePay: tạo tài khoản, liên kết ngân hàng, đặt cấu trúc mã đơn, tạo khóa API, nối webhook để đơn tự xác nhận khi khách chuyển tiền, có trang thanh toán tự chuyển sang trang cảm ơn. Kèm so sánh các cách nhận tiền và checklist an toàn. Từ khóa: nhận tiền tự động, SePay, VietQR, chuyển khoản tự xác nhận, cổng thanh toán, webhook thanh toán, đối soát đơn, mã QR ngân hàng."
---

# /ts-cai-thanh-toan — Cài nhận tiền qua mã VietQR (SePay)

> Khách quét mã QR bằng app ngân hàng → tiền vào thẳng tài khoản của bạn → hệ thống **tự biết** đơn nào đã trả tiền,
> không phải ngồi soi sao kê. AI lo phần kỹ thuật, bạn chỉ đăng ký SePay và bấm vài nút.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Lần đầu cài nhận tiền tự động cho trang bán hàng, khóa học, dịch vụ đặt cọc.
- Đang nhận chuyển khoản thủ công, mất thời gian kiểm tra và hay nhầm đơn.
- Muốn trang thanh toán **tự hiện "đã thanh toán"** và chuyển sang trang cảm ơn.
- Cần chọn giữa: chuyển khoản thủ công · SePay (VietQR tự xác nhận) · cổng thẻ quốc tế.

**Không dùng khi:** chỉ cần dán mã QR vào trang có sẵn (chưa cần tự xác nhận) → `/ts-gan-ma-qr`; cần báo đơn về điện thoại
→ `/ts-bao-don-telegram`; cần tự gửi sản phẩm sau khi trả tiền → `/ts-giao-hang-tu-dong`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Hỏi rõ (1–2 lượt)
Theo `references/_chung/clarification-gate.md`:
1. Bán gì, giá bao nhiêu, mỗi ngày khoảng bao nhiêu đơn? (ít đơn → thủ công vẫn ổn)
2. Khách trả bằng gì là chính? A. Chuyển khoản ngân hàng · B. Thẻ quốc tế/khách nước ngoài · C. Cả hai.
3. Nhận vào tài khoản ngân hàng nào (cá nhân hay doanh nghiệp)? Đã có tài khoản SePay chưa?
4. Trang bán hàng ở đâu? A. File HTML trên Vercel (`/ts-landing-page`, `/ts-dua-web-len-mang`) · B. LadiPage/Canva/WordPress · C. Chưa có.
5. Sau khi khách trả tiền muốn điều gì xảy ra? (hiện "đã thanh toán", báo Telegram, gửi sản phẩm, gửi email)

### Bước 2 — So sánh & chọn cách nhận tiền
| Cách | Hợp với | Ưu | Nhược |
|---|---|---|---|
| Chuyển khoản thủ công (dán số TK / ảnh QR tĩnh) | Mới bắt đầu, < 5 đơn/ngày | Không cài gì, không phí dịch vụ | Phải tự soi sao kê, khách chờ xác nhận, dễ nhầm |
| **SePay + VietQR tự xác nhận** (khuyên dùng) | Bán online tại Việt Nam | Khách quét là xong, tự đối soát theo mã đơn, báo ngay, nối giao hàng | Có phí dịch vụ theo gói, cần liên kết ngân hàng |
| Cổng thẻ quốc tế | Khách nước ngoài, cần thẻ Visa/Master | Nhận thẻ toàn cầu | Phí cao hơn, xét duyệt doanh nghiệp, ít ngân hàng VN |

Phí, gói và ngân hàng hỗ trợ **luôn kiểm tra trên sepay.vn tại thời điểm cài** — không nói con số theo trí nhớ.
Đọc `references/official-docs-index.md` và tài liệu chính thức trước khi đưa bước thật (tài liệu mới nhất được ưu tiên).

### Bước 3 — Thiết kế luồng thanh toán
```
Khách bấm "Mua" → trang thanh toán tạo MÃ ĐƠN ngẫu nhiên (vd DH8F3A2C) → hiện QR (số tiền + nội dung = mã đơn)
→ khách quét bằng app ngân hàng → tiền vào tài khoản → SePay thấy giao dịch
→ (1) trang hỏi SePay mỗi 5 giây "mã này trả chưa?" → hiện "Thanh toán thành công" → trang cảm ơn
→ (2) SePay gọi webhook → báo Telegram (/ts-bao-don-telegram) → gửi sản phẩm (/ts-giao-hang-tu-dong)
```
Quy tắc mã đơn: tiền tố cố định (vd `DH`) + 6–8 ký tự **ngẫu nhiên** (không dùng số tăng dần — người khác đoán được).
Nội dung chuyển khoản chỉ chữ và số, không dấu, không khoảng trắng. Tiền tố phải khớp **Cấu trúc mã thanh toán** trên SePay.
Thiết kế trang thanh toán dễ dùng trên điện thoại (QR ≥ 256px, số tiền to, nút chép nội dung, đếm ngược 15 phút, trạng thái
chờ/thành công/hết hạn): `references/checkout-flow-design-patterns.md`.

### Bước 4 — Hướng dẫn học viên cài SePay (học viên tự bấm)
Theo mục **Hướng dẫn cho học viên**: tạo tài khoản → liên kết ngân hàng → đặt cấu trúc mã thanh toán → tạo khóa API.
AI không đăng nhập hộ, không xin mật khẩu/OTP.

### Bước 5 — Dựng phần kỹ thuật (AI làm)
Trang dạng file HTML trên Vercel (A):
1. Chép `templates/trang-thanh-toan-tu-xac-nhan.html` thành `thanh-toan.html` (hoặc ghép vào trang có sẵn), điền
   `CAU_HINH`: tên sản phẩm, số tiền (số nguyên), ngân hàng (tên theo danh sách SePay, vd `Vietcombank`, `MBBank`),
   số tài khoản, tên chủ tài khoản không dấu, tiền tố, trang cảm ơn, Zalo hỗ trợ. Tạo thêm `cam-on.html`.
2. Chép `templates/api/kiem-tra-thanh-toan.js` thành `api/kiem-tra-thanh-toan.js` (cùng thư mục với trang).
3. Hướng dẫn học viên đặt biến môi trường trên Vercel (**Settings → Environment Variables**):
   `SEPAY_API_TOKEN` (khóa API SePay) và `SEPAY_ACCOUNT_NUMBER` (số tài khoản nhận). Rồi đưa trang lên lại bằng `/ts-dua-web-len-mang`.
4. Muốn báo Telegram / gửi sản phẩm / email ngay khi có tiền → cài **webhook** (my.sepay.vn → **Webhooks** → **+ Thêm webhook**,
   sự kiện *Có tiền vào*, bảo mật *API Key*): chi tiết ở `/ts-bao-don-telegram` và `/ts-giao-hang-tu-dong`.
   Webhook phải trả **HTTP 200 + `{"success": true}` trong 30 giây**, kiểm tra khóa, bỏ qua giao dịch trùng (`id`).

Trang trên LadiPage/Canva/WordPress (B): dùng tính năng/ứng dụng tích hợp SePay của nền tảng nếu có; nếu không, gắn ảnh
QR theo `/ts-gan-ma-qr` và bật báo đơn Telegram của SePay (không cần code). Code mẫu khác (Node.js, Express, HMAC):
`references/payment-gateway-integration-guide.md` — đọc khung "Cập nhật đối chiếu" ở đầu file trước.

### Bước 6 — Thử thật (bắt buộc trước khi bán)
- [ ] Mở trang thanh toán trên điện thoại, QR hiện đúng ngân hàng, số tiền, nội dung = mã đơn.
- [ ] Quét bằng app ngân hàng, chuyển **thử 2.000đ** (tạo đơn thử giá 2.000đ) → trong ≤ 30 giây trang báo thành công, chuyển trang cảm ơn.
- [ ] Giao dịch hiện trong my.sepay.vn → **Giao dịch**, đúng mã đơn.
- [ ] Thử chuyển **thiếu tiền** → trang không báo thành công.
- [ ] Để hết 15 phút không trả → trang báo hết hạn, có Zalo hỗ trợ kèm mã đơn.
- [ ] Không có khóa API/token nào trong file HTML (mở "Xem mã nguồn trang" để kiểm tra).

### Bước 7 — Báo kết quả (CỔNG DUYỆT)
Trình: cách đã chọn · ngân hàng (che bớt số TK, vd `****6789`) · tiền tố mã đơn · link trang thanh toán · kết quả thử ·
việc tiếp theo. > "Gõ **duyệt** để lưu cấu hình vào Bộ Não."

**Lỗi thường gặp:**
| Hiện tượng | Cách sửa |
|---|---|
| QR không hiện | Sai tên ngân hàng/số TK; mở thử link ảnh QR trong trình duyệt; đổi giữa `vietqr.app/img` và `qr.sepay.vn/img` |
| Đã trả tiền nhưng trang không báo | Khách sửa nội dung CK; chưa đặt `SEPAY_API_TOKEN` hoặc chưa đưa lại trang; tiền tố không khớp cấu trúc mã trên SePay |
| Lỗi 401 khi hỏi SePay | Khóa API sai/đã tắt → tạo khóa mới ở **API Access**, cập nhật Vercel |
| Ngân hàng không liên kết được | Vấn đề tài khoản/ngân hàng → liên hệ hỗ trợ SePay, không cố "lách" |

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** CCCD/thông tin cá nhân hoặc doanh nghiệp, tài khoản ngân hàng nhận tiền, điện thoại có app ngân hàng.

**1. Tạo tài khoản SePay (5–10 phút)**
- Vào `https://my.sepay.vn` → bấm **Đăng ký** → điền họ tên, email, số điện thoại, mật khẩu → xác nhận theo hướng dẫn trên màn hình.
- Đăng nhập. Nếu SePay yêu cầu chọn gói dịch vụ, đọc kỹ phí rồi chọn gói phù hợp số đơn của bạn.

**2. Liên kết ngân hàng**
- Trong trang quản lý, tìm mục **Ngân hàng** / **Thêm tài khoản ngân hàng** → chọn ngân hàng → làm theo hướng dẫn liên kết
  (mỗi ngân hàng một cách; có thể cần xác nhận trên app ngân hàng). **Không gửi mã OTP cho AI hay bất kỳ ai.**

**3. Đặt cấu trúc mã thanh toán**
- Vào **Công ty → Cấu hình chung → Cấu trúc mã thanh toán** → đặt tiền tố AI đề xuất (vd `DH`) → lưu.
  (Tên menu có thể thay đổi — chụp màn hình gửi AI nếu không thấy.)

**4. Tạo khóa API (để trang tự kiểm tra thanh toán)**
- Vào **Cấu hình Công ty → API Access** → bấm **+ Thêm API** → đặt tên (vd `trang-ban-hang`), trạng thái **Hoạt động** → **Thêm**.
- Sao chép khóa vừa tạo. **Không dán vào chat với AI.** Mở Vercel → dự án → **Settings → Environment Variables** → **Add**:
  Key `SEPAY_API_TOKEN`, Value dán khóa → **Save**. Thêm tiếp Key `SEPAY_ACCOUNT_NUMBER` = số tài khoản nhận tiền.

**5. Để AI dựng trang thanh toán & đưa lên mạng** — nói "dựng trang thanh toán và đưa lên", bấm **Cho phép** khi AI xin chạy lệnh.

**6. Thử 2.000đ** như Bước 6. Chụp màn hình trang báo thành công gửi AI.

**7. Gõ "duyệt"** để lưu (không lưu khóa API) vào Bộ Não.

## Câu lệnh mẫu
- `/ts-cai-thanh-toan cài nhận tiền tự động cho trang bán khóa học làm bánh 690k, tài khoản Vietcombank, trang đang ở Vercel.`
- `/ts-cai-thanh-toan spa Hồng muốn khách chuyển cọc 200k khi đặt lịch, tự xác nhận và báo cho lễ tân.`
- `/ts-cai-thanh-toan tôi bán nến thơm trên LadiPage, mỗi ngày 20 đơn, nên dùng SePay hay chuyển khoản thủ công?`
- `/ts-cai-thanh-toan khách đã chuyển tiền mà trang không báo thành công, kiểm tra giúp tôi.`

## Kết quả nhận được
- Bảng so sánh và khuyến nghị cách nhận tiền phù hợp quy mô.
- Sơ đồ luồng thanh toán + quy tắc mã đơn.
- Trang thanh toán tự xác nhận (`thanh-toan.html`, `cam-on.html`) + hàm `api/kiem-tra-thanh-toan.js`.
- Danh sách việc học viên tự bấm trên SePay/Vercel, đã đánh dấu xong.
- Kết quả thử thật 2.000đ và bảng xử lý lỗi.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-cai-thanh-toan-<chu-de-khong-dau>/`.
2. Lưu cấu hình đã cài thành `ket-qua.md` (cách nhận tiền, ngân hàng + 4 số cuối tài khoản, tiền tố mã đơn, link trang thanh toán
   và trang cảm ơn, **tên** biến môi trường đã đặt, webhook nếu có, ngày thử thành công, việc còn lại), mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-cai-thanh-toan
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `thanh-toan.html`, `kiem-tra-thanh-toan.js` đã dùng (không chứa khóa).
   **Tuyệt đối không lưu** khóa API SePay, mật khẩu, OTP, ảnh CCCD.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-cai-thanh-toan · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không xin mật khẩu, OTP, khóa API, ảnh giấy tờ trong chat. Học viên tự đăng nhập, tự dán khóa vào Vercel.
- Khóa API **chỉ** nằm ở biến môi trường phía máy chủ, không bao giờ trong file HTML/JavaScript của trang.
- Mã đơn ngẫu nhiên, kiểm tra **đủ số tiền**; webhook phải kiểm tra khóa và chống giao dịch trùng.
- Tin báo/trang "đã thanh toán" là tự động — với đơn giá trị lớn, đối chiếu lại số dư trong app ngân hàng trước khi giao.
- Bật trang bán thật (nhận tiền thật) là hành động công khai → trình bản thử và chờ người dùng nói "duyệt".
- Tuân thủ quy định thuế, hóa đơn của hộ kinh doanh/doanh nghiệp — hỏi kế toán nếu chưa rõ.

## Skill liên quan
- Trước: `/ts-landing-page` · `/ts-trang-ban-hang` · `/ts-dua-web-len-mang`
- Sau: `/ts-gan-ma-qr` · `/ts-bao-don-telegram` · `/ts-giao-hang-tu-dong` · `/ts-phan-tich-doanh-thu`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
