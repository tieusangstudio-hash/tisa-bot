# 70 - Sổ tay Cloudflare: token, Wrangler, Workers/Pages, D1/KV/R2, tên miền riêng, MCP

Ngày: 19/11/2026. Nguồn chính: developers.cloudflare.com (đọc trực tiếp các trang dẫn bên dưới), https://github.com/cloudflare/mcp-server-cloudflare, https://github.com/cloudflare/mcp.

## 1. Chọn đường
| Việc | Cách | Độ khó |
|---|---|---|
| Hỏi/ra lệnh Cloudflare qua chat | Cloudflare MCP chính chủ + OAuth | Dễ |
| Đưa web tĩnh/HTML lên mạng | `wrangler deploy` (Workers Static Assets) | Vừa |
| Đăng nhập Wrangler | `wrangler login` (OAuth trình duyệt) hoặc API token | Vừa |
| Gắn tên miền riêng | Custom Domain trên Worker + zone ở Cloudflare | Khó/Vừa (đổi nameserver là việc người thật ở nhà đăng ký) |
Pages hay Workers: có trang "Migrate your Pages project to Workers with static assets" nên hướng chính hiện nay là Workers + Static Assets cho web mới; trang đã đọc không nói Pages bị khai tử hay có hạn chót -> cần xác minh trên màn hình thật. Mặc định dùng Workers Static Assets.

## 2. Cloudflare MCP chính chủ
https://github.com/cloudflare/mcp-server-cloudflare (~4,5k sao).
- Server khuyến nghị: **Cloudflare API MCP** `https://mcp.cloudflare.com/mcp` (repo `cloudflare/mcp`). Công cụ: `search` (tìm endpoint trong đặc tả API), `execute` (chạy JavaScript gọi API Cloudflare), `docs`, `whoami`.
- Máy chủ khác: tài liệu `https://docs.mcp.cloudflare.com/mcp`, container, Browser Run, DEX, CASB, Blog... Các server cũ (Workers Bindings `bindings.mcp.cloudflare.com`, Observability...) đã **lỗi thời**, chuyển sang server API.
- Thêm vào client: mọi client hỗ trợ MCP từ xa nối thẳng URL. JSON: `"cloudflare-api": {"type": "http", "url": "https://mcp.cloudflare.com/mcp"}`. Claude Code: `claude mcp add --transport http cloudflare-api https://mcp.cloudflare.com/mcp` rồi `/mcp` (suy ra từ cách chung; README không có lệnh này).
- Xác thực: **OAuth (khuyến nghị)**: chuyển sang Cloudflare, chọn quyền lúc đồng ý. Hoặc **API token** làm Bearer cho CI/tự động.
- Thiếu quyền: server yêu cầu cấp lại quyền; một số endpoint trả danh sách rỗng khi thiếu scope, server coi rỗng là từ chối. Token tài khoản cần "Account Resources: Read" để tự biết account id. Token có **lọc IP** hiện chưa được hỗ trợ.
- Giới hạn: mỗi kết quả `search/execute` tối đa ~6.000 token; tắt chế độ code (`?codemode=false`) làm tốn ~244k token ngữ cảnh. Chuỗi gọi dài có thể gây "response interrupted" (hết ngữ cảnh): chia nhỏ yêu cầu.
- Một số tính năng cần gói Workers trả phí.
- `whoami` trả `user:<id>` hoặc `account:<id>`.

## 3. Tạo API token đúng quyền tối thiểu
https://developers.cloudflare.com/fundamentals/api/get-started/create-token/
1. Dashboard > **My Profile > API Tokens** (token người dùng) hoặc **Manage Account > API Tokens** (token tài khoản) > **Create Token**, đặt tên rõ (vd `tisa-bot-deploy-web`).
2. Chọn mẫu hoặc "Custom". Mẫu "Edit Cloudflare Workers" có trong dashboard từ kinh nghiệm chung nhưng trang tài liệu đọc không nhắc: cần xác minh trên màn hình thật. Với mẫu tự tạo, quyền thường cần cho deploy web tĩnh: Account > Workers Scripts: Edit; nếu gắn tên miền: Zone > Workers Routes: Edit và Zone > DNS: Edit cho đúng zone; D1/KV/R2 thì thêm đúng nhóm quyền tương ứng (D1: Edit, Workers KV Storage: Edit, Workers R2 Storage: Edit). (Tên nhóm quyền từ kinh nghiệm chung, cần xác minh.)
3. Giới hạn tài nguyên: chọn đúng **tài khoản** và đúng **zone**, đừng chọn "All". Có thể đặt hạn dùng (TTL) và lọc IP (nhưng IP filter làm MCP không dùng được).
4. Create Token -> chép **một lần duy nhất** (tiền tố `cfut_`); chủ tự dán vào kho khóa/biến môi trường, không dán vào chat.
5. Kiểm tra token: `curl "https://api.cloudflare.com/client/v4/user/tokens/verify" --header "Authorization: Bearer <TOKEN>"` -> `status: active`. (Token tài khoản có thể dùng endpoint verify của tài khoản: cần xác minh.)
6. Thu hồi/xoay: xoá hoặc "Roll" trong trang API Tokens (tài liệu trang này không mô tả; cần xác minh).
Lấy **Account ID**: dashboard > Workers & Pages (cột phải) hoặc trang tổng quan tài khoản.

## 4. Wrangler
Nguồn: https://developers.cloudflare.com/workers/wrangler/commands/general/ ; .../system-environment-variables/.
- Dùng `npx wrangler <lệnh>` (không cần cài toàn cục). Cần Node mới.
- `wrangler login`: OAuth trình duyệt (người thật bấm Cho phép). `--browser=false` in link thay vì tự mở. `--scopes-list` xem các scope. Thông tin lưu mặc định ở `~/.config/.wrangler/config/default.toml` (văn bản thường); `wrangler login --use-keyring` mã hoá và lưu khóa vào Keychain.
- `wrangler whoami` (thêm `--json`) kiểm tra đã đăng nhập đúng tài khoản. Nhiều tài khoản: cần xác định đúng account.
- `wrangler logout` xoá OAuth; nếu dùng `CLOUDFLARE_API_TOKEN` thì xoá token ở dashboard.
- Biến môi trường: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` (tài khoản dùng cho lệnh Workers). Thứ tự ưu tiên khi lấy thông tin xác thực: `CLOUDFLARE_API_TOKEN` > `CLOUDFLARE_API_KEY`+`CLOUDFLARE_EMAIL` > token OAuth. => Nếu `whoami` ra sai tài khoản, kiểm tra các biến này trước.
- Nhật ký lỗi: `WRANGLER_LOG=debug`, `WRANGLER_LOG_PATH=...`.
- Lệnh cơ bản: `wrangler dev` (chạy thử), `wrangler deploy` (đưa lên), `wrangler versions`. Lệnh bí mật `wrangler secret put TEN` (nhập giá trị tại dấu nhắc, không để trong lịch sử lệnh). Lệnh `tail` xem log thật. Chi tiết trang con "Workers commands": cần xác minh bằng `wrangler --help` bản đang cài.

## 5. Đưa web tĩnh/HTML lên mạng (Workers Static Assets)
Nguồn: https://developers.cloudflare.com/workers/static-assets/
1. Thư mục dự án có `index.html` (và ảnh, css, js) trong, ví dụ, `./public`.
2. Tạo `wrangler.jsonc`:
   ```jsonc
   { "name": "ten-trang-cua-ban", "compatibility_date": "2026-11-01",
     "assets": { "directory": "./public", "not_found_handling": "404-page" } }
   ```
   - `not_found_handling`: `"single-page-application"` trả `index.html` (200) cho đường dẫn không khớp (dùng cho SPA); `"404-page"` trả 404 và `404.html` gần nhất. Không có Worker script thì không khớp = 404.
   - Có API chung: thêm `main` và đặt `run_worker_first` cho `/api/*`.
3. Đăng nhập (mục 4) rồi `npx wrangler deploy`. Kết quả: địa chỉ `https://ten-trang-cua-ban.<subdomain>.workers.dev`.
4. Mở địa chỉ và kiểm tra trang hiển thị. Cập nhật = sửa file rồi chạy lại `npx wrangler deploy`.
5. Cách một dòng không cần cấu hình (`wrangler deploy --assets ./public --name ten`) có ở bản Wrangler gần đây theo kinh nghiệm chung, nhưng tài liệu đã đọc không nêu: cần xác minh.
6. Scaffolding: `npm create cloudflare@latest` (có mẫu React).
Giới hạn gói Free (https://developers.cloudflare.com/workers/platform/limits/): 100.000 yêu cầu/ngày (reset 00:00 UTC; vượt thì lỗi **1027**, có thể cấu hình fail open/closed); 10 ms CPU mỗi yêu cầu HTTP; **Static Assets: 20.000 file mỗi phiên bản Worker, mỗi file tối đa 25 MiB**; 100 Worker/tài khoản. Hạn mức KV/D1/R2: xem trang giới hạn riêng của từng sản phẩm (cần xác minh).

## 6. D1, KV, R2 (lệnh chuẩn, cần đối chiếu `--help`)
- D1: `npx wrangler d1 create TEN`, `npx wrangler d1 execute TEN --remote --command "SELECT 1"` hoặc `--file schema.sql`. Khai binding trong `wrangler.jsonc` (`d1_databases`).
- KV: `npx wrangler kv namespace create TEN` rồi khai binding `kv_namespaces`.
- R2: `npx wrangler r2 bucket create TEN`, binding `r2_buckets`.
- Nhớ cờ `--remote` khi muốn tác động dữ liệu thật; mặc định có thể là bản cục bộ.
- Ghi chú: chưa đọc trang riêng từng lệnh trong đợt này; đối chiếu với bản Wrangler cài trên máy.

## 7. Gắn tên miền riêng và DNS
Nguồn: https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- Điều kiện: tên miền đã là một **zone Cloudflare** (đã đổi nameserver về Cloudflare). Đổi nameserver tại nhà đăng ký tên miền, có thể phải đăng nhập/OTP/xác nhận email: **việc người thật**; có thể mất vài giờ.
- Cách dashboard: Workers & Pages > chọn Worker > **Settings > Domains & Routes > Add > Custom Domain** > nhập tên (vd `www.ten-mien.com` hoặc `ten-mien.com`) > Add.
- Cách mã: trong `wrangler.jsonc` thêm `"routes": [{"pattern": "www.ten-mien.com", "custom_domain": true}]` rồi deploy.
- Cloudflare tự tạo bản ghi DNS và cấp chứng chỉ HTTPS. **Không tạo được Custom Domain trên hostname đã có CNAME** (xoá CNAME cũ trước); không hỗ trợ wildcard. `www` và gốc là hai hostname riêng: muốn dùng cả hai, thêm cả hai hoặc đặt chuyển hướng.
- Kiểm tra: `dig ten-mien.com +short` hoặc mở trình duyệt, ổ khóa HTTPS; có thể mất vài phút để chứng chỉ sẵn sàng.

## 8. Lỗi hay gặp
- **Hết quota**: lỗi 1027 (vượt 100k yêu cầu/ngày ở gói Free) -> chờ 00:00 UTC hoặc nâng gói; kiểm tra có vòng lặp gọi.
- **Nhầm account id**: `wrangler whoami` ra tài khoản khác; nhiều tài khoản -> đặt `CLOUDFLARE_ACCOUNT_ID` đúng; hoặc `account_id` trong `wrangler.jsonc`. Xem lại biến môi trường cũ đang ghi đè OAuth.
- **Token thiếu quyền**: lỗi dạng "Authentication error" hoặc mã 10000 (kinh nghiệm chung) khi deploy/gắn route/ghi DNS -> thêm đúng nhóm quyền ở mục 3, và chọn đúng zone/tài khoản. Với MCP, thiếu quyền có thể trả rỗng.
- **Token có lọc IP** không dùng được với MCP.
- **Domain không gắn được**: đang có CNAME cùng tên; zone chưa active (nameserver chưa đổi); ở sai tài khoản.
- **`/sse` trả 410 Gone** -> dùng `/mcp`.
- **Phiên bản Wrangler cũ**: lệnh/cờ khác -> `npx wrangler@latest` rồi chạy lại.
- **Trang 404 sau deploy**: sai `assets.directory`, thiếu `index.html` ở gốc thư mục, hoặc cần `single-page-application`.
- **Tệp quá lớn/nhiều**: >25 MiB mỗi file hoặc >20.000 file.

## 9. Kiểm tra nối thật và thu hồi
- Nối thật: `npx wrangler whoami`; `curl .../user/tokens/verify`; mở URL `workers.dev` sau deploy; với MCP gọi `whoami`.
- Thu hồi: `wrangler logout`; xoá/Roll API token; thu hồi OAuth của MCP trong dashboard (mục ứng dụng được ủy quyền: cần xác minh); xoá Worker (`wrangler delete` hoặc dashboard) và bản ghi DNS.
- Việc chỉ người thật làm: đăng nhập Cloudflare (và 2FA), bấm Cho phép OAuth, đổi nameserver tại nhà đăng ký, thanh toán nâng gói, tạo và dán token.
