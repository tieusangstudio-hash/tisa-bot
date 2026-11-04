---
name: ts-bao-cao-facebook-ads
description: "Gọi bằng /ts-bao-cao-facebook-ads. Đọc số liệu Facebook/Instagram Ads từ file xuất, ảnh chụp hoặc kết nối; tính lại CPM, CTR, CPC, CPL/CPA, ROAS, tần suất theo chiến dịch/nhóm/quảng cáo; chẩn đoán nguyên nhân và đề xuất GIỮ/THEO DÕI/THỬ MỚI/GIẢM/TẮT. Chỉ đọc, không tự sửa quảng cáo. Dùng khi cần báo cáo ngày/tuần/tháng hoặc hỏi quảng cáo tốt hay xấu. Từ khóa: báo cáo quảng cáo, đọc số ads, chi phí tăng, CPM, CTR, CPC, ROAS, quảng cáo nào nên tắt, creative fatigue."
---

# /ts-bao-cao-facebook-ads — Báo cáo và đọc số Facebook Ads

> Biến bảng số liệu quảng cáo khó hiểu thành báo cáo rõ ràng: chỉ số nào tốt, chỗ nào đang hỏng, nên làm gì tiếp.
> Kết quả: bảng KPI tính lại từ số gốc, top/bottom, cảnh báo, nguyên nhân khả dĩ và 3 hành động ưu tiên.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Có file hoặc ảnh chụp số liệu Ads Manager và muốn biết "tốt hay xấu".
- Chi phí mỗi tin nhắn/đơn hàng tăng đột ngột, chưa rõ lý do.
- Cần báo cáo tuần/tháng gửi sếp, khách hàng hoặc đối tác.
- Muốn biết quảng cáo nào nên giữ, tăng ngân sách, thay hình hay tắt.
- Nghi quảng cáo bị "mỏi" (người xem thấy lặp lại quá nhiều).

**Không dùng khi:** cần dựng/bật chiến dịch mới → `/ts-len-camp-facebook`; cần báo cáo tự động gửi định kỳ →
`/ts-tu-dong-hoa-meta`; số liệu TikTok → `/ts-chay-tiktok-ads`; số liệu không phải quảng cáo → `/ts-doc-so-lieu-hinh-anh`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md` (giá bán, biên lãi để tính ROAS hòa vốn), `05-muc-tieu-quy-tac-lien-he.md` (KPI, CPA/CPL mục tiêu, ngân sách, tài khoản quảng cáo);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `bao-cao-facebook-ads`, `len-camp-facebook`, `viet-quang-cao` hoặc từ khóa) để so với kỳ trước.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Nhận dữ liệu (3 cách)
1. **File xuất từ Ads Manager** (tốt nhất) — CSV hoặc Excel. Hướng dẫn học viên xuất ở phần "Hướng dẫn cho học viên".
2. **Ảnh chụp màn hình** bảng số liệu — đọc từng ô, ghi rõ ô nào mờ/bị cắt, xin ảnh rõ hơn nếu cần.
3. **Kết nối Meta Ads** (nếu môi trường đã kết nối) — chỉ dùng thao tác đọc số liệu (insights), không gọi thao tác sửa.

### Bước 2 — Kiểm tra dữ liệu trước khi tính
Xác nhận và ghi lên đầu báo cáo:
- Khoảng ngày, múi giờ, tiền tệ của tài khoản.
- Cửa sổ ghi nhận (attribution), vd "7 ngày sau khi click, 1 ngày sau khi xem".
- Mục tiêu của từng chiến dịch và **loại kết quả** (tin nhắn, lead, lượt mua…). Không so chi phí/kết quả giữa các chiến dịch khác mục tiêu như thể giống nhau.
- Cấp dữ liệu: chiến dịch / nhóm quảng cáo / quảng cáo; có chia theo ngày không.
- Giữ nguyên dữ liệu gốc; tạo bản chuẩn hóa riêng và ghi rõ trường thiếu, trùng, sai kiểu, lệch đơn vị (vd dấu chấm/phẩy thập phân).

### Bước 3 — Tính lại KPI từ số gốc
Không tin mù quáng cột tổng hợp; tính lại và đối chiếu:

| Chỉ số | Công thức | Ý nghĩa dễ hiểu |
|---|---|---|
| Tần suất | Lượt hiển thị ÷ Người tiếp cận | Mỗi người thấy quảng cáo trung bình mấy lần |
| CPM | Chi tiêu ÷ Lượt hiển thị × 1.000 | Giá để quảng cáo hiện 1.000 lần |
| CTR (liên kết) | Click liên kết ÷ Lượt hiển thị × 100% | Bao nhiêu % người thấy bấm vào |
| CPC (liên kết) | Chi tiêu ÷ Click liên kết | Giá mỗi lần bấm |
| CVR | Kết quả ÷ Click liên kết × 100% | Bao nhiêu % người bấm trở thành kết quả |
| CPL | Chi tiêu ÷ Số khách tiềm năng (lead) | Giá mỗi số điện thoại/form |
| Chi phí/tin nhắn | Chi tiêu ÷ Số cuộc trò chuyện bắt đầu | Giá mỗi khách nhắn tin |
| CPA | Chi tiêu ÷ Số lượt mua (hoặc hành động mục tiêu) | Giá mỗi đơn |
| ROAS | Doanh thu từ quảng cáo ÷ Chi tiêu | 1 đồng quảng cáo ra mấy đồng doanh thu |
| ROAS hòa vốn | 1 ÷ Biên lợi nhuận gộp | vd biên lãi 40% → ROAS hòa vốn = 2,5 |
| Tỉ lệ xem 3 giây (hook) | Lượt phát 3 giây ÷ Lượt hiển thị × 100% | Video có giữ được người xem lúc đầu |
| Tỉ lệ ThruPlay | ThruPlay ÷ Lượt hiển thị × 100% | Bao nhiêu % xem gần hết/≥ 15 giây |

Ví dụ: chi 1.450.000đ, 52.000 lượt hiển thị, 610 click, 38 tin nhắn → CPM = 27.885đ; CTR = 1,17%; CPC = 2.377đ; chi phí/tin nhắn = 38.158đ.

**Có file CSV → chạy script** `scripts/bao_cao_ads.py` (Python 3, không cần cài thêm gì) để tính tự động:
- macOS: `python3 scripts/bao_cao_ads.py duong-dan/file.csv --cpa-muc-tieu 60000`
- Windows: `py scripts\bao_cao_ads.py duong-dan\file.csv --cpa-muc-tieu 60000`
- Tùy chọn: `--cap chien-dich|nhom|quang-cao`, `--tan-suat-canh-bao 3`, `--ra bao-cao.md`, `--xuat-csv chuan-hoa.csv`,
  `--cot "spend=Tên cột chi tiêu"` khi tự nhận diện sai cột. Chạy thử: `assets/mau-xuat-ads-manager.csv` (dữ liệu giả định).
- Script chỉ đọc file, tự bỏ dòng tổng, đối chiếu cột Ads Manager tự tính, tách theo loại kết quả.
- Môi trường không chạy được Python → AI tự tính theo bảng công thức trên và ghi công thức cạnh mỗi số.
- File Excel (.xlsx) → mở bằng công cụ đọc bảng tính đang có, hoặc nhờ học viên lưu lại dạng CSV.

### Bước 4 — So sánh đúng cách
- So với **kỳ trước cùng độ dài**, với **mục tiêu trong hồ sơ** và với **ngưỡng riêng của tài khoản**.
- Không dùng benchmark chung trên mạng như sự thật tuyệt đối; nếu nêu, ghi rõ "tham khảo".
- Không gọi là xu hướng nếu chỉ có 1–2 điểm dữ liệu.

### Bước 5 — Chẩn đoán theo 3 lớp
1. **Phân phối** (CPM, tần suất, tiếp cận): quảng cáo có được hiển thị với giá hợp lý không.
2. **Tương tác** (CTR, tỉ lệ xem 3 giây, ThruPlay): người xem có dừng lại và bấm không.
3. **Chuyển đổi** (CVR, chi phí/kết quả, tỉ lệ chốt): người bấm có thành khách không — gồm trang đích, tin nhắn chào, khâu chốt sale.

Gắn **mức chắc chắn** (Cao / Trung bình / Thấp) cho từng kết luận. Chỉ gọi là nguyên nhân khi có bằng chứng;
còn lại ghi là giả thuyết kèm cách kiểm tra. Cây chẩn đoán nhanh: `references/mau-bao-cao.md`.

### Bước 6 — Đề xuất hành động
Dùng 5 nhãn, mỗi nhãn kèm điều kiện:
- `GIỮ` — đạt mục tiêu, đủ dữ liệu (gợi ý ≥ 10 kết quả). Ứng viên tăng ngân sách từng bước 20–30%.
- `THEO DÕI` — lệch mục tiêu ít hoặc chưa đủ dữ liệu; ghi ngày kiểm tra lại.
- `THỬ MỚI` — tần suất cao, CTR giảm dần → thêm creative/hook mới (dùng `/ts-viet-quang-cao`).
- `GIẢM` — chi phí/kết quả cao hơn mục tiêu rõ rệt khi đã đủ dữ liệu.
- `TẮT` — đã chi ≥ 2 lần chi phí mục tiêu mà 0 kết quả, hoặc vi phạm chính sách.

Xếp hạng hành động theo **tác động × độ tin cậy × rủi ro**. Mỗi đề xuất có ngưỡng theo dõi, điều kiện dừng và thời điểm kiểm tra lại.

### Bước 7 — Viết báo cáo và cổng duyệt
Theo mẫu `references/mau-bao-cao.md`: tóm tắt → bảng KPI → top/bottom → cảnh báo → nguyên nhân khả dĩ → 3 hành động ưu tiên → dữ liệu thiếu.
Trình báo cáo, chờ người dùng gõ **"duyệt"** để lưu. Phân tích là **chế độ đọc**: không tự thay đổi chiến dịch,
ngân sách, attribution hay trạng thái quảng cáo. Người dùng muốn áp dụng → chuyển sang `/ts-len-camp-facebook`
hoặc `/ts-tu-dong-hoa-meta` với xác nhận cụ thể từng đối tượng thay đổi.

### Checklist chất lượng trước khi giao
- [ ] Ghi rõ khoảng ngày, tiền tệ, attribution, cấp dữ liệu.
- [ ] Mọi KPI tính lại từ số gốc, có công thức; tổng đã đối chiếu.
- [ ] Không so chi phí/kết quả giữa các loại kết quả khác nhau.
- [ ] Mỗi kết luận có mức chắc chắn; giả thuyết tách khỏi dữ kiện.
- [ ] Đúng 3 hành động ưu tiên, mỗi cái có điều kiện dừng và ngày kiểm tra lại.

## Hướng dẫn cho học viên (làm theo từng bước)
**Cách xuất file từ Trình quản lý quảng cáo (Ads Manager)** — tên nút có thể khác chút theo phiên bản:
1. Vào Trình quản lý quảng cáo trên máy tính, chọn đúng tài khoản quảng cáo ở góc trên bên trái.
2. Chọn khoảng ngày ở góc trên bên phải (vd "7 ngày qua").
3. Chọn tab cấp muốn xem: **Chiến dịch**, **Nhóm quảng cáo** hoặc **Quảng cáo**.
4. Bấm **Cột** → chọn **Hiệu quả và lượt click** (hoặc tùy chỉnh thêm: Người tiếp cận, Tần suất, CPM, Lượt click vào liên kết, Kết quả, Chi phí trên mỗi kết quả, Lượt phát video 3 giây, ThruPlay, Giá trị chuyển đổi lượt mua nếu bán web).
5. Bấm **Báo cáo** (hoặc biểu tượng mũi tên tải xuống) → **Xuất dữ liệu bảng** → chọn **.csv** → **Xuất**.
6. Gửi file cho AI. Không xuất được thì chụp màn hình bảng, rõ chữ, thấy cả dòng tiêu đề cột.

**Sau đó:**
1. Gõ `/ts-bao-cao-facebook-ads` và đính kèm file/ảnh, kèm 1 câu: "báo cáo tuần này, mục tiêu tin nhắn dưới 50k".
2. Trả lời câu hỏi AI (mục tiêu chi phí, giá bán, biên lãi nếu muốn tính ROAS hòa vốn).
3. Đọc phần **Tóm tắt** và **3 hành động ưu tiên** trước; phần bảng để tra cứu.
4. Hỏi lại chỗ chưa hiểu: "CPM là gì", "vì sao đề xuất tắt quảng cáo này".
5. Gõ **"duyệt"** để AI lưu báo cáo vào Bộ Não (lần sau AI tự so với kỳ này).
6. Tự vào Ads Manager thực hiện thay đổi đã chọn, hoặc nhờ AI làm qua `/ts-tu-dong-hoa-meta` (cần xác nhận từng thay đổi).

## Câu lệnh mẫu
- `/ts-bao-cao-facebook-ads đọc file tuần này của shop mỹ phẩm, mục tiêu đơn hàng, CPA mong muốn 80k [đính kèm CSV]`
- `/ts-bao-cao-facebook-ads ảnh chụp số liệu tiệm bánh Mây, chạy tin nhắn, sao tuần này chi phí/tin nhắn tăng gấp đôi?`
- `/ts-bao-cao-facebook-ads báo cáo tháng 11 cho khóa học quay video bằng điện thoại, so với tháng 10, gửi sếp`
- `/ts-bao-cao-facebook-ads dịch vụ sửa điều hòa chạy lead, quảng cáo nào nên tắt, quảng cáo nào nên tăng tiền?`

## Kết quả nhận được
- Báo cáo Markdown: tóm tắt, bảng KPI (có công thức), top/bottom, cảnh báo, chẩn đoán 3 lớp, 3 hành động ưu tiên, dữ liệu thiếu.
- Nhãn GIỮ / THEO DÕI / THỬ MỚI / GIẢM / TẮT cho từng chiến dịch/nhóm/quảng cáo kèm độ tin cậy.
- (Nếu có CSV) Bản dữ liệu chuẩn hóa riêng, file gốc giữ nguyên.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-bao-cao-facebook-ads-<chu-de-khong-dau>/`.
2. Lưu báo cáo quảng cáo đã duyệt (phạm vi dữ liệu, bảng KPI, chẩn đoán, hành động) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-bao-cao-facebook-ads
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd facebook-ads, bao-cao, tuan-45>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `du-lieu-goc.csv` (bản sao file người dùng gửi), `du-lieu-chuan-hoa.csv`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-bao-cao-facebook-ads · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu chi phí/kết quả thực tế ổn định khác KPI trong `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`, đề xuất cập nhật KPI; bài học creative thắng/thua đề xuất ghi vào `02-kien-thuc/cong-thuc/quang-cao-da-test.md` — hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Skill này chỉ ĐỌC. Không chỉnh attribution, ngân sách hoặc trạng thái quảng cáo nếu chưa có kết nối hợp lệ và xác nhận đúng đối tượng thay đổi.
- Không bịa số liệu; ô không đọc được ghi `[CẦN BỔ SUNG]` hoặc xin ảnh rõ hơn.
- Không dùng benchmark chung như sự thật; ngưỡng đề xuất là gợi ý, chỉnh theo tài khoản.
- Số liệu Ads Manager có thể thay đổi vài ngày sau (dữ liệu về muộn); ghi ngày lấy số.
- Không xin mật khẩu, mã đăng nhập, token trong chat.

## Skill liên quan
- Trước: `/ts-len-camp-facebook`, `/ts-viet-quang-cao` · Sau: `/ts-viet-quang-cao` (làm creative mới), `/ts-tu-dong-hoa-meta` (báo cáo định kỳ), `/ts-bang-tinh-excel`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
