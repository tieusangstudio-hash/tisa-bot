---
name: ts-ke-hoach-loi-nhuan
description: "Gọi bằng /ts-ke-hoach-loi-nhuan. Dẫn từng bước lập kế hoạch lợi nhuận: mục tiêu lời mỗi tháng, lãi gộp sản phẩm, chi phí cố định, chi phí mỗi đơn, điểm hòa vốn, số đơn cần bán, vốn ban đầu và số tháng hồi vốn, dự toán 3 kịch bản, cảnh báo; tính ngược muốn thu nhập X cần bao nhiêu khách, bao nhiêu lượt tiếp cận. Xuất bảng và file CSV mở bằng Excel. Từ khóa: điểm hòa vốn, kế hoạch lợi nhuận, bán bao nhiêu để hòa vốn, lãi gộp, chi phí cố định, hồi vốn, dự toán, cần bao nhiêu khách."
---

# /ts-ke-hoach-loi-nhuan — Kế hoạch lợi nhuận & điểm hòa vốn

> Trả lời rõ bằng con số: **phải bán bao nhiêu đơn mỗi tháng để không lỗ, bao nhiêu để lời đúng mục tiêu, bao lâu hồi vốn**, cần bao nhiêu khách và lượt tiếp cận — kèm bảng dự toán 3 kịch bản và file mở bằng Excel. Mọi thuật ngữ đều được giải thích bằng lời đơn giản.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Sắp mở cửa hàng/dịch vụ/kênh bán mới, muốn biết có lời không trước khi bỏ vốn.
- Đang bán mà không rõ lời hay lỗ, bao nhiêu đơn thì hòa vốn.
- Đặt mục tiêu thu nhập (vd 30 triệu/tháng) và muốn biết cần bao nhiêu khách, bao nhiêu người tiếp cận.
- Cân nhắc thuê thêm người, thuê mặt bằng lớn hơn, tăng ngân sách quảng cáo.
- Cần bảng dự toán để trình người góp vốn/đối tác.

**Không dùng khi:** cần đặt giá và đóng gói gói sản phẩm → dùng `/ts-dinh-gia-offer` trước. Cần phân tích doanh thu thực tế đã bán → dùng `/ts-phan-tich-doanh-thu`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `ke-hoach-loi-nhuan` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

Nếu Bộ Não có kết quả `/ts-dinh-gia-offer` (giá, chi phí mỗi đơn) hoặc `/ts-mo-hinh-kinh-doanh` (cơ cấu chi phí) trong `04-ket-qua/` → dùng luôn, chỉ hỏi xác nhận.

**Chế độ:** hỏi người dùng muốn **(A) Kế hoạch đầy đủ 9 bước** (~20 phút) hay **(B) Tính nhanh** "muốn thu nhập X/tháng cần bao nhiêu khách" (~3 phút, chỉ hỏi giá, lãi gộp, chi phí cố định, tỉ lệ chốt). Chế độ B chạy Bước 1, 2, 3, 6 và mục "Tính ngược" rồi trình kết quả.

Mỗi bước: hỏi 1–3 câu có gợi ý (bộ câu hỏi trong `references/giai-thich-thuat-ngu.md`, mục 2), **giải thích thuật ngữ bằng 1 câu đời thường + 1 ví dụ** khi nhắc lần đầu (từ điển ở mục 1), tóm lại con số rồi mới sang bước sau. Không biết số → AI đề xuất giả định hợp lý và ghi **[Giả định]**.

### Bước 1 — Mục tiêu lợi nhuận mỗi tháng
Lợi nhuận = tiền thật sự còn lại sau khi trả hết chi phí. Nhắc: ghi **lương của chính chủ** vào chi phí cố định để lợi nhuận là phần dư thật.

### Bước 2 — Sản phẩm chủ lực và lãi gộp
Liệt kê 1–5 sản phẩm chính: giá bán, tỉ trọng số đơn. **Lãi gộp mỗi đơn** = giá bán − chi phí biến đổi mỗi đơn (tiền còn lại để trả chi phí cố định và tạo lời). Nhiều sản phẩm → tính bình quân theo tỉ trọng. Chỉ ra món lãi gộp cao nhất nên đẩy mạnh.

### Bước 3 — Chi phí cố định (mỗi tháng)
Tiền phải trả dù bán 0 đơn: mặt bằng, lương cứng, điện nước, phần mềm, khấu hao/trả góp, kế toán… Dùng danh sách gợi ý để không sót.

### Bước 4 — Chi phí biến đổi mỗi đơn
Tiền tốn thêm mỗi khi bán thêm 1 đơn: giá vốn, bao bì, giao hàng, phí sàn, **phí thanh toán**, hoa hồng, **quảng cáo trung bình mỗi đơn**. Phí tính theo % giá → ghi vào `phi_phan_tram_tren_gia`.

### Bước 5 — Điểm hòa vốn
**Q = Chi phí cố định ÷ (Giá − Chi phí biến đổi)** → "Bán ít nhất Q đơn/tháng (≈ Q/30 đơn/ngày) thì không lỗ."

### Bước 6 — Số đơn cần để đạt mục tiêu
**(Chi phí cố định + Lợi nhuận mục tiêu) ÷ (Giá − Chi phí biến đổi)**. So với công suất tối đa (số đơn làm nổi mỗi tháng với người và máy hiện có).

### Bước 7 — Vốn ban đầu và số tháng hồi vốn
Liệt kê vốn: máy móc, sửa sang, cọc mặt bằng, hàng đầu tiên, giấy phép, **quỹ dự phòng ≥ 3 tháng chi phí cố định**. **Tháng hồi vốn = Vốn ban đầu ÷ Lợi nhuận mỗi tháng.**

### Bước 8 — Bảng dự toán 3 kịch bản
**Thận trọng** (~60% kỳ vọng, chi phí biến đổi +10%) · **Cơ sở** (kỳ vọng hợp lý) · **Tốt** (~140% kỳ vọng). Mỗi kịch bản: số đơn, doanh thu, chi phí biến đổi, lãi gộp, chi phí cố định, lợi nhuận, biên lợi nhuận, đơn hòa vốn, vùng an toàn, tháng hồi vốn. Quyết định dựa trên kịch bản **Thận trọng**.

### Bước 9 — Cảnh báo và việc nên làm
Nêu mọi dấu hiệu nguy hiểm (danh sách ở `references/giai-thich-thuat-ngu.md`, Bước 9): lãi gộp ≤ 0 hoặc < 20%, vùng an toàn < 20%, vượt công suất, hồi vốn > 18 tháng, thiếu quỹ dự phòng, kịch bản thận trọng lỗ. Kèm 3 việc cụ thể nên làm (tăng lãi gộp mỗi đơn bằng cách tăng giá trị rồi tăng giá, cắt chi phí không tạo ra khách, đẩy món lãi gộp cao…).

### Tính ngược — "Muốn thu nhập X/tháng cần bao nhiêu khách, bao nhiêu lượt tiếp cận"
```
Đơn cần       = (Chi phí cố định + X) ÷ Lãi gộp mỗi đơn
Khách cần     = Đơn cần ÷ Số đơn mỗi khách/tháng
Người hỏi     = Khách cần ÷ Tỉ lệ chốt
Lượt tiếp cận = Người hỏi ÷ Tỉ lệ (người thấy → người hỏi)
```
Tỉ lệ tham khảo để bắt đầu giả định ở `references/giai-thich-thuat-ngu.md` mục 3. **Luôn ghi rõ các tỉ lệ là giả định** và hẹn đo lại sau 2–4 tuần. Có chi phí 1.000 lượt tiếp cận → ước ngân sách quảng cáo và đối chiếu với khoản quảng cáo/đơn ở Bước 4.

### Chạy script
Ghi dữ liệu theo mẫu `scripts/vi-du-ke-hoach.json` rồi chạy:
- macOS: `python3 scripts/hoa_von.py scripts/vi-du-ke-hoach.json --out ke-hoach.md --csv du-toan.csv`
- Windows: `py scripts\hoa_von.py scripts\vi-du-ke-hoach.json --out ke-hoach.md --csv du-toan.csv`

Chỉ cần Python 3. File CSV mở bằng Excel/Google Sheets; Excel dồn 1 cột thì thêm `--csv-sep ";"`. Không ghi `kich_ban` thì script tự tạo 3 kịch bản từ `so_don_du_kien_thang`. Không chạy được script → AI tự tính và trình bảng cùng định dạng, ghi rõ công thức.

### Checklist chất lượng
- [ ] Mỗi thuật ngữ được giải thích bằng lời đơn giản ở lần đầu nhắc.
- [ ] Lương chủ đã nằm trong chi phí cố định (hoặc đã nói rõ là chưa tính).
- [ ] Chi phí biến đổi có phí thanh toán và quảng cáo/đơn.
- [ ] Mọi con số giả định có nhãn [Giả định].
- [ ] Có đủ: hòa vốn, đơn cho mục tiêu, vốn, hồi vốn, 3 kịch bản, cảnh báo.
- [ ] Phép tính khớp công thức (AI kiểm lại 1 dòng bằng tay).

### Ví dụ minh họa (doanh nghiệp giả định)
*Ví dụ: "Tiệm bánh Mây" — bánh kem đặt online, 1 bếp nhỏ* (dữ liệu `scripts/vi-du-ke-hoach.json`).
- 2 sản phẩm: bánh kem 450 nghìn (70% đơn) và hộp bánh mini 180 nghìn (30%). Lãi gộp bình quân **191.120 đ/đơn** (51,8%).
- Chi phí cố định 18 triệu/tháng → **hòa vốn 95 đơn/tháng**.
- Mục tiêu lời 30 triệu → cần **252 đơn/tháng (~9 đơn/ngày)**, dưới công suất 300 đơn.
- Vốn 104 triệu (gồm quỹ dự phòng 36 triệu) → hồi vốn **4,3 tháng** ở kịch bản cơ sở (220 đơn, lời ~24 triệu), nhưng **22,9 tháng** ở kịch bản thận trọng (130 đơn).
- Tính ngược: 252 đơn ÷ tỉ lệ chốt 25% = 1.008 người hỏi ÷ 1,5% = **67.200 lượt tiếp cận/tháng** (~2.240/ngày) [Giả định].
- Cảnh báo: kịch bản cơ sở chưa đạt mục tiêu 30 triệu → cần thêm 32 đơn hoặc tăng lãi gộp mỗi đơn.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (15 phút):** giá bán các món chính; chi phí cho 1 đơn (nguyên liệu/giá nhập, bao bì, giao hàng, phí sàn); các khoản trả hằng tháng (mặt bằng, lương, điện nước, phần mềm); số tiền đã/định bỏ ra ban đầu; (nếu có) tiền quảng cáo và số đơn tháng trước. Chưa có số chính xác thì ước lượng.
1. Gõ `/ts-ke-hoach-loi-nhuan` kèm mục tiêu (vd "muốn lời 30 triệu/tháng").
2. Chọn chế độ: A (đầy đủ) hoặc B (tính nhanh cần bao nhiêu khách).
3. Trả lời từng bước. Gặp từ lạ, hỏi lại ngay "lãi gộp là gì?" — AI sẽ giải thích bằng ví dụ.
4. Không nhớ số → nói "chưa biết", AI đề xuất số giả định để bạn sửa.
5. Xem bảng 3 kịch bản: nhìn kỹ dòng **Thận trọng** — nếu lỗ, bạn có đủ tiền chịu được bao lâu?
6. Đọc phần cảnh báo, chọn 1–2 việc làm ngay.
7. Gõ **duyệt** để lưu kế hoạch và file `du-toan.csv` vào Bộ Não. Mở CSV bằng Excel hoặc Google Sheets.
8. Mỗi tháng, gõ `/ts-ke-hoach-loi-nhuan cập nhật số thật tháng này: …` để so kế hoạch với thực tế.

## Câu lệnh mẫu
- `/ts-ke-hoach-loi-nhuan Tôi định mở quán cà phê mang đi 20m², giá ly trung bình 35 nghìn — bán bao nhiêu ly mới hòa vốn?`
- `/ts-ke-hoach-loi-nhuan Shop thời trang online trên TikTok Shop, muốn lời 50 triệu/tháng, lập kế hoạch đầy đủ.`
- `/ts-ke-hoach-loi-nhuan tính nhanh: khóa học online giá 1,2 triệu, muốn thu nhập 40 triệu/tháng thì cần bao nhiêu học viên, bao nhiêu lượt tiếp cận?`
- `/ts-ke-hoach-loi-nhuan Spa 3 giường muốn thuê thêm 1 kỹ thuật viên 9 triệu/tháng — có đáng không?`

## Kết quả nhận được
- Bảng sản phẩm: giá, chi phí biến đổi, lãi gộp, tỉ lệ lãi gộp, bình quân.
- Danh sách chi phí cố định và vốn ban đầu.
- Điểm hòa vốn, số đơn cần cho mục tiêu (theo tháng và theo ngày), thời gian hồi vốn.
- Bảng dự toán 3 kịch bản + file `du-toan.csv` mở bằng Excel/Google Sheets.
- Bảng tính ngược: đơn → khách → người hỏi → lượt tiếp cận (ghi rõ giả định).
- Cảnh báo và 3 việc nên làm.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-ke-hoach-loi-nhuan-<chu-de-khong-dau>/`.
2. Lưu báo cáo kế hoạch lợi nhuận đầy đủ (hòa vốn, mục tiêu, vốn, 3 kịch bản, tính ngược, cảnh báo) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-ke-hoach-loi-nhuan
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `ke-hoach.json` (dữ liệu đầu vào để chạy lại), `du-toan.csv` (bảng 3 kịch bản cho Excel).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-ke-hoach-loi-nhuan · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu mục tiêu lợi nhuận, số đơn cần bán/tháng hoặc ngân sách quảng cáo đã chốt khác với `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`, đề xuất cập nhật mục Mục tiêu/KPI và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Đây là **dự toán**, không phải cam kết. Số thật sẽ khác — cập nhật mỗi tháng.
- Không bịa tỉ lệ chuyển đổi, chi phí quảng cáo như số thống kê; luôn ghi [Giả định] và hẹn đo lại.
- Không khuyên vay nợ, thế chấp tài sản dựa trên kịch bản Tốt. Ra quyết định theo kịch bản **Thận trọng**.
- Thuế, bảo hiểm, giấy phép: nhắc học viên hỏi kế toán; AI chỉ đưa vào bảng khi người dùng cung cấp số.
- Không lưu số tài khoản ngân hàng, mật khẩu hay thông tin vay nợ cá nhân vào Bộ Não.

## Skill liên quan
- Trước: `/ts-mo-hinh-kinh-doanh` · `/ts-dinh-gia-offer`
- Sau: `/ts-thiet-ke-pheu` · `/ts-len-camp-facebook` · `/ts-phan-tich-doanh-thu` · `/ts-bang-tinh-excel`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
