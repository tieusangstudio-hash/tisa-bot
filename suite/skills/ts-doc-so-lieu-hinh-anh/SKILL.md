---
name: ts-doc-so-lieu-hinh-anh
description: "Gọi bằng /ts-doc-so-lieu-hinh-anh. Đọc và phân tích số liệu từ Excel, CSV, Google Sheets, biểu đồ, dashboard hoặc ảnh chụp màn hình: mô tả những gì nhìn thấy, kiểm tra chất lượng dữ liệu, tính chỉ số có công thức, tìm bất thường và đề xuất 3 việc nên làm. Dùng khi gửi file/ảnh số liệu và hỏi 'số này nói gì', 'lỗi ở đâu', 'nên làm gì tiếp'. Từ khóa: đọc số liệu, phân tích dữ liệu, đọc ảnh chụp màn hình, đọc biểu đồ, phân tích file Excel, dashboard, số liệu này nói gì."
---

# /ts-doc-so-lieu-hinh-anh — Đọc số liệu và hình ảnh

> Biến bảng số, biểu đồ hay ảnh chụp màn hình thành vài kết luận rõ ràng và việc cần làm, có tách bạch:
> điều nhìn thấy, điều tính ra, điều suy đoán và điều chưa chắc.
> Kết quả: báo cáo ngắn gồm tóm tắt, chất lượng dữ liệu, 3 phát hiện chính, bảng bằng chứng và 3 hành động ưu tiên.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Có file Excel/CSV/Google Sheets (doanh thu, đơn hàng, khách, học viên…) và muốn biết "số này nói gì".
- Có ảnh chụp dashboard, báo cáo, biểu đồ (Fanpage Insights, TikTok Analytics, phần mềm bán hàng…) cần đọc giúp.
- Có ảnh chụp màn hình báo lỗi, muốn biết lỗi gì, làm gì tiếp.
- Cần kiểm tra file số liệu có sai, trùng, thiếu trước khi dùng.
- Muốn so sánh 2 kỳ (tuần này – tuần trước, tháng này – tháng trước).

**Không dùng khi:** số liệu quảng cáo Facebook/Instagram → `/ts-bao-cao-facebook-ads`; số liệu TikTok Ads →
`/ts-chay-tiktok-ads`; phân tích doanh thu sâu theo sản phẩm/khách → `/ts-phan-tich-doanh-thu`; cần tạo file Excel/
dashboard mới → `/ts-bang-tinh-excel`; cần AI bấm giúp trên máy tính → `/ts-tro-ly-may-tinh`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

Nguyên tắc xuyên suốt: tách rõ **dữ kiện quan sát được**, **phép tính**, **suy luận** và **phần chưa chắc chắn**.

### Bước 1 — Xác định câu hỏi quyết định
Nêu người dùng cần quyết định gì (vd "có nên nhập thêm hàng mẫu A không", "tuần này Fanpage tụt vì đâu").
Nếu chưa rõ, hỏi **một câu** với gợi ý: (A) Tình hình chung tốt hay xấu · (B) Tìm chỗ bất thường/lỗi · (C) So sánh 2 kỳ ·
(D) Quyết định cụ thể (ghi rõ). Nếu câu hỏi không ảnh hưởng lớn, phân tích tổng quan rồi đề xuất câu hỏi tiếp theo.

### Bước 2 — Kiểm tra đầu vào
Theo checklist chi tiết trong `references/kiem-tra-dau-vao.md`.

**Với bảng dữ liệu:**
- Xác định cột, đơn vị, thời gian, nguồn và cấp độ dữ liệu (mỗi dòng là 1 đơn? 1 ngày? 1 khách?).
- Kiểm tra ô trống, trùng, sai kiểu (số lưu dạng chữ, ngày lẫn định dạng), ngoại lệ (số quá lớn/nhỏ) và tổng không khớp.
- Không trộn phần trăm với số tuyệt đối hoặc các kỳ thời gian khác nhau.
- Dữ liệu cá nhân (số điện thoại, địa chỉ khách) → không chép ra báo cáo, che bớt nếu cần minh họa.

**Với hình ảnh:**
- Mô tả giao diện, chữ, số và đối tượng nhìn thấy (ứng dụng nào, khoảng ngày, bộ lọc đang chọn).
- Ghi phần bị cắt, mờ, quá nhỏ hoặc không đọc chắc; gắn mức tin cậy Cao/Trung bình/Thấp.
- Không suy ra danh tính, nguyên nhân hay trạng thái hệ thống chỉ từ dấu hiệu mơ hồ.
- Ảnh không đọc chắc → xin ảnh rõ hơn hoặc file gốc thay vì đoán.

**Kiểm định dữ liệu trích xuất:**
- Giữ bản dữ liệu thô; tạo bản làm sạch riêng kèm nhật ký thay đổi (bỏ dòng trùng nào, xử lý ô trống ra sao, ngoại lệ giữ hay bỏ).
- Sau khi đọc số từ ảnh (OCR) hoặc trích bảng: đối chiếu tổng, tỉ lệ, và kiểm tra thủ công ít nhất một dòng mẫu.

### Bước 3 — Phân tích theo 3 lớp
1. `QUAN SÁT`: dữ liệu hoặc hình ảnh thể hiện trực tiếp (vd "Doanh thu tuần 45 là 42,3 triệu, tuần 44 là 51,0 triệu").
2. `GIẢI THÍCH`: ý nghĩa hợp lý và giả định đi kèm (vd "Giảm 17%, có thể do tuần 44 có ngày lễ — cần kiểm tra").
3. `HÀNH ĐỘNG`: việc nên kiểm tra hoặc thử tiếp theo (vd "Lọc doanh thu theo sản phẩm để xem mẫu nào giảm").

Khi tính toán, **nêu công thức và mẫu số**:
- Tăng/giảm % = (Kỳ này − Kỳ trước) ÷ Kỳ trước × 100%.
- Tỉ trọng = Phần ÷ Tổng × 100%.
- Giá trị đơn trung bình = Doanh thu ÷ Số đơn.
- Tỉ lệ chuyển đổi = Số người làm hành động ÷ Số người có cơ hội làm × 100%.

Khi so sánh, dùng cùng kỳ (cùng số ngày), cùng mục tiêu, cùng cấp độ.

Ví dụ (shop phụ kiện — giả định): ảnh chụp báo cáo bán hàng tuần cho thấy 120 đơn, doanh thu 18 triệu, 15 đơn hủy.
→ QUAN SÁT: tỉ lệ hủy = 15 ÷ 120 = 12,5%. GIẢI THÍCH: cao hơn tuần trước (6%) — giả thuyết: giao chậm hoặc khách đặt nhầm.
HÀNH ĐỘNG: xuất danh sách đơn hủy, xem lý do hủy và khu vực giao.

### Bước 4 — Trình bày kết quả
Theo mẫu `references/mau-bao-cao.md`, mặc định gồm:
- Tóm tắt 3–5 dòng.
- Chất lượng dữ liệu/ảnh.
- 3 phát hiện quan trọng nhất.
- Bảng chỉ số hoặc chi tiết bằng chứng.
- 3 hành động ưu tiên (việc, lý do, cách đo).
- Dữ liệu còn thiếu (chỉ những gì có thể thay đổi quyết định).

Phân loại đầu ra thành: dữ kiện · bất thường · giả thuyết nguyên nhân · bước kiểm chứng.
Nếu người dùng muốn file Excel/Google Sheets hoặc dashboard → chuyển kết quả sang `/ts-bang-tinh-excel` thay vì chỉ dán bảng văn bản.
Nếu môi trường có công cụ vẽ biểu đồ và biểu đồ giúp ra quyết định, có thể vẽ 1 biểu đồ đơn giản (cột hoặc đường).

### Bước 5 — Giới hạn kết luận
- Không khẳng định quan hệ nhân quả chỉ từ tương quan ("đăng nhiều video thì doanh thu tăng" chưa chắc là nhờ video).
- Không gọi một thay đổi là xu hướng nếu chỉ có một hoặc hai điểm dữ liệu.
- Không đưa quyết định ngân sách quảng cáo chỉ từ ảnh thiếu mục tiêu, kỳ thời gian hoặc chuyển đổi.
- Yêu cầu ảnh gốc hoặc file dữ liệu khi độ tin cậy không đủ.

### Cổng duyệt
Trình báo cáo; người dùng hỏi thêm hoặc yêu cầu đào sâu. Chỉ lưu vào Bộ Não khi người dùng gõ **"duyệt"** hoặc "lưu lại".

### Checklist chất lượng trước khi giao
- [ ] Đã ghi rõ vùng nhìn rõ/mờ/bị cắt, đơn vị, khoảng thời gian trước khi kết luận.
- [ ] Mỗi con số tính ra có công thức và mẫu số.
- [ ] Không có kết luận nhân quả, xu hướng thiếu căn cứ.
- [ ] Dữ liệu cá nhân của khách không xuất hiện trong báo cáo.
- [ ] Đúng 3 hành động ưu tiên, mỗi cái có cách đo.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** file gốc (tốt nhất) hoặc ảnh chụp màn hình rõ nét. Mẹo chụp ảnh:
- Chụp cả **dòng tiêu đề cột** và **khoảng ngày/bộ lọc** đang chọn.
- Không chụp nghiêng; phóng to vừa đủ để đọc số; bảng dài thì chụp nhiều ảnh nối tiếp.
- Che số điện thoại/địa chỉ khách nếu không cần thiết.
- Google Sheets: **Tệp → Tải xuống → .csv** hoặc **.xlsx** rồi gửi file.

1. Gõ `/ts-doc-so-lieu-hinh-anh`, đính kèm file/ảnh, kèm 1 câu bạn muốn biết (vd "tháng này bán kém hơn vì sao?").
2. Trả lời câu hỏi AI (nếu có), chọn chữ cái A-B-C-D.
3. Đọc phần **Tóm tắt** và **3 hành động** trước. Chỗ nào AI ghi "chưa chắc" thì gửi thêm ảnh/file nếu có.
4. Hỏi tiếp bằng lời: "đào sâu sản phẩm A", "so với tháng trước", "giải thích tỉ lệ chuyển đổi là gì".
5. Muốn có file Excel/dashboard từ kết quả: gõ "làm thành file Excel" (AI chuyển sang `/ts-bang-tinh-excel`).
6. Gõ **"duyệt"** để AI lưu báo cáo vào Bộ Não (nếu có).

## Câu lệnh mẫu
- `/ts-doc-so-lieu-hinh-anh đây là file doanh thu 3 tháng của shop quần áo, mẫu nào nên nhập thêm? [đính kèm Excel]`
- `/ts-doc-so-lieu-hinh-anh ảnh chụp thống kê Fanpage spa Hồng 28 ngày, lượt tiếp cận tụt mạnh, đọc giúp`
- `/ts-doc-so-lieu-hinh-anh danh sách học viên khóa học quay video, kiểm tra trùng, thiếu số điện thoại, ai chưa đóng đủ học phí`
- `/ts-doc-so-lieu-hinh-anh màn hình phần mềm bán hàng báo lỗi này là gì, tôi nên làm gì? [đính kèm ảnh]`

## Kết quả nhận được
- Báo cáo ngắn: tóm tắt, chất lượng dữ liệu/ảnh, 3 phát hiện, bảng bằng chứng (có công thức), 3 hành động ưu tiên, dữ liệu còn thiếu.
- Nhãn rõ ràng cho từng ý: QUAN SÁT / GIẢI THÍCH / HÀNH ĐỘNG và mức chắc chắn.
- (Nếu làm sạch dữ liệu) Bản dữ liệu sạch riêng và nhật ký thay đổi; file gốc giữ nguyên.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-doc-so-lieu-hinh-anh-<chu-de-khong-dau>/`.
2. Lưu báo cáo phân tích đã duyệt (tóm tắt, phát hiện, bảng bằng chứng, hành động, dữ liệu thiếu) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-doc-so-lieu-hinh-anh
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd so-lieu, doanh-thu, fanpage>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `du-lieu-sach.csv`, `nhat-ky-lam-sach.md`, ảnh gốc người dùng gửi (đã che dữ liệu cá nhân).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-doc-so-lieu-hinh-anh · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bịa số: ô không đọc được ghi `[CẦN BỔ SUNG]` hoặc xin ảnh rõ hơn.
- Không khẳng định nhân quả từ tương quan; không gọi xu hướng khi chỉ có 1–2 điểm dữ liệu.
- Không suy ra danh tính người trong ảnh, không đoán trạng thái hệ thống từ dấu hiệu mơ hồ.
- Không sửa file gốc; mọi làm sạch tạo bản riêng.
- Ảnh có mật khẩu, mã OTP, số thẻ → nhắc người dùng xóa/che và không chép lại các thông tin đó.

## Skill liên quan
- Trước: (không bắt buộc) · Sau: `/ts-bang-tinh-excel`, `/ts-phan-tich-doanh-thu`, `/ts-bao-cao-facebook-ads`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
