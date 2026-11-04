---
name: ts-cham-soc-khach-zalo
description: "Gọi bằng /ts-cham-soc-khach-zalo. Soạn tin nhắn chăm sóc khách qua Zalo, Messenger, SMS theo 5 nhóm: khách mới tương tác, khách đã hỏi chưa mua, khách đã hỏi giá, khách đã mua chưa dùng, khách cũ — gồm chuỗi nhắc lại 3 lần, nhắc lịch, chào mừng, xin đánh giá, giới thiệu sản phẩm tiếp theo. Dùng khi khách hỏi rồi im, cần nhắc lịch, muốn giữ chân khách cũ. Từ khóa: chăm sóc data, tin nhắn Zalo, follow-up khách, nhắc lịch, nurture lead, inbox khách, chăm sóc khách cũ, tin nhắn chốt đơn."
---

# /ts-cham-soc-khach-zalo — Chăm sóc khách qua Zalo / Messenger

> Soạn sẵn tin nhắn chăm sóc cho từng nhóm khách — từ người mới hỏi đến khách đã mua — để biến người
> quan tâm thành người mua và khách cũ thành khách quay lại. Tin nhắn ngắn, đúng giọng thương hiệu, sẵn copy gửi.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Khách đã nhắn hỏi rồi im lặng — cần chuỗi nhắc lại khéo, không làm phiền.
- Khách đã hỏi giá / hỏi lịch — cần tin nhắn chốt, nhắc hạn ưu đãi.
- Khách vừa mua / vừa đăng ký — cần tin nhắn chào mừng, hướng dẫn, nhắc lịch hẹn.
- Khách đã dùng xong — cần xin đánh giá, giới thiệu sản phẩm/dịch vụ tiếp theo.
- Muốn có bộ mẫu tin nhắn chuẩn cho nhân viên tư vấn dùng chung.

**Không dùng khi:** cần chuỗi email dài nhiều ngày → `/ts-email-cham-soc`; cần lời thoại xử lý khi khách chê
đắt/từ chối trong lúc tư vấn → `/ts-xu-ly-tu-choi`; cần trả lời bình luận/tin nhắn trên Fanpage → `/ts-cham-soc-fanpage`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `cham-soc-khach-zalo` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này: tên người ký tin nhắn, xưng hô lấy từ `04-thuong-hieu-noi-dung.md`; số điện thoại, địa chỉ,
link, giờ làm việc lấy từ `05-muc-tieu-quy-tac-lien-he.md`; băn khoăn khách lấy từ
`02-kien-thuc/khach-hang/bang-khoan-thuong-gap.md` (nếu có).

## Quy trình AI thực hiện

### Bước 1 — Xác định nhóm khách (5 nhóm)
| Nhóm | Ai | Chiến lược |
|---|---|---|
| **1. Khách lạnh** | Đã tương tác (thích, bình luận, theo dõi) nhưng chưa nhắn | Gửi giá trị, **chưa bán** |
| **2. Khách ấm** | Đã nhắn hỏi thông tin, chưa mua | Nhắc lại **tối đa 3 lần trong 7 ngày**, trả lời băn khoăn |
| **3. Khách nóng** | Đã hỏi giá, hỏi lịch, hỏi cách đặt | Nhắc lịch/hạn, tạo lý do quyết định **thật**, chốt |
| **4. Khách đã mua, chưa dùng** | Đã thanh toán / đặt lịch, chưa nhận hàng / chưa đến | Chào mừng, hướng dẫn, nhắc lịch, tạo hứng khởi |
| **5. Khách đã dùng xong** | Đã nhận hàng / dùng dịch vụ / học xong | Xin đánh giá, xin câu chuyện, giới thiệu sản phẩm tiếp theo |

Hỏi người dùng chọn nhóm (A–E tương ứng 1–5) nếu chưa rõ.

### Bước 2 — Xác định mục tiêu và kênh
- Mục tiêu tin nhắn: giới thiệu · nhắc lại · nhắc lịch · chào mừng · xin đánh giá · giới thiệu sản phẩm tiếp theo.
- Kênh: **Zalo** (ngắn, thân mật, 40–90 từ) · **Messenger** (ngắn, có thể dùng nút/biểu tượng) · **SMS** (≤ 160 ký tự,
  không dấu nếu nhà mạng yêu cầu) · **Email** → chuyển `/ts-email-cham-soc`.

### Bước 3 — Soạn tin nhắn từ mẫu
Dùng bộ mẫu ở `references/mau-tin-nhan-5-nhom.md`, điền bằng thông tin hồ sơ:
- `[Tên khách]`, `[tên sản phẩm/dịch vụ]`, `[giá]`, `[ngày/giờ/địa điểm/link]`, `[người ký]`.
- Băn khoăn trong tin nhắn nhắc lần 2: lấy 2 băn khoăn phổ biến nhất của khách trong hồ sơ, trả lời thật.
- Ưu đãi / số suất / quà tặng: **chỉ dùng khi người dùng xác nhận có thật**, kèm hạn chót thật.

### Bước 4 — Điều chỉnh giọng
- Zalo ngắn hơn, thân mật hơn; email đầy đủ hơn.
- Luôn gọi tên khách ở đầu tin; kết thúc bằng **1 câu hỏi hoặc 1 CTA** cụ thể.
- Đúng xưng hô thương hiệu (em – anh/chị, mình – bạn, shop – khách…). Hồ sơ chưa có giọng văn → hỏi nhanh
  3 câu theo `references/mau-giong-thuong-hieu.md`.

### Bước 5 — Xuất bộ tin nhắn + lịch gửi
Mỗi tin: **Gửi khi nào** (vd "ngay khi khách hỏi", "sau 2 ngày không trả lời") · **Kênh** · **Nội dung** sẵn copy.
Kèm bảng lịch gửi tổng (nhóm · tin số · thời điểm · điều kiện dừng).

### Bước 6 — Cổng duyệt
Trình bộ tin. Sửa theo yêu cầu đến khi người dùng gõ **"duyệt"**. Skill này **chỉ soạn**, không tự gửi.
Nếu môi trường có công cụ gửi tin (Zalo OA, Messenger, công cụ CRM) và người dùng muốn gửi: trình danh sách người
nhận + nội dung, chờ "duyệt" cho **từng đợt gửi** rồi mới gửi.

### Nguyên tắc chăm sóc (áp cho mọi tin)
- Không gửi quá **3 lần liên tiếp** khi khách không phản hồi; sau đó chuyển sang nhóm 1 (gửi giá trị thưa hơn).
- Mỗi tin phải có **giá trị** (thông tin, tài liệu, lý do rõ ràng) — không chỉ "Anh/chị còn quan tâm không ạ?".
- Thân thiện, không gây áp lực; không dọa mất cơ hội bằng khan hiếm giả.
- Gửi trong giờ hợp lý (8h–21h); tôn trọng khi khách nói "không cần nữa" — ngừng gửi.

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Đúng nhóm khách, đúng mục tiêu.
- [ ] Gọi tên khách ở đầu; có 1 câu hỏi hoặc 1 CTA ở cuối.
- [ ] Zalo/Messenger ≤ 90 từ; SMS ≤ 160 ký tự.
- [ ] Không có ưu đãi, số suất, lời khen bịa; thông tin liên hệ đúng hồ sơ.
- [ ] Chuỗi nhắc lại không quá 3 tin.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** biết khách đang ở nhóm nào (mới hỏi / hỏi giá / đã mua…), sản phẩm khách quan tâm, ưu
đãi đang có (nếu có), lịch hẹn/ngày giao hàng (nếu cần nhắc).
1. Gõ `/ts-cham-soc-khach-zalo` kèm 1 câu mô tả khách, vd "khách hỏi giá gói chụp ảnh 3 ngày rồi im".
2. Chọn nhóm khách và kênh (Zalo / Messenger / SMS) nếu AI hỏi.
3. Xác nhận ưu đãi, hạn chót, lịch hẹn là **thật**.
4. Xem bộ tin nhắn; sửa bằng lời ("thân mật hơn", "ngắn còn 2 câu").
5. Gõ **"duyệt"** để AI chốt và lưu bộ mẫu vào Bộ Não.
6. Copy từng tin gửi đúng thời điểm trong bảng lịch (hoặc dán vào trả lời nhanh / tin nhắn mẫu của Zalo, Messenger).

## Câu lệnh mẫu
- `/ts-cham-soc-khach-zalo khách hỏi giá combo nối mi rồi không trả lời 2 ngày, soạn chuỗi nhắc lại 3 tin trên Zalo`
- `/ts-cham-soc-khach-zalo nhắc lịch khách đặt bàn tiệc sinh nhật tối thứ 7, gửi trước 1 ngày và 3 tiếng`
- `/ts-cham-soc-khach-zalo tin nhắn chào mừng học viên mới đăng ký khóa học vẽ online, kèm chuẩn bị trước buổi 1`
- `/ts-cham-soc-khach-zalo xin đánh giá khách đã mua máy lọc nước 2 tuần, rồi giới thiệu gói thay lõi`

## Kết quả nhận được
- Bộ tin nhắn theo nhóm khách, mỗi tin ghi rõ gửi khi nào, kênh nào, sẵn copy.
- Bảng lịch gửi + điều kiện dừng.
- (Tùy chọn) bộ "trả lời nhanh" cho nhân viên dùng chung.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-cham-soc-khach-zalo-<chu-de-khong-dau>/`.
2. Lưu bộ tin nhắn đã duyệt (nhóm khách, mục tiêu, kênh, từng tin + thời điểm gửi) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-cham-soc-khach-zalo
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `lich-gui.csv` (nhom, tin-so, thoi-diem, kenh, dieu-kien-dung), `tra-loi-nhanh.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-cham-soc-khach-zalo · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Bộ mẫu tin nhắn dùng lại lâu dài: đề xuất lưu/cập nhật `02-kien-thuc/cong-thuc/mau-tin-nhan-cham-soc.md`. Băn khoăn mới của khách phát hiện được → đề xuất thêm vào `02-kien-thuc/khach-hang/bang-khoan-thuong-gap.md`. Hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Skill chỉ **soạn** tin; gửi hàng loạt qua công cụ chỉ khi người dùng "duyệt" từng đợt.
- Không lưu số điện thoại, thông tin cá nhân của khách vào `04-ket-qua/` — dùng `[Tên khách]` làm chỗ trống.
- Gửi tin hàng loạt cho người chưa đồng ý nhận có thể bị Zalo/Facebook hạn chế tài khoản và vi phạm quy định về
  tin nhắn quảng cáo — chỉ gửi cho khách đã tương tác/đồng ý.
- Không bịa ưu đãi, số suất, lời khen của khách khác.

## Skill liên quan
- Trước: `/ts-viet-bai-ban-hang` · `/ts-len-camp-facebook` · `/ts-xu-ly-tu-choi`
- Sau: `/ts-email-cham-soc` · `/ts-lap-lich-tu-dong` · `/ts-phan-tich-doanh-thu`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
