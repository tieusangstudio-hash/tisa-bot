# 07 - Các kênh và kết nối app đã hỗ trợ

Nguồn: `[app]/docs/09, 11, 12, 14, 15, 17, 25, 26, 29, 30, 31, 31-tung-buoc, 33, 34, 35, 36`, `[app]/dashboard/tisa-ket-noi-huong-dan.json`, `[app]/system/mcp-catalog.json`. `[app]` = `thư mục cài TISA BOT`.
Mức: DỄ (bấm Cho phép / dán một khóa, 2 đến 15 phút), VỪA (tự tạo ứng dụng OAuth, 15 đến 40 phút), KHÓ (có xét duyệt, tên miền, chờ ngày). Thang gốc ở `suite/skills/dq-dau-noi-cong-cu/SKILL.md`.

## 0. Phân biệt ba loại "nối" (đừng lẫn)

| Loại | Là gì | Ví dụ | Thẻ ở đâu |
|---|---|---|---|
| A. Kết nối công cụ (MCP/API) | TISA BOT dùng một dịch vụ ngoài để làm việc | Meta Ads, Google, Composio, Cloudflare, Zalo cá nhân | Trang **Kết nối** (nhóm Kết nối) |
| B. Kênh Admin | CHỦ nhắn cho TISA BOT qua app chat | Telegram, Zalo Bot, Slack, WhatsApp, Discord, Lark | Trang **Kênh Admin** (`channels`), mỗi kênh một tab |
| C. Kênh bot khách | KHÁCH nhắn, bot chuyên trách trả lời, vào Hộp thư | Messenger/Fanpage, Zalo OA, Zalo Bot, Telegram, WeChat, Slack, WhatsApp, Lark | Trang **Chatbot**, tab Bot, **Thêm kênh** (Messenger còn nối ở thẻ Facebook Messenger ở trang Kết nối) |

Mọi kênh C dùng một Agent + một brain: tạo brain riêng cho việc trả lời người ngoài (chỉ bỏ tài liệu được phép lộ). Mỗi bot một token riêng, KHÔNG dùng chung token với kênh Admin (409 hoặc hai bên cùng chết). Kênh của bot không đổi được sau khi tạo (`docs/25-chatbot.md`). Mặc định quyền bot khách là Chỉ đọc.

Quy tắc chung mọi thẻ: giá trị bí mật đi bằng `dan_vao_tisa`/`dan_ma`, không chép chat. Cần người thật: đăng nhập, OTP, CAPTCHA, hộp Cho phép, quét QR bằng điện thoại.

## 1. Meta (Facebook, Instagram, Threads)

### 1.1 Messenger / Fanpage (trả lời tin nhắn, bình luận, đăng bài) - VỪA đến KHÓ
- Thẻ: Kết nối, thẻ **Facebook Messenger** (tên trong hướng dẫn tự động: "Kết nối Meta"). Cần TISA mở bằng **tên miền HTTPS** (webhook Meta không gọi localhost/IP).
- Cần: App Meta của chủ (App ID, App secret), tài khoản là quản trị Fanpage. Một app dùng chung cho mọi thẻ Meta.
- Bước (`docs/31-messenger-tung-buoc.md`): (0) developers.facebook.com tạo app, use case "Tương tác với khách hàng trên Messenger". (1) Thêm 4 quyền ở "Quản lý mọi thứ trên Trang": `pages_read_engagement`, `pages_read_user_content`, `pages_manage_engagement`, `pages_manage_posts`. (2) Facebook Login, Cài đặt: bật hai công tắc OAuth; dán **Địa chỉ quay về** (`https://<miền>/messenger/oauth/callback`, nút Chép trong thẻ) vào Valid OAuth Redirect URIs; dán **Link chính sách** (`/messenger/privacy`) vào hai ô chính sách và xóa dữ liệu. (3) Dán App ID/Secret vào thẻ, chọn cách xử lý bình luận, **Đăng nhập Facebook**, chọn Trang, **Kết nối các Trang đã chọn** (TISA tự lấy token Trang không hết hạn, khai webhook, gắn Trang vào app, hiện bảng kiểm tra). (4) Chatbot, Bot: tick kênh vào một bot và bật. (5) Chuyển app sang Live; thử bằng nick KHÔNG có vai trò trong app.
- Instagram: tài khoản phải Business/Creator liên kết đúng Fanpage; Threads thêm bằng nút "+ Threads" trên thẻ sau khi nối Fanpage.
- Lỗi hay gặp (`docs/31`, `docs/09`): "URL bị chặn" = chưa dán Địa chỉ quay về nguyên văn; "Invalid Scopes" = thiếu quyền ở bước 1, thêm rồi đăng nhập lại; "Miền của URL này không được đưa vào miền của ứng dụng" = điền Miền ứng dụng (tên miền trần); bot im khi khách nhắn = chưa gắn bot hoặc app còn chế độ Development; lỗi 190 = token hết hạn (dùng token System User/Trang); 24 giờ ngoài cửa sổ; webhook đỏ = bấm **Sửa tự động** (hoặc `messenger_repair`), vẫn đỏ thì khai tay ở Messenger API settings và tick đúng 3 trường `messages`, `messaging_postbacks`, `feed`; app sai secret thì TISA chặn ngay lúc lưu. Nếu nút đăng nhập hỏng: "Dán token thay vì đăng nhập" (Graph API Explorer, đủ 7 quyền, token ~1 giờ, TISA tự đổi sang token Trang).
- App chỉ phục vụ Fanpage của chính chủ thường không cần App Review; nếu bot vẫn không trả lời người lạ khi Live thì nộp Advanced Access cho `pages_messaging` (xét duyệt, có thể kèm xác minh doanh nghiệp). Giới hạn: tối đa 100 Fanpage mỗi bot.

### 1.2 Meta Ads (số liệu, chiến dịch) - DỄ nếu đã có MCP Claude Code; VỪA nếu tự tạo app
- Đường 1 (ưu tiên, DỄ): MCP **Meta Ads của claude.ai/Claude Code** đã đăng nhập thì TISA dùng luôn, công cụ `ads_*` (xem trang Kết nối, thẻ "Đã nối MCP của Claude Code", `server/tisa_claude_mcp.py`). Chỉ engine Claude. `Needs authentication` = anh đăng nhập lại ở Claude Code, Connectors.
- Đường 2: thẻ **Meta Ads (Facebook & Instagram)** (Graph API, plugin `meta-ads-graph`, CHỈ ĐỌC). Cần App ID + App Secret (`docs/09` mục "Meta Ads qua Graph API", `tisa-ket-noi-huong-dan.json` id `meta-ads`): tạo app Business, giữ chế độ Development, anh là Admin app và ad account, bỏ qua Xác minh doanh nghiệp và App Review. Máy cá nhân phải mở bằng `localhost` (KHÔNG 127.0.0.1), không điền gì vào ô redirect; VPS/tên miền: dán Địa chỉ quay về (`/connect/oauth/callback`) và Miền ứng dụng. Nút "Lưu & mở trang đăng nhập", tick đúng tài khoản quảng cáo. Token ~60 ngày tự gia hạn; hết hẳn thì Kết nối lại.
- Lỗi: "Invalid Scopes" bấm OK (cảnh báo chỉ hiện cho nhà phát triển), kiểm bằng "liệt kê Trang/ad account của tôi"; không thấy tài khoản = thiếu `ads_read` hoặc không phải admin; "Facebook từ chối / redirect_uri" = rời Development hoặc dùng 127.0.0.1. Thẻ MCP chính chủ cũ của Meta (`mcp.facebook.com/ads`) báo DCR/"restricted to certain users": giới hạn phía Meta, gỡ và dùng thẻ trên.
- Bật/tắt/đổi ngân sách: ở trang **Quảng Cáo** nối tài khoản BẰNG API (token `ads_management`) rồi `tisa_qc_bat_tat`; hoặc `ads_update_entity` của MCP. Tạo chiến dịch luôn TẠM DỪNG (`ts-len-camp-facebook`).

### 1.3 Facebook Trang (thẻ cũ)
Từ 0.438.0 kho gỡ thẻ này; nối Fanpage ở thẻ Messenger là đủ (`docs/09` mục 5b). Máy đã cài vẫn dùng. Cùng App Meta, thêm quyền Trang, mặc định Chỉ đọc, đăng bài cần Toàn quyền, xóa bài không hoàn tác.

## 2. Zalo (ba chỗ khác nhau)

| | Zalo Agent MCP (cá nhân) | Zalo Bot | Zalo OA |
|---|---|---|---|
| Loại | A (chính nick chủ) | B và C | C |
| Thẻ | Kết nối, "Zalo Agent MCP" | Kênh Admin, thẻ **Zalo** (và Chatbot) | Chatbot, Bot, Thêm kênh, **Zalo OA** |
| API | zca-js KHÔNG chính thức, có thể bị hạn chế/khóa | Chính thức | Chính thức OA Open API v3 |
| Mức | DỄ về thao tác, rủi ro tài khoản | DỄ | KHÓ (tên miền + xác thực + OA đã xác minh) |

### 2.1 Zalo Agent MCP (`docs/12-zalo.md`)
- Cần Node.js 20+ trên máy chạy TISA và tải được từ GitHub; điện thoại đăng nhập Zalo.
- Bước: Kết nối, thẻ Zalo Agent MCP, Kết nối, đọc cảnh báo rủi ro, "Hiện mã QR", quét bằng Zalo (QR sống ~3 phút), tài khoản hiện ở Đã kết nối. Nhiều số: "+ Thêm tài khoản" (thư mục phiên riêng). Mặc định Toàn quyền; có thể hạ xuống Ghi nháp/Chỉ đọc. Nên dùng tài khoản phụ, tránh gửi hàng loạt.
- 11 tool `zalo_*` (xem file 06). Lịch sử chỉ từ lúc kết nối + ~2 tuần Zalo gửi lại (lưu 30 ngày); `sync.complete:false` = có khoảng mất kết nối, đừng kết luận khách chưa trả lời. Duyệt người xin vào nhóm cần là trưởng/phó nhóm và quyền Toàn quyền.
- Lỗi: "Cần cài Node.js 20+" cài rồi thử lại; QR hết hạn quét lại; `Not logged in` = đăng xuất, Kết nối lại và quét QR; tin nhóm đến chậm: biến `TISA_ZALO_PUSH=0` tắt cơ chế đẩy.

### 2.2 Zalo Bot (`docs/26-kenh-zalo-bot.md`)
- Lấy token: Zalo, Official Account **Zalo Bot Manager**, Tạo bot (tên phải mở đầu "Bot"), token dạng `123456789:abc-xyz` (không hết hạn).
- Kênh Admin, thẻ Zalo: tích Bật bot, dán token, ô "Chat ID được phép" ĐỂ TRỐNG, Lưu & bật; nhắn bot, nhận **mã ghép nối 4 số**; thẻ hiện khối "Đang chờ bạn cho phép", đối chiếu mã, bấm **Cho phép**. (Trống = CHƯA AI được phép, khác Telegram.)
- Giới hạn: không sửa/xóa tin (không có tin trạng thái), không gửi tài liệu, 2000 ký tự mỗi tin, không có nút bấm, không vào nhóm ở gói cơ bản.
- Lỗi: "Token không hợp lệ (Zalo từ chối)" thường dán nhầm token Telegram; bot xanh mà không trả lời: xem log `[zalo getUpdates] khuôn phản hồi lạ`; 429 tự nghỉ 1 phút.

### 2.3 Zalo OA (`docs/35-zalo-oa.md`) - KHÓ
- Cần tên miền HTTPS công khai. developers.zalo.me: tạo app, liên kết OA, chép App ID, App secret key; mục Webhook chép **OA secret key**.
- Bước: Chatbot, Bot, Thêm kênh, Zalo OA: form hiện **Địa chỉ webhook** (`https://<miền>/zalo-oa/webhook`) và ô **Mã xác thực tên miền** (dán tên file `zalo_verifier<mã>.html`, Lưu mã, rồi Xác thực trên Zalo). Bật các sự kiện `user_send_text/image/file/audio/sticker/location`. Khai **Callback URL** (`/zalo-oa/oauth/callback`) trong app. Ô Token dán `<App ID> <App secret key> <OA secret key>` (hoặc `app_secret=... oa_secret=...`) rồi **Cấp quyền bằng Zalo** (OAuth v4 + PKCE, access token ~25 giờ, refresh ~3 tháng, tự làm mới).
- Lỗi: thiếu OA secret key bot không chạy; sai redirect_uri = Callback URL phải đúng y và mở TISA bằng đúng tên miền đó; "Zalo không làm mới được token" = Sửa kênh, **Cấp quyền lại bằng Zalo**; `-230` khách lâu không nhắn (khung thời gian trả lời); `-224` gói OA chưa cho dùng API; không tin tới = webhook sai hoặc bị Zalo bỏ vì TISA không trả lời, bật lại ở app Zalo.

## 3. Telegram (`docs/11-telegram.md`) - DỄ
- Kênh Admin, tab **Telegram**. Cần: Bot token từ **@BotFather** (`/newbot`), Chat ID từ **@userinfobot** (ghi mọi người dùng chung, mỗi người bấm Start bot một lần). Không cần tên miền.
- Bước: dán token, dán Chat ID (nhiều ID cách dấu phẩy), **Lưu & bật**; xem dòng trạng thái phải là "Bot đang nhận tin" (Gửi test chỉ chứng minh token và ID đúng). Bot khách: Chatbot, Tài khoản, mỗi bot token riêng.
- Lỗi: 409 = cùng token chạy nơi khác hoặc còn webhook (TISA tự xóa webhook lúc khởi động; tìm nơi chạy thứ hai); "Bạn không có quyền dùng bot" = Chat ID không khớp; gửi test được mà không trả lời = trạng thái chưa xanh; file tối đa 20 MB tải về, bot gửi file ra dưới 50 MB, tối đa 10 file/lượt; video chưa xem được. Tin thoại cần key Groq ở trang Models (dùng chung Zalo/Slack/WhatsApp...).
- "Báo đơn" Telegram qua SePay là việc NGOÀI app (xem file 08, kịch bản 4).

## 4. Slack, WhatsApp, Discord, Lark, WeChat

| Kênh | Thẻ | Cần | Mức | Lỗi hay gặp |
|---|---|---|---|---|
| **Slack** (`docs/29`) | Kênh Admin, tab Slack; bot khách ở Chatbot, Tài khoản (`xoxb-... xapp-...` cách nhau dấu cách) | Tạo app bằng manifest YAML (Socket Mode, 10 scope), token `xapp-` (scope `connections:write`) + `xoxb-` | VỪA | `invalid_auth` = bot token sai/thu hồi; app token bị từ chối = thiếu `connections:write` hoặc chưa bật Socket Mode; im trong kênh = chưa `/invite @TISA BOT`. Lệnh bot dùng `!` thay `/` |
| **Slack MCP** (nguồn A, khác trên) | Kết nối (từ TISA Store) | Tạo app trong workspace, Redirect URL `http://localhost:7777/connect/oauth/callback` (VPS: https miền), User Token Scopes, Client ID/Secret | VỪA | Workspace bắt duyệt app cần admin; mặc định Chỉ đọc |
| **WhatsApp** (`docs/29`) | Kênh Admin, tab WhatsApp; bot khách: `<phone number id> <access token> <app secret>` | WhatsApp Business Cloud API (Meta), HTTPS miền, token System User (không dùng token 24 giờ), Callback URL + Verify token dán ở WhatsApp, Configuration, Webhook, đăng ký trường `messages` | KHÓ | lỗi 190 = token hết hạn; 131047 = ngoài cửa sổ 24 giờ (kết quả nền xong sau 24 giờ không gửi được, nằm ở chuông dashboard); Meta không verify = không HTTPS, miền chưa được phép (`TISA_ALLOWED_HOSTS`), sai verify token |
| **Discord** (`docs/30`) | Kênh Admin, tab Discord | Bot token (Developer Portal, Reset Token) + mời bot với quyền View Channels, Send Messages, Read Message History, Attach Files. Không cần Message Content Intent | DỄ | "Discord từ chối bot token" = reset lại token; gửi tin thử báo không mở được tin riêng = chưa chung server; im trong kênh = thiếu quyền ở kênh. Chưa có bot khách |
| **Lark / Feishu** (`docs/30`) | Kênh Admin, tab Lark; bot khách: Chatbot, Tài khoản `cli_... SECRET` | Custom App, thêm Bot, quyền `im:message`, `im:resource`; App ID `cli_...` + Secret; chọn Nền tảng Lark hay Feishu | VỪA | Bật TISA TRƯỚC rồi mới chọn "persistent connection" trong console, thêm sự kiện `im.message.receive_v1`, **phát hành phiên bản** (mỗi lần đổi quyền phải phát hành lại); "too many connections" = một app chỉ gắn một TISA; bot khách phải dùng app RIÊNG |
| **Lark MCP** (nguồn A) | Kết nối (Store) | App ID + App Secret tại open.larksuite.com, Node 18+ | VỪA | Chỉ làm được trong phạm vi quyền app; mặc định Chỉ đọc |
| **WeChat OA** (`docs/36`) | Chatbot, Bot, Thêm kênh, WeChat | Official Account ĐÃ XÁC MINH (hoặc tài khoản thử nghiệm miễn phí), AppID, AppSecret, EncodingAESKey, IP ra ngoài CỐ ĐỊNH trong IP whitelist, tên miền | KHÓ | 40164 = IP chưa trong whitelist (câu lỗi ghi rõ IP); 48001 = chưa xác minh; 40125/40001 = AppSecret sai; 45015 quá 48 giờ; 45047 hết số tin; nên chọn Chế độ an toàn (AES). WeChat đòi trả lời trong 5 giây nên TISA báo "đã nhận" rồi gửi sau |

## 5. Google (`docs/09` mục 4, `tisa-ket-noi-huong-dan.json` id `google-oauth`)
- Thẻ **Google** trong Kết nối (gộp 6 dịch vụ, nút "Chọn dịch vụ"; Search Console riêng). Làm client OAuth MỘT lần rồi "Dùng lại key" cho dịch vụ sau.
- Chuẩn bị chung (VỪA): console.cloud.google.com, dự án, bật đúng API (Gmail, Calendar, Drive, Docs, Sheets, Tasks, Analytics Data + Admin, Ads, Search Console), Google Auth Platform: External, **thêm email chủ vào Test users**, mẹo: bấm **Publish app** (In production) để token không hết sau 7 ngày (chủ tự dùng không cần xác minh, bấm Nâng cao, Tiếp tục).
- Từng dịch vụ:
  - **Gmail**, **Google Calendar** (remote, dùng được trên VPS): client loại **Web application**, Redirect URI copy từ thẻ; mặc định Chỉ đọc; Gmail chỉ tới NHÁP (không có tool gửi). Phải khai đủ scope ở Data Access (Calendar cần `calendar.events.freebusy`); thiếu scope thì đăng nhập vẫn xanh nhưng tool báo thiếu quyền, xóa cài lại không chữa được (`oauth_mcp.scope_report`).
  - **Google Workspace** (Gmail + Lịch + Drive + Docs + Sheets, chạy local): client loại **Desktop app**, chỉ máy có màn hình; nên điền email Google; mặc định Ghi nháp. Docker phải mở cổng 8000 (`docker-compose.google.yml`). **Google Tasks** dùng chung client.
  - **Google Sheets**, **Search Console**: Service account JSON (+ share Sheet/thư mục Drive cho email service account; Search Console thêm email làm người dùng property). Cần `uv`.
  - **Google Ads**: KHÓ. Developer token (API Center của tài khoản MCC, có thể chờ duyệt), Login customer ID, client Web application với redirect `http://localhost:7777/connect/oauth/callback`; cần `uv` VÀ Git trên máy. TISA tự dựng file đăng nhập, không cần `gcloud`.
  - **Google Analytics (GA4)**: bật Analytics Data API + Admin API.
  - **Google Keep**: master token toàn quyền tài khoản qua App Password; chỉ làm khi anh tự quyết. **NotebookLM**: mượn cookie phiên (KHÔNG chạy `notebooklm login`): `ui_tisa mo_the ten="NotebookLM" truong="Phiên đăng nhập"` rồi `dan_vao_tisa kieu=phien_trinh_duyet mien=google.com`.
  - **Google Drive qua API** (tệp lớn, đổi tên hàng loạt): không phải thẻ mà là `tisa_drive_do` + Keychain (file 06).
- Lỗi: 403 `access_denied` = chưa thêm Test user; "ACCESS_TOKEN_SCOPE_INSUFFICIENT"; `uv`/Git thiếu thì kết nối chết ngay ("Không khởi động được trình kết nối"): cài `uv` (`winget install astral-sh.uv`), lần đầu tải gói có thể chậm 1 đến 2 phút, bấm Kiểm tra lại. VPS không đăng nhập Google bằng cửa sổ máy chủ: dùng thẻ Calendar/Gmail. Tài khoản Google Cloud mới phải đồng ý Điều khoản trước khi tạo client.

## 6. GitHub (`docs/34-github-trong-chat.md`) - DỄ
- Thẻ **GitHub** luôn ở đầu trang Kết nối (có sẵn). Bấm Kết nối: TISA kiểm git (thiếu thì tự cài: Windows winget, Mac Homebrew hoặc hộp Command Line Tools, Linux apt...). Dán Fine-grained PAT (Contents, Pull requests, Workflows: Read/Write; Checks, Actions, Commit statuses, Metadata: Read) hoặc "Dùng token sao lưu brain". Gắn repo vào chat: dấu cộng, Repo GitHub. Token mã hoá, không gửi về trình duyệt.
- Dùng cho "nối MCP mới từ GitHub": đọc README của repo bằng `tisa_web_fetch`; GitHub token là nối mã nguồn, KHÁC với cài MCP.
- Lỗi: thiếu git (nút Cài git, hoặc lệnh tay), token hết hạn (tạo lại, Kết nối lại), tự merge chỉ khi CI xanh và repo có CI.

## 7. Cookies / Kho đăng nhập (`docs/33-kho-dang-nhap.md`) - DỄ
- Kết nối, **Cookies**, Thêm cookie (Cookie-Editor, Export JSON; hoặc file `cookies.txt`/JSON ≤ 1 MB; chuỗi `tên=giá trị;` thì điền thêm ô Trang web). Nút Kiểm tra mở "trang kiểm tra" (đổi sang trang chỉ xem được khi đã đăng nhập cho chính xác). Dùng qua `tisa_login` và ô **Đăng nhập** trong Theo dõi trang.
- Chỉ ĐỌC trang, cookie mã hoá (cần thư viện `cryptography`, thiếu thì từ chối lưu), chỉ gửi đúng tên miền ở mọi bước chuyển hướng; bot khách không thấy. API token không thêm được cookie (phải đăng nhập dashboard thật).
- Lỗi: "Đã hết hạn" = chuyển về màn đăng nhập hoặc 401/403, bấm Cập nhật dán cookie mới; Facebook/Google hay đòi xác minh khi dùng từ IP khác (VPS). Trang có API/MCP chính thức thì dùng đường đó.

## 8. TikTok Ads (`tisa-ket-noi-huong-dan.json` id `tiktok`, `docs/09` mục 5) - KHÓ
- Thẻ TikTok Ads (Store; server cộng đồng trên Marketing API, chỉ đọc). Cần **Advertiser ID** + **Access Token** (+ App ID/Secret để đổi token). business-api.tiktok.com: My Apps, Create New App (Advertiser redirect `https://localhost`, quyền Ads Management và Reporting), **gửi duyệt: vài giờ đến vài ngày, không rút ngắn được**; sau khi duyệt mở "Advertiser authorization URL", Confirm, lấy `auth_code` trên thanh địa chỉ (trang lỗi không sao), đổi lấy Access Token ("Get access token"). Chưa duyệt chỉ có sandbox.
- Trang **Quảng Cáo** cũng nối được TikTok bằng API (ô `ma_tk` = Advertiser ID, `token`), `server/tisa_quang_cao.py`. Cần `uv` trên máy cho thẻ MCP.

## 9. Cloudflare (`docs/15`, thẻ `cloudflare`, `cloudflare-oauth` trong catalog) - DỄ (OAuth) / VỪA (token)
- **Cloudflare (đăng nhập web)**: bấm Kết nối, đăng nhập, tick quyền ngay trên trang Cloudflare. Một chạm, không dùng được với gói "Cloudflare Deploy (Wrangler)".
- **Cloudflare (API token)**: dash.cloudflare.com/profile/api-tokens, Create Custom Token: Account > Workers Scripts Edit, Cloudflare Pages Edit, Workers KV Storage Edit, Workers R2 Storage Edit, D1 Edit, Account Settings Read; Zone > DNS Edit, Zone Read; Account Resources Include tài khoản; Zone Resources All zones hoặc đúng miền. **KHÔNG bật lọc IP** (MCP Cloudflare chưa nhận). Token chỉ hiện một lần: `dan_vao_tisa` vào ô "API token (Cloudflare)". Account ID chỉ khi token thấy nhiều tài khoản.
- MCP: `https://mcp.cloudflare.com/mcp`. `wrangler login` (OAuth) KHÔNG có quyền sửa DNS (`references/kinh-nghiem-da-lam.md`).
- Khác nữa: **Cloudflare Tunnel** để mở TISA ra Internet (Cài đặt, Truy cập từ xa): Link nhanh (`trycloudflare.com`, đổi mỗi lần khởi động), Tên miền riêng (dán lệnh tạo tunnel vào ô "Token tunnel Cloudflare", Public Hostname trỏ tới `127.0.0.1:7777`), Tailscale (riêng tư, không dùng cho webhook). Bắt buộc đặt mật khẩu admin trước; máy ngủ thì link tắt.
- Đưa trang web lên Cloudflare: cần xác minh trong mã. Skill `ts-dua-web-len-mang` trong bản này chỉ nói Vercel; gói "Cloudflare Deploy (Wrangler)" nằm ở TISA Store (`tisa-store`), không có trong `[app]`.

## 10. Composio, Botcake, Zernio, Substack và các thẻ khác

| Thẻ | Cần | Mức | Ghi chú và lỗi |
|---|---|---|---|
| **Composio** | Consumer key `ck_...` (Composio For You, Connect my agent), KHÔNG dùng Project key `ak_` | DỄ | `https://connect.composio.dev/mcp`, header `x-consumer-api-key`. Nối từng app ở For You, Connect Apps (key không tự cập nhật khi nối thêm app). Regenerate thì key cũ chết, bấm Kết nối lại. Lỗi 401 / "Bearer token rejected" = key sai (`connect_health.classify_error`). Một tool chung cho mọi app, quyền soi theo tên lệnh con; Toàn quyền = làm được MỌI hành động trên các app đã nối |
| **Botcake** | Page ID (Fanpage gắn Botcake) + API Key của page (Botcake, Cấu hình, Tích hợp, Public API) | DỄ | Cầu nối nội bộ (`botcake_mcp.py`). Làm mới/xóa key làm các kết nối cũ ngừng. Nhiều page: "+ Thêm tài khoản". Đọc khách, tag, flow; Toàn quyền mới gửi flow |
| **Zernio** | API key (Store, hướng dẫn `tisa-store/huong-dan/zernio.md`) | DỄ | Đăng bài nhiều mạng xã hội; chi tiết tham số: cần xác minh trong mã/Store (không có trong `[app]`) |
| **Substack** | Publication URL, cookie `substack.sid`, User ID | VỪA | Cookie là chìa khóa tài khoản, chủ tự lấy (F12, Application, Cookies) và dán, đừng dán vào chat; mặc định Ghi nháp; gửi email là không thu hồi được |
| **API tuỳ chỉnh** (`http-api`) | `base_url`, `api_key`, `auth_style` (vd `X-API-Key: {key}` hoặc `?api_key={key}`), `extra_headers`, `docs_url` | VỪA | Dịch vụ bất kỳ có API key. Tìm tài liệu bằng `tisa_web_*` trước |
| **Tự thêm (nâng cao)** / `tisa_add_mcp` | URL hoặc lệnh (+ header/env) | VỪA | HTTP, SSE, stdio; OAuth chuẩn MCP tự mở đăng nhập (DCR hoặc CIMD, `tisa_oauth_cimd.py`). HeyGen từng lỗi "Invalid redirect_uri" do client chung của DCR, đã xử lý bằng chọn client (a) CIMD khi có miền HTTPS công khai, (b) DCR, (c) client_id chủ nhập |
| **CRM của tôi** | `crm_url` + API key CRM | DỄ | Địa chỉ ở trang Quản lý web, thẻ Web CRM |
| **Pancake POS, Shopify, TTS Dropship, Webcake, Higgsfield, X, Apify, HeyGen, Bunny** | Theo thẻ trong Store | DỄ đến VỪA | Pancake dán API key (Cấu hình cửa hàng, Ứng dụng & API); Shopify chỉ cần địa chỉ cửa hàng (UCP, chỉ tra cứu); TTS Dropship dán `@publicToken` (sống ~3 ngày) + `@refreshToken` từ Local Storage; Webcake JWT (Node 18+); Higgsfield đăng nhập một chạm (tiêu credit); Apify token Personal API; HeyGen/Bunny khóa lưu bằng `luu_keychain` |

## 11. Lỗi chung của trang Kết nối (`docs/09`, `docs/17`, `connect_health.py`)
- Phân loại tự động: `auth` (Hết phiên đăng nhập, có nút Kết nối lại), `install` (gói npx cài dở, chờ ~2 phút rồi Kiểm tra), `spawn` (không khởi động được trình kết nối: thiếu Node/uv/Git), `net`, `unknown`. Vòng kiểm sức khỏe mỗi 600 giây bằng `tools/list` (không gọi tool thật).
- "Nối được 1 đơn, đơn 2 rớt kết nối" (Pancake): đã sửa 0.52.8.
- Sau cập nhật: server MCP cũ tự thành tài khoản trong trang Kết nối (backup `mcp_servers.v1.bak.json`).
- Đổi file `.py` thì khởi động lại server; giao diện sai thì Ctrl+Shift+R. Cổng 7777 kẹt: tắt tiến trình cũ trước (`docs/17-khac-phuc-su-co.md`).
- Claude báo chưa đăng nhập: trang Models, "Đăng nhập Claude". Máy mất kết nối engine: `claude auth login --claudeai`.
- Trang đăng nhập máy chủ công khai: đặt `TISA_ADMIN_USER` và `TISA_ADMIN_PASSWORD` lúc deploy; bật 2FA.
