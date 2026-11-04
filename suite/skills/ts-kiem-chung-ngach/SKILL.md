---
name: ts-kiem-chung-ngach
description: "Gọi bằng /ts-kiem-chung-ngach. Kiểm chứng một ngách hoặc ý tưởng kinh doanh tại Việt Nam bằng dữ liệu thật tra cứu web, chấm Điểm ngách 100 điểm theo 7 tiêu chí, kết luận NÊN LÀM, LÀM CÓ ĐIỀU KIỆN hay KHÔNG NÊN, ước tính quy mô thị trường và đề xuất 1 phép thử nhỏ xem khách có trả tiền không. Dùng trước khi bỏ vốn, khi phân vân giữa nhiều ý tưởng. Từ khóa: kiểm chứng ngách, chọn ngách, ý tưởng có nên làm không, thị trường có lớn không, có ai làm chưa, đo nhu cầu, khách có chịu trả tiền không."
---

# /ts-kiem-chung-ngach — Kiểm chứng ngách bằng dữ liệu thật

> Trước khi bỏ tiền và công sức, skill này tra cứu dữ liệu thật trên mạng Việt Nam, chấm **Điểm ngách 100 điểm**, cho bạn kết luận rõ ràng (NÊN LÀM / LÀM CÓ ĐIỀU KIỆN / KHÔNG NÊN) và **một phép thử rẻ** để biết khách có thật sự trả tiền không.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Có ý tưởng kinh doanh mới, muốn biết có đáng làm không trước khi bỏ vốn.
- Phân vân giữa 2–3 ngách, cần so sánh bằng điểm số.
- Muốn mở thêm sản phẩm/khóa học mới cho tệp khách hiện có.
- Đang bán mà ế, nghi ngờ chọn sai ngách.
- Cần số liệu thị trường để thuyết phục đối tác/người góp vốn.

**Không dùng khi:** đã chắc chắn ngách, chỉ cần hiểu sâu khách hàng → dùng `/ts-chan-dung-khach-hang`. Cần soi kỹ 1–3 đối thủ cụ thể → dùng `/ts-phan-tich-doi-thu`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `kiem-chung-ngach` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Làm rõ ý tưởng (hỏi tối đa 4 câu, có gợi ý A-B-C-D)
1. Bạn định bán gì? (A. hàng hóa · B. dịch vụ làm cho khách · C. khóa học/tài liệu số · D. phần mềm/công cụ)
2. Bán cho ai — càng hẹp càng tốt? (vd "chủ shop thời trang tự quay video" tốt hơn "người kinh doanh")
3. Giá dự kiến? (A. dưới 300 nghìn · B. 300 nghìn – 1 triệu · C. 1–5 triệu · D. trên 5 triệu)
4. Bạn có lợi thế gì? (A. kinh nghiệm/chuyên môn · B. nguồn hàng · C. tệp khách/người theo dõi sẵn · D. chưa có gì)

Nếu ý tưởng quá rộng, đề xuất 2–3 cách thu hẹp và để người dùng chọn. Có nhiều ý tưởng → chạy từng cái, cuối cùng so sánh bảng điểm.

### Bước 2 — Lập kế hoạch tra cứu
Viết ra **ít nhất 6 truy vấn** (tiếng Việt, đúng cách khách hay gõ), phủ ít nhất 4 nhóm nguồn theo `references/nguon-du-lieu-vn.md`: Google · Google Trends · sàn TMĐT (Shopee/Lazada/Tiki/TikTok Shop) hoặc nền tảng khóa học (Unica/Gitiho) · nhóm Facebook/Threads/Zalo · TikTok/YouTube · đối thủ và quảng cáo của họ.

### Bước 3 — Tra cứu dữ liệu thật (BẮT BUỘC)
- Dùng công cụ tìm kiếm/đọc web đang có. **Tối thiểu 6 lượt tìm kiếm.** Ghi nhật ký: truy vấn → nền tảng → kết quả chính → link → ngày kiểm tra.
- Mỗi nhận định quan trọng cần **≥ 3 nguồn độc lập** (khác nền tảng hoặc khác người đăng).
- Ghi số cụ thể (giá, đã bán, số thành viên, view) — không ghi "nhiều", "khá đông".
- Trang không truy cập được → ghi "không truy cập được", **không tự điền số**.
- **Nếu môi trường không có công cụ tìm kiếm web:** nói rõ, đưa 6 truy vấn + nơi tìm để học viên tự tra và dán ảnh/link vào. Chưa có dữ liệu thì mọi điểm ghi "tạm tính", kết luận tối đa là LÀM CÓ ĐIỀU KIỆN.

### Bước 4 — Chấm Điểm ngách (7 tiêu chí, tổng trọng số 100)

| # | Tiêu chí | Trọng số | Điểm 10 nghĩa là | Điểm 0–3 nghĩa là |
|---|---|---:|---|---|
| 1 | Mức độ đau / cấp thiết | 20 | Khách khổ thật, cần giải gấp, đã chi tiền cho cách khác | "Có thì tốt", không ai than |
| 2 | Khả năng & sẵn lòng chi trả | 20 | Đã có người bán ở mức giá bạn muốn, bán được nhiều | Khách quen dùng miễn phí, chê đắt |
| 3 | Nhu cầu tìm kiếm | 15 | Nhiều người chủ động tìm, có số liệu | Hầu như không ai tìm |
| 4 | Xu hướng | 10 | Tăng đều 12–24 tháng | Đang giảm, hoặc trào lưu vài tuần |
| 5 | Mức cạnh tranh (có chỗ trống) | 10 | Có người bán nhưng còn góc chưa ai làm tốt | Quá đông và người dẫn đầu quá mạnh, hoặc không ai bán (có thể không có cầu) |
| 6 | Kênh tiếp cận khách | 15 | Biết rõ khách ở đâu, tiếp cận rẻ | Không biết tìm khách ở đâu |
| 7 | Độ phù hợp với người làm | 10 | Có chuyên môn, uy tín, nguồn lực | Hoàn toàn mới, không có lợi thế |

**Cách tính:** điểm quy đổi = điểm × trọng số ÷ 10 → cộng lại.
**Kết luận:** ≥ 70 **NÊN LÀM** · 50–69 **LÀM CÓ ĐIỀU KIỆN** · < 50 **KHÔNG NÊN**.
**Luật chặn:** tiêu chí 1 hoặc 2 ≤ 3 điểm, hoặc chưa đủ 3 nguồn → không được kết luận NÊN LÀM.

Ghi dữ liệu theo mẫu `scripts/vi-du-ngach.json` rồi chạy `scripts/diem_ngach.py` (cách chạy bên dưới). Không chạy được thì AI tự tính, trình bảng cùng định dạng. Người dùng có thể đổi trọng số (trường `trong_so`), tổng vẫn phải bằng 100.

### Bước 5 — Ước tính quy mô thị trường (3 tầng, đơn giản)
1. **Tổng thị trường** = số khách có vấn đề này × số tiền mỗi người chi mỗi năm.
2. **Phần với tới được** = phần khách bạn phục vụ được (khu vực, kênh, ngôn ngữ, mức giá).
3. **Phần chiếm được năm đầu** = phần thực tế bán được năm đầu (người mới thường 0,5–3%).

Ghi rõ con số nào có nguồn, con số nào là ước lượng. Đây là để biết "đủ lớn để nuôi mình không", không phải dự báo chính xác.

### Bước 6 — Thiết kế 1 phép thử trả tiền
Chọn 1 phép thử trong `references/mau-bao-cao.md` (đặt cọc, trang đặt trước, bán thử nhỏ, tư vấn có phí, lớp thử). Ghi: cách làm, chi phí tối đa, thời gian 7–14 ngày, **ngưỡng đạt bằng con số**, đạt thì làm gì, không đạt thì làm gì. Nhắc: lượt thích và lời khen không phải bằng chứng — chỉ tiền mới là bằng chứng.

### Bước 7 — Trình báo cáo và chờ duyệt
Viết báo cáo theo `references/mau-bao-cao.md`: tóm tắt 30 giây → bảng điểm → bằng chứng từng tiêu chí → quy mô thị trường → phép thử → rủi ro → bước tiếp theo → nhật ký tra cứu. Hỏi: "Bạn muốn sửa gì? Gõ **duyệt** để lưu."

### Checklist chất lượng
- [ ] ≥ 6 lượt tìm kiếm, phủ ≥ 4 nhóm nguồn, có nhật ký tra cứu.
- [ ] Mỗi nhận định quan trọng ≥ 3 nguồn độc lập, có link + ngày kiểm tra.
- [ ] Không có con số nào không rõ nguồn (hoặc đã ghi "ước lượng").
- [ ] Bảng điểm đúng trọng số, tổng 100, áp dụng luật chặn.
- [ ] Có quy mô thị trường 3 tầng với giả định rõ ràng.
- [ ] Phép thử có ngưỡng đạt bằng con số và chi phí tối đa.

### Chạy script
- macOS: `python3 scripts/diem_ngach.py scripts/vi-du-ngach.json --out diem-ngach.md`
- Windows: `py scripts\diem_ngach.py scripts\vi-du-ngach.json --out diem-ngach.md`

Chỉ cần Python 3. Script tự cảnh báo: tiêu chí thiếu nguồn, nguồn quá 180 ngày, nguồn chưa ghi ngày, tỉ lệ chiếm thị trường quá lạc quan. Thêm `--ngay YYYY-MM-DD` để đặt ngày kiểm tra.

### Ví dụ minh họa (doanh nghiệp giả định)
*Ví dụ: khóa học online "Quay video bán hàng bằng điện thoại" cho chủ shop thời trang nhỏ.* Các link trong `scripts/vi-du-ngach.json` là link minh họa (example.com), chỉ để xem định dạng.
- Điểm: đau 8 · chi trả 7 · tìm kiếm 7 · xu hướng 8 · cạnh tranh 5 · kênh 8 · phù hợp 9 → **74,5/100**.
- Nhưng tiêu chí "Nhu cầu tìm kiếm" mới có 2 nguồn → script cảnh báo cần thêm nguồn.
- Quy mô (giả định): 300.000 chủ shop × 1,5 triệu/năm = 450 tỷ → với tới 20% = 90 tỷ → chiếm 1% năm đầu ≈ **900 triệu đ** (600 học viên).
- Phép thử: đăng bài vào 3 nhóm chủ shop, mở 20 suất lớp thử 199 nghìn, nhận cọc trong 10 ngày. Ngưỡng đạt: ≥ 10 người trả tiền.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** viết 1–2 câu mô tả ý tưởng (bán gì, cho ai, giá khoảng bao nhiêu); nếu biết tên 2–3 đối thủ hoặc nhóm Facebook khách hay vào thì ghi sẵn.
1. Gõ `/ts-kiem-chung-ngach` kèm câu mô tả ý tưởng.
2. Trả lời 4 câu hỏi (gõ chữ cái A-B-C-D). Nếu AI gợi ý thu hẹp ngách, chọn 1 hướng.
3. Chờ AI tra cứu (vài phút). Nếu AI báo không tìm web được, làm theo danh sách 6 truy vấn AI đưa, chụp màn hình kết quả và dán vào.
4. Đọc phần "Tóm tắt 30 giây" trước. Thấy con số nào lạ, hỏi lại: "nguồn của số này ở đâu?".
5. Nếu có thông tin AI không biết (vd bạn đã có 2.000 người theo dõi), nói để AI chấm lại.
6. Gõ **duyệt** để lưu báo cáo vào Bộ Não.
7. Làm phép thử trả tiền trong 7–14 ngày, quay lại gõ `/ts-kiem-chung-ngach kết quả phép thử: …` để AI cập nhật kết luận.

## Câu lệnh mẫu
- `/ts-kiem-chung-ngach Tôi muốn bán đồ ăn healthy giao tận văn phòng ở quận 1, giá 60–80 nghìn/phần.`
- `/ts-kiem-chung-ngach Dịch vụ dọn nhà theo giờ cho gia đình trẻ ở Hà Nội — có đáng làm không?`
- `/ts-kiem-chung-ngach Khóa học online dạy dùng AI viết bài bán hàng cho chủ shop, giá 990 nghìn.`
- `/ts-kiem-chung-ngach So sánh giúp 3 ý tưởng: nến thơm handmade, trà thảo mộc, xà phòng thiên nhiên.`

## Kết quả nhận được
- Báo cáo kiểm chứng đầy đủ, mở đầu bằng tóm tắt 30 giây và kết luận rõ ràng.
- Bảng Điểm ngách 7 tiêu chí có trọng số, số nguồn, bằng chứng.
- Bằng chứng từng tiêu chí, mỗi nhận định có link + ngày kiểm tra.
- Ước tính quy mô thị trường 3 tầng kèm giả định.
- 1 phép thử trả tiền có ngưỡng đạt cụ thể.
- Nhật ký tra cứu (để kiểm tra lại hoặc cập nhật sau).

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-kiem-chung-ngach-<chu-de-khong-dau>/`.
2. Lưu báo cáo kiểm chứng đầy đủ (theo mẫu `references/mau-bao-cao.md`) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-kiem-chung-ngach
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `diem-ngach.json` (dữ liệu chấm điểm), `diem-ngach.md` (kết quả script), `nhat-ky-tra-cuu.md` (danh sách truy vấn và link).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-kiem-chung-ngach · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Thông tin đối thủ (tên, giá, link) lưu thêm vào `02-kien-thuc/doi-thu/` để skill khác dùng lại. Nếu kết luận là NÊN LÀM và người dùng quyết định làm, đề xuất cập nhật `01-ho-so/01-ho-so-doanh-nghiep.md` (ngách, khách chính) và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Không bịa số liệu, link, đánh giá.** Không tìm được thì ghi `[CẦN BỔ SUNG: …]` hoặc "ước lượng".
- Số "đã bán" trên sàn và số học viên trên nền tảng có thể bị làm đẹp — dùng để so sánh, không coi là doanh thu chính xác.
- Kết luận chỉ là công cụ hỗ trợ. Phép thử trả tiền mới là câu trả lời cuối cùng.
- Phép thử có nhận tiền: phải minh bạch (đợt đầu, ngày giao, cách hoàn tiền). Không chạy quảng cáo hay nhận cọc khi người dùng chưa duyệt.
- Không vào nhóm kín bằng cách giả danh; không thu thập thông tin cá nhân của thành viên nhóm.
- Ngành có điều kiện (thực phẩm chức năng, mỹ phẩm, giáo dục cấp chứng chỉ, tài chính, y tế): nhắc kiểm tra giấy phép/quy định trước khi bán.

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` · `/ts-nghien-cuu-youtube` (lấy số liệu YouTube)
- Sau: `/ts-chan-dung-khach-hang` · `/ts-phan-tich-doi-thu` · `/ts-mo-hinh-kinh-doanh` · `/ts-ke-hoach-loi-nhuan`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
