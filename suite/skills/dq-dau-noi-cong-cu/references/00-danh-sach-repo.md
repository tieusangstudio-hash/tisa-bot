# 00 - Danh sách repo, skill, tài liệu đáng dùng để đấu nối

Ngày nghiên cứu: 19/11/2026. Số sao đọc trực tiếp từ trang GitHub trong đợt này (có thể đã lệch). Chỗ nào ghi "(thứ cấp)" là số liệu từ trang tổng hợp, chưa đọc thẳng từ GitHub.

Quy ước độ tin: [CHÍNH CHỦ] tài liệu của chính hãng; [CỘNG ĐỒNG] repo bên thứ ba; [BLOG] bài hướng dẫn bên thứ ba (kiểm lại với tài liệu hãng).

## A. Nền tảng MCP (cài, cấu hình, gỡ lỗi)

1. **modelcontextprotocol/servers** - https://github.com/modelcontextprotocol/servers - ~92,1k sao. [CHÍNH CHỦ]
   - Vì sao: bộ server mẫu chuẩn (Everything, Fetch, Filesystem, Git, Memory, Time...). Các server cũ (GitHub, Slack, Google Drive, Postgres...) đã chuyển sang repo `servers-archived`.
   - Lấy gì: mẫu cấu hình `mcpServers` (command + args), cách `npx -y` / `uvx`, ghi chú Windows phải bọc `cmd /c npx`, lưu ý đường dẫn tuyệt đối. README tự nhắc: đây là bản tham khảo, không phải sản phẩm production.
2. **anthropics/skills - mcp-builder** - https://github.com/anthropics/skills/blob/main/skills/mcp-builder/SKILL.md [CHÍNH CHỦ]
   - Lấy gì: quy trình 4 pha (nghiên cứu, cài đặt, kiểm tra, đánh giá), chọn transport (HTTP cho từ xa, stdio cho cục bộ), đặt tên tool `dich-vu_hanh-dong`, annotation `readOnlyHint/destructiveHint`, thông báo lỗi chỉ cách sửa.
3. **modelcontextprotocol/inspector** - https://github.com/modelcontextprotocol/inspector [CHÍNH CHỦ]
   - Lấy gì: công cụ thử server độc lập. Có chế độ dòng lệnh `--cli` để kiểm tra "nối được thật" bằng 1 lệnh và mã thoát rõ ràng (xem `10-mcp-chung.md`). Bản mới (v2) đổi cờ so với v1, cần Node mới.
4. **Tài liệu Claude Code về MCP** - https://code.claude.com/docs/en/mcp [CHÍNH CHỦ]
   - Lấy gì: `claude mcp add/list/get/remove`, phạm vi local/project/user, `.mcp.json` có `${VAR}`, OAuth qua `/mcp`, `--callback-port`, `--client-id`, thời gian chờ `MCP_TIMEOUT`, bảng trạng thái khi `claude mcp list`.
5. **Tài liệu gỡ lỗi MCP** - https://modelcontextprotocol.io/docs/tools/debugging [CHÍNH CHỦ]
   - Lấy gì: vị trí log Claude Desktop (`~/Library/Logs/Claude/mcp*.log`), lỗi hay gặp (thư mục làm việc, biến môi trường không kế thừa, đường dẫn), server stdio không được ghi ra stdout.
6. **punkpeye/awesome-mcp-servers** (~90k sao, thứ cấp) và **wong2/awesome-mcp-servers** (~4k, thứ cấp) - danh mục tra cứu server theo lĩnh vực. Không phải phần mềm; mỗi server có cách cài riêng. Dùng để TÌM, rồi tự đọc README của server trước khi cài.

## B. Google

7. **taylorwilsdon/google_workspace_mcp** - https://github.com/taylorwilsdon/google_workspace_mcp - ~3,5k sao, MIT. [CỘNG ĐỒNG]
   - Vì sao: phủ Gmail, Drive, Calendar, Docs, Sheets, Tasks, Slides, Forms, Contacts, Chat. Có mức công cụ `core/extended/complete`, `--read-only`, chạy `uvx workspace-mcp`.
   - Lấy gì: biến `GOOGLE_OAUTH_CLIENT_ID/SECRET`, redirect `http://localhost:PORT/oauth2callback`, `claude mcp add --transport http workspace-mcp http://localhost:8000/mcp`, cảnh báo prompt injection.
8. **Google Workspace MCP chính chủ (bản xem trước)** - https://developers.google.com/workspace/guides/configure-mcp-servers [CHÍNH CHỦ, preview]
   - Lấy gì: mỗi sản phẩm một endpoint `https://gmailmcp.googleapis.com/mcp/v1`..., phải vào Developer Preview Program, OAuth client loại Web có tick "AI agent", redirect Claude `https://claude.ai/api/mcp/auth_callback`.
9. **googleads/google-ads-mcp** - https://github.com/googleads/google-ads-mcp - ~1,2k sao, Apache-2.0. [CHÍNH CHỦ]
   - Lấy gì: chỉ đọc theo mặc định (tìm GAQL, liệt kê tài khoản), công cụ ghi có luồng "đề xuất rồi xác nhận" bằng checksum, đăng nhập `gcloud auth application-default login` với scope `adwords`.

## C. Meta, TikTok

10. **Meta Ads MCP chính chủ** - https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started [CHÍNH CHỦ]
    - Lấy gì: URL `https://mcp.facebook.com/ads`, OAuth (Facebook Login for Business) hoặc token, quyền tối thiểu `ads_mcp_management` + `ads_read`/`ads_management`. Bài ra mắt cho dev: https://developers.facebook.com/blog/post/2026/07/16/meta-ads-mcp-server/ (16/07/2026).
11. **pipeboard-co/meta-ads-mcp** - https://github.com/pipeboard-co/meta-ads-mcp - ~1,4k sao, giấy phép BSL 1.1 (thành Apache 2.0 ngày 01/01/2029). [CỘNG ĐỒNG]
    - Lấy gì: server Meta Ads có từ trước bản chính chủ; mặc định tạo chiến dịch/nhóm/quảng cáo ở trạng thái PAUSED; mục tiêu phải kiểu mới (OUTCOME_*), ngân sách tính bằng đơn vị nhỏ (cent).
12. **TikTok for Business MCP (Ads)** - https://ads.tiktok.com/resources/help/article/about-tiktok-for-business-mcp-server [CHÍNH CHỦ]
    - Lấy gì: 2 endpoint `.../open_mcp/tt-ads-mcp-flat` (~400 tool) và `.../tt-ads-mcp-layer` (~40 tool lõi); tài liệu kỹ thuật `https://business-api.tiktok.com/portal/docs/tiktok-ads-mcp-server/v1.3`.

## D. Zalo, Telegram

13. **zalo-agent** (CLI + MCP) - https://clawhub.ai/PhucMPham/zalo-agent [CỘNG ĐỒNG] - đăng nhập QR cho tài khoản cá nhân, hoặc OA qua API chính thức; `zalo-agent mcp start`.
14. **imrim12/claude-plugin-zalo** - https://cdn.jsdelivr.net/npm/claude-plugin-zalo@0.0.4/README.md [CỘNG ĐỒNG] - plugin Claude Code, tool `zalo_login` tạo ảnh QR.
15. **zca-js** (thư viện không chính thức cho Zalo cá nhân) - https://cdn.jsdelivr.net/npm/zca-js@2.2.0/README.md [CỘNG ĐỒNG] - README tự cảnh báo có thể bị khóa tài khoản.
   - Không tìm thấy repo tên "openzca" trong đợt này; nếu chủ có link thì cần kiểm riêng.
16. **chigwell/telegram-mcp** (~1,3k sao, thứ cấp) và **n24q02m/better-telegram-mcp** - Telegram qua Telethon (tài khoản người dùng) hoặc bot token. Tài khoản người dùng = toàn quyền, rủi ro cao.

## E. Thanh toán, Cloudflare

17. **Stripe MCP** - https://docs.stripe.com/mcp [CHÍNH CHỦ] - `https://mcp.stripe.com`, OAuth hoặc "agent API key"; hạn chót chuyển khóa 30/11/2026.
18. **SePay developer** - https://developer.sepay.vn [CHÍNH CHỦ] - webhook, 4 kiểu xác thực, API token. Không thấy MCP.
19. **payOS docs/SDK** - https://payos.vn/docs/ [CHÍNH CHỦ] - 3 khóa Client ID/API Key/Checksum Key. Không thấy MCP.
20. **cloudflare/mcp-server-cloudflare** (~4,5k sao) và **cloudflare/mcp** - https://github.com/cloudflare/mcp-server-cloudflare [CHÍNH CHỦ] - server khuyến nghị `https://mcp.cloudflare.com/mcp` (OAuth hoặc API token).

## 5 nguồn đáng nhất (xếp hạng)
1. Tài liệu Claude Code MCP (nền cho mọi thao tác `claude mcp add`).
2. modelcontextprotocol/inspector (kiểm tra "nối được thật" bằng 1 lệnh).
3. Meta Ads MCP chính chủ (đổi cuộc chơi: bấm Cho phép là xong, không cần tự tạo app).
4. taylorwilsdon/google_workspace_mcp (nối Gmail/Lịch/Drive/Sheets/Docs/Tasks trong một server).
5. cloudflare/mcp-server-cloudflare (đưa web lên mạng + quản lý hạ tầng cho học viên).
