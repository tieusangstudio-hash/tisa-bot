---
name: ts-mo-hinh-kinh-doanh
description: "Gọi bằng /ts-mo-hinh-kinh-doanh. Phỏng vấn từng bước và dựng mô hình kinh doanh 9 ô (Business Model Canvas), kiểm tra 9 ô có ăn khớp không, chấm điểm từng ô, chỉ ra 1–3 giả định rủi ro nhất và cách kiểm chứng rẻ trước khi bỏ tiền. Xuất bảng, sơ đồ và file .canvas mở bằng Obsidian. Dùng khi bắt đầu kinh doanh, mở hướng mới hoặc muốn rà lại mô hình. Từ khóa: mô hình kinh doanh, business model canvas, BMC, 9 ô, kế hoạch kinh doanh, ý tưởng có hợp lý không, khởi nghiệp."
---

# /ts-mo-hinh-kinh-doanh — Dựng mô hình kinh doanh 9 ô

> AI phỏng vấn bạn qua **9 ô của Business Model Canvas** (khung công khai của Alexander Osterwalder), rồi trả về **bản mô hình 1 trang**, sơ đồ trực quan, **điểm từng ô**, các chỗ **lệch nhau** và **1–3 giả định rủi ro nhất** kèm cách kiểm chứng rẻ trước khi bỏ vốn.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Sắp bắt đầu kinh doanh, muốn nhìn toàn bộ mô hình trên 1 trang.
- Mở thêm sản phẩm, chi nhánh, kênh bán mới — cần xem có khớp với cái đang có không.
- Đang bán nhưng lời ít/lỗ, muốn tìm ô nào đang yếu.
- Cần trình bày mô hình cho người góp vốn, đối tác, nhân sự mới.
- Dạy/hướng dẫn người khác suy nghĩ có hệ thống về việc kinh doanh.

**Không dùng khi:** chưa có ý tưởng hoặc chưa biết ngách có cầu không → dùng `/ts-kiem-chung-ngach` trước. Cần tính chi tiết số đơn hòa vốn → dùng `/ts-ke-hoach-loi-nhuan`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `mo-hinh-kinh-doanh` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Chốt phạm vi
Hỏi 1 câu: canvas này cho **(A) toàn bộ doanh nghiệp · (B) 1 sản phẩm/dịch vụ · (C) 1 ý tưởng mới chưa làm · (D) 1 chi nhánh/kênh mới**? Và chế độ: **nhanh** (mỗi ô 1–2 câu, ~15 phút) hay **kỹ** (mỗi ô 2–3 câu, ~40 phút).
- Nếu Bộ Não có kết quả của `/ts-chan-dung-khach-hang`, `/ts-kiem-chung-ngach`, `/ts-dinh-gia-offer`, `/ts-ke-hoach-loi-nhuan` trong `04-ket-qua/` → dùng để điền sẵn ô tương ứng, chỉ hỏi xác nhận.

### Bước 2 — Phỏng vấn 9 ô theo đúng thứ tự
Dùng câu hỏi trong `references/cau-hoi-9-o.md`. Thứ tự **bắt buộc**:

| # | Ô | Câu hỏi cốt lõi |
|---:|---|---|
| 1 | Phân khúc khách hàng | Bán cho ai? Họ đang gặp chuyện gì? |
| 2 | Giá trị mang lại | Vì sao khách chọn bạn thay vì cách khác? |
| 3 | Kênh | Khách biết, mua, nhận hàng ở đâu? |
| 4 | Quan hệ khách hàng | Giữ khách và khiến khách giới thiệu bằng cách nào? |
| 5 | Dòng doanh thu | Tiền vào từ đâu, bao nhiêu, bao lâu một lần? |
| 6 | Nguồn lực chính | Cần có gì để làm được? |
| 7 | Hoạt động chính | Việc gì phải làm giỏi mỗi ngày? |
| 8 | Đối tác chính | Ai bên ngoài giúp bạn? |
| 9 | Cơ cấu chi phí | Tiền ra đi đâu? (cố định và theo đơn) |

Quy tắc:
- Mỗi lượt **chỉ 1 ô**, 2–3 câu, có gợi ý A-B-C-D. Ô đã có trong Bộ Não → trình lại để xác nhận, không hỏi lại.
- "Chưa biết" → AI đề xuất phương án hợp lý, gắn nhãn **[Giả định]**.
- Sau mỗi ô: tóm lại 1–3 gạch đầu dòng ngắn, hỏi "Đúng chưa?" rồi mới sang ô tiếp.
- Thấy mâu thuẫn với ô trước (vd khách sinh viên nhưng giá 5 triệu) → nhắc ngay, không đợi tới cuối.

### Bước 3 — Dựng bản canvas
- Ghi dữ liệu theo mẫu `scripts/vi-du-canvas.json` (mỗi ô 1–6 ý ngắn + điểm + ghi chú).
- Chạy `scripts/tao_canvas.py` để ra **bảng Markdown 9 ô + sơ đồ Mermaid** và **file `.canvas`** (chuẩn JSON Canvas, bố cục chuẩn: Đối tác | Hoạt động/Nguồn lực | Giá trị | Quan hệ/Kênh | Khách hàng ở trên; Chi phí | Doanh thu ở dưới).
- Không chạy được script → AI tự viết bảng và sơ đồ Mermaid theo cùng định dạng.

### Bước 4 — Chấm điểm từng ô (1–10)
Theo thang trong `references/cau-hoi-9-o.md`: 9–10 rõ ràng có bằng chứng thật · 7–8 rõ, có một phần bằng chứng · 5–6 chung chung/chưa kiểm chứng · 3–4 mơ hồ · 1–2 trống hoặc mâu thuẫn. Điểm trung bình: ≥ 7,5 vững · 5,5–7,4 khá, cần kiểm chứng vài ô · < 5,5 còn mơ hồ, chưa nên bỏ vốn lớn.

### Bước 5 — Kiểm tra 9 ô có ăn khớp không
Đi qua **8 cặp ô** trong `references/cau-hoi-9-o.md` (khách ↔ giá trị, khách ↔ kênh, khách ↔ quan hệ, giá trị ↔ doanh thu, giá trị ↔ hoạt động + nguồn lực, hoạt động ↔ đối tác, hoạt động + nguồn lực ↔ chi phí, doanh thu ↔ chi phí). Mỗi cặp: **Khớp / Chưa chắc / Lệch** + 1 câu lý do. Tính nhanh doanh thu và chi phí/tháng ước lượng để kiểm cặp cuối.

### Bước 6 — Chỉ ra 1–3 giả định rủi ro nhất
Chọn giả định thỏa cả 2 điều: **(1) nếu sai thì mô hình sụp** và **(2) hiện chưa có bằng chứng**. Với mỗi giả định, ghi:
- Giả định: "Chúng tôi tin rằng …"
- Nếu sai thì: …
- Cách kiểm chứng rẻ (≤ 14 ngày, ≤ vài triệu): phỏng vấn 5–10 khách, trang đặt trước, bán thử số lượng nhỏ, nhận cọc, hỏi giá nhà cung cấp, chạy quảng cáo thử nhỏ…
- Ngưỡng đạt (bằng con số) và việc làm tiếp nếu đạt/không đạt.

### Bước 7 — Trình bản nháp và chờ duyệt
Trình 3 phần: **(1) Bản canvas** (bảng + sơ đồ) · **(2) Trang đánh giá** (điểm từng ô, 8 cặp ăn khớp, 3 điểm mạnh, 3 điểm yếu) · **(3) Giả định rủi ro + kế hoạch kiểm chứng**. Hỏi: "Bạn muốn sửa ô nào? Gõ **duyệt** để lưu và xuất file."

### Checklist chất lượng
- [ ] Điền đúng thứ tự 9 ô, mỗi ô 1–6 ý ngắn, cụ thể (có con số khi được).
- [ ] Mọi phương án AI tự đề xuất đều gắn [Giả định].
- [ ] Có điểm 9 ô + điểm trung bình.
- [ ] Đủ 8 cặp kiểm tra ăn khớp.
- [ ] 1–3 giả định rủi ro, mỗi cái có cách kiểm chứng rẻ + ngưỡng đạt.
- [ ] File `.canvas` mở được (JSON hợp lệ, 9 khối đúng bố cục).

### Chạy script
- macOS: `python3 scripts/tao_canvas.py scripts/vi-du-canvas.json --canvas mo-hinh.canvas --out canvas.md`
- Windows: `py scripts\tao_canvas.py scripts\vi-du-canvas.json --canvas mo-hinh.canvas --out canvas.md`

Mở `mo-hinh.canvas` trong Obsidian: chép file vào thư mục Bộ Não (hoặc kho Obsidian bất kỳ) → bấm vào file trong cột trái. Sơ đồ Mermaid hiển thị được trong Obsidian, GitHub, Notion và nhiều trình soạn Markdown.

### Ví dụ minh họa (doanh nghiệp giả định)
*Ví dụ: "Spa Hồng" — spa nhỏ 3 giường chăm sóc da cho nữ văn phòng* (dữ liệu trong `scripts/vi-du-canvas.json`).
- Điểm trung bình 6,4/10 — khá, cần kiểm chứng vài ô. Ô yếu nhất: **Đối tác chính 4/10** (định hợp tác với văn phòng gần đó nhưng chưa ký ai).
- Cặp lệch: Giá trị "liệu trình 45 phút vừa giờ nghỉ trưa" ↔ Nguồn lực "2 kỹ thuật viên, 3 giường" → giờ trưa chỉ phục vụ tối đa 3 khách cùng lúc, khó đạt doanh thu kỳ vọng.
- Giả định rủi ro nhất: "Nữ văn phòng sẵn sàng đi spa giờ nghỉ trưa". Kiểm chứng: mở 15 suất trưa giá thử 199 nghìn trong 10 ngày, đăng nhóm Zalo khách cũ + 2 văn phòng gần đó. Ngưỡng đạt: ≥ 10 suất được đặt.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (10 phút):** giá bán các sản phẩm chính; ước lượng chi phí mỗi tháng (mặt bằng, lương, quảng cáo…); bạn đang bán qua kênh nào. Không có số chính xác cũng được — AI sẽ ghi là giả định.
1. Gõ `/ts-mo-hinh-kinh-doanh` kèm 1 câu mô tả việc kinh doanh (hoặc ý tưởng).
2. Chọn phạm vi (A-B-C-D) và chế độ nhanh/kỹ.
3. Trả lời từng ô — 9 lượt. Gõ chữ cái nếu có gợi ý; không biết thì gõ "chưa biết", AI sẽ đề xuất.
4. Sau mỗi ô, AI tóm tắt lại — sửa ngay nếu sai ("ô này thêm kênh Shopee").
5. Đọc trang đánh giá: chú ý ô dưới 5 điểm và các cặp "Lệch".
6. Chọn 1 giả định rủi ro để kiểm chứng trong 2 tuần tới.
7. Gõ **duyệt** để AI lưu canvas, file `.canvas` và trang đánh giá vào Bộ Não.
8. Sau khi kiểm chứng xong, gõ `/ts-mo-hinh-kinh-doanh cập nhật: kết quả kiểm chứng là …` để chấm lại.

## Câu lệnh mẫu
- `/ts-mo-hinh-kinh-doanh Tôi bán nông sản sạch online (rau, trái cây) giao tận nhà ở TP.HCM.`
- `/ts-mo-hinh-kinh-doanh Dịch vụ sửa điều hòa tại nhà, 3 thợ — xem mô hình có chỗ nào yếu.`
- `/ts-mo-hinh-kinh-doanh Ý tưởng mới: khóa học online dạy chụp ảnh sản phẩm bằng điện thoại — làm chế độ nhanh.`
- `/ts-mo-hinh-kinh-doanh cập nhật ô Kênh: đã thêm TikTok Shop, chiếm 30% đơn.`

## Kết quả nhận được
- Bản canvas 9 ô dạng bảng Markdown (theo thứ tự điền) + sơ đồ Mermaid.
- File `mo-hinh.canvas` mở bằng Obsidian, bố cục 9 khối chuẩn có màu.
- Trang đánh giá: điểm từng ô, điểm trung bình, 8 cặp ăn khớp, điểm mạnh/yếu.
- 1–3 giả định rủi ro nhất + kế hoạch kiểm chứng rẻ có ngưỡng đạt.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-mo-hinh-kinh-doanh-<chu-de-khong-dau>/`.
2. Lưu bản canvas, trang đánh giá và kế hoạch kiểm chứng giả định thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-mo-hinh-kinh-doanh
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `mo-hinh.canvas` (mở bằng Obsidian), `canvas.json` (dữ liệu 9 ô để chạy lại script).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-mo-hinh-kinh-doanh · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu canvas là của doanh nghiệp đang hoạt động (phạm vi A) và khác với `01-ho-so/01-ho-so-doanh-nghiep.md` (hoặc tệp còn trống), trình đoạn đề xuất cập nhật (khách hàng chính, giá trị cốt lõi, kênh, dòng doanh thu, nguồn lực, đối tác) và hỏi trước khi ghi đè. Phạm vi C (ý tưởng mới) thì không ghi vào hồ sơ — có thể tạo trang theo dõi trong `05-du-an/`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Canvas là **bản giả thuyết**, không phải sự thật. Giá trị lớn nhất nằm ở việc chỉ ra giả định để kiểm chứng.
- Không bịa số liệu thị trường, doanh thu đối thủ hay lời khách. Thiếu thì ghi `[CẦN BỔ SUNG: …]` hoặc [Giả định].
- Không khuyên vay vốn, thế chấp hay bỏ việc dựa trên canvas chưa kiểm chứng.
- Số tiền trong canvas là ước lượng thô — muốn ra quyết định tài chính, chạy `/ts-ke-hoach-loi-nhuan`.
- Ngành có điều kiện (spa, thực phẩm, giáo dục, y tế…): ghi vào ô Nguồn lực/Hoạt động việc xin giấy phép cần thiết.

## Skill liên quan
- Trước: `/ts-kiem-chung-ngach` · `/ts-chan-dung-khach-hang`
- Sau: `/ts-dinh-gia-offer` · `/ts-ke-hoach-loi-nhuan` · `/ts-thiet-ke-pheu` · `/ts-tao-ho-so-doanh-nghiep`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
