---
name: ts-infographic
description: "Gọi bằng /ts-infographic. Tự thiết kế infographic bằng HTML/CSS rồi xuất ảnh PNG sẵn đăng (dọc 1080x1350, vuông 1080x1080, story 1080x1920), 6 bộ màu, chữ tiếng Việt chuẩn, đồng bộ thương hiệu. Dùng khi muốn làm ảnh kiến thức, ảnh N bước, ảnh tóm tắt, carousel cho Facebook, Instagram, Threads. Từ khóa: infographic, ảnh kiến thức, ảnh N bước, ảnh tóm tắt, carousel, đồ họa thông tin, HTML ra ảnh, thiết kế ảnh content."
---

# /ts-infographic — Thiết kế infographic bằng HTML, xuất ảnh PNG

> Bạn chỉ đưa chủ đề hoặc nội dung thô. AI chốt thông điệp, chia ý thành 3–6 thẻ, đổ vào mẫu HTML theo bộ màu
> thương hiệu và xuất thành ảnh PNG sắc nét — không cần mở Canva hay Photoshop.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Muốn biến một bài viết, video, ghi chú thành ảnh kiến thức dễ lưu, dễ chia sẻ.
- Cần ảnh dạng "N bước", "N lỗi thường gặp", "N mẹo", checklist, so sánh nên/không nên.
- Cần cả loạt ảnh cùng bộ nhận diện (carousel 5–10 ảnh) đăng Facebook, Instagram, Threads, LinkedIn.
- Cần ảnh story 9:16 tóm tắt nhanh một chủ đề.

**Không dùng khi:** cần ảnh quảng cáo bán hàng có sản phẩm, người mẫu → `/ts-thiet-ke-anh-quang-cao`;
cần slide thuyết trình nhiều trang → `/ts-thiet-ke-thuyet-trinh`; cần tài liệu dài nhiều chương → `/ts-tao-ebook`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `04-thuong-hieu-noi-dung.md` (màu sắc, logo, giọng văn), `03-khach-hang-muc-tieu.md`, `05-muc-tieu-quy-tac-lien-he.md` (website, fanpage, Zalo để ghi ở chân ảnh);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `infographic` hoặc từ khóa) để không làm lại từ đầu và giữ đồng bộ bộ màu đã dùng.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Logo: tìm file ảnh logo được nhắc trong `04-thuong-hieu-noi-dung.md` hoặc trong `03-tai-lieu-tho/dinh-kem/`.
Không thấy thì dùng tên thương hiệu dạng chữ.

## Quy trình AI thực hiện

### Bước 1 — Làm rõ đề bài (hỏi gộp 1 lần, chỉ hỏi phần thiếu)
1. Chủ đề / nội dung thô là gì? (dán bài viết, ghi chú, link video đã có bản chữ…)
2. Ai xem và xem xong cần biết/làm được gì?
3. Khổ ảnh: A. Dọc 1080×1350 (bài đăng — mặc định) · B. Vuông 1080×1080 · C. Story 1080×1920.
4. Bộ màu (nếu Bộ Não chưa có màu thương hiệu): A. Đen vàng · B. Gradient tím · C. Xanh · D. Cam vàng ·
   E. Đỏ cam · F. Trắng cam — xem gợi ý ngành ở `references/bo-mau.md`.
5. Một ảnh hay cả loạt (carousel bao nhiêu ảnh)?

### Bước 2 — Chốt thông điệp (80% nội dung)
Viết bản nháp chữ, **chưa thiết kế**:
- **Câu thông điệp:** "Xem xong, người đọc sẽ …"
- **Nhãn nhỏ** (1–2 từ: Cẩm nang, Checklist, Sai lầm, Mẹo…).
- **Tiêu đề** ≤ 12 chữ, có con số nếu là danh sách; đánh dấu 2–4 chữ cần nhấn màu.
- **Mô tả** ≤ 20 chữ (không bắt buộc).
- **3–6 thẻ:** tên ≤ 6 chữ + nội dung ≤ 14 chữ. Nhiều hơn 6 ý → chia thành nhiều ảnh.
- **Chân ảnh:** lời kêu gọi ngắn ("Lưu lại để làm theo") + website/fanpage/Zalo từ Bộ Não.
- Chọn dạng bố cục: N bước/N điểm (mẫu có sẵn) · so sánh 2 cột · cấp độ · con số nổi bật · checklist
  (xem `references/nguyen-tac-thiet-ke.md` mục 8).

Kiểm tra: số liệu nào cũng có nguồn; không hứa hẹn tuyệt đối; chữ có dấu đầy đủ.

**CỔNG DUYỆT 1:** "Nội dung chữ đã đúng chưa? Gõ *duyệt* để thiết kế, hoặc nói chỗ cần sửa."

### Bước 3 — Dựng HTML từ mẫu
1. Sao chép `templates/danh-sach-buoc.html` thành file mới, đặt tên không dấu, vd `5-buoc-quay-video.html`
   (loạt ảnh: `01-...html`, `02-...html` trong cùng thư mục).
2. Đổi `data-kho` và `data-mau` trên thẻ `<body>`. Có màu thương hiệu → điền vào khối `<style id="mau-thuong-hieu">`.
3. Thay chữ ở các chỗ ghi `SỬA:`; giữ hoặc nhân bản thẻ `<li class="the">` cho đủ 3–6 thẻ, đánh số lại.
4. Có logo → đặt file logo cạnh file HTML, thay chữ thương hiệu bằng `<img class="logo" src="logo.png" alt="Logo">`.
5. Dạng bố cục khác: giữ nguyên phần `<head>`, biến màu, đầu và chân; chỉ viết lại phần `<section class="than">`.
6. Chữ chép từ Word/PDF: chuẩn hóa Unicode dựng sẵn (NFC) trước khi dán.

### Bước 4 — Xuất ảnh PNG
Chạy script (không cần cài thêm gì nếu máy có Chrome hoặc Edge):
- macOS: `python3 scripts/xuat_anh.py 5-buoc-quay-video.html`
- Windows: `py scripts\xuat_anh.py 5-buoc-quay-video.html`
- Cả loạt trong một thư mục: `python3 scripts/xuat_anh.py thu-muc-anh/`
- Đổi khổ nhanh: thêm `--kho 1080x1080` · ảnh nét gấp đôi: thêm `--scale 2`
- Không tìm thấy trình duyệt: thêm `--chrome "<đường dẫn tới chrome.exe hoặc msedge.exe>"`

Script tự thử Playwright → Chrome/Edge chạy ẩn; tự dùng font dự phòng nếu không tải được Google Fonts; báo
**"Nội dung bị TRÀN"** nếu chữ dài quá khung (ảnh có viền đỏ) → rút gọn chữ hoặc bớt thẻ rồi xuất lại.

Nếu môi trường không chạy được lệnh: giao file HTML, hướng dẫn người dùng mở bằng Chrome/Edge → bấm F12 →
bật chế độ thiết bị (Ctrl+Shift+M, macOS Cmd+Shift+M) → nhập kích thước khổ ảnh → menu ⋮ → *Capture screenshot*.

### Bước 5 — Tự kiểm tra ảnh
Mở ảnh vừa xuất (nếu môi trường xem được ảnh) và kiểm:
- [ ] Đúng kích thước khổ đã chọn, không viền đỏ báo tràn.
- [ ] Đọc được trong 5 giây: tiêu đề → thẻ → chân ảnh.
- [ ] Không lỗi dấu tiếng Việt (ư, ơ, ă, đ, dấu chồng), không chữ bị cắt.
- [ ] Tương phản đủ: chữ phụ vẫn đọc được trên điện thoại.
- [ ] Màu nhấn chỉ dùng cho số thứ tự và 2–4 chữ tiêu đề.
- [ ] Loạt ảnh: cùng bộ màu, cùng vị trí logo, đánh số trang nếu là carousel.

**CỔNG DUYỆT 2:** gửi ảnh, hỏi "Gõ *duyệt* để lưu, hoặc nói chỗ cần sửa (đổi màu, đổi khổ, ngắn chữ)."

## Ví dụ minh họa (doanh nghiệp giả định — chỉ để tham khảo)
**Tiệm bánh Mây** muốn ảnh "5 lỗi khiến bánh bông lan bị sụp", khổ dọc, bộ màu cam vàng.
- Thông điệp: *Xem xong, người đọc biết 5 lỗi cần tránh trong lần nướng tới.*
- Tiêu đề: *5 lỗi khiến bánh bông lan **bị sụp*** · Nhãn: *Sai lầm*
- Thẻ 1: *Mở lò quá sớm* — *Nhiệt giảm đột ngột làm bánh xẹp ngay.* (… 4 thẻ còn lại)
- Chân ảnh: *Lưu lại trước khi nướng mẻ sau!* · *banhmay.vn* (tên miền giả định)
- Lệnh xuất: `python3 scripts/xuat_anh.py 5-loi-banh-sup.html` → `5-loi-banh-sup.png` 1080×1350.

## Hướng dẫn cho học viên (làm theo từng bước)
1. **Chuẩn bị trước:** nội dung muốn biến thành ảnh (bài viết, ghi chú, dàn ý); file logo PNG nền trong suốt
   (bỏ vào `03-tai-lieu-tho/dinh-kem/` của Bộ Não); máy có Chrome hoặc Edge.
2. Gõ `/ts-infographic` kèm chủ đề và khổ ảnh muốn làm.
3. Trả lời câu hỏi (chọn chữ cái cho khổ ảnh và bộ màu).
4. Đọc bản nháp chữ: tiêu đề, các thẻ. Sửa bằng lời ("thẻ 3 ngắn lại", "đổi tiêu đề có số 7") → gõ **duyệt**.
5. Chờ AI dựng và xuất ảnh. Nếu AI không chạy được lệnh trên máy bạn, làm theo hướng dẫn tự chụp AI gửi kèm.
6. Xem ảnh trên điện thoại. Muốn đổi: "đổi sang bộ màu xanh", "làm thêm bản vuông", "chữ to hơn".
7. Gõ **duyệt** để lưu vào Bộ Não. Lần sau chỉ cần nói "làm tiếp ảnh số 2 cùng bộ" để giữ đồng bộ.

## Câu lệnh mẫu
- `/ts-infographic làm ảnh 5 bước chăm sóc da sau nặn mụn cho spa Hồng, khổ dọc, bộ màu trắng cam`
- `/ts-infographic biến bài viết này thành carousel 4 ảnh vuông, bộ màu đen vàng: <dán bài viết>`
- `/ts-infographic ảnh story 6 lỗi khi quay video bán hàng bằng điện thoại, màu gradient tím`
- `/ts-infographic shop mỹ phẩm: so sánh nên/không nên khi dùng kem chống nắng, khổ 1080x1350`
- `/ts-infographic xuất lại ảnh hôm qua sang khổ vuông và story`

## Kết quả nhận được
- File HTML dùng lại được (sửa chữ là xuất lại ngay) + ảnh PNG đúng khổ, chữ tiếng Việt chuẩn.
- Loạt ảnh cùng bộ nhận diện (nếu làm carousel).
- Bản chữ đã duyệt (tiêu đề, thẻ, chân ảnh) để dùng làm caption.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-infographic-<chu-de-khong-dau>/`.
2. Lưu bản chữ đã duyệt (thông điệp, tiêu đề, các thẻ, chân ảnh, khổ, bộ màu) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-infographic
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): file `.html` nguồn, ảnh `.png` đã xuất, file logo đã dùng.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-infographic · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu người dùng chốt một bộ màu/mã màu riêng cho infographic mà `01-ho-so/04-thuong-hieu-noi-dung.md` chưa ghi, đề xuất bổ sung (bộ màu, mã màu nhấn, vị trí logo) và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bịa số liệu, nghiên cứu, trích dẫn. Số liệu phải có nguồn; ghi nguồn nhỏ ở chân ảnh nếu cần.
- Không dùng logo, hình ảnh, nhân vật của thương hiệu khác khi chưa được phép.
- Ngành sức khỏe, làm đẹp, tài chính: không khẳng định chữa khỏi, lợi nhuận đảm bảo.
- Google Fonts cần mạng; không có mạng ảnh vẫn xuất bằng font dự phòng (đủ dấu tiếng Việt, kiểu chữ hơi khác).
  Muốn đúng font khi offline: cài font Be Vietnam Pro vào máy (tải miễn phí từ Google Fonts).
- Script chỉ đọc file HTML cục bộ và ghi ảnh PNG cạnh file đó; không gửi dữ liệu đi đâu.

## Skill liên quan
- Trước: `/ts-lich-noi-dung` (chọn chủ đề) · `/ts-viet-bai-ban-hang` (viết bài đi kèm ảnh)
- Sau: `/ts-noi-dung-tu-dong-7-ngay` (lên lịch đăng) · `/ts-tao-ebook` (gom nhiều ảnh kiến thức thành ebook)

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
