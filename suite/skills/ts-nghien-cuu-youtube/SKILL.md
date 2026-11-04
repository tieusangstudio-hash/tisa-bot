---
name: ts-nghien-cuu-youtube
description: "Gọi bằng /ts-nghien-cuu-youtube. Tìm video YouTube theo chủ đề, lọc theo lượt xem và số người đăng ký kênh, tính chỉ số vượt cỡ (view chia sub), view mỗi ngày, tỉ lệ tương tác; rút ra mẫu tiêu đề thắng, khoảng trống nội dung và 10 ý tưởng video. Dùng trước khi làm video, khi muốn biết chủ đề nào đang hút view. Từ khóa: nghiên cứu YouTube, video nhiều view, video viral, chủ đề hot YouTube, kênh nhỏ view cao, video vượt cỡ, ý tưởng video, tiêu đề YouTube."
---

# /ts-nghien-cuu-youtube — Nghiên cứu video YouTube theo chủ đề

> Lấy số liệu thật từ YouTube (view, số người đăng ký, like, bình luận), tìm ra **video vượt cỡ** — video có view cao hơn hẳn quy mô kênh — rồi rút **mẫu tiêu đề thắng, khoảng trống nội dung và 10 ý tưởng video** cho bạn.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Sắp làm kênh YouTube/video ngắn, muốn biết chủ đề nào đang hút người xem.
- Muốn tìm video của kênh nhỏ mà view rất cao (dễ học theo hơn kênh lớn).
- Cần mẫu tiêu đề đang thắng trong ngành để đặt tên video.
- Muốn tìm khoảng trống: chủ đề người xem hỏi nhiều nhưng ít video làm tốt.
- Lấy số liệu nhu cầu tìm kiếm cho `/ts-kiem-chung-ngach`.

**Không dùng khi:** cần phân tích số liệu kênh của chính bạn → dùng `/ts-phan-tich-mang-xa-hoi`. Cần viết kịch bản chi tiết cho 1 video → dùng `/ts-kich-ban-reels` hoặc `/ts-kich-ban-video-quang-cao`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Chốt chủ đề và bộ lọc (hỏi 1 lượt, có gợi ý)
1. Chủ đề/ngành bạn muốn làm video? → AI đề xuất **3–5 từ khóa** tiếng Việt theo cách người xem hay gõ (vd "cách quay video bằng điện thoại", "quay video bán hàng", "edit video capcut"). Người dùng chọn/sửa.
2. Bạn muốn tìm gì? (A. video nhiều view nhất · B. kênh nhỏ mà view cao — vượt cỡ · C. video mới đang lên nhanh · D. tất cả)
3. Dạng video? (A. video dài · B. video ngắn ≤ 60 giây · C. cả hai)

Bộ lọc gợi ý theo lựa chọn:
| Mục tiêu | Tham số gợi ý |
|---|---|
| A. Nhiều view | `--min-views 50000 --sort views` |
| B. Kênh nhỏ vượt cỡ | `--min-views 10000 --min-subs 500 --max-subs 50000 --sort outlier` |
| C. Mới đang lên | `--days 90 --order date --sort per_day` |

### Bước 2 — Kiểm tra cách lấy dữ liệu
- **Có khóa API** (biến môi trường `YOUTUBE_API_KEY` hoặc học viên tự chạy lệnh): dùng script — số liệu chính xác.
- **Chưa có khóa:** hỏi học viên có muốn lấy khóa miễn phí không (10 phút, hướng dẫn trong `references/lay-api-key.md`). Không muốn → dùng **chế độ ước lượng** (Bước 3B).
- **Không bao giờ xin học viên dán khóa API vào khung chat.** Hướng dẫn họ đặt biến môi trường trên máy hoặc tự chạy lệnh.

### Bước 3A — Chạy script (có khóa API)
```
macOS:    python3 scripts/yt_tim_video.py --q "từ khóa 1" --q "từ khóa 2" --min-views 10000 --max 25 --out ket-qua-youtube.json
Windows:  py scripts\yt_tim_video.py --q "từ khóa 1" --q "từ khóa 2" --min-views 10000 --max 25 --out ket-qua-youtube.json
```
- Mặc định `--region VN --lang vi`. Mỗi từ khóa tốn khoảng 102 đơn vị hạn mức (≈ 90 từ khóa/ngày miễn phí).
- Lọc/xếp lại **không tốn hạn mức** bằng `--tu-file ket-qua-youtube.json` + bộ lọc mới.
- Thử script không cần mạng: `python3 scripts/yt_tim_video.py --tu-file scripts/vi-du-ket-qua.json --min-views 10000` (dữ liệu giả định).
- Các tham số khác: `--min-subs`, `--max-subs`, `--days`, `--order relevance|viewCount|date`, `--sort outlier|views|per_day|engagement`, `--top`.

### Bước 3B — Chế độ ước lượng (không có khóa API)
- Dùng công cụ tìm kiếm/đọc web: tìm từ khóa trên YouTube và Google (`site:youtube.com <từ khóa>`), ghi view, tên kênh, số người đăng ký, ngày đăng nhìn thấy được.
- **Ghi rõ ở đầu bảng: "SỐ LIỆU ƯỚC LƯỢNG từ tìm kiếm web ngày <ngày> — có thể làm tròn hoặc đã cũ."** Không có số thì để trống, không đoán.
- Không có cả công cụ web → hướng dẫn học viên tự tìm 10 video, chụp màn hình hoặc dán link + số view, AI tính chỉ số từ đó.

### Bước 4 — Tính và đọc chỉ số
| Chỉ số | Cách tính | Đọc thế nào |
|---|---|---|
| **Vượt cỡ** | view ÷ số người đăng ký kênh | ≥ 3: vượt cỡ · ≥ 10: rất vượt cỡ — chủ đề/tiêu đề được YouTube đề xuất rộng, không nhờ tệp sẵn có |
| **View/ngày** | view ÷ số ngày từ khi đăng | Cao + video mới → chủ đề đang nóng |
| **Tương tác %** | (like + bình luận) ÷ view × 100 | > 3%: người xem rất quan tâm; bình luận nhiều → nhiều câu hỏi chưa được trả lời |

Lưu ý: kênh ẩn số người đăng ký thì không tính được vượt cỡ. Video rất cũ thì view/ngày thấp dù tổng view cao.

### Bước 5 — Phân tích (AI tự làm từ bảng)
1. **Mẫu tiêu đề thắng** (5–7 mẫu): nhìn top 10 video vượt cỡ, rút ra công thức. Ví dụ dạng: "[Con số] + [cách/sai lầm] + [kết quả cụ thể]", "Tôi thử [việc] trong [thời gian]: kết quả", "[Việc khó] chỉ với [công cụ rẻ]", "Trước và sau khi [hành động]". Mỗi mẫu kèm 1 video minh chứng (link) và lý do nó hút.
2. **Đặc điểm chung của video thắng:** dạng (dài/ngắn), độ dài, thời điểm đăng, kiểu hình thu nhỏ nếu thấy được.
3. **Khoảng trống nội dung** (3–5 điểm): câu hỏi lặp lại trong bình luận, chủ đề nhiều view nhưng video cũ/chất lượng kém, góc chưa ai làm (đối tượng hẹp hơn, khu vực, ngành cụ thể).
4. **10 ý tưởng video**: mỗi ý tưởng có tiêu đề gợi ý (theo mẫu thắng), góc khác biệt, dạng (dài/ngắn), video tham khảo. Đánh dấu 3 ý tưởng nên làm trước.

### Bước 6 — Trình kết quả và chờ duyệt
Trình: bảng top video → mẫu tiêu đề thắng → khoảng trống → 10 ý tưởng. Hỏi: "Bạn muốn lọc lại, thêm từ khóa hay đổi góc? Gõ **duyệt** để lưu."

### Checklist chất lượng
- [ ] Ghi rõ nguồn số liệu (API hay ước lượng) và thời điểm lấy.
- [ ] Không bịa view, số người đăng ký, tiêu đề hay link.
- [ ] Mỗi mẫu tiêu đề có ít nhất 1 video minh chứng.
- [ ] 10 ý tưởng không sao chép nguyên tiêu đề của người khác — chỉ học công thức.
- [ ] Không lộ khóa API trong kết quả hay file lưu.

### Ví dụ minh họa (dữ liệu giả định)
*Ví dụ: chủ đề "quay video bán hàng bằng điện thoại".* Chạy `--tu-file scripts/vi-du-ket-qua.json --min-views 10000`:
- Video "Quay video bán quần áo bằng điện thoại cũ — trước và sau" của kênh 4.500 người đăng ký đạt 95.000 view → **vượt cỡ 21** — chủ đề "trước và sau" + "điện thoại cũ" rất hút.
- Video hướng dẫn đầy đủ của kênh 850.000 người đăng ký có 1,25 triệu view nhưng vượt cỡ chỉ 1,47 → view nhờ tệp sẵn có, khó học theo.
- Mẫu tiêu đề thắng: "Tôi thử [việc] 30 ngày: đây là kết quả" (vượt cỡ 11, tương tác 4%).
- Ý tưởng: "Quay video bán giày bằng điện thoại 3 triệu — trước và sau" (góc ngành giày, chưa ai làm).

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** nghĩ 1 chủ đề bạn muốn làm video; (nên có) khóa YouTube API miễn phí — làm theo `references/lay-api-key.md`, mất khoảng 10 phút, chỉ làm 1 lần.
1. Gõ `/ts-nghien-cuu-youtube` kèm chủ đề.
2. Chọn từ khóa AI đề xuất (hoặc thêm từ khóa của bạn) và chọn mục tiêu A-B-C-D.
3. Nếu có khóa API: đặt biến môi trường trên máy như hướng dẫn (không dán khóa vào chat), để AI chạy script hoặc tự chạy lệnh AI đưa, rồi dán kết quả vào. Chưa có khóa: gõ "dùng ước lượng".
4. Xem bảng. Muốn lọc khác, nói: "chỉ lấy kênh dưới 20 nghìn sub", "chỉ video 3 tháng gần đây".
5. Đọc 10 ý tưởng, chọn 3 cái muốn làm.
6. Gõ **duyệt** để lưu vào Bộ Não.
7. Chuyển sang `/ts-kich-ban-reels` để viết kịch bản cho ý tưởng đã chọn.

## Câu lệnh mẫu
- `/ts-nghien-cuu-youtube chủ đề làm bánh tại nhà — tìm kênh nhỏ dưới 50 nghìn sub mà video trên 100 nghìn view.`
- `/ts-nghien-cuu-youtube chăm sóc da cho nam, chỉ video ngắn đăng trong 3 tháng gần đây.`
- `/ts-nghien-cuu-youtube dạy dùng AI cho người kinh doanh — rút mẫu tiêu đề thắng và 10 ý tưởng video.`
- `/ts-nghien-cuu-youtube lọc lại file ket-qua-youtube.json: chỉ lấy video trên 50 nghìn view, xếp theo view mỗi ngày.`

## Kết quả nhận được
- Bảng top video: tiêu đề (có link), kênh, view, số người đăng ký, chỉ số vượt cỡ, view/ngày, tương tác %, dạng, ngày đăng.
- 5–7 mẫu tiêu đề thắng kèm video minh chứng.
- 3–5 khoảng trống nội dung.
- 10 ý tưởng video (3 ý tưởng ưu tiên).
- File `ket-qua-youtube.json` để lọc lại không tốn hạn mức.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-nghien-cuu-youtube-<chu-de-khong-dau>/`.
2. Lưu bảng top video, mẫu tiêu đề thắng, khoảng trống và 10 ý tưởng video thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-nghien-cuu-youtube
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `ket-qua-youtube.json` (dữ liệu gốc từ script, không chứa khóa API).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-nghien-cuu-youtube · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Mẫu tiêu đề thắng có thể lưu thêm vào `02-kien-thuc/cong-thuc/tieu-de-youtube.md` để các skill viết nội dung dùng lại (hỏi trước khi ghi).
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Khóa API là bí mật:** không xin dán vào chat, không ghi vào kết quả, không lưu vào Bộ Não.
- Số liệu YouTube thay đổi theo giờ — luôn ghi thời điểm lấy. Chế độ ước lượng phải ghi rõ "ước lượng".
- Học công thức, không sao chép nguyên tiêu đề, kịch bản, hình thu nhỏ của người khác (vi phạm bản quyền, dễ bị báo cáo).
- Video vượt cỡ có thể nhờ yếu tố ngoài (người nổi tiếng chia sẻ, chạy quảng cáo) — xem 3–5 video cùng mẫu trước khi kết luận.
- Hạn mức miễn phí 10.000 đơn vị/ngày: dùng `--tu-file` để lọc lại thay vì gọi API lại.

## Skill liên quan
- Trước: `/ts-chan-dung-khach-hang` (biết khách quan tâm gì để chọn từ khóa)
- Sau: `/ts-kich-ban-reels` · `/ts-lich-noi-dung` · `/ts-kiem-chung-ngach`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
