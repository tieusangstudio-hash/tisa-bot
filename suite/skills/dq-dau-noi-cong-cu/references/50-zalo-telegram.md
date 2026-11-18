# 50 - Sổ tay đấu nối Zalo (OA, ZNS, MCP/QR) và Telegram

Ngày: 19/11/2026. Cổng developers.zalo.me là trang JavaScript: không đọc được nội dung bằng công cụ trong đợt này. Mọi con số Zalo bên dưới đến từ bài thứ ba hoặc README repo cộng đồng và ghi "cần xác minh trên màn hình thật".

## A. Ba cách chạm Zalo - chọn đúng
| Cách | Độ khó | Rủi ro | Dùng khi |
|---|---|---|---|
| 1. Zalo cá nhân qua QR (zalo-agent, claude-plugin-zalo, zca-js) | Vừa (quét QR) | **Có thể bị khóa tài khoản** (README zca-js tự cảnh báo; không chính thức) | Thử nghiệm, tài khoản phụ |
| 2. Zalo OA qua API chính thức (OAuth app) | Khó | Thấp (API chính thức) | Chăm sóc khách, chatbot, tin theo kịch bản |
| 3. ZNS (tin thông báo/giao dịch theo mẫu) | Khó | Chi phí theo tin | Xác nhận đơn, OTP, nhắc lịch |

Khuyến nghị: dùng tài khoản chính của chủ qua cách 1 là RỦI RO; ưu tiên OA (cách 2/3) cho việc kinh doanh. Cách 1 chỉ dùng số phụ và nói rõ rủi ro với chủ.

## B. Zalo cá nhân qua QR (MCP/CLI cộng đồng)
1. **zalo-agent** (https://clawhub.ai/PhucMPham/zalo-agent):
   - Cài CLI `zalo-agent` (kiểm tra `zalo-agent --version`, cập nhật `zalo-agent update`).
   - Đăng nhập: `zalo-agent login --qr-url &` -> mở link/ảnh QR -> trên điện thoại mở Zalo, dùng **Quét mã QR trong ứng dụng Zalo** (không dùng camera hệ thống) -> xác nhận trên điện thoại. **QR hết hạn sau 60 giây.** Người thật quét, không tự động được. Máy chủ QR cục bộ tạm thời đóng sau khi quét hoặc quá giờ.
   - Chạy không màn hình: `zalo-agent login --credentials ./creds.json` (dùng lại thông tin đã xuất). Lưu thông tin ở `~/.zalo-agent-cli/` (cá nhân) và `~/.zalo-agent/` (OA): không đưa vào git/wiki.
   - MCP: `zalo-agent mcp start` (stdio, mặc định), `--http <cổng>` (HTTP), `--auth <token>` (Bearer cho HTTP), `--config <đường dẫn>`. Có 8 tool (gửi, lịch sử, tìm, liệt kê hội thoại, đánh dấu đã đọc...).
   - Giới hạn: một kết nối WebSocket/tài khoản; `listen` và Zalo web không chạy cùng lúc; lịch sử chỉ ~2 tuần; `react`/`undo` cần `cliMsgId`; nhắc tên (mention) chỉ trong nhóm.
   - Đề xuất: mỗi tài khoản một proxy riêng (theo README).
2. **claude-plugin-zalo** (https://cdn.jsdelivr.net/npm/claude-plugin-zalo@0.0.4/README.md):
   - Cần Bun >= 1.2. `claude plugin marketplace add imrim12/claude-plugin-zalo`, rồi `claude plugin install zalo@imrim12`.
   - Đăng nhập: `/zalo:auth` hoặc tool `zalo_login`: tạo `qr-login.png` -> Zalo > Thêm > Quét QR -> xác nhận.
   - Nhận tin nhắn đến cần chạy phiên với cờ `--dangerously-load-development-channels plugin:zalo@imrim12`, nếu không tin đến bị bỏ lặng lẽ. Cờ có chữ "dangerously": chỉ bật khi chủ hiểu rủi ro.
   - Chính sách mặc định `pairing` tự trả lời người lạ bằng mã ghép; `allowlist` bỏ qua người chưa duyệt. Credentials ở `~/.claude/channels/zalo`.
3. **zca-js** (thư viện, không phải MCP): `bun add zca-js`; `zalo.loginQR()`. Cần tự bọc nếu muốn thành MCP.
- Lỗi hay gặp (tổng hợp): QR hết 60 giây -> tạo QR mới; xung đột phiên (đăng nhập Zalo web cùng lúc) -> chỉ để một nơi; tin gửi mà người nhận chưa kết bạn có thể bị chặn (cần xác minh).
- Thu hồi: đăng xuất thiết bị trong Zalo (Cài đặt > Tài khoản và bảo mật > Quản lý đăng nhập / thiết bị, cần xác minh trên màn hình thật), xoá thư mục credentials ở trên.
- **Không** tìm thấy repo "openzca" trong đợt này; nếu chủ có tên chính xác cần kiểm riêng.

## C. Zalo OA qua API chính thức
Cổng: developers.zalo.me (không đọc được trực tiếp). Từ SDK cộng đồng RedAI (https://unpkg.com/@warriorteam/redai-zalo-sdk@1.11.1/docs/AUTHENTICATION.md):
1. Người thật: tạo tài khoản developer, **tạo ứng dụng** (App ID, Secret), tạo/xác thực **OA**, liên kết OA với ứng dụng, khai **Callback URL** (redirect_uri) trong console.
2. Xin quyền OA: URL `https://oauth.zaloapp.com/v4/oa/permission?app_id=...&redirect_uri=...&state=...` (+ PKCE `code_challenge` kiểu S256 nếu bật). Người quản trị OA đăng nhập và bấm Cho phép -> redirect về với `code` và `state` (kiểm tra `state` chống CSRF). Mã chỉ ~10 phút, dùng một lần.
3. Đổi token: các nguồn thứ ba nêu endpoint `https://oauth.zaloapp.com/v4/oa/access_token` (hoặc `/v4/access_token`, mâu thuẫn): cần xác minh; có header `secret_key` (bí mật của app).
4. Thời hạn: README SDK không ghi cố định (`expires_in`); zalo-agent ghi token OA hết sau ~25 giờ và dùng `zalo-agent oa refresh`. Mức "1 giờ/3 tháng" chủ nhắc chưa kiểm được -> cần xác minh. Luôn lưu refresh token mới sau mỗi lần làm mới (dạng xoay vòng: cần xác minh).
5. Webhook OA: cần HTTPS, tên miền đã xác minh; để lấy đủ dữ liệu người dùng có thể cần IP Việt Nam (theo README zalo-agent). Xác minh tên miền: người thật thêm thẻ meta/tệp HTML hoặc bản ghi DNS.
6. Lỗi hay gặp: `-201` tham số sai (code hết hạn, `redirect_uri` lệch); `-216` thông tin app sai hoặc refresh token hết hạn/không hợp lệ (ý nghĩa gộp chung); `-224` API cần gói OA cao hơn (https://zalo.cloud/oa/pricing).
7. Gói OA: nguồn thứ ba ghi gói cơ bản miễn phí giới hạn broadcast; gói trả phí khoảng 99.000 và 399.000 đồng/tháng kèm số tin miễn phí (hoanghamobile, cần đối chiếu: nguồn mâu thuẫn). Không dùng làm giá cam kết.
- Kiểm tra nối thật: gọi API lấy thông tin OA (cần xác minh endpoint trong tài liệu), hoặc `zalo-agent oa` các lệnh lấy thông tin; gửi một tin cho tài khoản thử của chủ.
- Thu hồi: gỡ liên kết ứng dụng khỏi OA, đổi Secret key ở console, xoá token.

## D. ZNS (Zalo Notification Service)
Nguồn: bài thứ ba (fptshop, Infobip, nhanh.vn, eSMS, BrandsVietnam) - chưa đối chiếu cổng Zalo.
- Cần OA đã đăng ký/xác thực, doanh nghiệp tại Việt Nam, có số điện thoại khách.
- Mẫu tin phải được Zalo **duyệt** trước khi gửi (4 dạng: OTP, văn bản, bảng, đánh giá; tối đa 2 nút CTA; tiêu đề tối đa 65 ký tự theo nhanh.vn).
- Hạn mức: OA mới có thể chỉ ~5.000 tin/ngày (BrandsVietnam) hoặc 500/ngày ở giai đoạn đầu (nhanh.vn): nguồn mâu thuẫn, cần xác minh. ZNS "Tag 3" (hậu mãi) cần khách từng nhận ZNS Tag 1/2 trong 12 tháng.
- Phí: có phí theo tin thành công (nhanh.vn ghi 360 đồng/ZNS, chưa kiểm). Cần nạp tiền: **thanh toán là việc người thật làm.**
- Giờ gửi: tin ZBS gửi trong khung 6h-22h trừ OTP (apidocs.nhanh.vn).
- Lỗi hay gặp: mẫu chưa duyệt, số ngoài danh sách thử khi OA chưa xác thực, hết hạn mức ngày, số tiền trong tài khoản không đủ.

## E. Telegram (dễ nhất)
1. Tạo bot: trong Telegram nhắn **@BotFather** -> `/newbot` -> đặt tên và username (kết thúc bằng `bot`) -> nhận **token** (như mật khẩu; https://core.telegram.org/bots/tutorial). Người thật làm trên điện thoại/Telegram.
2. Kiểm tra token: `curl "https://api.telegram.org/bot<TOKEN>/getMe"` -> trả `ok: true` và tên bot.
3. Lấy `chat_id`: nhắn tin cho bot (hoặc thêm bot vào nhóm và nhắn một tin) rồi `curl "https://api.telegram.org/bot<TOKEN>/getUpdates"`, đọc `message.chat.id` (nhóm thường là số âm). Bot không tự nhắn trước cho người chưa từng chat với nó.
4. Gửi thử: `curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" -d chat_id=<ID> -d text="Xin chao"` (văn bản 1-4096 ký tự).
5. `getUpdates` và webhook **loại trừ nhau**: đã `setWebhook` thì `getUpdates` không dùng được; đổi lại bằng `deleteWebhook` (tuỳ chọn `drop_pending_updates`). Webhook: HTTPS, cổng 443/80/88/8443, `secret_token` 1-256 ký tự (A-Z a-z 0-9 _ -) gửi lại ở header `X-Telegram-Bot-Api-Secret-Token`; non-2xx thì Telegram gửi lại. `getWebhookInfo` cho biết lỗi giao hàng gần nhất. (https://core.telegram.org/bots/api)
6. Cập nhật không lưu lâu: Telegram không giữ update sau khi bạn đã nhận (theo tutorial).
7. Bot trong nhóm: chế độ riêng tư (privacy mode) mặc định chỉ thấy lệnh/mention; tắt bằng BotFather `/setprivacy` (cần xác minh trên màn hình thật). Giới hạn tốc độ (khoảng 1 tin/giây mỗi chat, 20/phút trong nhóm, ~30/giây toàn bot): kiến thức chung, chưa đọc được trong trang tài liệu đợt này, cần xác minh.
8. Thu hồi/đổi token: BotFather > chọn bot > API Token > Revoke (cần xác minh tên mục).
9. MCP Telegram:
   - Chọn **bot** (an toàn): n24q02m/better-telegram-mcp (biến `TELEGRAM_BOT_TOKEN`), tensakulabs/telegram-mcp (nhỏ, hướng bot).
   - **Tài khoản người dùng** (Telethon, cần API ID/hash từ my.telegram.org): chigwell/telegram-mcp (~1,3k sao thứ cấp), jgalea/telegram-mcp. Quyền như chính chủ: rủi ro cao, không bật ghi tuỳ tiện. Chú ý trùng tên gói PyPI `telegram-mcp` (README chigwell cảnh báo không phải cùng dự án).
   - Bot chỉ thấy kênh/nhóm nó có mặt; muốn đọc hội thoại cá nhân phải dùng tài khoản người dùng.
10. Kiểm tra nối thật: `getMe`, sau đó gửi tin vào chat của chính chủ và chủ xác nhận nhận được.
