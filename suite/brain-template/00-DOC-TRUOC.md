---
loai: quy-tac
chu-so-huu: "{{TEN}}"
tao-ngay: {{NGAY}}
---

# Bộ Não Thứ 2 — {{TEN}}

Đây là "trí nhớ dài hạn" của bạn và trợ lý AI. Mọi thông tin doanh nghiệp, kiến thức và kết quả làm việc
được lưu ở đây, để lần sau AI đọc lại và làm đúng ngay — không phải hỏi lại từ đầu.

## Dành cho bạn (người dùng)

- **Mở bằng Obsidian** để xem đẹp, có liên kết và sơ đồ: Obsidian → *Open folder as vault* → chọn thư mục này.
- **Bắt đầu tại đây:** chạy `/ts-tao-ho-so-doanh-nghiep` để AI phỏng vấn và điền 5 tệp trong `01-ho-so/`.
- **Thả tài liệu** (bảng giá, brochure, ảnh chụp, file ghi âm đã chép lời…) vào `03-tai-lieu-tho/`.
- **Kết quả** của mỗi lần chạy lệnh `/ts-...` nằm trong `04-ket-qua/`, xem nhanh ở [[muc-luc]].
- Không lưu mật khẩu, mã OTP, token, số thẻ ngân hàng vào bất kỳ tệp nào ở đây.

## Dành cho trợ lý AI (đọc kỹ trước khi làm bất cứ việc gì)

1. **Thứ tự đọc:** tệp này → `muc-luc.md` → các tệp cần thiết trong `01-ho-so/` → `02-kien-thuc/` liên quan →
   các lần làm trước trong `04-ket-qua/` cùng chủ đề. Chỉ hỏi người dùng phần còn thiếu.
2. **Không bịa:** thông tin không có trong Bộ Não và người dùng chưa nói → hỏi lại hoặc ghi `[CẦN BỔ SUNG]`.
3. **Quyền của từng thư mục:**

   | Thư mục | AI được làm gì |
   |---|---|
   | `01-ho-so/` | Đọc. Chỉ sửa khi người dùng đồng ý (hỏi trước khi ghi đè). |
   | `02-kien-thuc/` | Đọc, thêm trang mới. Sửa trang cũ khi có thông tin mới hơn, ghi rõ ngày cập nhật. |
   | `03-tai-lieu-tho/` | Chỉ đọc. Không sửa, không xóa. |
   | `04-ket-qua/` | Tạo thư mục mới cho mỗi lần làm. Không xóa kết quả cũ. |
   | `05-du-an/` | Đọc, cập nhật tiến độ khi người dùng yêu cầu. |
   | `06-mau/` | Dùng làm mẫu. |
   | `99-luu-tru/` | Chỉ đọc khi được yêu cầu. |

4. **Mỗi lần làm xong một lệnh `/ts-...` đã được người dùng duyệt:**
   - Tạo `04-ket-qua/<YYYY-MM>/<YYYY-MM-DD>-<ma-skill>-<chu-de-khong-dau>/ket-qua.md`, mọi tệp phụ (ảnh, slide, video, PDF...) nằm cùng thư mục đó (có frontmatter `loai`, `skill`, `ngay`, `chu-de`, `the`).
   - Thêm 1 dòng vào mục **Kết quả** của `muc-luc.md`: `- [[04-ket-qua/<thư-mục>/ket-qua|Tên ngắn]] — mô tả 1 câu`.
   - Thêm 1 dòng vào cuối `nhat-ky.md`: `- <YYYY-MM-DD HH:mm> · /ts-<ten> · <chủ đề> · <đường dẫn>`.
   - Tri thức dùng lại lâu dài (chân dung khách đã chốt, bảng giá mới, công thức content hiệu quả…) →
     đề xuất lưu vào `02-kien-thuc/` hoặc cập nhật `01-ho-so/`, hỏi trước khi ghi đè.
5. **Đặt tên:** tiếng Việt không dấu, chữ thường, nối bằng gạch ngang (vd `2026-11-04-dinh-gia-offer-khoa-online`).
   Liên kết nội bộ dùng kiểu Obsidian `[[ten-tep]]`.
6. **Bảo mật:** không bao giờ ghi mật khẩu, OTP, token, khóa API, số thẻ vào Bộ Não. Chỉ ghi tên kết nối,
   quyền đã cấp và ngày.

## Cấu trúc

| Thư mục / tệp | Chứa gì |
|---|---|
| `00-DOC-TRUOC.md` | Tệp này — quy tắc chung |
| `CLAUDE.md` · `AGENTS.md` · `GEMINI.md` | Lời nhắc tự động cho Claude, ChatGPT/Codex, Gemini/Antigravity (đều trỏ về tệp này) |
| `muc-luc.md` | Mục lục mọi thứ trong Bộ Não |
| `nhat-ky.md` | Nhật ký: mỗi lần chạy lệnh là một dòng |
| `01-ho-so/` | 5 tệp hồ sơ doanh nghiệp — nền tảng cho mọi lệnh |
| `02-kien-thuc/` | Tri thức dùng lại: khách hàng, sản phẩm, đối thủ, công thức |
| `03-tai-lieu-tho/` | Tài liệu gốc bạn thả vào |
| `04-ket-qua/` | Kết quả từng lần làm việc |
| `05-du-an/` | Theo dõi dự án, khóa học, chiến dịch |
| `06-mau/` | Mẫu ghi chú cho Obsidian |
| `99-luu-tru/` | Tài liệu cũ |
| `.agent/workflows/` | Lệnh `/ts-...` cho Google Antigravity (đừng xóa) |

*Bộ Não Thứ 2 được tạo bởi bộ skill TISA AI Agent — Học Viện TISA.*
