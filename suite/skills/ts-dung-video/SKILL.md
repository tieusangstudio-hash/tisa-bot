---
name: ts-dung-video
description: "Gọi bằng /ts-dung-video. Dựng video ngắn chuyên nghiệp ngay trên máy (không cần khóa API): nhận dạng lời nói tiếng Việt, cắt khoảng lặng và từ đệm, caption bám lời, đồ họa và zoom có chủ đích, 7 nhóm phong cách; dựng video người nói (talking-head) hoặc cảnh quay sản phẩm có hook; kiểm tra chất lượng và sửa bằng câu nói tự nhiên. Không tự thêm nhạc nền. Dùng khi cần dựng reel, video TikTok/Facebook, thêm caption, sửa chữ, đổi phong cách. Từ khóa: dựng video, edit video tự động, cắt khoảng lặng, thêm phụ đề, caption video, làm reel, video người nói, b-roll."
---

# /ts-dung-video — Dựng video tự động

> Đưa video quay sẵn, AI dựng thành reel hoàn chỉnh ngay trên máy của bạn: cắt khoảng lặng, caption tiếng Việt
> bám lời, đồ họa – zoom đúng lúc, đúng phong cách bạn chọn. Muốn sửa chỉ cần nói ("sửa caption giây 12", "bớt đồ họa").

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Có video người nói trước máy quay (chia sẻ, bán hàng, dạy học) cần cắt gọn, thêm caption, đồ họa.
- Có cảnh quay sản phẩm/không gian (b-roll) cần thêm tiêu đề thu hút, dòng phụ và CTA.
- Video đã dựng cần sửa caption, đổi màu/phong cách, giảm/tăng đồ họa, bỏ nhạc.
- Muốn dựng nhiều video cùng một phong cách nhất quán.

**Không dùng khi:** chưa có video, muốn tạo video bằng AI từ kịch bản → `/ts-prompt-video-ai`.
Chưa có kịch bản để quay → `/ts-kich-ban-reels` hoặc `/ts-kich-ban-video-quang-cao`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

(Nếu có Bộ Não và tệp `02-kien-thuc/cong-thuc/phong-cach-dung-video.md` — phong cách người dùng đã chọn các
lần trước — đọc để đề xuất phong cách quen thuộc lên đầu.)

## Quy trình AI thực hiện

Chuỗi xử lý: `video gốc → nhận dạng lời nói → cắt khoảng lặng → EDL (bản kế hoạch dựng) → Remotion (bộ dựng) → video hoàn chỉnh`

**Thư mục chứa `SKILL.md` này là thư mục gốc của bộ dựng.** Chạy mọi lệnh với thư mục làm việc tại đây.
Lệnh Python: macOS/Linux dùng `python3`, Windows dùng `python` (hoặc `py`). Các ví dụ bên dưới ghi `python`;
trên macOS thay bằng `python3`.

### Nguyên tắc bắt buộc
1. Giữ nguyên video gốc; luôn làm việc trên bản sao trong `public/raw/`.
2. Số lượng đồ họa là **giới hạn tối đa**, không phải chỉ tiêu phải lấp đầy.
3. Caption sạch, dễ đọc trên điện thoại; đồ họa phải làm rõ ý, tạo nhịp hoặc hướng mắt.
4. **Không tự dùng nhạc nền.** Chỉ thêm nhạc khi người dùng chủ động yêu cầu và cung cấp tệp có quyền sử dụng.
5. Không ghi đè bản EDL đã chỉnh tay hoặc tệp đầu ra đã đặt tên khi chưa được xác nhận.
6. Chỉ cài thư viện, mở ứng dụng hoặc xử lý tệp ngoài thư mục dự án sau khi giải thích và được người dùng đồng ý.
7. Không mặc định gọi công cụ AI bên ngoài hay yêu cầu khóa API.

### Tài nguyên trong skill
- `scripts/doctor.py` — kiểm tra Python, Node.js, FFmpeg và thư viện.
- `scripts/run-pipeline.py` — dựng video người nói.
- `scripts/run-broll-pipeline.py` — dựng b-roll kèm hook.
- `scripts/generate-edl.py` — tạo EDL từ transcript (dùng ở chế độ `prefed`).
- `scripts/validate-edl-risk.py` — kiểm tra EDL trước khi render.
- `scripts/render-remotion-chunks.ps1` — render chia đoạn trên Windows (máy yếu, video dài).
- `references/style-menu.md` — 7 nhóm phong cách dựng.
- `references/workflow-talking-head.md` — quy trình video người nói.
- `references/workflow-broll-hook.md` — quy trình b-roll + hook.
- `references/edl-reasoning-talking-head.md` — cách phân tích transcript và lập kế hoạch dựng (4 lượt).
- `references/host-plan-schema.md` — cấu trúc tệp `out/host-plan.json`.
- `references/graphic-catalog.md` — danh mục 26 loại đồ họa và trường dữ liệu bắt buộc.
- `goldens/` — 7 ảnh tham chiếu cho 7 nhóm phong cách.
- `public/sfx/` — hiệu ứng âm thanh ngắn (không phải nhạc nền).

### Bước 1 — Nhận video và xác định nhu cầu
Nhận tệp người dùng đính kèm hoặc đường dẫn tệp trên máy. Chưa có tệp → hướng dẫn sao chép đường dẫn
(Windows: chuột phải tệp → *Copy as path*; macOS: chọn tệp → giữ Option → chuột phải → *Sao chép … dưới dạng tên
đường dẫn*), hoặc hỗ trợ tìm video khi công cụ cho phép.

Loại video chưa rõ → hỏi một câu:
1. **Người nói (talking-head):** người nói trước máy quay; cần cắt khoảng lặng, caption, đồ họa, zoom.
2. **B-roll + hook:** cảnh quay sản phẩm/không gian; cần tiêu đề thu hút, dòng phụ và CTA.

Xác nhận thêm nếu chưa có: nền tảng và tỷ lệ (9:16, 16:9, 1:1) · mục tiêu video và người xem · có giữ âm thanh gốc
không · **không nhạc nền** hay dùng tệp nhạc người dùng cung cấp.

### Bước 2 — Chọn phong cách (cổng duyệt 1)
Đọc `references/style-menu.md`, xem ảnh trong `goldens/` khi cần đối chiếu. Đề xuất **tối đa 3 phong cách** hợp
chủ đề + 1 lựa chọn "AI chọn giúp". Mỗi lựa chọn mô tả dễ hiểu: màu sắc, độ mạnh của chữ, cảm giác đầu ra.
Không hiển thị mã theme kỹ thuật trừ khi người dùng yêu cầu. 👉 Chờ người dùng chọn.

### Bước 3 — Kiểm tra môi trường (lần đầu)
Báo trước rồi chạy:
```bash
python scripts/doctor.py
```
Thiếu thành phần → trình danh sách cần cài và **xin xác nhận trước khi cài**:
```bash
pip install -r requirements.txt
npm install
```
(macOS: `python3 -m pip install -r requirements.txt`.) FFmpeg: Windows `winget install Gyan.FFmpeg` · macOS
`brew install ffmpeg`. Yêu cầu tối thiểu: Python 3.10+, Node.js 18+, FFmpeg và FFprobe. Lần chạy đầu sẽ tự tải
mô hình nhận dạng giọng nói (~460 MB) — báo người dùng chờ.

### Bước 4 — Dựng video
**Video người nói:** đọc `references/workflow-talking-head.md` và `references/edl-reasoning-talking-head.md`.
Ưu tiên chế độ `prefed`: chạy bước tạo transcript/face-zone (`--llm offline`), AI tự phân tích nội dung theo 4 lượt,
viết `out/host-plan.json` (theo `references/host-plan-schema.md`), tạo EDL bằng `scripts/generate-edl.py --llm prefed`,
kiểm tra rủi ro rồi render. Có thể dùng `offline` khi cần phương án cục bộ hoàn toàn.
Đường dẫn clip luôn **tương đối với `public/`** (vd `raw/video.mp4`).

**B-roll + hook:** đọc `references/workflow-broll-hook.md`. Người dùng chỉ đưa chủ đề → đề xuất **3 bộ**:
hook chính tối đa 2 dòng · dòng phụ đồng cảm · CTA ngắn rõ. 👉 Chỉ render sau khi người dùng chọn nội dung.
Không có nhạc → âm thanh gốc của b-roll mặc định bị tắt; muốn giữ tiếng gốc nhỏ thì thêm `--keep-clip-audio`.

### Bước 5 — Kiểm tra trước và sau render
Trước render:
```bash
python scripts/validate-edl-risk.py out/edl.json
```
Sau render:
1. Hook trong 3 giây đầu.
2. Caption khớp transcript (đúng dấu tiếng Việt).
3. Đồ họa đúng thời điểm, không che mặt.
4. Chữ đọc được trên màn hình điện thoại.
5. CTA và âm thanh (không có nhạc nền nếu người dùng không yêu cầu).
6. Trả đường dẫn `out/final.mp4`, thời gian xử lý và 3 lựa chọn tiếp theo.

### Chỉnh sửa bằng câu nói tự nhiên
| Người dùng nói | Cách xử lý |
|---|---|
| "Sửa caption ở giây X" | Tìm caption đúng thời điểm, xác nhận chữ cũ/mới, sửa EDL rồi render lại. |
| "Bớt đồ họa" | Bỏ các đồ họa ít giá trị nhất, giữ các điểm nhấn quan trọng. |
| "Đổi màu/phong cách" | Chọn theme mới, sửa khối style trong EDL rồi render lại. |
| "Bỏ nhạc nền" | Xóa/tắt khối music, giữ thoại và hiệu ứng âm thanh phù hợp. |
| "Làm lại từ đầu" | Cảnh báo chỉnh sửa tay có thể mất; chỉ dùng `--force-regen` sau khi xác nhận. |
| "Giữ bản này" | Sao chép video cuối sang tên riêng, không để dự án tiếp theo ghi đè. |

Chỉnh nhỏ: sửa trực tiếp `out/edl.json` rồi chạy `npm run render:edl`. Không chạy lại toàn bộ pipeline nếu hướng
dựng không đổi lớn.

### Mẫu phản hồi sau render
Luôn trả đủ: (1) đường dẫn video hoàn chỉnh · (2) thời gian đã xử lý · (3) lựa chọn tiếp theo: sửa caption, màu,
đồ họa hoặc âm thanh / chốt và lưu bản hiện tại / gửi video tiếp theo.

### Lệnh nhanh
```bash
python scripts/doctor.py
python scripts/run-pipeline.py raw/video.mp4 --llm offline --render
npm run studio:edl
npm run render:edl
python scripts/validate-edl-risk.py out/edl.json
```
(macOS thay `python` bằng `python3`.)

### Checklist chất lượng
- [ ] Video gốc không bị sửa; đầu ra ở `out/final.mp4` (hoặc tên riêng khi "giữ bản này").
- [ ] Theme đúng phong cách người dùng chọn (`strategy.theme` trong `out/edit-plan.json`).
- [ ] `validate-edl-risk.py` không báo lỗi đỏ.
- [ ] Caption đúng chính tả tiếng Việt; chữ trên màn hình không dùng gạch dài (—, –).
- [ ] Đồ họa có lý do (làm rõ ý / tạo nhịp / hướng mắt), không lặp 3 loại giống nhau liền nhau.
- [ ] Không có nhạc nền khi người dùng không yêu cầu.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** máy tính (Windows hoặc macOS) còn trống ≥ 5 GB; video quay dọc rõ tiếng; lần đầu cần cài Python,
Node.js, FFmpeg — AI sẽ kiểm tra và hướng dẫn từng bước. Dùng AI có quyền chạy lệnh trên máy (vd Claude Code,
Codex, Cowork, Antigravity).

1. Gõ `/ts-dung-video` và đính kèm video (hoặc dán đường dẫn tệp trên máy).
2. Trả lời: video người nói hay cảnh quay sản phẩm; đăng ở đâu; có giữ tiếng gốc không.
3. Chọn 1 trong 3 phong cách AI đề xuất (hoặc "AI chọn giúp").
4. Lần đầu: đồng ý cho AI kiểm tra và cài thành phần còn thiếu (AI hỏi trước khi cài).
5. Chờ AI dựng (video 1 phút thường mất vài phút, máy yếu lâu hơn).
6. Xem `out/final.mp4`; sửa bằng lời: "sửa caption giây 12 thành …", "bớt đồ họa", "đổi màu xanh".
7. Ưng rồi thì nói "giữ bản này" và "duyệt" để lưu vào Bộ Não.

## Câu lệnh mẫu
- `/ts-dung-video dựng video này thành reel TikTok, tôi nói về 3 mẹo chọn bánh kem, phong cách vui tươi` (kèm video)
- `/ts-dung-video video chia sẻ kiến thức kế toán 2 phút, cắt khoảng lặng, caption, phong cách chuyên gia tối giản`
- `/ts-dung-video cảnh quay spa, thêm hook "3 Bước Chăm Da|Sau 30 Tuổi" và CTA "Nhắn tin nhận lịch hẹn"`
- `/ts-dung-video sửa caption ở giây 15 thành "chỉ 199 nghìn" rồi xuất lại`
- `/ts-dung-video kiểm tra máy tôi đã đủ phần mềm để dựng video chưa`

## Kết quả nhận được
- Video hoàn chỉnh `out/final.mp4` (hoặc tên riêng người dùng đặt).
- Thời gian xử lý và tóm tắt những gì đã dựng (số đoạn cắt, số đồ họa, phong cách).
- Tệp `out/edl.json` để chỉnh tiếp bằng lời.
- 3 lựa chọn bước tiếp theo.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-dung-video-<chu-de-khong-dau>/`.
2. Lưu tóm tắt bản dựng (tệp gốc, loại video, phong cách/theme, thời lượng trước–sau khi cắt, số đồ họa, hook/CTA, các lần sửa) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-dung-video
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề video>
   the: [video, dung-video, <phong cách>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `edl.json` (để dựng lại), video cuối nếu người dùng muốn lưu trong Bộ Não
   (video nặng → chỉ ghi đường dẫn tệp trên máy).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Video <chủ đề>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-dung-video · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Hỏi người dùng có muốn ghi nhớ phong cách vừa chọn không; đồng ý → cập nhật
   `02-kien-thuc/cong-thuc/phong-cach-dung-video.md` (nhóm phong cách, theme, góp ý đã sửa, ngày) để lần sau đề xuất lên đầu.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không sửa, xóa video gốc của người dùng.
- Không cài phần mềm, không xử lý tệp ngoài thư mục dự án khi chưa được đồng ý.
- Không tự thêm nhạc nền; nhạc do người dùng cung cấp phải có quyền sử dụng.
- Video có người khác xuất hiện: nhắc người dùng đảm bảo đã được đồng ý dùng hình ảnh.
- Bộ dựng chạy cục bộ, không gửi video lên dịch vụ ngoài.

## Skill liên quan
- Trước: `/ts-kich-ban-reels` · `/ts-kich-ban-video-quang-cao` · `/ts-prompt-video-ai` (ghép các đoạn video AI)
- Sau: `/ts-noi-dung-tu-dong-7-ngay` · `/ts-len-camp-facebook` · `/ts-chay-tiktok-ads`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
