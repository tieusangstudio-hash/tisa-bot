---
name: ts-chan-dung-khach-hang
description: "Gọi bằng /ts-chan-dung-khach-hang. Dựng chân dung khách hàng mục tiêu (nhân khẩu học, tâm lý, hành vi, nơi họ tụ tập, lý do mua thật theo Jobs To Be Done), chấm điểm và xếp hạng nỗi đau, mong muốn, rồi gom thành 3–5 cụm nội dung có sẵn ý bài. Dùng khi chưa rõ bán cho ai, không biết làm nội dung gì trước, hoặc quảng cáo ra khách sai. Từ khóa: chân dung khách hàng, khách hàng mục tiêu, nỗi đau khách hàng, insight khách, persona, nên làm content gì, cụm nội dung, khách mua vì sao."
---

# /ts-chan-dung-khach-hang — Dựng chân dung khách hàng & bản đồ nỗi đau

> Giúp bạn biết rõ **khách là ai, đang khổ vì điều gì, thật sự mua để làm gì và hay ở đâu** — rồi biến những điều đó thành bảng xếp hạng nỗi đau có điểm số và 3–5 cụm nội dung làm được ngay.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Mới kinh doanh, chưa rõ nên bán cho ai, nói chuyện với ai.
- Đăng bài đều mà ít tương tác, chạy quảng cáo ra khách không đúng.
- Cần biết nên làm nội dung (bài viết, video) về chủ đề gì trước.
- Chuẩn bị viết trang bán hàng, kịch bản quảng cáo, kịch bản tư vấn — cần "ngôn ngữ của khách".
- Có sản phẩm mới, muốn kiểm tra lại tệp khách cũ còn đúng không.

**Không dùng khi:** chưa có ý tưởng kinh doanh cụ thể và cần biết ngách có đáng làm không → dùng `/ts-kiem-chung-ngach`. Muốn soi đối thủ đang bán gì → dùng `/ts-phan-tich-doi-thu`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `chan-dung-khach-hang` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Chốt phạm vi
Hỏi (gợi ý A-B-C-D) để chốt **1 sản phẩm/dịch vụ** và **1 nhóm khách** cho lần chạy này. Nếu người dùng có nhiều nhóm khách, đề nghị làm nhóm đem lại nhiều tiền nhất trước, nhóm khác chạy lần sau.

### Bước 2 — Thu thập thông tin
- Nếu có Bộ Não: đọc thêm `02-kien-thuc/khach-hang/` và `03-tai-lieu-tho/` (ảnh chụp tin nhắn, bình luận, kết quả khảo sát) — đây là bằng chứng thật, ưu tiên hơn phán đoán.
- Hỏi theo **Phần A** trong `references/bo-cau-hoi.md` (8 câu, chia 3 lượt, mỗi lượt 2–3 câu). Bỏ qua câu đã có trong Bộ Não.
- Xin người dùng dán ảnh/chữ: tin nhắn khách, bình luận, đánh giá, ghi chú phỏng vấn. Có bao nhiêu dùng bấy nhiêu.
- Nếu môi trường có công cụ tìm kiếm web: tìm thêm 3–5 nguồn công khai (bình luận nhóm Facebook, đánh giá trên sàn, video TikTok cùng chủ đề) để lấy câu nói thật của khách. Ghi link nguồn.

### Bước 3 — Dựng chân dung 5 lớp
Viết thành bảng, mỗi dòng ghi rõ **[Dữ kiện]** (có nguồn: khách nói, số liệu, link) hoặc **[Phán đoán]** (AI suy ra, cần kiểm chứng):

| Lớp | Nội dung cần có |
|---|---|
| 1. Nhân khẩu học | tuổi, giới, nơi sống, nghề, thu nhập, tình trạng gia đình, người trả tiền vs người dùng |
| 2. Tâm lý | giá trị họ coi trọng, nỗi sợ, niềm tin sai, hình mẫu họ muốn trở thành |
| 3. Hành vi | mua khi nào, mua bao lâu một lần, chi bao nhiêu, cân nhắc bao lâu, ai tác động |
| 4. Nơi tụ tập | nhóm Facebook, kênh TikTok/YouTube, Zalo, sàn, địa điểm ngoài đời — ghi tên cụ thể nếu biết |
| 5. Lý do mua thật (Jobs To Be Done) | xem bên dưới |

**Lý do mua thật — Jobs To Be Done** (khung công khai: khách không mua sản phẩm, khách "thuê" sản phẩm để làm xong một việc trong đời họ). Viết đủ 3 tầng:
- **Việc chức năng:** việc cụ thể cần xong (vd "có bánh sinh nhật đúng 18h thứ Bảy").
- **Việc cảm xúc:** cảm giác muốn có / muốn tránh (vd "yên tâm, không phải lo").
- **Việc xã hội:** người khác nhìn mình thế nào (vd "được khen là mẹ chu đáo").

Kèm 1 câu tóm: *"Khi [hoàn cảnh], tôi muốn [việc cần xong], để [kết quả mong đợi]."*
Thêm 2 ý: **sự kiện kích hoạt** (chuyện gì làm khách bắt đầu tìm) và **lực cản** (thói quen cũ, nỗi lo khiến khách chần chừ).

### Bước 4 — Liệt kê nỗi đau và mong muốn
- 8–15 **nỗi đau** (điều khách đang khổ, sợ, tốn kém, xấu hổ) và 5–8 **mong muốn** (kết quả họ mơ tới).
- Viết bằng **lời của khách**, cụ thể, có cảm xúc. Sai: "chất lượng kém". Đúng: "bánh nhận về khác hẳn ảnh, xấu hổ với khách mời".

### Bước 5 — Chấm điểm (thang 1–10) và xếp hạng
Mỗi mục chấm 3 tiêu chí:
- **Mức đau** (với mong muốn: **mức khao khát**) — 1 = hơi phiền, 10 = mất ngủ/mất tiền lớn.
- **Mức phổ biến** — 1 = rất ít người gặp, 10 = gần như ai trong nhóm khách cũng gặp.
- **Khả năng mình giải được** — 1 = sản phẩm hiện tại không giải được, 10 = giải trọn vẹn và chứng minh được.

**Điểm = Đau × Phổ biến × Giải được ÷ 10** (tối đa 100). ≥40: Ưu tiên 1 · 20–39: Ưu tiên 2 · <20: Để sau.

Cách chạy: ghi dữ liệu ra file JSON theo mẫu `scripts/vi-du-noi-dau.json`, rồi chạy `scripts/cham_diem.py` (xem phần "Chạy script"). Không chạy được script thì AI tự tính và trình bảng cùng định dạng.

Đánh dấu **CẦN KIỂM CHỨNG** cho mục là phán đoán hoặc chưa có bằng chứng. Mục điểm cao mà cần kiểm chứng → phải kiểm chứng trước khi đổ tiền quảng cáo.

### Bước 6 — Gom 3–5 cụm nội dung
Gom các nỗi đau/mong muốn cùng gốc thành **cụm** (đặt tên cụm bằng kết quả khách muốn). Xếp cụm theo tổng điểm. Mỗi cụm gợi ý **4 bài theo đúng thứ tự**:
1. **Khơi vấn đề** — gọi đúng nỗi đau bằng lời của khách.
2. **Kết quả mong muốn** — vẽ ra "sau khi giải quyết" trông thế nào.
3. **Cách làm** — chia sẻ 1 mẹo/quy trình thật, cho đi giá trị.
4. **Bằng chứng** — câu chuyện khách, số liệu, trước–sau (chỉ dùng bằng chứng thật; thiếu thì ghi `[CẦN BỔ SUNG: …]`).

Mỗi bài: tiêu đề gợi ý + 1 câu ý chính + định dạng gợi ý (bài viết / video ngắn / ảnh nhiều trang).

### Bước 7 — Kế hoạch kiểm chứng
Chọn 3 mục quan trọng nhất đang là phán đoán → đề xuất cách kiểm chứng rẻ: phỏng vấn 5 khách (Phần B), khảo sát nhanh (Phần C), đọc 50 bình luận trên nhóm/sàn, hoặc đăng 1 bài thử đo tương tác.

### Bước 8 — Trình bản nháp và chờ duyệt
Trình đủ: chân dung 5 lớp → bảng xếp hạng → cụm nội dung → kế hoạch kiểm chứng. Hỏi: "Bạn muốn sửa gì? Gõ **duyệt** để lưu."

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Chỉ 1 nhóm khách, 1 sản phẩm cho mỗi lần chạy.
- [ ] Mỗi nhận định có nhãn [Dữ kiện] hoặc [Phán đoán].
- [ ] Nỗi đau viết bằng lời của khách, không viết chung chung.
- [ ] Có đủ 3 tầng Jobs To Be Done + câu tóm "Khi… tôi muốn… để…".
- [ ] Điểm tính đúng công thức, bảng xếp đúng thứ tự.
- [ ] 3–5 cụm, mỗi cụm đủ 4 bài theo thứ tự.
- [ ] Không bịa lời khách, không bịa số liệu.

### Chạy script
- macOS: `python3 scripts/cham_diem.py scripts/vi-du-noi-dau.json --out bang-xep-hang.md`
- Windows: `py scripts\cham_diem.py scripts\vi-du-noi-dau.json --out bang-xep-hang.md`

Chỉ cần Python 3, không cài thêm gì. Nếu môi trường cho chạy lệnh, AI tự tạo file JSON từ dữ liệu đã hỏi và chạy giúp học viên. Script báo lỗi bằng tiếng Việt nếu điểm nằm ngoài 1–10 hoặc thiếu trường.

### Ví dụ minh họa (doanh nghiệp giả định)
*Ví dụ: "Tiệm bánh Mây" bán bánh kem sinh nhật đặt online.*
- **Chân dung:** mẹ 28–38 tuổi, đi làm văn phòng, có con 3–8 tuổi, tự đặt bánh qua Fanpage/Zalo, chi 350–700 nghìn/bánh, hay ở nhóm "mẹ bỉm" theo quận.
- **Jobs To Be Done:** *Khi sinh nhật con sắp tới mà mình bận đi làm, tôi muốn đặt được chiếc bánh đúng nhân vật con thích và giao đúng giờ, để con vui và mình không mất mặt với họ hàng.*
- **Top nỗi đau:** "Sợ bánh giao trễ, hỏng tiệc" (56,7 điểm) · "Bánh ngoài ảnh đẹp, nhận về khác hẳn" (51,2 điểm).
- **Cụm 1 — Bánh nhận về đúng như ảnh:** (1) "3 dấu hiệu tiệm bánh dùng ảnh mạng" · (2) "Khoảnh khắc con reo lên khi mở hộp bánh" · (3) "Cách tiệm chụp bánh thật trước khi giao" · (4) "[CẦN BỔ SUNG: video khách mở hộp, được khách đồng ý đăng]".

Chạy `scripts/cham_diem.py scripts/vi-du-noi-dau.json` để xem bảng đầy đủ của ví dụ này.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (10–15 phút):** chụp 5–10 tin nhắn/bình luận của khách thật (che tên, số điện thoại); ghi lại 3 câu khách hay hỏi nhất; nghĩ sẵn sản phẩm bán chạy nhất.
1. Gõ `/ts-chan-dung-khach-hang` kèm 1 câu: bạn bán gì, cho ai (nếu đã biết).
2. Trả lời 3 lượt câu hỏi. Có gợi ý A-B-C-D thì chỉ cần gõ chữ cái; không chắc thì gõ "chưa biết" — AI sẽ đề xuất và đánh dấu là phán đoán.
3. Dán ảnh/chữ tin nhắn khách khi AI xin. Càng nhiều câu thật, chân dung càng chính xác.
4. Xem bảng điểm. Thấy điểm nào chưa đúng với thực tế, nói thẳng: "nỗi đau số 3 phổ biến hơn, cho 8 điểm".
5. Chọn cụm nội dung muốn làm trước (thường là cụm hạng 1).
6. Gõ **duyệt** để AI lưu vào Bộ Não.
7. Trong 1–2 tuần: hỏi 5 khách thật theo `references/bo-cau-hoi.md` (Phần B), dán ghi chú lại, gõ `/ts-chan-dung-khach-hang cập nhật` để AI chấm lại điểm.

## Câu lệnh mẫu
- `/ts-chan-dung-khach-hang Tôi bán mỹ phẩm thiên nhiên online qua TikTok Shop, khách chủ yếu là nữ 20–30 tuổi.`
- `/ts-chan-dung-khach-hang Spa chăm sóc da ở Đà Nẵng, muốn biết khách thật sự lo gì để làm video.`
- `/ts-chan-dung-khach-hang Khóa học quay video bằng điện thoại cho chủ shop — gom giúp 4 cụm nội dung cho tháng sau.`
- `/ts-chan-dung-khach-hang cập nhật — đây là ghi chú phỏng vấn 6 khách tuần này: …`

## Kết quả nhận được
- Bảng chân dung 5 lớp, mỗi ý có nhãn [Dữ kiện]/[Phán đoán].
- Câu "lý do mua thật" theo Jobs To Be Done + sự kiện kích hoạt + lực cản.
- Bảng xếp hạng nỗi đau và mong muốn có điểm số, mức ưu tiên, cột "cần kiểm chứng".
- 3–5 cụm nội dung, mỗi cụm 4 bài (khơi vấn đề → kết quả mong muốn → cách làm → bằng chứng).
- Danh sách "ngôn ngữ của khách" (câu nguyên văn dùng làm tiêu đề/quảng cáo).
- Kế hoạch kiểm chứng 3 giả định quan trọng nhất.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-chan-dung-khach-hang-<chu-de-khong-dau>/`.
2. Lưu toàn bộ chân dung, bảng xếp hạng, cụm nội dung và kế hoạch kiểm chứng thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-chan-dung-khach-hang
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `noi-dau.json` (dữ liệu chấm điểm), `bang-xep-hang.md` (kết quả script), `ngon-ngu-khach.md` (câu nguyên văn của khách).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-chan-dung-khach-hang · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu chân dung khách đã chốt khác với `01-ho-so/03-khach-hang-muc-tieu.md` (hoặc tệp này còn trống), trình đoạn đề xuất cập nhật (chân dung 5 lớp rút gọn, câu Jobs To Be Done, top 5 nỗi đau, top 3 mong muốn, nơi tụ tập) và hỏi trước khi ghi đè. Câu nguyên văn của khách có thể lưu thêm vào `02-kien-thuc/khach-hang/`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Không bịa lời khách, đánh giá hay số liệu.** Thiếu thì ghi `[CẦN BỔ SUNG: …]` hoặc đánh dấu [Phán đoán].
- Không lưu tên thật, số điện thoại, ảnh đại diện của khách vào Bộ Não — chỉ lưu nội dung đã ẩn danh.
- Chân dung là giả thuyết sống: kiểm chứng và cập nhật mỗi 3 tháng hoặc khi ra sản phẩm mới.
- Không dùng chân dung để nhắm mục tiêu quảng cáo theo đặc điểm nhạy cảm (sức khỏe, tôn giáo, chính trị…) — vi phạm chính sách quảng cáo.
- Nếu nỗi đau rất cao mà "giải được" thấp: đừng hứa trong nội dung điều sản phẩm chưa làm được.

## Skill liên quan
- Trước: `/ts-kiem-chung-ngach` (ngách có đáng làm không) · `/ts-tao-ho-so-doanh-nghiep`
- Sau: `/ts-lich-noi-dung` (lên lịch theo cụm) · `/ts-dinh-gia-offer` · `/ts-viet-bai-ban-hang` · `/ts-kich-ban-reels`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
