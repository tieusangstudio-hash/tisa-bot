---
name: ts-soan-hop-dong
description: "Gọi bằng /ts-soan-hop-dong. Soạn và rà soát văn bản kinh doanh: hợp đồng dịch vụ, hợp đồng đào tạo, báo giá, biên bản nghiệm thu/bàn giao, proposal, công văn, quy trình; lập dàn ý trước, chừa chỗ trống rõ ràng, kiểm tra số tiền bằng số/chữ và xuất Word/PDF khi có công cụ. Không thay thế tư vấn pháp lý. Từ khóa: soạn hợp đồng, mẫu hợp đồng, báo giá, biên bản nghiệm thu, biên bản bàn giao, hợp đồng dịch vụ, hợp đồng đào tạo, proposal, rà soát hợp đồng."
---

# /ts-soan-hop-dong — Soạn văn bản, báo giá và hợp đồng

> Giúp bạn soạn nhanh văn bản kinh doanh trình bày chuyên nghiệp, đủ điều khoản cơ bản, không sai số tiền, không bỏ sót chỗ trống.
> Kết quả: dàn ý để duyệt, bản nháp hoàn chỉnh có chỗ trống đánh dấu rõ, bảng rà soát trước ký và file Word/PDF (nếu công cụ cho phép).

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Cần hợp đồng dịch vụ (quay dựng, chạy quảng cáo, thiết kế, chăm Fanpage…) hoặc hợp đồng đào tạo/ghi danh khóa học.
- Cần gửi báo giá nhanh, đẹp, có tổng tiền bằng chữ.
- Cần biên bản nghiệm thu, bàn giao sau khi làm xong việc.
- Cần proposal, công văn, thông báo, quy trình (SOP) hoặc biểu mẫu.
- Có sẵn văn bản, muốn rà soát chỗ thiếu, chỗ mâu thuẫn.

**Không dùng khi:** cần ý kiến pháp lý chính thức (tranh chấp, kiện tụng, hợp đồng giá trị lớn) → hỏi luật sư;
cần định giá gói dịch vụ trước khi báo giá → `/ts-dinh-gia-offer`; cần bảng tính tự động tính tiền → `/ts-bang-tinh-excel`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md` (tên pháp nhân, mã số thuế, địa chỉ, người đại diện), `02-san-pham-dich-vu.md` (hạng mục, đơn giá, chính sách), `05-muc-tieu-quy-tac-lien-he.md` (thông tin liên hệ, tài khoản nhận tiền);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `soan-hop-dong` hoặc từ khóa) để dùng lại mẫu đã duyệt.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Xác định loại văn bản và thông tin cốt lõi
Hỏi phần còn thiếu (gợi ý A-B-C-D):
- Loại: (A) Hợp đồng dịch vụ · (B) Hợp đồng đào tạo · (C) Báo giá · (D) Biên bản nghiệm thu/bàn giao · (E) Khác (proposal, công văn, SOP…).
- Mục đích và bên sử dụng: mình là bên cung cấp hay bên thuê? Gửi cho cá nhân hay công ty?
- Phạm vi công việc, số lượng, quy cách.
- Giá, thuế (đã/chưa gồm), cách thanh toán (mấy đợt, tỉ lệ), thời hạn.
- Luật/khu vực áp dụng (mặc định: Việt Nam), ngôn ngữ (tiếng Việt / song ngữ).
- Có mẫu cũ muốn giữ bố cục không? (gửi file).

### Bước 2 — Tách dữ liệu thành 3 nhóm
| Nhóm | Ví dụ | Xử lý |
|---|---|---|
| Đã có | Tên doanh nghiệp, mã số thuế (từ hồ sơ) | Điền thẳng, đọc lại cho người dùng xác nhận |
| Cần xác nhận | Thông tin bên kia, ngày ký, số hợp đồng | Để chỗ trống `[CẦN BỔ SUNG: …]` |
| Điều khoản tùy chọn | Bảo mật, phạt chậm thanh toán, độc quyền | Liệt kê, hỏi có đưa vào không |

### Bước 3 — Lập dàn ý trước (CỔNG DUYỆT 1)
Dùng dàn ý mẫu trong `references/dan-y-mau.md` (hợp đồng dịch vụ, hợp đồng đào tạo, báo giá, biên bản nghiệm thu,
proposal, công văn, SOP), chỉnh theo nhu cầu. Trình dàn ý (tên các điều, ý chính mỗi điều) và chờ người dùng gõ **"duyệt dàn ý"**
hoặc sửa bằng lời ("bỏ điều bảo mật", "thêm điều bảo hành 6 tháng").

### Bước 4 — Soạn bản nháp
- Ngôn ngữ nhất quán: một khi gọi "Bên A" thì dùng "Bên A" suốt văn bản; định nghĩa thuật ngữ một lần.
- Đánh số điều khoản (Điều 1, 1.1, 1.2…); dùng bảng cho hạng mục, tiến độ, thanh toán.
- Chỗ thiếu thông tin dùng placeholder rõ: `[CẦN BỔ SUNG: số tài khoản Bên B]` — không bịa tên, mã số thuế, địa chỉ, căn cứ pháp luật.
- Số tiền ghi cả **bằng số và bằng chữ**. Đổi số thành chữ bằng script (không cần cài thêm):
  - macOS: `python3 scripts/so_thanh_chu.py 15500000`
  - Windows: `py scripts\so_thanh_chu.py 15500000`
  - Kết quả: `15.500.000 → Mười lăm triệu năm trăm nghìn đồng chẵn`. Không chạy được script thì AI tự đổi và đọc lại cho người dùng kiểm.
- Hợp đồng đào tạo: không cam kết thu nhập/doanh số cho học viên; chính sách hoàn phí, bảo lưu chỉ ghi khi có thật trong hồ sơ.
- Tài khoản bàn giao: chỉ ghi tên tài khoản, không ghi mật khẩu vào văn bản.

### Bước 5 — Bảng rà soát bắt buộc
Lập bảng gồm: trường đã xác nhận · trường còn thiếu · điều khoản tùy chọn · rủi ro · người cần duyệt.
Kiểm tra theo loại văn bản:
- Định nghĩa, phạm vi công việc, nghiệm thu, thanh toán, chấm dứt, bảo mật, sở hữu trí tuệ, trách nhiệm, giải quyết tranh chấp.
- Tên pháp nhân, mã số, địa chỉ, số tiền bằng số = bằng chữ, tổng = cộng các dòng, ngày tháng không mâu thuẫn, phụ lục, chữ ký, tham chiếu chéo ("theo Điều 5" có đúng Điều 5 không).
- **Đánh dấu ⚠ cần chuyên gia pháp lý** với: giao dịch giá trị lớn, điều khoản phạt/bồi thường, lao động, thuế, sở hữu trí tuệ, dữ liệu cá nhân.

### Bước 6 — Trình bản nháp (CỔNG DUYỆT 2) và xuất file
- Trình bản nháp + bảng rà soát. Người dùng sửa bằng lời, AI cập nhật. Chờ **"duyệt"**.
- Xuất file: nếu môi trường có công cụ tạo tài liệu Word/PDF thì tạo file, định dạng gọn (cỡ chữ 12–13, lề đều, tiêu đề in đậm,
  bảng có viền), rồi **mở lại kiểm tra bản hiển thị** (không vỡ bảng, không lỗi font tiếng Việt). Không có công cụ → giao bản
  văn bản để học viên dán vào Word/Google Docs.
- Kèm **checklist trước ký** (Bước 5) để học viên tự đánh dấu.

### Checklist chất lượng trước khi giao
- [ ] Không có thông tin pháp nhân, căn cứ pháp luật, mức phạt nào bị bịa.
- [ ] Mọi số tiền có bằng chữ khớp bằng số; tổng cộng đúng.
- [ ] Mọi chỗ thiếu được đánh dấu `[CẦN BỔ SUNG]` và liệt kê ở bảng rà soát.
- [ ] Điều khoản nhạy cảm được đánh dấu cần chuyên gia kiểm tra.
- [ ] Có câu nhắc: văn bản hỗ trợ soạn thảo, không thay thế tư vấn pháp lý.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** thông tin hai bên (tên, mã số thuế/CCCD — chỉ dán khi cần và xóa khỏi chat sau khi xong nếu nền tảng cho phép,
địa chỉ, người đại diện); nội dung công việc; giá và cách thanh toán; mốc thời gian; mẫu cũ (nếu có).

1. Gõ `/ts-soan-hop-dong` kèm 1 câu: loại văn bản và cho ai (vd "báo giá gói quay 8 video cho quán cà phê").
2. Trả lời các câu hỏi AI đưa ra (gợi ý A-B-C-D thì chọn chữ cái). Chưa có thông tin nào thì nói "để trống".
3. Xem **dàn ý**, gõ "duyệt dàn ý" hoặc sửa ("thêm điều bảo hành", "bỏ điều phạt").
4. Xem **bản nháp**. Đọc kỹ bảng rà soát: các dòng `[CẦN BỔ SUNG]` là việc bạn cần điền.
5. Sửa bằng lời ("đổi thanh toán thành 2 đợt 50/50", "thêm số lần chỉnh sửa là 2 lần").
6. Gõ **"duyệt"** để AI xuất file Word/PDF (nếu có công cụ) và lưu vào Bộ Não.
7. Với hợp đồng quan trọng (giá trị lớn, có phạt, có lao động, dữ liệu cá nhân), gửi bản này cho luật sư/kế toán xem trước khi ký.

## Câu lệnh mẫu
- `/ts-soan-hop-dong báo giá gói chăm sóc Fanpage 3 tháng cho spa Hồng, 12 bài/tháng, thanh toán 2 đợt`
- `/ts-soan-hop-dong hợp đồng đào tạo khóa học quay video bằng điện thoại 6 buổi, có chính sách bảo lưu`
- `/ts-soan-hop-dong biên bản nghiệm thu và bàn giao 8 video quảng cáo cho tiệm bánh Mây theo hợp đồng số 05`
- `/ts-soan-hop-dong rà soát giúp hợp đồng thiết kế website này, chỉ ra chỗ thiếu và rủi ro [đính kèm file]`

## Kết quả nhận được
- Dàn ý văn bản để duyệt.
- Bản nháp hoàn chỉnh, đánh số điều khoản, có bảng hạng mục/thanh toán, số tiền bằng số và bằng chữ.
- Bảng rà soát: đã xác nhận / còn thiếu / tùy chọn / rủi ro / người cần duyệt.
- Checklist trước ký.
- File Word/PDF đã kiểm tra hiển thị (khi công cụ cho phép).

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-soan-hop-dong-<chu-de-khong-dau>/`.
2. Lưu văn bản đã duyệt (bản nháp cuối + bảng rà soát + checklist trước ký) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-soan-hop-dong
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd hop-dong, bao-gia, nghiem-thu>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `<ten-van-ban>.docx`, `<ten-van-ban>.pdf`. Không lưu số CCCD/giấy tờ cá nhân của bên kia vào Bộ Não nếu người dùng không yêu cầu.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-soan-hop-dong · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Mẫu văn bản đã duyệt có thể dùng lại: đề xuất lưu bản "mẫu trống" (đã xóa thông tin bên kia) vào `06-mau/` hoặc `02-kien-thuc/cong-thuc/mau-hop-dong-<loai>.md`; thông tin pháp nhân mới khác `01-ho-so/01-ho-so-doanh-nghiep.md` thì đề xuất cập nhật — hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Văn bản do AI hỗ trợ soạn thảo, không phải tư vấn pháp lý** và không thay thế luật sư/kế toán tại địa phương.
- Không bịa thông tin pháp nhân, mã số thuế, căn cứ pháp luật hoặc điều khoản luật.
- Với giao dịch quan trọng, điều khoản phạt/bồi thường, lao động, thuế, sở hữu trí tuệ hoặc dữ liệu cá nhân: ghi rõ cần chuyên gia pháp lý kiểm tra trước khi ký.
- Không ghi mật khẩu, mã OTP, số thẻ vào văn bản hay chat.
- Hạn chế dán giấy tờ cá nhân (CCCD) vào chat; chỉ dùng khi thật cần và để trống nếu được.

## Skill liên quan
- Trước: `/ts-dinh-gia-offer`, `/ts-tao-ho-so-doanh-nghiep` · Sau: `/ts-bang-tinh-excel` (theo dõi hợp đồng, công nợ), `/ts-lap-lich-tu-dong` (nhắc hạn thanh toán, nghiệm thu)

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
