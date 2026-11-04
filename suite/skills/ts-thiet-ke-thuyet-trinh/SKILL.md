---
name: ts-thiet-ke-thuyet-trinh
description: "Gọi bằng /ts-thiet-ke-thuyet-trinh. Lập mạch nội dung, storyboard từng slide, viết và thiết kế bài thuyết trình PowerPoint/Google Slides đúng màu, font, logo thương hiệu: bài bán hàng, webinar, bài giảng khóa học, proposal, báo cáo, hồ sơ năng lực; có biểu đồ, slide tương tác, ghi chú người nói; kiểm tra tràn chữ trước khi giao. Dùng khi cần slide, file PPT/PPTX, bài thuyết trình hoặc chỉnh bộ slide có sẵn. Từ khóa: làm slide, thuyết trình, powerpoint, google slides, bài giảng, webinar, proposal, hồ sơ năng lực, sửa slide."
---

# /ts-thiet-ke-thuyet-trinh — Thiết kế thuyết trình

> AI lập mạch câu chuyện trước, rồi storyboard từng slide (mỗi slide một ý, tiêu đề là kết luận), thiết kế
> đúng nhận diện thương hiệu, viết ghi chú người nói và kiểm tra hiển thị trước khi giao file.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Chuẩn bị buổi giới thiệu sản phẩm, webinar, buổi học, hội thảo.
- Gửi proposal / báo giá dạng slide cho khách doanh nghiệp.
- Làm báo cáo kết quả tháng/quý cho đối tác, nhân viên.
- Làm hồ sơ năng lực công ty.
- Có bộ slide cũ cần làm lại cho gọn, đẹp, đúng thương hiệu.

**Không dùng khi:** cần văn bản hợp đồng/báo giá dạng Word → `/ts-soan-hop-dong`. Cần ebook/tài liệu đọc → `/ts-tao-ebook`.
Cần một ảnh kiến thức đơn lẻ → `/ts-infographic`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md` (năng lực, bằng chứng), `02-san-pham-dich-vu.md` (offer, giá), `04-thuong-hieu-noi-dung.md` (màu, font, logo, giọng văn), `05-muc-tieu-quy-tac-lien-he.md` (liên hệ cho slide cuối);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `thiet-ke-thuyet-trinh` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** báo cáo/số liệu dùng cho slide thường nằm trong `04-ket-qua/` (vd kết quả `/ts-phan-tich-doanh-thu`)
hoặc `03-tai-lieu-tho/`; logo trong `03-tai-lieu-tho/dinh-kem/`.

## Quy trình AI thực hiện

### Bước 1 — Xác định yêu cầu
Người xem là ai · mục tiêu (họ hiểu/làm gì sau buổi) · thời lượng · số slide · bối cảnh trình chiếu (phòng lớn,
online, gửi file đọc) · CTA cuối · định dạng (PowerPoint `.pptx`, Google Slides, PDF). Thiếu → hỏi tối đa 4 câu, có
gợi ý A–D. Có bộ slide tham chiếu → hỏi được giữ cấu trúc/nhận diện đến đâu.

### Bước 2 — Lập mạch câu chuyện (story arc)
Khung chung: **mở vấn đề → bằng chứng → giải pháp → hành động**. Chọn mạch theo loại bài trong
`references/mach-noi-dung-va-bo-cuc.md` (bán hàng, webinar, bài giảng, proposal, báo cáo, hồ sơ năng lực).

### Bước 3 — Storyboard từng slide (cổng duyệt 1)
Bảng: số slide · **tiêu đề nêu kết luận** · mục đích · người xem hiểu/làm gì sau slide · bố cục · hình/biểu đồ ·
ý chính ghi chú người nói. 👉 Trình storyboard, chờ "duyệt" (thêm/bớt/đổi thứ tự slide) trước khi thiết kế.

### Bước 4 — Viết nội dung slide
Mỗi slide một ý; dùng biểu đồ/hình thay đoạn văn khi phù hợp; chữ trên slide ngắn, phần giải thích đưa vào ghi
chú người nói. Viết đúng giọng văn, xưng hô ở tệp 04.

### Bước 5 — Thiết kế
Áp dụng màu, font, logo, lưới, cấp bậc chữ nhất quán (quy chuẩn trong reference); ưu tiên đọc được từ xa. Chọn
bố cục theo loại nội dung (thư viện bố cục trong reference); chỉ dùng hình, sơ đồ, biểu đồ khi giúp hiểu nhanh
hơn chữ; bỏ trang trí không phục vụ nội dung.
- Môi trường có công cụ tạo file trình chiếu (PowerPoint/Google Slides) → tạo file thật.
- Không có → giao nội dung từng slide + hướng dẫn dựng bằng PowerPoint/Google Slides/Canva (bố cục, màu, cỡ chữ).

### Bước 6 — Ghi chú người nói và tương tác
Ghi chú cho mọi slide nội dung (khoảng 1–2 phút nói/slide). Bài đào tạo → thêm slide tương tác (câu hỏi khởi
động, kiểm tra nhanh, bài tập, "bạn sẽ làm gì hôm nay").

### Bước 7 — Render và kiểm định (cổng duyệt 2)
Render toàn bộ (xuất ảnh/PDF xem trước nếu môi trường cho phép), kiểm tra theo checklist trong reference: tràn
chữ, cắt hình, tương phản, tỷ lệ, chính tả, biểu đồ, ghi chú. Đánh dấu số liệu, trích dẫn, chứng nhận, case study
chưa xác nhận là `[CẦN XÁC NHẬN]` — không trình bày giả định như sự thật.
👉 Giao bản xem trước, chờ "duyệt" rồi mới giao file cuối.

### Checklist chất lượng
- [ ] Mạch rõ ràng; mỗi slide một ý; tiêu đề là kết luận.
- [ ] Đúng màu, font (có dấu tiếng Việt), logo theo hồ sơ.
- [ ] Cỡ chữ đạt chuẩn đọc từ xa; không tràn chữ; tương phản đủ.
- [ ] Không bịa số liệu, case study; dữ liệu có nguồn.
- [ ] Có ghi chú người nói; có slide CTA cuối.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** mục tiêu buổi trình bày, thời lượng, người nghe; tài liệu/số liệu muốn đưa vào; logo; bộ slide cũ
nếu muốn làm lại.

1. Gõ `/ts-thiet-ke-thuyet-trinh` kèm mục đích (vd "webinar 45 phút giới thiệu khóa học").
2. Trả lời vài câu: ai nghe, bao nhiêu phút, cần file PowerPoint hay Google Slides.
3. Đọc storyboard (danh sách slide + tiêu đề); thêm/bớt/đổi thứ tự bằng lời, gõ "duyệt".
4. Xem bản xem trước; sửa bằng lời ("slide 5 nhiều chữ quá", "đổi biểu đồ thành cột").
5. Kiểm tra lại các chỗ AI đánh dấu `[CẦN XÁC NHẬN]` (số liệu, tên khách hàng…).
6. Gõ "duyệt" để nhận file cuối và lưu vào Bộ Não.
7. Tập nói theo ghi chú người nói dưới mỗi slide.

## Câu lệnh mẫu
- `/ts-thiet-ke-thuyet-trinh webinar 45 phút giới thiệu khóa học quay video bằng điện thoại, có slide bán hàng cuối`
- `/ts-thiet-ke-thuyet-trinh proposal dịch vụ dọn dẹp văn phòng gửi công ty khách, 12 slide, file PowerPoint`
- `/ts-thiet-ke-thuyet-trinh báo cáo kết quả kinh doanh quý 3 của tiệm bánh cho đối tác góp vốn`
- `/ts-thiet-ke-thuyet-trinh làm lại bộ slide này cho gọn và đúng màu thương hiệu` (kèm file)
- `/ts-thiet-ke-thuyet-trinh bài giảng 60 phút "Chăm sóc da cơ bản" cho học viên spa, có câu hỏi tương tác`

## Kết quả nhận được
- Storyboard đã duyệt (mạch + từng slide).
- File trình chiếu (`.pptx` / Google Slides / PDF) hoặc nội dung từng slide + hướng dẫn dựng.
- Ghi chú người nói cho mọi slide nội dung; slide tương tác (nếu là đào tạo).
- Danh sách điểm `[CẦN XÁC NHẬN]`.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-thiet-ke-thuyet-trinh-<chu-de-khong-dau>/`.
2. Lưu storyboard + nội dung từng slide + ghi chú người nói thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-thiet-ke-thuyet-trinh
   ngay: <YYYY-MM-DD>
   chu-de: <tên bài thuyết trình>
   the: [thuyet-trinh, slide, <loại bài>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `<ten-bai>.pptx` hoặc đường dẫn Google Slides, `<ten-bai>.pdf`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Slide <tên bài>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-thiet-ke-thuyet-trinh · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Bộ slide dùng lại nhiều lần (hồ sơ năng lực, slide giới thiệu chuẩn) → đề xuất ghi đường dẫn vào
   `02-kien-thuc/san-pham/` để các lệnh khác dùng lại — hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bịa số liệu, case study, logo khách hàng, chứng nhận.
- Với bộ slide tham chiếu của người khác: chỉ giữ cấu trúc/nhận diện trong phạm vi người dùng có quyền.
- Ảnh, font, biểu tượng phải có quyền sử dụng.
- Không gửi/chia sẻ file ra ngoài khi người dùng chưa yêu cầu.

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` · `/ts-phan-tich-doanh-thu` (số liệu báo cáo) · `/ts-dinh-gia-offer` (slide offer)
- Sau: `/ts-pheu-qua-tang` (dùng slide làm quà) · `/ts-trang-ban-hang` · `/ts-email-cham-soc` (gửi tài liệu sau webinar)

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
