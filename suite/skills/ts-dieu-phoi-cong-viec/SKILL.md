---
name: ts-dieu-phoi-cong-viec
description: "Gọi bằng /ts-dieu-phoi-cong-viec. Biến một mục tiêu hoặc ý tưởng thành quy trình nhiều bước: chọn đúng lệnh /ts- trong 52 lệnh, chỉ ra dữ liệu còn thiếu, trình kế hoạch để duyệt rồi chạy lần lượt (có thể chia 3 sub-agent). Có sẵn quy trình mẫu: ra mắt khóa học 30 ngày, mở shop online, chạy quảng cáo kéo inbox, phễu quà tặng. Dùng khi chưa biết gọi lệnh nào hoặc muốn làm trọn gói. Từ khóa: làm trọn gói, lập quy trình, nên bắt đầu từ đâu, phối hợp các lệnh, kế hoạch triển khai, điều phối, workflow."
---

# /ts-dieu-phoi-cong-viec — Điều phối công việc

> Bạn nói mục tiêu bằng 1–2 câu, AI chọn đúng các lệnh `/ts-...` cần dùng, xếp thành quy trình có
> đầu vào – đầu ra rõ ràng, trình bạn duyệt, rồi chạy từng bước và dừng đúng chỗ cần bạn xác nhận.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Chưa biết nên gọi lệnh nào, hoặc không nhớ hết 52 lệnh.
- Muốn làm một dự án nhiều bước: ra mắt sản phẩm, mở shop online, chạy chiến dịch, dựng phễu.
- Nói "làm trọn gói giúp tôi", "lập quy trình", "bắt đầu từ đâu".
- Muốn AI tiếp tục chạy các bước sau khi đã duyệt kế hoạch.
- Muốn xem lại dự án đang làm dở đến đâu (đọc `05-du-an/` và `04-ket-qua/`).

**Không dùng khi:** việc chỉ cần đúng một lệnh (vd "viết 1 bài bán hàng") → gọi thẳng lệnh đó,
vd `/ts-viet-bai-ban-hang`. Chưa có Bộ Não → `/ts-cai-dat-bo-nao` trước.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `05-muc-tieu-quy-tac-lien-he.md` (đủ để biết bán gì, mục tiêu, ngân sách; đọc thêm tệp khác khi quy trình cần);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `dieu-phoi-cong-viec` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** đọc thêm `05-du-an/` (dự án đang chạy) và `nhat-ky.md` (10 dòng cuối) để biết
bước nào đã xong — không đưa lại vào kế hoạch những bước đã có kết quả được duyệt.

## Quy trình AI thực hiện

Không giả vờ có công cụ, tài khoản, quyền truy cập hoặc kết nối chưa được kiểm tra.

### Bước 1 — Hiểu kết quả cần đạt
Tóm tắt tối đa 5 dòng:
- Mục tiêu cuối cùng (có con số nếu được).
- Ai dùng / ai là khách hàng.
- Đầu ra cần tạo.
- Thời hạn hoặc nhịp làm (1 lần / mỗi tuần / 30 ngày).
- Ràng buộc: thương hiệu, ngân sách, nền tảng, quyền truy cập.

Chỉ hỏi **tối đa 3 câu ngắn** nếu câu trả lời làm thay đổi đáng kể quy trình (có gợi ý A-B-C-D).
Không hỏi lại dữ liệu đã có trong Bộ Não, cuộc trò chuyện hoặc tệp người dùng gửi.

### Bước 2 — Chọn lệnh và lập luồng
- Đọc `references/danh-muc-skill.md` (52 lệnh chia 5 giai đoạn, kèm quy tắc chọn và chuỗi đầu ra → đầu vào).
- Nếu mục tiêu giống một mẫu có sẵn, đọc `references/quy-trinh-mau.md` và dùng làm khung:
  1. Ra mắt khóa học mới 30 ngày · 2. Mở cửa hàng online · 3. Chạy quảng cáo kéo tin nhắn ·
  4. Dựng phễu quà tặng 0 đồng · 5. Lịch nội dung đều đặn mỗi tuần.
- Chỉ chọn lệnh thật sự cần. Ưu tiên luồng **3–7 bước**; dự án lớn thì chia giai đoạn, mỗi giai đoạn 3–7 bước.
- Mỗi bước ghi đủ 5 ý: (1) lệnh `/ts-...` · (2) đầu vào · (3) việc sẽ làm · (4) đầu ra · (5) điều kiện qua bước.
- Bước nào chạy song song được thì ghi rõ, nhưng không tự mở rộng phạm vi.

### Bước 3 — Kiểm tra khả năng thực hiện
Gắn nhãn từng bước:
- `LÀM NGAY` — đủ dữ liệu và công cụ.
- `CẦN DỮ LIỆU` — thiếu nội dung, tệp hoặc lựa chọn của người dùng.
- `CẦN KẾT NỐI` — cần kết nối Facebook, Telegram, Google… (gợi ý `/ts-ket-noi-ung-dung`).
- `CẦN XÁC NHẬN` — có hành động bên ngoài: chi tiền, đăng bài, gửi tin, đặt lịch, sửa dữ liệu.
- `HƯỚNG DẪN` — môi trường hiện tại không làm trực tiếp được, AI chỉ hướng dẫn từng bước.

Không biến một bước "hướng dẫn" thành lời khẳng định đã thao tác trên nền tảng.

### Bước 4 — Trình kế hoạch để duyệt (cổng duyệt)
```text
MỤC TIÊU: …
ĐẦU RA CUỐI: …
QUY TRÌNH:
1. /ts-…  | Đầu vào: … | Đầu ra: … | Nhãn: LÀM NGAY
2. /ts-…  | Đầu vào: … | Đầu ra: … | Nhãn: CẦN XÁC NHẬN
…
CẦN BẠN CUNG CẤP: …
CẦN BẠN XÁC NHẬN TRƯỚC KHI LÀM: …
THỜI GIAN ƯỚC TÍNH: …
👉 Gõ "duyệt" để bắt đầu, hoặc sửa: "bỏ bước 3", "thêm video", "làm nhanh hơn".
```
Nếu người dùng đã nói "làm luôn" và mọi bước đều an toàn, nội bộ, hoàn tác được → chạy tiếp.
Có hành động bên ngoài hoặc tốn tiền → vẫn dừng đúng điểm cần xác nhận.

### Bước 5 — Thực hiện và kiểm tra
Sau khi được duyệt:
1. Chạy theo thứ tự phụ thuộc; mỗi bước làm đúng theo hướng dẫn của lệnh `/ts-...` tương ứng
   (nếu lệnh đó có trong môi trường thì gọi nó; nếu không, làm theo mô tả trong danh mục).
2. Dùng lại đầu ra bước trước, không hỏi lại.
3. Kiểm tra chất lượng từng đầu ra trước khi sang bước sau.
4. Sau mỗi bước báo 1 dòng: `✅ Bước 2/6 xong — <đầu ra> — đã lưu <đường dẫn>`.
5. Không nói "hoàn thành" nếu mới có bản nháp hoặc hướng dẫn.

Đọc `references/cong-xac-nhan.md` trước khi: đăng bài, gửi tin, chạy quảng cáo, đổi ngân sách,
xuất bản website, kết nối tài khoản, đặt lịch.

### Bước 6 — Điều phối tối đa 3 sub-agent (nếu nền tảng hỗ trợ)
Chỉ dùng khi người dùng yêu cầu, hoặc quy trình có nhánh làm song song được. Nếu nền tảng không có
sub-agent (hoặc không chắc) → **làm tuần tự**, kết quả vẫn như nhau.

Không tạo nhiều agent khi các nhánh cùng sửa một tệp, dùng chung trạng thái dễ xung đột, hoặc bước sau
phụ thuộc hoàn toàn bước trước. Khi dùng 3 sub-agent, ưu tiên:
1. **NGHIÊN CỨU** — thu thập dữ kiện, nguồn, đối thủ, insight khách hàng.
2. **SẢN XUẤT** — viết, thiết kế, phân tích, tạo tài sản từ brief.
3. **KIỂM TRA / TRIỂN KHAI** — soát lỗi, đối chiếu yêu cầu, chuẩn bị xuất bản (vẫn dừng ở cổng xác nhận).

Mỗi nhiệm vụ giao cho sub-agent phải ghi rõ: đầu vào, đầu ra, giới hạn, tiêu chí hoàn thành, tệp được
phép sửa. Các agent dùng chung brief ban đầu (kèm tóm tắt hồ sơ từ Bộ Não). AI chính hợp nhất kết quả,
loại mâu thuẫn, đánh dấu giả định, trình một phương án cuối. Có kết quả nghiên cứu mới → chỉ làm lại
phần sản xuất bị ảnh hưởng, không làm lại toàn bộ. Bảng phân công gợi ý theo từng mẫu ở cuối
`references/quy-trinh-mau.md`.

### Bước 7 — Bàn giao
Kết thúc bằng:
- Kết quả đã tạo (kèm đường dẫn tệp/liên kết).
- Việc chưa làm được và lý do.
- **Một** bước tiếp theo có giá trị nhất.

### Checklist chất lượng
- [ ] Mỗi bước có đủ: lệnh, đầu vào, việc làm, đầu ra, điều kiện qua bước.
- [ ] Không có bước thừa; bước đã có kết quả trong Bộ Não được bỏ qua.
- [ ] Mọi hành động tốn tiền / công khai / gửi tin đều có nhãn `CẦN XÁC NHẬN`.
- [ ] Không khẳng định đã kết nối/đã đăng khi chưa kiểm tra thật.
- [ ] Tên lệnh đúng danh mục 52 lệnh `/ts-...`.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** đã chạy `/ts-cai-dat-bo-nao` và `/ts-tao-ho-so-doanh-nghiep` (ít nhất bản nhanh). Nghĩ sẵn
1 mục tiêu có con số và thời hạn (vd "40 học viên trong 30 ngày").

1. Gõ `/ts-dieu-phoi-cong-viec` kèm mục tiêu (vd "tôi muốn ra mắt khóa học mới trong 30 ngày").
2. Trả lời tối đa 3 câu hỏi AI đưa ra (chọn A-B-C-D).
3. Đọc kế hoạch: mỗi dòng là một lệnh `/ts-...` sẽ chạy, kèm thứ cần bạn chuẩn bị.
4. Sửa bằng lời nếu muốn ("bỏ bước quảng cáo", "thêm video TikTok", "ngân sách chỉ 3 triệu").
5. Gõ "duyệt" — AI chạy từng bước, báo tiến độ sau mỗi bước.
6. Khi AI dừng ở bước có chữ `CẦN XÁC NHẬN` (đăng bài, chi tiền…): đọc kỹ bản xem trước rồi mới gõ "duyệt".
7. Hôm sau muốn làm tiếp: gõ `/ts-dieu-phoi-cong-viec làm tiếp dự án <tên>` — AI đọc Bộ Não để biết đã đến đâu.

## Câu lệnh mẫu
- `/ts-dieu-phoi-cong-viec tôi muốn ra mắt khóa học quay video bằng điện thoại trong 30 ngày, mục tiêu 40 học viên`
- `/ts-dieu-phoi-cong-viec tôi mới mở tiệm bánh online, chưa có gì cả, bắt đầu từ đâu?`
- `/ts-dieu-phoi-cong-viec chạy quảng cáo kéo tin nhắn cho gói chăm sóc da 399k, ngân sách 300k/ngày`
- `/ts-dieu-phoi-cong-viec dựng phễu quà tặng ebook để thu số điện thoại khách cho shop mỹ phẩm`
- `/ts-dieu-phoi-cong-viec làm tiếp dự án ra mắt khóa học, hôm qua làm đến bước trang bán hàng`

## Kết quả nhận được
- Bản kế hoạch quy trình: các bước, lệnh dùng, đầu vào/đầu ra, điểm cần xác nhận, thời gian ước tính.
- Kết quả từng bước (do các lệnh `/ts-...` tạo), lưu trong Bộ Não.
- Trang theo dõi dự án trong `05-du-an/` (nếu dự án nhiều ngày).
- Danh sách việc chưa xong và bước tiếp theo.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-dieu-phoi-cong-viec-<chu-de-khong-dau>/`.
2. Lưu kế hoạch quy trình đã duyệt (bảng bước, nhãn, trạng thái từng bước, việc còn chờ) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-dieu-phoi-cong-viec
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [quy-trinh, ke-hoach, <tên dự án>]
   ---
   ```
   Kèm theo các file phụ (nếu có): không có — kết quả của từng lệnh con do chính lệnh đó lưu vào thư mục riêng.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-dieu-phoi-cong-viec · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Dự án kéo dài nhiều ngày: tạo hoặc cập nhật `05-du-an/<ten-du-an-khong-dau>.md` (mục tiêu, bảng bước có
   ô ✅/⏳, liên kết tới kết quả từng bước, ngày cập nhật) và thêm dòng vào mục **Dự án** của `muc-luc.md`.
   Hỏi trước khi ghi đè trang dự án đã có.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không đăng bài, gửi tin, bật/tắt quảng cáo, đổi ngân sách, xuất bản web, đặt lịch khi người dùng chưa nói rõ "duyệt".
- Không xin mật khẩu, OTP, token trong chat — kết nối qua luồng chính thức của nền tảng (`/ts-ket-noi-ung-dung`).
- Không bịa số liệu, kết quả dự kiến như chắc chắn; nêu giả định.
- Sub-agent không được tự hành động bên ngoài; mọi cổng xác nhận vẫn do người dùng quyết.

## Skill liên quan
- Trước: `/ts-cai-dat-bo-nao` · `/ts-tao-ho-so-doanh-nghiep`
- Sau: bất kỳ lệnh nào trong 52 lệnh — xem `references/danh-muc-skill.md`; tạo lệnh mới: `/ts-tao-skill`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
