---
name: ts-tu-dong-hoa-meta
description: "Gọi bằng /ts-tu-dong-hoa-meta. Thiết kế và vận hành tự động hóa Facebook/Instagram qua kết nối chính thức, chia 4 luồng ĐỌC, BẢN NHÁP, XUẤT BẢN, QUẢNG CÁO: lấy số liệu, báo cáo và cảnh báo định kỳ, soạn và hẹn bài, thao tác chiến dịch có giới hạn và cổng duyệt. Dùng khi muốn tự động đăng bài, báo cáo ads mỗi sáng, cảnh báo chi phí tăng. Từ khóa: tự động hóa facebook, API facebook, tự động đăng bài, hẹn giờ đăng, báo cáo ads tự động, cảnh báo quảng cáo, quy tắc tự động, Meta Business Suite."
---

# /ts-tu-dong-hoa-meta — Tự động hóa Facebook, Instagram và quảng cáo Meta

> Giúp bạn để AI làm thay các việc lặp lại trên Fanpage, Instagram và quảng cáo Meta một cách an toàn:
> đọc số, báo cáo, cảnh báo, soạn và hẹn bài, điều chỉnh quảng cáo trong giới hạn đã duyệt.
> Kết quả: sơ đồ luồng tự động, quyền cần cấp, lịch chạy, quy tắc cảnh báo và sổ tay xử lý sự cố.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Muốn mỗi sáng nhận báo cáo quảng cáo hôm qua mà không phải mở Ads Manager.
- Muốn được cảnh báo khi chi phí/kết quả tăng vọt hoặc quảng cáo tiêu tiền mà không ra kết quả.
- Muốn AI soạn sẵn bài và hẹn giờ đăng lên Fanpage/Instagram sau khi duyệt.
- Muốn quy tắc tự động: tạm dừng quảng cáo khi vượt ngưỡng, có giới hạn rõ.
- Muốn biết luồng nào nên tự động, luồng nào phải có người duyệt.

**Không dùng khi:** chỉ cần đọc báo cáo một lần → `/ts-bao-cao-facebook-ads`; lên chiến dịch mới → `/ts-len-camp-facebook`;
chưa kết nối Facebook với AI → làm `/ts-ket-noi-ung-dung` trước; chỉ cần lịch nhắc việc → `/ts-lap-lich-tu-dong`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `04-thuong-hieu-noi-dung.md` (giọng văn, mẫu bài), `05-muc-tieu-quy-tac-lien-he.md` (tên Fanpage/Instagram, tài khoản quảng cáo, KPI, ngân sách, kênh nhận báo cáo, người duyệt);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `tu-dong-hoa-meta`, `ket-noi-ung-dung`, `bao-cao-facebook-ads` hoặc từ khóa) để biết luồng nào đã cài, kết nối nào đã có.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Xác định việc cần tự động
Hỏi phần còn thiếu (gợi ý A-B-C-D):
- Muốn tự động việc gì? (A) Báo cáo quảng cáo định kỳ · (B) Cảnh báo khi chỉ số xấu · (C) Soạn và hẹn đăng bài · (D) Điều chỉnh quảng cáo theo quy tắc.
- Trên Page/Instagram/tài khoản quảng cáo nào (lấy tên từ hồ sơ, hỏi xác nhận).
- Chạy khi nào: giờ cố định (vd 8:00 mỗi sáng) hay khi có điều kiện (vd chi phí vượt ngưỡng).
- Kết quả gửi về đâu: chat với AI, email, Telegram, Google Sheets.
- Ai duyệt: tên người, duyệt bằng cách nào (gõ "duyệt" trong chat, đánh dấu trong Sheets…).

### Bước 2 — Kiểm tra kết nối và quyền
Ưu tiên công cụ kết nối chính thức đang có trong môi trường (kết nối Meta Ads, Facebook Pages, Meta Business Suite).
- Chưa kết nối → dừng và chuyển `/ts-ket-noi-ung-dung`; hoặc dùng cách không cần code ở Bước 6.
- Đã kết nối → liệt kê tài sản AI nhìn thấy: Business, Page, Instagram, tài khoản quảng cáo, **múi giờ, tiền tệ, ID**. Đọc lại cho người dùng xác nhận đúng tài sản.
- Quyền tối thiểu theo luồng: ĐỌC chỉ cần quyền đọc số liệu/nội dung; XUẤT BẢN cần quyền quản lý bài viết; QUẢNG CÁO cần quyền quản lý quảng cáo. Không xin quyền thừa.
- Kiểm tra phiên bản API hiện hành, giới hạn số lần gọi (rate limit), thời hạn kết nối (token có thể hết hạn).

### Bước 3 — Tách 4 luồng và mức kiểm soát
| Luồng | Làm gì | Ví dụ | Mức tự động cho phép |
|---|---|---|---|
| `ĐỌC` | Lấy số liệu, bài viết, bình luận, thông tin Page | Báo cáo ads 8:00 mỗi sáng; tổng hợp bình luận tuần | Tự chạy trong phạm vi đã duyệt |
| `BẢN NHÁP` | Soạn bài, chú thích, câu trả lời, đề xuất tối ưu | Soạn 7 bài tuần sau vào tối Chủ nhật | Tự chạy, **không công khai** |
| `XUẤT BẢN` | Đăng/hẹn giờ bài, trả lời bình luận | Đăng bài đã duyệt lúc 19:00 | Cần mẫu, Page, lịch và quy tắc duyệt rõ |
| `QUẢNG CÁO` | Tạo/bật/tắt, đổi ngân sách, đối tượng, creative | Tạm dừng quảng cáo vượt ngưỡng | Cần giới hạn cụ thể + xác nhận |

Không bao giờ tự động: xóa dữ liệu (bài, bình luận, quảng cáo, đối tượng), thay phương thức thanh toán, đổi quyền quản trị.

### Bước 4 — Thiết kế luồng chi tiết
Mỗi luồng ghi rõ: **kích hoạt** (giờ/điều kiện) → **dữ liệu vào** → **việc làm** → **dữ liệu ra** → **nơi nhận** → **người duyệt** → **cách dừng**.

**Ví dụ quy tắc cảnh báo** (tiệm bánh Mây — giả định; ngưỡng lấy từ KPI trong hồ sơ):
| Tên quy tắc | Điều kiện (kiểm tra mỗi ngày 9:00 và 15:00) | Hành động |
|---|---|---|
| Tiêu tiền không ra kết quả | Chi hôm nay ≥ 2 × CPA mục tiêu và 0 kết quả | Gửi cảnh báo + đề xuất tạm dừng (chờ duyệt) |
| Chi phí tăng vọt | Chi phí/kết quả 3 ngày gần nhất > 1,5 × trung bình 7 ngày trước | Gửi cảnh báo + gợi ý nguyên nhân |
| Quảng cáo mỏi | Tần suất 7 ngày > 3 và CTR giảm > 30% so với tuần trước | Đề xuất làm creative mới |
| Chi vượt ngân sách | Tổng chi tháng > 90% ngân sách tháng | Cảnh báo cho chủ doanh nghiệp |
| Không phân phối | Chiến dịch đang bật nhưng chi = 0 trong 24 giờ | Kiểm tra bị từ chối/thanh toán |

**Ví dụ luồng XUẤT BẢN:** Chủ nhật 20:00 AI soạn 7 bài (BẢN NHÁP) → gửi bảng duyệt → người dùng đánh dấu "duyệt" từng bài
→ AI hẹn giờ đăng đúng lịch → sau khi đăng, AI đọc lại để xác nhận bài đã lên → ghi nhật ký.

**Ví dụ luồng QUẢNG CÁO có giới hạn:** "Được tự tạm dừng quảng cáo khi chi ≥ 2 × CPA mục tiêu mà 0 kết quả;
mỗi ngày tối đa 3 lần; không được tăng ngân sách; báo ngay sau khi làm." Mọi việc ngoài giới hạn → hỏi trước.

Độ tin cậy kỹ thuật (AI tự lo khi cài, giải thích ngắn cho người dùng):
- Xử lý dữ liệu nhiều trang (pagination) để không thiếu chiến dịch.
- Chống đăng trùng: mỗi bài có mã riêng, kiểm tra đã đăng chưa trước khi đăng (idempotency).
- Thử lại có giới hạn khi lỗi mạng (vd tối đa 3 lần), tôn trọng giới hạn số lần gọi.
- Tách thử nghiệm và chạy thật: thử trên bài nháp, Page thử hoặc quảng cáo ngân sách nhỏ trước.

### Bước 5 — Chạy thử theo thứ tự an toàn
1. **Thử chỉ đọc**: lấy thông tin Page hoặc số liệu quảng cáo 7 ngày; đối chiếu với số người dùng thấy trong Ads Manager.
2. **Thử bản nháp**: tạo 1 bài nháp/1 báo cáo mẫu gửi về kênh nhận.
3. **Thử thay đổi nhỏ có thể hoàn tác**: hẹn 1 bài ở chế độ chỉ mình tôi/Page thử, hoặc tạm dừng rồi bật lại 1 quảng cáo thử — chỉ khi người dùng đồng ý.
4. Báo kết quả từng bước, có bằng chứng (ảnh, link, số liệu khớp).

### Bước 6 — Cách không cần code (khi chưa có kết nối)
- **Meta Business Suite → Lập lịch / Planner**: hẹn giờ đăng bài Facebook và Instagram (AI soạn sẵn nội dung và giờ đăng).
- **Ads Manager → Quy tắc tự động** (Automated Rules, nằm trong menu công cụ của Ads Manager): tự tạm dừng/gửi thông báo khi đạt điều kiện. AI viết sẵn từng quy tắc: áp dụng cho, hành động, điều kiện, khung thời gian, lịch kiểm tra, thông báo.
- **Báo cáo đã lên lịch** trong Ads Manager (nếu tài khoản có): gửi email báo cáo định kỳ.
- Lịch nhắc người dùng tự mở báo cáo → `/ts-lap-lich-tu-dong`.

### Bước 7 — Cổng duyệt và bật luồng
Trình bản tổng hợp: sơ đồ kết nối, danh sách quyền tối thiểu, các luồng + mức tự động, quy tắc cảnh báo, lịch chạy
và 3 lần chạy kế tiếp, cách tạm dừng/xóa. Chờ người dùng gõ **"duyệt"** cho **từng luồng**. Luồng QUẢNG CÁO cần xác nhận thêm:
tài khoản nào, giới hạn tiền, giới hạn số lần.

### Bước 8 — Nhật ký và sổ tay sự cố
- Mỗi lần chạy ghi: thời gian, luồng, hành động, đối tượng (tên chiến dịch/bài), kết quả, lỗi. **Không ghi token, mật khẩu.**
- Sổ tay sự cố: kết nối hết hạn (kết nối lại qua `/ts-ket-noi-ung-dung`), bị thu hồi quyền, đăng lỗi (thử lại 1 lần rồi báo),
  đăng nhầm (ẩn bài, báo người dùng), quảng cáo bị tạm dừng nhầm (bật lại sau khi người dùng xác nhận).
- Khi kết nối không khả dụng: chuyển sang hướng dẫn thao tác tay, **không giả vờ đã thực hiện**.

### Checklist chất lượng trước khi giao
- [ ] Đã xác nhận đúng Page, Instagram, Business, tài khoản quảng cáo, múi giờ, tiền tệ.
- [ ] Mỗi luồng gắn đúng nhãn ĐỌC / BẢN NHÁP / XUẤT BẢN / QUẢNG CÁO và mức tự động.
- [ ] Quy tắc cảnh báo có ngưỡng lấy từ KPI thật, không đoán.
- [ ] Đã chạy thử chỉ đọc và số liệu khớp với Ads Manager.
- [ ] Có cách tạm dừng/xóa từng luồng; nhật ký không chứa thông tin bí mật.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** quyền quản trị Fanpage và tài khoản quảng cáo; Facebook đã liên kết Instagram (nếu dùng);
KPI (chi phí/kết quả mong muốn, ngân sách tháng); nơi muốn nhận báo cáo (email/Telegram/chat).

1. Nếu chưa kết nối Facebook/Meta Ads với AI, gõ `/ts-ket-noi-ung-dung kết nối Facebook và quảng cáo Meta` và làm xong trước.
2. Gõ `/ts-tu-dong-hoa-meta` kèm 1 câu: muốn tự động việc gì (vd "báo cáo ads mỗi sáng 8 giờ").
3. Trả lời câu hỏi AI (chọn chữ cái A-B-C-D). Khi AI đọc tên Page/tài khoản quảng cáo, kiểm tra kỹ có đúng của mình không.
4. Xem bảng 4 luồng. Luồng nào bạn chưa yên tâm thì nói "chỉ để bản nháp, tôi tự đăng".
5. Cho AI chạy thử chỉ đọc; mở Ads Manager so số liệu xem có khớp không.
6. Gõ **"duyệt"** cho từng luồng muốn bật. Với luồng quảng cáo, nói rõ giới hạn (vd "chỉ được tạm dừng, không được tăng tiền").
7. Chưa kết nối được? Nhờ AI viết sẵn **Quy tắc tự động** trong Ads Manager và lịch đăng trong Meta Business Suite để bạn tự dán vào.

## Câu lệnh mẫu
- `/ts-tu-dong-hoa-meta mỗi sáng 8 giờ gửi tôi báo cáo quảng cáo hôm qua của shop giày, kèm cảnh báo nếu chi phí/đơn quá 100k`
- `/ts-tu-dong-hoa-meta tự soạn 5 bài/tuần cho Fanpage spa Hồng, tôi duyệt xong thì hẹn giờ đăng 19:00`
- `/ts-tu-dong-hoa-meta tạo quy tắc tự tạm dừng quảng cáo khóa học quay video khi tiêu 150k mà không có lead`
- `/ts-tu-dong-hoa-meta tôi chưa biết code, hướng dẫn cài quy tắc tự động trong Ads Manager cho tiệm bánh Mây`

## Kết quả nhận được
- Sơ đồ kết nối (hệ thống nào → quyền gì → làm gì → gửi về đâu).
- Danh sách quyền tối thiểu theo từng luồng.
- Bảng luồng tự động (ĐỌC / BẢN NHÁP / XUẤT BẢN / QUẢNG CÁO) kèm lịch chạy và người duyệt.
- Bộ quy tắc cảnh báo với ngưỡng cụ thể.
- Mẫu dữ liệu đã ẩn thông tin bí mật, sổ tay xử lý sự cố, cách tạm dừng/xóa từng luồng.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-tu-dong-hoa-meta-<chu-de-khong-dau>/`.
2. Lưu thiết kế tự động hóa đã duyệt (sơ đồ, luồng, quyền, quy tắc cảnh báo, lịch chạy, sổ tay sự cố) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-tu-dong-hoa-meta
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd tu-dong-hoa, meta, canh-bao>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `quy-tac-canh-bao.md`, `nhat-ky-chay.md` (không chứa token).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-tu-dong-hoa-meta · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Đề xuất tạo trang theo dõi trong `05-du-an/tu-dong-hoa-meta.md` (luồng nào đang bật, ngày bật, người duyệt, cách tắt). Chỉ ghi tên kết nối, quyền, ngày — tuyệt đối không ghi token/mật khẩu. Hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Tự động báo cáo/cảnh báo chỉ trong phạm vi đã duyệt. Đăng bài cần mẫu, Page, lịch và quy tắc duyệt rõ.
- Tạo/bật/tắt quảng cáo, thay ngân sách/đối tượng/creative cần giới hạn và xác nhận cụ thể.
- Không tự xóa dữ liệu hoặc thay thanh toán. Không xin mật khẩu, OTP, token trong chat.
- Mỗi lần chạy ghi thời gian, hành động, đối tượng, kết quả và lỗi — không ghi token.
- Khi API/kết nối không khả dụng, chuyển sang hướng dẫn chứ không giả vờ đã thực hiện.
- Tuân thủ chính sách nền tảng của Meta (giới hạn nhắn tin, nội dung quảng cáo); tự động hóa sai có thể làm khóa tài khoản.

## Skill liên quan
- Trước: `/ts-ket-noi-ung-dung`, `/ts-bao-cao-facebook-ads` · Sau: `/ts-lap-lich-tu-dong`, `/ts-cham-soc-fanpage`, `/ts-len-camp-facebook`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
