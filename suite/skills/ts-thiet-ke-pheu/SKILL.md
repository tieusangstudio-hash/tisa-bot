---
name: ts-thiet-ke-pheu
description: "Gọi bằng /ts-thiet-ke-pheu. Thiết kế phễu bậc thang 4 tầng: quà miễn phí → sản phẩm mồi giá thấp → sản phẩm chính → sản phẩm cao cấp, kèm giá, mục tiêu, kênh, tỉ lệ chuyển đổi giả định, bảng tính LTV trên 100 người để lại thông tin và lịch chăm sóc giữa các tầng. Dùng khi muốn xây hệ thống bán hàng, sắp xếp dòng sản phẩm, biết 1 khách đáng giá bao nhiêu. Từ khóa: phễu bán hàng, bậc thang sản phẩm, value ladder, LTV, sản phẩm mồi, upsell, dòng sản phẩm, chi phí mỗi lead."
---

# /ts-thiet-ke-pheu — Thiết kế phễu bậc thang 4 tầng & tính LTV

> Biến các sản phẩm rời rạc thành một bậc thang: khách nhận quà miễn phí → mua thử giá thấp → mua sản phẩm
> chính → lên gói cao cấp. Kết quả là bản thiết kế 4 tầng, bảng tính "100 người để lại thông tin sẽ mang về
> bao nhiêu tiền" và lịch chăm sóc để đưa khách lên từng bậc.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Có sản phẩm nhưng bán lẻ tẻ, chưa có lộ trình đưa khách từ "biết đến" tới "mua nhiều lần".
- Muốn biết 1 người để lại số điện thoại đáng giá bao nhiêu tiền → được phép chi tối đa bao nhiêu cho quảng cáo.
- Chuẩn bị ra sản phẩm mới và muốn xếp nó vào đúng vị trí trong dòng sản phẩm.
- Muốn có sản phẩm giá thấp để "mở hàng" khách mới, hoặc gói cao cấp để tăng doanh thu trên mỗi khách.
- Cần đối chiếu mục tiêu doanh thu tháng với số người cần thu thập thông tin.

**Không dùng khi:** chỉ cần làm chi tiết món quà miễn phí → `/ts-pheu-qua-tang`; chỉ cần định giá và đóng gói
1 sản phẩm → `/ts-dinh-gia-offer`; cần bài toán chi phí cố định, điểm hòa vốn → `/ts-ke-hoach-loi-nhuan`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `thiet-ke-pheu`, `dinh-gia-offer`, `pheu-qua-tang`, `ke-hoach-loi-nhuan` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Làm rõ đề bài (hỏi gộp 1 lần, tối đa 6 câu)
Chỉ hỏi phần Bộ Não chưa có. Mỗi câu kèm gợi ý để người dùng chọn nhanh.
1. Bạn đang bán những gì, giá bao nhiêu? (liệt kê hết, kể cả dịch vụ làm thêm)
2. Khách hàng chính là ai, họ đang gặp vấn đề gì lớn nhất?
3. Kênh đang có: A. Fanpage · B. TikTok · C. Zalo cá nhân/nhóm · D. Danh sách email · E. Chưa có kênh nào.
4. Mục tiêu doanh thu mỗi tháng? (vd 30 triệu, 100 triệu)
5. Sau khi trừ giá vốn, bạn còn khoảng bao nhiêu % trên mỗi đồng bán ra? (biên lợi nhuận gộp — không biết thì
   AI tạm dùng 50% cho hàng hóa, 70% cho khóa học/dịch vụ số và ghi rõ là giả định)
6. Mỗi tháng bạn phục vụ tối đa được bao nhiêu khách gói cao cấp? (giới hạn thời gian, nhân sự)

### Bước 2 — Vẽ "chuỗi vấn đề" của khách
Phễu tốt là một chuỗi: **giải xong vấn đề này thì khách tự thấy vấn đề tiếp theo**. AI viết 4 dòng:

| Tầng | Câu hỏi để tìm sản phẩm |
|---|---|
| 1 | Vấn đề nhỏ, gấp nào khách muốn giải ngay mà không tốn tiền? → quà miễn phí giải đúng vấn đề đó. |
| 2 | Dùng quà xong, khách nhận ra mình còn thiếu gì để làm được thật? → sản phẩm mồi. |
| 3 | Làm được bước đầu rồi, khách muốn kết quả trọn vẹn, ổn định → sản phẩm chính. |
| 4 | Đã có kết quả, khách muốn nhanh hơn / nhiều hơn / có người làm giúp → sản phẩm cao cấp. |

Nếu sản phẩm hiện có không khớp chuỗi, đề xuất **sửa hoặc thêm** sản phẩm, không ép sản phẩm cũ vào tầng sai.

### Bước 3 — Thiết kế 4 tầng
Với mỗi tầng ghi đủ 6 cột: **tên · giá · mục tiêu · kênh · tỉ lệ chuyển đổi giả định · tính trên đâu**.

| Tầng | Vai trò | Quy tắc |
|---|---|---|
| 1. Quà miễn phí | Đổi lấy tên + số điện thoại/Zalo/email | BẮT BUỘC là sản phẩm thông tin: ebook, video, checklist, mini course qua Zalo. Dùng được trong ≤ 30 phút, cho 1 "chiến thắng nhỏ". |
| 2. Sản phẩm mồi | Biến người lạ thành người đã trả tiền | Giá thấp, dễ quyết (gợi ý 1–10% giá sản phẩm chính). Mục tiêu là số người mua, không phải lợi nhuận. |
| 3. Sản phẩm chính | Dòng tiền chính của doanh nghiệp | Giải trọn vấn đề chính. Có lãi rõ ràng sau chi phí quảng cáo. |
| 4. Sản phẩm cao cấp | Tăng doanh thu trên mỗi khách | Nhanh hơn, riêng hơn, có người làm cùng/làm giúp. Giới hạn số suất theo năng lực thật. |

**Tỉ lệ khởi điểm thận trọng** (giả định để lập kế hoạch, không phải số liệu ngành — phải đo lại):
- Tầng 2: 3–10% tổng số lead mua.
- Tầng 3: 10–25% người đã mua tầng 2 (có thể thêm 1–3% lead mua thẳng tầng 3).
- Tầng 4: 5–15% người đã mua tầng 3.

Trình bày bảng 4 tầng + sơ đồ chữ, ví dụ: `Ebook (0đ) → Lớp video (99k) → Khóa chính (1,99tr) → Kèm 1-1 (12tr)`.

**CỔNG DUYỆT 1:** "Bậc thang này đã đúng sản phẩm, đúng giá chưa? Gõ *duyệt* để tính tiền, hoặc nói chỗ cần sửa."

### Bước 4 — Tính giá trị phễu trên 100 người để lại thông tin
Ưu tiên chạy script (tính chính xác, không cần cài thêm gì):
- Tạo file mô tả phễu theo mẫu `templates/pheu-mau.json` (sửa tên, giá, tỉ lệ).
- macOS: `python3 scripts/tinh_ltv.py pheu.json --ba-kich-ban --md ket-qua-ltv.md --csv bang-ltv.csv`
- Windows: `py scripts\tinh_ltv.py pheu.json --ba-kich-ban --md ket-qua-ltv.md --csv bang-ltv.csv`
- Nhập nhanh không cần file: `python3 scripts/tinh_ltv.py --nhanh "Ebook|0|100" "Lớp mini|99000|10" "Khóa chính|1990000|20" "Kèm 1-1|12000000|10" --bien 60`

Không chạy được lệnh thì tính tay theo đúng công thức, ghi rõ từng phép tính:
- Số người mua tầng = số người ở tầng gốc × tỉ lệ.
- Doanh thu tầng = số người mua × giá × số lần mua.
- **Doanh thu mỗi lead** = tổng doanh thu ÷ 100.
- **LTV** (giá trị vòng đời 1 khách trả tiền) = tổng doanh thu ÷ số người mua tầng trả phí đầu tiên.
- **Chi phí tối đa cho 1 lead** = doanh thu mỗi lead × biên lợi nhuận gộp × 50% (giữ lại nửa còn lại làm lãi và dự phòng).
- **Số lead cần mỗi tháng** = mục tiêu doanh thu ÷ doanh thu mỗi lead.

Luôn trình bày 3 kịch bản (thận trọng ×0,5 · kỳ vọng · tốt ×1,5) và khuyên **lập ngân sách theo kịch bản thận trọng**.

### Bước 5 — Kiểm tra logic (checklist bắt buộc)
- [ ] Tầng 1 miễn phí và là sản phẩm thông tin, giải đúng 1 vấn đề nhỏ của đúng khách tầng 3.
- [ ] Mỗi tầng sau giải tiếp vấn đề mà tầng trước để lộ ra (đọc lại bảng chuỗi vấn đề).
- [ ] Giá tăng dần; không có bước nhảy quá lớn (gấp hơn ~30 lần) mà thiếu gói trung gian hoặc trả góp.
- [ ] Tỉ lệ nằm trong vùng thận trọng; tỉ lệ nào cao hơn phải có lý do (vd đã có số liệu thật).
- [ ] Chi phí tối đa cho 1 lead ≥ chi phí quảng cáo hiện tại cho 1 lead (nếu biết). Nếu thấp hơn → phễu lỗ,
      phải tăng giá trị tầng 3–4 hoặc tăng tỉ lệ chuyển đổi trước khi chạy quảng cáo.
- [ ] Số suất tầng 4 mỗi tháng không vượt năng lực phục vụ ở câu hỏi 6.
- [ ] Số lead cần mỗi tháng khả thi với kênh hiện có.
Mục nào chưa đạt → nêu rõ và đề xuất 1–2 cách sửa cụ thể.

### Bước 6 — Lịch chăm sóc giữa các tầng
Thiết kế điểm chạm qua **Zalo, email, inbox Fanpage** để đưa khách lên bậc kế tiếp. Dùng khung và mẫu tin
trong `references/diem-cham-cham-soc.md`. Tối thiểu:
- Ngay khi để lại thông tin: gửi quà + 1 câu hỏi để khách trả lời (mở cuộc trò chuyện).
- Ngày 1–3: 1 mẹo dùng quà + 1 câu chuyện kết quả (chỉ dùng câu chuyện thật, thiếu thì ghi `[CẦN BỔ SUNG]`).
- Ngày 3–5: mời tầng 2 với hạn chót thật.
- Sau khi mua tầng 2: hướng dẫn dùng → hỏi kết quả → mời tầng 3 khi khách vừa có kết quả đầu tiên.
- Sau tầng 3: chăm sóc hoàn thành → xin cảm nhận → mời tầng 4 cho người phù hợp (không mời đại trà).
Ghi rõ: ai gửi, gửi qua kênh nào, gửi tay hay tự động. Không nhắn quá 1 tin/ngày cho một người.

### Bước 7 — Tổng hợp & duyệt cuối
Xuất 1 bản tổng hợp gồm: sơ đồ phễu · bảng 4 tầng · bảng giá trị trên 100 lead + 3 kịch bản · kết quả
checklist · lịch chăm sóc · 3 việc làm ngay trong 7 ngày tới.

**CỔNG DUYỆT 2:** "Gõ *duyệt* để lưu vào Bộ Não, hoặc nói phần cần chỉnh."

## Ví dụ minh họa (doanh nghiệp giả định — chỉ để tham khảo)
**Tiệm bánh Mây** dạy làm bánh online, biên lợi nhuận gộp giả định 60%, mục tiêu 50 triệu/tháng.

| Tầng | Tên | Giá | Mục tiêu | Kênh | Tỉ lệ giả định |
|---|---|---:|---|---|---|
| 1 | Ebook "7 công thức bánh không cần lò" | 0đ | Lấy số Zalo | Quảng cáo Facebook → trang nhận quà | 100% lead |
| 2 | Lớp video bông lan cơ bản | 99.000đ | Có người trả tiền đầu tiên | Zalo + email ngày 3–5 | 10% lead |
| 3 | Khóa làm bánh bán online | 1.990.000đ | Dòng tiền chính | Zalo 1-1, buổi live | 20% người mua tầng 2 |
| 4 | Kèm 1-1 mở tiệm bánh tại nhà | 12.000.000đ | Tăng doanh thu mỗi khách | Gọi điện tư vấn | 10% người mua tầng 3 |

Kết quả chạy script (kịch bản kỳ vọng): 100 lead → **7.370.000đ**; mỗi lead **73.700đ**; LTV **737.000đ**;
được chi tối đa **22.110đ** cho 1 lead; cần khoảng **678 lead/tháng** để đạt 50 triệu. Kịch bản thận trọng chỉ
còn 17.900đ/lead → nếu quảng cáo đang tốn 30.000đ/lead thì phải tăng tỉ lệ tầng 3 trước khi tăng ngân sách.

## Hướng dẫn cho học viên (làm theo từng bước)
1. **Chuẩn bị trước** (5 phút): danh sách sản phẩm đang bán + giá; ước lượng mỗi đơn còn lãi bao nhiêu %;
   mục tiêu doanh thu tháng; nếu đã chạy quảng cáo thì ghi chi phí cho 1 người để lại thông tin.
2. Gõ `/ts-thiet-ke-pheu` kèm 1 câu mô tả bạn bán gì cho ai.
3. Trả lời các câu hỏi AI đưa ra (chọn chữ cái A-B-C-D nếu có). Không biết thì nói "chưa biết", AI sẽ dùng giả định và ghi rõ.
4. Xem bậc thang 4 tầng. Sửa bằng lời: "đổi tầng 2 thành combo 199k", "tầng 4 tôi chỉ nhận 3 người/tháng".
   Gõ **duyệt**.
5. Xem bảng tính 100 lead. Chú ý dòng **Chi phí tối đa cho 1 lead** — đó là mức trần khi chạy quảng cáo.
6. Đọc phần kiểm tra logic. Mục nào ghi `[CẦN XEM LẠI]` thì hỏi AI "sửa giúp tôi mục này".
7. Xem lịch chăm sóc, chép các mẫu tin vào Zalo/email của bạn. Gõ **duyệt** để lưu.
8. Sau 2–4 tuần chạy thật, gõ `/ts-thiet-ke-pheu cập nhật tỉ lệ thật: ...` để tính lại bằng số thật.

## Câu lệnh mẫu
- `/ts-thiet-ke-pheu tôi bán mỹ phẩm handmade online, sản phẩm chính là bộ dưỡng da 650k, muốn xây phễu`
- `/ts-thiet-ke-pheu spa Hồng có gói triệt lông 3 triệu và liệu trình da 8 triệu, làm phễu giúp tôi`
- `/ts-thiet-ke-pheu khóa học quay video bằng điện thoại 2,5 triệu, mục tiêu 80 triệu/tháng, tính cần bao nhiêu lead`
- `/ts-thiet-ke-pheu kiểm tra phễu này có lỗ không: ebook 0đ, mini 49k, khóa 1,5tr, coaching 15tr, quảng cáo đang 25k/lead`
- `/ts-thiet-ke-pheu cập nhật tỉ lệ thật: 8% mua lớp mini, 15% lên khóa chính`

## Kết quả nhận được
- Sơ đồ phễu 4 tầng + bảng tên, giá, mục tiêu, kênh, tỉ lệ cho từng tầng.
- Bảng tính giá trị trên 100 lead, LTV, chi phí tối đa cho 1 lead, số lead cần mỗi tháng, 3 kịch bản.
- Kết quả kiểm tra logic kèm cách sửa.
- Lịch chăm sóc giữa các tầng với mẫu tin Zalo/email/inbox.
- File `bang-ltv.csv` mở được bằng Excel/Google Sheets (nếu chạy được script).

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-thiet-ke-pheu-<chu-de-khong-dau>/`.
2. Lưu bản thiết kế phễu (sơ đồ, bảng 4 tầng, bảng LTV, kiểm tra logic, lịch chăm sóc) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-thiet-ke-pheu
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `pheu.json` (dữ liệu đầu vào để tính lại), `bang-ltv.csv`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-thiet-ke-pheu · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu bậc thang sản phẩm đã chốt khác với `01-ho-so/02-san-pham-dich-vu.md` (sản phẩm mới, giá mới, vị trí tầng), đề xuất cập nhật và hỏi trước khi ghi đè. Tỉ lệ chuyển đổi THẬT (khi người dùng cập nhật) lưu thêm vào `02-kien-thuc/cong-thuc/ti-le-pheu.md` để các lần sau dùng.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Mọi tỉ lệ chuyển đổi là **giả định** cho tới khi có số thật. Luôn ghi chữ "giả định" cạnh con số.
- Không bịa câu chuyện khách hàng, số học viên, kết quả trong mẫu tin chăm sóc — thiếu thì ghi `[CẦN BỔ SUNG: …]`.
- Khan hiếm, hạn chót trong tin nhắn phải thật (số suất thật, ngày đóng thật).
- Gửi tin hàng loạt qua Zalo/email/Messenger: chỉ gửi cho người đã đồng ý nhận, có cách hủy nhận; tuân thủ
  quy định của từng nền tảng (Messenger hạn chế tin quảng cáo ngoài 24 giờ). AI chỉ soạn bản nháp, không tự gửi.
- Tầng 4 hứa "kèm riêng" thì số suất phải vừa năng lực thật, tránh nhận quá rồi phục vụ kém.

## Skill liên quan
- Trước: `/ts-chan-dung-khach-hang` (hiểu khách) · `/ts-dinh-gia-offer` (định giá, đóng gói từng tầng) ·
  `/ts-ke-hoach-loi-nhuan` (chi phí cố định, điểm hòa vốn)
- Sau: `/ts-pheu-qua-tang` (làm chi tiết quà miễn phí tầng 1) · `/ts-trang-ban-hang` (trang bán tầng 2–3) ·
  `/ts-email-cham-soc` · `/ts-cham-soc-khach-zalo` (dựng chuỗi chăm sóc) · `/ts-xu-ly-tu-choi` (chốt tầng 3–4)

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
