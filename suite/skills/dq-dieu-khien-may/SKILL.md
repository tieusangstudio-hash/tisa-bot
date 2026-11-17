---
name: dq-dieu-khien-may
description: "Điều khiển máy tính của anh như người thật: nhìn màn hình, di chuột, bấm, gõ, mở ứng dụng, thư mục. Không xóa tệp. Có 3 mức tự động."
group: Điều hành
---
# Điều khiển máy tính của người dùng

Dùng khi việc phải làm **trên chính máy tính** của anh: mở màn hình desktop, tìm thư mục, bấm vào tệp, mở hoặc dùng một ứng dụng, thao tác trong phần mềm không có MCP hay API. Chạy ngay trên máy này (macOS, Windows), không tải gì lên mạng. Việc trên web dùng Trình duyệt TISA (skill `dq-trinh-duyet`), không dùng cái này. Đọc, ghi, tìm tệp bằng công cụ tệp có sẵn thì **luôn tốt hơn bấm chuột**: chỉ dùng điều khiển máy khi phải thao tác trong giao diện một ứng dụng.

## Hai công cụ
- `tisa_desktop_look` (chỉ xem): `op=screenshot` chụp màn hình (ảnh được gửi kèm ngay trong kết quả để nhìn, không cần mở tệp); `op=zoom x y x2 y2` phóng to một vùng của ảnh gần nhất để đọc chữ nhỏ; `op=windows` ứng dụng đang mở; `op=front` ứng dụng đang ở trước; `op=permissions` kiểm tra quyền; `op=status`.
- `tisa_desktop_do` (thao tác): `click`, `double_click`, `right_click` (x, y); `move`; `drag` (x, y, x2, y2); `scroll` (dy, dương là xuống); `type` (text; tiếng Việt gõ được; thêm `kieu=phim` để gõ từng phím thật cho máy tính bỏ túi, trò chơi, phím tắt); `key` (ví dụ `cmd+space`, `enter`, `ctrl+c`, `alt+tab`); `open_app` (name); `open_path` (path: mở thư mục hoặc tệp bằng ứng dụng mặc định); `focus_app` (name); `quit_app` (name); `wait` (ms).

## Vòng làm việc (lặp tới khi xong)
1. **Nhìn**: `screenshot`, xem ảnh gửi kèm. Chữ nhỏ thì `zoom` vùng đó. Tọa độ (x, y) trong ảnh đúng bằng tọa độ để bấm, gốc ở góc trên trái. Kết quả không kèm ảnh (công cụ báo chụp lỗi, ảnh đen, máy khoá) thì nói thật với anh và làm theo thông báo (mở khoá máy, bật quyền), tuyệt đối không đoán nội dung màn hình.
2. **Nghĩ một bước**: mục tiêu của anh là gì, màn hình đang ở đâu, nút nào đưa gần mục tiêu nhất. Chọn theo chữ trên nút, không đoán.
3. **Làm đúng một bước** (bấm, gõ, mở), chờ 1 đến 2 giây (`wait`), rồi **`screenshot` lại để kiểm chứng**. Không thấy thay đổi thì đừng bấm lại ngay: xem ảnh, có thể ứng dụng chưa kịp, hoặc hộp thoại đang chắn.
4. **Lệch thì sửa**; kẹt cùng một chỗ ba lần thì dừng và mô tả đúng chỗ kẹt cho anh.
5. **Báo xong có bằng chứng**: đã làm gì, ảnh chụp hoặc đường dẫn tệp.

## Mẹo
- Mở ứng dụng: `open_app` bằng tên tiếng Anh (Calculator, Notes, Safari) hoặc đúng tên trong `windows`. Máy tiếng Việt hiển thị "Máy tính", "Cài đặt hệ thống": `focus_app` nhận cả tên đó.
- Tìm thư mục, tệp: dùng công cụ tìm tệp trước, rồi `open_path` để mở cho anh xem. Không cần lục từng thư mục bằng chuột.
- Mở Spotlight bằng `cmd+space` (macOS) hoặc phím Windows để mở ứng dụng nhanh, `type` tên rồi `enter`.
- Đưa chuột vào đúng giữa nút; ứng dụng chậm thì `wait` lâu hơn.
- Gõ nhanh mà ứng dụng rớt phím (máy tính bỏ bỏ túi): gõ từng nhóm ngắn rồi chụp lại.

## Luật an toàn (công cụ cũng tự chặn, không được tìm cách vòng)
- **KHÔNG BAO GIỜ xóa tệp, thư mục** trên máy anh: không phím xóa, không Dọn Thùng rác, không chuột phải hay kéo thả trong Finder và File Explorer, không gõ lệnh xóa vào Terminal. Công cụ trả `BI_CHAN_XOA`. Chỉ khi anh bật công tắc **Cho phép AI xóa tệp** (có hạn giờ, tự tắt) mới được, và chỉ xóa đúng thứ anh nói rõ. Cần "dọn" thì đề xuất danh sách để anh tự xóa. Đừng dùng cách khác (kéo vào Thùng rác, công cụ chạy lệnh) để né luật này.
- **Mật khẩu, khóa, ví, ngân hàng**: cửa sổ đăng nhập hệ thống, ứng dụng quản lý mật khẩu, ví coin, ứng dụng ngân hàng: không bấm, không gõ (`CAN_NGUOI_DUNG`). Nói với anh việc cần làm, chờ anh làm.
- **Ba mức anh chọn** (op=status cho biết `muc`): **hoi_het** xin duyệt từng thao tác; **quan_trong** (mặc định) chỉ xin duyệt khi gõ lệnh Terminal, gửi tin nhắn (Enter trong Zalo, Messages...), đổi cài đặt hệ thống, thoát ứng dụng, mở tệp cài đặt hoặc tệp chạy được; **toan_quyen** tự làm hết trừ các luật trên. Khi công cụ trả `CAN_DUYET`: nói rõ với anh sẽ làm gì, chờ anh bấm **Duyệt** trong TISA BOT, rồi gọi lại đúng lệnh với `duyet_id`. Mỗi mã dùng một lần.
- Anh bấm **Dừng AI ngay**, hoặc đưa chuột về góc trên trái màn hình: ngừng hẳn (`DA_DUNG`), không thử lại.
- Chưa cấp quyền (`CHUA_CAP_QUYEN` trên macOS): nói anh mở bảng Điều khiển máy tính trong TISA BOT, bấm "Mở cài đặt Trợ năng" và "Mở cài đặt Ghi màn hình", bật cho chương trình được ghi trong bảng, rồi thử lại.
- Không chụp rồi lưu, gửi đi nội dung riêng tư thấy trên màn hình (tin nhắn, giấy tờ, số tài khoản). Ảnh chụp chỉ để làm đúng việc được giao.
- Việc đang chạy một mình (không có anh ngồi cạnh) mà cần anh duyệt: đặt phần việc ở trạng thái chờ anh, ghi rõ cần gì.

## Tự chuẩn bị, bấm được thì tự bấm, không được thì nhờ anh
Trước khi làm việc cần điều khiển, tự kiểm tra và tự bật những gì cần, đừng chờ anh nhắc:
1. `tisa_desktop_look op=permissions` (macOS): thiếu Trợ năng hoặc Ghi màn hình thì gọi ngay `tisa_desktop_do op=cai_dat_quyen`. TISA BOT mở sẵn đúng chỗ trong Cài đặt, chờ anh bật công tắc rồi em làm tiếp. Nói anh MỘT câu: "Em cần anh bật công tắc quyền này, bật xong em làm tiếp".
2. Ứng dụng chưa mở thì mở (`open_app`); cửa sổ bị che thì `focus_app`; cần bật một cài đặt trong ứng dụng thì tự mở cài đặt đó và bật.
3. **Cái gì em bấm được thì tự bấm. Cái gì không bấm được thì nhờ anh, nói đúng một việc anh cần làm**: hộp xin quyền của hệ điều hành, hỏi mật khẩu máy hoặc Touch ID, công tắc quyền riêng tư, đăng nhập, mã xác thực, CAPTCHA. Sau khi anh làm, kiểm tra lại rồi tự làm tiếp, không bắt anh nhắn lại nhiều lần.
