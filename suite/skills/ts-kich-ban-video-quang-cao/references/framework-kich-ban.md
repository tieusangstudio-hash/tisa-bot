# Framework kịch bản quảng cáo

## AIDA

Attention → Interest → Desire → Action. Hợp với sản phẩm dễ hiểu và CTA trực tiếp.

## PAS

Problem → Agitate → Solution. Hợp khi nỗi đau rõ; không phóng đại nỗi sợ hoặc tạo áp lực gây hại.

## Before–After–Bridge

Hiện tại → Kết quả mong muốn → Cầu nối. Hợp với dịch vụ chuyển đổi có quy trình dễ hình dung.

## Problem–Solution–Proof–Offer

Vấn đề → Giải pháp → Bằng chứng → Đề nghị. Hợp với khách cần lý do tin trước khi hành động.

## Story–Offer

Bối cảnh → Xung đột → Khám phá → Kết quả → Offer. Hợp với câu chuyện thương hiệu hoặc case thật.

## Nhịp lời thoại tham khảo

- 60 giây: khoảng 120–150 từ tiếng Việt
- 90 giây: khoảng 180–220 từ
- 120 giây: khoảng 240–300 từ

Điều chỉnh theo tốc độ người nói. Ưu tiên dễ nghe hơn nhồi đủ chữ.


## Chọn cấu trúc nhanh

| Tình huống | Cấu trúc nên dùng |
|---|---|
| Sản phẩm dễ hiểu, giá vừa, CTA mua ngay | AIDA |
| Nỗi đau rõ, khách đang khổ | PAS |
| Dịch vụ "biến đổi" (đẹp hơn, giỏi hơn, gọn hơn) | Before–After–Bridge |
| Khách hoài nghi, cần lý do tin | Problem–Solution–Proof–Offer |
| Có câu chuyện thật của chủ/khách | Story–Offer |

## 5 góc hook (mỗi hook một tệp khách hoặc một nỗi đau khác nhau)

| Góc | Cách mở | Ví dụ minh họa (tiệm bánh giả định) |
|---|---|---|
| Gọi tên đúng người | "Nếu bạn là…" | "Mẹ nào sắp tổ chức sinh nhật cho bé mà chưa đặt bánh thì xem ngay." |
| Nỗi đau cụ thể | Nói thẳng điều khách đang khổ | "Đặt bánh online về bị lệch kem, chữ sai tên bé — buồn cả buổi tiệc." |
| Kết quả mong muốn | Vẽ ra cảnh sau khi dùng | "Bánh đến đúng giờ, đúng mẫu, bé reo lên khi mở hộp." |
| Phá niềm tin sai | "Bạn nghĩ … nhưng thật ra…" | "Bánh đẹp không có nghĩa là phải đặt trước 1 tuần." |
| Con số/bằng chứng thật | Mở bằng số liệu được xác minh | "[CẦN BỔ SUNG: số đơn thật] chiếc bánh giao đúng giờ tháng trước." |

Hook dài tối đa 2 câu, đọc trong 3–5 giây. Mỗi hook phải nối được vào cùng thân bài.

## Cấu trúc thân bài (lời thoại)

vấn đề → hệ quả → cơ chế giải pháp (vì sao cách này hiệu quả) → giá trị/lợi ích → điểm khác biệt →
bằng chứng thật → giảm rủi ro (bảo hành, đổi trả, thử miễn phí — chỉ khi có thật) → offer.

## Bảng cảnh sơ bộ (mẫu)

| Thời gian | Hình ảnh | Lời thoại | Chữ trên màn hình | Mục tiêu cảnh |
|---|---|---|---|---|
| 0–3s | Cận mặt nhân vật, nhìn thẳng | Hook | 3–6 chữ in đậm | Giữ người xem |
| 3–15s | … | … | … | … |

## Khối bàn giao cho `/ts-prompt-video-ai`

Đặt cuối kịch bản, trong một khối mã để sao chép:

```text
VIDEO_SCRIPT_HANDOFF
duration: 60
aspect_ratio: 9:16
selected_hook: <hook đã chọn, nguyên văn>
character: <mô tả nhân vật từ 04-thuong-hieu-noi-dung.md hoặc người dùng cung cấp>
product: <tên sản phẩm + đặc điểm nhìn thấy được>
narration: |
  <toàn bộ lời thoại liền mạch, tiếng Việt>
scene_intents:
  - 0-3s: <mục tiêu + hình ảnh chính>
  - 3-15s: <…>
  - …
on_screen_text: <các dòng chữ cần hiện>
cta: <câu CTA cuối>
music: none
```
