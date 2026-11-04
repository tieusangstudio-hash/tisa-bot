---
name: ts-tao-ebook
description: "Gọi bằng /ts-tao-ebook. Biến 1 chủ đề thành ebook PDF có thương hiệu: làm rõ đề bài, nghiên cứu từ tài liệu của bạn và web (có nguồn), duyệt dàn ý Phần - Chương, viết nội dung, chèn 3-5 hộp kêu gọi hành động, dựng PDF có bìa, logo, màu thương hiệu; tùy chọn đăng thành sách lật. Dùng khi cần quà tặng thu thông tin, ebook bán, tài liệu khóa học. Từ khóa: tạo ebook, viết sách điện tử, lead magnet ebook, ebook PDF, sách lật, flipbook, tài liệu tặng khách."
---

# /ts-tao-ebook — Tạo ebook có thương hiệu (Markdown → PDF)

> Từ một chủ đề, AI cùng bạn chốt đề bài, gom tư liệu thật, duyệt dàn ý, viết từng chương rồi dựng thành file
> PDF có bìa, logo, màu thương hiệu và các hộp kêu gọi hành động — sẵn sàng tặng, bán hoặc đăng thành sách lật.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Cần một ebook làm quà tặng để khách để lại số điện thoại/email (tầng 1 của phễu).
- Muốn đóng gói kiến thức thành ebook bán giá thấp hoặc tài liệu kèm khóa học.
- Có nhiều bài viết, ghi chú, bản chép video rời rạc và muốn gom thành một cuốn có cấu trúc.
- Cần bản PDF đẹp, đồng bộ thương hiệu từ một file Markdown đã viết sẵn.

**Không dùng khi:** chỉ cần một ảnh tóm tắt → `/ts-infographic`; cần lên ý tưởng và chọn loại quà tặng phù hợp
nhất trước → `/ts-pheu-qua-tang`; cần slide trình chiếu → `/ts-thiet-ke-thuyet-trinh`; cần tài liệu Word để
chỉnh sửa chung → dùng công cụ tạo tài liệu đang có.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md` (giọng văn, màu, logo), `05-muc-tieu-quy-tac-lien-he.md` (kênh liên hệ cho hộp CTA);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `tao-ebook`, `pheu-qua-tang`, `thiet-ke-pheu` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Ngoài ra liệt kê các tệp trong `03-tai-lieu-tho/` và `02-kien-thuc/` liên quan chủ đề — đây là nguồn tư liệu ưu tiên.

## Quy trình AI thực hiện

### Bước 1 — Làm rõ đề bài (hỏi gộp 1 lần, chỉ hỏi phần thiếu)
1. **Chủ đề** và **tên sách tạm** (nếu đã nghĩ ra).
2. **Người đọc** là ai, đang gặp khó khăn gì, đã biết đến đâu?
3. **Mục tiêu:** A. Quà tặng thu thông tin · B. Bán giá thấp · C. Tài liệu khóa học · D. Xây uy tín chuyên gia.
4. **Độ dài:** A. Ngắn 10–25 trang · B. Vừa 30–60 trang · C. Dài 60+ trang (xem bảng ở `references/cau-truc-va-cta.md`).
5. **Giọng:** A. Thân thiện · B. Chuyên gia · C. Truyền cảm hứng (bỏ qua nếu Bộ Não đã có).
6. **Hành động muốn người đọc làm** sau khi đọc (nhắn Zalo, đăng ký lớp, mua sản phẩm…) và kênh liên hệ.
7. **Khổ:** A. A5 — đọc trên điện thoại (mặc định) · B. A4 — để in.

### Bước 2 — Nghiên cứu tư liệu
1. Đọc tài liệu người dùng trong `03-tai-lieu-tho/` và `02-kien-thuc/` (chỉ đọc, không sửa). Tóm tắt ý chính có thể dùng.
2. Nếu môi trường có công cụ tìm kiếm web: tìm thêm số liệu, ví dụ, xu hướng mới; chỉ dùng nguồn rõ ràng.
   Ghi mỗi nguồn: tên · link · ngày truy cập.
3. Gom thành **bảng tư liệu**: ý chính · nguồn · dùng ở chương nào. Thông tin chưa chắc → `[CẦN KIỂM CHỨNG]`.
Không có công cụ web thì nói rõ và chỉ dùng tài liệu người dùng + kiến thức phổ thông (không đưa số liệu không nguồn).

### Bước 3 — Dàn ý Phần – Chương
Theo khung ở `references/cau-truc-va-cta.md` mục 2. Trình bày:
- Tên sách (3 phương án) + phụ đề.
- Dàn ý: Phần → Chương → 2–4 ý chính mỗi chương + ví dụ/bài tập dự kiến.
- Vị trí dự kiến của **3–5 hộp CTA** (ghi rõ sau chương nào và mời làm gì).
- Ước lượng số trang.

**CỔNG DUYỆT 1:** "Dàn ý này đã đúng chưa? Gõ *duyệt* để viết, hoặc nói chương cần thêm/bớt/đổi thứ tự."

### Bước 4 — Viết nội dung Markdown
- Viết từng phần; ebook dài (> 30 trang) thì gửi duyệt sau mỗi Phần thay vì viết hết một lần.
- Định dạng: `# Phần N: …` · `## Chương N: …` · `###` tiêu đề nhỏ · danh sách `-` / `1.` · `**đậm**` · `*nghiêng*` ·
  ảnh `![chú thích](anh.png)` · hộp mẹo `> [!MEO] Tiêu đề` · hộp CTA `> [!CTA] Tiêu đề` (dòng `>` tiếp theo là nội dung).
- Đầu file là khối thông tin bìa (xem mẫu `templates/ebook-mau.md`): `ten_sach`, `phu_de`, `tac_gia`, `nhan_bia`,
  `logo`, `mau_chinh`, `mau_nhan`, `kho`, `kieu_chu`, `lien_he`. Màu và logo lấy từ `04-thuong-hieu-noi-dung.md`.
- Đoạn văn 2–4 câu, mỗi chương có ví dụ hoặc bài tập; số liệu ghi nguồn ngay sau câu; cuối sách có **Nguồn tham khảo**.
- Chạy checklist ở `references/cau-truc-va-cta.md` mục 6.

**CỔNG DUYỆT 2:** "Nội dung đã ổn chưa? Gõ *duyệt* để dựng PDF."

### Bước 5 — Dựng PDF
Lưu file Markdown (vd `ebook.md`), đặt logo và ảnh minh họa cùng thư mục, rồi chạy:
- macOS: `python3 scripts/tao_pdf.py ebook.md`
- Windows: `py scripts\tao_pdf.py ebook.md`
- Tùy chọn: `--kho A4` · `--kieu-chu serif` (chữ có chân) · `--mau-chinh "#123B6D" --mau-nhan "#F5B700"` ·
  `--logo logo.png` · `--khong-muc-luc` · `--chi-html` (chỉ tạo HTML) · `--chrome "<đường dẫn Chrome/Edge>"`.

Script chỉ dùng thư viện có sẵn của Python: tự chuyển Markdown → HTML theo mẫu `templates/bia-va-noi-dung.html`
(bìa, mục lục tự động, mỗi Phần một trang mở đầu, mỗi Chương sang trang mới, số trang), rồi in ra PDF bằng
Playwright hoặc Chrome/Edge chạy ẩn. Script báo số chương, số hộp CTA (cảnh báo nếu ngoài 3–5) và ảnh bị thiếu.
Không dựng được PDF thì vẫn có file HTML + hướng dẫn mở bằng Chrome → Ctrl+P → *Lưu dưới dạng PDF*.

Kiểm tra PDF (nếu môi trường xem được): bìa đúng tên/logo/màu · không trang trắng thừa · hộp CTA không bị cắt
đôi · chữ tiếng Việt không lỗi dấu.

**CỔNG DUYỆT 3:** gửi PDF, hỏi "Gõ *duyệt* để lưu, hoặc nói chỗ cần sửa (màu bìa, đổi khổ A4, thêm ảnh…)."

### Bước 6 — (Tùy chọn) Đăng thành sách lật
Hướng dẫn thao tác trên Heyzine hoặc FlipHTML5 theo `references/cau-truc-va-cta.md` mục 7 — người dùng tự đăng,
AI không cần tài khoản hay API. Sau đó gợi ý gắn link vào chuỗi gửi quà (`/ts-pheu-qua-tang`, `/ts-giao-hang-tu-dong`).

## Ví dụ minh họa (doanh nghiệp giả định — chỉ để tham khảo)
**Spa Hồng** cần quà tặng thu số điện thoại cho chiến dịch trị mụn.
- Đề bài: *"7 thói quen buổi tối giúp da bớt mụn"* · người đọc: nữ 22–35 tuổi da dầu mụn · mục tiêu A · ngắn · giọng thân thiện · khổ A5.
- Dàn ý: Phần 1 *Hiểu làn da của bạn* (2 chương) · Phần 2 *7 thói quen* (7 chương ngắn) · Lời kết.
- 4 hộp CTA: sau chương "Vì sao rửa mặt kỹ vẫn mụn" → mời soi da miễn phí; sau thói quen số 3 → mời vào nhóm Zalo;
  sau thói quen số 6 → bảng theo dõi 14 ngày; lời kết → đặt lịch tư vấn.
- Lệnh dựng: `python3 scripts/tao_pdf.py 7-thoi-quen.md --mau-chinh "#8E2453" --mau-nhan "#F7B7C8"` → khoảng 20 trang A5.
- Mọi lời khuyên chăm sóc da ghi rõ "tham khảo, không thay thế tư vấn bác sĩ da liễu".

## Hướng dẫn cho học viên (làm theo từng bước)
1. **Chuẩn bị trước:** thả tài liệu sẵn có (bài viết cũ, ghi chú, bản chép video, ảnh) vào `03-tai-lieu-tho/`
   của Bộ Não; chuẩn bị file logo PNG; nghĩ trước hành động bạn muốn người đọc làm sau khi đọc xong.
2. Gõ `/ts-tao-ebook` kèm chủ đề và người đọc.
3. Trả lời các câu hỏi (chọn chữ cái A-B-C-D).
4. Xem dàn ý và 3 tên sách AI đề xuất. Sửa bằng lời ("bỏ chương 5", "thêm chương về giá") → gõ **duyệt**.
5. Đọc từng phần AI viết, sửa bằng lời → gõ **duyệt**. Điền các chỗ `[CẦN BỔ SUNG]` bằng thông tin thật.
6. Nhận file PDF. Mở trên điện thoại xem thử bìa, mục lục, các hộp CTA.
7. (Tùy chọn) Làm theo hướng dẫn đăng sách lật để có đường link chia sẻ.
8. Gõ **duyệt** để lưu vào Bộ Não. Muốn sửa sau này: sửa file `.md` rồi nhờ AI dựng lại PDF.

## Câu lệnh mẫu
- `/ts-tao-ebook làm ebook tặng khách '10 món bánh không cần lò' cho mẹ bỉm, khoảng 20 trang`
- `/ts-tao-ebook gom các bài viết trong 03-tai-lieu-tho thành ebook 'Quay video bán hàng bằng điện thoại', khổ A5`
- `/ts-tao-ebook ebook bán 99k về cách chọn kem chống nắng cho da dầu, giọng chuyên gia, có nguồn tham khảo`
- `/ts-tao-ebook tài liệu khóa học kế toán cho chủ shop online, khổ A4, chữ có chân`
- `/ts-tao-ebook dựng lại PDF từ file ebook.md, đổi màu bìa sang xanh navy và thêm logo`

## Kết quả nhận được
- Bảng tư liệu và danh sách nguồn tham khảo.
- Dàn ý Phần – Chương đã duyệt, 3 phương án tên sách.
- File `ebook.md` (sửa được, dựng lại được bất cứ lúc nào) + file HTML + file **PDF có bìa thương hiệu**,
  mục lục, 3–5 hộp CTA.
- (Tùy chọn) Hướng dẫn đăng sách lật và gắn link vào chuỗi gửi quà.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-tao-ebook-<chu-de-khong-dau>/`.
2. Lưu tóm tắt ebook (đề bài, dàn ý, vị trí và nội dung các hộp CTA, đường dẫn file) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-tao-ebook
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `ebook.md` (bản nguồn), `ebook.pdf`, `ebook.html`, `nguon.md` (danh sách nguồn), logo và ảnh minh họa đã dùng, link sách lật.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-tao-ebook · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Kiến thức đã nghiên cứu có nguồn là tri thức dùng lại: đề xuất lưu bảng tư liệu vào `02-kien-thuc/san-pham/<chu-de>.md` hoặc `02-kien-thuc/khach-hang/` (hỏi trước khi ghi). Nếu ebook là quà tặng mới, đề xuất bổ sung vào `01-ho-so/02-san-pham-dich-vu.md` (hỏi trước khi ghi đè).
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bịa số liệu, nghiên cứu, câu chuyện khách hàng, lời chứng thực. Thiếu → `[CẦN BỔ SUNG]` / `[CẦN KIỂM CHỨNG]`.
- Tôn trọng bản quyền: không chép nguyên văn sách/bài viết của người khác; trích ngắn có ghi nguồn; ảnh phải có quyền dùng.
- Ngành sức khỏe, làm đẹp, tài chính, pháp lý: thêm câu "nội dung tham khảo, không thay thế tư vấn chuyên môn";
  không hứa chữa khỏi, lợi nhuận đảm bảo.
- Ưu đãi và hạn chót trong hộp CTA phải có thật.
- Không đăng tài liệu nội bộ, có dữ liệu khách hàng lên dịch vụ sách lật công khai.
- Không có mạng, PDF dùng font dự phòng có sẵn trên máy (đủ dấu tiếng Việt); muốn đúng font Be Vietnam Pro / Lora
  thì cài font vào máy.

## Skill liên quan
- Trước: `/ts-chan-dung-khach-hang` · `/ts-pheu-qua-tang` (chọn loại quà tặng) · `/ts-thiet-ke-pheu`
- Sau: `/ts-trang-ban-hang` (trang nhận ebook 8 khối) · `/ts-giao-hang-tu-dong` (tự gửi ebook) ·
  `/ts-email-cham-soc` · `/ts-infographic` (ảnh quảng bá ebook)

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
