# Hướng dẫn kết nối Meta Ads vào AI (cho người không rành công nghệ)

> AI đọc hướng dẫn này cho học viên từng bước. Tên nút có thể khác nhau một chút giữa các ứng dụng AI và
> theo thời gian — nếu không thấy đúng chữ, tìm chữ gần nghĩa ("Connectors", "Kết nối", "Ứng dụng", "Apps",
> "Integrations", "Tools").

## Phần 1 — Kiểm tra trước khi kết nối (5 phút)

1. Vào **business.facebook.com** → **Trình quản lý quảng cáo (Ads Manager)**.
2. Góc trên bên trái, xem tên **tài khoản quảng cáo**:
   - Không có cảnh báo đỏ "Tài khoản bị vô hiệu hóa / hạn chế" → dùng được.
   - Có cảnh báo → xử lý trong *Chất lượng tài khoản (Account Quality)* trước, AI sẽ không dùng tài khoản này.
3. Vào **Cài đặt thanh toán** → đã có thẻ hoặc phương thức thanh toán.
4. Kiểm tra bạn là **quản trị viên Page** muốn chạy quảng cáo (Page → Cài đặt → Quyền truy cập Page).
5. Ghi lại tiền tệ của tài khoản (VND hay USD) — AI cần biết để nhập ngân sách đúng.

## Phần 2 — Kết nối Meta Ads vào ứng dụng AI

1. Mở ứng dụng AI bạn đang dùng (app máy tính hoặc trang web).
2. Vào phần **Kết nối / Connectors** (thường nằm trong *Cài đặt (Settings)* hoặc nút **+** cạnh ô nhập tin nhắn).
3. Tìm **Meta Ads** (hoặc "Meta", "Facebook Ads") → bấm **Thêm / Connect**.
4. Cửa sổ Facebook hiện ra → **đăng nhập Facebook** bằng tài khoản đang quản lý quảng cáo.
5. Ở màn hình cấp quyền:
   - Chọn **tài khoản quảng cáo** muốn cho AI dùng.
   - Chọn **Page** muốn chạy quảng cáo.
   - Bấm **Tiếp tục / Cho phép**.
6. Quay lại ứng dụng AI, thấy Meta Ads ở trạng thái **Đã kết nối** là xong.
7. Mở cuộc trò chuyện mới, gõ: "liệt kê tài khoản quảng cáo của tôi" để thử. AI đọc được tên tài khoản là thành công.

**Lưu ý:**
- **Không bao giờ** gửi mật khẩu Facebook, mã OTP hay mã bảo mật vào khung chat. Đăng nhập chỉ diễn ra trong
  cửa sổ của Facebook.
- Ứng dụng AI không có mục Meta Ads → dùng `/ts-ket-noi-ung-dung` để AI tìm cách kết nối phù hợp, hoặc dùng
  chế độ "AI soạn sẵn — bạn tự lên camp".
- Muốn ngắt kết nối: vào lại phần Kết nối / Connectors → Meta Ads → **Ngắt kết nối**; hoặc trên Facebook:
  *Cài đặt → Bảo mật → Tiện ích tích hợp doanh nghiệp* → gỡ ứng dụng.

## Phần 3 — Ghi ID vào hồ sơ (để lần sau khỏi chọn lại)

Sau lần chạy đầu, AI đề xuất ghi vào `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`:

```markdown
## Tài khoản quảng cáo
- Tài khoản quảng cáo Meta: <tên> — ID: <dãy số> — tiền tệ: <VND/USD>
- Page chạy quảng cáo: <tên Page> — ID: <dãy số>
- Ngân sách quảng cáo mặc định: <vd 200.000–500.000đ/ngày/chiến dịch>
- KPI: chi phí mỗi tin nhắn mong muốn ≤ <số>đ
- Khu vực bán hàng: <tỉnh/thành, bán kính>
```

ID tài khoản và ID Page không phải mật khẩu, lưu được. **Không** lưu mật khẩu, token, số thẻ.
