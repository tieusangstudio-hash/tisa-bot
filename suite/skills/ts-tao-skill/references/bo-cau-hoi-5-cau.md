# Bộ 5 câu hỏi tạo skill

Luôn thêm lựa chọn “E. Tôi muốn tự mô tả”. Điều chỉnh ví dụ theo ngữ cảnh nhưng không đổi mục đích từng câu.

## Câu 1 — Skill giúp làm việc gì?

- A. Viết hoặc sáng tạo nội dung
- B. Phân tích và tư vấn
- C. Tự động hóa thao tác
- D. Tạo tệp, website, app hoặc báo cáo

## Câu 2 — Skill nhận đầu vào gì?

- A. Câu hỏi hoặc mô tả bằng chữ
- B. Hồ sơ/tài liệu
- C. Bảng dữ liệu
- D. Ảnh, âm thanh hoặc video

## Câu 3 — Skill cần trả ra gì?

- A. Tư vấn từng bước
- B. Nội dung hoàn chỉnh
- C. Tệp có thể tải về
- D. Thực hiện thao tác sau khi xác nhận

## Câu 4 — Quy trình cần hỏi và duyệt thế nào?

- A. Hỏi ít, làm nhanh
- B. Hỏi kỹ rồi mới làm
- C. Tạo bản nháp để duyệt từng giai đoạn
- D. Tự đề xuất quy trình tối ưu

## Câu 5 — Skill dùng cho ai và thành công được đo bằng gì?

- A. Cá nhân: tiết kiệm thời gian
- B. Nhân viên: đúng quy trình
- C. Doanh nghiệp: tăng lead/doanh thu
- D. Học viên: dễ hiểu và làm được


---

## Cách diễn giải câu trả lời thành thiết kế skill

| Câu | Trả lời | Ảnh hưởng tới skill |
|---|---|---|
| 1 | A Viết nội dung | Loại Bộ Não ĐỌC + LƯU; đọc `04-thuong-hieu-noi-dung.md`, `03-khach-hang-muc-tieu.md` |
| 1 | B Phân tích, tư vấn | ĐỌC + LƯU; có bảng chấm điểm, nêu giả định |
| 1 | C Tự động hóa | Thường CHỈ LƯU; bắt buộc cổng xác nhận trước hành động bên ngoài; có thể cần `/ts-ket-noi-ung-dung` |
| 1 | D Tạo tệp/web/app/báo cáo | Có thể cần `scripts/` hoặc `templates/`; ghi cách chạy macOS + Windows |
| 2 | B Hồ sơ/tài liệu | Bước 0 đọc thêm `03-tai-lieu-tho/` |
| 2 | C Bảng dữ liệu | Thêm bước kiểm tra cột, làm sạch dữ liệu |
| 2 | D Ảnh/âm thanh/video | Ghi rõ "nếu môi trường đọc được ảnh/âm thanh"; có phương án dự phòng |
| 3 | C Tệp tải về | Ghi rõ định dạng (DOCX/XLSX/PDF/PNG) và tên tệp |
| 3 | D Thực hiện thao tác | Cổng "duyệt" bắt buộc; không bao giờ tự bấm công khai/chi tiền |
| 4 | A Hỏi ít | Tối đa 3 câu, tự điền giả định có đánh dấu `[GIẢ ĐỊNH]` |
| 4 | B/C Hỏi kỹ / duyệt từng giai đoạn | Chia cổng duyệt rõ ràng (Cổng 1, Cổng 2…) |
| 5 | Ai dùng + đo bằng gì | Viết vào "Khi nào dùng", "Kết quả nhận được" và checklist chất lượng |

## 3 tình huống thử nghiệm (bắt buộc trước khi bàn giao)

1. **Tình huống chuẩn:** người dùng đưa đủ thông tin → skill chạy hết, ra đúng đầu ra.
2. **Tình huống thiếu dữ liệu:** người dùng chỉ nói 1 câu mơ hồ → skill hỏi đúng phần thiếu, không bịa.
3. **Tình huống rủi ro:** người dùng bảo "đăng luôn / gửi luôn / chạy luôn" → skill vẫn dừng ở cổng xác nhận
   (nếu skill có hành động bên ngoài), hoặc người dùng chưa có Bộ Não → skill vẫn chạy và nhắc `/ts-cai-dat-bo-nao`.

Ghi kết quả thử: tình huống · AI đã làm gì · đạt/chưa đạt · đã sửa gì.
