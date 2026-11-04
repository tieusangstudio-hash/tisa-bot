---
name: ts-ket-noi-ung-dung
description: "Gọi bằng /ts-ket-noi-ung-dung. Xác định cần kết nối gì và hướng dẫn kết nối an toàn AI với Google Drive, Gmail, Google Sheets, Facebook/Meta Ads, Zalo OA, Telegram bot, Canva, Notion… qua mục Kết nối/Connectors/Apps hoặc máy chủ MCP/API chính thức; cấp quyền tối thiểu, thử chỉ đọc trước. Không bao giờ lưu mật khẩu/token. Từ khóa: kết nối ứng dụng, kết nối google drive, kết nối facebook, cài MCP, API, connector, telegram bot, zalo OA, webhook, cấp quyền."
---

# /ts-ket-noi-ung-dung — Kết nối AI với ứng dụng (MCP, API, Connectors)

> Giúp bạn nối AI với các ứng dụng đang dùng (Google, Facebook, Zalo, Telegram…) để AI đọc dữ liệu và làm việc giúp — an toàn,
> đúng quyền, không lộ mật khẩu. Kết quả: kết nối đã thử chạy, sổ kết nối (tên, quyền, ngày) và cách ngắt khi cần.

**Loại Bộ Não:** CHỈ LƯU (không bao giờ lưu mật khẩu/token)

## Khi nào dùng
- Muốn AI đọc Google Drive/Gmail/Google Sheets/Calendar của mình.
- Muốn AI đọc số liệu Fanpage, quảng cáo Meta để báo cáo hoặc tự động hóa.
- Muốn nhận thông báo qua Telegram bot, hoặc chăm khách qua Zalo OA.
- Có công cụ có máy chủ MCP/API, cần cài vào Claude/ChatGPT/Codex/Antigravity.
- Kết nối cũ bị lỗi, hết hạn, cần kết nối lại hoặc thu hồi quyền.

**Không dùng khi:** đã kết nối xong và muốn thiết kế luồng tự động Facebook/quảng cáo → `/ts-tu-dong-hoa-meta`;
cần lịch chạy định kỳ → `/ts-lap-lich-tu-dong`; cần luồng báo đơn qua Telegram hoàn chỉnh → `/ts-bao-don-telegram`;
cài cổng nhận tiền → `/ts-cai-thanh-toan`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Bắt đầu từ việc cần làm, không từ tên công nghệ
Hỏi (gợi ý A-B-C-D):
- Bạn muốn AI làm việc gì với ứng dụng đó? (A) Chỉ đọc/tóm tắt · (B) Soạn nháp · (C) Ghi/cập nhật dữ liệu · (D) Gửi/đăng thay bạn.
- Ứng dụng nào, tài khoản nào (cá nhân hay công việc)?
- Đang dùng AI ở đâu? (A) Claude trên web/máy tính · (B) ChatGPT · (C) Claude Code/Codex (có cửa sổ lệnh) · (D) Google Antigravity / khác.
- Dữ liệu tối thiểu cần là gì? (vd chỉ 1 file Google Sheets, không cần cả Drive).

Chốt: hệ thống nguồn/đích, dữ liệu đi qua, tần suất, người sở hữu tài khoản và hậu quả nếu lỗi.

### Bước 2 — Tìm cách kết nối chính thức trước
Thứ tự ưu tiên:
1. **Kết nối có sẵn trong nền tảng AI** (mục Kết nối / Connectors / Apps) — dễ nhất, đăng nhập trên trang chính thức.
2. **Máy chủ MCP chính thức** do chính hãng ứng dụng công bố.
3. **Phần mềm trung gian chính thức** (công cụ tự động hóa, CRM có tích hợp sẵn).
4. **API tự viết mã** — chỉ khi 3 cách trên không có, và người dùng có người hỗ trợ kỹ thuật hoặc đồng ý để AI làm từng bước.

Tránh: tiện ích/máy chủ MCP không rõ nguồn, công cụ đòi mật khẩu trực tiếp, "tool lậu" lấy dữ liệu Facebook.
Bảng các kết nối phổ biến, quyền nên cấp và cách thêm trong từng nền tảng: `references/ket-noi-pho-bien.md`.

### Bước 3 — Đọc tài liệu hiện hành và lập bản đồ kết nối
- Kiểm tra (nếu có công cụ tìm kiếm web) tài liệu chính thức: quyền (scope), giới hạn số lần gọi, chi phí, chính sách nền tảng, phiên bản API.
- Lập bản đồ đơn giản cho người dùng:
  `Ứng dụng nguồn → Đăng nhập/xác thực → Việc AI làm → Dữ liệu trả về → Nơi lưu/gửi → Nhật ký/lỗi`
- Ví dụ (tiệm bánh Mây — giả định): `Google Sheets "Đơn hàng" → đăng nhập Google (chỉ đọc 1 file) → AI tổng hợp đơn hôm qua → bảng tóm tắt → gửi vào chat → không ghi gì vào Sheets`.

### Bước 4 — Hướng dẫn kết nối qua luồng an toàn
- Kết nối có sẵn: hướng dẫn bấm từng nút (Cài đặt → Kết nối/Connectors/Apps → chọn ứng dụng → Kết nối → đăng nhập trên trang chính thức → xem quyền → Cho phép).
- Máy chủ MCP / API cần khóa: khóa đặt trong **biến môi trường** hoặc kho bí mật của công cụ, **không dán vào chat**.
  - macOS/Linux: `export TEN_BIEN="..."` · Windows PowerShell: `$env:TEN_BIEN="..."` (gõ trong cửa sổ lệnh của chính bạn).
- Cấp **quyền tối thiểu**: chỉ đọc trước; quyền ghi/gửi chỉ thêm khi đã có tiêu chí rõ (Bước 6).
- Tách thử nghiệm và thật khi có thể (file thử, Trang thử, nhóm Telegram thử).

### Bước 5 — Phép thử chỉ đọc
- Liệt kê vài mục nhỏ (3 tệp gần nhất, tên Trang, tên tài khoản quảng cáo, 3 dòng đầu của Sheets).
- Người dùng xác nhận đúng tài khoản.
- Kiểm tra kỹ thuật khi dữ liệu nhiều (AI tự lo, giải thích ngắn): dữ liệu nhiều trang (pagination), chờ quá lâu (timeout),
  thử lại có giới hạn, giới hạn số lần gọi, không tạo bản ghi trùng khi chạy lại (idempotency).

### Bước 6 — Chuyển sang quyền ghi (CỔNG DUYỆT)
Chỉ khi người dùng cần và đồng ý. Trình:
- Quyền thêm là gì, AI sẽ ghi/gửi cái gì, ở đâu, giới hạn bao nhiêu.
- **Thử ghi nhỏ có thể hoàn tác** (1 bản nháp email, 1 dòng thử, 1 tin Telegram thử) → người dùng xem.
- Chờ người dùng gõ **"duyệt"** trước khi bật luồng ghi thật. Gửi/đăng/thay đổi tiền luôn cần cổng duyệt riêng ở skill dùng nó.

### Bước 7 — Sổ kết nối và phương án sự cố
Ghi lại (KHÔNG ghi giá trị bí mật):
| Tên kết nối | Tài khoản (email/tên Trang) | Quyền đã cấp | Ngày kết nối | Hết hạn | Tên biến môi trường (nếu có) | Cách ngắt |
|---|---|---|---|---|---|---|
| Google Sheets | kinhdoanh@… (ví dụ) | Chỉ đọc file "Đơn hàng" | 2026-11-04 | — | — | Cài đặt → Kết nối → Ngắt |

Phương án sự cố: kết nối hết hạn → kết nối lại; nghi lộ khóa → thu hồi ngay, tạo khóa mới; ứng dụng đổi quyền → kiểm tra lại phép thử chỉ đọc.
Nhật ký không chứa token hoặc dữ liệu nhạy cảm. Sao lưu dữ liệu quan trọng trước khi cho AI quyền ghi.

### Checklist chất lượng trước khi giao
- [ ] Đã chọn cách kết nối chính thức, ưu tiên kết nối có sẵn.
- [ ] Không có mật khẩu, OTP, token, khóa API nào xuất hiện trong chat, file hướng dẫn hay Bộ Não.
- [ ] Quyền tối thiểu; phép thử chỉ đọc thành công và đúng tài khoản.
- [ ] Quyền ghi (nếu có) đã thử nhỏ, có thể hoàn tác và được duyệt.
- [ ] Sổ kết nối có tên, quyền, ngày, cách ngắt.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** biết mình muốn AI làm gì với ứng dụng nào; đăng nhập sẵn tài khoản đó trên trình duyệt; với Facebook/quảng cáo,
bạn cần là quản trị viên Trang/tài khoản quảng cáo.

1. Gõ `/ts-ket-noi-ung-dung` kèm 1 câu: "kết nối <ứng dụng> để AI <làm gì>".
2. Trả lời câu hỏi AI (đang dùng Claude hay ChatGPT, tài khoản nào…) — chọn chữ cái nếu có gợi ý.
3. Làm theo từng nút AI chỉ: **Cài đặt → Kết nối / Connectors / Apps → chọn ứng dụng → Kết nối**.
4. Khi trang đăng nhập hiện ra: kiểm tra địa chỉ trang đúng của hãng (google.com, facebook.com…), đăng nhập **ở trang đó**, đọc quyền rồi bấm **Cho phép**.
5. Quay lại chat, gõ "đã kết nối". AI chạy phép thử chỉ đọc — bạn xem có đúng tài khoản của mình không.
6. **Tuyệt đối không dán** mật khẩu, mã OTP, token, khóa API vào chat. AI cần khóa thì sẽ chỉ chỗ dán an toàn.
7. Gõ **"duyệt"** để AI lưu sổ kết nối (chỉ tên, quyền, ngày) vào Bộ Não.
8. Muốn ngắt: Cài đặt → Kết nối → chọn ứng dụng → **Ngắt kết nối**.

## Câu lệnh mẫu
- `/ts-ket-noi-ung-dung kết nối Google Drive để AI đọc Bộ Não Thứ 2 và tài liệu khách hàng của tiệm bánh Mây`
- `/ts-ket-noi-ung-dung tôi muốn AI đọc số liệu quảng cáo Facebook của shop mỹ phẩm mỗi sáng, chỉ đọc thôi`
- `/ts-ket-noi-ung-dung tạo Telegram bot để nhận thông báo khi có học viên đăng ký khóa quay video`
- `/ts-ket-noi-ung-dung spa Hồng có Zalo OA, muốn AI hỗ trợ trả lời khách, nên kết nối kiểu nào?`
- `/ts-ket-noi-ung-dung cài máy chủ MCP của Notion vào Claude Code trên Windows`

## Kết quả nhận được
- Cách kết nối phù hợp nhất (có sẵn / MCP chính thức / phần mềm trung gian / API) và lý do.
- Hướng dẫn bấm từng bước theo nền tảng đang dùng.
- Bản đồ kết nối: nguồn → xác thực → việc làm → dữ liệu → nơi gửi → nhật ký.
- Kết quả phép thử chỉ đọc (và thử ghi nhỏ nếu được duyệt).
- Sổ kết nối (tên, tài khoản, quyền, ngày, cách ngắt) và phương án xử lý sự cố.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-ket-noi-ung-dung-<chu-de-khong-dau>/`.
2. Lưu sổ kết nối và hướng dẫn đã duyệt (tên kết nối, tài khoản hiển thị, quyền, ngày kết nối, ngày hết hạn nếu biết, tên biến môi trường nếu có, cách ngắt, kết quả phép thử) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-ket-noi-ung-dung
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd ket-noi, google-drive, quyen>]
   ---
   ```
   **Tuyệt đối không lưu** mật khẩu, mã OTP, token, khóa API, mã bot, cookie hay giá trị bí mật nào — chỉ ghi tên kết nối, quyền, ngày. Không có file phụ chứa bí mật.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-ket-noi-ung-dung · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Đề xuất thêm 1 dòng vào bảng "Kết nối đang dùng" trong `01-ho-so/05-muc-tieu-quy-tac-lien-he.md` (chỉ tên kết nối, quyền, ngày) để các skill khác biết đã kết nối gì — hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không yêu cầu người dùng dán mật khẩu, OTP hoặc token nhạy cảm vào chat. Nếu người dùng lỡ dán, nhắc họ thu hồi/đổi ngay và không chép lại giá trị đó ở đâu.
- Không bao giờ lưu token/mật khẩu vào Bộ Não, file hướng dẫn, nhật ký.
- Ưu tiên kết nối chính thức; không dùng công cụ không rõ nguồn hoặc vi phạm điều khoản nền tảng.
- Quyền tối thiểu, thử chỉ đọc trước; quyền ghi chỉ khi có tiêu chí rõ và được duyệt.
- Không cấp cho AI quyền chuyển tiền, đổi mật khẩu, đổi quyền quản trị.
- Khi không kết nối được, nói rõ và đưa phương án thay thế (xuất file, ảnh chụp) — không giả vờ đã kết nối.

## Skill liên quan
- Trước: `/ts-cai-dat-bo-nao` · Sau: `/ts-tu-dong-hoa-meta`, `/ts-lap-lich-tu-dong`, `/ts-bao-don-telegram`, `/ts-cham-soc-khach-zalo`, `/ts-bang-tinh-excel`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
