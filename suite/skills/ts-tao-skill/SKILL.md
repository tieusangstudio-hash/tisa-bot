---
name: ts-tao-skill
description: "Gọi bằng /ts-tao-skill. Giúp người không rành công nghệ tự có một lệnh /ts- mới theo nhu cầu riêng: hỏi đúng 5 câu có gợi ý A-B-C-D, đề xuất thêm tính năng, trình bản thiết kế để duyệt, rồi tạo thư mục skill chuẩn (SKILL.md, openai.yaml, icon), thử 3 tình huống và hướng dẫn cài. Dùng khi muốn AI tự động hóa một việc lặp lại mà 52 lệnh có sẵn chưa làm. Từ khóa: tạo skill, làm skill mới, lệnh riêng, tự động hóa việc lặp lại, skill theo ý muốn, skill creator, sửa skill."
---

# /ts-tao-skill — Tạo skill theo ý muốn

> Bạn mô tả việc muốn AI làm giúp, AI hỏi 5 câu dễ hiểu, vẽ bản thiết kế cho bạn duyệt, rồi tạo một
> lệnh mới `/ts-<tên>` đúng chuẩn bộ skill TISA AI Agent — kèm hướng dẫn cài và câu lệnh mẫu.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Có một việc lặp đi lặp lại muốn AI làm theo đúng cách của mình (vd báo giá, trả lời bình luận, viết mô tả sản phẩm).
- 52 lệnh `/ts-...` có sẵn chưa có lệnh phù hợp, hoặc muốn một phiên bản riêng cho ngành của mình.
- Muốn sửa/nâng cấp một skill tự tạo trước đây.
- Muốn đóng gói quy trình của nhân viên thành lệnh để cả đội dùng chung.

**Không dùng khi:** việc đã có lệnh làm được → dùng thẳng lệnh đó (xem `/ts-dieu-phoi-cong-viec`).
Muốn làm cả một ứng dụng/web → `/ts-tao-app`. Muốn đặt lịch tự chạy → `/ts-lap-lich-tu-dong`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md` (để ví dụ và câu lệnh mẫu trong skill mới sát ngành của người dùng);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `tao-skill` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Quy tắc quan trọng
- **Dùng công cụ tạo skill có sẵn của nền tảng nếu có** (vd skill tên `skill-creator` hoặc tính năng
  "tạo skill" của ứng dụng). Đọc toàn bộ hướng dẫn của công cụ đó trước khi tạo tệp, rồi áp thêm
  quy chuẩn bộ TISA trong `references/khung-skill-chuan.md`. Không có → tự tạo theo khung đó.
- **Quy chuẩn:** đọc `references/khung-skill-chuan.md`. Nếu đang làm trong repo bộ skill và có tệp
  `tools/SKILL-SPEC.md` thì đọc tệp đó (quy chuẩn đầy đủ, ưu tiên cao hơn), và nhắc học viên mở xem.
- Hỏi đúng 5 câu trong `references/bo-cau-hoi-5-cau.md`. Có thể hỏi từng câu hoặc gộp, nhưng giữ gợi ý
  A–D và lựa chọn tự mô tả.
- Giải thích thuật ngữ bằng tiếng Việt đơn giản. Không bắt người dùng biết tên công nghệ.
- **Không tạo hay cài skill trước khi người dùng duyệt bản thiết kế.**

### Bước 1 — Kiểm tra trước
- Đọc tài liệu/tệp người dùng đã đưa để không hỏi lại.
- Đối chiếu 52 lệnh có sẵn (danh mục ở `/ts-dieu-phoi-cong-viec`): nếu đã có lệnh làm được ≥ 80% việc,
  nói rõ và hỏi: dùng lệnh có sẵn, hay vẫn tạo lệnh riêng (vd bản rút gọn cho ngành mình).

### Bước 2 — Hỏi 5 câu
1. Skill giúp làm việc gì? · 2. Nhận đầu vào gì? · 3. Trả ra gì? · 4. Hỏi và duyệt thế nào? ·
5. Dùng cho ai, thành công đo bằng gì?

Câu trả lời mơ hồ → diễn giải thành yêu cầu cụ thể, đánh dấu `[GIẢ ĐỊNH]`. Dùng bảng "Cách diễn giải
câu trả lời" trong `references/bo-cau-hoi-5-cau.md` để quyết định loại Bộ Não, cổng duyệt, có cần script không.

### Bước 3 — Đề xuất thêm 3–5 tính năng
Sáng tạo thêm tính năng hữu ích (vd "lưu mẫu báo giá vào Bộ Não để lần sau dùng lại", "xuất thêm bản
ngắn cho Zalo"). Tách rõ hai cột: **Bạn yêu cầu** · **AI đề xuất thêm** (người dùng chọn giữ/bỏ).

### Bước 4 — Trình bản thiết kế (blueprint) để duyệt
```text
TÊN LỆNH: /ts-<ten-khong-dau>          (VD: /ts-bao-gia-nhanh)
MỤC TIÊU: …
KÍCH HOẠT KHI: … (từ khóa người dùng hay nói)
LOẠI BỘ NÃO: ĐỌC + LƯU (đọc tệp: …) / CHỈ LƯU
ĐẦU VÀO: …
LUỒNG TỪNG BƯỚC: 1… 2… 3…
ĐẦU RA: … (định dạng, tên tệp)
CÔNG CỤ CẦN: … (nếu có: tạo ảnh, đọc web, kết nối …)
CỔNG XÁC NHẬN: … (bước nào phải chờ "duyệt")
GIỚI HẠN: … (không làm gì)
3 CÂU LỆNH MẪU: …
👉 Gõ "duyệt" để AI tạo skill, hoặc sửa bằng lời.
```
Tên lệnh: `ts-` + tiếng Việt không dấu, chữ thường, nối gạch ngang, 2–5 từ, không trùng 52 lệnh có sẵn.

### Bước 5 — Tạo skill (sau khi duyệt)
Tạo thư mục `ts-<ten>/` theo `references/khung-skill-chuan.md`:
- `SKILL.md`: frontmatter chỉ có `name` + `description` (≤ 600 ký tự, bắt đầu "Gọi bằng /ts-<ten>."),
  thân bài đủ các mục theo đúng thứ tự, có khối Bộ Não (ĐỌC hoặc CHỈ LƯU) và khối LƯU.
- `agents/openai.yaml` theo mẫu (display_name `TS · …`, short_description ≤ 60 ký tự).
- `assets/icon.svg`: chép biểu tượng của chính skill này (`assets/icon.svg`).
- `references/`, `scripts/`, `templates/` chỉ khi thật cần; tài nguyên tối thiểu.
- Không đưa mật khẩu, token, ID tài khoản thật hay thông tin doanh nghiệp ghi cứng vào skill — skill mới
  phải đọc thông tin đó từ Bộ Não của người dùng.

### Bước 6 — Kiểm tra và thử 3 tình huống
- Chạy checklist ở mục 8 của `references/khung-skill-chuan.md` (tên khớp thư mục, description ≤ 600 ký tự,
  đủ mục, đường dẫn tương đối có thật, script biên dịch được).
- Thử 3 tình huống: chuẩn · thiếu dữ liệu · rủi ro (xem cuối `references/bo-cau-hoi-5-cau.md`).
  Sửa lỗi rồi thử lại. Báo bảng kết quả thử cho người dùng.

### Bước 7 — Cài đặt
Dùng cách cài chính thức của nền tảng đang dùng. Không cài tự động được → giao thư mục (hoặc file zip)
hoàn chỉnh và hướng dẫn:

| Nền tảng | Cách cài skill tự tạo |
|---|---|
| Claude (app / web / Cowork) | Nén thư mục `ts-<ten>` thành zip → *Customize* → *Skills* → tải lên file zip |
| Claude Code | Chép thư mục vào `~/.claude/skills/` (Windows: `%USERPROFILE%\.claude\skills\`) rồi mở lại phiên |
| ChatGPT / Codex | Chép vào `~/.codex/skills/` (Windows: `%USERPROFILE%\.codex\skills\`), hoặc tải zip lên mục *Skills* của ChatGPT |
| Google Antigravity | Chép vào `~/.gemini/config/skills/` (Windows: `%USERPROFILE%\.gemini\config\skills\`) |

Tên mục trong giao diện có thể thay đổi theo phiên bản ứng dụng — nếu khác, hướng dẫn theo giao diện
người dùng đang thấy. Không tuyên bố "đã cài" khi chưa kiểm tra lệnh gọi được. Cần tài khoản/kết nối
ngoài → xin phép riêng, không yêu cầu mật khẩu/OTP/token trong chat.

### Bước 8 — Bàn giao
Hướng dẫn ngắn: cách gọi `/ts-<ten>`, dữ liệu nên chuẩn bị, 3 câu lệnh mẫu, các điểm cần xác nhận, cách
sửa skill sau này (gọi lại `/ts-tao-skill sửa skill ts-<ten>: …`).

### Checklist chất lượng
- [ ] Đúng 5 câu hỏi, có gợi ý A–D; giả định được đánh dấu.
- [ ] Blueprint được duyệt trước khi tạo tệp.
- [ ] Tên `ts-...` không dấu, không trùng lệnh có sẵn; `name` = tên thư mục.
- [ ] SKILL.md đúng bố cục chuẩn, có khối Bộ Não và khối LƯU, ≥ 3 câu lệnh mẫu.
- [ ] Đã thử 3 tình huống và ghi kết quả.
- [ ] Không có bí mật, không thông tin doanh nghiệp ghi cứng.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** nghĩ 1 việc cụ thể bạn hay làm đi làm lại (vd "mỗi lần khách hỏi giá, tôi phải tính
và gõ báo giá"). Nếu có, chuẩn bị 1–2 mẫu kết quả bạn thấy đạt (ảnh chụp, tệp, đoạn văn).

1. Gõ `/ts-tao-skill` kèm 1 câu mô tả việc muốn tự động.
2. Trả lời 5 câu hỏi — chọn chữ cái A–D hoặc tự mô tả.
3. Xem các tính năng AI đề xuất thêm, nói giữ hoặc bỏ.
4. Đọc bản thiết kế (tên lệnh, các bước, đầu ra), sửa bằng lời nếu cần, rồi gõ "duyệt".
5. Xem kết quả AI tự thử 3 tình huống.
6. Làm theo hướng dẫn cài (AI chỉ đúng nút cần bấm cho ứng dụng bạn đang dùng).
7. Gõ thử `/ts-<tên-mới>` với câu lệnh mẫu AI đưa. Chưa ưng → `/ts-tao-skill sửa skill ts-<tên>: …`.
8. Nếu đang dùng repo bộ skill: mở `tools/SKILL-SPEC.md` để xem quy chuẩn đầy đủ.

## Câu lệnh mẫu
- `/ts-tao-skill tôi bán nội thất, muốn lệnh tự báo giá khi khách gửi kích thước phòng`
- `/ts-tao-skill spa của tôi cần lệnh viết tin nhắc lịch hẹn và chăm sóc sau liệu trình`
- `/ts-tao-skill tôi dạy tiếng Anh online, muốn lệnh chấm bài viết của học viên theo thang điểm của tôi`
- `/ts-tao-skill shop quần áo cần lệnh viết mô tả sản phẩm từ ảnh chụp, đăng Shopee`
- `/ts-tao-skill sửa skill ts-bao-gia-nhanh: thêm phí vận chuyển theo tỉnh`

## Kết quả nhận được
- Bản thiết kế skill đã duyệt.
- Thư mục `ts-<ten>/` hoàn chỉnh (SKILL.md, agents/openai.yaml, assets/icon.svg, tệp phụ nếu cần) hoặc file zip.
- Bảng kết quả thử 3 tình huống.
- Hướng dẫn cài theo nền tảng + 3 câu lệnh mẫu.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-tao-skill-<ten-skill-moi>/`.
2. Lưu bản thiết kế đã duyệt + bảng thử 3 tình huống + hướng dẫn cài thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-tao-skill
   ngay: <YYYY-MM-DD>
   chu-de: <tên skill mới — việc nó làm>
   the: [skill, tu-dong-hoa, <lĩnh vực>]
   ---
   ```
   Kèm theo các file phụ (nếu có): bản sao thư mục `ts-<ten>/` hoặc file `ts-<ten>.zip` để cài lại khi đổi máy.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Skill /ts-<ten>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-tao-skill · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu skill mới là quy trình riêng của doanh nghiệp (vd cách báo giá), đề xuất lưu tóm tắt quy trình vào
   `02-kien-thuc/cong-thuc/<ten-khong-dau>.md` — hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không tạo skill giúp người chưa thành niên tiếp cận hàng hóa/dịch vụ hạn chế độ tuổi, hoạt động nguy hiểm,
  nội dung tình dục, hoặc cách né cơ chế bảo vệ.
- Không tạo skill thu thập mật khẩu, OTP, token, số thẻ hay dữ liệu nhạy cảm không cần thiết.
- Skill có hành động bên ngoài (đăng, gửi, chi tiền, xóa) bắt buộc có cổng "duyệt".
- Không tuyên bố đã cài khi chưa kiểm tra.

## Skill liên quan
- Trước: `/ts-dieu-phoi-cong-viec` (kiểm tra đã có lệnh phù hợp chưa)
- Sau: `/ts-ket-noi-ung-dung` (nếu skill mới cần kết nối) · `/ts-lap-lich-tu-dong` (cho skill chạy định kỳ)

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
