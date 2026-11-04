# Khung skill chuẩn /ts-... (rút gọn từ quy chuẩn bộ skill)

Nếu đang làm việc trong repo bộ skill và có tệp `tools/SKILL-SPEC.md`, **đọc tệp đó trước** — đó là
quy chuẩn đầy đủ, ưu tiên hơn bản rút gọn này.

## 1. Tên & thư mục

- Tên: `ts-<ten-tieng-viet-khong-dau>` — chữ thường, nối gạch ngang, 2–5 từ, nói rõ công dụng.
  Ví dụ tốt: `ts-bao-gia-nhanh`, `ts-tra-loi-binh-luan`, `ts-nhac-lich-hen-spa`.
  Ví dụ chưa tốt: `ts-tool1`, `ts-skill-moi`, `ts-ai-marketing-pro-max`.
- Không trùng 52 lệnh có sẵn (xem danh sách ở `/ts-dieu-phoi-cong-viec`). Trùng → đổi tên hoặc
  đề xuất dùng lệnh có sẵn.
- Cấu trúc thư mục:

```
ts-<ten>/
├── SKILL.md                 bắt buộc
├── agents/openai.yaml       cho ChatGPT/Codex
├── assets/icon.svg          biểu tượng
├── references/              (tùy chọn) tài liệu chi tiết, bộ câu hỏi, mẫu
├── scripts/                 (tùy chọn) script Python 3 / Node 18, không cần cài thêm thư viện nếu được
└── templates/               (tùy chọn) mẫu đầu ra
```

## 2. Frontmatter — CHỈ 2 trường

```yaml
---
name: ts-<ten>
description: "Gọi bằng /ts-<ten>. <Làm gì — 1 câu>. Dùng khi <tình huống>. Từ khóa: <5–10 cụm từ người dùng hay nói>."
---
```

- `description` tiếng Việt có dấu, **≤ 600 ký tự**, bọc nháy kép, một dòng, bên trong không dùng `"` (dùng `'`).
- `name` phải trùng tên thư mục.

## 3. `agents/openai.yaml`

```yaml
interface:
  display_name: "TS · <Tên tiếng Việt ngắn>"
  short_description: "<≤ 60 ký tự>"
  default_prompt: "Dùng $ts-<ten> để <việc mẫu>."
  icon_small: assets/icon.svg
  icon_large: assets/icon.svg
policy:
  products: [chatgpt, codex, api, atlas]
  allow_implicit_invocation: true
```

## 4. Bố cục SKILL.md (đúng thứ tự)

```markdown
# /ts-<ten> — <Tên tiếng Việt đầy đủ>

> <1–2 câu: skill này giúp gì, ra kết quả gì.>

**Loại Bộ Não:** ĐỌC + LƯU   ← hoặc: CHỈ LƯU

## Khi nào dùng
- … (3–6 gạch)
**Không dùng khi:** … → dùng `/ts-…` thay thế.

## Bước 0 — Đọc Bộ Não Thứ 2
(khối ĐỌC — mục 5 bên dưới)

## Quy trình AI thực hiện
### Bước 1 — …
### Bước 2 — …
(chi tiết, có cổng duyệt khi cần, có checklist chất lượng)

## Hướng dẫn cho học viên (làm theo từng bước)
1. …  (4–8 bước, kèm việc cần chuẩn bị trước)

## Câu lệnh mẫu
- `/ts-<ten> …` (ít nhất 3 ví dụ, đa dạng ngành)

## Kết quả nhận được
- …

## Bước cuối — Lưu vào Bộ Não Thứ 2
(khối LƯU — mục 6 bên dưới)

## Lưu ý & an toàn
- …

## Skill liên quan
- Trước: `/ts-…` · Sau: `/ts-…`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
```

Độ dài gợi ý 120–300 dòng. Chi tiết dài đưa vào `references/` và dẫn đường dẫn tương đối
(`references/...`). Không trỏ sang skill khác bằng `../`; muốn nhắc skill khác thì ghi lệnh `/ts-...`.

## 5. Khối ĐỌC Bộ Não (chọn 1)

**Loại ĐỌC + LƯU** (skill cần hiểu doanh nghiệp):

```markdown
## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: <liệt kê đúng các tệp skill này cần>;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `<ma-skill>` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.
```

**Loại CHỈ LƯU** (skill kỹ thuật, không cần hồ sơ):

```markdown
## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.
```

5 tệp hồ sơ có thể chọn: `01-ho-so-doanh-nghiep.md` · `02-san-pham-dich-vu.md` ·
`03-khach-hang-muc-tieu.md` · `04-thuong-hieu-noi-dung.md` (giọng văn, màu, logo, nhân vật đại diện) ·
`05-muc-tieu-quy-tac-lien-he.md` (mục tiêu, KPI, ngân sách, kênh, liên hệ, ID tài khoản quảng cáo).

## 6. Khối LƯU Bộ Não (mọi skill)

```markdown
## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-<ma-skill>-<chu-de-khong-dau>/`.
2. Lưu <mô tả file chính> thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-<ten>
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): <liệt kê>.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-<ten> · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. <Tri thức dùng lại lâu dài nếu có — hỏi trước khi ghi đè hồ sơ.>
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).
```

`<ma-skill>` = tên skill bỏ tiền tố `ts-`.

## 7. Nguyên tắc nội dung

- Viết cho người **không rành công nghệ**: câu ngắn, tiếng Việt có dấu, thuật ngữ khó phải giải thích trong ngoặc.
- Chạy được trên Claude, ChatGPT/Codex, Google Antigravity: viết trung tính ("nếu môi trường có công cụ
  tạo ảnh", "nếu đã kết nối Meta Ads"), không nhắc tên công cụ nội bộ của một nền tảng.
- Lệnh terminal (nếu có) ghi cả macOS và Windows.
- Không ghi cứng thông tin của một doanh nghiệp cụ thể (ID tài khoản, số điện thoại, địa chỉ) —
  lấy từ hồ sơ của người dùng trong Bộ Não. Ví dụ minh họa dùng doanh nghiệp giả định, ghi rõ "ví dụ".
- An toàn: tốn tiền / công khai / gửi tin / xóa / bật quảng cáo → luôn trình bản nháp, chờ "duyệt".
  Không xin mật khẩu, OTP, token, số thẻ. Không bịa số liệu, feedback — thiếu ghi `[CẦN BỔ SUNG: …]`.

## 8. Kiểm tra trước khi bàn giao

- [ ] `name` = tên thư mục, bắt đầu `ts-`; frontmatter đúng YAML, chỉ 2 trường.
- [ ] `description` ≤ 600 ký tự, có "Gọi bằng /ts-…", tình huống dùng, từ khóa.
- [ ] SKILL.md đủ các mục theo đúng thứ tự ở mục 4; có ≥ 3 câu lệnh mẫu.
- [ ] Có khối Bộ Não (ĐỌC hoặc CHỈ LƯU) và khối LƯU.
- [ ] Mọi đường dẫn tệp kèm theo là tương đối và tệp có thật.
- [ ] Script (nếu có) chạy được: `python3 -m py_compile scripts/*.py` (Windows: `py -m py_compile scripts\<ten>.py`).
- [ ] Không có mật khẩu, token, thông tin doanh nghiệp ghi cứng.
- [ ] Đã thử với 3 tình huống đại diện (xem `references/bo-cau-hoi-5-cau.md` mục thử nghiệm).
