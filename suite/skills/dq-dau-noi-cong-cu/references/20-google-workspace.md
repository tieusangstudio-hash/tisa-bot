# 20 - Sổ tay đấu nối Google Workspace (Gmail, Lịch, Drive, Sheets, Docs, Tasks)

Ngày: 19/11/2026. Giao diện Google Cloud đổi liên tục: mọi tên menu dưới đây ghi "cần xác minh trên màn hình thật".

## Chọn đường nối
| Đường | Độ khó | Ghi chú |
|---|---|---|
| A. `workspace-mcp` của taylorwilsdon (cộng đồng, chạy trên máy) | Khó (phải tự tạo OAuth client) | Đủ dịch vụ nhất, có chế độ chỉ đọc. https://github.com/taylorwilsdon/google_workspace_mcp |
| B. Server Google chính chủ, mỗi sản phẩm một endpoint (đang preview) | Khó | Cần vào Developer Preview Program. https://developers.google.com/workspace/guides/configure-mcp-servers |
| C. Connector Google có sẵn trong Claude (nếu gói có) | Dễ (bấm Cho phép) | Nên thử trước; chưa kiểm trong đợt này. |

## Chuẩn bị chung (A và B)
1. Một tài khoản Google (Gmail hoặc Workspace) đăng nhập đúng trong trình duyệt. Người dùng nhiều tài khoản: kiểm tra avatar góc phải, hoặc dùng cửa sổ ẩn danh/profile riêng.
2. Một dự án Google Cloud (console.cloud.google.com). Tạo dự án mới có tên rõ ràng (vd `tisa-bot-google`), kiểm tra tên dự án đang chọn ở thanh trên cùng: lỗi hay gặp nhất là bật API ở dự án này nhưng tạo khóa ở dự án khác.
3. Chuẩn bị 15-40 phút. Người thật phải làm: đăng nhập, 2FA/OTP, bấm đồng ý điều khoản Google Cloud, tick "tôi đồng ý" chính sách dữ liệu, có thể phải thêm thẻ thanh toán để mở một số dịch vụ (Gmail/Drive/Calendar API thường không tính phí, chưa xác minh).

## Bước trên web (cách A)
Nguồn: https://developers.google.com/workspace/guides/configure-oauth-consent và /create-credentials.
1. Bật API: vào Menu > APIs & Services > Library, bật Gmail API, Google Calendar API, Google Drive API, Google Sheets API, Google Docs API, Tasks API (chỉ bật cái cần). Cách nhanh bằng dòng lệnh: `gcloud services enable gmail.googleapis.com ...`.
2. Màn hình đồng ý OAuth: Menu > Google Auth platform > Branding. Nếu thấy "chưa cấu hình" bấm Get Started; nhập tên ứng dụng, email hỗ trợ; Audience chọn **External** (Gmail cá nhân) hoặc **Internal** (chỉ khi cả tổ chức Workspace của chính bạn); email liên hệ; tick đồng ý chính sách dữ liệu; Create.
3. Audience > Test users > Add users: thêm CHÍNH email sẽ đăng nhập (và mọi người dùng thử). Tối đa 100 người dùng thử.
4. Data Access > Add or Remove Scopes: thêm scope cần dùng (xem bảng dưới), Save.
5. Clients > Create Client > Application type: **Desktop app** (nếu server chạy trên máy với redirect localhost) hoặc **Web application** (nếu dùng redirect `http://localhost:PORT/oauth2callback` hoặc URL máy chủ). Đặt tên; Create; chép Client ID và Client Secret (giữ bí mật; không dán lên chat, không ghi vào wiki).
   - Tuỳ chọn "Use this client for an AI-powered agent": không bắt buộc với workspace-mcp (README nói không cần); bắt buộc với server Google chính chủ (cách B). Không sửa được sau khi tạo.
6. Chạy server: `uvx workspace-mcp --tool-tier core` (hoặc `--tools gmail drive calendar`, thêm `--read-only` để chỉ đọc). Cần Python 3.11+ và `uv`.
   - Đặt biến: `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` (hoặc `GOOGLE_CLIENT_SECRET_PATH` trỏ file client_secret.json). Với OAuth 2.1/HTTP: `MCP_ENABLE_OAUTH21=true`, `WORKSPACE_MCP_PORT=8000`, `GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8000/oauth2callback` (khớp từng ký tự với URI đã khai ở Clients).
   - Nối vào Claude Code: `claude mcp add --transport http workspace-mcp http://localhost:8000/mcp` (khi chạy `--transport streamable-http`). Dạng stdio là mặc định cho client cũ.
7. Lần gọi tool đầu tiên sẽ mở trình duyệt xin đăng nhập Google -> người thật bấm chọn tài khoản -> màn hình "Google chưa xác minh ứng dụng này" -> bấm **Nâng cao/Advanced** -> **Đi tới <tên ứng dụng> (không an toàn)** -> tick các quyền -> Continue. Đây là bình thường với ứng dụng Testing của chính chủ.

## Bảng scope tối thiểu (theo tài liệu server chính chủ)
- Gmail: `gmail.readonly` (đọc), `gmail.compose` (soạn nháp), `gmail.modify` (nhãn, lưu trữ). Server chính chủ: có tạo nháp, không thấy công cụ gửi.
- Drive: `drive.readonly` hoặc `drive.file` (chỉ file app tạo/được cấp). Docs/Sheets/Slides: thêm scope documents/spreadsheets/presentations.
- Calendar: `calendar.events.readonly`, `calendar.events` (ghi), `calendar.events.freebusy`.
- Tasks: scope `tasks` / `tasks.readonly` (cần xác minh, trang tổng hợp chưa liệt kê).
Nguyên tắc: bắt đầu bằng scope chỉ đọc, chỉ nâng lên ghi khi chủ duyệt. Scope "nhạy cảm/hạn chế" (Gmail, Drive đầy đủ) dẫn tới yêu cầu xác minh nếu mở cho nhiều người ngoài.

## Đường B (server chính chủ) - tóm tắt
- Vào Google Workspace Developer Preview Program trước.
- Bật API sản phẩm và dịch vụ MCP: `gmailmcp`, `drivemcp`, `docsmcp`, `sheetsmcp`, `slidesmcp`, `calendarmcp`, `chatmcp`, `classroommcp`, `workspacemcp` (+ `people.googleapis.com`).
- OAuth client loại Web, tick "AI-powered agent", redirect Claude: `https://claude.ai/api/mcp/auth_callback`. Thêm connector tuỳ chỉnh trong Claude (gói Pro/Max/Team/Enterprise), nhập Client ID/Secret ở phần nâng cao. Hướng dẫn Claude Code của Google: chưa thấy (cần xác minh).
- Xin quyền offline (`access_type=offline`, `prompt=consent`) kẻo phải đăng nhập lại mỗi giờ (token tĩnh chỉ sống 1 giờ).
- Service account có domain-wide delegation và client mặc định của Apps Script không dùng được cờ agent.

## Lỗi hay gặp và cách xử
- **"Ứng dụng chưa được xác minh" / access_blocked**: (1) email chưa nằm trong Test users -> thêm; (2) quản trị Workspace chặn ứng dụng bên thứ ba (Admin Console > Security > API controls) -> nhờ quản trị cho phép; (3) ứng dụng đã in production nhưng chưa xác minh, giới hạn 100 người mới (https://support.google.com/cloud/answer/7454865).
- **Token hết hạn sau 7 ngày**: dự án External ở trạng thái **Testing** thì refresh token chỉ sống 7 ngày (trừ khi chỉ xin scope name/email/profile). Cách xử: (a) chấp nhận đăng nhập lại mỗi tuần; (b) chuyển "Publish app" sang In production (vẫn hiện cảnh báo chưa xác minh nhưng token không còn hạn 7 ngày; chưa kiểm trong đợt này, cần xác minh); (c) tài khoản Workspace dùng Internal. Nguồn: https://developers.google.com/identity/protocols/oauth2
- **invalid_grant**: refresh token hết hạn/bị thu hồi, đổi mật khẩu (khi có scope Gmail), không dùng 6 tháng, hoặc quá 100 token/ client/ tài khoản (cái cũ nhất bị vô hiệu). Cách xử: xoá thông tin xác thực đã lưu và đăng nhập lại.
- **redirect_uri_mismatch (Error 400)**: URI trong yêu cầu phải KHỚP TỪNG KÝ TỰ với "Authorized redirect URIs" (không phải JavaScript origins). Kiểm tra cổng, `http` vs `https`, `127.0.0.1` vs `localhost`, dấu `/` cuối. Desktop app dùng loopback `http://127.0.0.1:cổng`; kiểu copy-dán mã (OOB) đã bị khai tử. (https://developers.google.com/identity/protocols/oauth2/native-app). Có báo cáo lỗi này khi nối Google MCP qua claude.ai (xem issue anthropics/claude-code, cần tra bản mới).
- **403 API chưa bật** ("has not been used in project... or it is disabled"): bật API đúng dự án chứa OAuth client, đợi vài phút.
- **access_denied**: người dùng bấm Từ chối hoặc chưa tick đủ quyền; app nên kiểm tra trường `scope` trả về.
- Thiếu quyền ghi: scope chỉ đọc đã cấp -> thêm scope, thu hồi quyền cũ rồi cấp lại.

## Kiểm tra đã nối thật (nên là lệnh CHỈ ĐỌC)
- Trong TISA BOT: gọi tool kiểu "liệt kê 3 email mới nhất (chỉ tiêu đề)" hoặc "liệt kê lịch hôm nay", "liệt kê 5 file Drive gần đây". Kết quả phải có dữ liệu thật của đúng tài khoản; nếu rỗng, kiểm tra tài khoản đã đăng nhập.
- Độc lập: Inspector `tools/list` (xem `10-mcp-chung.md`). Chuẩn bị tài khoản test trước khi chạm vào hộp thư thật.

## Thu hồi / xoá
- Phía Google: myaccount.google.com > Bảo mật > Ứng dụng của bên thứ ba có quyền truy cập tài khoản > chọn app > Xoá quyền truy cập (cần xác minh tên mục trên màn hình thật).
- Phía máy: xoá thư mục lưu credentials của server (workspace-mcp lưu trên đĩa/bộ nhớ theo cấu hình), `claude mcp remove workspace-mcp`.
- Phía Cloud: xoá OAuth client ở Google Auth platform > Clients; xoá dự án nếu không dùng.

## An toàn
- Email, tài liệu, sự kiện có thể chứa chỉ dẫn giả (prompt injection): README workspace-mcp và Google đều cảnh báo; không bật cùng lúc Gmail + Drive + Chat với quyền ghi nếu không cần.
- File lưu local của workspace-mcp chặn `.env*`, `~/.ssh/`, `~/.aws/`.
- Ghi chú: Google Ads dùng OAuth riêng, xem `35-mcp-ads.md`.
