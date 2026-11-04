---
name: ts-phan-tich-doanh-thu
description: "Gọi bằng /ts-phan-tich-doanh-thu. Phân tích số liệu kinh doanh bằng lời dễ hiểu: dự báo doanh thu 90 ngày, bảng 10 chỉ số KPI, phân tích lãi lỗ quảng cáo theo 4 kịch bản, bảng chi phí vận hành và điểm hòa vốn, tìm nguyên nhân doanh thu giảm — luôn kết thúc bằng 3 việc ưu tiên. Dùng khi cần biết đang lời hay lỗ, nên tăng ngân sách không, vì sao doanh thu giảm. Từ khóa: phân tích doanh thu, KPI, ROAS, ROI quảng cáo, dự báo doanh thu, chi phí mỗi khách, doanh thu giảm, dashboard Google Sheets, hòa vốn."
---

# /ts-phan-tich-doanh-thu — Phân tích & dự báo doanh thu

> Biến số liệu bán hàng, quảng cáo, chi phí của bạn thành câu trả lời rõ ràng: đang lời hay lỗ, chỉ số nào đang
> yếu, nguyên nhân ở đâu, tháng tới cần bao nhiêu khách — và 3 việc nên làm ngay tuần này.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Muốn dự báo doanh thu 1–3 tháng tới: cần bao nhiêu khách, bao nhiêu tiền quảng cáo.
- Muốn có bảng theo dõi chỉ số (KPI) hằng tuần, biết ngưỡng nào là báo động.
- Muốn biết quảng cáo đang lời hay lỗ, có nên tăng ngân sách không.
- Muốn tính tổng chi phí vận hành, cần bán bao nhiêu đơn để hòa vốn.
- Doanh thu tự nhiên giảm — cần tìm nguyên nhân gốc.
- Muốn dựng bảng theo dõi trên Google Sheets / Excel.

**Không dùng khi:** cần phân tích chi tiết từng chiến dịch/quảng cáo Facebook → `/ts-bao-cao-facebook-ads`; số liệu
mạng xã hội (lượt xem, tương tác) → `/ts-phan-tich-mang-xa-hoi`; lập kế hoạch lợi nhuận + điểm hòa vốn từ đầu khi
mở kinh doanh → `/ts-ke-hoach-loi-nhuan`; định giá sản phẩm → `/ts-dinh-gia-offer`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `phan-tich-doanh-thu` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này — dùng lại số liệu đã có thay vì hỏi lại:
- `05-muc-tieu-quy-tac-lien-he.md` → mục tiêu doanh thu, KPI, ngân sách quảng cáo.
- `03-tai-lieu-tho/` → file xuất đơn hàng, sao kê, báo cáo quảng cáo người dùng đã thả vào (chỉ đọc, không sửa).
- `04-ket-qua/` → kết quả `…-ke-hoach-loi-nhuan-…`, `…-dinh-gia-offer-…` (giá, chi phí biến đổi), `…-bao-cao-facebook-ads-…`
  / `…-len-camp-facebook-…` (chi tiêu quảng cáo), `…-email-cham-soc-…` (tỷ lệ mở/bấm), lần phân tích trước (để so sánh kỳ).

## Quy trình AI thực hiện

### Nguyên tắc phân tích
- Có con số cụ thể, có đơn vị (đ, %, lần) — không nói chung chung.
- Mỗi nhận định phải dẫn tới **việc làm được ngay**.
- Thuật ngữ nào cũng giải thích bằng lời thường ngay lần đầu xuất hiện.
- So với **mục tiêu và kỳ trước của chính doanh nghiệp** trước; số tham khảo ngành chỉ để định hướng, ghi rõ là tham khảo.
- Tách bạch **số thực** và **số ước tính**. Không bịa số — thiếu thì hỏi hoặc ghi `[CẦN BỔ SUNG: …]`.
- Luôn kết thúc bằng **3 việc ưu tiên tuần này**.

### Bước 1 — Thu thập số liệu (hỏi gộp 1 lần, chỉ phần chưa có)
```
Để phân tích chính xác, mình cần:
1. Sản phẩm/dịch vụ chính + giá bán (hoặc giá trị đơn trung bình)?
2. Doanh thu tháng gần nhất (và tháng trước nữa nếu có)?
3. Số đơn / số khách mới trong tháng?
4. Chi phí quảng cáo tháng (theo từng kênh nếu có)?
5. Kênh bán đang dùng (Facebook, TikTok, Shopee, cửa hàng, email…)?
6. Chi phí vận hành hằng tháng (mặt bằng, nhân sự, phần mềm, giá vốn hàng…)?
```
Có file (Excel, CSV, ảnh chụp báo cáo) → đọc file, tóm tắt lại số đã đọc để người dùng xác nhận trước khi tính.
Chưa bán được đơn nào → dùng giả định hợp lý, ghi rõ "**Ước tính — cập nhật khi có số thật**".

### Bước 2 — Chọn loại phân tích
> "Bạn cần: A. Dự báo doanh thu 90 ngày · B. Bảng 10 chỉ số KPI · C. Lãi lỗ quảng cáo theo 4 kịch bản ·
> D. Bảng chi phí vận hành + hòa vốn · E. Tìm nguyên nhân doanh thu giảm"

Công thức, khung trình bày chi tiết từng loại ở `references/cong-thuc-va-khung-phan-tich.md`. Tóm tắt:

**A. Dự báo 90 ngày** — tính ngược từ mục tiêu: số đơn cần = doanh thu mục tiêu ÷ giá; số khách tiềm năng cần =
số đơn ÷ tỷ lệ chốt; ngân sách quảng cáo = số khách tiềm năng × chi phí mỗi khách tiềm năng. Chia 3 tháng
(Khởi động → Tăng tốc → Mở rộng), mỗi tháng có doanh thu, chi phí, lợi nhuận, ROI và lý do số tăng; tổng kết
90 ngày + thời điểm hòa vốn.

**B. Bảng 10 KPI** — chi phí mỗi khách tiềm năng (CPL), tỷ lệ chuyển đổi, ROAS, chi phí có 1 khách mới (CAC),
giá trị vòng đời khách (LTV) và tỷ lệ LTV/CAC, tỷ lệ dùng/học hết (nếu phù hợp), tỷ lệ hoàn tiền/đổi trả, điểm
hài lòng (NPS), tỷ lệ mở email, doanh thu trên mỗi khách tiềm năng. Mỗi chỉ số: công thức · số hiện tại · mục
tiêu · ngưỡng báo động · cách cải thiện.

**C. Lãi lỗ quảng cáo 4 kịch bản** — với ngân sách và giá hiện tại, tính 4 mức ROAS (1,5 · 3 · 5 · 8 lần) **và
tính thêm theo biên lợi nhuận thật** (ROAS hòa vốn = 1 ÷ biên lợi nhuận gộp). Mỗi kịch bản: doanh thu, chi phí,
lời/lỗ, dấu hiệu nhận biết, việc nên làm.

**D. Chi phí vận hành + hòa vốn** — bảng chi phí cố định, chi phí biến đổi (% hoặc đ/đơn), chi phí quảng cáo →
tổng chi phí → số đơn cần để hòa vốn = chi phí cố định ÷ (giá − chi phí biến đổi mỗi đơn).

**E. Tìm nguyên nhân doanh thu giảm** — hỏi lần lượt 5 câu theo phễu (lượt xem → khách tiềm năng → tỷ lệ chốt →
giá trị đơn → mua lại), dừng ở câu "Có" đầu tiên để xác định chỗ hỏng: kênh / trang bán hoặc ưu đãi / quy trình
chốt / giá / giữ chân khách. Rồi đưa 3 giải pháp xếp theo mức tác động.

### Bước 3 — Tính toán chính xác
- Tính bằng công cụ chạy code/bảng tính nếu môi trường có (tránh sai số nhẩm); không có thì tính từng bước, ghi phép tính.
- Kiểm tra số bất thường (vd ROAS cao hơn hẳn mức thường gặp, tỷ lệ chốt > 50%): hỏi lại nhẹ nhàng
  "Số này cao hơn mức thường gặp — bạn kiểm tra lại giúp mình nhé?" — không phán xét.
- Hỏi "có nên tăng ngân sách không": chỉ gợi ý tăng khi lãi ổn định ≥ 2 tuần và ROAS trên mức hòa vốn rõ ràng;
  tăng dần 20–30%/lần, mỗi lần cách vài ngày — không nhân đôi đột ngột. Việc tăng thật trên tài khoản quảng cáo
  phải qua `/ts-len-camp-facebook` hoặc `/ts-bao-cao-facebook-ads` và chờ người dùng "duyệt".

### Bước 4 — Trình bày
Đầu báo cáo:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 [LOẠI PHÂN TÍCH]
Sản phẩm: [Tên] | Giá: [X]đ
Kỳ phân tích: [Tháng / Quý…]
Số liệu: [Thực tế / Ước tính / Kết hợp]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Thân: bảng + giải thích ngắn bằng lời thường. Nếu tiện, đề xuất 1 biểu đồ đơn giản (doanh thu theo tháng, chi phí theo khoản).
Cuối:
```
━━━ 3 VIỆC ƯU TIÊN TUẦN NÀY ━━━
1. [Việc tác động lớn nhất]
2. [Việc thứ hai]
3. [Việc thứ ba]

━━━ LỆNH GỢI Ý TIẾP THEO ━━━
→ Quảng cáo đang yếu: /ts-bao-cao-facebook-ads hoặc /ts-viet-quang-cao
→ Kênh hiệu quả nhất cần thêm nội dung: /ts-lich-noi-dung
→ Tỷ lệ chốt thấp: /ts-trang-ban-hang · /ts-xu-ly-tu-choi · /ts-cham-soc-khach-zalo
→ Giá / biên lợi nhuận có vấn đề: /ts-dinh-gia-offer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Chỉ giữ những dòng gợi ý liên quan tới kết quả phân tích.

### Bước 5 — (Tùy chọn) Bảng theo dõi Google Sheets / Excel
Mô tả cấu trúc bảng (tên cột, công thức từng ô), hướng dẫn từng bước tạo trong Google Sheets/Excel; nếu môi trường
có công cụ tạo bảng tính thì tạo luôn file `.xlsx`/`.csv` (hoặc gợi ý `/ts-bang-tinh-excel` để làm kỹ hơn).

### Bước 6 — Cổng duyệt
Hỏi: "Số liệu và kết luận này đúng với tình hình của bạn chưa?" — sửa đến khi người dùng gõ **"duyệt"**, rồi lưu.

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Mọi con số có đơn vị (đ, %, lần).
- [ ] Phân biệt rõ số thực và số ước tính.
- [ ] Mỗi KPI có mục tiêu / ngưỡng để so sánh; số tham khảo ngành ghi rõ là tham khảo.
- [ ] Thuật ngữ đã giải thích bằng tiếng Việt đơn giản.
- [ ] Phép tính kiểm tra lại được; tổng các khoản khớp nhau.
- [ ] Có 3 việc ưu tiên cụ thể + lệnh `/ts-...` gợi ý.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** số doanh thu, số đơn 1–3 tháng gần nhất; tiền quảng cáo đã chi; các khoản chi cố định hằng tháng.
Có file xuất từ Shopee/phần mềm bán hàng/Trình quản lý quảng cáo thì thả vào `03-tai-lieu-tho/` hoặc đính kèm.
1. Gõ `/ts-phan-tich-doanh-thu` kèm câu hỏi của bạn, vd "tháng này doanh thu giảm 30%, vì sao?".
2. Chọn loại phân tích A–E nếu AI hỏi.
3. Đưa số liệu (gõ, dán bảng, đính kèm file hoặc ảnh chụp màn hình).
4. Kiểm tra bảng tóm tắt số liệu AI đọc được — sai chỗ nào nói ngay.
5. Đọc kết quả và 3 việc ưu tiên; hỏi lại chỗ chưa hiểu ("ROAS là gì?").
6. Gõ **"duyệt"** để AI lưu vào Bộ Não — tháng sau AI sẽ so sánh với lần này.
7. Làm 3 việc ưu tiên, dùng lệnh `/ts-...` AI gợi ý.

## Câu lệnh mẫu
- `/ts-phan-tich-doanh-thu shop giày online: doanh thu tháng 10 là 180 triệu, tháng 11 còn 120 triệu, tìm nguyên nhân`
- `/ts-phan-tich-doanh-thu khóa học Excel giá 1,2 triệu, muốn đạt 100 triệu/tháng, dự báo 90 ngày cần bao nhiêu tiền quảng cáo`
- `/ts-phan-tich-doanh-thu tiệm nail: tính chi phí vận hành và cần bao nhiêu khách/tháng để hòa vốn`
- `/ts-phan-tich-doanh-thu tôi chi 15 triệu quảng cáo, thu 45 triệu, lãi gộp 40% — đang lời hay lỗ, có nên tăng ngân sách?`
- `/ts-phan-tich-doanh-thu dựng giúp tôi bảng KPI hằng tuần trên Google Sheets cho dịch vụ vệ sinh máy lạnh`

## Kết quả nhận được
- Báo cáo đúng loại phân tích đã chọn, có bảng và giải thích bằng lời thường.
- Đánh dấu rõ số thực / ước tính, chỉ số nào đạt, chỉ số nào báo động.
- 3 việc ưu tiên tuần này + lệnh `/ts-...` gợi ý tiếp theo.
- (Tùy chọn) cấu trúc hoặc file bảng theo dõi Google Sheets / Excel.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-phan-tich-doanh-thu-<chu-de-khong-dau>/`.
2. Lưu báo cáo phân tích đã duyệt (loại phân tích, kỳ, bảng số liệu đầu vào đã xác nhận, kết quả, 3 việc ưu tiên) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-phan-tich-doanh-thu
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `so-lieu.csv` (số liệu đầu vào đã chuẩn hóa), `bang-kpi.xlsx` hoặc `bang-kpi.csv`, biểu đồ `.png`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-phan-tich-doanh-thu · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu đã chốt mục tiêu doanh thu, KPI hoặc ngưỡng báo động mới khác `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`, đề xuất cập nhật và hỏi trước khi ghi đè. Không chép file gốc trong `03-tai-lieu-tho/` sang chỗ khác — chỉ dẫn đường dẫn.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Phân tích chỉ **đọc số liệu** — không tự đổi ngân sách, tắt quảng cáo hay sửa giá. Mọi thay đổi tốn tiền chờ "duyệt" ở lệnh tương ứng.
- Không hứa hẹn doanh thu; dự báo luôn ghi rõ giả định và mức chắc chắn.
- Không lưu số tài khoản ngân hàng, số thẻ, mật khẩu phần mềm bán hàng vào Bộ Não.
- Số liệu ít (dưới 2 tuần, dưới vài chục đơn) → nói rõ "chưa đủ để kết luận chắc", ưu tiên thu thêm dữ liệu.

## Skill liên quan
- Trước: `/ts-ke-hoach-loi-nhuan` · `/ts-dinh-gia-offer` · `/ts-bao-cao-facebook-ads` · `/ts-doc-so-lieu-hinh-anh`
- Sau: `/ts-bang-tinh-excel` · `/ts-len-camp-facebook` · `/ts-lich-noi-dung` · `/ts-trang-ban-hang` · `/ts-chien-luoc-tang-truong`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
