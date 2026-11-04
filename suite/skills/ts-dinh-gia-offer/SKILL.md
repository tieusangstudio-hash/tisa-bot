---
name: ts-dinh-gia-offer
description: "Gọi bằng /ts-dinh-gia-offer. Định giá theo giá trị và đóng gói offer: chấm phương trình giá trị (Value Equation), biến trở ngại của khách thành thành phần offer, tính giá sàn không lỗ và giá trần theo giá trị hoặc đối thủ, dựng bảng 3 gói Cơ bản – Tiêu chuẩn – Cao cấp có biên lợi nhuận, bảo hành, quà tặng, khan hiếm thật, neo giá. Dùng khi ra giá sản phẩm mới, khách chê đắt, muốn tăng giá. Từ khóa: định giá, bảng giá, offer, gói dịch vụ, combo, khách chê đắt, tăng giá, giá sàn, 3 gói."
---

# /ts-dinh-gia-offer — Định giá theo giá trị & đóng gói offer

> Giúp bạn ra giá **không lỗ** mà vẫn **đáng tiền** trong mắt khách: tính giá sàn, giá trần, đóng gói thành **bảng 3 gói** có biên lợi nhuận, bảo hành, quà tặng và cách trình bày giá. Khách chê đắt → **tăng giá trị**, không giảm giá.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Ra sản phẩm/dịch vụ/khóa học mới, chưa biết đặt giá bao nhiêu.
- Bán nhiều mà lời ít, nghi giá đang quá thấp.
- Khách hay chê đắt, so giá với đối thủ.
- Muốn tăng giá mà không mất khách.
- Muốn có bảng giá 3 gói rõ ràng để khách tự chọn.

**Không dùng khi:** cần tính số đơn hòa vốn và kế hoạch lợi nhuận cả tháng → dùng `/ts-ke-hoach-loi-nhuan`. Cần câu trả lời khi khách đang chê đắt trong tin nhắn → dùng `/ts-xu-ly-tu-choi`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `dinh-gia-offer` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Hiểu sản phẩm và khách (hỏi tối đa 4 câu, có gợi ý)
Nếu Bộ Não có kết quả `/ts-chan-dung-khach-hang` (nỗi đau, mong muốn) và `/ts-phan-tich-doi-thu` (giá đối thủ) trong `04-ket-qua/` hoặc `02-kien-thuc/doi-thu/` → dùng luôn, bỏ qua câu đã có đáp án.
1. Sản phẩm/dịch vụ cần định giá là gì? Giá hiện tại (nếu có)?
2. Khách mua để đạt **kết quả gì**? (A. kiếm thêm tiền · B. tiết kiệm thời gian · C. đẹp/khỏe/tự tin hơn · D. bớt lo lắng, rủi ro)
3. Khách đang so với lựa chọn nào? (A. đối thủ cùng loại · B. tự làm · C. không làm gì · D. sản phẩm thay thế khác)
4. Đối thủ bán bao nhiêu? (ghi 2–5 mức giá; không biết thì AI tìm trên web nếu có công cụ, ghi link + ngày)

### Bước 2 — Chấm phương trình giá trị (Value Equation)
Chấm 4 yếu tố thang 1–10 (giải thích trong `references/dong-goi-offer.md`, mục 1):
**Kết quả mơ ước** (tăng) · **Khả năng tin đạt được** (tăng) · **Thời gian chờ** (giảm) · **Công sức** (giảm).
Chỉ số = (Kết quả × Tin) ÷ (Thời gian × Công sức). Chỉ ra yếu tố yếu nhất → đó là chỗ thêm giá trị rẻ nhất.

### Bước 3 — Liệt kê trở ngại → biến thành thành phần offer
- Liệt kê 8–15 trở ngại khách gặp trước, trong, sau khi mua.
- Viết lại mỗi trở ngại thành "Làm sao để…", rồi thành 1 thành phần: **tự làm** (tài liệu, mẫu) / **làm cùng** (nhóm, buổi hỏi đáp) / **làm giúp**.
- Lọc giữ thành phần giá trị cao, chi phí thấp. Thành phần tốn công đưa vào gói cao cấp.

### Bước 4 — Xếp gói giá trị (value stack)
Liệt kê thành phần + **giá trị quy đổi có căn cứ** (giá từng bán lẻ, giá thị trường, chi phí khách tự làm). Ghi căn cứ cạnh mỗi con số. Không thổi phồng.

### Bước 5 — Tính GIÁ SÀN và GIÁ TRẦN
Hỏi chi phí (giải thích bằng lời đơn giản):
- **Chi phí biến đổi** = tiền tốn thêm mỗi khi bán thêm 1 đơn (giá vốn, đóng gói, giao hàng, thuê ngoài…).
- **Chi phí cố định** = tiền phải trả mỗi tháng dù bán được hay không (mặt bằng, lương cứng, phần mềm…).
- **Phí theo % giá** = phí sàn, cổng thanh toán, hoa hồng, thuế khoán…
- **Biên lợi nhuận mong muốn** = phần lời muốn giữ lại trên mỗi đồng doanh thu (gợi ý 20–40%).

Công thức:
- **Giá hòa vốn** = (Biến đổi + Phân bổ cố định mỗi đơn) ÷ (1 − Phí %). Thấp hơn là lỗ.
- **GIÁ SÀN** = (Biến đổi + Phân bổ cố định mỗi đơn) ÷ (1 − Phí % − Biên mong muốn).
- **GIÁ TRẦN** (tham chiếu) = thấp hơn trong 2 mốc: **theo giá trị** (giá trị khách cảm nhận × 20–30%) và **theo đối thủ** (giá đối thủ cao nhất cùng tầng + 10–30% nếu bạn khác biệt rõ).

Ghi vào file JSON theo mẫu `scripts/vi-du-dinh-gia.json` rồi chạy `scripts/dinh_gia.py` (cách chạy bên dưới). Không chạy được thì AI tự tính và trình bảng cùng định dạng.

### Bước 6 — Dựng bảng 3 gói
| | Cơ bản | Tiêu chuẩn (nên chọn) | Cao cấp |
|---|---|---|---|
| Cách giao | Tự làm | Làm cùng | Làm giúp |
| Giá | ≥ giá sàn | ≈ 2–3 × Cơ bản | ≈ 2–3 × Tiêu chuẩn |

Mỗi gói ghi: thành phần, giá, biên lãi gộp, lãi ròng/đơn, chỉ số giá trị, bảo hành, quà tặng. Gói nào dưới sàn → script báo **LỖ/DƯỚI SÀN**; trên trần → **TRÊN TRẦN** (cần thêm giá trị/bằng chứng).

### Bước 7 — Bọc offer
- **Bảo hành/đảm bảo:** chọn 1 loại trong `references/dong-goi-offer.md` mục 5 — chỉ hứa điều chắc chắn làm được, ghi rõ điều kiện.
- **Quà tặng:** 1–3 quà giải đúng trở ngại, chi phí thấp.
- **Khan hiếm THẬT:** chỉ dùng giới hạn có thật (năng lực, khai giảng, mùa vụ). Cấm "còn 2 suất" giả, đồng hồ đếm ngược tự chạy lại.
- **Tên offer:** ngắn, nói kết quả (vd "Gói 30 video bán hàng trong 7 ngày").

### Bước 8 — Cách trình bày giá (neo giá)
Giá trị trước, giá sau · neo bằng con số lớn có thật (chi phí thuê ngoài, tổng giá trị thành phần) · đặt gói cao cấp nổi bật để gói giữa hợp lý · chia nhỏ theo ngày khi phép chia đúng. Viết sẵn 1 đoạn trình bày giá mẫu (≤ 120 chữ) để dán vào bài bán hàng.

### Bước 9 — Trình bản nháp và chờ duyệt
Trình: chỉ số giá trị → trở ngại & thành phần → bảng 3 gói (kèm kết quả script) → bảo hành, quà, khan hiếm → đoạn trình bày giá → cảnh báo. Hỏi: "Bạn muốn chỉnh gì? Gõ **duyệt** để lưu."

### Checklist chất lượng
- [ ] Mọi gói ≥ giá sàn; gói trên trần có lý do và bằng chứng đi kèm.
- [ ] Gói sau đắt hơn gói trước 1,5–3 lần và có chỉ số giá trị cao hơn.
- [ ] Giá trị quy đổi có căn cứ; giá đối thủ có link + ngày kiểm tra.
- [ ] Bảo hành thực hiện được; khan hiếm có thật.
- [ ] Không có lời khuyên "giảm giá" khi khách chê đắt — chỉ tăng giá trị hoặc hướng xuống gói thấp hơn.

### Chạy script
- macOS: `python3 scripts/dinh_gia.py scripts/vi-du-dinh-gia.json --out bang-gia.md`
- Windows: `py scripts\dinh_gia.py scripts\vi-du-dinh-gia.json --out bang-gia.md`

Chỉ cần Python 3. Script in giá hòa vốn, giá sàn, giá trần, biên lãi gộp, lãi ròng/đơn, chỉ số giá trị, tổng tháng; cảnh báo gói lỗ, dưới sàn, trên trần, bậc giá quá gần.

### Ví dụ minh họa (doanh nghiệp giả định)
*Ví dụ: "Studio Nắng" — chụp ảnh & quay video sản phẩm cho shop online* (dữ liệu `scripts/vi-du-dinh-gia.json`). Chi phí cố định 24 triệu/tháng, dự kiến 36 đơn → phân bổ 666.667 đ/đơn; phí 5%; biên mong muốn 30%.

| Gói | Giá | Giá sàn | Giá trần | Biên lãi gộp | Chỉ số giá trị |
|---|---:|---:|---:|---:|---:|
| Cơ bản — 10 ảnh | 1.500.000 đ | 1.487.179 đ | 1.500.000 đ | 75,0% | 1,2 |
| Tiêu chuẩn — 30 ảnh + 3 video | 3.500.000 đ | 2.794.872 đ | 4.500.000 đ | 62,1% | 4,08 |
| Cao cấp — 60 ảnh + 10 video + người mẫu + ý tưởng 1 tháng | 8.000.000 đ | 7.487.179 đ | 8.400.000 đ | 42,5% | 12,0 |

Lợi nhuận tháng dự kiến ≈ 38,2 triệu. Gói Cơ bản sát sàn → không giảm thêm; nếu khách chê đắt, thêm "giao ảnh trong 48 giờ" (giảm thời gian chờ) thay vì giảm giá. Bảo hành: "Ảnh chưa ưng, chụp lại miễn phí 1 lần." Khan hiếm thật: "Mỗi tháng chỉ nhận 4 gói Cao cấp vì 1 ê-kíp."

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** danh sách chi phí mỗi tháng (mặt bằng, lương, phần mềm…); chi phí cho mỗi đơn (giá vốn, giao hàng, phí sàn…); giá của 2–3 đối thủ; ước lượng số đơn/tháng. Chưa có số chính xác thì ước lượng — AI sẽ ghi là giả định.
1. Gõ `/ts-dinh-gia-offer` kèm tên sản phẩm và giá hiện tại (nếu có).
2. Trả lời 4 câu hỏi (gõ chữ cái A-B-C-D).
3. Chấm 4 yếu tố giá trị cùng AI — trả lời thật, đừng chấm cao cho đẹp.
4. Đọc danh sách trở ngại, bổ sung những gì khách hay than mà AI chưa nhắc.
5. Đưa số liệu chi phí khi AI hỏi. AI tính và cho xem bảng 3 gói.
6. Thấy gói nào báo **LỖ** hoặc **DƯỚI SÀN** → sửa ngay (tăng giá trị rồi tăng giá, hoặc bớt chi phí).
7. Gõ **duyệt** để lưu bảng giá vào Bộ Não.
8. Dùng đoạn trình bày giá trong bài bán hàng (`/ts-viet-bai-ban-hang`) hoặc trang bán hàng (`/ts-trang-ban-hang`).

## Câu lệnh mẫu
- `/ts-dinh-gia-offer Tôi bán son handmade 150 nghìn/thỏi, khách hay chê đắt so với hàng chợ.`
- `/ts-dinh-gia-offer Dịch vụ dọn dẹp văn phòng theo tháng — dựng giúp bảng 3 gói có biên lợi nhuận.`
- `/ts-dinh-gia-offer Khóa học online dạy edit video bằng điện thoại, muốn tăng giá từ 499 nghìn lên 1,5 triệu.`
- `/ts-dinh-gia-offer Tiệm bánh nhận đặt bánh sinh nhật — tính giá sàn cho bánh 2 tầng và gói tiệc.`

## Kết quả nhận được
- Chỉ số giá trị (Value Equation) và yếu tố cần cải thiện.
- Danh sách trở ngại → thành phần offer (tự làm / làm cùng / làm giúp).
- Bảng 3 gói: thành phần, giá, giá sàn, giá trần, biên lãi gộp, lãi ròng/đơn.
- Bảo hành, quà tặng, khan hiếm thật, tên offer.
- Đoạn trình bày giá mẫu (neo giá) dán được ngay.
- Cảnh báo gói lỗ/dưới sàn/trên trần.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-dinh-gia-offer-<chu-de-khong-dau>/`.
2. Lưu toàn bộ phân tích giá trị, bảng 3 gói, bảo hành, quà, khan hiếm và đoạn trình bày giá thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-dinh-gia-offer
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `dinh-gia.json` (dữ liệu chi phí và giá), `bang-gia.md` (kết quả script), `bang-gia.csv` (nếu người dùng muốn mở bằng Excel).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-dinh-gia-offer · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu bảng giá đã chốt khác với `01-ho-so/02-san-pham-dich-vu.md` (hoặc tệp còn trống), trình đoạn đề xuất cập nhật (tên gói, giá, thành phần, bảo hành) và hỏi trước khi ghi đè. Giá đối thủ có thể lưu thêm vào `02-kien-thuc/doi-thu/`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Không bịa** giá đối thủ, testimonial, số khách đã mua, giá trị quy đổi. Thiếu thì ghi `[CẦN BỔ SUNG: …]`.
- **Khan hiếm phải thật**, bảo hành phải thực hiện được — khan hiếm giả và hứa suông làm mất uy tín, có thể vi phạm quy định quảng cáo.
- Không đổi giá đang niêm yết trên web/sàn/quảng cáo khi người dùng chưa nói rõ "duyệt".
- Giá sàn phụ thuộc số đơn dự kiến: bán ít hơn dự kiến thì phân bổ cố định mỗi đơn tăng → kiểm lại bằng `/ts-ke-hoach-loi-nhuan`.
- Thuế: nhắc học viên hỏi kế toán về thuế áp dụng cho loại hình của mình; ghi phần thuế khoán vào "phí theo % giá" nếu đã biết.

## Skill liên quan
- Trước: `/ts-chan-dung-khach-hang` · `/ts-phan-tich-doi-thu` · `/ts-mo-hinh-kinh-doanh`
- Sau: `/ts-ke-hoach-loi-nhuan` · `/ts-viet-bai-ban-hang` · `/ts-trang-ban-hang` · `/ts-xu-ly-tu-choi`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
