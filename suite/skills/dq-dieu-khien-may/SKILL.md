---
name: dq-dieu-khien-may
description: "Điều khiển máy tính của anh như người thật: nhìn màn hình, di chuột, bấm, gõ, mở ứng dụng, thư mục. Không xóa tệp. Có 3 mức tự động."
group: Điều hành
---
# Điều khiển máy tính của người dùng

Dùng khi việc phải làm **trên chính máy tính** của anh: mở màn hình desktop, tìm thư mục, bấm vào tệp, mở hoặc dùng một ứng dụng, thao tác trong phần mềm không có MCP hay API. Chạy ngay trên máy này (macOS, Windows), không tải gì lên mạng. Việc trên web dùng Trình duyệt TISA (skill `dq-trinh-duyet`), không dùng cái này. Đọc, ghi, tìm tệp bằng công cụ tệp có sẵn thì **luôn tốt hơn bấm chuột**: chỉ dùng điều khiển máy khi phải thao tác trong giao diện một ứng dụng.

## Hai công cụ
- `tisa_desktop_look` (chỉ xem): `op=screenshot` chụp màn hình (ảnh được gửi kèm ngay trong kết quả để nhìn, không cần mở tệp); `op=zoom x y x2 y2` phóng to một vùng của ảnh gần nhất để đọc chữ nhỏ; `op=windows` ứng dụng đang mở; `op=front` ứng dụng đang ở trước; `op=permissions` kiểm tra quyền; `op=status`.
- `tisa_desktop_do` (thao tác): `click`, `double_click`, `right_click` (x, y); `move`; `drag` (x, y, x2, y2); `scroll` (dy, dương là xuống); `type` (text; tiếng Việt gõ được; thêm `kieu=phim` để gõ từng phím thật cho máy tính bỏ túi, trò chơi, phím tắt); `key` (ví dụ `cmd+space`, `enter`, `ctrl+c`, `alt+tab`); `open_app` (name); `open_path` (path: mở thư mục hoặc tệp bằng ứng dụng mặc định); `focus_app` (name); `quit_app` (name); `wait` (ms); `mo_khoa` (mở khóa màn hình đăng nhập Mac, xem luật an toàn bên dưới).

## Vòng làm việc (lặp tới khi xong)
1. **Nhìn**: `screenshot`, xem ảnh gửi kèm. Chữ nhỏ thì `zoom` vùng đó. Tọa độ (x, y) trong ảnh đúng bằng tọa độ để bấm, gốc ở góc trên trái. Kết quả không kèm ảnh (công cụ báo chụp lỗi, ảnh đen, máy khoá) thì nói thật với anh và làm theo thông báo (mở khoá máy, bật quyền), tuyệt đối không đoán nội dung màn hình.
2. **Nghĩ một bước**: mục tiêu của anh là gì, màn hình đang ở đâu, nút nào đưa gần mục tiêu nhất. Chọn theo chữ trên nút, không đoán.
3. **Làm đúng một bước** (bấm, gõ, mở). Từ V3.20 mỗi lệnh bấm, gõ, nhấn phím, cuộn, kéo, mở ứng dụng **tự kèm ảnh chụp mới**, nên KHÔNG gọi thêm `screenshot` chỉ để xem kết quả (đặt `chup_sau=false` nếu không cần ảnh; `cho_ms` nếu giao diện đổi chậm). Việc gồm nhiều thao tác liền nhau thì dùng MỘT lệnh `op=nhieu_buoc cac_buoc=[{op,x,y,text,key...}]` (tối đa 15 bước, một ảnh cuối, bước bị chặn thì dừng) để khỏi mất thời gian từng lượt. Xem ảnh trả về để **kiểm chứng**. Không thấy thay đổi thì đừng bấm lại ngay: xem ảnh, có thể ứng dụng chưa kịp, hoặc hộp thoại đang chắn.
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
- **Mở khóa máy Mac** (anh nói "mở khóa máy", "mở khóa màn hình", "máy đang khóa", "unlock"): gọi NGAY `tisa_desktop_do op=mo_khoa`, không hỏi lại, không bảo anh "nhắn qua Zalo hay dashboard" (anh đã nhắn rồi). KHÔNG dùng `type`, `key` hay `click` (các op đó vẫn bị chặn ở màn hình khóa). Mật khẩu TISA BOT tự lấy từ Keychain: anh nhập MỘT lần ở **TISA BOT → Điều khiển của AI → tab Máy tính → Mở khóa máy** (ô nhập được kiểm đúng với máy rồi mới cất; có công tắc bật/tắt). **Tuyệt đối không hỏi, không nhận, không đọc lại mật khẩu trong chat, không truyền mật khẩu qua tham số** (có tham số kiểu mật khẩu là bị từ chối). Chat nào trong dashboard TISA BOT cũng được (kể cả chat với cộng sự); Zalo thì phải là Zalo anh đã bấm "Đây là Zalo của anh" ở Cài đặt. Nhóm chat, khách, bot Fanpage, việc nền: công cụ trả `TU_CHOI`, đừng tìm cách vòng. Mỗi lần cần anh bấm Duyệt (`CAN_DUYET`, gọi lại với `duyet_id`) trừ khi phiên đang Toàn quyền. Công cụ tự kiểm mật khẩu lưu có khớp mật khẩu máy không TRƯỚC khi gõ (`SAI_MAT_KHAU_LUU` = không gõ, không tốn lần thử: bảo anh nhập lại ở Cài đặt), tự đánh thức màn hình, chờ tới 15 giây cho máy mở, và nếu mật khẩu đã kiểm đúng mà lần gõ đầu bị nuốt thì thử lại một lần. `TAT` = anh đang tắt tính năng hoặc chưa nhập mật khẩu: chỉ anh đường vào Cài đặt ở trên. `CHUA_CAI_MAT_KHAU` tương tự. Thất bại 3 lần thì dừng 30 phút (`DA_DUNG_THU`): báo anh (anh bấm "Cho thử lại" ở Cài đặt), không thử mật khẩu khác. `KHONG_MO_DUOC` kèm câu "mật khẩu ĐÚNG": nói thật là máy chưa nhận phím, KHÔNG nói sai mật khẩu. Sau khi gõ công cụ tự chụp màn hình: xem ảnh để chắc đã vào màn hình chính. Gặp `CAN_NGUOI_DUNG` (hộp Touch ID, mã khóa, xác minh) thì dừng và báo anh. Windows: màn hình khóa nằm ngoài tầm của chương trình chạy trong phiên đăng nhập nên chưa mở khóa từ xa được, nói thật như vậy. Mỗi lần dùng đều có nhật ký (giờ, kênh, kết quả), không có mật khẩu.
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

## Việc mới (18/11/2026): Chrome đúng hồ sơ, gõ tiếng Việt, quay màn hình, việc nền dài
- **Chỉ dùng đúng hồ sơ Chrome anh đã chọn.** `op=chon_chrome` xem hồ sơ đã chọn (đổi thì anh phải bấm Duyệt, kể cả khi Toàn quyền). `op=mo_chrome url=...` (bỏ trống `ho_so`) mở trang đúng hồ sơ đó; xin hồ sơ khác trả `KHOA_HO_SO`: **không tìm cách mở hồ sơ khác** (có thể chưa đăng nhập tài khoản). `open_app Chrome` cũng chỉ đưa đúng hồ sơ đã chọn lên.
- **Chống chen ngang:** trước khi `type`/`key` vào trình duyệt, công cụ tự kiểm có thứ khác đang điều khiển trình duyệt không (tiện ích như Claude in Chrome, chromedriver, playwright nối vào Chrome...). Có thì trả `BI_CHEN` kèm nguyên nhân: báo anh rõ nguyên nhân, đừng gõ mù. `op=kiem_chen` xem trước.
- **Gõ tiếng Việt:** `type` có chữ có dấu tự **dán qua clipboard** (không gõ từng phím, tránh Telex). Chỉ dùng `kieu=phim` khi thật sự cần phím (máy tính bỏ túi, phím tắt).
- **Quay và chụp màn hình:** `op=chup_cua_so ung_dung=<tên> mo_ta=<mô tả>` chụp đúng cửa sổ; `op=quay_bat ung_dung=<tên> giay=<s> mo_ta=<mô tả>` / `op=quay_dung`. Tệp lưu ở brain: `04-ket-qua/<YYYY-MM>/<ngày>-<mô tả>/`. Không quay cửa sổ mật khẩu, ví, ngân hàng.
- **Việc nền dài (dựng video nhiều giờ):** việc nền của TISA BOT tự giữ máy thức. Việc tự chạy ngoài khung đó thì `op=giu_may_thuc ly_do=... phut=...` (xong `op=tha_may`). Muốn máy tự mở khóa lại nếu khóa giữa chừng: `op=giu_may_thuc tu_mo_khoa=true` (chỉ làm khi chính anh nhắn từ dashboard hoặc Zalo của anh, anh duyệt, mật khẩu lấy từ Keychain, tối đa 3 lần thử).
- **Cần người thật** (Touch ID, mã khóa, CAPTCHA, OTP): `op=cho_nguoi_that ly_do=...`: TISA BOT báo anh một tin ngắn, tạm dừng đúng chỗ, tự làm tiếp khi anh xong. Tuyệt đối không tự vượt các bước này.

## Thiếu quyền thì HƯỚNG DẪN, không dừng ở "em không làm được" (cập nhật 18/11/2026)
TISA BOT tự cài quyền lần đầu: khi mở lần đầu nó hiện hộp xin quyền của máy, mở đúng trang Cài đặt và chờ người dùng bật. Máy (macOS) **không cho phần mềm tự bật quyền cho chính nó**, nên người dùng phải bấm công tắc; việc của em là chỉ họ thật cụ thể:
1. Người dùng ra lệnh mà công cụ trả `CHUA_CAP_QUYEN`/`CAN_QUYEN` hoặc em không xem được màn hình, không bấm được: **KHÔNG nói "em chưa đọc được màn hình/chưa bấm được" rồi dừng.** Gọi ngay `tisa_desktop_do op=cai_dat_quyen` (hiện hộp xin quyền, mở sẵn trang Cài đặt, chờ).
2. Nói người dùng MỘT câu: "Em cần anh/chị bật một công tắc quyền để em điều khiển máy, em chỉ từng bước ngay đây". Rồi đọc **từng bước** trong kết quả `op=huong_dan_quyen` (có cho Mac và Windows), nói rõ bấm vào đâu, chữ nào trên màn hình, và hỏi họ đang thấy gì nếu họ kẹt. Có thể chụp màn hình (`tisa_desktop_look op=screenshot`) để chỉ đúng chỗ.
3. Người dùng làm xong thì gọi lại `op=cai_dat_quyen` để kiểm tra rồi **làm tiếp đúng việc họ đã giao**, không bắt họ ra lệnh lại.
4. Các quyền: Trợ năng (chuột, bàn phím), Ghi màn hình (xem, quay), Tự động hóa (điều khiển ứng dụng, Chrome), thư mục Màn hình nền, Tài liệu, Tải xuống, Truy cập toàn bộ ổ đĩa (đọc, sao chép mọi thư mục), và công tắc Chrome `chrome://inspect/#remote-debugging` để TISA BOT dùng đúng Chrome của họ. Windows gần như không cần: chỉ bấm Có ở hộp UAC, hoặc chạy lại ứng dụng nếu nó đang chạy bằng quyền quản trị.
5. **Giới hạn giữ nguyên dù đã bật hết quyền:** không xóa tệp của người dùng; không bấm bất cứ bước nào tốn tiền (thanh toán, mua, nạp, nâng gói, đăng ký gói); không tự vượt mật khẩu, OTP, CAPTCHA, Touch ID.


## Chuột riêng của TISA BOT (macOS và Windows, V3.20, mặc định bật)

Anh muốn vừa làm việc ở app khác vừa để TISA BOT làm việc, nên TISA BOT KHÔNG dùng con chuột và bàn phím thật của anh:
- Bấm, kéo, cuộn đi thẳng vào cửa sổ ở điểm đó; nút bấm, ô tích, liên kết, mục menu được bấm bằng Trợ năng (chạy cả khi cửa sổ nằm sau). Con trỏ của TISA BOT là mũi tên cam, kèm viền cam nhẹ quanh màn hình lúc nó thao tác.
- `type`, `key` đi vào cửa sổ vừa bấm gần nhất (10 phút), hoặc truyền `ung_dung="<tên ứng dụng>"`. Chưa bấm gì mà gõ thì nhận `CHUA_CO_DICH`: bấm vào ô cần gõ trước. Em KHÔNG gõ vào ứng dụng anh đang dùng.
- Cửa sổ bị che: `tisa_desktop_look op=screenshot ung_dung="<tên>"` chụp riêng cửa sổ đó, rồi `click/type/scroll` kèm `ung_dung="<tên>"` theo toạ độ TRONG ảnh cửa sổ.
- Đừng `focus_app` (giành màn hình của anh): bỏ qua. `open_app` mở ở nền.
- Ứng dụng chỉ nhận chuột khi đang ở trước (trò chơi, vài ứng dụng tự vẽ): `op=chuot_che_do che_do=that`, nói anh biết lúc đó anh đừng chạm chuột, xong việc đổi lại `rieng`.
- Cửa sổ thu nhỏ hoặc ở màn hình ảo (Space) khác thì chưa chụp, chưa bấm được: nói anh.

Windows (cùng cách dùng, khác cách làm bên trong): gửi tin nhắn cửa sổ thẳng vào đúng cửa sổ con; nút Win32 bấm bằng BM_CLICK; gõ chữ bằng WM_CHAR (tiếng Việt giữ dấu); chụp riêng cửa sổ bằng PrintWindow kể cả khi bị che. `ung_dung` là tên tiến trình (chrome, notepad, excel) hoặc một phần tiêu đề cửa sổ. Giới hạn: phần này CHƯA kiểm trên Windows thật; phím tắt kiểu ctrl+c cần cửa sổ ở trước; ứng dụng tự vẽ hoặc UWP có thể không nhận chuột khi ở nền; open_app chưa mở nền được. Gặp vậy thì `op=chuot_che_do che_do=that`.
