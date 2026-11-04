---
name: ts-landing-page
description: "Gọi bằng /ts-landing-page. Dựng trọn landing page thành 1 file HTML chạy ngay (Tailwind, đẹp trên điện thoại), lấy màu, logo, giọng văn từ hồ sơ thương hiệu, dùng lại chữ đã viết bằng /ts-trang-ban-hang nếu có, có 10 mẫu theo ngành, kiểm tra chống trang kiểu AI. Dùng khi cần trang bán hàng, trang thu lead, trang sự kiện có file thật để đưa lên mạng. Từ khóa: landing page, làm trang web bán hàng, trang đích, file HTML, trang đăng ký, trang sự kiện, làm web theo mẫu."
---

# /ts-landing-page — Dựng landing page thành file HTML chạy ngay

> AI dựng một trang landing page hoàn chỉnh trong **1 file `index.html`** (mở bằng trình duyệt là xem được,
> đẹp trên điện thoại), dùng đúng màu, logo, giọng văn của bạn. Xong là đưa lên mạng được ngay.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Đã có (hoặc chưa có) chữ cho trang bán hàng, muốn có **file trang web thật** để đưa lên mạng.
- Cần trang thu thông tin khách (tặng quà, đăng ký học thử, đặt lịch tư vấn).
- Cần trang cho sự kiện, hội thảo online, ra mắt sản phẩm, menu quán ăn, giới thiệu cá nhân.
- Có ảnh chụp một trang mẫu đẹp, muốn làm trang theo phong cách tương tự.
- Trang cũ trông "giống AI", muốn làm lại cho có chất người thật.

**Không dùng khi:** chỉ cần viết chữ để dán vào LadiPage/Canva → `/ts-trang-ban-hang`; đã có file, cần link
thật → `/ts-dua-web-len-mang`; cần gắn mã QR nhận tiền vào trang có sẵn → `/ts-gan-ma-qr`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `landing-page`, `trang-ban-hang` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Lấy gì từ đâu:**
| Cần | Lấy từ |
|---|---|
| Màu sắc, font, logo, giọng văn, xưng hô | `04-thuong-hieu-noi-dung.md` (logo nằm trong `03-tai-lieu-tho/dinh-kem/`) |
| Tên sản phẩm, giá, gói, bảo hành | `02-san-pham-dich-vu.md` |
| Khách là ai, nỗi lo, chữ khách hay nói | `03-khach-hang-muc-tieu.md` |
| Hotline/Zalo, email, địa chỉ, giờ làm, link website | `05-muc-tieu-quy-tac-lien-he.md` |
| Chữ đã viết sẵn cho trang | thư mục `04-ket-qua/…-trang-ban-hang-…/ket-qua.md` (từ `/ts-trang-ban-hang`) |
| Ảnh sản phẩm, ảnh phản hồi khách thật | `03-tai-lieu-tho/` và `03-tai-lieu-tho/dinh-kem/` |

## Quy trình AI thực hiện

### Bước 1 — Hỏi rõ đề bài (cổng hỏi, tối đa 3 lượt)
Theo `references/_chung/clarification-gate.md`. Chỉ hỏi phần Bộ Não chưa có:
1. Trang này để làm gì? A. Bán sản phẩm/khóa học/dịch vụ · B. Thu thông tin khách (tặng quà, học thử) · C. Sự kiện/hội thảo · D. Giới thiệu cá nhân/cửa hàng.
2. **Một hành động duy nhất** khách cần làm: mua ngay · để lại số điện thoại · nhắn Zalo · đặt lịch · đăng ký.
3. Khách đến trang từ đâu? (quảng cáo Facebook, TikTok, nhóm Zalo, tìm Google…) — để tiêu đề trang khớp lời hứa ở quảng cáo.
4. Bằng chứng thật đang có: ảnh phản hồi (khách đã đồng ý), số khách thật, ảnh trước/sau, giấy phép.
5. Đã có chữ viết sẵn chưa? A. Có, từ `/ts-trang-ban-hang` · B. Có, tôi dán vào · C. Chưa, AI viết giúp.
6. Thích phong cách nào? (có thể gửi ảnh/link trang mẫu) · Nhận thanh toán ngay trên trang không?

### Bước 2 — Lấy chữ cho trang
- **Có chữ từ `/ts-trang-ban-hang`** (hoặc người dùng dán): dùng nguyên văn đã duyệt, chỉ cắt gọn cho vừa bố cục;
  muốn sửa ý thì hỏi trước. Mỗi khối chữ → 1 khối (section) trên trang, giữ đúng thứ tự và vị trí nút.
- **Chưa có chữ:** AI tự viết theo `references/conversion-structure-principles.md` (bài kiểm tra 5 giây,
  khớp lời hứa quảng cáo, 1 hành động chính, bằng chứng đặt cạnh lời hứa). Giọng văn và xưng hô theo
  `04-thuong-hieu-noi-dung.md`. Trang bán hàng dài, nhiều khối → gợi ý chạy `/ts-trang-ban-hang` trước.
- Thiếu bằng chứng → để `[CẦN BỔ SUNG: …]`, không bịa lời khen, con số, logo đối tác.

### Bước 3 — Chọn thiết kế
**a) Mẫu HTML theo ngành** — chỉ đọc **đúng 1 file** khớp nhất trong `templates/` (file rất dài, không mở hết):

| Mẫu | Phong cách | Hợp với |
|---|---|---|
| `landing-page-template.html` | Sáng, tiêu chuẩn | Dịch vụ chung, chưa có sở thích riêng |
| `landing-page-dark-modern.html` | Nền tối, hiện đại | Công nghệ, AI, phần mềm |
| `landing-page-minimal-clean.html` | Tối giản, sang | Coaching, dịch vụ cao cấp, thương hiệu cá nhân |
| `landing-page-creative-bold.html` | Chữ to, phá cách | Agency, sáng tạo, khởi nghiệp |
| `landing-page-saas-product.html` | Tập trung sản phẩm | Phần mềm, ứng dụng (mẫu gốc `lang="en"` → đổi `vi`) |
| `landing-page-ecommerce-product.html` | Bán hàng | Sản phẩm vật lý / sản phẩm số |
| `landing-page-webinar-event.html` | Sự kiện | Hội thảo online, workshop, ra mắt |
| `landing-page-portfolio-personal.html` | Hồ sơ cá nhân | Freelancer, chuyên gia, người dạy |
| `landing-page-restaurant-food.html` | Ẩm thực | Quán ăn, quán cà phê, giao đồ ăn |
| `landing-page-mobile-app.html` | Ứng dụng | Ra mắt app, công cụ |

**b) Màu:** ưu tiên màu trong `04-thuong-hieu-noi-dung.md` — nếu là 1 trong 6 bộ (đen vàng, gradient tím, xanh,
cam vàng, đỏ cam, trắng cam) thì dùng bảng mã màu ở mục "Bộ 6 màu" trong `references/design-data.md`.
Chưa có màu → chọn theo ngành trong cùng file, rồi hỏi người dùng có muốn lưu làm màu thương hiệu không.

**c) Font:** bắt buộc font có hỗ trợ **tiếng Việt** (kiểm tra mục "Vietnamese" trên Google Fonts).
An toàn: Be Vietnam Pro, Inter, Roboto, Montserrat, Noto Sans, Nunito, Open Sans, Lexend, Lora, Playfair Display,
Merriweather. Font khác (Poppins, Bebas Neue, Fredoka…) dễ lỗi dấu → tránh hoặc kiểm tra trước. Hồ sơ có font → dùng font đó.

**d) Bố cục:** chọn kiểu trang theo mục tiêu:

| Mục tiêu | Kiểu trang | Thứ tự khối gợi ý |
|---|---|---|
| Doanh nghiệp mới, chưa có phản hồi | Lợi ích + tính năng | Hero → lợi ích → cách hoạt động → ưu đãi → hỏi đáp → nút |
| Dịch vụ cần lòng tin (spa, nha khoa, luật) | Bằng chứng nặng | Hero → vấn đề → giải pháp → phản hồi thật → bảo đảm → nút |
| Hứa thay đổi (khóa học, làm đẹp) | Trước – sau | Hero → trước/sau → cách làm → bằng chứng → nút |
| Tặng quà lấy thông tin | Trang quà + form | Tiêu đề quà → trong quà có gì → form ≤ 3 ô |
| Nhiều gói giá | Bảng giá | Hero → giá trị → 2–3 gói → so sánh → hỏi đáp |
| Sắp ra mắt | Danh sách chờ | Hero → hé lộ → đếm ngược (ngày thật) → form |

Đổi kiểu phần đầu trang (canh giữa, chữ trái – ảnh phải, chia đôi, ảnh tràn nền…) theo bảng
"Layout Variation Matrix" và "Randomization Rule" trong `references/design-data.md` để hai trang cùng ngành
không giống nhau. **Không** mặc định "nền xanh tím chuyển màu + 3 thẻ đều nhau".

### Bước 4 — Trình phác thảo (CỔNG DUYỆT 1)
Trình ngắn gọn: mẫu đã chọn · bộ màu (mã màu) · font · danh sách khối từ trên xuống · chữ trên nút chính ·
hành động khi bấm nút (mở form / mở Zalo / cuộn tới mã QR) · danh sách `[CẦN BỔ SUNG]`.
> "Gõ **duyệt** để mình dựng file, hoặc nói chỗ muốn đổi (vd 'đổi sang nền tối', 'bỏ bảng giá')."

### Bước 5 — Dựng file HTML
- Lấy khung và các khối có sẵn trong `references/thu-vien-component.md` (đầu trang, tính năng, phản hồi, bảng giá,
  hỏi đáp, chân trang, khối VietQR, mẫu thẻ SEO) + mẫu đã chọn ở Bước 3.
- 1 file duy nhất `index.html`, `<html lang="vi">`, Tailwind qua CDN, Google Fonts, đủ `title`, `description`,
  thẻ chia sẻ Facebook (`og:title`, `og:description`, `og:image` 1200×630).
- Chữ hiển thị 100% tiếng Việt có dấu; đổi hết chữ tiếng Anh còn sót trong mẫu ("Get Started", "Pricing"…).
- **Logo & ảnh:** chép vào thư mục `hinh-anh/` cạnh `index.html`, gọi bằng đường dẫn tương đối (`hinh-anh/logo.png`).
  Tên file viết thường, không dấu, không khoảng trắng. Chưa có ảnh → khung màu nhạt + chú thích `[CẦN BỔ SUNG: ảnh …]`.
- **Liên hệ:** hotline/Zalo (`https://zalo.me/<số điện thoại>`), địa chỉ, giờ làm lấy từ `05-muc-tieu-quy-tac-lien-he.md`.
- **Form:** trang tĩnh không tự lưu được dữ liệu. Chọn 1: (A) nút mở Zalo/Messenger, (B) nhúng Google Form,
  (C) dịch vụ nhận form miễn phí (Formspree, Web3Forms — người dùng tự tạo tài khoản, AI chỉ dán mã form công khai).
  Form tối đa 3–4 ô, ghi rõ dùng thông tin để làm gì.
- **Thanh toán:** cần mã QR nhận tiền → chừa khối VietQR (có trong thư viện) với chỗ trống, rồi chạy `/ts-gan-ma-qr`
  để điền đúng ngân hàng, số tài khoản và nội dung chuyển khoản.
- Làm theo ảnh/link mẫu → làm theo `references/lam-theo-anh-mau.md` (phân tích 8 mặt → kế hoạch dựng → so sánh).

### Bước 6 — Tự kiểm tra trước khi giao
1. Chạy `references/anti-ai-slop-checklist.md` — sửa hết 10 dấu hiệu "trang kiểu AI".
2. Thêm chi tiết người thật theo `references/humanize-design-patterns.md` (địa chỉ, giá VND, gương mặt chủ shop…).
3. Đánh dấu checklist:
   - [ ] Đọc 5 giây hiểu: đây là gì, cho ai, được gì, bấm vào đâu.
   - [ ] 1 hành động chính, nút lặp lại 2–4 lần, chữ trên nút cụ thể (không "Gửi", "Tìm hiểu thêm").
   - [ ] Đẹp ở bề ngang 375px (điện thoại), 768px, 1440px; vùng bấm ≥ 44px; chữ thân ≥ 16px.
   - [ ] Tương phản chữ/nền ≥ 4.5:1; tất cả ảnh có `alt`; không còn `{{...}}`, "Lorem ipsum", chữ tiếng Anh.
   - [ ] Không có số liệu, lời khen, logo bịa; đếm ngược và "chỉ còn X suất" là thật.
   - [ ] Đường dẫn ảnh tương đối, đúng chữ hoa/thường; link Zalo/điện thoại bấm được.
   - [ ] Màu, logo, giọng văn khớp `04-thuong-hieu-noi-dung.md`.
4. Ghi 1 dòng xác nhận: *"Kiểm tra chống AI: không gradient mặc định, không câu sáo rỗng, bố cục đa dạng, nút cụ thể, bằng chứng cạnh lời hứa, chi tiết địa phương thật ✅"*.

### Bước 7 — Giao file & xem thử (CỔNG DUYỆT 2)
- Lưu vào thư mục `landing-<ten-khong-dau>/` gồm `index.html` + `hinh-anh/`. Có công cụ xem trước thì mở cho người dùng xem.
- Liệt kê việc cần bổ sung (`[CẦN BỔ SUNG]`) và hỏi: "Gõ **duyệt** để lưu, hoặc nói chỗ cần sửa."
- **Gợi ý bước tiếp:** `/ts-dua-web-len-mang` để có link thật gửi khách · `/ts-gan-ma-qr` để gắn mã QR nhận tiền
  · sau đó `/ts-bao-don-telegram` để có đơn là báo về điện thoại.

### Ví dụ minh họa (doanh nghiệp giả định)
*Tiệm bánh Mây* bán khóa "Bánh mì tại nhà" 690.000đ, khách đến từ quảng cáo Facebook, hồ sơ chọn bộ màu **cam vàng**.
AI chọn mẫu `landing-page-ecommerce-product.html`, font Be Vietnam Pro + Lora, phần đầu trang "ảnh tràn nền + chữ đè",
nút chính "Giữ chỗ học thử miễn phí" mở Zalo, khối phản hồi để `[CẦN BỔ SUNG: 3 ảnh phản hồi học viên đã đồng ý]`.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (5–10 phút):**
- Logo (file PNG nền trong suốt nếu có), 3–6 ảnh thật: sản phẩm, bạn đang làm việc, khách dùng sản phẩm.
- Ảnh chụp tin nhắn khen của khách (đã xin phép), giá và quà tặng, số Zalo nhận khách.
- Nếu có Bộ Não: thả ảnh vào `03-tai-lieu-tho/dinh-kem/`. Nếu không: gửi kèm tin nhắn.

1. Gõ `/ts-landing-page` kèm 1 câu: trang để bán/tặng gì, cho ai. Có chữ từ `/ts-trang-ban-hang` thì nói "dùng chữ đã viết".
2. Trả lời câu hỏi (chọn A-B-C-D). Thích trang nào thì gửi ảnh chụp màn hình trang đó.
3. Xem phác thảo AI đưa (màu, font, các khối). Muốn đổi thì nói bằng lời, xong gõ **duyệt**.
4. AI tạo thư mục `landing-…` có file `index.html`. Mở xem:
   - **macOS:** mở Finder → vào thư mục → nhấp đúp `index.html` (hoặc chuột phải → Mở bằng → Chrome/Safari).
   - **Windows:** mở File Explorer → vào thư mục → nhấp đúp `index.html` (hoặc chuột phải → Open with → Chrome/Edge).
   - Xem dạng điện thoại: kéo hẹp cửa sổ trình duyệt lại còn khoảng bằng màn hình điện thoại.
5. Sửa bằng lời: "tiêu đề to hơn", "đổi nút sang màu đỏ", "thêm câu hỏi về giao hàng". Gửi ảnh còn thiếu cho AI điền.
6. Gõ **duyệt** để lưu vào Bộ Não.
7. Chạy `/ts-dua-web-len-mang` để có link thật, mở link trên điện thoại kiểm tra lần cuối trước khi chạy quảng cáo.

## Câu lệnh mẫu
- `/ts-landing-page dùng chữ đã viết bằng /ts-trang-ban-hang hôm qua để làm trang bán khóa học làm bánh, màu theo hồ sơ.`
- `/ts-landing-page trang đặt lịch soi da miễn phí cho spa Hồng, nút mở Zalo, phong cách tối giản sang trọng.`
- `/ts-landing-page trang bán bộ nến thơm quà tặng 390k, có mã QR chuyển khoản, khách đến từ TikTok.`
- `/ts-landing-page trang đăng ký hội thảo online 'Quay video bán hàng bằng điện thoại' tối thứ 7, có đếm ngược.`
- `/ts-landing-page làm trang giống phong cách ảnh này cho quán cà phê của tôi <gửi kèm ảnh chụp màn hình>.`

## Kết quả nhận được
- Phác thảo thiết kế: mẫu, bộ màu (mã màu), font, thứ tự khối, chữ trên nút.
- Thư mục `landing-<tên>/` có `index.html` chạy ngay + `hinh-anh/` (logo, ảnh).
- Kết quả kiểm tra chống "trang kiểu AI" + checklist chất lượng.
- Danh sách `[CẦN BỔ SUNG]` (ảnh, phản hồi, số liệu thật cần bạn gửi).
- Gợi ý bước tiếp: đưa lên mạng, gắn QR, báo đơn.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-landing-page-<chu-de-khong-dau>/`.
2. Lưu bản mô tả trang (mục tiêu, hành động chính, mẫu, màu, font, thứ tự khối, chữ từng khối, việc cần bổ sung) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-landing-page
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `index.html`, thư mục `hinh-anh/` (logo, ảnh đã dùng).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-landing-page · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu bộ màu, font hoặc logo vừa chốt chưa có (hoặc khác) trong `01-ho-so/04-thuong-hieu-noi-dung.md`, đề xuất cập nhật mục **Nhận diện** và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Không bịa** lời khen, số khách, số sao đánh giá, logo báo chí, ảnh trước/sau. Thiếu → `[CẦN BỔ SUNG: …]`.
- Đếm ngược, "chỉ còn X suất" phải là thật; không dùng đồng hồ tự quay lại khi hết giờ.
- Không hứa tuyệt đối ("chắc chắn khỏi", "thu nhập đảm bảo") — dễ vi phạm luật và chính sách quảng cáo.
- Không dùng ảnh, logo, chữ có bản quyền của trang mẫu; chỉ học bố cục và cảm giác.
- Không đưa khóa API, mật khẩu, token vào file HTML (ai mở trang cũng xem được mã nguồn).
- Phản hồi khách phải được khách đồng ý; che số điện thoại, tên đầy đủ nếu khách muốn.

## Skill liên quan
- Trước: `/ts-trang-ban-hang` (viết chữ) · `/ts-dinh-gia-offer` · `/ts-tao-ho-so-doanh-nghiep` (màu, logo, giọng văn)
- Sau: `/ts-dua-web-len-mang` · `/ts-gan-ma-qr` · `/ts-bao-don-telegram` · `/ts-giao-hang-tu-dong` · `/ts-viet-quang-cao`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
