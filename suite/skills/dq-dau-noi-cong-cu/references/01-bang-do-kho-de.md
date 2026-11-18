# 01 - Bảng độ khó DỄ -> KHÓ cho từng công cụ

Ngày: 19/11/2026. Thời gian là ước tính cho người đã có tài khoản, chưa kể thời gian chờ duyệt dài. "Người thật" = việc AI không làm thay (đăng nhập, mật khẩu, OTP/2FA, CAPTCHA, đồng ý điều khoản, thanh toán, xác minh). Ước tính dựa trên tài liệu/bài hướng dẫn đã đọc, chưa chạy thử thực tế: cần xác minh bằng lần chạy đầu tiên.

## Định nghĩa
- **Dễ**: MCP công khai không mã, chỉ OAuth bấm Cho phép. 5-15 phút.
- **Vừa**: dán API key/token, hoặc cài CLI cục bộ. 15-60 phút.
- **Khó**: tạo app OAuth, xét duyệt, developer token/cấp truy cập, xác minh doanh nghiệp, tên miền/DNS, webhook công khai. 1 giờ đến vài ngày, có thể vài tuần nếu chờ duyệt.

## Bảng tổng hợp (xếp từ dễ đến khó)
| # | Công cụ | Mức | Thời gian | Việc chỉ người thật làm | Chi tiết |
|---|---|---|---|---|---|
| 1 | TikTok Ads MCP (OAuth) | Dễ | 5-10 phút (+ gia hạn ~30 ngày, BLOG) | Đăng nhập TikTok for Business, bấm Cho phép | 35 |
| 2 | Stripe MCP (connector/OAuth, sandbox) | Dễ | 5-10 phút | Đăng nhập Stripe, bấm Cho phép, duyệt hoàn tiền | 60 |
| 3 | Cloudflare MCP chính chủ (OAuth) | Dễ | 5-10 phút | Đăng nhập, chọn quyền, bấm Cho phép | 70 |
| 4 | Meta Ads MCP chính chủ (OAuth, không app) | Dễ -> Vừa | 5-15 phút; có thể chờ Meta bật tài khoản (ngày) | Đăng nhập Facebook, chọn đúng ad account, cấp `ads_management` nếu cần ghi | 35, 30 |
| 5 | Telegram bot (BotFather + dán token) | Dễ -> Vừa | 5-10 phút | Nhắn BotFather, chép token kín, nhắn thử bot | 50 |
| 6 | Connector Google có sẵn trong Claude (nếu gói có; chưa kiểm) | Dễ | 5 phút | Đăng nhập Google, bấm Cho phép | 20 |
| 7 | MCP stdio cục bộ chung (npx/uvx + env) | Vừa | 10-30 phút | Dán khóa vào chỗ an toàn | 10 |
| 8 | Zalo cá nhân qua QR (zalo-agent/plugin) | Vừa (rủi ro khóa) | 10-20 phút | Quét QR trong 60 giây bằng điện thoại, xác nhận | 50 |
| 9 | Cloudflare Wrangler login + `wrangler deploy` web tĩnh | Vừa | 10-30 phút | Đăng nhập, bấm Cho phép OAuth; tạo/dán API token nếu dùng token | 70 |
| 10 | SePay (liên kết ngân hàng + webhook) | Vừa | 20-60 phút | Đăng ký, liên kết ngân hàng (OTP), duyệt cấu hình | 60 |
| 11 | pipeboard Meta Ads MCP (host) | Vừa | 5-15 phút | Đăng nhập Facebook, chọn tài khoản | 35 |
| 12 | payOS (kênh thanh toán + 3 khóa + webhook) | Vừa -> Khó | 30-60 phút + chờ xác minh | Đăng ký, xác minh ngân hàng/kênh, dán khóa | 60 |
| 13 | Google Workspace qua `workspace-mcp` (tự tạo OAuth client) | Khó | 20-45 phút | Đăng nhập Google Cloud, đồng ý điều khoản, tạo client, thêm test user, bấm "Nâng cao > Đi tới", 2FA | 20 |
| 14 | Google Workspace MCP chính chủ (preview) | Khó | 45-90 phút + vào chương trình preview | Như trên + đăng ký Developer Preview, tick "AI agent" | 20 |
| 15 | Cloudflare gắn tên miền riêng + DNS | Khó/Vừa | 15 phút thao tác + vài giờ nameserver | Đổi nameserver ở nhà đăng ký (đăng nhập/OTP), mua tên miền | 70 |
| 16 | Telegram qua tài khoản người dùng (Telethon, API ID/hash) | Khó/rủi ro | 20-30 phút | Đăng nhập my.telegram.org, mã đăng nhập gửi về Telegram | 50 |
| 17 | Google Ads MCP (gcloud + OAuth + quyền truy cập dự án) | Khó | 1 giờ + chờ duyệt quyền truy cập (có thể vài ngày) | Đăng nhập, tạo OAuth client, `gcloud auth ...` bấm Cho phép, xin mức truy cập | 35 |
| 18 | Meta Graph API tự tạo app (Page, Messenger, Instagram) dev mode | Khó | 1-2 giờ | Đăng nhập, 2FA, tạo app, thêm use case, tạo token | 30 |
| 19 | Meta App Review + Business Verification (phục vụ người ngoài/Live) | Rất khó | Ngày -> tuần | Hồ sơ, quay video demo, giấy tờ doanh nghiệp | 30 |
| 20 | TikTok Marketing API (app + duyệt) | Khó | Ngày -> tuần | Tạo tài khoản dev, tạo app, gửi duyệt, ủy quyền | 40 |
| 21 | TikTok Content Posting API (+ audit) | Khó | Ngày -> tuần | Đăng ký app, xác minh tên miền (DNS), audit, ủy quyền | 40 |
| 22 | Zalo OA API (app + OA + OAuth + webhook) | Khó | 1-3 giờ + xác thực OA | Tạo app/OA, xác thực OA, bấm Cho phép, xác minh tên miền webhook | 50 |
| 23 | Zalo ZNS (mẫu duyệt + hạn mức + nạp tiền) | Khó | Vài ngày (duyệt mẫu) | Duyệt mẫu, nạp tiền, xác thực OA | 50 |

## Cách dùng bảng
- Khách hỏi "nối X": tra mức -> báo thời gian và việc họ phải tự bấm TRƯỚC khi bắt đầu (đỡ bất ngờ ở giữa chừng).
- Cùng một mục tiêu có nhiều đường: ưu tiên đường **Dễ** hơn (ví dụ quảng cáo Meta: MCP chính chủ trước, tự tạo app sau; web: Wrangler trước, tên miền riêng sau).
- Dừng ở các điểm "người thật" và đưa hướng dẫn từng bước; không tự nhập mật khẩu/OTP/thẻ/khóa.
- Chạm tài khoản thật (email, quảng cáo, thanh toán, Page): đọc trước, ghi sau, chủ duyệt từng việc ghi; quảng cáo luôn tạo TẠM DỪNG.

## Tổng kết cảnh báo độ tin cậy
- Chắc (đã đọc trang chính hãng trực tiếp): Claude Code MCP, Inspector, Meta Ads MCP (tài liệu dev), Meta Graph/Marketing authorization, token Meta, Stripe MCP, Cloudflare (MCP, token, Wrangler login, static assets, custom domains, giới hạn Free), Google OAuth (hết hạn token, consent, tạo client), google-ads-mcp, Google Workspace MCP chính chủ, TikTok Content Posting (đoạn đọc được), Telegram core.
- Yếu (chỉ bài thứ ba hoặc không đọc được): toàn bộ cổng Zalo, ZNS, TikTok Marketing API và TikTok Ads MCP chi tiết, payOS đăng ký, thời hạn token TikTok Ads, quy trình thu hồi trên nhiều nền tảng, mọi tên menu giao diện.
