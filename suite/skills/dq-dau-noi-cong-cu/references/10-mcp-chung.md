# 10 - Sổ tay MCP chung (cài, cấu hình, OAuth, gỡ lỗi)

Ngày: 19/11/2026. Nguồn chính: https://code.claude.com/docs/en/mcp, https://modelcontextprotocol.io/docs/tools/debugging, https://github.com/modelcontextprotocol/inspector, https://github.com/modelcontextprotocol/servers.

## 1. Ba loại kết nối (transport)
- **HTTP (streamable)**: server từ xa, khuyến nghị cho dịch vụ đám mây. `claude mcp add --transport http <tên> <url>`.
- **SSE**: cũ, đã bị đánh dấu lỗi thời. Bản Claude Code mới (ghi v2.1.265+) thử HTTP trước rồi tự chuyển SSE; bản cũ cần `--transport sse`. Server Cloudflare đã tắt `/sse`, trả `410 Gone` và báo dùng `/mcp`.
- **stdio**: server chạy ngay trên máy. `claude mcp add [tuỳ chọn] <tên> -- <lệnh> [tham số]`. Mọi thứ sau `--` đi nguyên cho server. Truyền khóa: `--env KEY=giá-trị`.
- WebSocket (`ws`): chỉ khai báo qua `add-json` hoặc `.mcp.json`, không có trong `--transport`.

## 2. Phạm vi lưu cấu hình
| Phạm vi | Cờ | Lưu ở | Ghi chú |
|---|---|---|---|
| local (mặc định) | `-s local` | `~/.claude.json` | riêng dự án, riêng tư |
| project | `--scope project` | `.mcp.json` ở gốc dự án | chia sẻ qua git, hỏi duyệt khi mở |
| user | `--scope user` | `~/.claude.json` | mọi dự án |
Ưu tiên: local > project > user > plugin > connector claude.ai. Không trộn giữa các phạm vi.
Lệnh quản lý: `claude mcp list`, `claude mcp get <tên>`, `claude mcp remove <tên>`, trong phiên gõ `/mcp`.

## 3. `.mcp.json` mẫu (biến môi trường không ghi cứng khóa)
```json
{ "mcpServers": {
  "api": { "type": "http", "url": "${API_BASE_URL:-https://api.example.com}/mcp",
           "headers": { "Authorization": "Bearer ${API_KEY}" } } } }
```
- `${VAR}` mở rộng thành giá trị; `${VAR:-mặc định}` dùng mặc định khi chưa đặt. Biến chưa đặt và không có mặc định: cảnh báo, giữ nguyên chữ `${VAR}`.
- Mục có `url` mà thiếu `type` sẽ bị coi là stdio và bị bỏ qua -> báo `has a "url" but no "type"`. Luôn ghi `"type": "http"`.
- Token dán thừa dấu xuống dòng gây lỗi `Leading or trailing whitespace`.
- Tên dành riêng không dùng được: `workspace`, `claude-in-chrome`, `computer-use`, `Claude Preview`, `Claude Browser`.
- Khóa dịch vụ Anthropic (`ANTHROPIC_API_KEY`...) bị làm rỗng khi gửi sang server từ xa: copy sang biến tên khác.

## 4. OAuth cho server từ xa
1. `claude mcp add --transport http <tên> <url>`.
2. Trong phiên gõ `/mcp`, chọn server, làm theo cửa sổ trình duyệt. Hoặc ngoài phiên: `claude mcp login <tên>` (thêm `--no-browser` để in link thay vì mở).
3. Cần cổng gọi lại cố định (dịch vụ chỉ cho phép redirect đã đăng ký): `--callback-port 8080`.
4. Dịch vụ không hỗ trợ đăng ký động, bạn có app OAuth riêng: `--client-id <ID> --client-secret` (nhập khóa ở ô ẩn; CI dùng biến `MCP_CLIENT_SECRET`).
5. Giới hạn scope: trong `.mcp.json` mục `"oauth": {"scopes": "a b c"}`.
6. Thu hồi: `claude mcp logout <tên>` rồi thu hồi phía dịch vụ (trang "ứng dụng đã kết nối" của họ).
Việc chỉ người thật làm: đăng nhập, bấm Cho phép, mã OTP/2FA.

## 5. Kiểm tra "nối được thật"
- Trong Claude Code: `claude mcp list` -> trạng thái `Connected` / `Needs authentication` / `Failed to connect` (kèm lý do) / `Pending approval` / `Disabled`. Rồi gọi thử một tool CHỈ ĐỌC nhỏ (vd liệt kê tài khoản).
- Độc lập bằng Inspector (cần Node mới, xem README):
  - Bắt tay: `npx @modelcontextprotocol/inspector --cli --transport http --server-url <url> --method initialize`
  - Liệt kê tool: `... --method tools/list --format json`
  - Gọi tool: `... --method tools/call --tool-name <tên> --tool-args-json '{"k":"v"}' --format json`
  - stdio: thay phần transport bằng lệnh server, ví dụ `npx @modelcontextprotocol/inspector --cli node build/index.js --method tools/list`.
  - Mã thoát: 0 ok; 3 chưa xác thực; 4 không tới được server; 5 tool lỗi; 11 bị giới hạn tốc độ (429); 12 URL OAuth bị chặn.
  - Dùng `--connect-timeout <ms>` để khỏi treo; ghim phiên bản cụ thể khi viết kịch bản tự động.
- Cẩn thận: Inspector v2 đổi cờ so với v1 (`--config` và `--catalog` tách riêng): cần xác minh bằng `--help` của bản đang cài.

## 6. Thời gian chờ
- `MCP_TIMEOUT=10000 claude` (khởi động 10 giây). `MCP_TOOL_TIMEOUT` (mili giây) cho cuộc gọi tool; riêng từng server: `"timeout": 600000`.
- Cuộc gọi chạy quá 2 phút tự chuyển nền (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`).
- Server stdio được tắt theo thứ tự SIGINT, SIGTERM, SIGKILL.

## 7. Lỗi stdio hay gặp (tài liệu gỡ lỗi MCP)
- Thư mục làm việc có thể không xác định (macOS có thể là `/`): dùng đường dẫn tuyệt đối cho `command`, file dữ liệu, `.env`.
- Server stdio chỉ kế thừa một phần biến môi trường: khóa phải khai trong `env` của cấu hình.
- App chạy từ Dock/Finder không thấy PATH của terminal -> `npx`/`uvx` "không tìm thấy" (ENOENT). Dùng đường dẫn tuyệt đối tới `npx`/`uvx` hoặc cài vào chỗ cố định. (Gốc: tài liệu gỡ lỗi + kinh nghiệm chung, cần xác minh trên máy thật.)
- Windows: bọc `cmd /c npx ...` cho server npx; `uvx` giữ nguyên.
- Server stdio không được ghi log ra stdout (làm hỏng giao thức); ghi ra stderr.
- Chạy server stdio trực tiếp ngoài terminal sẽ "treo" là bình thường: nó chờ client.
- Sửa cấu hình hoặc mã server: thoát hẳn rồi mở lại client (đóng cửa sổ chưa đủ với Claude Desktop).

## 8. Log và gỡ lỗi
- Claude Desktop: macOS `~/Library/Logs/Claude/mcp*.log`; Windows `%APPDATA%\Claude\logs`; Linux `~/.config/Claude/logs`. Theo dõi: `tail -n 20 -F ~/Library/Logs/Claude/mcp*.log`.
- Claude Code: `claude --debug-file /tmp/claude-debug.log`, tìm chuỗi liên quan tên server.
- Server HTTP không có stderr phía client: xem tab Network của DevTools hoặc `curl`.
- Chế độ DevTools của Claude Desktop: tạo `developer_settings.json` với `{"allowDevTools": true}` rồi Cmd+Option+I (cần xác minh trên bản hiện hành).

## 9. Mẹo vận hành cho TISA BOT
- Ưu tiên server từ xa có OAuth (không phải giữ khóa trên máy khách). Chỉ dùng stdio khi không có lựa chọn khác.
- Đặt tên server ngắn, không trùng tên dành riêng. Mỗi server đặt đúng phạm vi (user nếu dùng ở mọi dự án).
- Mọi server ghi dữ liệu (đăng bài, chạy quảng cáo, gửi tin, thanh toán): bật chế độ hỏi duyệt từng lần gọi tool. Nhớ nguyên tắc: nội dung đọc từ email/web/tài liệu có thể chứa lệnh giả (prompt injection); README của workspace-mcp và Google, Stripe đều cảnh báo.
- Cài server lạ = chạy mã lạ trên máy. Chỉ cài từ nguồn chính hãng hoặc repo có nhiều sao, đọc README, ghim phiên bản (`google-ads-mcp==0.0.6`). Chưa kiểm chứng an toàn của từng repo cộng đồng trong đợt này.
