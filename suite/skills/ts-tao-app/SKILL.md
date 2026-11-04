---
name: ts-tao-app
description: "Gọi bằng /ts-tao-app. Biến ý tưởng tiếng Việt của người không biết lập trình thành ứng dụng chạy được (vibe coding): hỏi tối đa 8 câu dễ trả lời, viết đặc tả 1 trang, chọn bản nhỏ nhất (MVP), xây từng phần chạy được, kiểm thử và viết hướng dẫn sử dụng. Dùng cho công cụ nội bộ, CRM mini, máy tính giá, form đăng ký, dashboard, trợ lý chuyên ngành. Từ khóa: tạo app, vibe coding, làm ứng dụng, làm web app, app quản lý, công cụ nội bộ, không biết code, làm phần mềm."
---

# /ts-tao-app — Tạo app từ ý tưởng (vibe coding)

> Bạn mô tả bằng lời, AI hỏi vài câu, viết đặc tả rồi xây ứng dụng nhỏ chạy được ngay — không cần biết lập trình.
> Kết quả: đặc tả 1 trang, ứng dụng chạy được (thường là 1 trang web mở bằng trình duyệt), hướng dẫn sử dụng và danh sách việc làm tiếp.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Cần công cụ nhỏ cho việc kinh doanh: máy tính báo giá, form đặt lịch, quản lý khách mini, theo dõi đơn, bảng điểm danh.
- Muốn biến file Excel đang dùng thành giao diện dễ nhập hơn trên điện thoại.
- Cần trang hỏi đáp/trợ lý cho khách theo ngành (vd tư vấn chọn size, chọn gói).
- Muốn thử ý tưởng app trước khi thuê lập trình viên.

**Không dùng khi:** cần trang bán hàng/landing page → `/ts-landing-page` hoặc `/ts-trang-ban-hang`; đưa web lên mạng có link thật →
`/ts-dua-web-len-mang`; chỉ cần file Excel → `/ts-bang-tinh-excel`; cần nhận tiền qua mã QR → `/ts-cai-thanh-toan`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Hỏi tối đa 8 câu dễ trả lời
Mỗi câu có gợi ý A-B-C-D, người dùng chỉ cần chọn chữ:
1. Ai dùng app? (A) Chỉ mình tôi · (B) Nhân viên · (C) Khách hàng · (D) Cả nhân viên và khách.
2. Việc chính app giúp làm là gì? (1 câu, vd "tính giá bánh theo size và topping").
3. Dữ liệu gì cần nhập/lưu? (vd tên khách, số điện thoại, món, giá).
4. Dùng trên thiết bị nào? (A) Điện thoại · (B) Máy tính · (C) Cả hai.
5. Dữ liệu lưu ở đâu? (A) Ngay trên máy đang dùng (đơn giản nhất) · (B) Google Sheets · (C) Cần nhiều người dùng chung, lưu trên mạng · (D) Chưa biết.
6. Có cần đăng nhập/tài khoản không? (A) Không · (B) Một mật khẩu chung đơn giản · (C) Mỗi người một tài khoản.
7. Có cần AI hoặc kết nối ứng dụng khác (gửi Telegram, đọc Sheets…) không?
8. Kết quả cuối cần là gì? (A) Xem trên màn hình · (B) Xuất file Excel/PDF · (C) Gửi tin nhắn · (D) In ra.

Thiếu câu nào AI tự chọn phương án đơn giản nhất và ghi rõ là giả định.

### Bước 2 — Đặc tả 1 trang (CỔNG DUYỆT 1)
| Mục | Nội dung |
|---|---|
| Mục tiêu | App giúp ai làm việc gì, đo thành công bằng gì |
| Vai trò | Ai dùng, được làm gì |
| Tính năng | Chia 3 nhóm: **Bắt buộc** (3–7 tính năng lõi) · **Nên có** · **Để sau** |
| Luồng chính | Bước 1 → 2 → 3 người dùng thao tác |
| Dữ liệu | Danh sách trường (tên, kiểu, bắt buộc?) |
| Màn hình | Liệt kê màn hình, trạng thái rỗng ("chưa có khách nào"), trạng thái lỗi |
| Giới hạn | Những gì app **không** làm |
| Tiêu chí hoàn thành | Danh sách kiểm tra để nghiệm thu |

Ví dụ (tiệm bánh Mây — giả định): "Máy tính báo giá bánh: chọn size → chọn cốt → chọn topping → app hiện tổng tiền và nút
'Copy báo giá' để dán vào Messenger. Dữ liệu giá sửa ở 1 bảng. Không cần đăng nhập. Dùng trên điện thoại."

Chờ người dùng gõ **"duyệt đặc tả"** hoặc sửa bằng lời.

### Bước 3 — Chọn bản nhỏ nhất (MVP) và cách làm đơn giản nhất
- Ưu tiên **web app** (mở bằng trình duyệt, chạy cả điện thoại và máy tính) trước app di động cài đặt, nếu không có lý do khác.
- Mặc định đơn giản nhất: **1 file HTML** tự chứa (giao diện + xử lý), lưu dữ liệu trên trình duyệt của máy đang dùng — mở là chạy, không cần cài gì.
  Ghi rõ giới hạn: dữ liệu chỉ nằm trên máy đó, xóa dữ liệu trình duyệt là mất → có nút **Xuất/Nhập file** để sao lưu.
- Cần nhiều người dùng chung → lưu Google Sheets (qua kết nối/`/ts-ket-noi-ung-dung`) hoặc dịch vụ cơ sở dữ liệu — chỉ khi người dùng duyệt (có thể phát sinh tài khoản/chi phí).
- Nếu nền tảng AI có khung xem trước/chia sẻ trang web, dùng để người dùng thử ngay.
- Không thêm thanh toán, đăng nhập phức tạp hoặc nền tảng trả phí nếu chưa được duyệt.

### Bước 4 — Thiết kế trước khi code
Ngắn gọn cho người dùng duyệt: luồng người dùng, mô hình dữ liệu, quyền (ai xem/sửa gì), trạng thái rỗng/lỗi, tiêu chí nghiệm thu.

### Bước 5 — Xây theo lát dọc (từng phần chạy được)
- Mỗi lát là một chức năng hoàn chỉnh từ giao diện đến lưu dữ liệu, chạy được với **dữ liệu mẫu** (vd lát 1: thêm/xem khách; lát 2: tìm kiếm; lát 3: xuất Excel).
- Sau mỗi lát: kiểm thử nhanh, hướng dẫn chạy, checkpoint để người dùng xem và góp ý.
- Giao diện tiếng Việt có dấu, nút to dễ bấm trên điện thoại, chữ đủ lớn, màu theo thương hiệu người dùng (hỏi nếu cần).
- **Không nhúng khóa bí mật vào phần giao diện** (frontend). Cần khóa API → để phía máy chủ/biến môi trường, hoặc bỏ tính năng đó khỏi MVP.

### Bước 6 — Kiểm thử
- Luồng chính chạy đúng (happy path).
- Nhập sai/thiếu: báo lỗi dễ hiểu, không mất dữ liệu đang nhập (validation).
- Dữ liệu rỗng: màn hình đầu tiên không trống trơn, có hướng dẫn.
- Quyền: người không được phép không xem/sửa được (nếu có đăng nhập).
- Điện thoại: thử khung hình hẹp, không tràn ngang.
- Bảo mật cơ bản: không lộ khóa, không chèn được mã độc qua ô nhập (thoát ký tự khi hiển thị).
- Hiệu năng cơ bản với 500–1.000 dòng dữ liệu mẫu; có sao lưu; ghi lỗi (logging) đơn giản nếu cần.

### Bước 7 — Bàn giao (CỔNG DUYỆT 2)
- Mã nguồn chạy được + cách mở/chạy:
  - 1 file HTML: bấm đúp để mở bằng trình duyệt (macOS và Windows như nhau).
  - Có máy chủ chạy cục bộ: macOS `python3 -m http.server 8000` · Windows `py -m http.server 8000` → mở `http://localhost:8000`.
- **Hướng dẫn sử dụng** ngay trong app (nút "Hướng dẫn") hoặc file `HUONG-DAN.md`.
- Danh sách việc để sau (backlog) theo ưu tiên, phần chưa làm, giới hạn kỹ thuật, cách bảo trì (sửa giá ở đâu, sao lưu thế nào).
- Chỉ kết nối dữ liệu hoặc tài khoản thật sau khi người dùng duyệt. Muốn đưa lên mạng có link → `/ts-dua-web-len-mang`.
Chờ người dùng gõ **"duyệt"** để lưu vào Bộ Não.

### Checklist chất lượng trước khi giao
- [ ] Đặc tả đã duyệt; app làm đủ tính năng "Bắt buộc", không thêm thứ chưa duyệt.
- [ ] Chạy được với dữ liệu mẫu; trạng thái rỗng/lỗi rõ ràng; dùng tốt trên điện thoại.
- [ ] Không có khóa bí mật trong giao diện; dữ liệu có cách sao lưu.
- [ ] Có hướng dẫn chạy (macOS + Windows) và hướng dẫn sử dụng tiếng Việt.
- [ ] Có danh sách việc để sau và giới hạn.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** viết 3–5 câu mô tả việc bạn đang làm tay mỗi ngày mà muốn app làm giúp; nếu có file Excel đang dùng, chuẩn bị sẵn để gửi;
nghĩ trước ai sẽ dùng app.

1. Gõ `/ts-tao-app` kèm 1 câu mô tả ý tưởng (vd "app tính giá bánh theo size và topping cho nhân viên dùng trên điện thoại").
2. Trả lời tối đa 8 câu hỏi — chỉ cần gõ chữ A, B, C hoặc D.
3. Đọc **đặc tả 1 trang**. Đặc biệt xem nhóm "Bắt buộc": ít thôi để có app nhanh. Gõ "duyệt đặc tả".
4. AI xây từng phần. Sau mỗi phần, mở thử và nói cảm nhận: "nút to hơn", "thêm ô ghi chú", "đổi màu cam".
5. Thử nhập sai, để trống, dùng trên điện thoại — thấy lỗi thì chụp màn hình gửi AI.
6. Nhận file app + hướng dẫn. Lưu file vào thư mục dễ tìm; nhớ bấm **Xuất dữ liệu** định kỳ để sao lưu.
7. Gõ **"duyệt"** để AI lưu đặc tả và hướng dẫn vào Bộ Não (lần sau nâng cấp app, AI biết app đang có gì).

## Câu lệnh mẫu
- `/ts-tao-app máy tính báo giá bánh kem theo size, cốt bánh, topping cho tiệm bánh Mây, có nút copy báo giá gửi khách`
- `/ts-tao-app app điểm danh học viên khóa quay video bằng điện thoại, mỗi buổi tick có mặt, cuối khóa xuất Excel`
- `/ts-tao-app form đặt lịch cho spa Hồng: khách chọn dịch vụ, ngày giờ, để lại số điện thoại, tôi xem danh sách lịch`
- `/ts-tao-app CRM mini cho shop online: lưu khách, trạng thái tư vấn, nhắc khách cần gọi lại hôm nay`

## Kết quả nhận được
- Đặc tả 1 trang (mục tiêu, vai trò, tính năng chia 3 nhóm, luồng, dữ liệu, màn hình, giới hạn, tiêu chí hoàn thành).
- Ứng dụng chạy được (thường 1 file HTML) với dữ liệu mẫu, giao diện tiếng Việt, dùng được trên điện thoại.
- Hướng dẫn chạy (macOS + Windows) và hướng dẫn sử dụng.
- Danh sách việc để sau, phần chưa làm, giới hạn kỹ thuật và cách bảo trì.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-tao-app-<chu-de-khong-dau>/`.
2. Lưu đặc tả app đã duyệt (mục tiêu, tính năng, dữ liệu, cách chạy, giới hạn, việc để sau) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-tao-app
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd app, cong-cu-noi-bo, bao-gia>]
   ---
   ```
   Kèm theo các file phụ (nếu có): mã nguồn app (vd `app/index.html`), `HUONG-DAN.md`. Không lưu khóa API hay dữ liệu khách thật.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-tao-app · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Đề xuất tạo trang dự án `05-du-an/app-<ten-app>.md` để theo dõi các lần nâng cấp — hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không nhúng khóa bí mật (API key, token) vào giao diện. Không xin mật khẩu trong chat.
- Không thêm thanh toán, đăng nhập phức tạp hoặc nền tảng trả phí nếu chưa được duyệt.
- App thu thập dữ liệu khách (tên, số điện thoại) → chỉ thu đúng thứ cần, nói rõ cho khách mục đích sử dụng, có cách xóa dữ liệu.
- Dữ liệu lưu trên trình duyệt có thể mất → luôn có nút sao lưu và nhắc người dùng.
- Không chạy lệnh cài đặt, xóa file trên máy người dùng khi chưa hỏi.
- App do AI tạo phù hợp công cụ nhỏ/nội bộ; hệ thống lớn, có tiền, có dữ liệu nhạy cảm nên nhờ lập trình viên rà soát.

## Skill liên quan
- Trước: `/ts-bang-tinh-excel` (nếu đang quản lý bằng Excel) · Sau: `/ts-dua-web-len-mang`, `/ts-ket-noi-ung-dung`, `/ts-bao-don-telegram`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
