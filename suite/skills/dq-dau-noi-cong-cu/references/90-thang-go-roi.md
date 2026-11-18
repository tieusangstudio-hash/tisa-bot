# 90 - Thang gỡ rối chung khi nối công cụ không được

Ngày: 19/11/2026. Dùng theo thứ tự từ trên xuống. Mỗi bước kiểm tra rẻ, nhanh trước, bước tốn công sau. Dừng ngay khi tìm ra nguyên nhân; ghi lại bước đã thử để khỏi lặp.

Nguyên tắc: (1) đổi MỘT thứ mỗi lần; (2) đọc nguyên văn thông báo lỗi, đừng đoán; (3) không dán khóa/token/mã vào chat, không in ra log; (4) chạm vào hộp thư/quảng cáo/tiền thật chỉ bằng lệnh chỉ đọc cho tới khi chủ duyệt.

## Thang 12 bậc
1. **Đọc đúng lỗi.** Chép nguyên văn (mã lỗi, `log_id`, request id). Phân loại: không tới được (mạng), 401/403 (quyền), 400 (tham số), 404 (sai đường dẫn/ID), 429 (giới hạn), 5xx (phía họ).
2. **Đăng nhập đúng tài khoản/profile.** Trình duyệt đang đăng nhập tài khoản nào? Nhiều profile Chrome, nhiều tài khoản Google/Meta/TikTok dễ gây "thấy tài khoản trống" hoặc "duplicate account". Mở cửa sổ ẩn danh hoặc profile sạch, đăng nhập đúng người, thử lại. Vai trò: tài khoản đó có vai trò (admin/advertiser/developer/tester) trên Page, ad account, app hay không?
3. **Đúng dự án/app/tài khoản.** Google: đúng dự án Cloud chứa OAuth client và API đã bật. Meta: đúng App ID, đúng Business/portfolio, đúng ad account. Cloudflare: đúng account id (`wrangler whoami`). Stripe/PayOS: sandbox hay live, đúng kênh.
4. **API/dịch vụ đã bật chưa.** Google: bật API trong Library; thông báo "has not been used... or disabled" -> bật và đợi vài phút. Meta: đã thêm đúng use case/sản phẩm (Messenger, Marketing API, ads MCP). TikTok: đã thêm sản phẩm Content Posting/Login Kit.
5. **Scope/quyền.** So scope đã cấp với scope cần (xem file từng công cụ). Thiếu -> thu hồi quyền cũ, cấp lại đủ. Cẩn thận: nhiều dịch vụ trả kết quả RỖNG thay vì lỗi khi thiếu quyền (Cloudflare MCP, Meta token hết hạn).
6. **Chế độ ứng dụng.** Google: Testing (token 7 ngày, chỉ test users) hay In production (chưa xác minh = tối đa 100 người). Meta: Development (chỉ người có vai trò) hay Live (cần App Review). TikTok: chưa qua audit = đăng chỉ riêng tư. Meta Ads MCP: tài khoản chưa được bật đợt (`is_ads_mcp_enabled: false`).
7. **Redirect URI/callback.** So từng ký tự: `http` vs `https`, `localhost` vs `127.0.0.1`, cổng, dấu `/` cuối, chữ hoa. Cổng gọi lại cố định: `--callback-port` (Claude Code). Lỗi `redirect_uri_mismatch`/`invalid_request` ở TikTok là cùng nguyên nhân.
8. **Mã/token hết hạn hoặc bị thu hồi.** Google Testing 7 ngày; refresh token 6 tháng không dùng; đổi mật khẩu. Meta token người dùng ~60 ngày, Page token không hết hạn theo lịch nhưng bị vô hiệu khi đổi mật khẩu/mất vai trò. TikTok Ads MCP 30 ngày (BLOG); TikTok user token 2 giờ + refresh 180 ngày xoay vòng. Zalo OA token ngắn, QR cá nhân 60 giây. Cách xử: làm mới hoặc đăng nhập lại.
9. **Múi giờ và đồng hồ.** Chữ ký HMAC (SePay timestamp lệch quá 300 giây bị từ chối), JWT, lịch Calendar, báo cáo quảng cáo theo múi giờ tài khoản (so với giờ Việt Nam). Kiểm tra đồng hồ máy đúng giờ mạng.
10. **Quota, giới hạn tốc độ, gói.** Meta mã 4/17; Cloudflare Free 100k yêu cầu/ngày (lỗi 1027); TikTok Smart+ 1 thao tác/5 giây; payOS 429; Zalo gói OA/ZNS hạn mức ngày; Inspector mã 11. Chờ, giảm tần suất, nâng gói (việc người thật nếu tốn tiền).
11. **Mạng, tường lửa, VPN, proxy, quản trị IT.** Server MCP từ xa không tới được (Inspector mã 4): thử mạng khác/tắt VPN; công ty có thể chặn miền (Stripe: nhờ cho phép `mcp.stripe.com`); Workspace admin chặn ứng dụng bên thứ ba. Chrome/trình duyệt chặn cookie bên thứ ba làm vòng lặp đăng nhập.
12. **Phiên bản CLI/gói và môi trường chạy.**
    - Cập nhật: `claude --version` và cập nhật Claude Code; `npx wrangler@latest`; `pipx upgrade google-ads-mcp`; `uvx` tự lấy bản mới nhất (ghim phiên bản để lặp lại được).
    - PATH/ENOENT: app mở từ Dock không có PATH của terminal -> dùng đường dẫn tuyệt đối tới `npx/uvx/node/python`.
    - Node/Python quá cũ (Inspector cần Node mới; workspace-mcp cần Python 3.11+).
    - Biến môi trường có xuống dòng/khoảng trắng thừa (lỗi `Leading or trailing whitespace`).
    - Cấu hình JSON sai cú pháp; mục `url` thiếu `type`; cần thoát hẳn client rồi mở lại (Claude Desktop).

## Công cụ chẩn đoán nhanh
- MCP: `claude mcp list` (trạng thái), `/mcp`, `claude --debug-file /tmp/x.log`, log `~/Library/Logs/Claude/mcp*.log`, Inspector `--cli ... --method initialize`/`tools/list` (mã thoát 3 chưa xác thực, 4 không tới server, 5 tool lỗi, 11 429). Xem `10-mcp-chung.md`.
- Hạ tầng: `curl -I https://...`, `dig ten-mien +short`, `curl -v` để xem mã trạng thái/tiêu đề; `wrangler whoami`, `WRANGLER_LOG=debug`.
- Token: Google tokeninfo (cần xác minh), Meta Debug Token tool, Cloudflare `tokens/verify`, Telegram `getMe`, `getWebhookInfo`.
- Trình duyệt thật (DevTools > Network, Console): thấy yêu cầu OAuth thất bại ở bước nào, đọc tham số `error`/`error_description` trên thanh địa chỉ.

## Khi người thật phải vào cuộc (dừng, báo chủ, đừng cố vượt)
Đăng nhập, mật khẩu, OTP/2FA, CAPTCHA, xác minh email/số điện thoại, đồng ý điều khoản, thanh toán/nạp tiền, xác minh doanh nghiệp, gửi hồ sơ duyệt app/audit, đổi nameserver tại nhà đăng ký, cấp quyền admin. AI chuẩn bị link và hướng dẫn từng bước, chủ tự bấm.

## Cách tự nghiên cứu khi vẫn kẹt
1. **Tìm lỗi nguyên văn** (đặt trong ngoặc kép) + tên công cụ trên GitHub Issues của chính repo: `"<thông báo lỗi>" repo:taylorwilsdon/google_workspace_mcp`; `repo:anthropics/claude-code "mcp" "<lỗi>"`; `repo:cloudflare/workers-sdk "<lỗi>"` cho Wrangler. Đọc cả issue đã đóng: thường có cách sửa ở bình luận cuối hoặc ở bản phát hành.
2. **StackOverflow/diễn đàn hãng**: `site:stackoverflow.com "<lỗi>" <dịch vụ>`; Meta: developers.facebook.com/community; Cloudflare: community.cloudflare.com; TikTok: developers.tiktok.com/community; Zalo: nhóm nhà phát triển (cần xác minh).
3. **Changelog/ghi chú phát hành**: kiểm tra phiên bản đang cài có nằm trước một bản sửa không (GitHub Releases/CHANGELOG; Claude Code changelog; Wrangler releases; Meta Graph API changelog và Marketing API deprecations; Google Ads API release notes; Stripe changelog). Ví dụ đã gặp trong nghiên cứu này: Claude bỏ sót tool sau 256 tool đầu (sửa 20/07/2026), tên công cụ google-ads-mcp đổi từ v0.0.6, Stripe ngừng nhận khóa không có thẻ Agent từ 12/2026, Google Ads chuyển cách cấp truy cập.
4. **Đọc tài liệu chính hãng bằng tay** khi bài hướng dẫn mâu thuẫn: ưu tiên trang developers.* của chính hãng; bài blog chỉ để gợi ý. Ghi ngày của nguồn.
5. **Tái hiện nhỏ nhất**: thử bằng `curl`/Inspector (không qua TISA BOT) để biết lỗi ở dịch vụ hay ở lớp cấu hình.
6. **Chụp màn hình thật** các bước giao diện đã đổi và cập nhật lại sổ tay: nguồn nào ghi "cần xác minh trên màn hình thật" phải được người/AI xác minh và sửa ngay trong file tương ứng.
7. **Báo cáo lại cho chủ** theo mẫu: đã làm gì (bước thang nào), lỗi nguyên văn (che khóa), nguyên nhân khả dĩ, việc chủ cần tự bấm.

## Mẫu ghi nhật ký sự cố (3 dòng)
- Công cụ + phiên bản + máy (Mac/Windows) + tài khoản (ẩn danh).
- Lỗi nguyên văn + bước thang đã loại trừ.
- Cách đã sửa hoặc câu hỏi còn mở.
