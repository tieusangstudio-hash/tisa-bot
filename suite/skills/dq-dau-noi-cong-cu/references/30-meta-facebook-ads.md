# 30 - Sổ tay đấu nối Meta (Facebook Page, Messenger, Instagram, Marketing API / Meta Ads)

Ngày: 19/11/2026. Nguồn chính hãng đọc trực tiếp: developers.facebook.com (các trang dẫn bên dưới). Bài hướng dẫn bên thứ ba ghi rõ [BLOG].

## 1. Hai họ đường nối
| Đường | Độ khó | Dùng khi |
|---|---|---|
| **Meta Ads MCP chính chủ** `https://mcp.facebook.com/ads` | Dễ -> Vừa | Quản lý/báo cáo quảng cáo qua chat. OAuth bấm Cho phép. |
| **Graph API / Marketing API tự tạo app** (Page, Messenger, Instagram, đăng bài, webhook) | Khó | Cần đăng bài Page, nhận tin Messenger, đọc bình luận, IG. |

## 2. Meta Ads MCP chính chủ (xem chi tiết ở `35-mcp-ads.md`)
- Nguồn: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started và bài ra mắt cho dev 16/07/2026 https://developers.facebook.com/blog/post/2026/07/16/meta-ads-mcp-server/.
- Cách người không viết mã: thêm làm connector/MCP từ xa với URL đúng như trên, đăng nhập Facebook bằng tài khoản có vai trò trong Business Manager, tick đúng portfolio (Business) và tài khoản quảng cáo cần dùng. [BLOG: Livain 14/05/2026; AdAdvisor cập nhật 12/11/2026]
- Cách có app riêng (Claude Code): `claude mcp add --transport http --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads`, sau đó `/mcp` để đăng nhập.
- Quyền tối thiểu theo tài liệu: `ads_mcp_management` + (`ads_read` hoặc `ads_management`). Thêm tuỳ chọn: `ads_management`, `catalog_management`, `business_management`, `pages_show_list`, `instagram_basic`.
- Token hệ thống (system user): chỉ vai trò **Employee**; token Admin không vào được.
- Ai cũng nối được server, nhưng công cụ tài khoản quảng cáo được bật dần theo đợt. Cờ `is_ads_mcp_enabled: false` = đợt triển khai chưa tới tài khoản [BLOG]; chờ và thử lại, không có cách ép.

## 3. Marketing API tự tạo app
Nguồn: https://developers.facebook.com/docs/marketing-api/overview/authorization
1. developers.facebook.com/apps > Create app, chọn use case phù hợp (ví dụ "Create & manage ads with ads MCP server" hoặc quảng cáo/Marketing API). Cần tài khoản Facebook đã bật 2FA, người thật xác nhận.
2. Quyền: `ads_read` (báo cáo), `ads_management` (tạo/sửa), `business_management` (quản lý tài sản Business). Standard Access tự động cho app doanh nghiệp: dùng được cho tài khoản của CHÍNH BẠN. Quản lý tài khoản người khác cần **Advanced Access** qua App Review (và Business Verification nếu truy cập dữ liệu nhạy cảm).
3. Giữ Advanced Access: cần >= 500 lệnh gọi thành công trong 15 ngày và tỉ lệ lỗi < 15% trên 500 lệnh gần nhất (tài liệu hiện hành). Tầng truy cập Marketing API: Limited (mặc định, giới hạn tốc độ chặt, "chỉ để phát triển") / Full.
4. System user: Limited được 1 user + 1 admin; Full được 10 + 1.

## 4. Token (nguồn: https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived)
- Token người dùng ngắn hạn: vài giờ. Đổi lấy dài hạn (~60 ngày): `GET https://graph.facebook.com/{ver}/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=TOKEN_NGAN`. Gọi từ máy chủ (có app secret); token đã hết hạn không đổi được.
- **Page access token không hết hạn theo lịch**: lấy từ token người dùng dài hạn của người có vai trò trên Page: `GET /{user-id}/accounts?access_token=<dài-hạn>` -> mỗi Page trả `access_token`. Có thể bị vô hiệu khi đổi mật khẩu/gỡ quyền/mất vai trò.
- Instagram Login: mã 1 giờ, token ngắn 1 giờ, token dài 60 ngày, làm mới được trước khi hết hạn.
- [BLOG] Token Meta Ads MCP thường hết sau ~60 ngày; token hết hạn có thể trả KẾT QUẢ RỖNG thay vì lỗi rõ ràng -> đăng nhập lại.
- Kiểm tra token: Debug Token tool (developers.facebook.com/tools/debug/accesstoken) hoặc `GET /debug_token?input_token=...&access_token=APP_ID|APP_SECRET` (từ kinh nghiệm chung, cần xác minh).

## 5. Facebook Page (đăng bài)
Nguồn: https://developers.facebook.com/docs/pages-api/getting-started
- Quyền: `pages_manage_posts`, `pages_manage_metadata`, `pages_show_list`, và `pages_manage_read_engagement` (tài liệu ghi tên này; một số nơi vẫn dùng `pages_read_engagement`: cần xác minh).
- Trên Page, người dùng cần task `CREATE_CONTENT` để đăng.
- Đăng: `POST /{page-id}/feed` với `message` + Page token. Bài lên ngay, trả post id. Kiểm tra: `GET /{page-id}/feed`.
- Cách lấy ID Page: `GET /me/accounts` bằng token người dùng.

## 6. Messenger
Nguồn: https://developers.facebook.com/docs/messenger-platform/get-started
- Quyền: `pages_show_list` (user token, lấy Page ID), `pages_messaging` (Page token, người có task MESSAGING).
- Lấy PSID: `GET /{page-id}/conversations?fields=participants,messages{id,message}` sau khi tự nhắn thử vào Page bằng tài khoản của mình.
- Gửi: `POST /{page-id}/messages` với `recipient` (PSID), `messaging_type=RESPONSE`, `message`. RESPONSE chỉ được gửi trong **24 giờ** từ tin nhắn cuối của khách; quá 24 giờ phải dùng cơ chế khác (xem Send API; cần xác minh các loại tag hiện hành).
- Webhook: callback URL HTTPS, verify token, đăng ký trường (messages, messaging_postbacks): trang tổng quan fetch được không có phần này, cần đọc riêng và xác minh.
- Trong chế độ **Development**, chỉ người có vai trò trên app mới nhắn được; khách thật chỉ dùng khi app **Live** và quyền đã qua App Review.

## 7. Instagram
Nguồn: https://developers.facebook.com/docs/instagram-platform/overview
- Cần tài khoản chuyên nghiệp (Business/Creator).
- "Instagram Login": không cần Page, gọi `graph.instagram.com`, quyền `instagram_business_basic`, `_content_publish`, `_manage_comments`, `_manage_messages`.
- "Facebook Login": IG phải liên kết Page, gọi `graph.facebook.com`, quyền `instagram_basic`, `instagram_content_publish`, `instagram_manage_*`, kèm `pages_show_list`, `pages_read_engagement`.
- Standard Access chỉ cho người có vai trò trên app (dev/test). Phục vụ tài khoản người khác: Advanced Access cần App Review + Business Verification.

## 8. Chế độ app Development / Live
Nguồn: https://developers.facebook.com/docs/development/build-and-test/app-modes
- Development (mặc định): chỉ người có vai trò dùng được; dữ liệu thử chỉ họ thấy. Live: ai cũng dùng được nhưng quyền phải qua App Review mới chạy với người ngoài. Chuyển bằng nút ở thanh trên App Dashboard; chỉ chuyển khi xong review. Yêu cầu chính sách quyền riêng tư/danh mục: cần xác minh trên màn hình thật.
- Quy tắc nhanh cho chủ doanh nghiệp tự dùng cho Page/tài khoản của mình: dev mode + vai trò admin của app là đủ, khỏi review.

## 9. Lỗi hay gặp (https://developers.facebook.com/docs/graph-api/guides/error-handling)
- **190**: token hết hạn/không hợp lệ (subcode 463/467 hết hạn hoặc bị thu hồi; 460 đổi mật khẩu; 458 chưa cài app) -> lấy token mới/đăng nhập lại.
- **10 / 200-299**: thiếu quyền -> cấp quyền còn thiếu (và vai trò trên Page/tài khoản quảng cáo).
- **4, 17**: giới hạn tốc độ -> chờ rồi thử lại, giảm tần suất. Tầng Limited rất chặt.
- **368**: tạm bị chặn do vi phạm chính sách -> chờ.
- **100** (tham số sai): ví dụ mục tiêu chiến dịch cũ `CONVERSIONS`/`LINK_CLICKS` phải đổi sang `OUTCOME_*` [pipeboard README]. Chưa có trong trang lỗi đã đọc.
- OAuth cửa sổ lặp/đăng nhập sai: cookie bị chặn, nhiều profile Meta trong cùng trình duyệt, chọn nhầm Business -> đăng xuất các phiên Meta khác, dùng cửa sổ ẩn danh [BLOG].
- Thấy tài khoản trùng/không thấy tài khoản quảng cáo: thiếu vai trò trên ad account -> quản trị Business Manager cấp quyền Advertiser/Admin rồi nối lại.
- Ghi bị từ chối: thiếu `ads_management` -> nối lại và cấp quyền ghi.

## 10. Kiểm tra đã nối thật
- MCP: gọi công cụ liệt kê tài khoản quảng cáo, rồi xem insight 7 ngày của một tài khoản (chỉ đọc). Phải thấy ĐÚNG tài khoản/Page của chủ.
- Graph: `GET https://graph.facebook.com/v{ver}/me?access_token=...` (xem tài khoản đang dùng) rồi `GET /me/accounts` (xem Page). Phiên bản `v{ver}` lấy bản hiện hành trong tài liệu, cần xác minh.

## 11. Thu hồi / xoá
- Phía Meta: Facebook Cài đặt > Ứng dụng và trang web (Business Integrations) > gỡ ứng dụng; Business Settings > Integrations; xoá system user token. Tên mục đổi thường xuyên -> cần xác minh trên màn hình thật. Bài [BLOG] không nói rõ gỡ connector phía Claude có cắt quyền phía Meta không -> phải gỡ cả hai.
- Đổi App Secret nếu nghi lộ; token cũ bị vô hiệu theo.
