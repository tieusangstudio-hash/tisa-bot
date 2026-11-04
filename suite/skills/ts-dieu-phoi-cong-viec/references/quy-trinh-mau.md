# 5 quy trình mẫu trọn gói

Dùng làm khung khi mục tiêu của người dùng giống một trong các mẫu dưới đây. Luôn **cắt bớt** bước
đã có kết quả trong Bộ Não (`04-ket-qua/`) hoặc bước người dùng không cần. Mỗi bước ghi: lệnh · đầu vào ·
đầu ra · điều kiện qua bước. `[DUYỆT]` = cổng người dùng phải nói "duyệt" trước khi làm tiếp.

Ví dụ trong ngoặc chỉ để minh họa, thay bằng thông tin thật của người dùng.

---

## Mẫu 1 — Ra mắt khóa học mới trong 30 ngày
*(vd "khóa học quay video bằng điện thoại", học phí 1,5 triệu, mục tiêu 40 học viên)*

| Tuần | Bước | Lệnh | Đầu ra | Điều kiện qua bước |
|---|---|---|---|---|
| 0 | 1 | `/ts-tao-ho-so-doanh-nghiep` (bản nhanh, nếu hồ sơ trống) | 5 tệp hồ sơ | Có giá, khách hàng, giọng văn |
| 1 | 2 | `/ts-chan-dung-khach-hang` | Chân dung + 3–5 cụm nội dung | `[DUYỆT]` chân dung |
| 1 | 3 | `/ts-dinh-gia-offer` | Bảng giá 3 tầng, quà, bảo hành, hạn ưu đãi | `[DUYỆT]` offer |
| 1 | 4 | `/ts-ke-hoach-loi-nhuan` | Số học viên cần để hòa vốn, ngân sách tối đa | Ngân sách hợp lý |
| 2 | 5 | `/ts-pheu-qua-tang` (quà: buổi học thử/ebook) | Quà + trang nhận quà + chuỗi nuôi dưỡng | `[DUYỆT]` quà |
| 2 | 6 | `/ts-trang-ban-hang` → `/ts-landing-page` | Trang bán khóa học | `[DUYỆT]` nội dung trang |
| 2 | 7 | `/ts-gan-ma-qr` + `/ts-bao-don-telegram` | Thu tiền + báo đơn | Thử 1 giao dịch nhỏ thành công |
| 2 | 8 | `/ts-dua-web-len-mang` | Link trang công khai | `[DUYỆT]` trước khi công khai |
| 3 | 9 | `/ts-lich-noi-dung` (30 ngày, nhịp: giáo dục → bằng chứng → mở bán) | Lịch bài | `[DUYỆT]` |
| 3 | 10 | `/ts-kich-ban-video-quang-cao` + `/ts-thiet-ke-anh-quang-cao` | Kịch bản + ảnh quảng cáo | `[DUYỆT]` creative |
| 3 | 11 | `/ts-len-camp-facebook` (tạm dừng, chờ bật) | Chiến dịch dựng sẵn | `[DUYỆT]` ngân sách + bật |
| 4 | 12 | `/ts-email-cham-soc` hoặc `/ts-cham-soc-khach-zalo` | Chuỗi nhắc mở bán, đếm ngược | `[DUYỆT]` trước khi gửi |
| 4 | 13 | `/ts-bao-cao-facebook-ads` (3 ngày/lần) → `/ts-phan-tich-doanh-thu` (cuối tháng) | Báo cáo + việc tối ưu | — |

KPI chính: lead/ngày, chi phí mỗi lead, tỷ lệ lead → học viên, doanh thu so mục tiêu.

## Mẫu 2 — Mở cửa hàng online từ con số 0
*(vd "tiệm bánh Mây" bán bánh kem giao trong thành phố)*

| Bước | Lệnh | Đầu ra | Điều kiện qua bước |
|---|---|---|---|
| 1 | `/ts-cai-dat-bo-nao` → `/ts-tao-ho-so-doanh-nghiep` | Bộ Não + hồ sơ | Hồ sơ đã duyệt |
| 2 | `/ts-phan-tich-doi-thu` (5–8 tiệm cùng khu vực) | Bảng giá – dịch vụ – content đối thủ + khoảng trống | Có ≥3 khoảng trống có nguồn |
| 3 | `/ts-dinh-gia-offer` | Bảng giá, combo, ưu đãi khai trương | `[DUYỆT]` |
| 4 | `/ts-xay-dung-fanpage` | Fanpage chuẩn + ảnh bìa + 5 bài đầu | `[DUYỆT]` trước khi đăng |
| 5 | `/ts-thiet-ke-anh-quang-cao` | Bộ ảnh sản phẩm/khai trương | `[DUYỆT]` |
| 6 | `/ts-noi-dung-tu-dong-7-ngay` | 7 bài tuần đầu | `[DUYỆT]` từng bài trước khi đăng |
| 7 | `/ts-trang-ban-hang` → `/ts-landing-page` → `/ts-gan-ma-qr` → `/ts-dua-web-len-mang` (tùy chọn) | Trang đặt hàng có QR | Thử đặt 1 đơn |
| 8 | `/ts-xu-ly-tu-choi` | Câu trả lời mẫu cho inbox | — |
| 9 | `/ts-bang-tinh-excel` | Sổ đơn hàng + thu chi | — |
| 10 | `/ts-lap-lich-tu-dong` | Nhắc đăng bài, nhắc tổng kết tuần | `[DUYỆT]` trước khi đặt lịch |

## Mẫu 3 — Chạy chiến dịch quảng cáo kéo tin nhắn (Messenger)
*(vd spa Hồng, gói chăm sóc da 399.000đ, ngân sách 300.000đ/ngày)*

| Bước | Lệnh | Đầu ra | Điều kiện qua bước |
|---|---|---|---|
| 1 | Kiểm tra hồ sơ tệp 05: ID tài khoản quảng cáo, Page ID, ngân sách | Bảng đã có / còn thiếu | Có ID (không cần mật khẩu) |
| 2 | `/ts-ket-noi-ung-dung` (nếu chưa kết nối Meta) | Kết nối Meta đã kiểm tra | Kết nối hoạt động, hoặc chuyển sang chế độ hướng dẫn tay |
| 3 | `/ts-viet-quang-cao` | 3–5 góc nội dung + ma trận test | `[DUYỆT]` nội dung |
| 4 | `/ts-thiet-ke-anh-quang-cao` (hoặc `/ts-kich-ban-video-quang-cao` → `/ts-prompt-video-ai`) | Ảnh/video quảng cáo | `[DUYỆT]` creative |
| 5 | `/ts-xu-ly-tu-choi` | Kịch bản trả lời inbox, câu chốt | Sẵn sàng trả lời khách |
| 6 | `/ts-len-camp-facebook` | Chiến dịch → nhóm QC → quảng cáo ở trạng thái **tạm dừng** + bản xem trước | `[DUYỆT]` ngân sách, đối tượng, ngày chạy |
| 7 | Bật chiến dịch (chỉ khi người dùng nói rõ "bật") | Chiến dịch đang chạy | — |
| 8 | `/ts-bao-cao-facebook-ads` sau 3 ngày | Chẩn đoán: giữ / tắt / tăng ngân sách | `[DUYỆT]` mọi thay đổi |
| 9 | `/ts-lap-lich-tu-dong` (tùy chọn) | Báo cáo tự động mỗi sáng thứ Hai | `[DUYỆT]` |

Ngưỡng gợi ý (điều chỉnh theo tệp 05): tắt mẫu quảng cáo có chi phí mỗi tin nhắn gấp 2 lần mục tiêu sau
khi tiêu đủ 2–3 lần mục tiêu; chỉ tăng ngân sách 20–30% mỗi lần cho mẫu đang tốt.

## Mẫu 4 — Dựng phễu quà tặng 0 đồng
*(vd khóa học online: quà "Checklist 15 phút quay video bán hàng")*

| Bước | Lệnh | Đầu ra | Điều kiện qua bước |
|---|---|---|---|
| 1 | `/ts-chan-dung-khach-hang` (nếu tệp 03 còn mỏng) | Nỗi đau ưu tiên | `[DUYỆT]` |
| 2 | `/ts-pheu-qua-tang` — Cổng 1: chọn quà | Ma trận 3–7 quà, chấm điểm | `[DUYỆT]` chọn 1 quà |
| 3 | `/ts-pheu-qua-tang` — Cổng 2: đóng gói quà (dùng `/ts-tao-ebook`, `/ts-bang-tinh-excel`, `/ts-thiet-ke-thuyet-trinh` hoặc `/ts-infographic` tùy dạng quà) | Quà hoàn chỉnh | `[DUYỆT]` bản xem trước |
| 4 | `/ts-trang-ban-hang` (biến thể trang nhận quà) → `/ts-landing-page` | Trang nhận quà + trang cảm ơn | `[DUYỆT]` |
| 5 | `/ts-giao-hang-tu-dong` + `/ts-bao-don-telegram` | Tự gửi quà + báo lead mới | Thử đăng ký 1 lần thành công |
| 6 | `/ts-email-cham-soc` hoặc `/ts-cham-soc-khach-zalo` | Chuỗi 5–7 tin nuôi dưỡng → offer | `[DUYỆT]` trước khi gửi |
| 7 | `/ts-dua-web-len-mang` | Link công khai | `[DUYỆT]` |
| 8 | `/ts-viet-quang-cao` → `/ts-len-camp-facebook` | Quảng cáo kéo người nhận quà | `[DUYỆT]` ngân sách + bật |
| 9 | `/ts-phan-tich-mang-xa-hoi` / `/ts-bao-cao-facebook-ads` | Đo: xem trang → đăng ký → nhận quà → mua | — |

## Mẫu 5 — Lịch nội dung đều đặn mỗi tuần (xây kênh)
*(vd chủ shop thời trang muốn 5 bài + 3 video mỗi tuần)*

| Bước | Lệnh | Đầu ra | Điều kiện qua bước |
|---|---|---|---|
| 1 | `/ts-chan-dung-khach-hang` | Cụm nội dung | `[DUYỆT]` |
| 2 | `/ts-nghien-cuu-youtube` hoặc `/ts-phan-tich-doi-thu` (phần content) | Chủ đề đang hút view | — |
| 3 | `/ts-lich-noi-dung` (tháng) | Lịch 4 tuần | `[DUYỆT]` |
| 4 | Mỗi tuần: `/ts-noi-dung-tu-dong-7-ngay` | 7 bài + ảnh | `[DUYỆT]` từng bài |
| 5 | Mỗi tuần: `/ts-kich-ban-reels` → quay → `/ts-dung-video` | 3 video hoàn chỉnh | `[DUYỆT]` bản dựng |
| 6 | `/ts-lap-lich-tu-dong` | Nhắc mỗi Chủ nhật soạn tuần mới | `[DUYỆT]` |
| 7 | Cuối tháng: `/ts-phan-tich-mang-xa-hoi` | Bài/video hiệu quả nhất → lưu công thức vào `02-kien-thuc/cong-thuc/` | — |

---

## Phân công 3 sub-agent cho các mẫu (nếu nền tảng hỗ trợ)

| Mẫu | NGHIÊN CỨU | SẢN XUẤT | KIỂM TRA / TRIỂN KHAI |
|---|---|---|---|
| 1 Ra mắt khóa học | chân dung khách, đối thủ, giá | offer, trang, nội dung, creative | soát lỗi trang, thử thanh toán, dựng chiến dịch tạm dừng |
| 2 Cửa hàng online | đối thủ khu vực | Fanpage, ảnh, 7 bài | soát chính tả/giá, thử đặt đơn |
| 3 Quảng cáo inbox | đọc hồ sơ tệp 05, số liệu cũ | nội dung + creative | dựng chiến dịch tạm dừng, xem trước |
| 4 Phễu quà tặng | nỗi đau, quà đối thủ đang tặng | quà, trang, chuỗi tin | thử form, link tải, giao quà tự động |
| 5 Nội dung đều đặn | chủ đề hút view | bài, kịch bản | soát giọng thương hiệu, lịch đăng |

Không nền tảng nào hỗ trợ sub-agent → chạy tuần tự theo đúng thứ tự bảng.
