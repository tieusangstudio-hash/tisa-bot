# Nguyên tắc thiết kế infographic

Dùng cho `/ts-infographic`. Tóm lược các nguyên tắc thiết kế thông tin phổ biến, diễn đạt lại cho người mới.

## 1. Thông điệp trước, thiết kế sau (80/20)
- 80% công sức dành cho **nội dung**: một ảnh trả lời đúng một câu hỏi của khách.
- Trước khi thiết kế phải viết được 1 câu: *"Xem xong ảnh này, người đọc sẽ biết/làm được ___."*
- Chỉ giữ thông tin phục vụ câu đó. Ý nào hay nhưng lạc đề → để dành cho ảnh khác.

## 2. Mỗi thẻ một ý
- Tên thẻ ≤ 6 chữ, bắt đầu bằng động từ khi là "bước" (Chọn…, Viết…, Quay…).
- Nội dung thẻ ≤ 14 chữ, một câu, không chấm phẩy nhiều vế.
- 3–6 thẻ là vừa. 7 ý trở lên → tách thành 2 ảnh (carousel).

## 3. Bốn nguyên tắc bố cục
| Nguyên tắc | Nghĩa đơn giản | Áp dụng trong mẫu |
|---|---|---|
| **Tương phản** | Thứ quan trọng phải khác hẳn thứ phụ | Tiêu đề rất to và đậm; số thứ tự nằm trong ô màu nhấn; chữ phụ nhạt hơn |
| **Lặp lại** | Thành phần cùng loại trông giống nhau | Mọi thẻ cùng kiểu, cùng khoảng cách, cùng màu |
| **Căn lề** | Mọi thứ xếp theo đường thẳng vô hình | Lề trái chung cho tiêu đề, thẻ, chân trang |
| **Gần nhau** | Thứ liên quan đặt gần, thứ khác nhóm đặt xa | Tên thẻ sát nội dung thẻ; khoảng trống rõ giữa đầu – thân – chân |

## 4. Ít chữ, không trang trí thừa
- Bỏ khung viền, bóng đổ, biểu tượng không mang thông tin.
- Không dùng quá 2 kiểu chữ (font). Mẫu dùng 1 font với 3 độ đậm.
- Khoảng trống là bạn: đừng nhồi thêm chữ vào chỗ trống.
- Số liệu: chỉ đưa số có nguồn. Biểu đồ đơn giản (cột, thanh ngang) tốt hơn biểu đồ 3D hay tròn nhiều lát.

## 5. Chữ tiếng Việt chuẩn
- File HTML luôn lưu dạng UTF-8 và có `<meta charset="utf-8">`.
- Dùng font hỗ trợ đầy đủ dấu tiếng Việt: Be Vietnam Pro (mặc định), dự phòng Inter, Segoe UI, Arial, Noto Sans.
- Gõ chữ dạng **Unicode dựng sẵn**. Khi chép chữ từ Word/PDF có thể dính ký tự tổ hợp (dấu tách rời) → AI chuẩn hóa
  về dạng dựng sẵn (NFC) trước khi đưa vào HTML.
- Kiểm tra kỹ các chữ dễ lỗi: ư, ơ, ă, đ và dấu chồng (ặ, ẩ, ữ, ợ).
- Không viết hoa toàn bộ câu dài (khó đọc, dấu dễ đè nhau); chỉ viết hoa nhãn nhỏ 1–2 từ.

## 6. Kích cỡ chữ đọc được trên điện thoại (khổ 1080 px ngang)
| Thành phần | Cỡ chữ tối thiểu |
|---|---|
| Tiêu đề | 60 px |
| Tên thẻ | 28 px |
| Nội dung thẻ | 20 px |
| Chân trang, ghi chú | 20 px |

## 7. Chọn khổ ảnh
| Khổ | Dùng cho | Lưu ý |
|---|---|---|
| 1080×1350 (dọc 4:5) | Bài đăng Facebook, Instagram, Threads, LinkedIn — chiếm nhiều diện tích bảng tin nhất | Mặc định |
| 1080×1080 (vuông) | Carousel, ảnh dùng lại nhiều nền tảng | Ít chỗ hơn → tối đa 5 thẻ ngắn |
| 1080×1920 (dọc 9:16) | Story, Reels, TikTok ảnh | Chừa vùng trên ~200 px và dưới ~260 px vì giao diện ứng dụng che |

## 8. Các dạng bố cục khác (AI tự dựng khi nội dung không phải "N bước")
Giữ nguyên biến màu, font, khổ của mẫu; chỉ thay phần thân:
- **So sánh 2 cột** (Nên / Không nên, Trước / Sau): 2 cột thẻ, cột trái màu nhạt, cột phải màu nhấn.
- **Cấp độ / bậc thang**: thẻ xếp từ dưới lên, thẻ trên cùng to nhất.
- **Con số nổi bật**: 1–3 con số rất to (có nguồn) + 1 dòng giải thích dưới mỗi số.
- **Câu trích dẫn**: 1 câu lớn giữa ảnh + tên người nói (chỉ trích dẫn có thật).
- **Checklist**: ô vuông đánh dấu thay cho số thứ tự.
