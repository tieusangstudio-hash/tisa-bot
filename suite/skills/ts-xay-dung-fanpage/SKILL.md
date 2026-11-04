---
name: ts-xay-dung-fanpage
description: "Gọi bằng /ts-xay-dung-fanpage. Biến hồ sơ doanh nghiệp thành Fanpage Facebook rõ định vị: 3 phương án tên - danh mục - username - giới thiệu - nút hành động, concept logo và ảnh bìa đúng màu thương hiệu, gói nội dung khởi động (bài ghim, 5 bài đầu, FAQ, tin nhắn chào, trả lời nhanh, lịch 7 ngày), checklist thiết lập; hỗ trợ thao tác trên Facebook khi bạn cho phép. Dùng khi tạo mới, làm lại hoặc kiểm tra Fanpage. Từ khóa: tạo fanpage, xây fanpage, ảnh bìa fanpage, giới thiệu fanpage, tối ưu trang facebook, fanpage mới, chuẩn hóa fanpage."
---

# /ts-xay-dung-fanpage — Xây dựng Fanpage

> Biến hồ sơ doanh nghiệp thành một Fanpage rõ định vị, đồng bộ hình ảnh và sẵn sàng vận hành: thông tin trang,
> logo/ảnh bìa, bài ghim, 5 bài đầu, FAQ, tin nhắn chào, lịch 7 ngày — kèm checklist trạng thái.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Mở Fanpage mới cho cửa hàng, dịch vụ, khóa học, thương hiệu cá nhân.
- Fanpage cũ lộn xộn: tên, giới thiệu, ảnh bìa không rõ bán gì.
- Đổi định vị/đổi tên thương hiệu, cần chuẩn hóa lại trang.
- Muốn kiểm tra Fanpage hiện tại còn thiếu gì trước khi chạy quảng cáo.

**Không dùng khi:** Fanpage đã chuẩn, chỉ cần bài đăng hằng tuần → `/ts-noi-dung-tu-dong-7-ngay` hoặc `/ts-lich-noi-dung`.
Cần trả lời bình luận/inbox hằng ngày → `/ts-cham-soc-fanpage`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: cả 5 tệp — `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md` (giọng văn, màu, font, logo), `05-muc-tieu-quy-tac-lien-he.md` (liên hệ, Page ID nếu đã có trang);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `xay-dung-fanpage` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

Chủ động đọc tệp, tài liệu và thông tin đã có; không hỏi lại dữ liệu đã biết.

### Bước 1 — Tóm tắt nền tảng
Sản phẩm, khách hàng, khu vực, điểm khác biệt, bằng chứng, mục tiêu, giọng thương hiệu, màu/font/logo.
Nếu đã có Fanpage (link hoặc Page ID trong tệp 05): đọc trang công khai (nếu có công cụ đọc web) và chấm
nhanh theo checklist `references/cau-truc-fanpage.md`.

### Bước 2 — Hỏi phần thiếu có ảnh hưởng lớn
Luôn hỏi: **"Anh/chị đã có logo và ảnh bìa chưa?"** Các câu khác (tối đa 3, có gợi ý A–D): nút hành động
mong muốn (nhắn tin / gọi / đặt lịch / mua), có địa chỉ cửa hàng công khai không, ai trả lời tin nhắn.

### Bước 3 — Đưa 3 phương án định vị Fanpage
Mỗi phương án dùng **bảng thông tin Fanpage** (mẫu trong `references/cau-truc-fanpage.md`): tên trang,
danh mục, username, mô tả ngắn, phần giới thiệu, CTA, lý do chọn. Ba phương án phải khác nhau về góc định vị
(vd theo chuyên gia / theo kết quả / theo cộng đồng), không chỉ đổi vài chữ.

### Bước 4 — Chốt một phương án (cổng duyệt 1)
👉 Chờ người dùng chọn/sửa trước khi thiết kế hoặc thao tác Facebook.

### Bước 5 — Logo và ảnh bìa
- Có rồi: kiểm tra kích thước, vùng an toàn, độ rõ khi hiển thị nhỏ.
- Chưa có: đề xuất **2–3 concept** (màu lấy từ tệp 04 — nếu chưa có màu, cho chọn 1 trong 6 bộ: đen vàng,
  gradient tím, xanh, cam vàng, đỏ cam, trắng cam; font có dấu tiếng Việt; biểu tượng; bố cục; thông điệp).
  Sau khi chọn: nếu môi trường có công cụ tạo ảnh thì tạo đúng kích thước, kiểm tra chữ tiếng Việt, giao tệp
  tải về; không có thì giao prompt từng ảnh (có thể dùng `/ts-thiet-ke-anh-quang-cao`).

### Bước 6 — Gói nội dung khởi động
Bài ghim, 5 bài đầu (vấn đề – giải pháp – bằng chứng – câu chuyện – ưu đãi), FAQ, tin nhắn chào, câu trả lời
nhanh, lịch đăng 7 ngày. Mẫu trong `references/cau-truc-fanpage.md`. Viết đúng giọng văn và xưng hô ở tệp 04.

### Bước 7 — Kiểm tra trước khi bàn giao (cổng duyệt 2)
Chạy checklist `references/cau-truc-fanpage.md` → bảng trạng thái **Đã có / Cần bổ sung / Chờ xác nhận**.
👉 Trình toàn bộ, chờ "duyệt".

### Bước 8 — Thao tác trên Facebook (chỉ khi được phép)
- Hỏi rõ: người dùng **tự làm theo hướng dẫn** (thứ tự thao tác trong `references/cau-truc-fanpage.md`) hay
  **cho phép AI thao tác** trên trình duyệt đang đăng nhập (nếu môi trường có công cụ điều khiển trình duyệt)
  hoặc qua kết nối Meta chính thức (`/ts-ket-noi-ung-dung`, `/ts-tu-dong-hoa-meta`).
- Trước khi tạo trang, đổi thông tin, đăng bài hoặc bấm nút công khai: trình bản xem trước, xin xác nhận.
- Dừng ngay nếu gặp OTP, mật khẩu, CAPTCHA, quyền quản trị hoặc điều khoản cần người dùng tự xử lý.
- Không yêu cầu gửi mật khẩu, OTP, cookie, token qua trò chuyện.
- Báo rõ việc đã làm, việc chưa làm, đường dẫn trang.

### Checklist chất lượng
- [ ] 3 phương án khác nhau thật sự; phương án chốt có đủ mọi trường.
- [ ] Ảnh đúng kích thước, chữ tiếng Việt đúng dấu, logo rõ khi nhỏ, nội dung chính nằm trong vùng an toàn.
- [ ] Giọng văn, xưng hô, màu đúng hồ sơ tệp 04.
- [ ] Liên hệ đúng tệp 05, chỉ thông tin được công khai.
- [ ] Không có chứng nhận, đánh giá, số liệu chưa kiểm chứng.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** hồ sơ doanh nghiệp; file logo (nếu có); 3–5 ảnh sản phẩm/không gian thật; số điện thoại,
địa chỉ, giờ làm việc muốn công khai. Đăng nhập sẵn Facebook trên máy nếu muốn AI hỗ trợ thao tác.

1. Gõ `/ts-xay-dung-fanpage` kèm 1 câu (vd "tạo Fanpage mới cho tiệm bánh Mây").
2. Trả lời: đã có logo/ảnh bìa chưa, muốn nút "Nhắn tin" hay "Gọi ngay"…
3. Đọc 3 phương án tên – giới thiệu – nút hành động, chọn 1 (hoặc ghép: "tên phương án 1, giới thiệu phương án 2").
4. Chọn concept logo/ảnh bìa; nhận ảnh hoặc prompt ảnh.
5. Đọc bài ghim, 5 bài đầu, tin nhắn chào; sửa bằng lời, gõ "duyệt".
6. Chọn: tự làm theo hướng dẫn từng bước, hay cho phép AI thao tác (AI sẽ hỏi lại trước mỗi nút công khai).
7. Mở trang trên điện thoại kiểm tra lại ảnh bìa, nút, thông tin liên hệ.

## Câu lệnh mẫu
- `/ts-xay-dung-fanpage tạo Fanpage mới cho tiệm bánh Mây ở Đà Nẵng, chưa có logo`
- `/ts-xay-dung-fanpage làm lại Fanpage khóa học quay video bằng điện thoại cho rõ định vị hơn`
- `/ts-xay-dung-fanpage kiểm tra Fanpage spa Hồng còn thiếu gì trước khi chạy quảng cáo`
- `/ts-xay-dung-fanpage văn phòng luật nhỏ, muốn trang chuyên nghiệp, nút đặt lịch tư vấn`

## Kết quả nhận được
- Bảng thông tin Fanpage hoàn chỉnh (phương án đã chốt).
- Bộ nhận diện cần tạo hoặc tệp logo/ảnh bìa đã tạo (hoặc prompt ảnh).
- Gói nội dung khởi động: bài ghim, 5 bài đầu, FAQ, tin nhắn chào, trả lời nhanh, lịch 7 ngày.
- Checklist trạng thái: Đã có / Cần bổ sung / Chờ xác nhận.
- Hướng dẫn thao tác từng bước hoặc báo cáo việc AI đã làm trên Facebook.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-xay-dung-fanpage-<ten-trang-khong-dau>/`.
2. Lưu bảng thông tin Fanpage + gói nội dung khởi động + checklist trạng thái thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-xay-dung-fanpage
   ngay: <YYYY-MM-DD>
   chu-de: <tên Fanpage>
   the: [fanpage, facebook, nhan-dien]
   ---
   ```
   Kèm theo các file phụ (nếu có): `logo.png`, `anh-bia.png`, `prompt-anh.md`, `5-bai-dau.md`, `faq.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Fanpage <tên>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-xay-dung-fanpage · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Đề xuất cập nhật hồ sơ (hỏi trước khi ghi đè): link Fanpage, username, Page ID → `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`;
   logo mới → `03-tai-lieu-tho/dinh-kem/` và đường dẫn trong `01-ho-so/04-thuong-hieu-noi-dung.md`; FAQ → `02-san-pham-dich-vu.md`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không hỗ trợ quảng bá hàng hóa, dịch vụ hạn chế độ tuổi hoặc nội dung nguy hiểm cho người chưa thành niên.
- Không bịa chứng nhận, đánh giá, số liệu hay tuyên bố bảo đảm.
- Không xin mật khẩu, OTP, cookie, token; dừng khi gặp bước xác minh để người dùng tự làm.
- Không bấm tạo trang/đăng bài/công khai khi chưa có xác nhận rõ ràng.

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` · `/ts-thiet-ke-anh-quang-cao`
- Sau: `/ts-noi-dung-tu-dong-7-ngay` · `/ts-cham-soc-fanpage` · `/ts-lich-noi-dung` · `/ts-len-camp-facebook`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
