---
name: ts-cai-dat-bo-nao
description: "Gọi bằng /ts-cai-dat-bo-nao. Bước ĐẦU TIÊN khi cài bộ skill TISA AI Agent: hướng dẫn tạo thư mục 'Bộ Não Thứ 2 - Tên Của Bạn', kết nối thư mục vào AI, tạo cấu trúc chuẩn mở được bằng Obsidian. Dùng khi mới cài bộ skill, chưa có Bộ Não, đổi máy, hoặc Bộ Não bị thiếu thư mục. Từ khóa: bộ não thứ 2, second brain, cài đặt, bắt đầu, kết nối thư mục, obsidian, tạo folder."
---

# /ts-cai-dat-bo-nao — Cài đặt Bộ Não Thứ 2

> Tạo "trí nhớ dài hạn" cho AI: một thư mục trên máy của bạn chứa hồ sơ doanh nghiệp, kiến thức và kết quả
> làm việc. Từ đó mọi lệnh `/ts-...` tự đọc thông tin trước khi làm và tự lưu kết quả sau khi làm.

**Loại Bộ Não:** TẠO BỘ NÃO (chạy đầu tiên, trước mọi lệnh khác)

## Khi nào dùng
- Vừa cài bộ skill TISA AI Agent lần đầu.
- AI báo "Bạn chưa kết nối Bộ Não Thứ 2".
- Đổi máy tính, hoặc muốn tạo Bộ Não riêng cho một thương hiệu khác.
- Bộ Não cũ bị thiếu thư mục/tệp (skill sẽ bổ sung, không ghi đè).

**Không dùng khi:** đã có Bộ Não và chỉ muốn điền hồ sơ → dùng `/ts-tao-ho-so-doanh-nghiep`.

## Bước 0 — Kiểm tra Bộ Não hiện có

1. Tìm trong thư mục đang làm việc và các folder đã kết nối: thư mục có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có tệp `00-DOC-TRUOC.md` ở gốc.
2. Nếu đã có: báo "Đã tìm thấy Bộ Não tại …", kiểm tra còn thiếu thư mục/tệp nào so với cấu trúc chuẩn
   (mục *Cấu trúc chuẩn* bên dưới) → chuyển thẳng tới **Bước 4** để bổ sung phần thiếu, rồi **Bước 6**.
3. Nếu chưa có: đi lần lượt từ **Bước 1**.

## Quy trình AI thực hiện

### Bước 1 — Hỏi 2 câu (gộp 1 lần)
1. "Bạn muốn đặt tên Bộ Não theo tên ai hoặc thương hiệu nào?" (vd *Lan*, *Tiệm Bánh Mây*)
2. "Bạn đang dùng AI ở đâu?"
   A. Claude (app máy tính / Cowork / Claude Code) · B. ChatGPT hoặc Codex · C. Google Antigravity ·
   D. Chỉ dùng trên trình duyệt web

### Bước 2 — Hướng dẫn tạo thư mục (người dùng tự làm, AI chỉ từng bước)
Tên thư mục **chính xác**: `Bộ Não Thứ 2 - <Tên>` (vd `Bộ Não Thứ 2 - Lan`).

Chọn ổ đĩa **còn trống ít nhất 2 GB**:
- **Windows:** mở *File Explorer* → *This PC* → xem ổ nào còn nhiều dung lượng (thường là ổ `D:`).
  Vào ổ đó → chuột phải vào chỗ trống → *New* → *Folder* → gõ tên → Enter.
- **macOS:** menu Apple → *Cài đặt hệ thống* → *Cài đặt chung* → *Dung lượng* để xem dung lượng trống.
  Mở *Finder* → *Tài liệu (Documents)* → chuột phải → *Thư mục mới* → gõ tên → Enter.
- Không đặt trong thư mục tạm, thùng rác hay ổ USB hay rút ra. Đặt trong Google Drive / OneDrive / iCloud
  được (để đồng bộ nhiều máy), nhưng chọn "luôn giữ trên máy này".

Hỏi người dùng gửi lại **đường dẫn đầy đủ** của thư mục (Windows: bấm vào thanh địa chỉ của File Explorer
→ copy; macOS: chọn thư mục → giữ phím Option → chuột phải → *Sao chép … dưới dạng tên đường dẫn*).

### Bước 3 — Kết nối thư mục vào AI (theo câu trả lời ở Bước 1)

| Nền tảng | Cách kết nối |
|---|---|
| **Claude Desktop (Chat / Cowork)** | Bấm nút **+** cạnh ô nhập tin nhắn → **Add folder** (hoặc chọn thư mục khi tạo Cowork task / Project) → chọn thư mục Bộ Não. |
| **Claude Code** | Mở Terminal tại thư mục: `cd "<đường dẫn>"` rồi gõ `claude`. Hoặc trong phiên đang mở gõ `/add-dir "<đường dẫn>"`. |
| **Codex (CLI / app)** | `cd "<đường dẫn>"` rồi gõ `codex`; trên app Codex chọn mở thư mục này làm workspace. |
| **Google Antigravity** | *File* → *Open Folder* → chọn thư mục Bộ Não. Các lệnh `/ts-...` có sẵn trong `.agent/workflows/`. |
| **Chỉ dùng web (claude.ai / ChatGPT web)** | Web chưa đọc/ghi thẳng thư mục trên máy. AI tạo file zip Bộ Não để bạn tải về và giải nén vào thư mục đã tạo. Khi cần AI đọc hồ sơ, đính kèm các tệp trong `01-ho-so/`; khi AI giao kết quả, tải về bỏ vào `04-ket-qua/`. Nên chuyển sang app máy tính để tự động hoàn toàn. |

Sau khi người dùng báo đã kết nối, AI thử liệt kê nội dung thư mục để xác nhận đọc/ghi được.

### Bước 4 — Tạo cấu trúc chuẩn
Cách 1 (ưu tiên) — chạy script đi kèm skill, **không bao giờ ghi đè tệp có sẵn**:
- macOS / Linux: `python3 scripts/tao_bo_nao.py "<đường dẫn>" --ten "<Tên>"`
- Windows: `py scripts\tao_bo_nao.py "<đường dẫn>" --ten "<Tên>"`

Cách 2 — nếu không chạy được lệnh: dùng công cụ ghi file đang có, tạo từng tệp/thư mục theo mẫu trong
`assets/bo-nao-mau/` (thay `{{TEN}}` bằng tên, `{{NGAY}}` bằng ngày hôm nay dạng YYYY-MM-DD).

Cách 3 — chỉ có web: `python3 scripts/tao_bo_nao.py --zip "Bo-Nao-Thu-2-<Ten>.zip" --ten "<Tên>"` rồi
giao file zip cho người dùng tải về, hướng dẫn giải nén vào ổ còn trống.

Kiểm tra lại: đủ các mục trong *Cấu trúc chuẩn*, tệp `00-DOC-TRUOC.md` có đúng tên chủ sở hữu.

### Bước 5 — Cài Obsidian để xem Bộ Não
1. Vào **obsidian.md** → *Download* → cài như phần mềm bình thường (miễn phí).
2. Mở Obsidian → **Open folder as vault** → chọn thư mục `Bộ Não Thứ 2 - <Tên>`.
3. Nếu hỏi *Trust author and enable plugins?* → chọn **Trust**.
4. Mở **00-DOC-TRUOC** và **muc-luc** (đã ghim sẵn ở mục Bookmarks bên trái).
5. Bấm biểu tượng **Graph view** (hình mạng nhện) để xem sơ đồ liên kết. Thư mục `06-mau/` đã được cài làm
   thư mục mẫu: *Ctrl/Cmd + P* → *Templates: Insert template*.

### Bước 6 — Bước tiếp theo
Đề xuất ngay: "Chạy `/ts-tao-ho-so-doanh-nghiep` (20–30 phút) để AI hiểu doanh nghiệp của bạn. Sau đó mọi
lệnh khác sẽ dùng hồ sơ này." Nếu người dùng chưa biết bắt đầu từ đâu: gợi ý `/ts-dieu-phoi-cong-viec`.

## Cấu trúc chuẩn

```
Bộ Não Thứ 2 - <Tên>/
├── 00-DOC-TRUOC.md      quy tắc chung cho AI và người
├── CLAUDE.md · AGENTS.md · GEMINI.md   lời nhắc tự động cho từng nền tảng AI
├── muc-luc.md           mục lục
├── nhat-ky.md           nhật ký mỗi lần chạy lệnh
├── 01-ho-so/            5 tệp hồ sơ doanh nghiệp
│   ├── 01-ho-so-doanh-nghiep.md
│   ├── 02-san-pham-dich-vu.md
│   ├── 03-khach-hang-muc-tieu.md
│   ├── 04-thuong-hieu-noi-dung.md
│   └── 05-muc-tieu-quy-tac-lien-he.md
├── 02-kien-thuc/        khach-hang/ · san-pham/ · doi-thu/ · cong-thuc/
├── 03-tai-lieu-tho/     tài liệu gốc (AI chỉ đọc) · dinh-kem/
├── 04-ket-qua/          mỗi lần chạy lệnh = 1 thư mục <ngày>-<lệnh>-<chủ-đề>
├── 05-du-an/            theo dõi dự án, khóa học, chiến dịch
├── 06-mau/              mẫu ghi chú cho Obsidian
├── 99-luu-tru/          tài liệu cũ
├── .obsidian/           cấu hình sẵn cho Obsidian
└── .agent/workflows/    lệnh /ts-... cho Google Antigravity
```

## Hướng dẫn cho học viên (làm theo từng bước)
1. Gõ `/ts-cai-dat-bo-nao` (hoặc nói "cài Bộ Não Thứ 2 cho tôi").
2. Trả lời 2 câu: tên Bộ Não và bạn đang dùng AI ở đâu.
3. Tạo thư mục `Bộ Não Thứ 2 - <Tên Của Bạn>` ở ổ còn trống theo hướng dẫn, gửi đường dẫn cho AI.
4. Kết nối thư mục vào AI theo bảng ở Bước 3 (ví dụ Claude Desktop: nút **+** → **Add folder**).
5. Chờ AI tạo cấu trúc, xem danh sách tệp AI báo đã tạo.
6. Cài Obsidian, mở thư mục làm vault, xem thử `00-DOC-TRUOC`.
7. Chạy tiếp `/ts-tao-ho-so-doanh-nghiep`.

## Câu lệnh mẫu
- `/ts-cai-dat-bo-nao tên tôi là Lan, tôi dùng Claude trên máy Windows`
- `/ts-cai-dat-bo-nao tạo Bộ Não cho thương hiệu Tiệm Bánh Mây, tôi dùng Antigravity trên Mac`
- `/ts-cai-dat-bo-nao tôi chỉ dùng ChatGPT trên web, làm file zip giúp tôi`
- `/ts-cai-dat-bo-nao kiểm tra Bộ Não của tôi còn thiếu gì`

## Kết quả nhận được
- Thư mục Bộ Não đầy đủ cấu trúc, mở được bằng Obsidian.
- 5 tệp hồ sơ mẫu chờ điền, mục lục, nhật ký, mẫu ghi chú.
- Lệnh `/ts-...` dùng được trong Antigravity khi mở thư mục này.

## Bước cuối — Lưu vào Bộ Não Thứ 2
1. Đảm bảo `nhat-ky.md` có dòng đầu tiên: `- <YYYY-MM-DD> · /ts-cai-dat-bo-nao · Tạo Bộ Não Thứ 2 · ./`
   (script đã tự ghi; nếu bổ sung Bộ Não cũ thì thêm dòng `… · Bổ sung cấu trúc · ./`).
2. Không tạo thư mục trong `04-ket-qua/` cho lệnh này.
3. Báo người dùng: đường dẫn Bộ Não, số tệp đã tạo, số tệp đã có sẵn được giữ nguyên.

## Lưu ý & an toàn
- Không bao giờ xóa hoặc ghi đè tệp đã có trong Bộ Não.
- Không lưu mật khẩu, OTP, token, khóa API, số thẻ vào Bộ Não.
- Nếu người dùng có nhiều thương hiệu: mỗi thương hiệu một Bộ Não riêng, kết nối đúng thư mục khi làm việc.
- Sao lưu: khuyên người dùng đặt Bộ Não trong Google Drive/OneDrive hoặc định kỳ nén thư mục lưu ra ổ khác.

## Skill liên quan
- Sau: `/ts-tao-ho-so-doanh-nghiep` → `/ts-dieu-phoi-cong-viec`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
