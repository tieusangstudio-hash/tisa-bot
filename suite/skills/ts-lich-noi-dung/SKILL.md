---
name: ts-lich-noi-dung
description: "Gọi bằng /ts-lich-noi-dung. Lập lịch nội dung tuần hoặc tháng cho Fanpage, TikTok, Zalo của doanh nghiệp bạn: chia chủ đề theo tuần, phân bổ loại bài (bài viết, video ngắn, kéo tin nhắn, câu chuyện khách hàng, ưu đãi, quà miễn phí) kèm CTA và danh sách việc cần chuẩn bị. Dùng khi cần kế hoạch đăng bài đều đặn, chưa biết tuần này đăng gì, sắp mở bán hoặc ra mắt. Từ khóa: lịch content, kế hoạch đăng bài, content tháng, content tuần, lịch bài, lên lịch fanpage, chủ đề tuần."
---

# /ts-lich-noi-dung — Lập lịch nội dung tuần / tháng

> Biến hồ sơ doanh nghiệp của bạn thành một lịch đăng bài rõ ràng: mỗi ngày đăng loại bài gì, nói chủ đề
> gì, nhằm mục tiêu gì, kêu gọi khách làm gì — kèm danh sách ảnh/video cần chuẩn bị trước.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Muốn có lịch đăng bài cả tuần hoặc cả tháng cho Fanpage / TikTok / Zalo OA / Instagram.
- Không biết tuần này nên đăng gì, đăng lung tung không theo mục tiêu.
- Sắp mở bán, ra mắt sản phẩm, khai trương, mở lớp, chạy ưu đãi — cần lịch "hâm nóng" trước.
- Muốn chia việc cho nhân viên/cộng tác viên: ai quay gì, thiết kế gì, ngày nào.
- Muốn rút ra bộ "câu nỗi đau cốt lõi" và "chủ đề xoay vòng" để dùng lại nhiều tháng.

**Không dùng khi:** muốn AI viết luôn caption + thiết kế ảnh + đăng bài 7 ngày → dùng `/ts-noi-dung-tu-dong-7-ngay`;
chỉ cần viết 1 bài bán hàng → `/ts-viet-bai-ban-hang`; chỉ cần kịch bản video → `/ts-kich-ban-reels`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `lich-noi-dung` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này: nếu có `02-kien-thuc/cong-thuc/chu-de-noi-dung.md` (bộ nỗi đau + chủ đề xoay vòng đã lưu
lần trước) thì đọc và dùng lại, không rút lại từ đầu.

## Quy trình AI thực hiện

### Bước 1 — Thu thập thông tin (hỏi gộp 1 lần, chỉ hỏi phần Bộ Não chưa có)
1. Lập lịch cho **tuần** nào hay **tháng** nào?
2. Kênh đăng: A. Fanpage · B. TikTok · C. Zalo OA · D. Instagram · E. Nhiều kênh (ghi rõ).
3. Sản phẩm/dịch vụ ưu tiên đẩy trong kỳ này là gì?
4. Có sự kiện đặc biệt không: mở bán, ra mắt, khai trương, mở lớp, sale, lễ tết, hết hàng…? Ngày cụ thể?
5. Sức làm nội dung: A. Nhẹ (3–4 bài/tuần) · B. Chuẩn (7 bài/tuần) · C. Mạnh (7 bài + 7 video/tuần).

### Bước 2 — Rút "nguyên liệu" từ hồ sơ (làm 1 lần, lưu dùng lại)
Đọc kỹ phương pháp ở `references/phuong-phap-rut-chu-de.md`, rồi:
- **6–9 câu nỗi đau cốt lõi**: từ nỗi đau, nỗi sợ, mong muốn trong `03-khach-hang-muc-tieu.md`, viết thành
  câu ngắn khách đọc là "đúng mình rồi". Chia theo 2–3 mảng sản phẩm/dịch vụ chính.
- **Chủ đề xoay vòng 4 tuần**: điền khung 4 tuần ở Bước 3 bằng chủ đề cụ thể của ngành người dùng.
- Cho người dùng xem nhanh, sửa bằng lời trước khi đi tiếp.

### Bước 3 — Ghép vào khung chuẩn
**Gói nội dung mỗi tuần (mức Chuẩn — giảm/tăng theo lựa chọn ở Bước 1):**
- 7 bài đăng chính trên kênh chủ lực
- 3–7 kịch bản video ngắn (Reels/TikTok)
- 3 bài kéo tin nhắn / đăng ký tư vấn
- 1–2 bài thông báo (ưu đãi, lịch mở bán, sự kiện, hàng mới) — chỉ khi có thật
- 2 bài câu chuyện khách hàng / hậu trường
- 1 tin nhắn hoặc email chăm sóc khách cũ
- 1 nội dung tặng quà miễn phí để thu thông tin khách (checklist, bảng giá mẫu, ebook, voucher…)

**Khung tuần mặc định (đổi ngày được):**

| Ngày | Loại nội dung | Mục tiêu | Nhóm chủ đề |
|---|---|---|---|
| Thứ 2 | Bài nỗi đau / sự thật ngược | Tăng nhận biết | Mảng sản phẩm chính |
| Thứ 3 | Video ngắn mẹo thực tế | Tăng lượt tiếp cận | Mẹo dùng / mẹo chọn |
| Thứ 4 | Bài kéo tin nhắn / CTA | Thu khách tiềm năng | Tư vấn miễn phí |
| Thứ 5 | Câu chuyện khách hàng | Tăng niềm tin | Kết quả trước – sau |
| Thứ 6 | Thông báo ưu đãi / lịch / hàng mới | Chốt đơn | Sản phẩm ưu tiên |
| Thứ 7 | Hậu trường / hình ảnh thật | Xây thương hiệu | Con người, quy trình |
| Chủ nhật | Quà miễn phí / giá trị | Thu thông tin khách | Checklist, mẫu, voucher |

**Chủ đề xoay vòng theo tháng:**
- **Tuần 1 — Nhận biết & giá trị:** mẹo hữu ích, lỗi thường gặp của khách, so sánh trước/sau, tặng quà.
- **Tuần 2 — Xây niềm tin:** câu chuyện khách thật, hậu trường, video khách nói, trả lời băn khoăn phổ biến.
- **Tuần 3 — Tạo nhu cầu & kéo khách:** đánh vào nỗi đau, so sánh "tự làm / thuê ngoài / dùng giải pháp
  bài bản", câu chuyện thành công, CTA mạnh "tư vấn miễn phí".
- **Tuần 4 — Mở bán & chốt:** thông báo ưu đãi/lịch, đếm ngược, bài chốt (ưu đãi, số lượng có hạn — chỉ khi có thật).

Không có đợt mở bán trong tháng → Tuần 4 đổi thành "Giữ chân khách cũ": hướng dẫn dùng, khách quay lại, giới thiệu bạn bè.

### Bước 4 — Xuất lịch
Bảng markdown cho mỗi tuần, đủ cột:

| Ngày | Kênh | Loại nội dung | Chủ đề cụ thể | Người đại diện nói gì (ý chính) | Mục tiêu | CTA |
|---|---|---|---|---|---|---|

- "Người đại diện" lấy từ `04-thuong-hieu-noi-dung.md` (chủ shop, chuyên gia, nhân vật…), đúng cách xưng hô.
- CTA lấy từ bộ CTA trong hồ sơ; chưa có thì dùng mẫu ở `references/mau-giong-thuong-hieu.md`.
- Lịch tháng: phần **Tổng quan tháng** (mục tiêu, sản phẩm ưu tiên, 4 chủ đề tuần) + 4 bảng tuần.

### Bước 5 — Ghi chú chiến lược + việc cần chuẩn bị
- **Ghi chú chiến lược (3–5 dòng):** lý do chọn chủ đề từng ngày; bài nào nên chạy quảng cáo đẩy bài
  (boost); bài nào phải chuẩn bị ảnh/video trước. Chỉ gợi ý ngân sách đẩy bài khi được hỏi, dựa trên
  ngân sách trong `05-muc-tieu-quy-tac-lien-he.md`.
- **Checklist việc cần chuẩn bị:** video cần quay, ảnh cần thiết kế, tài liệu quà tặng cần làm, người phụ trách.

### Bước 6 — Cổng duyệt
Hỏi: "Lịch này ổn chưa? Bạn muốn đổi ngày nào, chủ đề nào?" → sửa đến khi người dùng gõ **"duyệt"**.
Sau đó gợi ý lệnh tiếp theo (xem *Skill liên quan*) và lưu vào Bộ Não.

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Mỗi ngày có đúng 1 mục tiêu và 1 CTA.
- [ ] Chủ đề cụ thể theo ngành người dùng, không chung chung kiểu "chia sẻ giá trị".
- [ ] Có ít nhất 1 bài thu thông tin khách và 1 bài xây niềm tin mỗi tuần.
- [ ] Không có ưu đãi, số lượng, ngày mở bán, câu chuyện khách hàng bịa — thiếu thì ghi `[CẦN BỔ SUNG: …]`.
- [ ] Số bài khớp với sức làm người dùng đã chọn.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (5 phút):** biết tuần/tháng muốn lên lịch, sản phẩm muốn đẩy, ngày sự kiện (nếu có),
và mỗi tuần bạn làm được bao nhiêu bài.
1. Gõ `/ts-lich-noi-dung` kèm 1 câu, ví dụ "lịch tháng 12 cho Fanpage, đẩy combo quà Tết".
2. Trả lời các câu AI hỏi — có gợi ý A-B-C-D thì chỉ cần gõ chữ cái.
3. Xem bộ "câu nỗi đau" và "chủ đề 4 tuần" AI rút ra; sửa bằng lời ("bỏ câu số 3", "thêm chủ đề giao hàng nhanh").
4. Xem bảng lịch; sửa bằng lời ("thứ 7 đổi sang livestream", "bớt bài bán, thêm bài mẹo").
5. Gõ **"duyệt"** để AI chốt lịch và lưu vào Bộ Não.
6. Làm tiếp từng bài: `/ts-viet-bai-ban-hang`, `/ts-kich-ban-reels`, hoặc `/ts-noi-dung-tu-dong-7-ngay`.

## Câu lệnh mẫu
- `/ts-lich-noi-dung lên lịch tháng 12 cho Fanpage shop mỹ phẩm, đẩy combo quà Tết, mỗi tuần 7 bài`
- `/ts-lich-noi-dung lịch tuần sau cho spa, có chương trình khai trương chi nhánh mới ngày 15`
- `/ts-lich-noi-dung lịch 4 tuần cho khóa học tiếng Anh online, tuần cuối mở lớp mới, kênh TikTok + Fanpage`
- `/ts-lich-noi-dung tôi bán đồ gỗ nội thất, mỗi tuần chỉ làm được 3 bài, lên lịch nhẹ giúp tôi`

## Kết quả nhận được
- Bộ 6–9 câu nỗi đau cốt lõi + chủ đề xoay vòng 4 tuần cho đúng ngành của bạn.
- Bảng lịch tuần (hoặc tổng quan tháng + 4 bảng tuần) đủ kênh, chủ đề, ý chính, mục tiêu, CTA.
- Ghi chú chiến lược ngắn + checklist ảnh/video/tài liệu cần chuẩn bị.
- (Tùy chọn) tệp `lich-noi-dung.csv` để dán vào Google Sheets / Excel.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-lich-noi-dung-<chu-de-khong-dau>/`.
2. Lưu lịch nội dung đã duyệt (tổng quan + bảng tuần + ghi chú chiến lược + checklist chuẩn bị) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-lich-noi-dung
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `lich-noi-dung.csv` (bảng lịch dạng cột: ngay, kenh, loai, chu-de, y-chinh, muc-tieu, cta).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-lich-noi-dung · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Bộ câu nỗi đau cốt lõi + chủ đề xoay vòng là tri thức dùng lại nhiều tháng: đề xuất lưu (hoặc cập nhật) `02-kien-thuc/cong-thuc/chu-de-noi-dung.md`. Nếu giọng văn, CTA, hashtag vừa chốt khác `01-ho-so/04-thuong-hieu-noi-dung.md`, đề xuất cập nhật và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Lịch là kế hoạch — skill này **không tự đăng bài**. Muốn đăng thì dùng `/ts-noi-dung-tu-dong-7-ngay`.
- Không bịa ưu đãi, số suất còn lại, ngày mở bán, lời khen của khách. Thiếu thì ghi `[CẦN BỔ SUNG: …]`.
- Tránh lời hứa tuyệt đối ("khỏi 100%", "chắc chắn giàu") — dễ vi phạm chính sách quảng cáo và mất uy tín.
- Ngành nhạy cảm (y tế, thẩm mỹ, tài chính, thực phẩm chức năng): nhắc người dùng kiểm tra quy định quảng cáo của ngành.

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` · `/ts-chan-dung-khach-hang` · `/ts-phan-tich-doi-thu`
- Sau: `/ts-noi-dung-tu-dong-7-ngay` · `/ts-viet-bai-ban-hang` · `/ts-kich-ban-reels` · `/ts-thiet-ke-anh-quang-cao` · `/ts-pheu-qua-tang`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
