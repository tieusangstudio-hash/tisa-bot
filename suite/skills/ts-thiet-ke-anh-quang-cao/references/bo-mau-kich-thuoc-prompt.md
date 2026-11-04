# Bộ màu, kích thước và mẫu prompt ảnh quảng cáo

## 1. Sáu bộ màu chuẩn (dùng khi hồ sơ chưa có màu thương hiệu)

| # | Bộ màu | Màu chính | Màu phụ | Chữ / nhấn | Hợp với | Mô tả tiếng Anh cho prompt |
|---|---|---|---|---|---|---|
| 1 | Đen vàng | `#0D0D0D` | `#FFC300` | `#FFFFFF` | cao cấp, mạnh mẽ, khuyến mãi lớn, bất động sản | black and golden yellow palette, premium high-contrast |
| 2 | Gradient tím | `#6A11CB` → `#2575FC` | `#F2E9FF` | `#FFFFFF` | công nghệ, AI, khóa học online, sáng tạo | purple-to-blue gradient background, modern tech look |
| 3 | Xanh | `#0057FF` | `#00C2FF` | `#FFFFFF` | tin cậy, y tế, giáo dục, tài chính, dịch vụ B2B | clean blue and cyan palette, trustworthy professional |
| 4 | Cam vàng | `#FF7A00` | `#FFC93C` | `#1A1A1A` | ăn uống, bán lẻ, vui tươi, thân thiện | warm orange and yellow palette, cheerful energetic |
| 5 | Đỏ cam | `#E52D27` | `#FF6A00` | `#FFFFFF` | sale, flash deal, khẩn trương, sự kiện | bold red-orange palette, urgent sale energy |
| 6 | Trắng cam | `#FFFFFF` | `#FF6B00` | `#222222` | sạch, nhẹ, mỹ phẩm, spa, sản phẩm gia đình | clean white background with orange accents, airy minimal |

Hồ sơ có mã màu riêng → dùng mã màu đó, ghi trong prompt dạng "brand colors #XXXXXX and #YYYYYY".

## 2. Kích thước theo vị trí (tham khảo — nền tảng có thể thay đổi, kiểm tra khi tải lên)

| Vị trí | Tỷ lệ | Kích thước gợi ý | Vùng an toàn |
|---|---|---|---|
| Bảng tin Facebook/Instagram | 1:1 | 1080 × 1080 | Chữ cách mép ≥ 60 px |
| Bảng tin dọc (khuyên dùng) | 4:5 | 1080 × 1350 | Chữ cách mép ≥ 60 px |
| Story / Reels / TikTok | 9:16 | 1080 × 1920 | Chừa trống ~250 px trên và ~350 px dưới (thanh tên, nút, chú thích che) |
| Ảnh ngang / link / banner web | 1.91:1 | 1200 × 628 | Chữ chính ở giữa |
| Thumbnail YouTube | 16:9 | 1280 × 720 | Tránh góc dưới phải (thời lượng video che) |
| Ảnh bìa Fanpage | ≈ 2.63:1 | 1640 × 624 | Nội dung chính ở giữa ~1200 px (điện thoại cắt hai bên) |

**Tỷ lệ ảnh tổng ≠ tỷ lệ khung video bên trong.** Vd ảnh bảng tin 4:5 có thể chứa khung video 1:1 — ghi rõ cả hai.

## 3. Thứ bậc thị giác (xác định trước khi viết prompt)

1. **Thông điệp chính** — to nhất, ≤ 7 chữ.
2. **Hình chính** — sản phẩm / người / kết quả.
3. **Bằng chứng / lợi ích phụ** — 1 dòng nhỏ (chỉ điều có thật).
4. **CTA** — nút hoặc dải màu nhấn, 2–4 chữ.
5. **Nhận diện** — logo góc, màu thương hiệu.

Chữ trên ảnh chiếm khoảng ≤ 20–25% diện tích là dễ đọc trên điện thoại.

## 4. Mẫu prompt — mỗi ảnh một prompt, sao chép được

Viết prompt **bằng tiếng Anh**; chữ cần hiện trên ảnh ghi **nguyên văn tiếng Việt có dấu** trong ngoặc kép.

```text
[ẢNH 1 — Concept A — 4:5, 1080×1350]
Advertising poster, 4:5 vertical. Subject: <mô tả sản phẩm/người, khớp ảnh tham chiếu>.
Composition: <bố cục: sản phẩm bên phải, khoảng trống bên trái cho chữ…>.
Style: <phong cách: ảnh thật, ánh sáng studio mềm / phẳng tối giản / 3D…>.
Brand colors: <bộ màu hoặc mã màu>. Font style: bold rounded sans-serif that supports Vietnamese diacritics.
On-image text (exact Vietnamese, correct diacritics):
  Headline: "<THÔNG ĐIỆP CHÍNH>"
  Sub: "<dòng phụ>"
  CTA button: "<CTA>"
Logo: place the provided logo small in the top-left corner, unchanged.
Keep the product shape, color, label and logo exactly as the reference. High contrast, readable on mobile.
Avoid: misspelled text, extra text, distorted hands or faces, fake badges, watermarks.
```

Công cụ tạo ảnh hay viết sai dấu tiếng Việt → phương án dự phòng: tạo ảnh **không chữ** (thêm "no text" vào
prompt) rồi đặt chữ bằng công cụ thiết kế (Canva, PowerPoint…) theo đúng nội dung chữ đã duyệt.

## 5. Mẫu concept (trình trước khi tạo ảnh)

```text
CONCEPT A — <tên góc, vd "Kết quả trước – sau">
Góc tiếp cận: …            Khách nhắm tới: …
Thông điệp chính: "…"      CTA: "…"
Bố cục: …                  Hình chính: …
Màu: …                     Tỷ lệ: …
Giả thuyết A/B: Nếu nhấn vào <…> thì <chỉ số, vd CTR> cao hơn concept B vì <…>.
```

Các concept phải khác nhau về **góc tiếp cận, bố cục và hình ảnh**, không chỉ đổi màu trên cùng một mẫu.
Góc gợi ý: nỗi đau · kết quả/trước–sau · bằng chứng/feedback thật · ưu đãi có hạn · so sánh lựa chọn ·
hướng dẫn nhanh/mẹo · câu hỏi gây tò mò.

## 6. Checklist kiểm tra ảnh

- [ ] Đúng tỷ lệ và kích thước vị trí đặt.
- [ ] Chữ tiếng Việt đúng chính tả, đúng dấu, không thừa chữ lạ.
- [ ] Một thông điệp chính, một CTA.
- [ ] Nội dung quan trọng nằm trong vùng an toàn.
- [ ] Tương phản đủ, đọc được trên điện thoại (thu nhỏ còn ~30% vẫn đọc được tiêu đề).
- [ ] Sản phẩm, logo, gương mặt tham chiếu không bị biến dạng.
- [ ] Không có logo/feedback/chứng nhận/huy hiệu người dùng chưa cung cấp.
- [ ] Có quyền sử dụng mọi ảnh, font, nhân vật.
