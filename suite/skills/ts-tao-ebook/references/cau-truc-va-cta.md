# Cấu trúc ebook, cách viết và đặt hộp CTA

Tài liệu tham khảo cho `/ts-tao-ebook`.

## 1. Chọn độ dài theo mục tiêu

| Mục tiêu | Độ dài gợi ý | Cấu trúc | Ghi chú |
|---|---|---|---|
| Quà tặng thu thông tin (lead magnet) | 10–25 trang A5 (3.000–6.000 chữ) | 1–2 Phần · 4–6 Chương | Đọc xong trong 20–30 phút, cho 1 kết quả nhanh |
| Ebook bán giá thấp | 30–60 trang A5 | 2–3 Phần · 8–12 Chương | Có bài tập, mẫu điền sẵn |
| Tài liệu khóa học / cẩm nang nội bộ | 40–100 trang A4 | 3–5 Phần | Ưu tiên tra cứu: mục lục rõ, bảng, checklist |

Người Việt đọc ebook chủ yếu trên điện thoại → mặc định **A5**, đoạn văn ngắn (2–4 câu), nhiều tiêu đề nhỏ.

## 2. Khung dàn ý Phần – Chương (mẫu)

```
Tên sách: <kết quả cụ thể> cho <ai> trong <thời gian>
Phụ đề:   <lời hứa phụ / hình thức>

Lời mở đầu (½–1 trang): sách dành cho ai · đọc xong làm được gì · cách đọc
Phần 1 — Hiểu đúng vấn đề
  Chương 1: Vì sao <cách phổ biến> không hiệu quả
  Chương 2: Nguyên tắc cốt lõi
Phần 2 — Làm từng bước
  Chương 3: Bước 1 …
  Chương 4: Bước 2 …
  Chương 5: Bước 3 …
Phần 3 — Đi xa hơn
  Chương 6: Lỗi thường gặp & cách sửa
  Chương 7: Kế hoạch 7 ngày
Lời kết + bước tiếp theo (CTA chính)
```

Mỗi chương nên có: 1 ý chính (nói ở câu đầu) → giải thích → ví dụ → bài tập/checklist ngắn → câu nối sang chương sau.

## 3. Giọng văn

| Chọn | Hợp với | Dấu hiệu |
|---|---|---|
| Thân thiện | Mẹ bỉm, chủ shop nhỏ, người mới | Xưng "mình – bạn", câu ngắn, ví dụ đời thường |
| Chuyên gia | Dịch vụ B2B, tài chính, sức khỏe | Xưng "chúng tôi – bạn", có số liệu kèm nguồn, ít cảm thán |
| Truyền cảm hứng | Phát triển bản thân, khởi nghiệp | Câu chuyện, câu hỏi tu từ, kết chương bằng thông điệp |

Lấy giọng từ `01-ho-so/04-thuong-hieu-noi-dung.md` nếu đã có.

## 4. Nghiên cứu & trích nguồn

- Ưu tiên tài liệu của chính người dùng trong `03-tai-lieu-tho/` (bài viết cũ, ghi chú khóa học, bản chép video).
- Thông tin từ web: chỉ dùng nguồn rõ ràng (cơ quan nhà nước, báo chính thống, nghiên cứu, trang chính thức của
  công cụ). Ghi lại **tên nguồn + đường link + ngày truy cập** vào `nguon.md`.
- Số liệu trong sách luôn kèm nguồn ngắn ngay sau câu, vd *(Nguồn: Tổng cục Thống kê, 2025)*. Cuối sách có mục
  **Nguồn tham khảo**.
- Không chép nguyên văn đoạn dài; diễn đạt lại và trích dẫn ngắn có ghi nguồn.
- Không chắc chắn → ghi `[CẦN KIỂM CHỨNG: …]` để người dùng xác nhận trước khi xuất bản.

## 5. Hộp kêu gọi hành động (CTA)

Cú pháp trong Markdown:
```
> [!CTA] Tiêu đề ngắn nói lợi ích
> 1–2 câu: làm gì, ở đâu, nhận được gì.
```

**3–5 hộp cho cả cuốn**, đặt ở các **điểm cảm xúc cao** — lúc người đọc vừa:
1. **Nhận ra vấn đề** của mình (cuối chương nói về sai lầm) → mời nhận công cụ tự kiểm tra.
2. **Có chiến thắng nhỏ** (sau bài tập đầu tiên làm được) → mời tham gia nhóm/cộng đồng.
3. **Thấy khoảng cách** giữa biết và làm (giữa phần hướng dẫn) → mời buổi tư vấn/lớp thử.
4. **Đọc xong** (lời kết) → CTA chính, rõ ràng nhất.

Quy tắc:
- Mỗi hộp **một** hành động; thống nhất kênh liên hệ (Zalo, link đăng ký, fanpage) lấy từ `05-muc-tieu-quy-tac-lien-he.md`.
- Hộp đầu tiên không xuất hiện trước 20% cuốn sách — cho giá trị trước.
- Ưu đãi, hạn chót trong CTA phải có thật. Thiếu thông tin → `[CẦN BỔ SUNG: link đăng ký]`.
- Hộp mẹo dùng cú pháp `> [!MEO] Tiêu đề` (không tính vào số CTA).

## 6. Checklist trước khi dựng PDF

- [ ] Tên sách nói rõ kết quả; phụ đề nói rõ dành cho ai.
- [ ] Mỗi chương bắt đầu bằng `## `, mỗi phần bằng `# Phần N: …`.
- [ ] Không đoạn nào dài quá 5 dòng trên điện thoại.
- [ ] Có ít nhất 1 ví dụ / bài tập mỗi chương.
- [ ] 3–5 hộp CTA ở đúng điểm cảm xúc; kênh liên hệ đúng và thống nhất.
- [ ] Số liệu có nguồn; mục Nguồn tham khảo ở cuối.
- [ ] Chính tả tiếng Việt, dấu đầy đủ; không còn `[CẦN BỔ SUNG]` / `[CẦN KIỂM CHỨNG]` khi xuất bản.
- [ ] Ảnh minh họa (nếu có) nằm cùng thư mục với file `.md`, ảnh có quyền sử dụng.

## 7. Đăng thành sách lật (flipbook) — tùy chọn

Sách lật giúp người đọc lật trang trên điện thoại như sách thật, chia sẻ bằng 1 đường link. Các dịch vụ phổ biến như
**Heyzine**, **FlipHTML5** đều có gói miễn phí (giới hạn tính năng và có thể kèm logo của dịch vụ — kiểm tra trang giá
của họ trước khi dùng cho mục đích thương mại). Thao tác chung (tên nút có thể khác theo phiên bản):

1. Vào trang chủ dịch vụ → đăng ký tài khoản bằng email.
2. Bấm **Upload PDF** / **Create flipbook** → chọn file PDF vừa tạo.
3. Chờ xử lý 1–3 phút → xem thử, chọn kiểu lật trang, màu nền gần màu thương hiệu.
4. Ở phần cài đặt: đặt tên sách, ảnh bìa (thường tự lấy trang 1), bật/tắt nút tải PDF.
5. Bấm **Publish / Share** → sao chép đường link hoặc mã nhúng (embed) để gắn vào trang web.
6. Quà tặng thu thông tin: gửi link sách lật trong tin nhắn cảm ơn sau khi khách để lại thông tin
   (xem `/ts-pheu-qua-tang`, `/ts-giao-hang-tu-dong`).

Lưu ý: không tải lên dịch vụ công khai những tài liệu nội bộ, có thông tin khách hàng hoặc tài liệu chưa được phép phát hành.
