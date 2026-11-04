---
name: ts-thiet-ke-anh-quang-cao
description: "Gọi bằng /ts-thiet-ke-anh-quang-cao. Thiết kế ảnh quảng cáo đúng thương hiệu: đọc màu, logo, font từ hồ sơ (chưa có màu thì chọn 1 trong 6 bộ: đen vàng, gradient tím, xanh, cam vàng, đỏ cam, trắng cam), viết creative brief, đưa 2–4 concept khác nhau để chọn, rồi mỗi ảnh một prompt sao chép được và tạo/chỉnh ảnh trực tiếp nếu có công cụ tạo ảnh. Dùng cho ảnh Facebook/TikTok Ads, banner, poster, thumbnail, ảnh bìa, khung video. Từ khóa: ảnh quảng cáo, thiết kế banner, poster, prompt ảnh, thumbnail, ảnh bìa, creative quảng cáo, sửa ảnh quảng cáo."
---

# /ts-thiet-ke-anh-quang-cao — Thiết kế ảnh quảng cáo

> AI đọc màu – logo – font của thương hiệu, đề xuất 2–4 concept khác nhau để bạn chọn, rồi viết **mỗi ảnh một
> prompt** (sao chép dán vào công cụ tạo ảnh) hoặc tạo ảnh luôn nếu môi trường có công cụ — đúng tỷ lệ, đúng
> chữ tiếng Việt, đúng thương hiệu.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Cần ảnh chạy quảng cáo Facebook/Instagram/TikTok, banner web, poster sự kiện, thumbnail YouTube.
- Cần ảnh bìa Fanpage, khung (frame) cho video, ảnh khuyến mãi.
- Có ảnh quảng cáo cũ cần chỉnh: đổi chữ, đổi tỷ lệ, làm rõ CTA.
- Muốn nhiều phiên bản ảnh để thử nghiệm A/B.

**Không dùng khi:** cần ảnh kiến thức nhiều ý, dạng "5 bước", "checklist" → `/ts-infographic`.
Cần cả bộ 7 bài đăng có ảnh → `/ts-noi-dung-tu-dong-7-ngay`. Cần video → `/ts-prompt-video-ai`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `04-thuong-hieu-noi-dung.md` (màu, font, logo, phong cách hình ảnh, nhân vật đại diện), `02-san-pham-dich-vu.md` (offer, giá, CTA), `03-khach-hang-muc-tieu.md` (nỗi đau, mong muốn);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `thiet-ke-anh-quang-cao` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** logo và ảnh sản phẩm thường nằm trong `03-tai-lieu-tho/dinh-kem/` (đường dẫn ghi trong tệp 04).
Đọc thêm kết quả `/ts-viet-quang-cao` (tiêu đề, góc nội dung đã có) nếu có.

## Quy trình AI thực hiện

### Bước 1 — Đọc brief và nhận diện
Xác định: mục tiêu ảnh (bán / kéo tin nhắn / thu lead / nhận diện), sản phẩm, khách hàng, nền tảng và vị trí
đặt, tỷ lệ, bộ nhận diện.
- **Màu:** lấy từ tệp 04. **Chưa có màu** → hỏi chọn 1 trong 6 bộ (bảng mã màu trong
  `references/bo-mau-kich-thuoc-prompt.md`):
  ```text
  Bạn muốn dùng bộ màu nào?
  A. Đen vàng   B. Gradient tím   C. Xanh   D. Cam vàng   E. Đỏ cam   F. Trắng cam
  ```
- **Logo, font:** lấy từ tệp 04; chưa có logo → không tự vẽ logo giả, chỉ dùng tên thương hiệu dạng chữ.

### Bước 2 — Kiểm kê tài sản
Logo, ảnh sản phẩm, ảnh nhân vật, chữ bắt buộc (giá, ưu đãi, hạn), tuyên bố được phép nói. Thiếu ảnh sản phẩm
thật → hỏi; không tự vẽ sản phẩm khác hình dạng thật.

### Bước 3 — Creative brief
Viết ngắn: mục tiêu · khách hàng · offer · kênh/vị trí · tỷ lệ + kích thước · tài sản bắt buộc · giới hạn
tuyên bố (claim). Xác định **thứ bậc thị giác** trước: thông điệp chính → hình chính → bằng chứng → CTA → nhận diện.

### Bước 4 — Đưa 2–4 concept (cổng duyệt 1)
Mỗi concept khác nhau về **góc tiếp cận, bố cục, hình ảnh** (không chỉ đổi màu). Dùng mẫu concept trong
reference: góc tiếp cận, thông điệp chính, CTA, bố cục, hình chính, màu, tỷ lệ, **giả thuyết A/B**.
👉 Chờ người dùng chọn concept (có thể chọn nhiều để test). **Chưa tạo ảnh trước khi chọn.**

### Bước 5 — Viết prompt: mỗi ảnh = 1 prompt
- Mỗi ảnh một khối mã riêng (có nút sao chép), theo mẫu trong `references/bo-mau-kich-thuoc-prompt.md`:
  tỷ lệ + kích thước, chủ thể, bố cục, phong cách, màu, font, **chữ trên ảnh nguyên văn tiếng Việt có dấu**,
  vị trí logo, điều cần tránh.
- Prompt mô tả bằng tiếng Anh; chữ hiện trên ảnh giữ tiếng Việt trong ngoặc kép.
- Nhiều kích thước cho cùng concept → mỗi kích thước một prompt riêng.

### Bước 6 — Tạo hoặc chỉnh ảnh (nếu có công cụ)
- Môi trường có công cụ tạo ảnh và người dùng yêu cầu tạo → tạo ngay theo từng prompt.
- Chỉnh ảnh có sẵn → xem ảnh gốc trước, chỉ sửa phần được yêu cầu, giữ nguyên sản phẩm/gương mặt.
- Không có công cụ → giao prompt + hướng dẫn dán vào công cụ tạo ảnh người dùng đang có.
- Công cụ viết sai dấu tiếng Việt → tạo bản không chữ rồi hướng dẫn đặt chữ bằng Canva/PowerPoint.

### Bước 7 — Kiểm tra và bàn giao (cổng duyệt 2)
Chạy checklist (cuối reference): chính tả, vùng an toàn, tương phản, thứ bậc, đọc được trên điện thoại, trung thực
sản phẩm, quyền sử dụng tài sản. Bàn giao ảnh đúng kích thước + prompt/chữ + **ghi rõ nội dung cần người dùng
xác minh** (giá, hạn ưu đãi, tuyên bố). Kèm giả thuyết A/B cho mỗi concept.
Không tự thay creative đang chạy hoặc xuất bản nếu chưa được duyệt.

### Quy chuẩn chung
- Mỗi ảnh **một thông điệp chính** và **một CTA**.
- Không nhồi chữ; không thêm logo, feedback, chứng nhận, huy hiệu chưa được cung cấp.
- Không làm sai hình dáng sản phẩm hoặc gương mặt tham chiếu.
- Tách **tỷ lệ ảnh tổng** và **tỷ lệ khung video bên trong** khi làm khung video.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** ảnh sản phẩm thật (nền sạch càng tốt), file logo PNG nền trong (nếu có), nội dung ưu đãi/giá
chính xác, biết ảnh dùng ở đâu (bảng tin, story, ảnh bìa…).

1. Gõ `/ts-thiet-ke-anh-quang-cao` kèm sản phẩm + nơi đăng (vd "ảnh quảng cáo bánh kem Trung thu, đăng bảng tin Facebook").
2. Đính kèm ảnh sản phẩm/logo. Chưa có màu thương hiệu → chọn 1 trong 6 bộ màu (gõ chữ cái).
3. Đọc 2–4 concept, chọn 1 hoặc vài concept muốn thử.
4. Bấm sao chép từng prompt → dán vào công cụ tạo ảnh bạn dùng (hoặc để AI tạo luôn nếu có công cụ).
5. Kiểm tra chữ trên ảnh: sai dấu → báo AI, AI sửa prompt hoặc hướng dẫn đặt chữ bằng Canva.
6. Xác minh lại giá, hạn ưu đãi trên ảnh rồi gõ "duyệt".
7. Dùng ảnh chạy quảng cáo: `/ts-len-camp-facebook` hoặc `/ts-chay-tiktok-ads`.

## Câu lệnh mẫu
- `/ts-thiet-ke-anh-quang-cao ảnh quảng cáo bánh kem Trung thu tiệm bánh Mây, bảng tin 4:5 và story 9:16`
- `/ts-thiet-ke-anh-quang-cao poster khai giảng khóa học quay video bằng điện thoại, màu gradient tím`
- `/ts-thiet-ke-anh-quang-cao thumbnail YouTube cho video "3 lỗi khi chăm da mùa hanh khô" của spa Hồng`
- `/ts-thiet-ke-anh-quang-cao sửa ảnh quảng cáo này: đổi giá thành 299k và làm nút CTA nổi hơn` (kèm ảnh)
- `/ts-thiet-ke-anh-quang-cao 3 phiên bản ảnh để test A/B cho dịch vụ dọn nhà theo giờ`

## Kết quả nhận được
- Creative brief ngắn.
- 2–4 concept có giả thuyết A/B.
- Mỗi ảnh một prompt sao chép được (tiếng Anh + chữ tiếng Việt nguyên văn), theo từng kích thước.
- Ảnh hoàn chỉnh (nếu có công cụ tạo ảnh) + danh sách nội dung cần xác minh.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-thiet-ke-anh-quang-cao-<chu-de-khong-dau>/`.
2. Lưu creative brief + concept đã chọn + toàn bộ prompt + giả thuyết A/B thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-thiet-ke-anh-quang-cao
   ngay: <YYYY-MM-DD>
   chu-de: <sản phẩm — chiến dịch>
   the: [anh-quang-cao, creative, <kênh>]
   ---
   ```
   Kèm theo các file phụ (nếu có): ảnh đã tạo (`concept-a-4x5.png`, `concept-a-9x16.png`…), `prompts.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Ảnh QC <chủ đề>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-thiet-ke-anh-quang-cao · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Người dùng vừa chọn bộ màu/font mới mà tệp 04 chưa có → đề xuất ghi vào mục *Màu thương hiệu*, *Font chữ* của
   `01-ho-so/04-thuong-hieu-noi-dung.md` (hỏi trước khi ghi đè). Concept thắng A/B → đề xuất lưu vào
   `02-kien-thuc/cong-thuc/creative-hieu-qua.md`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không thêm logo, feedback, chứng nhận, huy hiệu, số liệu người dùng chưa cung cấp.
- Chỉ dùng ảnh, font, nhân vật có quyền sử dụng; không dùng hình người nổi tiếng/thương hiệu khác.
- Tuân thủ chính sách quảng cáo: không ảnh trước–sau gây hiểu nhầm, không nhắm đặc điểm cơ thể tiêu cực.
- Không thay creative đang chạy hay đăng ảnh khi chưa được duyệt.

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` (màu, logo) · `/ts-viet-quang-cao` (tiêu đề, góc nội dung)
- Sau: `/ts-len-camp-facebook` · `/ts-chay-tiktok-ads` · `/ts-xay-dung-fanpage` · `/ts-bao-cao-facebook-ads`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
