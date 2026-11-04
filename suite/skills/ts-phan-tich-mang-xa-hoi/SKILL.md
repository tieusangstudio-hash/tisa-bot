---
name: ts-phan-tich-mang-xa-hoi
description: "Gọi bằng /ts-phan-tich-mang-xa-hoi. Đọc và phân tích số liệu Facebook, Instagram, TikTok, YouTube, Zalo OA từ ảnh chụp, file xuất hoặc số bạn dán: tính tỉ lệ tương tác, lưu, chia sẻ, xem hết video, so với kỳ trước, tìm bài thắng, giờ đăng tốt, khâu yếu nhất, rồi ra 3 việc nên làm tuần này. Giải thích từng chỉ số bằng lời dễ hiểu. Từ khóa: phân tích fanpage, số liệu TikTok, insights Facebook, báo cáo mạng xã hội, tỉ lệ tương tác, bài nào hiệu quả, kênh không tăng."
---

# /ts-phan-tich-mang-xa-hoi — Xem số liệu mạng xã hội & biết nên làm gì

> Đưa AI ảnh chụp hoặc file số liệu kênh của bạn. AI tính các chỉ số quan trọng, **giải thích bằng lời dễ hiểu**,
> chỉ ra bài nào thắng, khâu nào đang yếu, và kết thúc bằng **3 việc nên làm trong tuần này** — không chỉ là bảng số.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Xem lại tuần/tháng: kênh đang lên hay xuống, bài nào hiệu quả nhất.
- Muốn biết nên đăng dạng gì, giờ nào, chủ đề nào nhiều hơn.
- So sánh Facebook với TikTok (hoặc Instagram, YouTube) để dồn sức đúng kênh.
- Đánh giá một chiến dịch/đợt đăng bài: trước – trong – sau.
- Kênh "đứng hình", nhiều view mà không ra đơn — cần tìm chỗ nghẽn.

**Không dùng khi:** cần báo cáo **quảng cáo** Facebook (chi phí, CPA, ROAS) → `/ts-bao-cao-facebook-ads`; cần số **doanh thu, đơn hàng**
→ `/ts-phan-tich-doanh-thu`; nghiên cứu kênh **người khác** → `/ts-phan-tich-doi-thu` hoặc `/ts-nghien-cuu-youtube`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

(Nếu có Bộ Não, được phép mở thêm báo cáo kỳ trước trong `04-ket-qua/…-phan-tich-mang-xa-hoi-…/` để so sánh.)

## Quy trình AI thực hiện

### Bước 1 — Hỏi rõ (1 lượt)
Theo `references/_chung/clarification-gate.md`:
1. Kênh nào? A. Facebook · B. Instagram · C. TikTok · D. YouTube · E. Zalo OA (chọn nhiều được).
2. Khoảng thời gian? (7 ngày / 28–30 ngày / 90 ngày) và có số kỳ trước để so không?
3. Mục tiêu chính của kênh? A. Nhiều người biết · B. Tương tác, cộng đồng · C. Khách nhắn tin/bấm link · D. Ra đơn.
4. Có chạy quảng cáo trong kỳ không? (để tách số tự nhiên và số trả tiền)
5. Có sự kiện đặc biệt không? (lễ, khuyến mãi, video "nổ" bất ngờ)

### Bước 2 — Nhận số liệu
Cách nhận (ưu tiên theo thứ tự):
- **Ảnh chụp màn hình** trang thống kê → AI đọc số (đọc không rõ thì hỏi lại, không đoán).
- **File xuất** CSV/Excel từ Meta Business Suite, TikTok, YouTube Studio → AI đọc trực tiếp.
- **Dán số** theo mẫu nhanh (trong `references/platform-insights-reading-guide.md`, mục "Universal Data Paste Templates").
- **Kết nối có sẵn** (nếu môi trường đã kết nối công cụ mạng xã hội/Meta) → chỉ **đọc** số, không đăng hay sửa gì.
Đường vào trang thống kê từng nền tảng, cách xuất file: `references/platform-insights-reading-guide.md`.

Ghi rõ nguồn và thời gian của số liệu ở đầu báo cáo. Thiếu số nào để trống, không tự điền.

### Bước 3 — Tính chỉ số (giải thích bằng lời thường)
| Chỉ số | Cách tính | Nói dễ hiểu |
|---|---|---|
| Tỉ lệ tương tác (ER) | Tổng tương tác ÷ Người tiếp cận × 100 | 100 người thấy, mấy người thả tim/bình luận/chia sẻ |
| ER theo người theo dõi | Tổng tương tác ÷ Người theo dõi × 100 | Người hâm mộ có còn "nhiệt" không |
| Tỉ lệ tiếp cận tự nhiên | Tiếp cận tự nhiên ÷ Người theo dõi × 100 | Đăng bài thì mấy % người theo dõi thấy |
| Tăng người theo dõi | (Mới − Bỏ theo dõi) ÷ Tổng × 100 | Kênh lớn lên nhanh hay chậm |
| Tỉ lệ lưu | Lưu ÷ Tiếp cận × 100 | Bài có đáng giữ lại xem sau không (dấu hiệu nội dung giá trị) |
| Tỉ lệ chia sẻ | Chia sẻ ÷ Tiếp cận × 100 | Người xem có muốn khoe với bạn bè không |
| Tỉ lệ bấm (CTR) | Lượt bấm ÷ Lượt hiển thị × 100 | Cứ 100 lần hiện, mấy lần được bấm |
| Tỉ lệ xem hết | Lượt xem hết ÷ Tổng lượt xem × 100 | Video giữ chân người xem tới cuối không |
| Thời gian xem trung bình | Tổng thời gian xem ÷ Lượt xem | Trung bình người ta xem được bao lâu |

Công thức đầy đủ, nhóm chỉ số "phù phiếm" vs "ra quyết định", ví dụ tính: `references/social-kpi-framework.md`.
**Về mốc chuẩn ngành:** số mốc trong file tham khảo là mức chung, có thể cũ — ưu tiên so với **chính kênh kỳ trước**.
Cần mốc ngành cụ thể thì tìm số liệu thật theo `references/_chung/data-sourcing-protocol.md` (ghi nguồn + ngày).

### Bước 4 — Phân tích
1. **Tổng quan:** tăng/giảm so với kỳ trước (%), kèm 1 câu giải thích.
2. **Top 3 bài thắng & 3 bài yếu:** theo chỉ số khớp mục tiêu (mục tiêu D → xem bấm link/nhắn tin, không chỉ view).
   Rút ra điểm chung: dạng (video/ảnh/nhiều ảnh), độ dài, chủ đề, câu mở đầu, giờ đăng.
3. **Giờ & ngày đăng tốt** của chính kênh (nếu có dữ liệu theo giờ).
4. **So sánh kênh** (nếu nhiều nền tảng): kênh nào đáng dồn sức.
5. **Khâu yếu nhất & 3 việc tuần này:** theo `references/tu-so-lieu-den-hanh-dong.md` — đi từ tiếp cận → tương tác → bấm →
   trang đích → thanh toán → mua lại; khâu yếu đầu tiên là chỗ sửa trước. Mỗi việc cụ thể, đo được, kèm lệnh `/ts-…` hỗ trợ.

### Bước 5 — Trình báo cáo (CỔNG DUYỆT)
Theo mẫu `templates/mau-bao-cao-mang-xa-hoi.md` (rút gọn theo nhu cầu), luôn có 3 phần cuối:
```
📊 Chuyện gì đang xảy ra   (2–3 câu)
🔍 Khâu yếu nhất           (1 khâu + vì sao)
✅ Làm trong tuần này       (3 việc + lệnh /ts-… hỗ trợ)
```
> "Bạn muốn xem sâu bài nào, hay so thêm kỳ khác? Gõ **duyệt** để lưu báo cáo vào Bộ Não."

### Checklist chất lượng
- [ ] Ghi nguồn số liệu (ảnh/file/kết nối) và khoảng thời gian; so sánh cùng độ dài kỳ (7 ngày với 7 ngày).
- [ ] Không bịa số, không tự điền số thiếu; số đọc từ ảnh không chắc thì đánh dấu `(?)` và hỏi lại.
- [ ] Tách số tự nhiên và số quảng cáo nếu có.
- [ ] Mỗi chỉ số có 1 câu giải thích dễ hiểu; không dùng thuật ngữ không giải thích.
- [ ] Kết thúc bằng đúng 3 việc cụ thể, không phải danh sách 10 việc chung chung.
- [ ] Không kết luận "vì A nên B" khi chỉ thấy hai thứ cùng tăng — ghi "có thể".

### Ví dụ minh họa (số liệu giả định)
*Tiệm bánh Mây*, TikTok 28 ngày: 120.000 lượt xem, tỉ lệ xem hết 18% (kỳ trước 26%), 3 video "trước – sau khi nướng" có tỉ lệ lưu 4%.
→ **Khâu yếu: giữ chân người xem** (video dài 60–90 giây, 5 giây đầu là logo). **Tuần này:** (1) cắt 3 video mới còn 20–30 giây,
mở đầu bằng cảnh bánh nở → `/ts-kich-ban-reels`; (2) làm thêm 2 video dạng "trước – sau"; (3) ghim video lưu nhiều nhất, thêm link đặt bánh.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị số liệu (5 phút) — chọn 1 cách:**
- **Facebook:** vào Meta Business Suite (`business.facebook.com`) → **Thông tin chi tiết / Insights** → chọn khoảng thời gian →
  chụp màn hình phần Tổng quan và Nội dung (hoặc bấm **Xuất dữ liệu / Export**).
- **TikTok:** app TikTok → **Hồ sơ** → biểu tượng ☰ → **Công cụ cho nhà sáng tạo / Business Suite** → **Số liệu phân tích** →
  chụp các tab Tổng quan, Nội dung, Người theo dõi. (Trên máy tính: TikTok Studio có nút tải dữ liệu.)
- **YouTube:** YouTube Studio → **Số liệu phân tích** → **Nâng cao** → **Xuất**.
- **Instagram:** hồ sơ → **Bảng điều khiển chuyên nghiệp** → **Thông tin chi tiết**.
Tên mục có thể khác theo phiên bản app — chụp màn hình gửi AI nếu không thấy.

1. Gõ `/ts-phan-tich-mang-xa-hoi` kèm kênh + khoảng thời gian, gửi kèm ảnh/file.
2. Trả lời câu hỏi mục tiêu (chọn A-B-C-D).
3. Đọc báo cáo: phần "Chuyện gì đang xảy ra" và "3 việc tuần này" là quan trọng nhất.
4. Hỏi thêm bằng lời: "vì sao video số 2 nhiều view mà ít đơn?", "so với tháng trước thì sao?".
5. Gõ **duyệt** để lưu; tuần sau chạy lại để so sánh tiến bộ.
6. Làm 3 việc đã đề xuất bằng các lệnh `/ts-…` AI gợi ý.

## Câu lệnh mẫu
- `/ts-phan-tich-mang-xa-hoi phân tích TikTok 28 ngày qua của tiệm bánh, tôi gửi kèm 3 ảnh chụp số liệu.`
- `/ts-phan-tich-mang-xa-hoi fanpage spa Hồng tháng này nhiều người xem mà ít nhắn tin, tìm chỗ yếu giúp tôi.`
- `/ts-phan-tich-mang-xa-hoi so sánh Facebook và TikTok của kênh dạy quay video bằng điện thoại, nên dồn sức vào kênh nào?`
- `/ts-phan-tich-mang-xa-hoi đọc file xuất YouTube Studio này, cho tôi biết video nào giữ chân người xem tốt nhất.`

## Kết quả nhận được
- Bảng chỉ số chính kỳ này so với kỳ trước, mỗi chỉ số có giải thích dễ hiểu.
- Top 3 bài thắng / 3 bài yếu và điểm chung rút ra; giờ đăng tốt của kênh.
- So sánh kênh (nếu nhiều nền tảng).
- Khâu yếu nhất trong phễu + **3 việc làm trong tuần**, kèm lệnh `/ts-…` hỗ trợ.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-phan-tich-mang-xa-hoi-<chu-de-khong-dau>/`.
2. Lưu báo cáo đã duyệt (nguồn số liệu, kỳ phân tích, bảng chỉ số, bài thắng/yếu, khâu yếu, 3 việc tuần này) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-phan-tich-mang-xa-hoi
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `so-lieu.csv` (bảng số đã chuẩn hóa để kỳ sau so sánh), ảnh chụp số liệu gốc.
   Không lưu mật khẩu, mã đăng nhập hay token kết nối.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-phan-tich-mang-xa-hoi · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Mẫu bài thắng (dạng, độ dài, câu mở đầu, giờ đăng) có thể lưu thêm vào `02-kien-thuc/cong-thuc/bai-thang-mang-xa-hoi.md` để các skill viết nội dung dùng lại (hỏi trước khi ghi).
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Không bịa số liệu**, không "làm tròn cho đẹp". Thiếu → để trống hoặc `[CẦN BỔ SUNG]`.
- Chỉ **đọc** số liệu; không đăng, xóa, ẩn bài hay sửa trang khi chưa được yêu cầu và chưa được "duyệt".
- Không xin mật khẩu, mã OTP, token đăng nhập trong chat. Ảnh chụp có thông tin khách (tên, số điện thoại) → che trước khi gửi.
- Số liệu nền tảng có độ trễ 24–48 giờ và có thể làm tròn — ghi chú khi so sánh.
- Tương quan không phải nguyên nhân: viết "có thể do…" thay vì khẳng định chắc chắn.

## Skill liên quan
- Trước: `/ts-lich-noi-dung` · `/ts-noi-dung-tu-dong-7-ngay` · `/ts-cham-soc-fanpage`
- Sau: `/ts-kich-ban-reels` · `/ts-viet-bai-ban-hang` · `/ts-chien-luoc-marketing` · `/ts-phan-tich-doanh-thu`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
