---
name: ts-tao-ho-so-doanh-nghiep
description: "Gọi bằng /ts-tao-ho-so-doanh-nghiep. Phỏng vấn từng câu dễ hiểu (gợi ý A-B-C-D) rồi tạo 5 tệp hồ sơ nền trong Bộ Não Thứ 2: doanh nghiệp, sản phẩm, khách hàng, thương hiệu (giọng văn, màu, logo, nhân vật đại diện), mục tiêu - KPI - ngân sách - liên hệ. Mọi lệnh /ts- khác đọc hồ sơ này. Dùng khi mới cài bộ skill, chưa có hồ sơ hoặc thông tin doanh nghiệp thay đổi. Từ khóa: hồ sơ doanh nghiệp, tạo data, AI hiểu doanh nghiệp, giọng thương hiệu, khách hàng mục tiêu, bảng giá, màu thương hiệu, cập nhật hồ sơ."
---

# /ts-tao-ho-so-doanh-nghiep — Tạo hồ sơ doanh nghiệp (skill nền)

> AI hỏi bạn từng câu ngắn, có gợi ý sẵn để chọn, rồi viết thành 5 tệp hồ sơ trong Bộ Não Thứ 2.
> Từ đó mọi lệnh `/ts-...` khác tự hiểu bạn bán gì, cho ai, giọng ra sao — không phải kể lại.

**Loại Bộ Não:** ĐỌC + LƯU (ghi thẳng vào `01-ho-so/`)

## Khi nào dùng
- Vừa chạy xong `/ts-cai-dat-bo-nao`, 5 tệp hồ sơ còn trống.
- AI làm nội dung "chung chung", không đúng sản phẩm, không đúng giọng của bạn.
- Đổi giá, thêm sản phẩm mới, đổi màu thương hiệu, đổi nhân vật đại diện, đổi mục tiêu tháng.
- Có sẵn tài liệu (bảng giá, giới thiệu công ty, link Fanpage) và muốn AI chuẩn hóa thành hồ sơ.
- Muốn kiểm tra hồ sơ hiện tại còn thiếu gì.

**Không dùng khi:** chưa có thư mục Bộ Não → chạy `/ts-cai-dat-bo-nao` trước (hoặc vẫn phỏng vấn, AI giao 5 tệp để tải về).
Muốn phân tích sâu chân dung khách → `/ts-chan-dung-khach-hang`. Muốn định giá lại → `/ts-dinh-gia-offer`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: cả 5 tệp `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md` (để biết trường nào đã có, trường nào còn `[CẦN BỔ SUNG]`);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `tao-ho-so-doanh-nghiep` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:**
- Đọc thêm tài liệu thô trong `03-tai-lieu-tho/` (bảng giá, giới thiệu, ảnh logo trong `dinh-kem/`) và
  các tệp người dùng đính kèm trong cuộc trò chuyện. Nếu có link website/Fanpage công khai và môi trường
  có công cụ đọc web, đọc để điền sẵn — vẫn phải hỏi lại để xác nhận.
- Không có Bộ Não: hỏi người dùng muốn **(A)** dừng để chạy `/ts-cai-dat-bo-nao` trước (khuyên dùng) hay
  **(B)** phỏng vấn luôn rồi nhận 5 tệp để tải về, sau này bỏ vào `01-ho-so/`.

## Quy trình AI thực hiện

### Bước 1 — Kiểm kê dữ liệu có sẵn
Lập bảng trạng thái cho 5 tệp, mỗi trường gắn 1 nhãn:
`ĐÃ CÓ` (đọc được, rõ ràng) · `CẦN XÁC NHẬN` (suy ra, cũ, hoặc tài liệu mâu thuẫn) · `CÒN THIẾU`.

```text
HỒ SƠ HIỆN CÓ
01 Doanh nghiệp ......... 6/8 trường  (thiếu: năm bắt đầu, bằng chứng)
02 Sản phẩm ............. 3 sản phẩm, 1 sản phẩm chưa có giá
03 Khách hàng ........... CÒN THIẾU
04 Thương hiệu .......... có màu, chưa có font, chưa có nhân vật đại diện
05 Mục tiêu & liên hệ ... có SĐT, chưa có ngân sách, chưa có ID tài khoản quảng cáo
```
Không hỏi lại trường `ĐÃ CÓ`. Tài liệu mâu thuẫn (vd 2 bảng giá khác nhau) → trích cả hai, hỏi bản nào đang dùng.

### Bước 2 — Chọn chế độ (hỏi 1 câu)
- **A. Nhanh (≈10 phút, 10 câu)** — đủ để các lệnh khác chạy được.
- **B. Đầy đủ (20–30 phút, 24 câu)** — khuyên dùng lần đầu.
- **C. Chỉ cập nhật 1 phần** — vd đổi giá, đổi màu, thêm sản phẩm, đổi mục tiêu tháng.
- **D. Kiểm tra hồ sơ** — chỉ báo còn thiếu gì, chưa hỏi.

### Bước 3 — Phỏng vấn từng phần
Đọc `references/bo-cau-hoi.md` (24 câu, chia 5 phần tương ứng 5 tệp). Quy tắc:
- Tối đa **3 câu mỗi lượt**, đi theo thứ tự phần 1 → 5; báo tiến độ ("Phần 2/5 — Sản phẩm").
- Mỗi câu: 1 câu hỏi ngắn + 4 gợi ý A–D cụ thể theo ngành của người dùng + `E. Mô tả theo tình hình thực tế`.
- Người dùng chọn chữ cái → hỏi thêm **tối đa 1 chi tiết** thật sự cần (con số, tên gọi).
- Câu 16 (màu) có 6 bộ màu chuẩn: đen vàng, gradient tím, xanh, cam vàng, đỏ cam, trắng cam — hoặc màu riêng.
- Câu 18 (nhân vật đại diện): nếu có người xuất hiện trong video/ảnh, hỏi đủ ngoại hình + trang phục
  mặc định + giọng nói, viết thêm 1 đoạn mô tả tiếng Anh để dùng cho công cụ video AI.
- Câu 24 (tài khoản quảng cáo): **chỉ xin ID**, kèm cách tìm ID nếu người dùng không biết.

Mẫu một lượt hỏi:
```text
Phần 3/5 — Khách hàng (câu 9–10)

9. Khách hàng thường là ai?
   A. Người tiêu dùng cá nhân (ghi độ tuổi, nghề)   B. Chủ shop, người kinh doanh nhỏ
   C. Doanh nghiệp cần dịch vụ chuyên môn          D. Một nhóm nghề cụ thể (spa, giáo viên…)
   E. Mô tả theo tình hình thực tế của anh/chị
10. Khách đang gặp vấn đề gì trước khi tìm đến anh/chị?
   A. Thiếu thời gian   B. Không biết cách làm   C. Đã thử, tốn tiền mà chưa hiệu quả
   D. Muốn đẹp/nhanh/chuyên nghiệp hơn   E. Mô tả theo tình hình thực tế

👉 Trả lời kiểu "9A – mẹ bỉm 28–35 tuổi, 10C" là được.
```

### Bước 4 — Kiểm tra tính nhất quán
Đối chiếu trước khi viết tệp:
- Sản phẩm và mức giá có hợp với túi tiền nhóm khách không.
- Nỗi đau (tệp 03) có nối được với lợi ích sản phẩm (tệp 02) không.
- USP có bằng chứng đi kèm không; bằng chứng có được phép công khai không.
- Giọng văn và xưng hô có hợp nền tảng, hợp nhóm khách không.
- Màu, font, logo có đủ để thiết kế ảnh; nhân vật có đủ chi tiết để vẽ lại nhất quán.
- Mục tiêu có con số, có hạn; ngân sách có khớp mục tiêu (vd mục tiêu 300 lead nhưng ngân sách 0 → hỏi lại).
- Thông tin liên hệ nào được đưa vào nội dung công khai.

Không tự tạo thành tích, chứng nhận, feedback, địa chỉ, cam kết. Thiếu → ghi `[CẦN BỔ SUNG]`.

### Bước 5 — Soạn 5 tệp
Đọc `references/cau-truc-5-tep.md` và soạn đúng 5 tệp, đúng tên, mỗi tệp có frontmatter:
```yaml
---
loai: ho-so
tep: <tên tệp không đuôi>
cap-nhat: <YYYY-MM-DD>
trang-thai: nhap
---
```
Mẫu trống do `/ts-cai-dat-bo-nao` tạo có `trang-thai: chua-dien`: giữ nguyên mọi mục của mẫu đó,
điền vào và bổ sung thêm mục theo `references/cau-truc-5-tep.md` (không xóa mục nào).
Bắt buộc có:
- **Tệp 04** — mục *Giọng văn*, *Xưng hô*, *Màu thương hiệu* (mã màu), *Font chữ*, *Logo* (vị trí tệp),
  *Nhân vật đại diện* (ngoại hình, trang phục, giọng nói, mô tả tiếng Anh cho AI).
- **Tệp 05** — mục *Mục tiêu doanh thu/lead*, *KPI*, *Ngân sách quảng cáo*, *Kênh ưu tiên*,
  *Thông tin liên hệ*, *Tài khoản quảng cáo & Trang* (ID tài khoản quảng cáo Meta, Page ID, TikTok
  Advertiser ID — không mật khẩu, không token).

Viết tiếng Việt có dấu, tiêu đề dễ hiểu, dùng bảng khi cần so sánh. Phân biệt rõ `[GIẢ ĐỊNH]`,
`[CẦN BỔ SUNG]`, `[NỘI BỘ]` (không được công khai).

### Bước 6 — Xác nhận trước khi ghi (cổng duyệt)
Trình **tóm tắt 10 dòng quan trọng nhất** và hỏi lại các trường dễ sai: tên thương hiệu, giá, khu vực,
số điện thoại/Zalo, ưu đãi, cam kết, ID tài khoản quảng cáo. Người dùng sửa bằng lời → cập nhật → hỏi lại.
Chỉ khi người dùng nói "duyệt" mới chuyển `trang-thai: da-xac-nhan` và ghi tệp.

**Chế độ cập nhật (C):** nếu tệp đã có nội dung, trình bảng "trước → sau" cho từng trường thay đổi,
chép bản cũ vào `99-luu-tru/<YYYY-MM-DD>-<tên tệp>` rồi mới ghi đè. Không xóa nội dung người dùng tự viết.

### Bước 7 — Ghi tệp và bàn giao
Thực hiện **Bước cuối** bên dưới. Báo rõ: tệp nào đã ghi, còn bao nhiêu `[CẦN BỔ SUNG]`, gợi ý lệnh tiếp theo.

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Đủ 5 tệp, đúng tên, đúng thư mục `01-ho-so/`, frontmatter YAML hợp lệ (`loai: ho-so`, `cap-nhat:`).
- [ ] Mỗi sản phẩm có giá hoặc ghi `[CẦN BỔ SUNG]`; có CTA chuẩn.
- [ ] Tệp 04 có đủ 6 mục: giọng văn, xưng hô, màu, font, logo, nhân vật đại diện.
- [ ] Tệp 05 có đủ: mục tiêu, KPI, ngân sách, kênh, liên hệ, ID tài khoản (không mật khẩu).
- [ ] Không có số liệu, feedback, chứng nhận do AI tự nghĩ ra.
- [ ] Giá, số điện thoại, địa chỉ khớp nhau giữa các tệp.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (có gì đưa nấy, thiếu cũng không sao):** bảng giá, logo (file PNG), 1–2 ảnh người
đại diện, link Fanpage/website, số Zalo, ID tài khoản quảng cáo (không cần mật khẩu). Nếu đã có Bộ Não,
thả các tệp này vào thư mục `03-tai-lieu-tho/` (ảnh vào `03-tai-lieu-tho/dinh-kem/`).

1. Gõ `/ts-tao-ho-so-doanh-nghiep` kèm 1 câu giới thiệu (vd "tôi bán bánh kem ở Đà Nẵng").
2. Chọn chế độ: **A** nhanh 10 phút, **B** đầy đủ 20–30 phút, **C** chỉ cập nhật 1 phần.
3. Trả lời từng nhóm câu hỏi — gõ chữ cái là đủ (vd "9A, 10C"), muốn nói thêm thì cứ gõ tự nhiên.
4. Câu nào chưa biết, gõ "bỏ qua" — AI ghi `[CẦN BỔ SUNG]`, lần sau điền tiếp.
5. Đọc bản tóm tắt 10 dòng, sửa bằng lời ("giá gói VIP là 2,5 triệu", "xưng em – chị").
6. Gõ "duyệt" để AI ghi 5 tệp vào `01-ho-so/`.
7. Mở Obsidian xem lại 5 tệp; muốn sửa tay cũng được — các lệnh khác luôn đọc bản mới nhất.
8. Mỗi khi đổi giá, thêm sản phẩm, đổi mục tiêu tháng: chạy lại lệnh này, chọn **C**.

## Câu lệnh mẫu
- `/ts-tao-ho-so-doanh-nghiep tôi bán quần áo trẻ em online toàn quốc, làm bản nhanh`
- `/ts-tao-ho-so-doanh-nghiep spa Hồng ở Cần Thơ, tôi đã bỏ bảng giá vào 03-tai-lieu-tho, đọc rồi hỏi phần còn thiếu`
- `/ts-tao-ho-so-doanh-nghiep tôi dạy khóa học quay video bằng điện thoại, làm bản đầy đủ`
- `/ts-tao-ho-so-doanh-nghiep cập nhật: thêm gói combo 1,2 triệu và đổi màu sang cam vàng`
- `/ts-tao-ho-so-doanh-nghiep kiểm tra hồ sơ của tôi còn thiếu gì`

## Kết quả nhận được
- 5 tệp hồ sơ trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`,
  `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`.
- Mục **Hồ sơ doanh nghiệp** trong `muc-luc.md` được cập nhật, có ngày.
- Danh sách trường còn `[CẦN BỔ SUNG]` và lệnh nên chạy tiếp.
- Không có Bộ Não: 5 tệp `.md` để tải về.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-tao-ho-so-doanh-nghiep-<ten-thuong-hieu-khong-dau>/`.
2. Lưu biên bản phỏng vấn (câu hỏi – câu trả lời tóm tắt, bảng trạng thái trước/sau, danh sách trường còn thiếu) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-tao-ho-so-doanh-nghiep
   ngay: <YYYY-MM-DD>
   chu-de: <Hồ sơ doanh nghiệp — tên thương hiệu>
   the: [ho-so, doanh-nghiep, thuong-hieu]
   ---
   ```
   Kèm theo các file phụ (nếu có): không có.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Phỏng vấn hồ sơ]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-tao-ho-so-doanh-nghiep · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Tri thức dùng lại lâu dài — đây là việc chính của skill:
   - Ghi 5 tệp vào `01-ho-so/` đúng tên ở trên (bản cũ có nội dung thì chép sang `99-luu-tru/` trước).
   - Cập nhật mục **Hồ sơ doanh nghiệp** trong `muc-luc.md` (chưa có mục thì tạo `## Hồ sơ doanh nghiệp`
     ngay sau mục *Quy tắc*), thay các dòng cũ của mục này bằng:
     ```markdown
     ## Hồ sơ doanh nghiệp
     - [[01-ho-so/01-ho-so-doanh-nghiep|Hồ sơ doanh nghiệp]] — cập nhật <YYYY-MM-DD>
     - [[01-ho-so/02-san-pham-dich-vu|Sản phẩm & dịch vụ]] — cập nhật <YYYY-MM-DD>
     - [[01-ho-so/03-khach-hang-muc-tieu|Khách hàng mục tiêu]] — cập nhật <YYYY-MM-DD>
     - [[01-ho-so/04-thuong-hieu-noi-dung|Thương hiệu & nội dung]] — cập nhật <YYYY-MM-DD>
     - [[01-ho-so/05-muc-tieu-quy-tac-lien-he|Mục tiêu, quy tắc & liên hệ]] — cập nhật <YYYY-MM-DD>
     ```
   - Logo/ảnh nhân vật người dùng gửi: lưu vào `03-tai-lieu-tho/dinh-kem/` và ghi đường dẫn vào tệp 04.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bao giờ xin hoặc lưu mật khẩu, mã OTP, token, cookie, số thẻ, số tài khoản ngân hàng đầy đủ.
  ID tài khoản quảng cáo và Page ID là thông tin định danh, được phép lưu.
- Không lưu dữ liệu nhạy cảm của khách hàng (tên, SĐT từng khách) trong hồ sơ.
- Không bịa thành tích, số khách, feedback, chứng nhận, cam kết. Thiếu là ghi `[CẦN BỔ SUNG]`.
- Không ghi đè tệp hồ sơ đã có khi chưa được duyệt; luôn lưu bản cũ vào `99-luu-tru/`.
- Ngành có quy định riêng (mỹ phẩm, thực phẩm chức năng, y tế, tài chính): ghi rõ ở tệp 04 để các lệnh
  viết nội dung tránh vi phạm.

## Skill liên quan
- Trước: `/ts-cai-dat-bo-nao`
- Sau: `/ts-dieu-phoi-cong-viec` (chưa biết làm gì tiếp) · `/ts-chan-dung-khach-hang` · `/ts-chien-luoc-marketing` · `/ts-thiet-ke-anh-quang-cao`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
