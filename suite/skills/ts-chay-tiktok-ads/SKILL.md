---
name: ts-chay-tiktok-ads
description: "Gọi bằng /ts-chay-tiktok-ads. Lập kế hoạch và hướng dẫn chạy TikTok Ads: chọn mục tiêu, cấu trúc Chiến dịch → Nhóm quảng cáo → Quảng cáo, Spark Ads và mã ủy quyền video, Pixel, ngân sách test, KPI và quy tắc giữ/tắt/tăng; đọc số liệu để tối ưu. Chỉ tạo/bật/sửa khi có kết nối và được duyệt. Dùng khi muốn chạy TikTok Ads, test video, tối ưu chi phí. Từ khóa: chạy tiktok ads, quảng cáo tiktok, spark ads, mã ủy quyền video, tiktok pixel, test video tiktok, CPA tiktok, tỉ lệ xem 2 giây."
---

# /ts-chay-tiktok-ads — Chạy quảng cáo TikTok

> Giúp bạn lên chiến dịch TikTok Ads có cấu trúc rõ, test nhiều video đúng cách và đọc số để quyết định giữ, tắt hay tăng.
> Kết quả: bảng thiết lập chiến dịch để duyệt, kế hoạch video test, ngân sách gợi ý, KPI và quy tắc tối ưu.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Lần đầu chạy TikTok Ads, chưa biết bắt đầu từ đâu.
- Có video TikTok tự nhiên đang tốt, muốn đẩy bằng Spark Ads.
- Muốn test nhiều video/hook để tìm mẫu ra đơn rẻ.
- Chi phí mỗi đơn/tin nhắn tăng, cần đọc số để tối ưu.
- Cần báo cáo quảng cáo TikTok theo tuần.

**Không dùng khi:** chỉ cần viết nội dung/hook quảng cáo → `/ts-viet-quang-cao`; cần kịch bản quay video →
`/ts-kich-ban-reels` hoặc `/ts-kich-ban-video-quang-cao`; chạy Facebook/Instagram → `/ts-len-camp-facebook`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md` (KPI, ngân sách, tài khoản quảng cáo, link đích);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `chay-tiktok-ads`, `viet-quang-cao` hoặc từ khóa) để biết video/angle nào đã test.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Chốt mục tiêu và tài nguyên
Hỏi phần còn thiếu (gợi ý A-B-C-D):
- Muốn khách làm gì? (A) Mua trên website · (B) Để lại thông tin (lead) · (C) Nhắn tin/ghé trang cá nhân · (D) Mua trên TikTok Shop.
- Đích đến: link website/landing page, form, trang TikTok, cửa hàng TikTok Shop.
- Sự kiện chuyển đổi đo bằng gì: đã cài TikTok Pixel chưa? Có Events API (gửi dữ liệu từ máy chủ) không?
- Có bao nhiêu video sẵn? Ai quay? Mỗi tuần làm thêm được mấy video?
- Ngân sách/ngày và chi phí mỗi kết quả chấp nhận được (CPA mục tiêu).

### Bước 2 — Kiểm tra tài khoản và đo lường
- Tài khoản TikTok Ads Manager đã xác minh, có phương thức thanh toán, đúng múi giờ và tiền tệ (đổi sau rất khó).
- Pixel: vào **Công cụ → Quản lý sự kiện** (Events Manager), kiểm tra Pixel có nhận sự kiện (Xem nội dung, Thêm vào giỏ, Gửi biểu mẫu, Hoàn tất thanh toán…).
- Gắn UTM vào link đích (vd `?utm_source=tiktok&utm_medium=paid&utm_campaign=<ten>`) để đối chiếu với số liệu website.
- Cửa sổ ghi nhận (attribution) mặc định có thể khác Facebook → khi so hai nền tảng phải ghi rõ.
- Ngành nhạy cảm (sức khỏe, làm đẹp, tài chính, giảm cân…) → đọc chính sách quảng cáo TikTok hiện hành trước khi làm video.

### Bước 3 — Cấu trúc Chiến dịch → Nhóm quảng cáo → Quảng cáo
| Cấp | Chọn gì ở cấp này | Ví dụ (tiệm bánh Mây — giả định) |
|---|---|---|
| **Chiến dịch** (Campaign) | Mục tiêu, ngân sách tổng (tùy chọn) | Mục tiêu "Chuyển đổi trên trang web" |
| **Nhóm quảng cáo** (Ad Group) | Đối tượng, vị trí, ngân sách/ngày, lịch, sự kiện tối ưu, cách trả giá | Nữ 22–40, TP.HCM, tối ưu "Hoàn tất thanh toán" |
| **Quảng cáo** (Ad) | Video, chữ quảng cáo, nút CTA, link | 3 video khác hook, cùng link landing page |

Nhóm mục tiêu chính (tên có thể đổi theo phiên bản): **Nhận biết** (Phạm vi tiếp cận) · **Cân nhắc** (Lưu lượng truy cập,
Lượt xem video, Tương tác cộng đồng, Tìm kiếm khách tiềm năng) · **Chuyển đổi** (Chuyển đổi trang web, Bán sản phẩm).

Tách 3 loại chiến dịch:
- **Prospecting** (tìm khách mới): đối tượng rộng, để thuật toán tự tìm; ưu tiên nhiều video hơn là chia đối tượng nhỏ.
- **Retargeting** (bám đuổi): người đã xem video ≥ 6 giây, ghé web, tương tác trang trong 7–30 ngày.
- **Spark Ads**: đẩy chính bài đăng TikTok tự nhiên (xem Bước 4).

Quy tắc đặt tên để truy vết: `<Nền tảng>_<Mục tiêu>_<Sản phẩm>_<Vòng test>_<Ngày>`
vd `TT_ChuyenDoi_BanhSinhNhat_V1_2026-11` · Nhóm: `Rong_Nu22-40_HCM` · Quảng cáo: `V1_Hook-CauHoi_Creator-Chu`.

### Bước 4 — Spark Ads và mã ủy quyền video
**Spark Ads là gì:** quảng cáo dùng chính bài đăng trên một tài khoản TikTok (của bạn hoặc của KOC/creator).
Lượt thích, bình luận, theo dõi được tính cho bài gốc; quảng cáo trông tự nhiên như video thường.

**Cách lấy mã ủy quyền** (người sở hữu video làm trên ứng dụng TikTok; tên mục có thể đổi theo phiên bản):
1. Vào **Hồ sơ → ☰ (menu) → Cài đặt và quyền riêng tư → Công cụ dành cho nhà sáng tạo / Công cụ doanh nghiệp → Cài đặt quảng cáo**, bật **Ủy quyền quảng cáo**.
2. Mở video muốn đẩy → bấm **… (thêm)** hoặc **Chia sẻ** → **Cài đặt quảng cáo**.
3. Bật **Ủy quyền quảng cáo**, chọn thời hạn (vd 7, 30, 60 ngày… tùy lựa chọn hiện có) → **Tạo mã** → **Sao chép**.
4. Gửi mã cho người chạy quảng cáo qua kênh riêng (không đăng công khai).
5. Trong TikTok Ads Manager: **Tài sản → Sáng tạo → Bài đăng TikTok → Đăng ký ủy quyền** (hoặc chọn "Dùng tài khoản TikTok" khi tạo quảng cáo) → dán mã → xác nhận.

Lưu ý: chỉ dùng video của creator khi có thỏa thuận (thời hạn, phí, phạm vi); hết hạn mã thì quảng cáo dừng.
Không tải lại video người khác khi chưa có quyền.

### Bước 5 — Kế hoạch 3–5 video test
Ưu tiên video "native" (giống video TikTok thường, quay dọc 9:16, người thật, nói tự nhiên), rõ sản phẩm trong 3 giây đầu, CTA rõ.
Ma trận gợi ý: **hook × angle × phong cách người nói × CTA**, mỗi video khác ít nhất hook hoặc angle.

| Video | Hook (2 giây đầu) | Angle | Người nói | CTA | Giả thuyết |
|---|---|---|---|---|---|
| V1 | "Bánh kem 250k mà đẹp vầy?" | Kết quả | Chủ tiệm | Bấm đặt bánh | Giá + hình đẹp giữ người xem |
| V2 | Cảnh cắt bánh chậm | Cơ chế | Không lời, chữ trên màn hình | Xem menu | Hình ảnh đủ hút |
| V3 | "3 lỗi khi đặt bánh online" | Phản đối | Nhân viên | Nhắn tin tư vấn | Gỡ lo ngại tăng tỉ lệ chuyển đổi |

Cần viết hook/angle → `/ts-viet-quang-cao`; cần kịch bản quay → `/ts-kich-ban-reels`.

### Bước 6 — Ngân sách test, thời gian, KPI, điều kiện dừng/tăng
**Ngân sách (GỢI Ý — kiểm chứng lại trong Ads Manager, mức tối thiểu và giai đoạn học có thể thay đổi):**
- TikTok có mức ngân sách tối thiểu cho chiến dịch và nhóm quảng cáo, tính theo tiền tệ của tài khoản — xem ngay khi nhập ngân sách.
- Khi tối ưu chuyển đổi, ngân sách/ngày mỗi nhóm nên khoảng **5–10 lần CPA mục tiêu** để có đủ sự kiện cho thuật toán học
  (TikTok thường cần khoảng vài chục chuyển đổi/tuần mỗi nhóm để ổn định — kiểm chứng con số hiện hành).
- Ngân sách nhỏ → dùng ít nhóm, nhiều video trong một nhóm; hoặc tối ưu sự kiện sớm hơn (vd "Thêm vào giỏ") rồi chuyển dần.
- Chạy tối thiểu 3–5 ngày trước khi kết luận; không sửa nhóm quảng cáo liên tục (mỗi lần sửa lớn có thể làm học lại).

**Chỉ số cần xem (AI tính lại từ số gốc):**
| Chỉ số | Công thức | Cho biết điều gì |
|---|---|---|
| CPM | Chi phí ÷ Lượt hiển thị × 1.000 | Giá để được hiển thị; cao → đối tượng hẹp/cạnh tranh |
| Tỉ lệ xem 2 giây | Lượt xem 2 giây ÷ Lượt hiển thị × 100% | Hook có giữ người xem không |
| Tỉ lệ xem 6 giây | Lượt xem 6 giây ÷ Lượt hiển thị × 100% | Nội dung đầu có đủ hấp dẫn không |
| Thời gian xem trung bình, % xem hết | Có sẵn trong báo cáo | Video có giữ đến đoạn CTA không |
| CTR | Lượt click ÷ Lượt hiển thị × 100% | Lời mời và CTA có thuyết phục không |
| CPC | Chi phí ÷ Lượt click | Giá mỗi click |
| CVR | Chuyển đổi ÷ Lượt click × 100% | Trang đích/khâu chốt có tốt không |
| CPA | Chi phí ÷ Số chuyển đổi | Chỉ số quyết định chính |
| ROAS | Doanh thu ÷ Chi phí | Có lãi không (cần giá trị đơn) |

**Quy tắc quyết định (gợi ý, chỉnh theo tài khoản):**
- **GIỮ / TĂNG**: CPA ≤ mục tiêu sau ≥ 3 ngày và ≥ 10 chuyển đổi → tăng ngân sách từng bước (vd 20–30% mỗi 2–3 ngày) hoặc nhân bản sang nhóm mới.
- **THEO DÕI**: CPA cao hơn mục tiêu ≤ 30% hoặc chưa đủ dữ liệu.
- **THỬ MỚI**: tỉ lệ xem 2 giây thấp → đổi hook; xem tốt nhưng CTR thấp → đổi CTA/offer; CTR tốt nhưng CVR thấp → xem lại trang đích.
- **TẮT**: chi ≥ 2 lần CPA mục tiêu mà 0 chuyển đổi, hoặc CPA > 1,5 lần mục tiêu sau khi đủ dữ liệu.
- **Mỏi quảng cáo (fatigue)**: CTR/tỉ lệ xem giảm liên tục, CPM tăng, tần suất tăng → lên lịch thay video mới mỗi 7–14 ngày (tùy ngân sách).

Không tắt vội chỉ vì biến động 1 ngày.

### Bước 7 — Bảng thiết lập để duyệt (CỔNG DUYỆT)
Trình bảng gồm: tài khoản quảng cáo (lấy từ hồ sơ), tên chiến dịch, mục tiêu, nhóm quảng cáo (đối tượng, vị trí,
ngân sách/ngày, lịch chạy, sự kiện tối ưu), danh sách quảng cáo (video, chữ, CTA, link + UTM), ngày bắt đầu/kết thúc,
tổng chi tối đa dự kiến. Chờ người dùng gõ **"duyệt"**.
- Có kết nối TikTok Ads và đã duyệt → tạo ở trạng thái **tạm dừng** trước, cho người dùng xem lại, rồi mới bật khi được xác nhận lần nữa.
- Không có kết nối → hướng dẫn học viên bấm từng bước trong Ads Manager theo bảng.
- Mọi thay đổi ngân sách, bật/tắt sau này đều cần xác nhận cụ thể: tài khoản nào, chiến dịch nào, số tiền bao nhiêu.

### Checklist chất lượng trước khi giao
- [ ] Mục tiêu chiến dịch khớp điều muốn khách làm; sự kiện tối ưu đo được bằng Pixel.
- [ ] Mỗi vòng test có giả thuyết, KPI chính, ngân sách, thời hạn, tiêu chí đủ dữ liệu.
- [ ] Tên chiến dịch/nhóm/quảng cáo theo quy tắc, truy vết được vòng test.
- [ ] Link có UTM; video có quyền sử dụng; Spark Ads có mã ủy quyền còn hạn.
- [ ] Ngân sách ghi rõ là gợi ý; không hứa trước kết quả.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** tài khoản TikTok Ads Manager (đăng ký tại trang quảng cáo của TikTok, xác minh doanh nghiệp, thêm
thanh toán); 3–5 video dọc 9:16; link đích; ngân sách/ngày; CPA mong muốn. Muốn dùng Spark Ads thì chuẩn bị mã ủy quyền (Bước 4).

1. Gõ `/ts-chay-tiktok-ads` kèm 1 câu: bán gì, muốn khách làm gì, ngân sách bao nhiêu/ngày.
2. Trả lời các câu hỏi AI đưa ra (gợi ý A-B-C-D thì chọn chữ cái).
3. Nếu chưa có Pixel, làm theo hướng dẫn AI đưa ra hoặc nhờ người làm web gắn giúp (AI soạn sẵn tin nhắn gửi họ).
4. Xem bảng thiết lập. Sửa bằng lời: "giảm ngân sách còn 300k/ngày", "chỉ chạy TP.HCM", "thêm 1 video".
5. Gõ **"duyệt"**. Nếu chưa kết nối, mở TikTok Ads Manager → **Tạo** → làm theo bảng từng ô; chụp màn hình gửi AI kiểm tra trước khi bấm **Gửi**.
6. Sau 3 ngày: vào **Báo cáo**, xuất file (CSV/Excel) hoặc chụp màn hình bảng số liệu, gửi lại bằng `/ts-chay-tiktok-ads đọc số tuần này`.
7. Làm theo đề xuất GIỮ / THEO DÕI / THỬ MỚI / TẮT — mỗi thay đổi tiền đều tự bạn xác nhận.

## Câu lệnh mẫu
- `/ts-chay-tiktok-ads lên chiến dịch cho shop phụ kiện điện thoại bán trên website, ngân sách 500k/ngày, CPA mong muốn 60k`
- `/ts-chay-tiktok-ads tôi có video TikTok của tiệm bánh Mây đang 50k view, hướng dẫn chạy Spark Ads`
- `/ts-chay-tiktok-ads chạy thu lead cho khóa học quay video bằng điện thoại, chưa có Pixel, chỉ có form`
- `/ts-chay-tiktok-ads đọc số tuần này của spa Hồng [dán bảng/đính kèm ảnh], nên tắt video nào?`

## Kết quả nhận được
- Bảng thiết lập Chiến dịch → Nhóm quảng cáo → Quảng cáo, đặt tên chuẩn, để duyệt.
- Kế hoạch 3–5 video test (hook, angle, người nói, CTA, giả thuyết).
- Ngân sách test gợi ý, thời gian chạy, KPI và quy tắc giữ/tăng/thử mới/tắt.
- Hướng dẫn Spark Ads và lấy mã ủy quyền; checklist Pixel/UTM.
- (Khi gửi số liệu) Bảng chỉ số tính lại, chẩn đoán theo phễu và lịch thay video.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-chay-tiktok-ads-<chu-de-khong-dau>/`.
2. Lưu kế hoạch chiến dịch TikTok Ads đã duyệt (cấu trúc, video test, ngân sách, KPI, quy tắc tối ưu; hoặc báo cáo đọc số) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-chay-tiktok-ads
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd tiktok-ads, spark-ads, test-video>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `bang-thiet-lap.csv`, `bao-cao-so-lieu.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-chay-tiktok-ads · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu đã có video thắng/thua rõ ràng, đề xuất ghi bài học vào `02-kien-thuc/cong-thuc/quang-cao-da-test.md`; nếu CPA/ngân sách thực tế khác KPI trong `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`, đề xuất cập nhật — hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bảo đảm kết quả. Mọi con số ngân sách, ngưỡng là gợi ý ban đầu, cần kiểm chứng với tài khoản thật.
- Chỉ tạo/bật/sửa chiến dịch khi đã xác nhận tài khoản, lịch và ngân sách; tạo ở trạng thái tạm dừng trước.
- Không sao chép video, nhạc, hình của người khác khi không có quyền; nhạc trong quảng cáo dùng thư viện nhạc thương mại của TikTok.
- Không xin mật khẩu, OTP, thông tin thẻ trong chat; kết nối tài khoản làm qua `/ts-ket-noi-ung-dung`.
- Phân tích theo mục tiêu và khi đủ dữ liệu; không tắt vội chỉ vì biến động ngắn.

## Skill liên quan
- Trước: `/ts-viet-quang-cao`, `/ts-kich-ban-reels` · Sau: `/ts-doc-so-lieu-hinh-anh`, `/ts-bang-tinh-excel`, `/ts-lap-lich-tu-dong`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
