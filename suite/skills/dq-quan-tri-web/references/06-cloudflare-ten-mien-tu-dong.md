# 06 - Cloudflare: đưa web lên và gắn tên miền tự động (bổ sung cho sổ tay 70)

Ngày: 19/11/2026. Nguồn: developers.cloudflare.com, đã đọc trực tiếp (hoặc qua công cụ `docs`/`search` của Cloudflare API MCP, tra đặc tả OpenAPI):
- workers/configuration/routing/custom-domains/ ; .../routes/ ; .../workers-dev/
- workers/static-assets/ ; .../headers/ ; .../redirects/ ; .../direct-upload/ ; .../billing-and-limitations/ ; .../migration-guides/migrate-from-pages/
- workers/wrangler/commands/general/ ; .../commands/workers/ ; .../configuration/ ; d1/wrangler-commands/
- workers/configuration/versions-and-deployments/rollbacks/ ; workers/platform/limits/ ; workers/platform/claim-deployments/
- workers/authorization/ và .../authorization/workers/ ; workers/observability/errors/
- fundamentals/api/reference/permissions/ ; .../reference/template/ ; fundamentals/api/get-started/create-token/
- fundamentals/manage-domains/add-site/ ; dns/zone-setups/full-setup/setup/ ; dns/cname-flattening/
- ssl/edge-certificates/universal-ssl/ ; ssl/troubleshooting/version-cipher-mismatch/ ; ssl/edge-certificates/additional-options/total-tls/error-messages/
- support/troubleshooting/http-status-codes/ (1xxx và 5xx: 1000, 1014, 1016, 522, 523, 525, 526)
- rules/url-forwarding/ ; .../examples/redirect-www-to-root/ ; .../single-redirects/create-api/ ; cache/how-to/purge-cache/ ; cache/how-to/cache-rules/
- registrar/get-started/register-domain/ ; registrar/top-level-domains/ ; cloudflare.com/tld-policies/
- web-analytics/ ; turnstile/plans/ ; turnstile/get-started/server-side-validation/ ; email-routing/ ; images/pricing/
- github.com/cloudflare/mcp ; developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/
- blog.cloudflare.com/cloudflare-cf-cli-launch ; github.com/cloudflare/workers-sdk/issues/9045
- Thực nghiệm trên máy này (19/11/2026): `npx wrangler@latest` = 4.165.0; chạy `login --scopes-list`, `deploy --help`, `rollback --help`, `versions --help`. Không đăng nhập, không gọi API tài khoản nào.
- Đặc tả OpenAPI qua `search` của Cloudflare API MCP (tên nhóm quyền "x-api-token-group", mô tả endpoint).

Quy ước: `<TOKEN>`, `<ACCOUNT_ID>`, `<ZONE_ID>`, `<DOMAIN_ID>`, `<VERSION_ID>` là chỗ giữ chỗ. "Cần xác minh" = không thấy trong tài liệu hoặc chưa chạy thật.

---
## 0. Tóm tắt nhanh và chỗ sửa sổ tay 70

Đường nhanh nhất cho web tĩnh có tên miền riêng: (1) hỏi chủ 5 câu (mục 1) -> (2) đăng nhập Cloudflare (người) -> (3) `npx wrangler deploy` lên `workers.dev` kiểm tra trước -> (4) nếu tên miền chưa ở Cloudflare: tạo zone, người đổi nameserver, chờ `active` -> (5) thêm Custom Domain (wrangler `routes` hoặc API) -> (6) kiểm tra bằng `curl -I`.

Sửa/bổ sung so với sổ tay 70:
- Đã xác minh `wrangler deploy` có `--assets <thư mục>`, `--name`, `--domain`, `--route` (chạy `--help` bản 4.165.0). Không cần `wrangler.jsonc` cho web tĩnh đơn giản (chưa chạy thật cả cụm `--assets ... --domain ...` cùng lúc).
- Có mẫu token "Edit Cloudflare Workers" thật (mục 3). Sổ tay 70 ghi chưa xác minh.
- Quyền gắn Custom Domain: tài liệu nói cần Editor trên Worker + Zone > Workers Routes > Edit cho từng zone; đặc tả API lại chỉ ghi "Workers Scripts Write". Cứ cấp cả hai.
- Tạo Worker MỚI cần vai trò Admin cấp sản phẩm Workers (tài liệu Authorization); cập nhật Worker có sẵn chỉ cần Editor. Đây có thể là nguồn gốc nhiều lỗi "không đủ quyền" khi tạo mới (cần xác minh với lỗi 10013, mục 5).
- Wrangler OAuth (`wrangler login`) KHÔNG có quyền DNS/Zone Edit (mục 3).
- Rollback: `wrangler rollback [VERSION_ID]`, tối đa 100 phiên bản gần nhất (sổ tay 70 chỉ nhắc `versions`).
- Có `wrangler deploy --temporary` (4.102.0+) để agent deploy tạm không cần tài khoản; claim trong 60 phút. KHÔNG phù hợp cho web thật của chủ. Bản 4.165.0 chạy `--help` không thấy cờ này: cần xác minh.
- Cloudflare mới ra CLI `cf` (open beta 28/09/2026, `npm i -g cf`); bài ra mắt không nói thay `wrangler deploy` (vẫn giao việc deploy cho Wrangler). Giữ Wrangler.

---
## 1. Kịch bản hỏi chủ (làm trước mọi lệnh)

Hỏi từng câu, ngắn, tiếng đời thường:
1. "Anh/chị đã có tên miền (kiểu ten-ban.com) chưa? Mua ở đâu (Mắt Bão, PA Việt Nam, GoDaddy, Namecheap, Cloudflare...)?" Chưa có -> mục 2c (mua).
2. "Tên miền đó đang chạy web hay email nào chưa?" CÓ -> DỪNG, không đổi nameserver/DNS, hỏi tiếp cách chuyển (mục 7).
3. "Đã có tài khoản Cloudflare chưa (email nào)? Có bật xác thực 2 lớp chưa?" Chưa -> người tự đăng ký (gói Free đủ).
4. "Muốn địa chỉ dạng nào: ten-mien.com, www.ten-mien.com, hay shop.ten-mien.com? Có cần cả hai ten-mien.com và www không?" Mặc định gợi ý: tên gốc làm chính, www chuyển hướng về gốc (hoặc gắn cả hai).
5. "Web chỉ có chữ/ảnh (tĩnh) hay có form nhận đơn, thanh toán, lưu dữ liệu?" -> tĩnh: mục 2b; có API/D1: mục 2b.2.

Ai làm gì:
| Việc | Người thật | AI tự làm |
|---|---|---|
| Mua tên miền, thanh toán | BẮT BUỘC (API Create Registration tính tiền, không hoàn lại; AI không gọi) | Tìm/kiểm tra tên còn trống (domain-check, chỉ đọc) |
| Đăng ký/đăng nhập Cloudflare, 2FA | BẮT BUỘC | Không |
| `wrangler login` bấm "Cho phép"; OAuth MCP | BẮT BUỘC | In link (`--browser=false`) |
| Tạo API token, dán vào kho khóa | Người bấm tạo/dán (không dán chat) | Hướng dẫn quyền (mục 3) |
| Đổi nameserver ở nhà đăng ký | BẮT BUỘC (đăng nhập/OTP/email xác nhận; tắt DNSSEC trước nếu đang bật) | Lấy 2 nameserver, kiểm tra active |
| Tạo zone, bản ghi DNS, Custom Domain, redirect | Chủ duyệt trước | Tự làm bằng API/wrangler |
| Deploy, cập nhật, rollback | Duyệt lần đầu | Tự làm |
| Xóa Worker/zone/bản ghi | Chủ gật đầu rõ từng việc | Làm sau khi sao lưu |
| Nâng gói trả phí | BẮT BUỘC | Không |

---
## 2. Quy trình tự động từ A đến Z

### 2a. Kiểm tra đăng nhập đúng tài khoản
```bash
npx wrangler whoami --json                      # lỗi thoát khác 0 nếu chưa đăng nhập (tài liệu general commands)
npx wrangler whoami --account <ACCOUNT_ID>      # xem thành viên của một tài khoản
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" -H "Authorization: Bearer <TOKEN>"
curl -s "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/tokens/verify" -H "Authorization: Bearer <TOKEN>"   # token tài khoản
curl -s "https://api.cloudflare.com/client/v4/accounts" -H "Authorization: Bearer <TOKEN>"   # liệt kê tài khoản để chọn ACCOUNT_ID
```
- Có nhiều tài khoản: đặt `account_id` trong `wrangler.jsonc` hoặc `CLOUDFLARE_ACCOUNT_ID`. Thứ tự ưu tiên: `CLOUDFLARE_API_TOKEN` > key+email > OAuth (sổ tay 70): `whoami` ra sai nơi thì xóa biến cũ.
- Wrangler 4.165.0 có `--profile` (nhiều hồ sơ đăng nhập). Xác minh `whoami` hiển thị quyền token: cần xác minh trên màn hình thật.
- Cloudflare MCP: gọi `whoami` (trả `{id,email}` hoặc `{id,name}`).

### 2b. Deploy
**Web tĩnh (Workers Static Assets)**
```bash
npx wrangler deploy --assets ./public --name ten-trang --compatibility-date 2026-11-01   # cờ có trong --help 4.165.0
```
hoặc `wrangler.jsonc`:
```jsonc
{ "name": "ten-trang", "compatibility_date": "2026-11-01",
  "assets": { "directory": "./public", "not_found_handling": "404-page" } }
```
- `not_found_handling`: `404-page` | `single-page-application` | `none` (mặc định). `html_handling` mặc định `auto-trailing-slash`.
- Thêm `.assetsignore` để không đẩy `node_modules`, `.git` (hướng dẫn migrate). Giới hạn 20.000 file, mỗi file 25 MiB.
- Chạy thử không đẩy: `npx wrangler deploy --dry-run`. Kết quả: `https://ten-trang.<subdomain>.workers.dev`. Lần đầu có thể 523 một phút rồi tự hết (tài liệu get-started). Lần đầu chưa có subdomain workers.dev, Wrangler bản mới hỏi "register workers.dev subdomain?" (workers-sdk #9045).
- Tên Worker: tối đa 63 ký tự, chỉ chữ/số/gạch ngang, không bắt đầu/kết thúc bằng gạch (tài liệu workers.dev).
- Lưu ý: khi có `routes` trong cấu hình, `workers_dev` mặc định thành `false` (workers.dev tắt). Muốn giữ thì `"workers_dev": true`.
- Dùng MCP/API thuần để upload tài sản: phức tạp (3 bước: `POST .../workers/scripts/<tên>/assets-upload-session` -> `POST .../workers/assets/upload?base64=true` -> `PUT .../workers/scripts/<tên>`). `execute` của MCP chạy trong Worker cô lập nên không đọc được file trên máy (suy luận, cần xác minh). Kết luận: upload bằng Wrangler; MCP/API dùng cho zone, DNS, domain, kiểm tra.

**2b.2 Worker có API/D1**
```jsonc
{ "name": "ten-trang", "main": "src/index.js", "compatibility_date": "2026-11-01",
  "assets": { "directory": "./public", "binding": "ASSETS", "run_worker_first": ["/api/*"] },
  "d1_databases": [ { "binding": "DB" } ] }   // bỏ id: wrangler deploy tự tạo và ghi lại id (provisioning tự động)
```
```bash
npx wrangler d1 migrations create DB "khoi-tao"
npx wrangler d1 migrations apply DB --remote
npx wrangler d1 execute DB --remote --command "SELECT 1"
npx wrangler d1 export DB --remote --output backup.sql     # sao lưu trước khi sửa
npx wrangler secret put TEN_BI_MAT                         # nhập giá trị tại dấu nhắc
```
Cần thêm quyền Account > D1 > Edit (và KV/R2 nếu dùng). `run_worker_first` tối đa 100 mẫu; gói Free: yêu cầu khớp mẫu này luôn gọi Worker, vượt hạn mức trả 429.

### 2c. Tạo zone (thêm site), nameserver, kích hoạt
Trước hết kiểm tra hiện trạng (chỉ đọc):
```bash
dig NS ten-mien.com @1.1.1.1 +short ; dig A ten-mien.com +short ; dig MX ten-mien.com +short ; curl -sI https://ten-mien.com | head -5
```
- Đã trỏ về Cloudflare rồi (NS dạng `*.ns.cloudflare.com`): có sẵn zone, lấy `<ZONE_ID>`: `GET /client/v4/zones?name=ten-mien.com`.
- Đang chạy nơi khác: ĐỪNG đổi NS (mục 7). Sao lưu bản ghi cũ trước.

Tạo zone (đường API; đường dashboard: Domains > Onboard a domain):
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  --data '{"name":"ten-mien.com","account":{"id":"<ACCOUNT_ID>"},"type":"full"}'
```
Kết quả: `result.id` (= ZONE_ID), `result.name_servers` (2 nameserver), `result.status` = `pending`. Giá trị `status`: initializing | pending | active | moved (đặc tả).
Quét bản ghi cũ (tài liệu nói hữu ích khi chưa đổi nameserver; KHÔNG tự thêm vào zone, phải review):
`POST /zones/<ZONE_ID>/dns_records/scan/trigger` rồi `GET/POST /zones/<ZONE_ID>/dns_records/scan/review`. Tài liệu cảnh báo quét có thể sót (apex, www, MX/SPF/DKIM/DMARC): so với bản ghi thật ở nhà đăng ký cũ.

Người thật đổi nameserver tại nhà đăng ký: xóa NS cũ, nhập đúng 2 NS Cloudflare; tắt DNSSEC trước nếu đang bật, bật lại qua Cloudflare sau khi active. Chờ tới 24 giờ (tài liệu full-setup).
Kiểm tra active:
```bash
dig NS ten-mien.com @1.1.1.1 +short                                  # thấy NS Cloudflare
curl -s "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>" -H "Authorization: Bearer <TOKEN>"   # result.status
curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/activation_check" -H "Authorization: Bearer <TOKEN>"
```
`activation_check`: gọi lại tối đa 5 phút/lần (gói trả phí), 1 giờ/lần (zone Free) (đặc tả). Active khi dashboard hiện Active và có email xác nhận. Kẹt "Pending Nameserver Update" = nameserver chưa có hiệu lực ở bên cha, kiểm lại ở nhà đăng ký.

**Mua tại Cloudflare Registrar (khác biệt):** mọi tên miền dùng nameserver Cloudflare, không đổi sang DNS khác được khi còn ở Registrar; trang tài liệu viết Cloudflare hoàn tất phần thiết lập còn lại, không phải đổi nameserver. Tab "Domains" trong Worker (changelog 14/05/2026) cho mua tên mới và nối tự động vào Worker. Mua: người bấm "Complete purchase" (có thanh toán, tự gia hạn mặc định bật). API `POST /accounts/<ACCOUNT_ID>/registrar/registrations` là thao tác tính tiền, không hoàn lại: AI chỉ dùng `domain-check`/`domain-search` (chỉ đọc). Quyền token cho Registrar: đặc tả không ghi nhóm quyền, cần xác minh. `.vn`/`.com.vn`: không thấy trong trang chính sách TLD của Cloudflare (đã hỏi `cloudflare.com/tld-policies`), cần xác minh trên màn hình thật; với `.vn` giữ ở nhà đăng ký Việt Nam và đổi nameserver (hỏi nhà đăng ký có cho đổi NS không). Tên miền Unicode (IDN) không hỗ trợ.

### 2d. Gắn tên miền vào Worker (Custom Domains)
Điều kiện: zone `active` cùng tài khoản; hostname chưa có bản ghi CNAME. Cloudflare TỰ tạo bản ghi DNS (trỏ thẳng vào Worker) và cấp chứng chỉ; không cần tạo DNS tay.
Cách 1 - wrangler (`wrangler.jsonc`) rồi `npx wrangler deploy`:
```jsonc
"routes": [ { "pattern": "ten-mien.com", "custom_domain": true },
            { "pattern": "www.ten-mien.com", "custom_domain": true } ]
```
Một lệnh: `npx wrangler deploy --domain ten-mien.com --domain www.ten-mien.com` (cờ `--domain` thấy trong `--help` 4.165.0).
Cách 2 - API (Workers Domains):
```bash
curl -s -X PUT "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/workers/domains" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  --data '{"hostname":"www.ten-mien.com","service":"ten-trang","zone_id":"<ZONE_ID>"}'
curl -s "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/workers/domains" -H "Authorization: Bearer <TOKEN>"        # liệt kê, lấy <DOMAIN_ID>
```
Đặc tả: bắt buộc `hostname` và `service`; có `zone_id`, `zone_name`, `enabled`, `previews_enabled`, `cert_id` (chỉ đọc); `zone_id` có bắt buộc hay không: cần xác minh (cứ gửi cho chắc).
Cách 3 - dashboard: Workers & Pages > Worker > Domains (hoặc Settings > Domains & Routes) > Add > Custom Domain.
- Subdomain: pattern `shop.ten-mien.com`. Apex: pattern `ten-mien.com` (Cloudflare tự lo, không cần CNAME flattening). Không hỗ trợ wildcard; khớp đúng tên máy, mọi đường dẫn vào cùng Worker.
- Chứng chỉ: Cloudflare cấp Advanced Certificate mặc định cho hostname, kể cả subdomain nhiều cấp, không cần mua Advanced Certificate Manager. Thời gian cấp tài liệu không nêu: cần xác minh (thực tế thường vài phút). Universal SSL (zone mới active): 15 phút đến 24 giờ.
- www <-> gốc: Custom Domain khớp đúng tên nên hai tên khác nhau. Hoặc (i) gắn cả hai, hoặc (ii) redirect: tạo bản ghi proxied cho tên NGUỒN chuyển hướng (A `192.0.2.0` hoặc AAAA `100::`, địa chỉ giữ chỗ, không ai tới được) rồi quy tắc Single Redirect:
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/dns_records" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  --data '{"type":"A","name":"www","content":"192.0.2.0","proxied":true}'      # tên trường theo API DNS chuẩn: cần kiểm lại bằng search
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/rulesets" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  --data '{"name":"www ve goc","kind":"zone","phase":"http_request_dynamic_redirect","rules":[{"expression":"http.host eq \"www.ten-mien.com\"","action":"redirect","action_parameters":{"from_value":{"target_url":{"expression":"concat(\"https://ten-mien.com\", http.request.uri.path)"},"status_code":301,"preserve_query_string":true}}}]}'
```
(JSON rule dựa trên ví dụ trong tài liệu create-api; mẫu "www.*" của trang redirect-www-to-root dùng mẫu khớp `https://www.*` -> `https://${1}`, 301, giữ query. Nên dùng cách mẫu trên dashboard Rules > Templates cho chắc; JSON trên cần chạy thử.) Đã có entrypoint redirect thì dùng `PUT /zones/<ZONE_ID>/rulesets/<RULESET_ID>`. Quyền: Zone > Single Redirect > Edit. `_redirects` KHÔNG đổi tên máy (www -> gốc) được.
- Custom Domain trùng bản ghi có sẵn: xem mục 5.

### 2e. Kiểm tra sau khi gắn
```bash
dig +short ten-mien.com @1.1.1.1                       # phải ra IP Cloudflare (proxied)
curl -sI https://ten-mien.com | head -8                # HTTP/2 200, header server: cloudflare
curl -s -o /dev/null -w "%{http_code} ssl=%{ssl_verify_result}\n" https://ten-mien.com
curl -sI http://ten-mien.com | head -3                 # có chuyển sang https? (nếu chưa: bật Always Use HTTPS; endpoint chưa tra, cần xác minh)
echo | openssl s_client -connect ten-mien.com:443 -servername ten-mien.com 2>/dev/null | openssl x509 -noout -issuer -dates
curl -s "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/workers/domains" -H "Authorization: Bearer <TOKEN>"   # enabled:true
```
Rồi mở thật trên trình duyệt (ổ khóa), cả bản điện thoại, cả `www`. Chưa có chứng chỉ: chờ rồi thử lại (mục 5). Ghi kết quả vào `output/` kèm giờ.

### 2f. Cập nhật, xem bản cũ, quay lại
```bash
npx wrangler deploy --message "cap nhat gia thang 12"      # đẩy bản mới (ghi chú đi kèm version và deployment)
npx wrangler versions list                                 # 10 bản gần nhất (--json)
npx wrangler deployments list ; npx wrangler deployments status
npx wrangler rollback <VERSION_ID> --message "quay lai ban cu"   # không ghi ID: về bản trước bản mới nhất
```
Rollback tạo deployment mới chuyển 100% lưu lượng về bản chọn; chỉ về được 100 bản gần nhất; chặn nếu giữa hai bản có đổi lớp Durable Object hoặc bản cũ gắn tài nguyên (R2/KV/queue) đã xóa. Binding không bị đổi (dữ liệu D1 không tự lùi). Có thể chậm lan truyền: trang đã tải có thể còn hỏi tệp bản mới.
API: `GET /accounts/<ACCOUNT_ID>/workers/scripts/<tên>/versions` rồi
`POST /accounts/<ACCOUNT_ID>/workers/scripts/<tên>/deployments` thân `{"strategy":"percentage","versions":[{"version_id":"<VERSION_ID>","percentage":100}]}` (quyền Workers Scripts Write; thân đúng đặc tả, nhưng cần xác minh bằng chạy thử).
Cache cũ: dữ liệu tài sản nằm trong phiên bản Worker (mỗi version có bản kê tài sản riêng). Nếu vẫn thấy nội dung cũ: `POST /zones/<ZONE_ID>/purge_cache` thân `{"hosts":["ten-mien.com"]}` hoặc `{"files":["https://ten-mien.com/"]}` hoặc `{"purge_everything":true}` (quyền Cache Purge). Gói Free: xóa theo URL 800 URL/giây; theo host/tag/prefix/tất cả 5 lệnh/phút. Tài liệu static assets không nói cần purge sau mỗi deploy: cần xác minh. Triển khai dần (`wrangler versions deploy <id>@10% <id2>@90%`) với web tĩnh có thể lệch bản (version skew): web bán hàng bình thường nên deploy 100%.

### 2g. Gỡ/xóa an toàn
Trước khi xóa: sao lưu (`wrangler versions list`, `d1 export`, xuất DNS `GET /zones/<ZONE_ID>/dns_records/export`), báo chủ nêu rõ web nào sẽ ngừng.
- Gỡ tên miền khỏi Worker: `DELETE /accounts/<ACCOUNT_ID>/workers/domains/<DOMAIN_ID>`. Chứng chỉ KHÔNG tự xóa (xóa ở SSL/TLS > Edge Certificates). Bản ghi DNS do Custom Domain tạo có tự mất hay không: tài liệu không nêu, cần xác minh, kiểm bằng `GET .../dns_records?name=...`.
- Xóa Worker: `npx wrangler delete --name ten-trang` (không thấy `--force`; tài liệu chỉ có `--name --env --dry-run`) hoặc `DELETE /accounts/<ACCOUNT_ID>/workers/scripts/<tên>`. Xóa là mất bản chạy; dữ liệu D1 xóa riêng.
- Xóa zone (`DELETE /zones/<ZONE_ID>`, quyền Zone Write) = web, email, DNS của tên miền sẽ hỏng nếu còn dùng nameserver Cloudflare. Chỉ làm khi chủ đã đổi NS đi nơi khác hoặc bỏ tên miền.
- `wrangler logout`; xóa/Roll token (`PUT /user/tokens/<ID>/value` hoặc `/accounts/<ACCOUNT_ID>/tokens/<ID>/value`).

---
## 3. Quyền API token tối thiểu (tên nhóm như dashboard: "Edit"; trong đặc tả API là "Write")

| Việc | Nhóm quyền | Phạm vi |
|---|---|---|
| Deploy Worker có sẵn, versions, rollback, xem domain | Workers Scripts Edit (Read nếu chỉ xem) | Account |
| `wrangler` hoạt động trơn (mẫu "Edit Cloudflare Workers") | Workers Scripts Edit, Workers KV Storage Edit, Workers Tail Read, Workers R2 Storage Edit, Account Settings Read, User Details Read, User Memberships Read; Workers Routes Edit | Account/User; Zone (Routes) |
| Tạo Worker MỚI | vai trò Admin cấp Workers (tài liệu Authorization); token mẫu có đủ không: cần xác minh | Account |
| Gắn/gỡ Custom Domain hoặc Route | Workers Routes Edit (mỗi zone) + Workers Scripts Edit; nên thêm Zone Read | Zone + Account |
| Liệt kê/tạo zone | Zone Read / Zone Edit (tạo zone cần phạm vi "tất cả zone của tài khoản"; suy luận) | Zone |
| Tạo/xóa bản ghi DNS, xuất DNS | DNS Edit (xuất: DNS Read cũng được) | Zone |
| Kiểm tra activation | Zone Edit | Zone |
| Redirect www/gốc | Single Redirect Edit | Zone |
| Purge cache | Cache Purge | Zone |
| Chứng chỉ (xem/đặt lại) | SSL and Certificates Read/Edit | Zone |
| D1 / KV / R2 | D1 Edit / Workers KV Storage Edit / Workers R2 Storage Edit | Account |
| Email Routing | Email Routing Rules Edit (zone) + Email Routing Addresses Edit (account) | Zone, Account |
| Turnstile | Turnstile Edit | Account |
| Web Analytics (đọc số liệu) | Account Analytics Read | Account |
Chọn đúng tài khoản và đúng zone (không "All"); đặt hạn dùng; không bật lọc IP nếu dùng MCP (MCP chưa hỗ trợ). Tạo nhanh: mẫu `permissionGroupKeys` có link sẵn trong tài liệu "account-owned-token-template" (Workers scripts only; Workers full access = scripts + KV + routes).

**Cộng sự tự kiểm tra token đủ quyền** (chỉ đọc, an toàn):
1. `GET /user/tokens/verify` (hoặc `/accounts/<ID>/tokens/verify`) -> `status: active`, kiểm hạn dùng.
2. Mỗi quyền một lệnh GET: `GET /accounts/<ID>/workers/scripts` (Workers Scripts), `GET /zones?name=ten-mien.com` (Zone Read), `GET /zones/<ZONE_ID>/dns_records` (DNS Read), `GET /zones/<ZONE_ID>/workers/routes` (Routes), `GET /accounts/<ID>/workers/domains`.
3. Kết quả 200 = có; 403/"Authentication error" = thiếu. Cẩn thận: qua MCP một số GET (như `GET /zones`) trả danh sách RỖNG khi thiếu quyền; coi rỗng là thiếu quyền, đừng kết luận "chưa có zone".
4. Xem chi tiết token cần API Tokens Read (token deploy thường không có): đừng dựa vào đó.
Cộng sự báo chủ nhóm quyền thiếu bằng tên đúng ở bảng trên, không tự xin quyền rộng hơn.

**Cloudflare MCP chính thức:** `https://mcp.cloudflare.com/mcp` (repo cloudflare/mcp): công cụ `search` (tra đặc tả OpenAPI, có sẵn tên quyền từng endpoint), `execute` (chạy JavaScript gọi API qua `cloudflare.request()`, trong Worker cô lập), `docs`, `whoami`. Xác thực OAuth (chọn quyền lúc đồng ý; tên quyền OAuth trùng tên nhóm quyền token theo mô tả công cụ `search`) hoặc token Bearer (token người dùng và token tài khoản đều được; token tài khoản cần "Account Resources: Read" để tự tìm account id; token người dùng thì truyền `account_id`). Thiếu quyền: client chuẩn nhận 403 `insufficient_scope` kèm tên quyền thiếu để cấp lại. Giới hạn: kết quả mỗi lần ~6.000 token (chia nhỏ yêu cầu); token có lọc IP chưa hỗ trợ; không có công cụ "deploy tệp từ máy". Máy chủ khác: docs, container, Browser Run, DEX, CASB, Agents SDK docs; các máy chủ từng sản phẩm "tùy chọn", đa số dùng server API là đủ. Cũng có MCP riêng của Cloudflare với công cụ như `workers_list`, `d1_*`, `kv_*`, `r2_*`, `migrate_pages_to_workers_guide` (cần xác minh nguồn chính thức nếu tích hợp).

**OAuth qua `wrangler login` có thiếu quyền DNS không?** Có. Chạy `wrangler login --scopes-list` (4.165.0, 19/11/2026): có `workers:write`, `workers_scripts:write`, `workers_routes:write`, `workers_kv:write`, `d1:write`, `pages:write`, `zone:read`, `account:read`, `user:read`, `email_routing:write`, `challenge-widgets.write` (Turnstile), `ssl_certs:write` (mTLS), v.v.; KHÔNG có DNS Edit, Zone Edit, Cache Purge, Single Redirect, Registrar. Hệ quả: Wrangler OAuth deploy và có thể gắn Custom Domain cho zone đã active (Cloudflare tự tạo DNS) nhưng KHÔNG tạo zone, không sửa DNS, không purge, không tạo redirect: những việc này cần API token (hoặc MCP với OAuth chọn thêm quyền DNS/Zone). Gắn Custom Domain bằng OAuth thật sự chạy được không: cần xác minh trên màn hình thật.

---
## 4. Pages hay Workers cho web mới (2026)
- Trang Pages của tài liệu mở đầu bằng "Are you sure you want to use Pages? Start new projects with Workers." Hướng dẫn migrate nói Workers có tập tính năng rộng hơn; KHÔNG thấy tuyên bố Pages bị khai tử hay có hạn chót (một bài blog nói Pages "deprecated" tháng 4/2025: không phải nguồn chính thức, bỏ qua).
- Chỉ Workers có: gradual deployments, Cron Triggers, Workers Logs, Email Workers, Vite plugin, v.v. Cả hai có: rollback, preview URL, redirects/headers, D1/KV/R2.
- Chỉ Pages có: tên miền ngoài zone Cloudflare (CNAME về `pages.dev`, không cần đổi nameserver); Workers BẮT BUỘC nameserver Cloudflare.
- Khuyến nghị mặc định: **Workers Static Assets**. Ngoại lệ: chủ không đổi được nameserver (hoặc chưa cho đổi) và chỉ cần web tĩnh -> cân nhắc Pages với CNAME (đường phụ, cần xác minh trên màn hình thật). Dự án Pages cũ: giữ chạy, chuyển theo bài migrate khi cần (`wrangler pages deploy` -> `wrangler deploy`; thay `pages_build_output_dir` bằng `assets.directory`; cần Wrangler 4+).
- Trường hợp `.vn` nhà đăng ký không cho đổi NS: thử hỏi nhà đăng ký trước.

---
## 5. Lỗi hay gặp và cách gỡ
| Lỗi | Ý nghĩa/cách gỡ (nguồn) |
|---|---|
| API 10013 khi tạo Worker mới | KHÔNG có trong trang Errors chính thức. Báo cáo cộng đồng: mã "workers.api.error.unknown", thường lỗi tạm của API (có ca gắn với `/workers/scripts/<tên>/subdomain` trả 500). Làm theo thứ tự: (1) chờ 1-2 phút, chạy lại; (2) `npx wrangler@latest`; (3) kiểm tra Cloudflare Status; (4) đăng ký workers.dev subdomain bằng dashboard (Workers & Pages > Your subdomain); (5) thử OAuth (`wrangler login`) thay vì token, hoặc cấp vai trò Admin Workers (tạo Worker mới cần Admin); (6) tạo Worker rỗng trên dashboard rồi deploy đè. Cần xác minh nguyên nhân thật. |
| 10063 | Cần workers.dev subdomain: Wrangler mới tự hỏi đăng ký; hoặc đặt tay trên dashboard (workers-sdk #9045). |
| 10007 / 10015 / 10016 / 10021 / 10037 | Không thấy Worker/subdomain / tài khoản chưa được dùng Workers / tên Worker sai / lỗi lúc chạy mã khởi động (cú pháp, hết CPU/RAM) / quá số Worker tối đa. (trang observability/errors) |
| 1027 | Vượt 100.000 yêu cầu/ngày gói Free (reset 00:00 UTC). |
| 1101 / 1102 / 1042 | Mã Worker ném lỗi / quá CPU / Worker gọi Worker cùng zone không có cờ `global_fetch_strictly_public` (hoặc workers.dev bị tắt). |
| 1000 | Bản ghi A trỏ IP Cloudflare, vòng proxy kép, `CF-Connecting-IP` giả... Gỡ: trỏ lại đúng hoặc dùng Custom Domain. |
| 1014 | CNAME giữa hai tài khoản Cloudflare khác nhau: bị cấm. |
| 1016 | Cloudflare không phân giải được "nguồn": thiếu bản ghi A hoặc CNAME chết. |
| 522 | Hết thời gian nối nguồn. Với Worker: Worker trên Custom Domain tự `fetch()` về chính hostname của mình gây 522 (dùng Route/cờ `global_fetch_strictly_public`); hoặc bản ghi A cũ vẫn trỏ máy chủ cũ chết. |
| 523 | Không tới được nguồn. Lần deploy workers.dev đầu: chờ ~1 phút tự hết. |
| 525 / 526 | Bắt tay SSL/chứng chỉ ở NGUỒN lỗi (chế độ SSL Full/Strict). Web tĩnh Worker không có nguồn: nếu gặp, hostname đang trỏ vào máy chủ cũ, tức Custom Domain chưa thực sự gắn (suy luận): `GET .../workers/domains` kiểm tra, rà bản ghi A/CNAME cũ. |
| "SSL pending", `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` | Chứng chỉ chưa cấp: zone mới active chờ 15 phút-24 giờ; bản ghi phải bật mây cam (proxied); Universal chỉ phủ tên gốc + 1 cấp subdomain (`a.b.ten-mien.com` không phủ, trừ Custom Domain đã tự cấp Advanced cert hoặc có Total TLS). Quá 24 giờ: tạm "Pause Cloudflare" và liên hệ hỗ trợ. CAA ở DNS cũ có thể chặn (kiểm `dig CAA`). |
| "This hostname is not covered by a certificate" (cảnh báo ở DNS) | Zone còn pending: thường bỏ qua, tự hết sau khi active. Zone đã active: tên đa cấp chưa phủ -> Total TLS / Advanced / Custom hoặc bỏ cấp thừa. |
| Tên miền đang trỏ nơi khác | Zone chưa active thì Custom Domain không dùng được; trước khi đổi xem mục 7. |
| Không tạo được Custom Domain | Hostname đã có bản ghi CNAME (xóa CNAME sau khi sao lưu), hoặc zone không thuộc tài khoản, hoặc zone chưa active. Hướng dẫn chuyển từ Vercel nói Custom Domain "thay" bản ghi DNS cũ của hostname: không khớp với cảnh báo CNAME: cần xác minh; cách an toàn: sao lưu rồi xóa bản ghi cũ. |
| Bản ghi xung đột | CNAME không được cùng tên với A/AAAA/CNAME khác; NS con (mã 81056) chặn A/AAAA cùng tên: xóa NS trước (có thể gây gián đoạn). Hostname dùng Route cần bản ghi proxied (A `192.0.2.0`/AAAA `100::`), không có bản ghi sẽ ERR_NAME_NOT_RESOLVED. |
| CNAME flattening ở apex | Với Custom Domain không cần: Cloudflare tự tạo bản ghi. Chỉ cần khi chủ muốn CNAME ở tên gốc trỏ nơi khác: flatten tự bật "ở một số trường hợp"; CNAME cụt cho NODATA; xác minh dịch vụ ngoài bằng CNAME có thể hỏng khi flatten tất cả. |
| Nội dung cũ | Mục 2f (purge). Xóa cache trình duyệt/Ctrl+F5. |
| `_headers` | Đặt trong thư mục tài sản, tối đa 100 quy tắc, mỗi dòng ≤2.000 ký tự, CHỈ áp lên phản hồi tài sản tĩnh (không áp lên phản hồi do Worker sinh ra). |
| `_redirects` | Trong thư mục tài sản; `nguồn đích [mã]` mã mặc định 302 (301/302/303/307/308); tối đa 2.000 tĩnh + 100 động; không đổi tên máy (www<->gốc), không áp cho phản hồi của Worker; redirect thắng headers. Trên 2.100: dùng Bulk Redirects. |
| 404 sau deploy | Sai `assets.directory`, thiếu `index.html`, quên `not_found_handling`. |

Giới hạn gói Free (https://developers.cloudflare.com/workers/platform/limits/): 100.000 yêu cầu/ngày vào Worker; 10 ms CPU/yêu cầu; 100 Worker/tài khoản; 20.000 file tài sản/phiên bản, mỗi file 25 MiB; 100 Custom Domain/zone; 1.000 Route/zone; 50 subrequest/lần chạy; Worker ≤64 MiB. Trang billing-and-limitations: "yêu cầu tới tài sản tĩnh miễn phí và không giới hạn", chỉ yêu cầu gọi mã Worker mới tính hạn mức. Single Redirects 10 quy tắc/zone (không regex); Bulk Redirects 15 quy tắc, 10.000 URL (rules/url-forwarding); Cache Rules 10 quy tắc (cache/how-to/cache-rules).

---
## 6. Tính năng miễn phí có ích cho web bán hàng (ngắn)
- **Web Analytics**: "available on all plans", tự thêm đoạn đo cho hostname đi qua Cloudflare (mặc định bật), hoặc dán snippet thủ công; không chèn được nếu trang có `Cache-Control: public, no-transform`. Tài liệu gọi là "privacy-first"; việc "không cookie" tài liệu đã đọc không ghi rõ: cần xác minh trước khi hứa với chủ.
- **Turnstile** (thay CAPTCHA cho form nhận đơn): miễn phí, 20 widget/tài khoản, 10 hostname/widget, không giới hạn lượt. Phải kiểm ở máy chủ: `POST https://challenges.cloudflare.com/turnstile/v0/siteverify` với `secret` + `response`; token sống 300 giây, dùng một lần. Khóa bí mật để ở Worker (secret), không đưa vào HTML.
- **Email Routing**: có trên Workers Free; chuyển thư `lienhe@ten-mien.com` về hộp thư hiện có; chỉ NHẬN, không gửi. Cảnh báo: cần MX của Cloudflare, xung đột với MX cũ (Google Workspace, Zoho...): đừng bật khi chủ đang dùng email tên miền.
- **Cache Rules** (10 quy tắc, cần bản ghi proxied): chỉnh thời gian lưu cache. Web tĩnh Workers đã được cache toàn cầu; chưa rõ Cache Rules áp lên tài sản Workers: cần xác minh.
- **Ảnh**: Free có 5.000 biến đổi duy nhất/tháng nhưng chỉ cho ảnh lưu NGOÀI Cloudflare Images (vd R2). Không áp cho tài sản tĩnh Worker. Việc thực tế: nén ảnh (WebP, chiều rộng hợp lý) trước khi đẩy lên; Polish/Mirage: tài liệu giá chưa nói, cần xác minh.

---
## 7. Rủi ro và quy tắc cứng cho cộng sự
1. **Không đổi nameserver/DNS của tên miền đang chạy web hoặc email khác khi chưa hỏi chủ.** Đổi NS = toàn bộ DNS (web, email, xác minh dịch vụ) chuyển sang zone Cloudflare; bản quét tự động có thể sót bản ghi.
2. **Luôn sao lưu bản ghi DNS cũ trước khi sửa** và lưu vào `output/` (thư mục YYYY-MM-DD-...): với tên miền chưa vào Cloudflare dùng `dig` các loại A, AAAA, CNAME, MX, TXT, NS, CAA + ảnh chụp màn hình DNS ở nhà đăng ký + `dns_records/scan`; với zone đã có dùng `GET /zones/<ZONE_ID>/dns_records/export` (BIND). Hạ TTL cũ trước khi chuyển nếu được (hướng dẫn migrate của Cloudflare).
3. Thử trước trên `workers.dev`, chỉ gắn tên miền khi chủ xem và đồng ý; đổi NS vào giờ ít khách; giữ web cũ chạy tới khi mới OK.
4. Trước khi sửa bản ghi tên gốc/www: ghi lại bản ghi MX/SPF/DKIM/DMARC và giữ nguyên.
5. Token: không dán vào chat, không ghi vào wiki/output; dùng `CLOUDFLARE_API_TOKEN` trong kho khóa; quyền tối thiểu, hạn dùng, đúng zone.
6. Không tự mua tên miền, không tự nâng gói, không gọi API Registrar tạo đăng ký; không xóa zone/Worker khi chưa có chữ "đồng ý" của chủ cho đúng việc đó.
7. Tên miền đã mua ở Cloudflare Registrar: không chuyển DNS ra ngoài được; báo chủ.

---
## 8. Chỗ còn cần xác minh trên màn hình thật
- Lỗi 10013 nguyên nhân chính thức; Admin Workers có bắt buộc khi token mẫu "Edit Cloudflare Workers" tạo Worker mới.
- `wrangler login` OAuth có gắn được Custom Domain (cần DNS do Cloudflare tự tạo) cho zone active không; `wrangler deploy --assets ... --domain ...` chạy trọn một lệnh; cờ `--temporary` trên bản hiện tại.
- Thân `PUT /workers/domains` (zone_id bắt buộc?), thân `POST /zones/<ZONE_ID>/dns_records` và JSON redirect (đã dựa tài liệu, chưa chạy thật).
- Thời gian cấp chứng chỉ Custom Domain; DNS do Custom Domain tạo có tự xóa khi gỡ không; Custom Domain "thay" bản ghi cũ hay bị CNAME chặn.
- Cần purge sau deploy không; Cache Rules áp lên tài sản Workers không.
- `.vn` ở Cloudflare Registrar; quyền token cho Registrar; Web Analytics "không cookie" và cách bật cho Worker.
- Nhóm quyền "Zone Edit" có đủ tạo zone mới (cần phạm vi tất cả zone) trong dashboard.
