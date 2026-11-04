---
name: ts-chien-luoc-marketing
description: "Gọi bằng /ts-chien-luoc-marketing. Phân tích sản phẩm rồi chấm điểm và chọn 1 trong 3 chiến lược marketing: đánh nhanh chốt gọn, dẫn dắt niềm tin, hoặc phễu quà tặng 0 đồng; thiết kế hành trình khách, lập KPI và lịch triển khai quý - tháng - tuần - ngày kèm ngưỡng dừng/tăng ngân sách. Dùng khi chưa biết nên bán theo hướng nào, sắp ra mắt sản phẩm, hoặc marketing đang làm lung tung. Từ khóa: chiến lược marketing, kế hoạch marketing, KPI marketing, nên chạy quảng cáo hay làm nội dung, kế hoạch 30 ngày, lộ trình bán hàng."
---

# /ts-chien-luoc-marketing — Chiến lược marketing

> AI chấm điểm 3 chiến lược marketing cho đúng sản phẩm của bạn, đề xuất 1 chiến lược chính + 1 dự phòng,
> rồi biến thành lịch việc cụ thể theo quý → tháng → tuần → ngày, có KPI và ngưỡng dừng/tăng ngân sách.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Có sản phẩm nhưng chưa biết nên chạy quảng cáo bán thẳng, làm nội dung xây niềm tin hay tặng quà thu khách.
- Sắp ra mắt sản phẩm/khóa học/dịch vụ mới, cần kế hoạch 30–90 ngày.
- Đang làm marketing "mỗi thứ một chút", không đo được cái gì hiệu quả.
- Cần bảng KPI để giao việc cho nhân viên hoặc đối tác.

**Không dùng khi:** đã có khách và số liệu, muốn tìm cách tăng doanh thu từ nhiều hướng → `/ts-chien-luoc-tang-truong`.
Chỉ cần lịch đăng bài → `/ts-lich-noi-dung`. Đã chọn phễu quà tặng, cần dựng ngay → `/ts-pheu-qua-tang`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `chien-luoc-marketing` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** đọc thêm kết quả của `/ts-chan-dung-khach-hang`, `/ts-phan-tich-doi-thu`,
`/ts-dinh-gia-offer`, `/ts-bao-cao-facebook-ads` trong `04-ket-qua/` nếu có — dùng làm dữ liệu chấm điểm.

## Quy trình AI thực hiện

**Nguyên tắc:** chọn **một** chiến lược chính thay vì trộn cả ba ngay từ đầu. Đánh giá theo giá bán, nhu cầu
có sẵn, thời gian ra quyết định, mức tin tưởng cần có, bằng chứng và nguồn lực. Đọc `references/ba-chien-luoc.md`
trước khi chấm điểm.

### Bước 1 — Chẩn đoán nhanh
Tóm tắt từ Bộ Não: sản phẩm chủ lực, giá, khách hàng, kênh, ngân sách, mục tiêu. Đánh dấu dữ liệu `ĐÃ CÓ` /
`CÒN THIẾU`.

### Bước 2 — Hỏi tối đa 5 câu còn thiếu (có gợi ý A–D)
Chỉ hỏi những gì ảnh hưởng tới lựa chọn: mục tiêu doanh thu/lead và thời hạn · giá & biên lợi nhuận ·
khách hàng · ngân sách quảng cáo/tháng · năng lực đội ngũ (ai làm nội dung, ai trả lời tin nhắn).

### Bước 3 — Chấm điểm 3 chiến lược
Chấm từng chiến lược theo 7 tiêu chí, thang 1–5 (bảng gợi ý trong `references/ba-chien-luoc.md`). Đánh dấu
tiêu chí **quyết định** (trọng số ×2). Giải thích ngắn mỗi điểm và ghi giả định. Không chọn chỉ theo điểm tổng.

### Bước 4 — Đề xuất (cổng duyệt 1)
- **1 chiến lược chính** + lý do (2–3 câu).
- **1 phương án dự phòng** + khi nào chuyển sang.
- **Vì sao không chọn** phương án còn lại.
👉 Chờ người dùng "duyệt" hoặc chọn khác.

### Bước 5 — Thiết kế hành trình khách hàng
Theo chiến lược đã chọn: thông điệp chính, offer, kênh, loại nội dung, quảng cáo, trang đích, kịch bản bán
hàng, chăm sóc sau bán. Ghi rõ mỗi điểm chạm dùng lệnh `/ts-...` nào để làm.

### Bước 6 — Lập lịch triển khai quý → tháng → tuần → ngày
Mỗi việc có: người làm, đầu ra, công cụ/lệnh, ngân sách, KPI, hạn. Đưa chi tiết **7 / 14 / 30 ngày đầu**.

### Bước 7 — KPI và ngưỡng ra quyết định
- Bảng KPI đầu phễu – giữa phễu – cuối phễu (mẫu trong `references/ba-chien-luoc.md`).
- Điều kiện **dừng** và điều kiện **tăng ngân sách** cụ thể bằng con số.
- Danh sách quyết định cần người dùng duyệt.

### Bước 8 — Duyệt kế hoạch (cổng duyệt 2) rồi mới phối hợp lệnh khác
Sau khi duyệt, gợi ý đúng lệnh theo đầu việc (vd `/ts-pheu-qua-tang`, `/ts-lich-noi-dung`, `/ts-viet-quang-cao`,
`/ts-thiet-ke-anh-quang-cao`, `/ts-trang-ban-hang`, `/ts-len-camp-facebook`, `/ts-xu-ly-tu-choi`,
`/ts-bao-cao-facebook-ads`) hoặc chuyển cho `/ts-dieu-phoi-cong-viec` để chạy trọn gói.
Chỉ làm hành động bên ngoài (đăng, chạy quảng cáo) sau xác nhận riêng.

### Checklist chất lượng
- [ ] Có bảng chấm 3 chiến lược × 7 tiêu chí, ghi rõ giả định và tiêu chí quyết định.
- [ ] Chỉ 1 chiến lược chính; có dự phòng và lý do loại phương án còn lại.
- [ ] Lịch có đủ 4 cấp; 7 ngày đầu chi tiết tới từng ngày.
- [ ] Mỗi KPI có con số mục tiêu và ngưỡng cảnh báo; có điều kiện dừng/tăng ngân sách.
- [ ] Ngân sách trong kế hoạch không vượt ngân sách trong hồ sơ (hoặc đã hỏi lại).
- [ ] Không hứa kết quả chắc chắn; dự báo ghi là "ước tính".

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** đã có hồ sơ doanh nghiệp (`/ts-tao-ho-so-doanh-nghiep`). Biết sơ bộ: mục tiêu tháng
(doanh thu hoặc số khách), ngân sách quảng cáo có thể chi, ai sẽ trả lời tin nhắn khách.

1. Gõ `/ts-chien-luoc-marketing` kèm sản phẩm muốn đẩy (vd "gói chăm sóc da 6 buổi").
2. Trả lời tối đa 5 câu hỏi (chọn A–D).
3. Xem bảng chấm điểm 3 chiến lược — hỏi lại AI nếu chỗ nào chưa hiểu.
4. Gõ "duyệt" chiến lược AI đề xuất, hoặc nói "tôi muốn thử phễu quà tặng".
5. Xem lịch 30 ngày và bảng KPI; sửa bằng lời ("ngân sách chỉ 5 triệu", "tôi không quay video được").
6. Gõ "duyệt" để AI lưu kế hoạch vào Bộ Não.
7. Bắt tay làm: gõ lệnh AI gợi ý cho việc đầu tiên, hoặc `/ts-dieu-phoi-cong-viec làm theo kế hoạch marketing vừa duyệt`.

## Câu lệnh mẫu
- `/ts-chien-luoc-marketing shop giày nữ online, giá 350–550k, mục tiêu 300 đơn/tháng, ngân sách 15 triệu`
- `/ts-chien-luoc-marketing khóa học quay video bằng điện thoại 1,5 triệu, sắp mở lớp sau 30 ngày`
- `/ts-chien-luoc-marketing nha khoa ở Biên Hòa muốn đẩy dịch vụ niềng răng 35 triệu`
- `/ts-chien-luoc-marketing dịch vụ kế toán thuế cho hộ kinh doanh, chưa chạy quảng cáo bao giờ`

## Kết quả nhận được
- Bảng chẩn đoán và chấm điểm 3 chiến lược (có giả định).
- Chiến lược chính + dự phòng + lý do.
- Bản đồ hành trình khách hàng và offer, mỗi điểm chạm gắn lệnh `/ts-...`.
- Lịch triển khai quý → tháng → tuần → ngày; chi tiết 7/14/30 ngày đầu.
- Bảng KPI 3 tầng phễu, điều kiện dừng/tăng ngân sách, danh sách quyết định cần duyệt.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-chien-luoc-marketing-<chu-de-khong-dau>/`.
2. Lưu toàn bộ bản chiến lược đã duyệt (chẩn đoán, chấm điểm, hành trình, lịch, KPI) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-chien-luoc-marketing
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [chien-luoc, marketing, kpi, <tên chiến lược>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `lich-trien-khai.csv` (bảng lịch), `kpi.csv` (bảng KPI) để mở bằng Excel.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Chiến lược marketing <tên>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-chien-luoc-marketing · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu KPI/mục tiêu/ngân sách đã chốt khác với `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`, đề xuất cập nhật
   tệp đó và hỏi trước khi ghi đè. Kế hoạch nhiều tuần → đề xuất tạo trang theo dõi `05-du-an/<ten-chien-dich>.md`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không lập chiến dịch cho hàng hóa/dịch vụ hạn chế độ tuổi, cờ bạc hoặc hoạt động nguy hiểm nhắm người chưa thành niên.
- Không bịa dữ liệu, không cam kết kết quả, không dùng thủ thuật gây hiểu nhầm (khan hiếm giả, giảm giá giả).
- Mọi việc tốn tiền hoặc công khai chỉ làm sau khi người dùng duyệt riêng.

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` · `/ts-chan-dung-khach-hang` · `/ts-phan-tich-doi-thu` · `/ts-dinh-gia-offer`
- Sau: `/ts-pheu-qua-tang` · `/ts-lich-noi-dung` · `/ts-viet-quang-cao` · `/ts-len-camp-facebook` · `/ts-dieu-phoi-cong-viec`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
