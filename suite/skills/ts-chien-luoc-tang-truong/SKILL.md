---
name: ts-chien-luoc-tang-truong
description: "Gọi bằng /ts-chien-luoc-tang-truong. Đọc số liệu kinh doanh, xác định chỉ số nền (doanh thu, giá trị đơn, chi phí có khách, mua lại, LTV), phân tích 6 đòn bẩy tăng trưởng, chấm điểm 8–15 sáng kiến theo ICE, chọn tối đa 3 ưu tiên và lập kế hoạch 30/60/90 ngày kèm thẻ thử nghiệm, KPI và nhịp họp. Dùng khi doanh thu chững lại, muốn tăng trưởng mà không chỉ đổ thêm tiền quảng cáo. Từ khóa: tăng doanh thu, chiến lược tăng trưởng, upsell, giữ chân khách, khách mua lại, giới thiệu khách, kế hoạch 90 ngày, doanh thu chững."
---

# /ts-chien-luoc-tang-truong — Chiến lược tăng trưởng

> AI đọc số liệu hiện tại, soi 6 "đòn bẩy" làm tăng doanh thu (phễu sản phẩm, bán thêm, giữ chân, giới thiệu,
> bán theo vấn đề, trung thành), chọn 3 việc đáng làm nhất và lập kế hoạch 30/60/90 ngày có thể đo được.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Doanh thu đứng yên hoặc giảm vài tháng liền.
- Chi phí quảng cáo ngày càng đắt, muốn tăng doanh thu từ khách cũ.
- Có nhiều ý tưởng tăng trưởng nhưng không biết làm cái nào trước.
- Cần kế hoạch 90 ngày có thử nghiệm, KPI, người phụ trách cho đội ngũ.

**Không dùng khi:** chưa có khách/chưa bán, cần chọn hướng marketing ban đầu → `/ts-chien-luoc-marketing`.
Chỉ cần đọc và giải thích số liệu doanh thu → `/ts-phan-tich-doanh-thu`. Cần thiết kế lại dòng sản phẩm → `/ts-thiet-ke-pheu`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `chien-luoc-tang-truong` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** tìm thêm số liệu trong `03-tai-lieu-tho/` (file đơn hàng, doanh thu, báo cáo quảng cáo)
và kết quả của `/ts-phan-tich-doanh-thu`, `/ts-bao-cao-facebook-ads`, `/ts-thiet-ke-pheu`, `/ts-phan-tich-doi-thu`
trong `04-ket-qua/`.

## Quy trình AI thực hiện

### Bước 1 — Đọc dữ liệu hiện có
Hồ sơ, dữ liệu bán hàng, marketing, phản hồi khách. File Excel/CSV/ảnh chụp → đọc và tóm tắt
(nếu cần xử lý sâu, gợi ý `/ts-doc-so-lieu-hinh-anh` hoặc `/ts-bang-tinh-excel`).

### Bước 2 — Xác định chỉ số nền (baseline)
Doanh thu, số khách, giá trị đơn trung bình, biên lợi nhuận, chi phí có 1 khách (CAC), tỷ lệ chuyển đổi,
tỷ lệ mua lại, tỷ lệ rời bỏ, LTV. Cách tính và giải thích dễ hiểu trong `references/sau-don-bay.md`.
Đánh dấu chỉ số thiếu `[CẦN BỔ SUNG]` — **không tự bịa**, có thể ước lượng nhưng phải ghi `[ƯỚC TÍNH]` + cách ước.

### Bước 3 — Hỏi tối đa 5 câu quan trọng
Mục tiêu (bao nhiêu, khi nào) · giới hạn (ngân sách, thời gian) · năng lực đội ngũ · thị trường/khu vực ·
thời hạn đánh giá. Có gợi ý A–D.

### Bước 4 — Nghiên cứu bổ sung (nếu cần)
Khi cần dữ liệu thị trường hiện hành và môi trường có công cụ tìm kiếm web: dùng nguồn đáng tin, ghi ngày
kiểm tra và đường dẫn. Không có công cụ → nói rõ và dùng dữ liệu người dùng cung cấp.

### Bước 5 — Phân tích 6 đòn bẩy
Đọc `references/sau-don-bay.md`. Với mỗi đòn bẩy: hiện trạng · dấu hiệu cơ hội · bằng chứng · mức ưu tiên.
Trình **ma trận 6 đòn bẩy** (bảng).

### Bước 6 — Tạo 8–15 sáng kiến, chấm ICE, chọn tối đa 3
Mỗi sáng kiến gắn 1 đòn bẩy và 1 giả thuyết. Chấm Impact – Confidence – Ease (1–10), chọn tối đa 3 ưu tiên.
Với mỗi đòn bẩy được chọn, dùng mẫu: vì sao phù hợp (≤ 70 từ) · kế hoạch 5 bước · 3–5 offer và mức giá
tham khảo · mẫu nội dung/quy trình · KPI và mốc 30/60/90 · rủi ro và cách giảm.

### Bước 7 — Trình phương án (cổng duyệt)
Trình: chẩn đoán, 3 ưu tiên, giả định, rủi ro, khoảng bất định của dự báo. 👉 Chờ "duyệt" hoặc chỉnh.

### Bước 8 — Lập kế hoạch 30/60/90 ngày
Chia thành tháng → tuần → ngày. Mỗi thử nghiệm dùng **thẻ thử nghiệm** (giả thuyết, người phụ trách,
nguồn lực, KPI, ngưỡng dừng/nhân rộng, ngày đánh giá) — mẫu trong `references/sau-don-bay.md`.
Kèm dashboard KPI và nhịp họp đánh giá (tuần/tháng/90 ngày).

### Bước 9 — Phối hợp triển khai (khi người dùng yêu cầu)
Gợi ý lệnh theo đòn bẩy: phễu → `/ts-thiet-ke-pheu`, `/ts-pheu-qua-tang` · upsell/offer → `/ts-dinh-gia-offer` ·
giữ chân → `/ts-email-cham-soc`, `/ts-cham-soc-khach-zalo` · bán theo vấn đề → `/ts-chan-dung-khach-hang`,
`/ts-viet-quang-cao` · đo lường → `/ts-bang-tinh-excel`, `/ts-lap-lich-tu-dong`. Hoặc giao cho `/ts-dieu-phoi-cong-viec`.

### Checklist chất lượng
- [ ] Baseline có nguồn cho từng con số; chỗ thiếu ghi rõ, chỗ ước tính ghi cách ước.
- [ ] Đủ ma trận 6 đòn bẩy; 8–15 sáng kiến có điểm ICE.
- [ ] Tối đa 3 ưu tiên; mỗi ưu tiên có thẻ thử nghiệm đầy đủ.
- [ ] Kế hoạch 30/60/90 có người làm, hạn, KPI; có nhịp họp.
- [ ] Dự báo trình bày dạng khoảng (thấp – vừa – cao), không như kết quả chắc chắn.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** số liệu 3–6 tháng gần nhất nếu có (doanh thu theo tháng, số đơn, chi phí quảng cáo, số khách
mua lại). Xuất ra Excel hoặc chụp màn hình đều được; bỏ vào `03-tai-lieu-tho/` của Bộ Não hoặc gửi kèm.

1. Gõ `/ts-chien-luoc-tang-truong` kèm mục tiêu (vd "tăng doanh thu từ 80 lên 120 triệu/tháng trong 3 tháng").
2. Gửi số liệu hoặc trả lời câu hỏi AI về doanh thu, số đơn, khách mua lại.
3. Trả lời tối đa 5 câu hỏi (chọn A–D).
4. Xem bảng chỉ số nền và ma trận 6 đòn bẩy — hỏi lại chỗ chưa hiểu.
5. Xem 3 việc ưu tiên AI chọn; gõ "duyệt" hoặc nói "tôi muốn ưu tiên khách cũ trước".
6. Nhận kế hoạch 30/60/90 ngày + thẻ thử nghiệm; gõ "duyệt" để lưu vào Bộ Não.
7. Mỗi tuần gõ `/ts-chien-luoc-tang-truong cập nhật kết quả tuần này: …` để AI giúp quyết định giữ/sửa/bỏ.

## Câu lệnh mẫu
- `/ts-chien-luoc-tang-truong tiệm bánh Mây doanh thu 60 triệu/tháng đứng yên 4 tháng, muốn lên 90 triệu`
- `/ts-chien-luoc-tang-truong khóa học online có 800 học viên cũ, muốn bán thêm khóa nâng cao`
- `/ts-chien-luoc-tang-truong spa Hồng khách mới nhiều nhưng ít quay lại, tôi gửi file doanh thu 6 tháng`
- `/ts-chien-luoc-tang-truong shop phụ kiện điện thoại, quảng cáo ngày càng đắt, tìm hướng khác`

## Kết quả nhận được
- Tóm tắt chẩn đoán và bảng chỉ số nền.
- Ma trận 6 đòn bẩy.
- Bảng 8–15 sáng kiến chấm ICE, 3 ưu tiên.
- Kế hoạch 30/60/90 ngày (tháng → tuần → ngày) + thẻ thử nghiệm.
- Dashboard KPI và nhịp họp đánh giá.
- Rủi ro, phụ thuộc và quyết định cần duyệt.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-chien-luoc-tang-truong-<chu-de-khong-dau>/`.
2. Lưu bản chiến lược đã duyệt (baseline, ma trận, ICE, kế hoạch 30/60/90, thẻ thử nghiệm) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-chien-luoc-tang-truong
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [tang-truong, doanh-thu, ke-hoach-90-ngay]
   ---
   ```
   Kèm theo các file phụ (nếu có): `sang-kien-ice.csv`, `ke-hoach-30-60-90.csv`, `the-thu-nghiem.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Chiến lược tăng trưởng]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-chien-luoc-tang-truong · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Chỉ số nền đã xác nhận → đề xuất lưu vào `02-kien-thuc/san-pham/chi-so-nen.md` để lần sau so sánh; mục tiêu
   mới khác `01-ho-so/05-muc-tieu-quy-tac-lien-he.md` → đề xuất cập nhật, hỏi trước khi ghi đè. Thử nghiệm chạy
   nhiều tuần → đề xuất trang theo dõi `05-du-an/tang-truong-<quy>.md`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không hỗ trợ tăng trưởng cho hàng hóa/dịch vụ hạn chế độ tuổi hoặc hoạt động nguy hiểm với người chưa thành niên.
- Không trình bày dự báo như kết quả chắc chắn; luôn nêu giả định và khoảng bất định.
- Không bịa số liệu; dữ liệu khách hàng chỉ dùng dạng tổng hợp, không lưu thông tin cá nhân từng khách.
- Chương trình giới thiệu/khuyến mãi phải minh bạch, không hứa thưởng không trả được.

## Skill liên quan
- Trước: `/ts-phan-tich-doanh-thu` · `/ts-tao-ho-so-doanh-nghiep` · `/ts-bao-cao-facebook-ads`
- Sau: `/ts-thiet-ke-pheu` · `/ts-dinh-gia-offer` · `/ts-email-cham-soc` · `/ts-cham-soc-khach-zalo` · `/ts-dieu-phoi-cong-viec`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
