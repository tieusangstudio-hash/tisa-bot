# Danh mục đầy đủ 52 lệnh /ts-... (chia 5 giai đoạn)

Mỗi dòng: **lệnh** — làm gì · *Đầu vào* · *Đầu ra*. Hầu hết lệnh tự đọc hồ sơ trong `01-ho-so/` của
Bộ Não Thứ 2 nên đầu vào chỉ ghi phần **cần thêm**. Kết quả được lưu vào `04-ket-qua/` sau khi duyệt.

> Hai lệnh luôn đứng đầu: `/ts-cai-dat-bo-nao` (tạo Bộ Não) → `/ts-tao-ho-so-doanh-nghiep` (điền hồ sơ).
> Thiếu hồ sơ thì mọi lệnh khác vẫn chạy được nhưng phải hỏi nhiều hơn.

---

## Giai đoạn 1 — Nền tảng & chiến lược (14 lệnh)

| Lệnh | Làm gì | Đầu vào | Đầu ra |
|---|---|---|---|
| `/ts-cai-dat-bo-nao` | Tạo thư mục Bộ Não Thứ 2, kết nối vào AI, mở bằng Obsidian | Tên Bộ Não, nền tảng AI đang dùng | Thư mục Bộ Não đủ cấu trúc |
| `/ts-tao-ho-so-doanh-nghiep` | Phỏng vấn A-B-C-D, viết 5 tệp hồ sơ nền | Trả lời phỏng vấn, bảng giá, logo | 5 tệp trong `01-ho-so/` |
| `/ts-dieu-phoi-cong-viec` | Chọn đúng lệnh, lập quy trình nhiều bước, chạy sau khi duyệt | Mục tiêu bằng 1–2 câu | Kế hoạch quy trình + kết quả từng bước |
| `/ts-tao-skill` | Hỏi 5 câu, thiết kế và tạo skill mới theo nhu cầu riêng | Mô tả việc muốn tự động | Thư mục skill `ts-...` + hướng dẫn cài |
| `/ts-chien-luoc-marketing` | Chấm 3 chiến lược (đánh nhanh / dẫn dắt niềm tin / phễu quà), chọn 1, lập KPI | Mục tiêu doanh thu/lead, ngân sách | Chiến lược + lịch quý→ngày + bảng KPI |
| `/ts-chien-luoc-tang-truong` | Phân tích 6 đòn bẩy tăng trưởng, chọn 3 sáng kiến ưu tiên | Số liệu bán hàng hiện tại | Ma trận đòn bẩy + kế hoạch 30/60/90 ngày |
| `/ts-chan-dung-khach-hang` | Dựng chân dung khách, xếp hạng nỗi đau/mong muốn, gom cụm nội dung | Sản phẩm, câu khách hay hỏi | Chân dung + bảng nỗi đau + 3–5 cụm nội dung |
| `/ts-kiem-chung-ngach` | Đo nhu cầu thật của một ngách/ý tưởng, chấm điểm, ra quyết định làm/không | Ý tưởng ngách | Điểm ngách có bằng chứng + quyết định |
| `/ts-nghien-cuu-youtube` | Tìm video YouTube nhiều view theo chủ đề, lọc video vượt cỡ kênh | Chủ đề, ngưỡng view | Bảng video + chủ đề nên làm |
| `/ts-phan-tich-doi-thu` | Nghiên cứu đối thủ đa kênh, so giá – chất lượng – dịch vụ, content nổi bật | Tên đối thủ (nếu có), khu vực | Báo cáo Excel/Sheets 5 trang + khoảng trống |
| `/ts-mo-hinh-kinh-doanh` | Dựng mô hình kinh doanh 9 ô, tìm giả định rủi ro nhất | Ý tưởng/doanh nghiệp | Canvas 9 ô + việc cần kiểm chứng |
| `/ts-dinh-gia-offer` | Tính giá sàn/giá trần, bảng giá 3 tầng, đóng gói offer hấp dẫn | Chi phí, sản phẩm | Bảng giá 3 tầng + offer + bảo hành/quà |
| `/ts-ke-hoach-loi-nhuan` | Tính điểm hòa vốn, số đơn cần bán, dự toán chi phí | Chi phí cố định/biến đổi, giá | Bảng dự toán + điểm hòa vốn |
| `/ts-thiet-ke-pheu` | Thiết kế phễu bậc thang 4 tầng, tính giá trị vòng đời khách (LTV) | Danh mục sản phẩm | Sơ đồ phễu + bảng LTV + lịch chăm sóc |

## Giai đoạn 2 — Nội dung, hình ảnh, video (14 lệnh)

| Lệnh | Làm gì | Đầu vào | Đầu ra |
|---|---|---|---|
| `/ts-pheu-qua-tang` | Dựng phễu quà tặng 0 đồng: chọn quà, đóng gói quà, trang nhận quà, chuỗi nuôi dưỡng | Sản phẩm chính | Quà hoàn chỉnh + trang + chuỗi tin + KPI |
| `/ts-xay-dung-fanpage` | Lập định vị, tên, giới thiệu, ảnh bìa, gói bài khởi động cho Fanpage | Hồ sơ, logo (nếu có) | Bảng thông tin Fanpage + 5 bài đầu + checklist |
| `/ts-lich-noi-dung` | Lập lịch đăng bài tuần/tháng theo mục tiêu | Mục tiêu tháng, kênh | Lịch nội dung + loại bài + CTA |
| `/ts-noi-dung-tu-dong-7-ngay` | Gợi ý, viết, thiết kế và đăng 7 bài Fanpage (đăng khi đã kết nối và duyệt) | Chủ đề tuần (tùy chọn) | 7 bài + ảnh/prompt ảnh + lịch đăng |
| `/ts-viet-bai-ban-hang` | Viết 5 dạng bài bán hàng: kéo tin nhắn, mở bán, trả lời băn khoăn, câu chuyện khách, so sánh gói | Sản phẩm, dạng bài | Bài đăng có CTA |
| `/ts-kich-ban-reels` | Kịch bản video ngắn 30–90 giây cho Reels/TikTok/Shorts | Chủ đề video | Kịch bản theo cảnh + caption + hashtag |
| `/ts-kich-ban-video-quang-cao` | Kịch bản quảng cáo 60/90/120 giây, 5 hook cho 5 tệp khách | Sản phẩm, thời lượng | Kịch bản + bảng cảnh + khối bàn giao |
| `/ts-prompt-video-ai` | Tách kịch bản thành cảnh 8 giây, viết prompt JSON cho công cụ video AI (không nhạc nền) | Kịch bản, ảnh nhân vật/sản phẩm | Prompt JSON từng cảnh, copy được |
| `/ts-dung-video` | Dựng reel từ video quay sẵn: cắt khoảng lặng, caption, đồ họa, zoom (chạy trên máy) | File video | Video hoàn chỉnh `out/final.mp4` |
| `/ts-thiet-ke-anh-quang-cao` | Concept + prompt + tạo ảnh quảng cáo đúng màu, logo thương hiệu | Sản phẩm, kênh, tỷ lệ | 2–4 concept, prompt từng ảnh, ảnh (nếu có công cụ) |
| `/ts-infographic` | Thiết kế infographic/ảnh kiến thức, xuất ảnh PNG | Chủ đề/nội dung | Ảnh infographic đúng nhận diện |
| `/ts-tao-ebook` | Soạn ebook có thương hiệu, xuất PDF làm quà/sản phẩm | Chủ đề ebook | Bản thảo + PDF |
| `/ts-thiet-ke-thuyet-trinh` | Lập mạch và thiết kế slide PowerPoint/Google Slides | Mục tiêu buổi trình bày | Bộ slide + ghi chú người nói |
| `/ts-cham-soc-fanpage` | Lịch nội dung, phân loại bình luận/inbox, gợi ý trả lời, FAQ | Bình luận/tin nhắn mẫu | Quy trình chăm sóc + câu trả lời mẫu |

## Giai đoạn 3 — Quảng cáo (6 lệnh)

| Lệnh | Làm gì | Đầu vào | Đầu ra |
|---|---|---|---|
| `/ts-viet-quang-cao` | Viết hook, tiêu đề, nội dung, CTA và ma trận test cho quảng cáo | Sản phẩm, kênh | Bộ mẫu quảng cáo + ma trận A/B |
| `/ts-len-camp-facebook` | Dựng chiến dịch Facebook (vd kéo tin nhắn) ở trạng thái tạm dừng, xem trước, bật sau khi duyệt | Nội dung + ảnh/video, ngân sách | Chiến dịch → nhóm QC → quảng cáo (tạm dừng) |
| `/ts-chay-tiktok-ads` | Lập kế hoạch, cấu trúc và tối ưu quảng cáo TikTok | Video, ngân sách, mục tiêu | Cấu trúc chiến dịch + KPI + hướng dẫn |
| `/ts-bao-cao-facebook-ads` | Đọc số liệu quảng cáo Meta, chẩn đoán, đề xuất tối ưu | File xuất/ảnh chụp/kết nối | Báo cáo chỉ số + việc nên làm |
| `/ts-tu-dong-hoa-meta` | Đăng/hẹn bài, lấy số liệu, cảnh báo chỉ số qua kết nối Meta chính thức | Kết nối Meta, quy tắc | Luồng tự động + báo cáo định kỳ |
| `/ts-doc-so-lieu-hinh-anh` | Đọc bảng số liệu, biểu đồ, ảnh chụp màn hình, phát hiện bất thường | Ảnh/file số liệu | Tóm tắt số liệu + đề xuất |

## Giai đoạn 4 — Chốt đơn, web, thu tiền (11 lệnh)

| Lệnh | Làm gì | Đầu vào | Đầu ra |
|---|---|---|---|
| `/ts-trang-ban-hang` | Viết trọn nội dung trang bán hàng 12 khối, phiếu dựng cho LadiPage/Canva/WordPress | Sản phẩm, offer | Nội dung trang copy-paste được |
| `/ts-landing-page` | Tạo trang landing page HTML hoàn chỉnh, chạy được ngay | Nội dung trang | File HTML + hướng dẫn xem thử |
| `/ts-dua-web-len-mang` | Đưa trang web lên mạng (Vercel…), có link thật, gắn tên miền | File web | Link web công khai |
| `/ts-cai-thanh-toan` | Hướng dẫn cài nhận tiền chuyển khoản tự động (VietQR qua SePay) | Tài khoản ngân hàng (không mật khẩu) | Cấu hình thanh toán + cách thử |
| `/ts-gan-ma-qr` | Gắn mã VietQR thanh toán vào trang bán hàng | Trang web, thông tin nhận tiền | Trang có mã QR tự cập nhật |
| `/ts-bao-don-telegram` | Có đơn/có lead thì báo về Telegram | Bot Telegram, nguồn đơn | Luồng thông báo hoạt động |
| `/ts-giao-hang-tu-dong` | Tự gửi sản phẩm số (email/link/Telegram) sau khi khách trả tiền | Sản phẩm số, nguồn thanh toán | Luồng giao hàng tự động |
| `/ts-xu-ly-tu-choi` | Soạn lời tư vấn, xử lý từ chối (chê đắt, để suy nghĩ…), câu chốt | Lời từ chối của khách | Kịch bản trả lời theo tình huống |
| `/ts-cham-soc-khach-zalo` | Viết tin chăm sóc khách tiềm năng qua Zalo/Messenger, nhắc lịch, follow-up | Nhóm khách, mục tiêu | Chuỗi tin nhắn theo ngày |
| `/ts-email-cham-soc` | Viết chuỗi email chào mừng, mở bán, nuôi dưỡng, xin cảm nhận | Sản phẩm, hành trình khách | Chuỗi email + lịch gửi |
| `/ts-soan-hop-dong` | Soạn hợp đồng, báo giá, biên bản, văn bản hành chính | Thông tin hai bên, điều khoản | File văn bản (DOCX/PDF) |

## Giai đoạn 5 — Đo lường & vận hành (7 lệnh)

| Lệnh | Làm gì | Đầu vào | Đầu ra |
|---|---|---|---|
| `/ts-phan-tich-doanh-thu` | Phân tích doanh thu, KPI, dự báo 30–90 ngày, tìm nguyên nhân giảm | File doanh thu/đơn hàng | Báo cáo + dự báo + việc cần làm |
| `/ts-phan-tich-mang-xa-hoi` | Phân tích hiệu quả Facebook/Instagram/TikTok/YouTube, giải thích dễ hiểu | Số liệu kênh | Báo cáo + việc làm tuần này |
| `/ts-bang-tinh-excel` | Tạo bảng tính, công thức, dashboard (CRM, thu chi, KPI) | Mô tả bảng cần | File Excel/Sheets |
| `/ts-lap-lich-tu-dong` | Tạo nhắc việc, tác vụ định kỳ (báo cáo hằng tuần, nhắc đăng bài) | Việc + thời gian | Lịch/tác vụ đã đặt (sau khi duyệt) |
| `/ts-ket-noi-ung-dung` | Kết nối AI với Facebook, Google, Telegram, Zalo… an toàn (không lưu mật khẩu) | Nền tảng cần kết nối | Kết nối đã kiểm tra + hướng dẫn |
| `/ts-tao-app` | Biến ý tưởng thành ứng dụng web nhỏ chạy được (vibe coding) | Ý tưởng app | App chạy được + hướng dẫn dùng |
| `/ts-tro-ly-may-tinh` | Đọc màn hình, hướng dẫn hoặc thao tác máy tính/trình duyệt khi được cấp quyền | Ảnh màn hình / việc cần làm | Thao tác đã làm hoặc hướng dẫn từng bước |

Tổng: 14 + 14 + 6 + 11 + 7 = **52 lệnh**.

---

## Quy tắc chọn lệnh

- **Thiếu hồ sơ → làm hồ sơ trước.** Chưa có Bộ Não → `/ts-cai-dat-bo-nao`; hồ sơ còn trống →
  `/ts-tao-ho-so-doanh-nghiep` (bản nhanh 10 phút là đủ để bắt đầu).
- **Chiến lược trước, sản xuất sau.** Chưa rõ hướng → `/ts-chien-luoc-marketing` hoặc
  `/ts-chien-luoc-tang-truong` trước khi viết bài, làm ảnh.
- **Đối thủ cụ thể → `/ts-phan-tich-doi-thu`; ý tưởng/ngách mới chưa chắc → `/ts-kiem-chung-ngach`.**
- **Tách tạo nội dung khỏi đăng/xuất bản.** Viết xong (giai đoạn 2) → duyệt → mới đăng (`/ts-noi-dung-tu-dong-7-ngay`,
  `/ts-tu-dong-hoa-meta`).
- **Tách đọc báo cáo khỏi thay đổi quảng cáo.** `/ts-bao-cao-facebook-ads` chỉ đọc; thay đổi thì qua
  `/ts-len-camp-facebook` hoặc `/ts-tu-dong-hoa-meta` sau khi duyệt.
- **Cần thao tác trên nền tảng ngoài** (Facebook, Telegram, Vercel…) → kiểm tra `/ts-ket-noi-ung-dung` trước.
- **Video:** có kịch bản + muốn video AI → `/ts-prompt-video-ai`; đã quay video thật → `/ts-dung-video`.
- **Trang web bán hàng:** nội dung `/ts-trang-ban-hang` → dựng `/ts-landing-page` → thu tiền `/ts-gan-ma-qr`
  → lên mạng `/ts-dua-web-len-mang`.
- Chọn **ít lệnh nhất** đạt được mục tiêu; không thêm bước "cho đủ bộ".

## Chuỗi đầu ra → đầu vào hay dùng

| Đầu ra của | Làm đầu vào cho |
|---|---|
| `/ts-chan-dung-khach-hang` (cụm nội dung) | `/ts-lich-noi-dung`, `/ts-viet-quang-cao`, `/ts-kich-ban-reels` |
| `/ts-dinh-gia-offer` (bảng giá, offer) | `/ts-trang-ban-hang`, `/ts-viet-bai-ban-hang`, `/ts-xu-ly-tu-choi` |
| `/ts-kich-ban-video-quang-cao` (khối `VIDEO_SCRIPT_HANDOFF`) | `/ts-prompt-video-ai` |
| `/ts-viet-quang-cao` + `/ts-thiet-ke-anh-quang-cao` | `/ts-len-camp-facebook`, `/ts-chay-tiktok-ads` |
| `/ts-trang-ban-hang` | `/ts-landing-page` → `/ts-gan-ma-qr` → `/ts-dua-web-len-mang` |
| `/ts-bao-cao-facebook-ads`, `/ts-phan-tich-doanh-thu` | `/ts-chien-luoc-tang-truong`, `/ts-viet-quang-cao` (làm mẫu mới) |
