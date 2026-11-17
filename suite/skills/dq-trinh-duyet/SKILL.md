---
name: dq-trinh-duyet
description: "Điều khiển trình duyệt TISA như người thật khi việc không có MCP hay API: đăng nhập sẵn, bấm, gõ, đăng bài, tạo Fanpage. Có rào an toàn."
group: Điều hành
---
# Làm việc trên web bằng Trình duyệt TISA

Dùng khi việc **không có MCP hay API** và phải thao tác trực tiếp trên web: tạo Fanpage, đăng bài, lấy mã truy cập, nối công cụ, tìm kiếm trong trang cần đăng nhập, điền biểu mẫu. Anh (người dùng) đã đăng nhập sẵn trong cửa sổ trình duyệt riêng của TISA BOT. Việc của agent là **nhìn trang, tự tìm đúng nút, di chuột, bấm, gõ, kiểm tra kết quả**, như một nhân viên ngồi cạnh anh. Có MCP hoặc API làm được thì dùng chúng trước, trình duyệt là phương án khi không có.

## Hai công cụ
- `tisa_browser_look` (chỉ xem): `op=open url=...` mở trang (tự bật cửa sổ nếu chưa mở); `op=look` xem trang: chữ và danh sách nút, ô nhập đánh số `[n]`; `op=screenshot` chụp màn hình (đọc ảnh bằng công cụ đọc tệp khi cần nhìn bố cục); `op=tabs`; `op=status`.
- `tisa_browser_do` (thao tác): `click id=n`; `type id=n text=...`; `press key=Enter|Tab|Escape`; `scroll huong=down|up`; `select id=n value=...`; `upload id=n path=...`; `wait ms=... text=...`; `wait_user ly_do=...`; `back`, `forward`, `reload`, `new_tab url=...`, `switch_tab`, `close_tab`.

## Trình duyệt anh đã chọn (BẮT BUỘC làm đúng)
Anh chọn trình duyệt nào trong bảng thì **chỉ được dùng đúng trình duyệt đó**: nó là trình duyệt "đang dùng" (nhãn "AI đang dùng"). **Đầu mỗi việc có trình duyệt**, gọi `tisa_browser_look op=profiles`, đọc trình duyệt "đang dùng mặc định" và nói với anh một câu: "Em dùng trình duyệt <tên>". Mọi lệnh sau đó cứ để mặc định (hoặc truyền đúng `trinh_duyet` anh nói). **Không bao giờ** tự đổi sang trình duyệt khác, không mở trang ở trình duyệt khác, dù trình duyệt kia đang mở sẵn hay đang đăng nhập đúng trang cần. Trình duyệt anh chọn chưa mở thì `open` đúng nó; chưa đăng nhập đúng tài khoản thì báo anh, không lấy trình duyệt khác thay. Mỗi kết quả `look` ghi dòng "TRÌNH DUYỆT ĐANG DÙNG": nếu khác trình duyệt anh chọn thì dừng và báo anh.

## Nhiều trình duyệt (nhiều tài khoản)
Anh có thể tạo **nhiều trình duyệt** có tên (Trình duyệt 1, Facebook Sang, Fanpage Shop A...), mỗi cái đăng nhập tài khoản riêng, ví dụ 3 tài khoản Facebook cần làm việc cùng lúc. `tisa_browser_look op=profiles` liệt kê tên và trạng thái. Anh nói "dùng Facebook 2" hay "tài khoản thứ 3" thì truyền **`trinh_duyet="Facebook 2"` (tên hoặc số) ở MỌI lệnh** của việc đó (open, look, click, type...). Anh không nói thì dùng trình duyệt mặc định (cái anh đặt làm mặc định). Số `[n]` và mã tab chỉ đúng trong đúng trình duyệt đó. Nhiều tài khoản: làm xong tài khoản này rồi mới sang tài khoản kia, ghi rõ trình duyệt nào đã làm gì trong kết quả. Chuyển mã giữa hai trình duyệt: `dan_ma tu_trinh_duyet=<tên> tu_tab=... tu_id=... id=...`. Trình duyệt chưa mở thì `open` sẽ mở cửa sổ của nó; chưa đăng nhập thì `wait_user`. Không tự tạo, đổi tên, xóa trình duyệt: đó là việc của anh trong bảng. Có trình duyệt anh nhập từ hồ sơ Chrome có sẵn (đã mang theo đăng nhập từ Chrome của anh): dùng như trình duyệt khác, không cần đăng nhập lại; đừng nhập hay làm mới hồ sơ Chrome thay anh, và nhớ trình duyệt đó đang đăng nhập NHIỀU tài khoản của anh nên chỉ làm đúng việc được giao.

## Vòng làm việc (lặp tới khi xong)
1. **Mở và xem**: `open` rồi đọc kỹ kết quả `look` (chữ trang và danh sách `[n]`). Số `[n]` chỉ đúng cho lần look gần nhất. Mỗi lần trang đổi (bấm, mở menu, chuyển trang) phải `look` lại trước khi bấm tiếp.
2. **Nghĩ một bước**: mục tiêu của anh là gì, màn hình này đang ở đâu trong quy trình, nút nào đưa gần mục tiêu nhất. Chọn theo **ý nghĩa** của nhãn, không đoán vị trí.
3. **Làm đúng một bước** (`click`, `type`...), rồi `look` để **kiểm chứng bằng bằng chứng thật**: chữ xác nhận, địa chỉ trang đổi, ô đã có nội dung. Không có bằng chứng thì chưa coi là xong.
4. **Lệch thì sửa**: không thấy nút thì `scroll`, mở menu, hoặc thử nhãn khác; hộp thoại chắn thì xử lý hộp thoại; bị đưa về trang đăng nhập thì `wait_user`. Kẹt cùng một chỗ ba lần thì dừng, mô tả đúng chỗ kẹt (kèm `screenshot`) cho anh.
5. **Báo xong có bằng chứng**: nói đã làm gì, trang cuối (tên, địa chỉ), ảnh chụp nếu cần. Việc tạo, đăng: ghi lại đường dẫn hoặc mã vừa tạo.

## Luật an toàn (công cụ cũng tự chặn, không được tìm cách vòng)
- **Mật khẩu, mã xác thực (OTP, 2FA), số thẻ, CAPTCHA, kiểm tra "bạn là người"**: agent KHÔNG nhập, KHÔNG giải. Gặp thì nói với anh việc cần làm, rồi `wait_user ly_do="..."` để chờ anh làm ngay trong cửa sổ trình duyệt. Xong tự làm tiếp.
- **Chưa đăng nhập**: mở đúng trang đăng nhập, `wait_user ly_do="đăng nhập Facebook"`. Không đoán, không xin mật khẩu trong chat.
- **Thanh toán, mua, nạp tiền, nâng gói**: agent không bấm. Dẫn anh tới bước cuối, anh tự bấm. Trang ngân hàng, ví, sàn coin: không thao tác.
- **Đăng công khai, gửi tin, nộp biểu mẫu, xóa, đổi bảo mật, cấp quyền, đăng ký tài khoản**: công cụ trả `CAN_DUYET` kèm mã. Nói rõ với anh sẽ làm gì (nội dung đăng, nơi đăng) rồi chờ anh bấm **Duyệt** trong TISA BOT; sau đó mới gọi lại đúng lệnh đó với `duyet_id`. Chưa duyệt thì KHÔNG làm. Mỗi mã chỉ dùng một lần.
- Anh bấm **Dừng AI ngay** thì mọi lệnh trả `DA_DUNG`: ngừng hẳn, không thử lại.
- Chỉ làm trên tài khoản của chính anh, trong đúng việc được giao. Không làm hàng loạt, không spam, giữ nhịp như người (công cụ giới hạn tốc độ; thấy `CHAM_LAI` thì chờ).
- Không đọc ra, không ghi cookie, token, mật khẩu vào bộ não, kết quả hay tin nhắn.
- Việc đang chạy một mình (không có anh ngồi cạnh) mà cần anh duyệt hoặc đăng nhập: đặt phần việc ở trạng thái chờ anh, ghi rõ cần gì, không chờ vô hạn.

## Mức tự động anh đã chọn
Anh chọn ba mức trong bảng Trình duyệt TISA (op=status cho biết `muc`): **hoi_het** (xin duyệt từng thao tác bấm, gõ, chọn), **quan_trong** (mặc định: chỉ xin duyệt khi đăng, gửi, xóa, đổi bảo mật, đăng ký), **toan_quyen** (tự làm cả những việc đó, không hỏi). Cứ làm và theo phản hồi của công cụ: chỉ khi trả `CAN_DUYET` mới dừng chờ. Ở mức hoi_het đừng than phiền chuyện bị hỏi nhiều; gom việc thành ít bước nhất có thể. Ở mức toan_quyen vẫn nói rõ trong kết quả đã làm gì. **Ba thứ luôn dành cho anh ở mọi mức**: mật khẩu và mã xác thực và CAPTCHA, thanh toán, trang ngân hàng và ví.

## Đấu nối một nền tảng vào TISA BOT giúp học viên (MCP, API)
Học viên không biết cách nối. Việc của agent: tự điều khiển cả TISA BOT lẫn trang nền tảng, người dùng chỉ đăng nhập.
1. **Hiểu việc và xem hiện trạng**: nền tảng nào (Facebook Ads, TikTok, Google Ads, Zalo OA, Pancake...), muốn dùng để làm gì (chỉ xem số liệu hay cả bật, tắt, đổi ngân sách). Xem đã nối chưa bằng `tisa_connections` và trang Quảng Cáo, mục Tài khoản và kết nối (có hướng dẫn từng nền tảng và bảng "muốn dùng tính năng nào thì cần gì").
2. **Nghiên cứu cách nối**: `tisa_web_search` và `tisa_web_fetch` trang tài liệu chính thức của nền tảng. Ưu tiên MCP chính chủ, rồi API. Chọn quyền tối thiểu cần dùng (ví dụ chỉ đọc số liệu trước, quyền ghi chỉ khi anh muốn bật, tắt, đổi ngân sách).
3. **Nối MCP công khai không cần mã**: nếu có công cụ `tisa_add_mcp` và địa chỉ MCP chuẩn thì thêm thẳng, không cần mở trình duyệt.
4. **Cần mã hoặc đăng nhập**: mở trình duyệt với hai tab: một tab là trang TISA BOT đúng chỗ dán mã (ví dụ `http://127.0.0.1:7777/tisa-quang-cao/` hoặc tên miền anh đang dùng; trình duyệt này chưa đăng nhập TISA BOT thì `wait_user` một lần), một tab là trang nền tảng. Nói với anh: "Anh đăng nhập vào <tên trang> trong cửa sổ vừa hiện, xong em làm tiếp." rồi `wait_user`.
5. **Tự thao tác trên nền tảng** sau khi anh đăng nhập: tạo ứng dụng hoặc mã theo đúng quyền tối thiểu; bước chấp nhận điều khoản, cấp quyền theo luật duyệt của mức đang chọn.
6. **Chuyển mã mà không lộ**: khi trang hiện mã (token, app secret, đường dẫn MCP kèm khóa), `look` tab nền tảng (mã được che, thấy số `[n]` của khối chữ hoặc ô chứa mã), `switch_tab` về TISA BOT, `look` để lấy số ô cần dán, rồi `dan_ma tu_tab=<mã tab nền tảng> tu_id=<số khối mã> id=<số ô dán>`. Giá trị đi thẳng giữa hai trang, **không hiện cho agent, không vào chat, không vào nhật ký**. Không tự gõ mã bằng `type`.
7. **Hoàn tất và kiểm tra**: bấm Lưu, Thêm tài khoản hoặc Kiểm tra kết nối ở TISA BOT, đọc kết quả. Lỗi thì đọc thông báo (thiếu quyền, mã hết hạn, sai tài khoản quảng cáo), sửa rồi thử lại; kẹt thì mô tả đúng chỗ kẹt cho anh.
8. **Báo kết quả**: nối được gì, quyền nào đã cấp, dùng để làm gì tiếp (ví dụ báo cáo quảng cáo, tạo chiến dịch tạm dừng), và nhắc anh quyền ghi đang bật hay chưa. Không in mã ra.

## Kịch bản mẫu (làm theo ý nghĩa, giao diện web có thể khác)
**Đăng bài lên Fanpage** (luôn qua duyệt): 1) `open` Meta Business Suite (business.facebook.com) hoặc trang của Fanpage; 2) chọn đúng Fanpage anh nói; 3) bấm Tạo bài viết; 4) `type` nội dung đã được anh chốt (và chọn ảnh bằng `upload` từ Kho tư liệu nếu cần); 5) **dừng trước nút Đăng**, báo anh nội dung và Fanpage; 6) anh duyệt thì bấm Đăng, rồi `look` xác nhận bài đã lên, ghi đường dẫn bài.
**Tạo Fanpage mới**: mở trang tạo Trang của Facebook; điền tên, hạng mục, mô tả theo hồ sơ doanh nghiệp trong bộ não; hết các ô bắt buộc thì dừng trước nút Tạo Trang, xin duyệt (tạo là việc ra ngoài); sau khi tạo, điền thêm ảnh đại diện, ảnh bìa từ Kho tư liệu, thông tin liên hệ; báo đường dẫn Fanpage.
**Lấy mã truy cập hoặc nối công cụ** (ví dụ Meta, Zalo OA): đi theo hướng dẫn của trang Quảng Cáo, mở trang nhà phát triển, tạo ứng dụng hoặc mã theo đúng quyền tối thiểu cần dùng; **khi trang hiện mã bí mật, đừng chép vào chat**: bảo anh tự bấm sao chép và dán vào ô trong TISA BOT. Bước chấp nhận điều khoản, cấp quyền: xin duyệt.
**Tìm kiếm trong trang cần đăng nhập** (ví dụ đối thủ, thư viện quảng cáo): `open`, `type` từ khóa vào ô tìm, `press Enter`, `look`, `scroll` để đọc thêm; ghi lại tên, đường dẫn, số liệu thấy được.

## Mẹo
- Ô nhập có chữ cũ: `type` tự xóa chữ cũ rồi gõ (đặt `xoa=false` nếu muốn gõ nối).
- Danh sách chọn thật (`danh sách chọn`) dùng `select`; menu tự vẽ thì `click` mở rồi `click` từng mục.
- Trang tải chậm: `wait text="..."` chờ một chữ cụ thể thay vì chờ mù.
- Nội dung quan trọng thấy qua `look` bị cắt: `scroll` và `look` lại, hoặc `screenshot`.
