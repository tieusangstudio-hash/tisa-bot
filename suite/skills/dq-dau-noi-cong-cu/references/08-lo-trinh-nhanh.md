# 08 - Lộ trình nhanh cho 10 yêu cầu hay gặp của chủ shop

Mỗi kịch bản: thứ tự thao tác + công cụ/op dùng ở từng bước. Chi tiết từng ô và lỗi: file 07. Tham số công cụ và mã trả về: file 06. Hiểu app: file 05.
Ký hiệu: **[NGƯỜI]** = chỉ người thật làm được (đăng nhập, mật khẩu, OTP, CAPTCHA, hộp Cho phép, quét QR, thanh toán). Gặp bước này: nói đúng MỘT việc, `tisa_browser_do op=wait_user ly_do="..."` (trình duyệt) hoặc `tisa_desktop_do op=cho_nguoi_that ly_do="..."` (máy), TISA báo anh qua dashboard/Zalo rồi tự làm tiếp.
Mở đầu MỌI kịch bản (3 lệnh, không bỏ): (a) `tisa_connections` xem đã nối chưa; (b) `tisa_browser_look op=profiles` rồi nói "Em dùng trình duyệt <tên>"; (c) `tisa_browser_look op=tabs` để dùng lại tab nền tảng đã đăng nhập (`switch_tab`), không mở Chrome mới. Mật khẩu/token/khóa: chỉ `dan_vao_tisa`, `dan_ma`, `luu_keychain`, không chép chat.
Mở web mới của nền tảng: `tisa_browser_do op=hoi_mo ly_do=... trang=[{ten,url,mo_ta}]` (hộp cho anh chọn web và trình duyệt), trừ khi đã có tab sẵn.

---
## 1. "Nối Meta Ads để xem báo cáo quảng cáo" (DỄ nếu có MCP Claude Code, VỪA nếu tự tạo app)

1. `tisa_connections`: có nguồn `claude_account` tên Meta Ads, hoặc công cụ `ads_*`/`mcp__claude_ai_Meta_Ads__*`? Hoặc đọc thẻ "Đã nối MCP của Claude Code" (`GET /tisa-claude-mcp/trang-thai?quet=1`).
2. Có và xanh: thử ngay `ads_get_ad_accounts` rồi `ads_insights_performance_trend` (chỉ đọc). Xong, báo anh tên tài khoản. Chỉ chạy bằng engine Claude (Models, Claude Code).
3. Thẻ báo `Needs authentication`: **[NGƯỜI]** anh mở Claude Code, Connectors, đăng nhập lại Meta Ads. Không phải hỏng.
4. Chưa có: `tisa_browser_do op=ui_tisa lenh=mo_the ten="Meta Ads"` rồi `lenh=xem` (đọc ô App ID, App Secret, nút "Lưu & mở trang đăng nhập").
5. `hoi_mo` developers.facebook.com/apps; **[NGƯỜI]** đăng nhập Facebook (Admin ad account). Dùng app sẵn nếu có, không thì Tạo ứng dụng (loại Business, trường hợp "Khác"), giữ **Development**, bỏ qua Xác minh doanh nghiệp/App Review.
6. Nhìn cột trái: "Sản phẩm" = giao diện cũ, "Trường hợp sử dụng" = mới; mở Đăng nhập bằng Facebook BẢN THƯỜNG, Cài đặt. Máy cá nhân: không điền redirect, mở TISA bằng `localhost`. VPS/miền: `ui_tisa lenh=xem` lấy Địa chỉ quay về dán nguyên văn + Miền ứng dụng.
7. Cài đặt ứng dụng, Thông tin cơ bản: `ui_tisa lenh=chon_o truong="App ID (Facebook)"` rồi `dan_vao_tisa tu_tab=<tab> tu_id=<n>`; lặp cho "App Secret (Facebook)" (Meta có thể bắt nhập lại mật khẩu: **[NGƯỜI]**).
8. `ui_tisa lenh=bam nhan="Lưu & mở trang đăng nhập"`; **[NGƯỜI]** đăng nhập, TICK đúng tài khoản quảng cáo, Cho phép. Bảng "Invalid Scopes" bấm OK.
9. Kiểm chỉ đọc: `meta_ads_accounts`, rồi `meta_ads_insights`. Không thấy tài khoản: thêm use case Marketing API, quyền `ads_read`, kết nối lại.
10. Bật/tắt/đổi ngân sách là việc KHÁC: nối ở trang **Quảng Cáo** bằng API (`ads_management`) rồi `tisa_qc_bat_tat`, hoặc `ads_update_entity`; tạo chiến dịch luôn TẠM DỪNG, hỏi anh mới bật (`/ts-len-camp-facebook`).

---
## 2. "Nối Fanpage để bot trả lời tin nhắn (và bình luận, đăng bài)" (VỪA đến KHÓ)

1. Kiểm điều kiện: TISA mở được bằng **tên miền HTTPS**? `tisa_ui action=open_page` Cài đặt, Truy cập từ xa (hoặc hỏi anh). Chưa có: Tên miền riêng qua Cloudflare Tunnel (file 07 mục 9) hoặc VPS; Link nhanh `trycloudflare.com` chỉ để thử (đổi mỗi lần khởi động). Anh phải là quản trị Fanpage.
2. `ui_tisa lenh=mo_the ten="Kết nối Meta"` (hoặc "Facebook Messenger"); `lenh=xem` đọc **Địa chỉ quay về** và **Link chính sách quyền riêng tư**.
3. `hoi_mo` developers.facebook.com/apps; **[NGƯỜI]** đăng nhập. Dùng lại app Meta đã có hoặc Tạo ứng dụng (tên = tên Fanpage + "Bot", use case "Tương tác với khách hàng trên Messenger").
4. Thêm 4 quyền ở "Quản lý mọi thứ trên Trang": `pages_read_engagement`, `pages_read_user_content`, `pages_manage_engagement`, `pages_manage_posts` (hộp hỏi ảnh hưởng thì Add); kiểm đều "Sẵn sàng thử nghiệm".
5. Facebook Login, Cài đặt: bật hai công tắc OAuth, dán Địa chỉ quay về vào Valid OAuth Redirect URIs, Lưu. Cài đặt ứng dụng, Thông tin cơ bản: dán Link chính sách vào hai ô, chọn Hạng mục, Lưu.
6. Dán App ID và App secret bằng `chon_o` + `dan_vao_tisa`. `ui_tisa lenh=bam nhan="Đăng nhập Facebook"`; **[NGƯỜI]** đăng nhập, "Chỉnh sửa cài đặt", tick Fanpage, đồng ý TẤT CẢ quyền.
7. `lenh=bam nhan="Kết nối các Trang đã chọn"`; đọc bảng kiểm tra (xanh xong, vàng nhắc, đỏ bấm "Sửa tự động" hoặc gọi `messenger_repair page=<Page ID>`).
8. Trang Chatbot, tab Bot: tạo Agent trong brain RIÊNG cho khách, tạo bot, tick kênh Messenger, bật bot (không có bot thì Hộp thư trống).
9. Chuyển app sang **Live** (**[NGƯỜI]** hoặc `op=click` có duyệt; hỏi anh trước), rồi thử bằng nick Facebook KHÔNG có vai trò trong app. Nếu Meta vẫn chặn người lạ: nộp Advanced Access `pages_messaging` (xét duyệt, báo anh thời gian chờ).
10. Kiểm: `messenger_check`; Hộp thư nhận được tin và bình luận. Nút đăng nhập hỏng: "Dán token thay vì đăng nhập" (Graph API Explorer, 7 quyền).

---
## 3. "Nối Zalo OA cho bot chăm khách" (KHÓ, chờ xác thực tên miền)

1. Hỏi MỘT câu: OA đã xác minh chưa? Nếu chủ chỉ cần bot nhắn nhanh và không có OA, đề xuất **Zalo Bot** (DỄ, kênh B, `docs/26`) thay cho OA. Zalo OA cần tên miền HTTPS (như kịch bản 2 bước 1).
2. `hoi_mo` developers.zalo.me; **[NGƯỜI]** đăng nhập quản trị OA. Tạo ứng dụng; mục Official Account liên kết OA; chép **App ID**, **App secret key**.
3. Trang Chatbot, Bot, Thêm kênh, **Zalo OA** (`ui_tisa lenh=bam nhan="Thêm kênh"`): đọc **Địa chỉ webhook** (`https://<miền>/zalo-oa/webhook`) và **Callback URL** (`/zalo-oa/oauth/callback`).
4. Zalo, Xác thực tên miền, chọn file HTML, lấy tên `zalo_verifier<mã>.html`; dán vào ô "Mã xác thực tên miền Zalo" của TISA, Lưu mã; quay lại Zalo bấm Xác thực (`POST /zalo-oa/site-verification`).
5. Webhook trong app Zalo: dán Địa chỉ webhook, bật `user_send_text`, `user_send_image`, `user_send_file`, `user_send_audio`, `user_send_sticker`, `user_send_location`; chép **OA secret key**. Dán Callback URL ở mục Official Account của app.
6. Ô Token trong form: `<App ID> <App secret key> <OA secret key>` (dán kín từng giá trị bằng `dan_vao_tisa` hoặc anh tự gõ); `lenh=bam nhan="Cấp quyền bằng Zalo"`; **[NGƯỜI]** chọn đúng OA, Cho phép.
7. Gắn kênh vào bot (Chatbot, Bot), bật bot. Kiểm: nhắn OA từ một nick thường, tin phải vào Hộp thư.
8. Lỗi: thiếu OA secret key bot không chạy; `-230` ngoài khung trả lời; `-224` gói OA không cho; refresh token chết thì Sửa kênh, "Cấp quyền lại bằng Zalo". OA chỉ trả lời trong khung thời gian sau tin cuối của khách.

---
## 4. "Nối Telegram để báo đơn" (DỄ)

Hai nghĩa khác nhau, hỏi một câu để chọn:
- **(A) TISA BOT báo kết quả/nhắc hẹn/đơn mà TISA biết về điện thoại anh**: Kênh Admin Telegram.
  1. **[NGƯỜI]** (hoặc `hoi_mo` web.telegram.org) trong Telegram: **@BotFather** `/newbot`, lấy token; **@userinfobot** lấy Chat ID. Bắt đầu chat với bot, bấm Start.
  2. `tisa_ui action=open_page` trang Kênh Admin; `ui_tisa` tìm tab Telegram; `chon_o truong="Bot token"` rồi `dan_vao_tisa` (token đi kín); điền Chat ID; `lenh=bam nhan="Lưu & bật"`.
  3. Đợi dòng trạng thái "Bot đang nhận tin" (Gửi test không đủ); nhắn bot một câu để kiểm. Lỗi 409 = token chạy nơi khác.
  4. Chỉnh loại thông báo: `tisa_notify`; báo định kỳ: `tisa_schedule op=create`.
- **(B) Báo ĐƠN CÓ TIỀN VÀO từ ngân hàng/SePay**: skill `/ts-bao-don-telegram`, cách A "SePay có sẵn" (không code).
  1. `tisa_use_skill name=ts-bao-don-telegram` (nếu chưa có Bộ não thì bỏ bước lưu).
  2. my.sepay.vn, menu **Tích hợp Telegram**: tạo nhóm, thêm bot của SePay, nhập ID nhóm, Kiểm tra kết nối; chọn tài khoản ngân hàng, sự kiện "Có tiền vào"; sửa mẫu tin; thử bằng giao dịch nhỏ (**[NGƯỜI]** chuyển tiền thật).
  3. Cần tin theo mẫu riêng/ghép giao hàng: cách B, webhook `api/sepay-webhook.js` (xem kịch bản 7), biến `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `SEPAY_WEBHOOK_APIKEY` do anh tự đặt vào ô Environment Variables, KHÔNG dán chat.

---
## 5. "Nối Google Sheets / Drive" (VỪA)

Chọn theo việc (hỏi một câu):
- **Đọc/ghi bảng tính** (doanh thu, tồn kho): thẻ Google Sheets (Service account, nhanh nhất). **Gmail + Lịch + Drive + Docs + Sheets trong một**: Google Workspace (máy có màn hình). **Chỉ Lịch/Gmail**: hai thẻ remote.
- **Tải tệp lớn, đổi tên hàng loạt trên Drive**: `tisa_drive_do` (kịch bản dưới).
1. `ui_tisa lenh=mo_the ten="Google" dich_vu="Google Sheets"` rồi `lenh=xem` để biết ô cần điền (service account JSON + ID thư mục). Kiểm máy có `uv` (cần cho Sheets/Search Console): thiếu thì báo cài `winget install astral-sh.uv` (Windows).
2. `hoi_mo` console.cloud.google.com; **[NGƯỜI]** đăng nhập Google, đồng ý Điều khoản Cloud lần đầu. Dự án có sẵn thì dùng lại; chưa có: New Project "TISA BOT".
3. Bật **Google Sheets API** (và Drive API nếu cần). IAM và Admin, Service Accounts, Create, Keys, Add key, JSON (tải về, KHÔNG đọc ra chat). Dán vào ô JSON: `dan_vao_tisa` (nếu thẻ có ô kéo thả file thì anh kéo thả).
4. Share bảng tính hoặc thư mục Drive cho email của service account (Editor nếu muốn ghi). Dán ID thư mục. `lenh=bam nhan="Kết nối"`.
5. Kiểm chỉ đọc: liệt kê một sheet, đọc 3 dòng đầu. Mặc định thẻ Sheets ở Ghi nháp; hạ xuống Chỉ đọc nếu chỉ cần xem.
6. **OAuth (Workspace/Gmail/Lịch)**: Google Auth Platform: External, **Test users** thêm email chủ, **Publish app** để token không hết sau 7 ngày; client Desktop app (Workspace) hoặc Web application + Redirect URI copy từ thẻ (Gmail, Lịch); dán Client ID/Secret rồi Kết nối; **[NGƯỜI]** tick HẾT các ô quyền, Cho phép. Dịch vụ thứ hai: "Dùng lại key".
7. **Drive bằng API**: tạo OAuth client loại **Desktop app**; `luu_keychain tu_tab tu_id ten=drive-client truong=client_id`, rồi `truong=client_secret` (anh Duyệt một lần); `tisa_drive_do op=dang_nhap` (mở cổng 127.0.0.1 tạm), **[NGƯỜI]** bấm Cho phép trên Google; kiểm `op=trang_thai`, `op=liet_ke`. Đổi tên hàng loạt: `op=doi_ten` XEM TRƯỚC rồi mới `chay=true` (duyệt, có tệp hoàn tác). Không có thao tác xóa.
8. Lỗi: 403 access_denied = thiếu Test user; scope thiếu = khai đủ ở Data Access rồi đăng nhập lại; Docker + Workspace phải mở cổng 8000.

---
## 6. "Đưa web lên Cloudflare" (VỪA; có phần cần xác minh)

Hiện trạng trong app: connector Cloudflare có (API token hoặc OAuth), skill `ts-dua-web-len-mang` trong `[app]` chỉ dạy Vercel, gói "Cloudflare Deploy (Wrangler)" nằm ở TISA Store. Phần deploy bằng Wrangler cần xác minh trong mã/Store trước khi hứa với anh.
1. `tisa_connections` xem thẻ Cloudflare đã nối chưa. Chưa: `ui_tisa lenh=mo_the ten="Cloudflare"`. Đường nhanh: thẻ "Cloudflare (đăng nhập web)" (OAuth, tick quyền ngay trên Cloudflare). Cần Wrangler: thẻ API token.
2. `hoi_mo` dash.cloudflare.com/profile/api-tokens; **[NGƯỜI]** đăng nhập. Create Custom Token (tên "TISA BOT"): Account Workers Scripts Edit, Cloudflare Pages Edit, Workers KV Edit, R2 Edit, D1 Edit, Account Settings Read; Zone DNS Edit, Zone Read. Account Resources: tài khoản anh. Zone Resources: đúng miền cần dùng. KHÔNG bật lọc IP.
3. Token chỉ hiện MỘT lần: `ui_tisa lenh=chon_o truong="API token (Cloudflare)"` rồi `dan_vao_tisa tu_tab tu_id`; Account ID để trống nếu chỉ một tài khoản. `lenh=bam nhan="Kết nối"`, đợi đèn xanh, Kiểm tra.
4. Kiểm chỉ đọc qua MCP Cloudflare (`https://mcp.cloudflare.com/mcp`): liệt kê zone/Workers. Thiếu quyền mảng nào thì Edit token thêm quyền, không tạo mới.
5. Deploy: engine Claude có shell riêng, chạy `npx wrangler deploy` hoặc `wrangler pages deploy` trong thư mục dự án (engine API: `tisa_run_command` chỉ có khi chat gắn thư mục làm việc). Khóa cho Wrangler: biến `CLOUDFLARE_API_TOKEN` do anh tự đặt trong cửa sổ lệnh của anh (không dán chat); đường lấy khóa từ Keychain cho shell: cần xác minh trong mã (`secret_guard.py` chặn lệnh chạm file bí mật của TISA, không rõ về Keychain). `wrangler login` (OAuth) KHÔNG sửa được DNS.
6. Tên miền: thêm custom domain trong Workers/Pages hoặc qua DNS Edit; DNS có thể cần chờ lan.
7. Kiểm: mở địa chỉ thật + một trang con (`tisa_browser_look op=open`), thấy HTTPS hợp lệ mới báo xong. Build Vite/React: `emptyOutDir: false` khi deploy lại.
8. Ghi vào trang **Quản lý web** (`/tisa-web/`, nút "Tìm web đã tạo" quét ghi chép trong `04-ket-qua`): kiểm tra mã trả về, hạn chứng chỉ; form khách `/tisa-web/thu/<khoá>`.

---
## 7. "Nối thanh toán SePay (khách quét QR, tự báo đã trả)" (VỪA; nằm ngoài app, qua skill)

1. `tisa_use_skill name=ts-cai-thanh-toan` (trước đó nên có trang bán hàng; `ts-gan-ma-qr` nếu chỉ cần gắn QR). Hỏi: ngân hàng nào, tài khoản SePay chưa, sau khi trả muốn làm gì.
2. **[NGƯỜI]** đăng ký/đăng nhập my.sepay.vn, liên kết tài khoản ngân hàng (OTP ngân hàng: không làm hộ; TISA chặn trang ngân hàng). `hoi_mo` my.sepay.vn để mở đúng tab.
3. Đặt **Cấu trúc mã thanh toán** (tiền tố khớp với tiền tố mã đơn của trang). Tạo khóa API ở **API Access**.
4. Khóa: `luu_keychain` hoặc chủ tự đặt vào ô Environment Variables của nơi chạy trang (biến `SEPAY_API_TOKEN`, `SEPAY_ACCOUNT_NUMBER`). Không dán vào chat/tệp.
5. Trang thanh toán: mã đơn ngẫu nhiên, QR (số tiền + nội dung = mã đơn, nội dung chỉ chữ và số), trang hỏi SePay mỗi 5 giây "mã này trả chưa" rồi hiện đã thanh toán. Đưa trang lên lại (`/ts-dua-web-len-mang`, hoặc kịch bản 6 nếu lên Cloudflare).
6. Webhook nếu cần báo/giao hàng tự động: my.sepay.vn, Webhooks, "+ Thêm webhook": sự kiện "Có tiền vào", URL `https://<miền>/api/sepay-webhook`, bảo mật API Key (dán đúng `SEPAY_WEBHOOK_APIKEY`). Trả HTTP 200/201 + `{"success": true}` trong 30 giây (SePay gửi lại tối đa 7 lần).
7. Thử: **[NGƯỜI]** chuyển khoản số tiền nhỏ; kiểm giao dịch hiện ở my.sepay.vn, Giao dịch, và trang báo "đã thanh toán". Bao giờ cũng dặn: phí/gói/ngân hàng hỗ trợ tra lại trên sepay.vn lúc cài, không nói theo trí nhớ.
8. Lỗi: QR không hiện (sai tên ngân hàng/số TK); trả tiền mà trang không báo (khách sửa nội dung CK, chưa đặt `SEPAY_API_TOKEN`, tiền tố sai); 401 khi hỏi SePay (khóa sai, tạo khóa mới).
9. TISA không chuyển tiền, không bấm bước thanh toán: `CAN_NGUOI_DUNG`/`BI_CHAN` là đúng thiết kế.

---
## 8. "Nối MCP mới từ GitHub / một MCP bất kỳ" (DỄ đến VỪA)

1. `tisa_add_mcp op=find name=<tên dịch vụ>`. Kho Kết nối/Store đã có thẻ thì dùng thẻ (có mẫu đăng nhập và phân loại đọc/ghi), DỪNG ở đây.
2. Chưa có: `tisa_web_fetch` README của repo GitHub (hoặc trang tài liệu chính thức); rút ra: loại MCP (HTTP/SSE từ xa hay lệnh `npx`/`uvx` chạy local), biến cần có, scope tối thiểu. Ưu tiên MCP chính chủ; nghi ngờ repo lạ thì báo anh trước (stdio = chạy lệnh trên máy).
3. MCP từ xa không cần khóa: `tisa_add_mcp op=add name="<tên>" url=<https://...>` (`perm` mặc định `readonly`). Có khóa: `headers="Authorization: Bearer ..."` do anh tự dán ở ô trên trang Kết nối thay vì gõ vào chat (hoặc `ui_tisa lenh=mo_the ten="Tự thêm"` + `dan_vao_tisa`).
4. MCP chạy bằng lệnh (`command=npx args="-y @x/mcp"`, `env=`): `op=add` luôn thêm ở trạng thái TẮT; đọc lệnh, kiểm máy có Node/`uv`/Git, rồi anh (hoặc `ui_tisa lenh=bam`) bật ở trang Kết nối. Server đăng nhập OAuth thì TISA tự mở trang đăng nhập (**[NGƯỜI]** Cho phép).
5. Trang Kết nối, **Kiểm tra** (hoặc `tisa_connections`): `trang_thai` "ổn" và có tool. `Không khởi động được trình kết nối` = thiếu Node/uv/Git; "đang khởi động (tải gói)" chờ 1-2 phút; `install` chờ ~2 phút để TISA dọn gói cài dở.
6. Phân quyền: để Chỉ đọc; chỉ nâng khi anh nói rõ. Thử một tool đọc nhỏ qua `tisa_search_tools` rồi `tisa_run_tool`.
7. TUYỆT ĐỐI không `claude mcp add`/`codex mcp add`: rơi vào config riêng, trang Kết nối không hiện. Muốn dùng riêng cho Claude Code thì đó là nguồn "MCP của Claude Code" (chỉ engine Claude).
8. Sau khi nối: ghi một dòng `TISA_LESSON:` (cách nối, thứ tự, thời gian thật).

---
## 9. "Nối Zalo cá nhân để TISA đọc/gửi tin thay anh" (DỄ thao tác, có rủi ro khóa nick)

1. Nói rõ rủi ro (API không chính thức `zca-js`, nick có thể bị hạn chế/khóa); khuyên **tài khoản phụ**; hỏi anh đồng ý. Nếu chỉ cần khách nhắn vào bot: dùng Zalo Bot/OA (kịch bản 3), không dùng cái này.
2. Máy có Node.js 20+ (`tisa_run_command`/shell: `node -v`); thiếu thì nhờ cài từ nodejs.org.
3. `ui_tisa lenh=mo_the ten="Zalo Agent MCP"`; `lenh=bam nhan="Tôi hiểu rủi ro, hiện mã QR"` (QR sống ~3 phút).
4. Chụp màn hình (`tisa_desktop_look op=screenshot ung_dung="TISA BOT"` nếu cần) cho anh thấy mã; **[NGƯỜI]** quét QR bằng Zalo điện thoại và xác nhận đăng nhập (`wait_user`/`cho_nguoi_that`).
5. `tisa_connections`: tài khoản hiện đèn xanh; thử chỉ đọc `zalo_list_threads` rồi `zalo_get_messages`.
6. Quyền mặc định `full` (để gửi tin): hạ xuống Ghi nháp/Chỉ đọc nếu chỉ cần đọc (menu chip). Gửi `zalo_send_message` chỉ khi anh nói rõ nội dung + người nhận.
7. Muốn có tin cũ trong Hộp thư: Chatbot, thẻ tài khoản Zalo, **Nhập tin cũ** (khoảng 2 tuần, tối đa 5.000 tin).
8. Lỗi: QR hết hạn lấy lại; `Not logged in` = Kết nối lại, quét QR; `sync.complete:false` = mất kết nối giữa chừng, đừng báo "khách chưa trả lời".

---
## 10. "Nối TikTok Ads / Google Ads để xem báo cáo" (KHÓ, có chờ duyệt: nói anh ngay từ đầu)

**TikTok Ads**
1. Báo trước: TikTok duyệt app vài giờ đến vài ngày (không rút ngắn được); làm phần không chờ trước. Cần quyền Admin nhà quảng cáo.
2. `hoi_mo` business-api.tiktok.com/portal; **[NGƯỜI]** đăng nhập TikTok For Business. My Apps, Create New App: tên "TISA BOT", Advertiser redirect URL `https://localhost`, quyền Ads Management + Reporting, gửi duyệt. Báo anh, dừng; anh quay lại nói khi đã duyệt.
3. Khi duyệt: mở "Advertiser authorization URL", **[NGƯỜI]** Confirm các tài khoản; auth_code nằm trên thanh địa chỉ (trang lỗi không sao). "Get access token" (App ID + Secret) ra `access_token` và `advertiser_id`.
4. `ui_tisa lenh=mo_the ten="TikTok"`; dán Advertiser ID và Access Token bằng `chon_o` + `dan_vao_tisa`; `lenh=bam nhan="Lưu và kiểm tra"`. Hoặc trang **Quảng Cáo**, thêm tài khoản TikTok bằng API (`ma_tk`, `token`).
5. Cần `uv` cho thẻ MCP. Kiểm chỉ đọc: liệt kê tài khoản, chiến dịch, báo cáo.

**Google Ads**
1. Báo trước: Developer token xin ở tài khoản MCC (Tools and settings, API Center), có thể chờ Google duyệt (mức Explorer đủ để đọc).
2. Máy có `uv` và **Git** (thiếu một là chết). Chuẩn bị Google Cloud: bật Google Ads API, màn hình đồng ý External + Test users, client **Web application** với redirect `http://localhost:7777/connect/oauth/callback` (VPS: thêm `https://<miền>/connect/oauth/callback`).
3. `ui_tisa lenh=mo_the ten="Google" dich_vu="Google Ads"`; điền Developer token, Client ID/Secret (`dan_vao_tisa`), Login customer ID (10 số); `lenh=bam` nút đăng nhập; **[NGƯỜI]** Cho phép, "ứng dụng chưa được xác minh" thì Nâng cao, Tiếp tục (app của chính anh).
4. Kiểm chỉ đọc: truy vấn GAQL chiến dịch/chi phí. Thẻ thuần chỉ đọc.
5. Quản lý và bật/tắt: trang **Quảng Cáo** (API) và `tisa_qc_bat_tat nen=google`.

---
## Khi kẹt (chung cho mọi kịch bản)
1. Đọc NGUYÊN VĂN lỗi/mã (file 06 bảng 3); kiểm đúng tài khoản/hồ sơ đang đăng nhập, đúng dự án/ứng dụng, API đã bật, đúng scope, redirect URI, mã hết hạn, `uv`/Node/Git.
2. `tisa_web_search` nguyên văn lỗi trên tài liệu chính thức và GitHub issues của chính MCP đó.
3. Đổi đường: MCP chính chủ, API chính thức, thao tác trên web, MCP cộng đồng. Mỗi đường tối đa 3 lần.
4. Kẹt cùng một chỗ 3 lần: dừng, `tisa_browser_look op=screenshot`, báo anh 3 ý (đã thử gì, kẹt ở đâu, anh cần làm gì). Không bảo anh tự chạy lệnh.
5. Cuối: `TISA_LESSON: <công cụ>: <điều học được>`; không ghi khóa, email, số điện thoại, tên khách.
