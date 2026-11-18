# 05 - TISA BOT tự hiểu chính nó (dành cho Đạt Đấu Nối)

Nguồn: bản dựng `thư mục cài TISA BOT` (VERSION 0.574.0). Trong file này `[app]` = thư mục đó.
Máy học viên cài bản git clone ở `~/TISABot` (macOS, theo `[app]/packaging/macos/bootstrap.sh`). Đường dẫn bên dưới tính từ `[app]` hoặc từ thư mục cài.
Quy ước đặt tên: tên công cụ, header, biến môi trường trong bản học viên đều là `tisa_*`, `X-TISA-*`, `TISA_*` (xưởng `build.py` đổi từ TISA, xem `(đường dẫn máy xưởng)`). Vài tài liệu cũ trong `[app]/docs` (06, 07, 20, 25) vẫn ghi "TISA" và `tisa_*`: đọc là `tisa_*`.

## 1. App gồm những phần nào

| Phần | Là gì | Nơi nằm |
|---|---|---|
| Máy chủ TISA BOT | Một tiến trình Python FastAPI, cổng `7777` (`TISA_PORT`), bind `127.0.0.1` mặc định | `[app]/server/main.py` (rất lớn, tra bằng grep), `ARCHITECTURE.md` |
| Dashboard | JS thuần, không build, phục vụ ở `/static` | `[app]/dashboard/` (`console.js` giữ thanh bên) |
| MCP Hub | Cổng công cụ DUY NHẤT cho mọi engine: gộp kết nối, plugin, công cụ file, kiểm quyền cứng, ghi nhật ký | `server/mcp_hub.py`, endpoint `POST /hub/mcp` |
| Kho kết nối | Mẫu connector (`system/mcp-catalog.json`) + tài khoản đã nối (`mcp_servers.json`) | `server/mcp_catalog.py`, `server/mcp_store.py` |
| Plugin gói sẵn | Công cụ `tisa_*` viết bằng Python (`plugin.yaml` + `plugin.py`) | `system/plugins/*` (xem file 06) |
| Trình duyệt TISA / Điều khiển máy | Công cụ `tisa_browser_*`, `tisa_desktop_*`, `tisa_drive_do` | `server/tisa_browser.py`, `tisa_desktop.py`, `tisa_drive.py` |
| Trang riêng của bộ TISA | Quản lý web, Quảng Cáo, Hồ sơ, Chuyển máy, Tài khoản nhân viên | `server/tisa_web.py` (`/tisa-web/`), `tisa_quang_cao*.py` (`/tisa-quang-cao/`), v.v. |
| Đội Quân AI | Bảng giao việc riêng, cổng `7788`, là GIAO DIỆN của cùng TISA BOT | `suite/` (`mcp_doi_quan.py`, `setup_suite.py`, `skills/`, `agents/`), `QUICKSTART.md` |
| Skill `/ts-` và `dq-` | 52 skill `ts-*` + 24 skill `dq-*` (cộng sự), đếm trong `suite/skills/` | `suite/skills/`, được `system_sync.py` chép vào mọi brain |

## 2. Thanh bên (rail) và trang nào làm gì

Nguồn: `[app]/dashboard/console.js` (`RAIL_GROUPS`), `dashboard/tisa-icons.js` (bảng `DQ`, `TRANG_RIENG`), nhãn trong `dashboard/i18n/vi.json`.

| Nhóm | Mục (id) | Dùng khi đấu nối |
|---|---|---|
| Ghim | Hỏi nhanh (`chat`), Hỏi chuyên gia (`workspace`), Giao dự án (`dq-du-an`), Chatbot (`conversations`), Quảng Cáo (`dq-quang-cao`) | Chatbot = hòm thư khách + tab Bot + tab Kênh (token từng kênh của bot) |
| Đội Quân AI | Team, Cần anh, Đang làm, Kết quả, Đội ngũ | Đạt Đấu Nối là cộng sự trong Đội ngũ |
| Bộ não | Mạng nơ-ron (`home`), Hồ sơ của anh, Tệp tin, Tự học, Nạp kiến thức, Kho tư liệu | Hồ sơ doanh nghiệp để skill đọc |
| Năng lực | Kỹ năng, Công cụ (`plugins`), Terminal | Công cụ = bật/tắt plugin `tisa_*` |
| Việc | Nhiệm vụ (`tasks`), Tích hợp (`webhooks`) | Tích hợp = webhook và Token API cho chương trình ngoài gọi vào |
| **Kết nối** | Quản lý web (`dq-web`), **Kết nối** (`mcp`), TISA Store (`packs`), **Kênh Admin** (`channels`), Cookies (`logins`) | Nơi làm việc chính của Đạt |
| Hệ thống (đáy) | Models, Cài đặt, Link chia sẻ, Tài khoản, Tài khoản nhân viên, Chuyển máy chủ | Models = đăng nhập engine; Cài đặt có Truy cập từ xa, Tên miền & SSL |

Trang ẩn khỏi thanh bên nhưng vẫn mở được: `chatbots`, `usage`, `pet`, `logs` (Cập nhật), `coding` (`RAIL_AN` trong `console.js`).
Trang Kết nối (`page.mcp`) có 3 khu: Đã kết nối, Kết nối sẵn có (ô tìm + lọc nhóm), khối gập "Kết nối sẵn của Claude Code và Codex" (theo `docs/09-mcp-va-so-lieu.md`). Từ 0.55.36 phần lớn dịch vụ nằm ở tab **TISA Store**, phải bấm Cài đặt trước.
Mỗi thẻ kết nối có nút **Kết nối tự động** (V3.02): cấp Toàn quyền trình duyệt và máy rồi gửi cho cộng sự lời nhờ lấy từ `dashboard/tisa-ket-noi-huong-dan.json` (15 thẻ, cập nhật 17/11/2026).

## 3. Dữ liệu và cấu hình nằm đâu

Ba nơi tách biệt (`ARCHITECTURE.md` mục "Data on disk"):

| Nơi | Mặc định | Có gì |
|---|---|---|
| Cây mã | `~/TISABot` | `server/`, `dashboard/`, `system/`, `suite/`, `CLAUDE.md` (lõi lời dặn, KHÔNG sửa tay) |
| `TISA_STATE_DIR` | `~/TISABot/server` (`bin/tisa-start.sh` đặt `TISA_STATE_DIR="${APP_DIR}/server"`); Docker `/data/state` | Trạng thái chạy |
| `BRAINS_DIR` | `<cây mã>/brains` | Mỗi brain một thư mục |
| Đội Quân AI | `~/.config/doi-quan-ai/.env` (mã bảng), `~/.doi-quan-ai/setup-status.json`, `~/.doi-quan-ai/logs/` | Theo `QUICKSTART.md`, `suite/mcp_doi_quan.py` |

Trong `TISA_STATE_DIR` (đã xác nhận trong mã hoặc docs):
- `settings.json`: cấu hình; trường bí mật lưu dạng `enc:` (Fernet), khoá ở `.secret_key`. Chép settings sang máy khác mà thiếu `.secret_key` là mất hết khoá (`docs/14-bao-mat-tai-khoan.md`). Khoá hay đụng: `model.main` (provider), `mcp.hub`, `mcp.strict`, `mcp.lazy_tools`, `web.tavily_key|brave_key|searxng_url`, `media`, `telegram.token`.
- `mcp_servers.json`: kho kết nối v2 (secret mã hoá). Bản v1 cũ backup ở `mcp_servers.v1.bak.json`.
- `.hub_token`: Bearer cho `/hub/mcp` (chỉ gọi được từ chính máy). AI không đọc được (`secret_guard.py`).
- `.oauth_mcp.json`, `.oauth_clients.json`: token và client OAuth của MCP (`oauth_mcp.py`, `tisa_oauth_cimd.py`).
- `mcp_audit.jsonl`: nhật ký gọi công cụ (xem ở menu chip tài khoản, "Nhật ký gọi tool").
- `channel_accounts.json`, `chatbots.json`, `customer_conversations.sqlite3`: kênh bot khách. `inbox.json`: kết quả nền. `conversations.db`: lịch sử chat.
- `claude-mcp-cache.json`, `claude-mcp-mac-dinh.json`: cache và dấu của `tisa_claude_mcp.py`.
- `trinh-duyet/` (`ho-so.json`, `muc.json`, `nhat-ky.jsonl`, `ho-so/`, `anh/`), `dieu-khien-may/` (`muc.json`, nhật ký, `drive-hoan-tac-*.json`), `quang-cao/` (`tai-khoan.json`, `so-mcp.json`, `phieu-thiet-lap.json`), `tisa_web/web.json`, `login_vault.sqlite3` (Cookies, quyền 600).
- `tisa.log`, `update.log`: nhật ký máy chủ. `server/tisa.pid`.
Brain mặc định `Brain Default`: `CLAUDE.md`, `memory/MEMORY.md`, `wiki/`, `sources/`, `agents/<slug>.md` (cộng sự), `skills/<slug>/SKILL.md`, `TISA/` (loops, reminders, kanban), `04-ket-qua/` (kết quả skill, hay thấy trong bộ não học viên).

Bí mật ngoài settings: macOS Keychain, mục bắt đầu `tisa-bot-` (`tisa-bot-drive`, `tisa-bot-drive-client`, `tisa-bot-mo-khoa`, `tisa-bot-<dịch vụ>`). Chỉ macOS, Windows chưa làm (`server/tisa_keychain.py`). Mục `mo-khoa` bị cấm ghi qua `luu_keychain`.

## 4. Cổng và dịch vụ

| Cổng/địa chỉ | Là gì | Nguồn |
|---|---|---|
| `127.0.0.1:7777` | TISA BOT (dashboard + API + `/hub/mcp`). Ngoài loopback thì tự bắt đăng nhập | `docs/16-cau-hinh-env.md` |
| `127.0.0.1:7788` | Bảng Đội Quân AI | `suite/setup_suite.py` (`TISA_BOARD_PORT`) |
| `127.0.0.1:9335` đến `+64` | Trình duyệt TISA (Chrome DevTools, `TISA_BROWSER_PORT`), chỉ nghe loopback, mỗi hồ sơ một cổng | `tisa_browser.py` đầu file |
| `localhost:8000` | Google Workspace/Tasks chạy local: Google trả về cổng này sau khi bấm Đồng ý (Docker phải mở cổng 8000) | `docs/09` mục 4 |
| `127.0.0.1` ngẫu nhiên | `tisa_drive.dang_nhap` mở cổng tạm chờ Google chuyển về | `tisa_drive.py` |
| `/connect/oauth/callback` | Địa chỉ quay về OAuth MCP (Slack, Google Ads, Meta Ads Graph, Cloudflare OAuth...) | `main.py` dòng ~7434 |
| `/messenger/webhook`, `/messenger/oauth/callback`, `/messenger/privacy` | Fanpage | `main.py` ~29025 |
| `/zalo-oa/webhook`, `/zalo-oa/oauth/callback` | Zalo OA | `main.py` ~29651 |
| `/wechat/webhook` | WeChat OA | `main.py` ~29821 |
| `/tisa-web/thu/<khoá>` | Form khách để lại thông tin (công khai, chỉ nhận ghi) | `tisa_web.py` |

Webhook Meta, Zalo OA, WeChat, WhatsApp đều cần tên miền HTTPS công khai (Cài đặt, Truy cập từ xa: Link nhanh `trycloudflare.com` đổi mỗi lần khởi động, Tên miền riêng qua Cloudflare Tunnel, hoặc Tailscale chỉ riêng tư, `docs/15-thuong-hieu-ten-mien.md`). Slack Socket Mode, Discord, Lark, Telegram, Zalo Bot dùng kết nối ra ngoài, KHÔNG cần tên miền.

## 5. Engine (bộ não) và việc nối công cụ

Nguồn: `ARCHITECTURE.md` mục Engines, `docs/10-models-va-engine.md`. 12 provider, hai nhóm:
- Engine CLI/OAuth: `anthropic-cli` (Claude Code, mặc định), `openai-oauth` (ChatGPT qua `codex`), `grok-cli`, `antigravity-cli`. Có Bash, file, WebSearch/WebFetch riêng của CLI.
- Engine API: openrouter, anthropic-api, openai, gemini, groq, deepseek, ollama. Chỉ có công cụ qua hub, KHÔNG có Bash, không WebSearch riêng.
TISA BOT không đọc token đăng nhập Claude, chạy chính binary `claude` qua `claude-agent-sdk` (`server/claude_sdk_engine.py`). Máy PHẢI có `claude` CLI. Đăng nhập: trang Models, thẻ Claude Code, "Đăng nhập Claude" (hoặc `claude auth login --claudeai`).
Lõi lời dặn mọi engine nhận: `CLAUDE.md` gốc + `memory/MEMORY.md` + khối điều khiển trình duyệt/máy của chủ (`server/tisa_cong_cu_ai.py`, giữ TĨNH để cache engine không vỡ).

## 6. Ba nguồn MCP và cách được nạp

| # | Nguồn | Ai thấy | Nạp thế nào | Xem ở đâu |
|---|---|---|---|---|
| 1 | **Kho Kết nối của TISA BOT** (`mcp_store`) | MỌI engine | Hub gộp: engine CLI thấy MỘT server MCP tên `tisa` (`POST /hub/mcp`, file cấu hình `.mcp_hub_<mode>*.json` quyền 600, header `X-TISA-Mode`, `X-TISA-Engine=claude`, `X-TISA-Vault`); engine API gọi `discover_all()` trong tiến trình. Codex: hub tự đẩy sang qua `codex_profile()`. Antigravity: ghi `~/.gemini/config/mcp_config.json` (tắt bằng `TISA_AGY_MCP_HOME=0`). Grok: `<brain>/.grok/config.toml` | Trang Kết nối, khu Đã kết nối |
| 2 | **MCP của Claude Code trên máy** (`claude mcp add`, `~/.claude.json`, `.mcp.json`) | CHỈ engine Claude | Công tắc `mcp.strict` mặc định False nên Claude nạp luôn. Công cụ tên `mcp__<tên>__*` gọi THẲNG, KHÔNG qua `tisa_run_tool` | Thẻ "Đã nối MCP của Claude Code vào TISA BOT" (`server/tisa_claude_mcp.py`, quét `claude mcp list` mỗi 600 giây, `/tisa-claude-mcp/trang-thai`); khối gập cuối trang Kết nối |
| 3 | **Connector đồng bộ từ claude.ai** (Meta Ads, Drive, Canva...) | CHỈ engine Claude | Hiện trong `claude mcp list` với tiền tố "claude.ai "; `tisa_connections` liệt kê với `source: claude_account` | Cùng thẻ trên; trạng thái `Needs authentication` = đăng nhập lại ở Claude Code, không phải hỏng |

Hệ quả khi đấu nối:
- Nối vào Kho (nguồn 1) là cách DUY NHẤT mọi bộ não dùng chung. Tuyệt đối không dùng `claude mcp add` hay `codex mcp add` để "thêm MCP cho học viên": nó rơi vào config riêng, trang Kết nối không hiện ở khu Đã kết nối (lý do tồn tại của `tisa_add_mcp`, `system/plugins/tisa-connect/plugin.py`).
- Đã có MCP bên Claude Code (ví dụ Meta Ads `ads_*`) thì dùng luôn, chỉ khi không có mới rơi về plugin chỉ đọc `meta_ads_*` (`tisa_cong_cu_ai.py`).
- Engine API không gọi được connector tài khoản Claude: `tisa_connections` ghi `dung_duoc_o_luot_nay: false` và chỉ hai cách (nối vào Kho, hoặc đổi engine sang Claude Code).
- Tool bị mức quyền ẩn vẫn "CÓ THẬT": `tisa_connections` liệt kê ở `tool_bi_an_do_quyen` + `cach_mo`.
- Lọc lười: khi tool nhiều (`mcp.lazy_tools=auto`, ngưỡng 40) hub chỉ đưa lõi + hai meta-tool `tisa_search_tools` (tìm) và `tisa_run_tool` (gọi). Công cụ trình duyệt/máy nằm ở tầng này: tìm bằng `tisa_search_tools query="trình duyệt"` rồi gọi bằng `tisa_run_tool`. KHÔNG dùng ToolSearch của Claude hay Playwright MCP để tìm chúng (`tisa_cong_cu_ai.py`).
- Chế độ cũ không qua hub: `settings.json` đặt `"mcp": {"hub": false}` (`docs/09`).

### Quyền kết nối (cứng trong mã, không phải lời dặn)
`mcp_catalog.allowed()`: mỗi kết nối có `perm` = `readonly` | `safe` (Ghi nháp) | `full` (Toàn quyền); mỗi lượt chạy có `mode` (`suggest` ép readonly, `auto` trần safe); áp mức chặt hơn. Mặc định hầu hết thẻ readonly (xem `default_perm` trong catalog); Zalo `full`; Google Workspace/Sheets/Tasks, Substack `safe`. Nâng quyền chỉ người dùng làm ở menu chip. Bot khách và việc nền `auto` bị siết thêm, `tisa_add_mcp`, `tisa_web_*`, `tisa_browser_*`, `tisa_desktop_*`, `tisa_drive_do`, `tisa_login` thuộc `OWNER_ONLY_TOOLS` (`mcp_hub.py` ~192): chatbot trả lời khách không thấy.

Bộ 17 connector dựng sẵn trong `system/mcp-catalog.json`: composio, cloudflare, cloudflare-oauth, zalo, botcake, google-sheets, google-search-console, google-workspace, google-tasks, google-ads, google-analytics, google-calendar, gmail, http-api, substack, google-keep, notebooklm. Mọi dịch vụ khác (Meta Ads, Slack, Lark, Pancake, TikTok Ads, Zernio...) nằm ở kho `github.com/tieusangstudio-hash/tisa-store` (`system/pack-index.json` đã đóng băng), cài bằng tab TISA Store.

## 7. Cộng sự và skill chạy thế nào

- Cộng sự = file `agents/<slug>.md` trong brain: `name, slug, role, skills[], model, model_provider, reasoning`. Đạt Đấu Nối là `suite/agents/tisa-dau-noi.md` (Opus, `anthropic-cli`, reasoning high, skill: `dq-dau-noi-cong-cu`, `dq-ho-tro-ket-noi`, `dq-trinh-duyet`, `dq-dieu-khien-may`, `dq-kho-tu-lieu`, `ts-ket-noi-ung-dung`, `ts-dua-web-len-mang`, `ts-cai-thanh-toan`, `ts-len-camp-facebook`).
- Đội Quân AI và trang Cộng sự của TISA BOT dùng chung dữ liệu: sửa bên này, bên kia đổi trong vài giây (`QUICKSTART.md` mục 4). Claude giao việc cho đội qua MCP `doi-quan-ai` (`suite/mcp_doi_quan.py`, đọc mã bảng ở `~/.config/doi-quan-ai/.env`). Khởi động lại Claude sau khi cài.  MCP `doi-quan-ai` báo `ENOENT` (không thấy file python) nghĩa là đường python đã ghi vào cấu hình Claude không còn tồn tại: cần xác minh trong mã `setup_suite.py`/bộ cài, rồi chạy lại bộ cài (chạy lại bao nhiêu lần cũng được, `QUICKSTART.md`).
- Skill: thư mục `skills/<slug>/SKILL.md`, `description` tối đa 150 ký tự và không mở đầu bằng "Kích hoạt khi..." (`docs/06-skills.md`). Engine nạp theo mô tả: Claude native từ `.claude/skills`, engine khác qua `tisa_use_skill name=<slug>`. `system_sync.py` chép skill hệ thống vào mọi brain, không ghi đè file người dùng đã sửa.
- Bài học tự ghi: cuối câu trả lời `TISA_LESSON: <công cụ>: <điều học được>` được nạp lại ở lần sau (`suite/skills/dq-dau-noi-cong-cu/SKILL.md`).
- Chạy nền (Kanban, loop, nhắc hẹn, workflow) bị chặn công cụ theo từng lần gọi; việc nền mức `auto` không bao giờ đụng tiền/đơn/gửi tin.

## 8. Quyền trình duyệt và máy (hai bảng "Điều khiển của AI")

Giao diện: bảng nổi "Điều khiển của AI" (`dashboard/tisa-trinh-duyet.js`). API: `/trinh-duyet/*` và `/may-ai/*`.

**Trình duyệt TISA** (`server/tisa_browser.py`): Chrome/Edge riêng của TISA, hồ sơ bền ở `trinh-duyet/ho-so/`, giao thức DevTools. Ba mức tự động (`muc.json`): `hoi_het` (duyệt từng bấm/gõ), `quan_trong` (mặc định, chỉ duyệt đăng/gửi/xóa/đổi bảo mật/đăng ký), `toan_quyen` (có hạn giờ, hết hạn tự về `quan_trong`). Cấp Toàn quyền xóa cờ "Đã dừng".
Rào luôn có ở mọi mức:
- Ô mật khẩu, OTP, số thẻ, CAPTCHA: AI không gõ (`CAN_NGUOI_DUNG`, dùng `wait_user`).
- Thanh toán, nạp tiền, mua: `CAN_NGUOI_DUNG`. Trang ngân hàng, ví, sàn coin, Stripe, PayPal: `BI_CHAN` (regex `_MIEN_CHAN`).
- Đăng, gửi, xóa, đổi bảo mật, cấp quyền, đăng ký, tạo quảng cáo: `CAN_DUYET` kèm `duyet_id` (dùng một lần, 10 phút, khớp đúng việc) cho tới khi anh bấm Duyệt (`/trinh-duyet/duyet`).
- Tối đa 45 thao tác/phút (`CHAM_LAI`). Nút Dừng ngay: `DA_DUNG`.
- Cổng DevTools không bật `--remote-allow-origins`: trang web không nối vào được.
Hồ sơ: nhiều trình duyệt có tên (Facebook 1, Facebook 2...), chọn bằng `trinh_duyet=`. Anh đã chọn một cái thì tham số khác bị `KHOA_TRINH_DUYET`; đổi bằng `op=doi_trinh_duyet` (anh Duyệt). "Chrome của anh" (`tisa_browser_ngoai.py`): nối vào Chrome thật qua `chrome://inspect/#remote-debugging`, Chrome hỏi Allow một lần (`CHUA_BAT_CHROME`, `CHUA_CHO_PHEP`); TISA không bao giờ đóng tiến trình Chrome của anh. Hồ sơ Chrome thật chọn bằng `op=mo_chrome ho_so=<tên>` (`KHOA_HO_SO` nếu đổi). Trình duyệt TISA nhập cookie từ Chrome thường KHÔNG giữ được đăng nhập Google (`references/kinh-nghiem-da-lam.md`).

**Điều khiển máy** (`server/tisa_desktop.py`): mức `tat | hoi_het | quan_trong | toan_quyen`. macOS cần quyền Trợ năng + Ghi màn hình (`op=cai_dat_quyen`, `huong_dan_quyen`). Chuột riêng của TISA (chấm cam) không giành chuột thật. Cấm xóa tệp, cấm cửa sổ đăng nhập hệ thống/quản lý mật khẩu/ví/ngân hàng; công tắc "Cho phép AI xóa tệp" có hạn giờ 15 phút. Đưa chuột về góc trên trái cũng dừng. `op=mo_khoa`: mở khóa Mac lúc anh ở xa, mật khẩu tự lấy từ Keychain, chỉ khi chính anh nhắn từ dashboard hoặc Zalo (`tisa_mo_khoa.py`).
Mọi nhật ký ở `trinh-duyet/nhat-ky.jsonl` và `dieu-khien-may/`.

## 9. Điều cần nhớ khi đấu nối

1. Nối vào Kho Kết nối trước, mọi engine dùng chung; MCP của Claude Code chỉ là đường bổ sung cho engine Claude.
2. Mật khẩu/token đi bằng `dan_vao_tisa`, `dan_ma`, `luu_keychain` (giá trị đi thẳng, AI không thấy); không `type`, không chép chat.
3. Giao diện TISA điều khiển bằng `tisa_browser_do op=ui_tisa`, không mở TISA trong Chrome.
4. Việc "chỉ người thật làm được" (đăng nhập, OTP, CAPTCHA, hộp Cho phép, Touch ID) dừng bằng `wait_user` hoặc `tisa_desktop_do op=cho_nguoi_that`, TISA báo anh qua dashboard/Zalo rồi tự làm tiếp (`tisa_bao_anh.py`).
5. Thay đổi file `.py` thì khởi động lại server; giao diện sai thì Ctrl+Shift+R (`docs/17-khac-phuc-su-co.md`).
6. App không có công cụ riêng để deploy web lên Cloudflare: xem file 08, kịch bản 6 (phần cần xác minh).
