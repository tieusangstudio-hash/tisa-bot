# 03 - Web CRM và hệ thống thu lead chạy trên Cloudflare

Ngày: 19/11/2026.
Nguồn đã đọc (WebFetch/WebSearch):
- Cloudflare: https://developers.cloudflare.com/d1/platform/limits/ , /d1/platform/pricing/ , /workers/platform/limits/ , /d1/reference/migrations/ , /d1/reference/time-travel/ , /d1/best-practices/import-export-data/ , /d1/worker-api/d1-database/ , /workers/configuration/secrets/ , /workers/configuration/cron-triggers/ , /workers/runtime-apis/bindings/rate-limit/ , /workers/runtime-apis/web-crypto/ , /workers/runtime-apis/request/ , /workers/static-assets/billing-and-limitations/ , /turnstile/get-started/server-side-validation/ , /turnstile/plans/ , /cloudflare-one/policies/access/ , /cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/ , .../authorization-cookie/validating-json/ , /cloudflare-one/account-limits/ (tất cả dưới developers.cloudflare.com)
- GitHub: honojs/hono, cloudflare/templates, cloudflare/templates/saas-admin-template, h1n054ur/hookforms-cloud, Sigmakib2/cf-workers-contact-form-api, biomathcode/sass-waitlist-cloudflare, ifindev/fullstack-next-cloudflare, choyiny/saasmail, twentyhq/twenty (+ LICENSE), espocrm/espocrm, frappe/crm, convobrains/zero-cost-crm
- Hono: https://hono.dev/docs/middleware/builtin/jwt , https://hono.dev/docs/getting-started/cloudflare-workers
- Telegram: https://core.telegram.org/bots/faq , https://core.telegram.org/bots/api (chỉ đọc được phần đầu)
- Google Sheets: https://developers.google.com/workspace/sheets/api/guides/values
- Pháp lý (thứ cấp): https://luatvietnam.vn/linh-vuc-khac/du-lieu-ca-nhan-duoc-bao-ve-nhu-the-nao-tu-01-7-2023-883-93965-article.html ; https://vanban.chinhphu.vn/?pageid=27160&docid=207759 (chỉ có thông tin hành chính) ; kết quả tìm kiếm về Luật BVDLCN 2025 và NĐ 356/2025 (luatvietnam.vn, lsvn.vn, luatvietan.vn)
- Zalo: chỉ có tài liệu bên thứ ba (SDK), chưa đọc được developers.zalo.me.

Quy ước: "cần xác minh" = chưa đọc được nguồn gốc, đừng đưa cho học viên như sự thật. Số sao GitHub là số tại thời điểm đọc hôm nay và thay đổi liên tục.

---

## 1. Tóm tắt cho cộng sự "Quản Trị WEB"

- Hệ thống tối thiểu cho shop nhỏ chỉ cần: trang lead (tĩnh) -> 1 Worker (Hono) -> D1 -> trang admin -> thông báo Telegram/Zalo. Không cần CRM mã nguồn mở nặng.
- Các CRM tự host lớn (Twenty, EspoCRM, Frappe CRM) cần Postgres/MySQL + Docker/PHP/Python, KHÔNG chạy trên Workers. Quá nặng cho chủ shop không biết kỹ thuật.
- Mặc định bảo vệ admin bằng Cloudflare Access (không phải tự viết đăng nhập). Nếu tự viết thì băm mật khẩu, cookie HttpOnly, không bao giờ có mật khẩu mặc định.
- Gói miễn phí đủ cho shop nhỏ (xem mục 5), nhưng phải kiểm tra lại số liệu trên trang Cloudflare mỗi khi báo giá cho học viên.
- Với TISA BOT: cách đơn giản nhất là cloud là nơi nhận lead 24/7, máy TISA BOT KÉO (pull) lead mới về định kỳ qua API có token. Không mở cổng vào máy của chủ.

---

## 2. Danh sách repo và công cụ đã xem (14 mục)

| # | Tên và URL | Sao / giấy phép (đọc 19/11/2026) | Chạy trên Cloudflare? | Nên dùng cho việc gì |
|---|---|---|---|---|
| 1 | Hono - github.com/honojs/hono | ~33,0k sao; MIT | Có (Workers được hỗ trợ chính thức; bản `hono/tiny` dưới 12kB theo README) | Khung API cho Worker. Nên dùng. |
| 2 | Cloudflare Templates - github.com/cloudflare/templates | ~2,2k sao; MIT | Có (của Cloudflare). Có các mẫu `d1-template`, `d1-starter-sessions-api-template`, `openauth-template`, `saas-admin-template`, `react-router-hono-fullstack-template` | Lấy cấu trúc wrangler + D1 chuẩn để bắt đầu. |
| 3 | saas-admin-template (trong cloudflare/templates) | Cùng kho, MIT | Có (Astro + Workers + D1) | CHỈ THAM KHẢO. README ghi "không còn được bảo trì". Admin đăng nhập bằng user `admin` + token, nên đổi cách xác thực. |
| 4 | hookforms-cloud - github.com/h1n054ur/hookforms-cloud | 8 sao; MIT | Có (Hono + D1 + KV + Queues; nút Deploy to Cloudflare) | Mẫu gần nhất "form -> Worker -> D1 -> thông báo": gửi Discord/Slack/Teams/Telegram/ntfy/email, Turnstile tùy chọn, KV rate limit. Quá ít người dùng, chỉ đọc lấy ý tưởng, không giao nguyên cho học viên. |
| 5 | cf-workers-contact-form-api - github.com/Sigmakib2/cf-workers-contact-form-api | 10 sao; README không thấy giấy phép (coi là chưa cấp phép) | Có (Hono + Workers) | Mẫu rất nhỏ: honeypot + CORS + webhook Discord. Chỉ tham khảo, README chỉ gợi ý D1 chứ không có bước cài. |
| 6 | sass-waitlist-cloudflare - github.com/biomathcode/sass-waitlist-cloudflare | 0 sao; README không nêu giấy phép | Có (Astro + Hono + D1 qua Drizzle + Resend) | Mẫu luồng đăng ký + xác nhận email + chống trùng. Chỉ tham khảo. |
| 7 | fullstack-next-cloudflare - github.com/ifindev/fullstack-next-cloudflare | ~1,4k sao; MIT | Có (Next.js 15 + D1 + R2 + Drizzle + Better Auth) | Nền để dựng app đầy đủ có đăng nhập. README không nói về CRM (một kết quả tìm kiếm có nhắc PR thêm CRM, chưa đọc: cần xác minh). Nặng hơn Hono thuần. |
| 8 | saasmail - github.com/choyiny/saasmail | ~280 sao; Apache-2.0 | Có (Workers + D1 + R2 + Queues + Email Routing) | Hộp thư + timeline khách hàng. Không phải CRM lead, nhưng là mẫu tốt cho đăng nhập passkey và API key. README ước tính ~5 USD/tháng gói Workers Paid. |
| 9 | Frostbase - github.com/frostbase-dev/frostbase | 243 sao; Apache-2.0 (theo bài tổng hợp bitdoze.com, nguồn thứ cấp, cần xác minh) | Có (theo bài tổng hợp) | Backend-as-a-service để tự dựng bảng. Chưa đọc README gốc. |
| 10 | Twenty - github.com/twentyhq/twenty | ~61,2k sao; chủ yếu AGPL-3.0, file có tiêu đề Enterprise thuộc giấy phép thương mại riêng, một số gói MIT (theo file LICENSE) | KHÔNG (README nêu PostgreSQL, Redis, BullMQ/NestJS, chạy bằng Docker Compose) | CRM đầy đủ tự host trên VPS. Quá nặng cho shop nhỏ. |
| 11 | EspoCRM - github.com/espocrm/espocrm | ~3,6k sao; AGPLv3 | KHÔNG (PHP 8.3-8.5 + MySQL 8/MariaDB 10.6/PostgreSQL 15; cài tay, script, Docker) | CRM đủ chức năng lead/cơ hội/chiến dịch, hợp nếu chủ chịu thuê VPS/hosting PHP. |
| 12 | Frappe CRM - github.com/frappe/crm | ~4,0k sao; AGPL-3.0 | KHÔNG (Frappe/Python, cài bằng script hoặc Docker) | CRM bán hàng có kanban. Nặng, cần máy chủ. |
| 13 | zero-cost-crm - github.com/convobrains/zero-cost-crm | 15 sao; MIT | KHÔNG (React + Express 5 + PostgreSQL; Vercel hoặc Docker/VPS) | Chỉ để tham khảo danh sách tính năng pipeline/import CSV. |
| 14 | Cloudflare Turnstile và Cloudflare Access (dịch vụ, không phải repo) | Turnstile gói Free: 20 widget, thử thách không giới hạn, tối đa 10 hostname/widget | Có | Turnstile chống spam form; Access khóa trang admin (mục 4). |

Ghi chú không dùng được:
- "alcogy/cork" (một kết quả tìm kiếm nói là nền tảng nghiệp vụ SvelteKit + D1): WebFetch trả 404, không xác minh được, không đưa vào danh sách.
- PulsegateEdge (pulsegate-docs.pages.dev): không thấy giấy phép mã nguồn mở, bỏ qua.
- Zalo OA: xem mục 6, chưa có tài liệu chính thức.

Kết luận chọn lựa:
- Tự dựng (Hono + D1) là lựa chọn nhẹ nhất. Mẫu #2, #4, #5 dùng để tham khảo cấu trúc, tự viết phần còn lại.
- Chỉ chạm tới Twenty/EspoCRM/Frappe khi chủ thật sự cần CRM đầy đủ (nhiều nhân viên, báo giá, hợp đồng) và chấp nhận thuê máy chủ. Cả ba đều giấy phép AGPL: nếu sửa mã và cho người khác dùng qua mạng thì phải công khai mã đã sửa (cần xác minh với người hiểu giấy phép trước khi đóng gói bán).

---

## 3. Sơ đồ hệ thống tối thiểu

```
Khách điền form (trang tĩnh Workers Static Assets, hoặc trang của TISA BOT)
   + Turnstile widget + ô ẩn honeypot + UTM từ URL
        |
        v  POST /api/lead  (JSON)
  [Worker Hono]  -- rate limit -> honeypot -> Turnstile siteverify -> kiểm dữ liệu
        |                                   \
        |  ghi D1 (leads + lead_events)      \-- ctx.waitUntil -> Telegram sendMessage (và sau này Zalo/Sheets)
        v
     [D1 SQLite]
        ^
        |  GET/PATCH /admin/api/*   (sau Cloudflare Access hoặc đăng nhập tự viết)
  [Trang admin CRM: bảng khách, lọc theo trạng thái, ghi chú, xuất CSV]
        ^
        |  GET /api/sync/leads?since=...  (token máy-với-máy)
  [TISA BOT trên máy chủ: kéo lead mới về CRM trên máy]
```

Trang tĩnh phục vụ qua Workers Static Assets: Cloudflare ghi "yêu cầu tới static assets là miễn phí và không giới hạn" (đọc 19/11/2026), chỉ yêu cầu chạy Worker mới tính vào hạn mức.

---

## 4. Thiết kế chi tiết

### 4.1 Schema D1 (migration `migrations/0001_init.sql`)

```sql
CREATE TABLE leads (
  id TEXT PRIMARY KEY,                       -- uuid, cũng dùng làm khóa đồng bộ
  name TEXT NOT NULL,
  phone TEXT NOT NULL UNIQUE,                -- đã chuẩn hóa 0xxxxxxxxx
  email TEXT,
  note TEXT,                                 -- khách ghi trên form
  status TEXT NOT NULL DEFAULT 'moi'
    CHECK (status IN ('moi','da_lien_he','quan_tam','hen_gap','thanh_cong','that_bai','spam')),
  source TEXT,                               -- ten landing page / kênh
  utm_source TEXT, utm_medium TEXT, utm_campaign TEXT, utm_content TEXT, utm_term TEXT,
  referrer TEXT,
  consent_at TEXT NOT NULL,                  -- thời điểm khách tick đồng ý
  consent_text_version TEXT NOT NULL,        -- phiên bản câu đồng ý đã hiển thị
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  deleted_at TEXT                            -- xóa mềm; xóa thật theo yêu cầu khách
);
CREATE INDEX idx_leads_status_created ON leads(status, created_at DESC);
CREATE INDEX idx_leads_updated ON leads(updated_at);

CREATE TABLE lead_events (                   -- lịch sử: form, đổi trạng thái, ghi chú, đồng bộ
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id TEXT NOT NULL REFERENCES leads(id),
  kind TEXT NOT NULL,                        -- form_submit | status | note | sync_in | sync_out
  detail TEXT,
  actor TEXT,                                -- email admin hoặc 'system'
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_events_lead ON lead_events(lead_id, created_at);
```

Nếu tự viết đăng nhập, thêm `admin_users(id, email UNIQUE, pw_hash, pw_salt, created_at)` và `sessions(token_hash PRIMARY KEY, user_id, expires_at)`. Nếu dùng Cloudflare Access thì không cần hai bảng này.
Lưu ý: dùng múi giờ UTC trong D1, hiển thị đổi sang giờ Việt Nam ở trang admin.

Migration (theo tài liệu D1): file `.sql` đánh số trong thư mục `migrations/`, theo dõi bằng bảng `d1_migrations`. Lệnh: `npx wrangler d1 migrations create <tên_db> <mô_tả>`, `npx wrangler d1 migrations list <tên_db> --remote`, `npx wrangler d1 migrations apply <tên_db> --remote` (`--local` khi thử trên máy; tài liệu migrations tôi đọc không ghi cờ này, cần xác minh trong trang tham chiếu lệnh Wrangler D1). Gọi theo TÊN database, không theo tên binding.

### 4.2 Worker mẫu (Hono, tự viết, ~55 dòng, chưa chạy thử trong phiên này)

```ts
import { Hono } from 'hono'
import { cors } from 'hono/cors'

type Env = { Bindings: { DB: D1Database; RL: RateLimit; TURNSTILE_SECRET: string;
  TG_TOKEN: string; TG_CHAT: string; ALLOWED_ORIGIN: string } }
const app = new Hono<Env>()
app.use('/api/lead', (c, next) => cors({ origin: c.env.ALLOWED_ORIGIN, allowMethods: ['POST'] })(c, next))

const normPhone = (s: string) => {
  const d = (s || '').replace(/\D/g, '')
  const p = d.startsWith('84') ? '0' + d.slice(2) : d
  return /^0\d{9}$/.test(p) ? p : null
}

app.post('/api/lead', async (c) => {
  const ip = c.req.header('CF-Connecting-IP') ?? 'anon'
  if (!(await c.env.RL.limit({ key: ip })).success) return c.json({ ok: false }, 429)
  const b = (await c.req.json().catch(() => null)) as Record<string, string> | null
  if (!b) return c.json({ ok: false }, 400)
  if (b.website) return c.json({ ok: true })            // honeypot: bot điền ô ẩn -> giả vờ thành công
  const v = (await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({ secret: c.env.TURNSTILE_SECRET, response: b.turnstile ?? '', remoteip: ip }),
  }).then((r) => r.json())) as { success: boolean }
  if (!v.success) return c.json({ ok: false, error: 'captcha' }, 400)
  const phone = normPhone(b.phone); const name = (b.name ?? '').trim().slice(0, 100)
  if (!phone || !name || b.consent !== '1') return c.json({ ok: false, error: 'invalid' }, 400)
  const id = crypto.randomUUID()
  await c.env.DB.batch([
    c.env.DB.prepare(
      `INSERT INTO leads (id,name,phone,note,source,utm_source,utm_medium,utm_campaign,consent_at,consent_text_version)
       VALUES (?,?,?,?,?,?,?,?,datetime('now'),?)
       ON CONFLICT(phone) DO UPDATE SET updated_at=datetime('now')`)
      .bind(id, name, phone, (b.note ?? '').slice(0, 500), b.source ?? null,
            b.utm_source ?? null, b.utm_medium ?? null, b.utm_campaign ?? null, b.consent_v ?? 'v1'),
    c.env.DB.prepare(`INSERT INTO lead_events (lead_id,kind,detail,actor)
       SELECT id,'form_submit',?,'system' FROM leads WHERE phone=?`).bind(b.source ?? '', phone),
  ])
  c.executionCtx.waitUntil(fetch(`https://api.telegram.org/bot${c.env.TG_TOKEN}/sendMessage`, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ chat_id: c.env.TG_CHAT, text: `Lead mới: ${name} - ${phone} (${b.source ?? '?'})` }),
  }))
  return c.json({ ok: true })
})
export default app
```

`wrangler.jsonc` cần: binding `DB` (d1_databases), `ratelimits` (xem 4.3), biến thường `ALLOWED_ORIGIN`. Ba khóa còn lại là secret (mục 4.7). Luôn dùng `?` + `.bind()` cho mọi tham số, không ghép chuỗi SQL. Gửi Telegram dạng văn bản thường (không `parse_mode`) để tên khách không phá định dạng.

### 4.3 Chống spam (nhiều lớp)
1. Turnstile: widget ở trang, Worker BẮT BUỘC gọi `POST https://challenges.cloudflare.com/turnstile/v0/siteverify` (secret + token + tùy chọn remoteip). Token sống 300 giây, dùng một lần, tối đa 2048 ký tự. Gói Free: 20 widget, challenge không giới hạn, 10 hostname/widget, không gỡ được logo Cloudflare (theo trang plans, đọc 19/11/2026). Có khóa thử riêng (sitekey/secret kiểm thử) để chạy local; khóa thật từ chối token giả.
2. Honeypot: ô `website` ẩn bằng CSS, người thật không điền. Nếu có giá trị thì trả `ok:true` nhưng không ghi.
3. Rate limit: binding `ratelimits` (cần Wrangler 4.36.0 trở lên), `period` chỉ nhận 10 hoặc 60 giây. Ví dụ `{"name":"RL","namespace_id":"1001","simple":{"limit":5,"period":60}}`. Lưu ý chính tài liệu: giới hạn tính theo từng địa điểm Cloudflare, gần đúng, và khuyên tránh khóa theo IP vì nhiều người dùng chung IP; với form công khai chưa có định danh khác nên vẫn dùng IP như một lớp phụ, đừng coi là chặn tuyệt đối.
4. Khác: giới hạn độ dài trường, kiểm số điện thoại Việt Nam (10 số, đầu 0), CORS chỉ cho đúng tên miền trang lead, `UNIQUE(phone)` chống trùng.
5. Đọc IP từ header `CF-Connecting-IP`: tài liệu Request tôi đọc không nhắc header này, cần xác minh.

### 4.4 Xác thực admin
Lựa chọn đơn giản nhất cho chủ shop: Cloudflare Access trước đường dẫn `/admin*`.
- Cách làm (tài liệu): Zero Trust > Access controls > Applications > Self-hosted > thêm hostname công khai > gắn chính sách Allow (ví dụ đúng email của chủ). Mọi ứng dụng Access mặc định từ chối, cần chính sách Allow. Tạo Access trước khi mở đường ra ngoài.
- Cảnh báo cấu hình sai (tài liệu): chính sách "mọi người + One-time PIN" cho bất kỳ email hợp lệ nào vào được. Chỉ cho đúng email của chủ.
- Worker PHẢI tự kiểm tra token, không tin mặc định: đọc header `Cf-Access-Jwt-Assertion`, lấy khóa tại `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs`, kiểm chữ ký RS256 và `iss`, `aud` (AUD tag của ứng dụng), `exp`, `nbf`. Ví dụ chính thức dùng thư viện `jose`. Tài liệu còn nhắc `ctx.access` cho Worker, cần xem giới hạn trước khi dùng.
- Số người dùng tối đa của Zero Trust gói Free: trang tôi đọc không ghi con số, cần xác minh trước khi hứa với học viên.

Nếu phải tự viết đăng nhập (không Access):
- Băm mật khẩu bằng PBKDF2 (Web Crypto của Workers có hỗ trợ `deriveBits`), kèm salt ngẫu nhiên mỗi người; so sánh bằng `crypto.subtle.timingSafeEqual` (tiện ích riêng của Workers). Giới hạn số vòng lặp PBKDF2 trên Workers: cần xác minh bằng cách chạy thử.
- Mật khẩu admin đầu tiên do chủ tự đặt khi cài, hoặc sinh ngẫu nhiên dài và chỉ hiện một lần. KHÔNG có mật khẩu mặc định trong mã, trong README, trong mẫu cho học viên.
- Phiên: sinh token ngẫu nhiên 32 byte, lưu BĂM của token trong bảng `sessions`, gửi cookie `HttpOnly; Secure; SameSite=Strict` (hoặc `Lax`), hạn ngắn (vài giờ đến vài ngày), có đăng xuất. Hono có sẵn middleware JWT (bắt buộc khai báo `alg`, có tùy chọn đọc từ cookie) nếu muốn dùng JWT thay phiên trong D1.
- Giới hạn đăng nhập sai (rate limit theo email), thêm Turnstile ở trang đăng nhập, bắt buộc HTTPS.
- Mẫu cloudflare/saas-admin-template dùng user `admin` cố định + token làm mật khẩu: đừng bắt chước.

API máy-với-máy (cho TISA BOT): `Authorization: Bearer <token dài ngẫu nhiên>`, token lưu bằng secret, so sánh bằng `timingSafeEqual`, tách riêng với đăng nhập admin, thay được bằng `wrangler secret put`.

### 4.5 Bảo vệ dữ liệu cá nhân (nêu ngắn, phải xác minh với người hiểu luật)
- Cập nhật quan trọng: các nguồn tìm được hôm nay (luatvietnam.vn, lsvn.vn, luatvietan.vn; đều là bài phân tích, chưa đọc văn bản gốc) nói Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 (thông qua 26/6/2025) có hiệu lực từ 01/01/2026, và Nghị định 356/2025/NĐ-CP hướng dẫn, thay thế Nghị định 13/2023/NĐ-CP. Cần xác minh trên Công báo/cơ sở dữ liệu pháp luật chính thống trước khi trích số hiệu hay điều khoản cho học viên.
- Các ý nền (theo bài tóm tắt NĐ 13/2023, nguồn thứ cấp; luật mới có thể đổi chi tiết, cần xác minh): sự đồng ý phải rõ ràng, cụ thể, có thể bằng đánh dấu ô đồng ý; im lặng không phải đồng ý; chủ thể có quyền rút lại đồng ý và yêu cầu hạn chế/phản đối xử lý (nguồn ghi mốc 72 giờ để thực hiện, cần xác minh).
- Về "số điện thoại là dữ liệu nhạy cảm": bài tóm tắt NĐ 13 liệt kê nhóm nhạy cảm gồm quan điểm chính trị/tôn giáo, sức khỏe, di truyền, đời sống tình dục, dữ liệu tội phạm, thông tin khách hàng tổ chức tín dụng, dữ liệu vị trí; số điện thoại không nằm trong danh sách ví dụ đó. Dù vậy vẫn là dữ liệu cá nhân cần bảo vệ, và Nghị định 356 được nói là mở rộng danh mục nhạy cảm (cần xác minh). Cứ xử lý số điện thoại như dữ liệu cần giữ kín.
- Việc nên làm trong thiết kế: (1) ô tick đồng ý KHÔNG chọn sẵn, kèm đường dẫn chính sách quyền riêng tư nói rõ thu gì, dùng để làm gì, ai xem; (2) lưu `consent_at` và `consent_text_version`; (3) chỉ thu trường thật cần; (4) có cách xóa/chỉnh theo yêu cầu khách (xóa mềm rồi xóa thật); (5) không đưa số điện thoại vào URL, log, hay tin nhắn gửi nhóm đông người; (6) hạn chế quyền xem, bật Access; (7) không để dữ liệu thật trong kho mã/mẫu cài đặt.
- Hồ sơ đánh giá tác động và nghĩa vụ thông báo: nguồn thứ cấp nhắc thời hạn 60 ngày gửi hồ sơ cho cơ quan chuyên trách, cần xác minh có áp dụng cho shop nhỏ không. Gợi ý chủ hỏi luật sư hoặc cơ quan có thẩm quyền.

### 4.6 Sao lưu và xuất dữ liệu
- Time Travel của D1 luôn bật, không thêm phí: khôi phục theo phút trong 7 ngày (gói Free) hoặc 30 ngày (gói Paid). Lệnh `npx wrangler d1 time-travel restore <db> --timestamp=<unix>` ghi đè tại chỗ; kết quả trả bookmark để hoàn tác.
- Sao lưu chủ động: `npx wrangler d1 export <db> --remote --output=backup.sql` (có `--table`, `--no-data`, `--no-schema`). Hạn chế: bảng ảo (FTS5) không xuất được; đang xuất thì chặn các truy vấn khác nên chạy ngoài giờ cao điểm. Nhập lại: `wrangler d1 execute <db> --remote --file=backup.sql` (bỏ `BEGIN TRANSACTION/COMMIT` nếu vướng).
- Tự động: Cron Trigger (`"triggers": {"crons": ["0 20 * * *"]}`, tính theo UTC, cập nhật có thể mất đến 15 phút) gọi hàm `scheduled` để đẩy bản sao sang R2 hoặc xuất CSV gửi qua Telegram; giới hạn số cron trên gói Free: cần xác minh.
- Xuất CSV: endpoint `/admin/api/export.csv` (sau Access) trả CSV; bắt buộc thoát ký tự đầu `=`, `+`, `-`, `@` (chống chèn công thức khi mở bằng Excel). Kết quả truy vấn tối đa 50 MB (D1 ghi áp dụng từ 04/11/2026).

### 4.7 Biến bí mật
- `npx wrangler secret put TURNSTILE_SECRET` (tương tự `TG_TOKEN`, `TG_CHAT`, `SYNC_TOKEN`). Lệnh này tạo phiên bản mới và triển khai ngay; nếu dùng triển khai dần thì `wrangler versions secret put`.
- Chạy local: file `.dev.vars` (hoặc `.env`) cùng thư mục cấu hình; thêm `.dev.vars*` và `.env*` vào `.gitignore`, không commit.
- Không để thông tin nhạy cảm trong `vars` của wrangler (chúng hiển thị). Giá trị secret không xem lại được sau khi đặt.
- Tối đa 64 biến (secret + text) mỗi Worker, mỗi biến 5 KB (gói Free).
- Cộng sự không bao giờ in giá trị secret ra khung chat hoặc ghi vào tệp báo cáo.

---

## 5. Giới hạn gói miễn phí (đọc trực tiếp từ trang chính thức ngày 19/11/2026)

D1 (trang /d1/platform/limits và /d1/platform/pricing):
- 10 database/tài khoản; tối đa 500 MB/database; 5 GB lưu trữ/tài khoản.
- Đọc 5 triệu dòng/ngày; ghi 100.000 dòng/ngày (gói Free).
- 50 truy vấn mỗi lần Worker chạy (`db.batch()` tính là 1); 6 kết nối đồng thời mỗi lần chạy; mỗi truy vấn tối đa 30 giây.
- Một dòng/chuỗi tối đa 2 MB; tối đa 100 tham số bind mỗi truy vấn; 100 cột mỗi bảng.
- Time Travel 7 ngày.
- Gói Paid (so sánh): 10 GB/database, 1.000 truy vấn mỗi lần chạy, Time Travel 30 ngày.

Workers Free (trang /workers/platform/limits):
- 100.000 yêu cầu/ngày, đặt lại lúc nửa đêm UTC.
- 10 ms CPU mỗi yêu cầu HTTP; 50 subrequest mỗi lần chạy; 100 Worker/tài khoản; Worker tối đa 64 MiB.
- Không có giới hạn chung theo số yêu cầu/giây.

Nhận xét: shop nhỏ vài chục đến vài trăm lead/ngày dùng chưa tới 1% hạn mức ghi. Chỗ cần coi chừng: truy vấn quét cả bảng ở trang admin (tốn "dòng đọc") và việc chỉ mục có tính vào "dòng ghi" hay không (cần xác minh). Luôn `LIMIT` + phân trang, có chỉ mục. Khi vượt hạn mức Free thì request bị từ chối (429); nếu lead quan trọng thì nâng Workers Paid (giá tính theo trang Cloudflare, tôi chưa đọc con số, cần xác minh).
CPU 10 ms/yêu cầu rất chặt cho việc băm mật khẩu PBKDF2 nặng: thêm lý do chọn Cloudflare Access thay vì tự băm trên gói Free (cần xác minh bằng thử thật).

---

## 6. Kênh thông báo và đẩy dữ liệu đi
- Telegram (khuyên dùng, đơn giản nhất): `POST https://api.telegram.org/bot<token>/sendMessage` với `chat_id` và `text`, trả JSON có `ok`. FAQ chính thức: một chat không nên gửi quá 1 tin/giây, nhóm tối đa 20 tin/phút, broadcast ~30 tin/giây. Giới hạn 4096 ký tự mỗi tin và cách lấy `chat_id`: cần xác minh (trang API quá dài, chỉ đọc được phần đầu).
- Zalo: chỉ có tài liệu bên thứ ba (SDK) nói endpoint tin tư vấn `https://openapi.zalo.me/v3.0/oa/message/cs`, chỉ gửi được trong 48 giờ kể từ lần khách nhắn OA gần nhất, cần OA được duyệt và access token riêng. TOÀN BỘ cần xác minh trên developers.zalo.me. Với lead mới từ form (khách chưa nhắn OA) thì tin tư vấn có thể không gửi được; ZNS (tin theo mẫu, tính phí) là hướng khác: chưa đọc, cần xác minh. Khuyên: lead mới thông báo cho CHỦ qua Telegram; Zalo để TISA BOT lo trên máy nếu đã có.
- Google Sheets: `spreadsheets.values.append` cần `spreadsheetId`, `range`, `valueInputOption` và body `values`; xác thực bằng tài khoản dịch vụ hoặc OAuth. Làm từ Worker phải tự ký JWT tài khoản dịch vụ: phức tạp, nên để bước nâng cao. Cách đơn giản hơn là xuất CSV.
- Email: hookforms-cloud dùng Resend/SendGrid/Gmail qua Queues; saasmail dùng Cloudflare Email Sending/Resend. Chọn Resend hoặc tương đương nếu cần, chưa đọc giá.
- Webhook chung: Worker có thể POST JSON sang bất kỳ URL, nhưng KHÔNG nên trỏ về địa chỉ do người dùng nhập tùy ý (nguy cơ SSRF; hookforms-cloud có danh sách chặn SSRF).

---

## 7. Nối với TISA BOT: thêm đường CRM chạy đám mây

Hiện tại (theo mô tả): form -> TISA BOT trên máy -> CRM trên máy; chatbot có công cụ `crm_push_lead`. Tôi chưa đọc mã nguồn gói đó nên các giả định dưới đây cần đối chiếu.

### Phương án A (khuyên dùng, đơn giản nhất): cloud nhận lead, máy KÉO về
1. Trang lead trỏ form tới `https://<tên miền>/api/lead` của Worker. Lead lưu vào D1, Telegram báo ngay cho chủ. Máy tắt thì lead vẫn vào.
2. TISA BOT, khi máy bật và định kỳ (ví dụ 5 phút), gọi `GET /api/sync/leads?since=<updated_at cuối cùng>&limit=100` với Bearer token. Với mỗi lead, đối chiếu theo `id` (hoặc `phone`) rồi ghi vào CRM trên máy. Nhập lại nhiều lần không sinh trùng (idempotent).
3. Sau khi nhập xong, TISA BOT có thể gọi `POST /api/sync/ack` để Worker ghi sự kiện `sync_out`. Không bắt buộc.
Lợi: không mở cổng vào máy chủ, không cần tunnel; máy tắt lead vẫn an toàn. Rủi ro thấp nhất.

### Phương án B: máy đẩy lên (chatbot -> cloud)
- `crm_push_lead` thêm chế độ gọi `POST /api/sync/import` (Bearer) kèm `client_id` ổn định để cloud upsert. Dùng cho lead đến từ Messenger/Zalo/điện thoại mà chatbot nhập tay, để cloud cũng có bản đầy đủ.
- Hai chiều đủ cho hầu hết nhu cầu: web -> cloud -> kéo về máy; chatbot trên máy -> đẩy lên cloud.

### Phương án C (không khuyên): cloud gọi vào máy
- Worker POST webhook vào TISA BOT cần máy có địa chỉ công khai (tunnel/cổng mở). Máy tắt là mất tin, lại thêm bề mặt tấn công vào máy chủ shop.

### Quy tắc tránh xung đột
- Chọn MỘT nơi là sổ chính cho trạng thái chăm sóc. Mặc định: cloud là sổ chính cho lead đến từ web (khi chủ bật "chạy 24/7"); CRM máy chỉ sao chép + được phép sửa trạng thái thông qua API.
- Nếu cho sửa hai nơi: dùng `updated_at`, bản mới hơn thắng, ghi `lead_events` cho mỗi thay đổi để truy được. Đừng cố đồng bộ xóa; dùng `deleted_at`.
- Khóa đồng bộ là `leads.id` (uuid) + `phone` chuẩn hóa. Chuẩn hóa số điện thoại ở cả hai phía bằng cùng một hàm.

### Rủi ro chính
1. Lộ dữ liệu: token đồng bộ hoặc admin bị lộ nghĩa là lộ danh bạ khách. Giảm bằng Access, secret, token riêng có thể đổi, không ghi vào mã.
2. Spam làm cạn 100.000 yêu cầu/ngày hoặc 100.000 dòng ghi/ngày: lớp chống spam ở 4.3; theo dõi Workers Analytics.
3. Chủ không biết kỹ thuật bị kẹt khi gặp lỗi migration/secret: cộng sự phải có kịch bản "kiểm tra sức khỏe" (gửi lead thử, xem D1, xem Telegram) và sao lưu `d1 export` định kỳ trước mỗi lần đổi schema.
4. Pháp lý dữ liệu cá nhân (4.5): cần chính sách quyền riêng tư và cách xóa theo yêu cầu.
5. Hai nguồn sự thật làm lệch trạng thái: xem quy tắc ở trên.
6. Cloudflare đổi giới hạn/giá: mọi con số ở mục 5 phải đọc lại trước khi báo cho học viên.
7. Dùng mẫu GitHub ít sao hoặc không giấy phép (mục 2 #4-#6): chỉ lấy ý tưởng, tự viết lại.

### Gợi ý triển khai cho cộng sự (thứ tự)
1. Tạo D1 + chạy migration `0001` (kèm sao lưu `d1 export` trước các lần đổi sau).
2. Tạo Turnstile widget, `wrangler secret put` các khóa, triển khai Worker với `/api/lead`.
3. Bật Cloudflare Access cho `/admin*`, kiểm token trong Worker.
4. Gửi lead thử từ trang thật, xác nhận D1 + Telegram.
5. Thêm `/api/sync/leads` + token máy-với-máy, rồi mới sửa TISA BOT để kéo về.
6. Ghi lại cho chủ: tên miền, tên database, nơi lưu sao lưu, ai có quyền admin. Không ghi giá trị khóa.

---

## 8. Việc cần xác minh thêm (danh sách gom)
- Giới hạn số vòng PBKDF2 và 10 ms CPU với băm mật khẩu trên Workers Free.
- Số người dùng tối đa Zero Trust gói Free; giá Workers Paid.
- Chỉ mục có tính vào "dòng ghi" của D1 hay không.
- Cờ `--local/--remote` và cú pháp chính xác của `wrangler d1 migrations` (trang tham chiếu lệnh Wrangler).
- Số cron trigger tối đa gói Free.
- `CF-Connecting-IP`, giới hạn 4096 ký tự Telegram, cách lấy `chat_id`.
- Toàn bộ Zalo OA/ZNS (developers.zalo.me).
- Văn bản gốc Luật BVDLCN 91/2025/QH15 và NĐ 356/2025/NĐ-CP: nghĩa vụ của shop nhỏ, hồ sơ đánh giá tác động, danh mục dữ liệu nhạy cảm.
- Giấy phép AGPL của Twenty/EspoCRM/Frappe nếu chủ muốn đóng gói lại.
- Mã nguồn gói "Web CRM + Lead Page" hiện tại của TISA BOT (tên trường, cách `crm_push_lead` gọi).
