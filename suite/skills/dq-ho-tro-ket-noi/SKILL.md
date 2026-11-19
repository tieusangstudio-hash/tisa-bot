---
name: dq-ho-tro-ket-noi
description: "Kết nối giúp anh một ứng dụng vào TISA BOT (MCP, API, khóa, tài khoản): đọc màn hình TISA và hướng dẫn, hỏi anh chọn web và trình duyệt, tự thao tác lấy mã rồi dán vào TISA BOT. Kích hoạt khi anh nói: kết nối, đấu nối, nối, lấy API key, lấy token, cấp quyền cho TISA BOT."
group: Điều hành
---
# Hỗ trợ kết nối ứng dụng vào TISA BOT

> Từ V3.25 mọi nút "Nhờ TISA BOT kết nối giúp" giao việc cho cộng sự **Đạt Đấu Nối** (`tisa-dau-noi`). Phương pháp làm việc (nghiên cứu trước, làm liên tục, tự gỡ lỗi, tự ghi kinh nghiệm), thang dễ đến khó và sổ tay từng công cụ nằm ở kỹ năng **`dq-dau-noi-cong-cu`**: đọc nó trước, rồi dùng skill này cho phần thao tác trên màn hình.

Anh (chủ doanh nghiệp, thường không rành kỹ thuật) nhờ nối một ứng dụng (Meta Ads, Fanpage, Zalo OA, TikTok Ads, Google, Pancake, Telegram, Sheets...) vào TISA BOT. Việc của bạn: **tự đọc, tự nghiên cứu, tự thao tác** như nhân viên ngồi cạnh; anh chỉ chọn web, đăng nhập và duyệt những bước nhạy cảm. Xưng "em", gọi "anh". Làm theo `dq-trinh-duyet` (luật an toàn, mức tự động) và `dq-dieu-khien-may` (khi cần dùng máy tính).

## Làm LUÔN, không vòng vo (anh bấm "Bắt đầu nhờ AI" là đã giao việc)
- **Việc trong TISA BOT (xem thẻ kết nối, mở thẻ, chọn ô, bấm Kết nối/Lưu) làm bằng lệnh điều khiển giao diện: `tisa_browser_do op=ui_tisa`** (`lenh=xem`, `mo_the ten=<thẻ>`, `chon_o truong=<ô>`, `bam nhan=<nút>`). Lệnh chạy thẳng trong cửa sổ TISA BOT đang mở, **không dùng chuột, bàn phím**, nên không bị cửa sổ khác đè (Zalo, Chrome...) và không vướng khi anh đang gõ. **KHÔNG dừng lại chỉ vì thấy cửa sổ khác hay anh đang gõ**; đó không phải lý do để dừng.
- **KHÔNG mở TISA BOT trong trình duyệt (Chrome), KHÔNG bắt anh đăng nhập lại TISA BOT, KHÔNG nhờ anh tự chạy lệnh hay tự copy file** khi em làm được.
- Điều khiển máy tính (chuột, chụp màn hình) chỉ là **đường dự phòng** khi `ui_tisa` báo `KHONG_CO_CUA_SO`.
- Việc trên web của nền tảng (tạo ứng dụng, lấy mã) làm bằng **trình duyệt anh đã chọn**.
- Chỉ dừng hỏi anh khi thật sự cần: chọn web (hộp hoi_mo), đăng nhập nền tảng, mật khẩu/OTP/CAPTCHA, thanh toán, duyệt phiên đăng nhập, và các bước nhạy cảm theo mức tự động.
- **Lệnh trước đó trong cuộc chat này từng báo lỗi (ví dụ "Browser context management is not supported") thì thử lại**: máy chủ đã được sửa, đừng dựa vào kết quả cũ.
- Mở đầu chỉ cần **một câu** nói em sẽ làm gì, rồi làm.

## Luật cứng
- **Mã, token, khóa, đường dẫn MCP kèm khóa**: KHÔNG đọc ra, KHÔNG chép vào chat, kết quả, bộ nhớ, tệp. Chỉ chuyển bằng `dan_ma` (giá trị đi thẳng từ trang nền tảng sang ô của TISA BOT mà bạn không nhìn thấy). Không tự gõ mã bằng `type`.
- **Mật khẩu, mã xác thực (OTP, 2FA), CAPTCHA, thẻ, thanh toán, nạp tiền, nâng gói**: không làm. Nói anh làm trong cửa sổ trình duyệt rồi `wait_user`.
- **TUYỆT ĐỐI không mở trình duyệt nào khác ngoài trình duyệt anh đã chọn**: không chạy lệnh có thể tự mở trình duyệt (`<công cụ> login`, ví dụ `notebooklm login`; `playwright`, `chromium`, `selenium`, `puppeteer`, `open -a "Google Chrome"`...). Những lệnh đó mở Chromium mới chưa đăng nhập gì và bắt anh đăng nhập lại, trái ý anh. Trang cần đăng nhập mà trình duyệt đã chọn chưa đăng nhập thì `wait_user` ngay trong trình duyệt đó.
- **Chỉ dùng đúng trình duyệt anh đã chọn** (đầu việc: `tisa_browser_look op=profiles`, nói "Em dùng trình duyệt <tên>"). Không tự đổi.
- **Chỉ xin quyền tối thiểu** cần cho việc anh muốn (xem số liệu thì quyền đọc; quyền ghi chỉ khi anh muốn bật, tắt, tạo, đổi). Nói rõ quyền nào sẽ cấp.
- Chấp nhận điều khoản, cấp quyền OAuth, tạo ứng dụng/tài khoản, bấm Lưu thay đổi bảo mật: theo luật duyệt của mức tự động (công cụ trả `CAN_DUYET` thì nói rõ làm gì rồi chờ anh duyệt).
- Không đoán. Chưa chắc ở đâu thì đọc hướng dẫn, chụp màn hình, hoặc hỏi anh đúng một câu.
- Kẹt cùng một chỗ 3 lần: dừng, nói đúng chỗ kẹt (kèm ảnh chụp) và việc anh cần làm.

## Quy trình (làm lần lượt, báo anh một câu ngắn ở mỗi bước lớn)

### 1. Hiểu yêu cầu
Nền tảng nào, muốn dùng để làm gì (chỉ xem hay cả tạo, sửa, bật tắt), tài khoản nào. Thiếu thì hỏi **một** câu rồi làm tiếp. Yêu cầu nói bằng giọng thường ngắn, đoán ý theo ngữ cảnh ("nối Meta" thường là Meta Ads hoặc Fanpage: hỏi một câu nếu khác nhau về cách nối).

### 2. Đọc màn hình TISA BOT
- `tisa_connections`: đã nối những gì. Nền tảng đã nối rồi thì nói với anh và hỏi có muốn nối thêm tài khoản khác hay sửa quyền không.
- `tisa_browser_do op=ui_tisa lenh=mo_the ten="<tên thẻ>"`: TISA BOT tự mở trang Kết nối, mở đúng thẻ và trả về **tên hộp, các ô cần điền, các nút** (chỉ chữ nhãn). Thẻ nhiều dịch vụ (Google) thì thêm `dich_vu="Gmail"`. Không thấy thẻ thì kết quả liệt kê các thẻ đang có. Đọc kỹ ô nào cần mã gì; thẻ thường có link **Hướng dẫn**, mở bằng `tisa_web_fetch`.
- `lenh=xem` bất cứ lúc nào để biết TISA BOT đang hiện gì (hộp, ô, nút, thông báo lỗi).

### 3. Nghiên cứu cách nối
`tisa_web_search` và `tisa_web_fetch` tài liệu chính thức của nền tảng (ưu tiên MCP chính chủ, rồi API chính thức). Rút ra: cần loại mã gì, tạo ở trang nào, quyền tối thiểu, có tốn tiền hay cần xét duyệt không (ví dụ ứng dụng Meta ở chế độ Development). Nói anh **kế hoạch 3 đến 6 dòng**: sẽ mở web nào, làm gì, cần anh làm gì (đăng nhập, bấm duyệt).

Nếu chỉ cần thêm một MCP công khai không cần mã: dùng `tisa_add_mcp` với địa chỉ chuẩn, không cần mở trình duyệt.

### 4. Hỏi anh chọn web và trình duyệt
Gọi `tisa_browser_do op=hoi_mo ly_do="<vì sao cần mở>" trang=[{"ten":"...","url":"https://...","mo_ta":"..."}, ...]` với 1 đến 4 trang **chính thức** (đúng tên miền của nền tảng, ví dụ developers.facebook.com, business.facebook.com, ads.tiktok.com, oa.zalo.me, console.cloud.google.com). TISA BOT hiện hộp cho anh chọn trang và trình duyệt; lệnh chờ tới khi anh chọn rồi tự mở trang đó. **Không tự mở web nền tảng khi chưa qua hộp này** (trừ trang của chính TISA BOT). Bị `TU_CHOI` hoặc `HET_GIO` thì hỏi anh muốn làm gì tiếp, đừng tự mở. Đây là hộp trên chính cửa sổ TISA BOT; anh chọn xong trang tự mở, không cần anh làm gì thêm.

### 5. Đăng nhập
`look` trang vừa mở. Chưa đăng nhập: nói "Anh đăng nhập vào <tên trang> trong cửa sổ vừa hiện, xong em làm tiếp" rồi `wait_user ly_do="đăng nhập <tên>"`. Có OTP, CAPTCHA: `wait_user`.

### 6. Thao tác lấy mã
Theo vòng của `dq-trinh-duyet`: `look`, nghĩ một bước, làm một bước, `look` kiểm chứng. Tạo ứng dụng hoặc khóa theo quyền tối thiểu. Mỗi khi trang đổi phải `look` lại trước khi bấm tiếp. Trang hiển thị mã: `look` sẽ che mã và cho số `[n]` của khối chứa mã; ghi lại số đó. Một số nền tảng chỉ hiện mã một lần: **đừng rời trang** trước khi `dan_ma` xong.

### 7. Dán mã vào TISA BOT (không lộ)
**Cách chính: điều khiển giao diện TISA BOT bằng lệnh, dán thẳng vào ô.**
1. Trang nền tảng (tab trong trình duyệt đã chọn) đang hiện mã; `look` lấy số `[n]` của khối chứa mã và mã tab (`op=tabs`).
2. `tisa_browser_do op=ui_tisa lenh=mo_the ten="<thẻ>" truong="<nhãn ô>"` (nếu hộp đã mở thì `lenh=chon_o truong="<nhãn ô>"`): ô cần dán **đang có con trỏ**.
3. Gọi ngay `tisa_browser_do op=dan_vao_tisa tu_tab=<mã tab nền tảng> tu_id=<số [n] khối mã>`. Giá trị đi thẳng từ trang nền tảng vào ô (em không nhìn thấy), ô hiện **chấm tròn**. Nhiều ô (App ID, App Secret, Token): lặp lại từng ô (`chon_o` rồi `dan_vao_tisa`). Trả `KHONG_DAN_DUOC` thì đọc lý do, `chon_o` lại đúng ô rồi gọi lại.
4. **Không cố đọc lại ô vừa dán.** `tisa_browser_do op=ui_tisa lenh=bam nhan="Kết nối"` (hoặc Lưu, Kiểm tra), rồi đọc kết quả ở phần "Thông báo". `lenh=bam` không bấm nút xóa, gỡ, đăng xuất.

**Đường dự phòng:** `ui_tisa` báo `KHONG_CO_CUA_SO` (TISA BOT chưa mở trên màn hình): nhờ anh mở TISA BOT; vẫn không được và máy tính được phép dùng thì điều khiển máy tính (`focus_app name="TISA BOT"`, click ô, rồi `dan_vao_tisa`); cuối cùng mới tới mở tab TISA BOT trong trình duyệt (`new_tab url=<trang_tisa>`, `dan_ma`). Nói rõ với anh vì sao phải dùng đường dự phòng.

**Kết nối đòi cookie phiên đăng nhập** (ví dụ Google NotebookLM: ô "Phiên đăng nhập (dán storage_state.json)"): KHÔNG chạy `notebooklm login` hay lệnh nào mở trình duyệt khác, KHÔNG bảo anh tự chạy lệnh trong Terminal. Trình duyệt anh đã chọn thường đã đăng nhập sẵn tài khoản đó. Làm thế này:
0. **Mở trang trong đúng trình duyệt đã chọn để xác nhận đã đăng nhập**: `tisa_browser_look op=open url=https://notebooklm.google.com` (cửa sổ trình duyệt hiện ra cho anh thấy), `look` xem có danh sách notebook hoặc tên tài khoản không. Thấy trang đăng nhập thì `wait_user ly_do="đăng nhập Google"` để anh đăng nhập ngay trong cửa sổ đó, rồi `look` lại. Chỉ khi đã đăng nhập mới lấy phiên. **Lưu ý thật:** trình duyệt nhập từ hồ sơ Chrome thường KHÔNG giữ được đăng nhập Google (Google tự hủy phiên bị chép), dù có cookie tên SID. Đừng tin cookie, tin những gì thấy trên trang. Cần anh đăng nhập Google một lần trong trình duyệt TISA thì nói thẳng, đừng thử đi đường khác. Lưu ý: `notebook.google.com` hiện tên "Gemini Notebook"; nếu thẻ NotebookLM báo lỗi giao thức sau khi nối được phiên, nói thật là thư viện notebooklm-py có thể đã lỗi thời và gợi ý đường khác.
1. Nói anh một câu: "Em lấy phiên đăng nhập Google từ trình duyệt <tên> đưa vào TISA BOT, em không nhìn thấy nội dung" (đang Toàn quyền thì làm luôn, không chờ duyệt).
2. `tisa_browser_do op=ui_tisa lenh=mo_the ten="NotebookLM" truong="Phiên đăng nhập"`: TISA BOT mở thẻ và đặt con trỏ vào ô "Phiên đăng nhập".
3. `tisa_browser_do op=dan_vao_tisa kieu=phien_trinh_duyet mien=google.com`. Lệnh tự chờ anh bấm Duyệt trên thẻ trong TISA BOT (tối đa 5 phút) rồi tự làm tiếp trong cùng một lệnh. Chỉ khi trả `CAN_DUYET` (hết 5 phút) mới gọi lại với `duyet_id` sau khi anh duyệt. Trả `CHUA_DANG_NHAP` thì `open` trang Google trong đúng trình duyệt đã chọn, `wait_user` để anh đăng nhập, rồi gọi lại. Cần anh duyệt, trừ khi trình duyệt web đang ở mức Toàn quyền (khi đó tự làm, không hỏi lại).
4. `op=ui_tisa lenh=bam nhan="Kết nối"`, đọc thông báo; kiểm tra thẻ chuyển sang Đã kết nối (`tisa_connections`), thử một thao tác chỉ đọc. Thẻ yêu cầu `uv` mà máy chưa có thì báo rõ và hướng dẫn cài. Nhắc anh: phiên này tương đương đăng nhập tài khoản Google, nên giữ mức Chỉ đọc trừ khi anh muốn ghi.

### 8. Kiểm tra nối được thật
`tisa_connections` hoặc xem thẻ chuyển sang **Đã kết nối**; thử một thao tác chỉ đọc nhỏ (liệt kê tài khoản quảng cáo, đọc 1 trang, gửi thử tin tới chính anh nếu anh cho). Lỗi (thiếu quyền, mã hết hạn, sai tài khoản, ứng dụng chưa được duyệt): đọc đúng thông báo, sửa, thử lại; sửa được thì nói rõ đã sửa gì.

### 9. Báo kết quả (ngắn, thật)
Nối được gì, quyền nào đã cấp (và quyền nào CHƯA cấp), dùng để làm gì tiếp (ví dụ "xem báo cáo quảng cáo", "tạo chiến dịch ở trạng thái tạm dừng"), còn cần anh làm gì. **Không in mã.** Nối chưa xong thì nói bước đã xong, bước kẹt, cách làm tiếp. Dọn: đóng tab thừa của nền tảng nếu anh không cần.

## Khi anh đổi ý giữa chừng
Anh bảo dừng hoặc đổi sang nền tảng khác thì dừng ngay, không làm tiếp việc cũ, không để dở biểu mẫu chưa lưu mà không báo.

## Gặp tình huống thường thấy
- **Meta (Facebook) Ads**: MCP chính chủ của Meta cần đăng nhập tài khoản (OAuth) ở thẻ **Meta Ads (MCP chính chủ)**: bấm Đăng nhập tài khoản trong TISA BOT, anh đăng nhập và cấp quyền. Muốn API riêng (tự tạo app): mở developers.facebook.com, tạo app, thêm Marketing API, tạo token quyền `ads_read` (xem) và `ads_management` (bật tắt, đổi ngân sách) chỉ khi anh muốn ghi. Ứng dụng ở chế độ Development vẫn dùng được cho tài khoản của chính anh.
- **Fanpage / Messenger**: thẻ **Kết nối Meta**, bấm Kết nối Fanpage, anh đăng nhập và chọn Trang.
- **Zalo OA**: cần OA đã xác minh; lấy ID ứng dụng và khóa ở developers.zalo.me.
- **TikTok Ads**: ads.tiktok.com và trang nhà phát triển; cần tài khoản quảng cáo và quyền Admin.
- **Google (Ads, Sheets, Drive, Gmail)**: thường đăng nhập Google OAuth ngay ở thẻ; Ads còn cần Developer Token (xin duyệt, mất vài ngày): nói rõ để anh khỏi chờ.
Giao diện web các nền tảng đổi thường xuyên: làm theo **ý nghĩa nhãn** hiện trên màn hình, không theo vị trí nhớ sẵn.

## Nút "Kết nối tự động" (V3.02)
Ở trang Kết nối, mỗi thẻ có nút **⚡ Kết nối tự động**. Bấm là TISA BOT tự cấp Toàn quyền (trình duyệt và máy, không xóa tệp) rồi gửi cho bạn một lời nhờ có sẵn **mục tiêu, thứ cần lấy, trang web và các bước chi tiết** của đúng công cụ đó (nguồn: `dashboard/tisa-ket-noi-huong-dan.json`, tra tài liệu chính thức ngày 17/11/2026). Làm theo các bước đó; giao diện nền tảng khác mô tả thì tìm mục tương đương hoặc tra tài liệu chính thức. Làm từ đầu đến cuối, chỉ dừng nhờ anh ở: đăng nhập, mật khẩu, mã xác thực, quét QR, đồng ý quyền.

## Dùng lại tab đã đăng nhập (V3.02)
Trình duyệt TISA BOT đang chạy thường đã đăng nhập sẵn nhiều tài khoản. **Trước khi mở web: `tisa_browser_look op=tabs`.** Nền tảng đã có tab mở sẵn thì `switch_tab` dùng luôn (hoặc `hoi_mo`, nó tự chuyển sang tab có sẵn), KHÔNG mở Chrome mới, KHÔNG bắt anh đăng nhập lại. Chưa có tab thì mở TAB MỚI trong cùng trình duyệt, giữ nguyên các tab đang đăng nhập khác. Hộp chọn web của TISA BOT đã đánh dấu trang nào đã mở sẵn hoặc đã đăng nhập và mặc định chọn trình duyệt đang chạy.

## Tự làm trọn, không bắt anh dán tay (cập nhật 18/11/2026)
Anh muốn TISA BOT làm hết phần máy, chỉ dừng ở bước **chỉ người thật làm được**. Làm theo thứ tự:
1. **Tự vào trang nền tảng** bằng đúng trình duyệt/hồ sơ anh đã chọn (không đổi sang hồ sơ khác: `KHOA_TRINH_DUYET`/`KHOA_HO_SO` nghĩa là phải dùng cái đã chọn; thật sự cần đổi thì `op=doi_trinh_duyet`/`op=chon_chrome`, anh duyệt).
2. **Tự tạo khóa API hoặc token** theo quyền tối thiểu (tạo khóa là thao tác ra ngoài: nếu công cụ trả `CAN_DUYET` thì nói rõ làm gì rồi chờ anh duyệt, đừng tự bỏ qua).
3. **Tự chép khóa sang chỗ cần, không để giá trị lộ ra chat**: vào ô kết nối của TISA BOT bằng `dan_vao_tisa`/`dan_ma`; cần cất trong Keychain cho công cụ API (Drive, Bunny...) thì `tisa_browser_do op=luu_keychain tu_tab=<tab> tu_id=<số khối chứa giá trị> ten=<tên mục> [truong=<khóa>]` (anh duyệt một lần; giá trị đi thẳng từ trang vào Keychain). Không bao giờ tự gõ, đọc ra hay in khóa.
4. **Gặp bước chỉ người thật làm được** (Touch ID, mã khóa, CAPTCHA, OTP, màn hình khóa, hộp "Cho phép" của Google): không vượt. Gọi `tisa_browser_do op=wait_user ly_do=...` (trình duyệt) hoặc `tisa_desktop_do op=cho_nguoi_that ly_do=...` (máy): TISA BOT gửi anh một tin ngắn (dashboard, Zalo), **tạm dừng đúng chỗ đó**, rồi **tự làm tiếp khi anh làm xong**. Không bỏ cả phiên, không hỏi lại từ đầu.
5. **Thiếu kết nối** thì tự nêu đúng cần gì rồi làm tiếp khi có (bảng dưới), không bảo anh "tự làm đi".

### Kết nối thường thiếu và cái cần
| Kết nối | Cần gì | Cách có |
|---|---|---|
| **Google Drive (API, tệp lớn, đổi tên hàng loạt)** | OAuth client loại *Desktop app* (client_id, client_secret) rồi đăng nhập một lần | Mở console.cloud.google.com > APIs & Services: bật *Google Drive API*, màn hình đồng ý (người dùng thử là email của anh), tạo *OAuth client ID* loại Desktop. Cất hai giá trị: `op=luu_keychain ten=drive-client truong=client_id`, rồi `truong=client_secret`. Sau đó `tisa_drive_do op=dang_nhap` mở trang Google cho anh bấm **Cho phép** (đây là bước người thật; gặp Touch ID thì `cho_nguoi_that`). Khóa tự vào Keychain mục `tisa-bot-drive`. Công cụ Drive chỉ nhận tệp tới 10 MB: dùng `tisa_drive_do` cho tệp lớn. |

> **Drive cho Kho tư liệu (V3.34):** sau khi `tisa_drive_do op=dang_nhap_xem` báo đã nối, nhắc anh mở trang **Kho tư liệu**, thẻ Google Drive, bấm **Chọn thư mục** cho thư mục làm việc và thư mục nhận kết quả. Từ V3.34 kho khóa chạy cả Windows và Linux (tệp mã hóa trong thư mục dữ liệu của TISA BOT), không chỉ Mac Keychain.
| **Composio Drive** | Kết nối Composio chưa bật | Nói rõ: "Composio Drive chưa bật; em dùng `tisa_drive_do` (API trực tiếp) thay thế". Anh muốn bật Composio thì mở thẻ Composio trong TISA BOT và nối tài khoản Google. |
| **Bunny (Bunny.net, Stream/Storage)** | API Key (Account API key) và, nếu dùng Stream, Library ID + Stream API key | bunny.net > Account Settings > API Key (và Stream > Library > API). Cất: `op=luu_keychain ten=bunny truong=api_key`. Trang kết nối của Bunny trong TISA BOT dùng `dan_vao_tisa`. |
| **HeyGen (gốc)** | API Key HeyGen | app.heygen.com > Settings > API (Subscriptions & API). Tạo khóa gốc rồi `dan_vao_tisa` vào thẻ HeyGen hoặc `luu_keychain ten=heygen`. Tạo khóa có thể tốn credit/gói: nếu trang đòi nâng gói hoặc trả tiền thì **dừng, hỏi anh duyệt** (không tự chi tiền, đổi gói, nạp credit). |

### Giới hạn không được bỏ khi tự làm
- Chi tiền, thanh toán, đổi gói, nạp credit: luôn hỏi duyệt. Xóa dữ liệu vĩnh viễn, đổi mật khẩu hay bảo mật tài khoản: luôn hỏi duyệt. Đăng bài, nhắn khách, bật quảng cáo: hỏi anh trước.
- Không tự vượt OTP, CAPTCHA, Touch ID, mã khóa. Không ghi mật khẩu, OTP, token, khóa, số thẻ vào tệp, brain, log, chat.


## Chrome anh đã chọn (V3.20)

Bấm "Nhờ TISA BOT kết nối giúp" thì TISA BOT bắt anh chọn hồ sơ Chrome (tên và email tài khoản) nếu chưa chọn; lời nhờ kèm dòng "[Chrome anh đã chọn: ...]". Chỉ mở và làm việc trong ĐÚNG hồ sơ đó (`op=mo_chrome` không cần `ho_so`): KHÔNG mở Chrome mới, KHÔNG mở hồ sơ khác. Anh đổi hồ sơ ở nút "Đổi" trong cửa sổ trợ lý nổi. Trang chưa đăng nhập thì nhờ anh đăng nhập ngay trong hồ sơ đó rồi làm tiếp.


## MCP của Claude Code (V3.20)

Anh đã kết nối MCP bên Claude Code (Meta Ads, Google Drive, Canva...) thì TISA BOT dùng luôn, không cần kết nối lại bằng API hay MCP trong TISA BOT. Trang Kết nối có thẻ "Đã nối MCP của Claude Code vào TISA BOT" (chạy `claude mcp list` ở nền). Hỏi anh "kết nối Meta Ads" thì xem thẻ đó trước: đã nối (xanh) thì dùng công cụ `ads_*`, cần đăng nhập lại (cam) thì nói anh mở Claude Code, vào Connectors, đăng nhập lại; chưa có thì nói anh thêm Meta Ads ở Claude Code. Chỉ engine Claude dùng được các MCP này.


## Kết nối Meta (Fanpage, Messenger, Instagram, số liệu bài viết) - bổ sung 19/11/2026
Làm theo mục `ket-noi-meta` trong hướng dẫn và phần "Meta / Fanpage" ở `dq-dau-noi-cong-cu/references/kinh-nghiem-da-lam.md`. Ba điều hay sai:
1. **HTTPS trước tiên.** Nút Đăng nhập Facebook xám hoặc hộp báo cần HTTPS: bật Truy cập từ xa (hoặc tên miền riêng) và mở lại hộp, rồi mới làm tiếp. Địa chỉ quay về dán vào Meta phải là địa chỉ https đó.
2. **Hai ô quyền thêm để TRỐNG** (Nối cả Instagram, Đọc số liệu bài viết) khi nối lần đầu. Chỉ tick khi anh muốn dùng VÀ app Meta đã thêm đúng quyền (instagram_basic, instagram_manage_messages, instagram_manage_comments; read_insights). Sai thì Facebook báo "Invalid Scopes" và hỏng cả lần đăng nhập. Muốn thêm sau thì thêm quyền vào app, rồi ở Trang đã nối bấm Đổi token, tick ô, đăng nhập lại.
3. **Không báo xong sớm.** Sau khi nối bấm Kiểm tra ở Trang, đọc bảng kiểm tra; nhớ tick kênh vào một bot và bật bot. Chuyển app sang Live phải hỏi anh trước.
Gặp "Invalid Scopes": bỏ tick hai ô, đóng tab lỗi, bấm Đăng nhập Facebook lại. Không đổi quyền hay cài đặt khác của app khi chưa được anh đồng ý.
