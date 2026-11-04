---
name: ts-phan-tich-doi-thu
description: "Gọi bằng /ts-phan-tich-doi-thu. Đọc hồ sơ doanh nghiệp trước, hỏi phần thiếu, rồi nghiên cứu đối thủ đa kênh tại Việt Nam (website, Google, Facebook, TikTok, YouTube, Instagram, Google Maps, Shopee/Lazada…), lập sổ nguồn có kiểm chứng, so sánh giá - chất lượng - dịch vụ, chấm content nổi bật, tìm 3 khoảng trống và 5 hành động; xuất Excel hoặc Google Sheets khi đã kết nối. Dùng khi cần biết đối thủ bán gì, giá bao nhiêu, làm content gì. Từ khóa: phân tích đối thủ, nghiên cứu đối thủ, so sánh giá, đối thủ làm content gì, khoảng trống thị trường, spy đối thủ."
---

# /ts-phan-tich-doi-thu — Phân tích đối thủ

> AI hiểu doanh nghiệp của bạn trước, rồi mới đi tìm đối thủ trên các kênh phổ biến ở Việt Nam, ghi lại
> từng bằng chứng có đường dẫn, so sánh giá – chất lượng – dịch vụ – nội dung, và chỉ ra khoảng trống
> bạn có thể chiếm. Kết quả là báo cáo Excel/Google Sheets 5 trang.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Muốn biết đối thủ bán gì, giá bao nhiêu, ưu đãi gì, chăm sóc khách ra sao.
- Muốn biết đối thủ làm nội dung gì đang hút tương tác (không sao chép, chỉ học nguyên lý).
- Chuẩn bị định giá, viết quảng cáo, mở cửa hàng mới, ra sản phẩm mới.
- Cần báo cáo có nguồn rõ ràng để trình đối tác/nhân viên.

**Không dùng khi:** chưa có ý tưởng kinh doanh cụ thể, muốn kiểm tra một ngách có đáng làm không → `/ts-kiem-chung-ngach`.
Chỉ muốn tìm video YouTube nhiều view theo chủ đề → `/ts-nghien-cuu-youtube`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `05-muc-tieu-quy-tac-lien-he.md` (khu vực, kênh);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `phan-tich-doi-thu` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** đọc thêm `02-kien-thuc/doi-thu/` (hồ sơ đối thủ đã lưu từ lần trước) — chỉ cập nhật
phần thay đổi (giá, ưu đãi, nội dung mới), ghi ngày.

## Quy trình AI thực hiện

Luôn hiểu doanh nghiệp trước khi nghiên cứu đối thủ. Không biến suy luận thành sự thật và không gọi nội
dung là "viral" nếu thiếu chỉ số phù hợp.

### Bước 1 — Lập hồ sơ doanh nghiệp tạm thời
Kiểm kê tệp trong Bộ Não và tệp người dùng gửi (giới thiệu, bảng giá, danh mục sản phẩm, hồ sơ khách,
kế hoạch marketing, nội dung mẫu, website, nhận diện, bảng tính). Tạo `HỒ SƠ DOANH NGHIỆP TẠM THỜI`:
- Tên doanh nghiệp/cá nhân hoặc dự án · sản phẩm/dịch vụ · khách hàng mục tiêu và vấn đề của họ ·
  khu vực, ngôn ngữ, kênh đang hoạt động · mức giá/mô hình doanh thu · điểm khác biệt, bằng chứng,
  mục tiêu nghiên cứu · tệp nguồn của từng thông tin.
- Trạng thái mỗi trường: `ĐÃ CÓ`, `SUY RA`, `CÒN THIẾU`.

Không quét thư mục ngoài phạm vi người dùng cho phép. Không coi tên thư mục/tên tệp là sự thật khi chưa
đọc nội dung. Chi tiết: `references/ho-so-doanh-nghiep.md`.

### Bước 2 — Chỉ hỏi phần còn thiếu (tối đa 5 câu)
Chưa xác định được sản phẩm/dịch vụ → **dừng, chưa nghiên cứu web**, hỏi trước:
1. Anh/chị đang cung cấp sản phẩm hoặc dịch vụ gì?
2. Khách hàng mục tiêu là ai?
3. Hoạt động ở khu vực nào?
4. Mục tiêu nghiên cứu: định vị, giá, dịch vụ hay nội dung?
5. Có đối thủ cụ thể nào cần đưa vào không?

Không hỏi lại thông tin đã có. Sau khi trả lời, cập nhật hồ sơ và nêu rõ phần nào vẫn là giả định.

### Bước 3 — Xác định phạm vi và nhóm đối thủ (cổng duyệt)
Ghi: đối thủ **trực tiếp** (cùng khách, cùng nhu cầu, cùng dạng giải pháp), **gián tiếp** (cùng nhu cầu, khác
giải pháp), **thay thế** (khách tự làm, trì hoãn, dùng cách khác) · khu vực, ngôn ngữ, khoảng thời gian ·
quyết định báo cáo cần hỗ trợ · tiêu chí so sánh · số lượng đối thủ hợp lý (thường 3–8).
Chưa có danh sách → lập danh sách ứng viên từ dữ liệu công khai, ghi lý do chọn. Không gọi là đối thủ
trực tiếp chỉ vì trùng vài từ khóa. Khung chi tiết: `references/khung-nghien-cuu.md`.
👉 Trình danh sách đối thủ + phạm vi, chờ "duyệt" rồi mới nghiên cứu sâu.

### Bước 4 — Nghiên cứu đa kênh tại Việt Nam
Chọn kênh theo ngành, không bắt buộc đủ mọi kênh:
- Website, Google, trang giá: gói, giá, điều kiện, thông điệp.
- Facebook: Fanpage, nội dung, phản hồi công khai, tín hiệu cộng đồng.
- TikTok, YouTube: hook, định dạng, lượt xem, cách trình bày.
- Instagram: hình ảnh, định vị, nội dung trực quan.
- LinkedIn: B2B, tuyển dụng, chuyên môn.
- Google Maps: địa điểm, đánh giá, trải nghiệm tại chỗ.
- Shopee, Lazada, TikTok Shop hoặc sàn chuyên ngành: giá, biến thể, phản hồi.

Đọc `references/kenh-nghien-cuu-viet-nam.md` để chọn kênh và mẫu truy vấn. Cần công cụ tìm kiếm/đọc web;
môi trường không có → nói rõ, hướng dẫn người dùng tự chụp màn hình/dán link và AI phân tích phần được cung cấp.
Chỉ dùng dữ liệu công khai hoặc nguồn người dùng cấp quyền; không giả danh, không vượt đăng nhập, không thu
dữ liệu riêng tư, không tương tác gây hiểu nhầm (vd giả làm khách hỏi giá).

### Bước 5 — Lập sổ nguồn có kiểm chứng
Mỗi phát hiện một dòng: đối thủ · kênh · URL hoặc tên tệp · ngày truy cập (YYYY-MM-DD) · dữ kiện quan sát ·
trạng thái `SỰ THẬT` / `SUY LUẬN` / `CHƯA KIỂM CHỨNG` · độ tin cậy cao / trung bình / thấp.

Kiểm tra sổ nguồn bằng script (lưu sổ thành CSV trước):
- macOS / Linux: `python3 scripts/kiem_tra_nguon.py so-nguon.csv`
- Windows: `py scripts\kiem_tra_nguon.py so-nguon.csv`

Script báo URL thiếu/sai, ngày sai định dạng, nhãn không hợp lệ, URL trùng. Không chạy được lệnh → AI tự
soát theo đúng các tiêu chí đó.

### Bước 6 — Chuẩn hóa và phân tích
- Đưa giá về cùng đơn vị; ghi thời lượng, thuế/phí, phạm vi dịch vụ, điều kiện ưu đãi, thời điểm quan sát.
  Đọc `references/tieu-chi-so-sanh.md` (cột "chỉ báo chất lượng", không phải "chất lượng tuyệt đối").
- Đánh giá nội dung theo `references/phuong-phap-content.md` (chuẩn hóa tỷ lệ, khung chấm 100 điểm). So trong
  cùng nền tảng, cùng khung thời gian. Không sao chép nguyên văn; chuyển thành mô-típ hook, bằng chứng, cấu
  trúc, định dạng, CTA có thể thử.

### Bước 7 — Chọn đầu ra Excel hoặc Google Sheets
1. Có công cụ Google Drive/Sheets đã kết nối và được cấp quyền tạo tệp → tạo Google Sheet mới ở vị trí được phép.
2. Chưa kết nối, thiếu quyền hoặc người dùng muốn tệp trên máy → chép `assets/MAU_BAO_CAO_PHAN_TICH_DOI_THU.xlsx`
   và điền.
3. Không tuyên bố đã tạo Google Sheet nếu công cụ không có. Nói rõ đầu ra thay thế.

Workbook gồm các trang: `Hồ sơ DN` · `Sổ nguồn` · `So sánh` · `Content` · `Tổng hợp` (mẫu có thêm trang
`Hướng dẫn`). Cấu trúc và quy tắc quyền: `references/dau-ra-excel-drive.md`.

### Bước 8 — Hoàn tất báo cáo
Mặc định gồm:
1. Hồ sơ doanh nghiệp và dữ liệu còn thiếu.
2. Tóm tắt điều hành tối đa 10 dòng.
3. Sổ nguồn đa kênh.
4. Bảng so sánh giá – chất lượng – dịch vụ.
5. Bảng content nổi bật có chỉ số và mức chắc chắn.
6. **3 khoảng trống**, **5 hành động ưu tiên** và phép đo.
7. Giới hạn dữ liệu và câu hỏi cần làm tiếp.

Dùng đúng cột trong `references/mau-dau-ra.md`. Chỉ kết luận khi nhận định quan trọng truy ngược được về
tệp/URL. Dùng "chưa tìm thấy bằng chứng" thay cho "không có".

### Bước 9 — Chuyển phát hiện thành thử nghiệm
Mỗi khoảng trống: bằng chứng hỗ trợ · rủi ro diễn giải sai · một thử nghiệm nhỏ đo được. Không suy đoán
doanh thu, ngân sách quảng cáo, hiệu quả kinh doanh của đối thủ khi thiếu bằng chứng. Xếp 3 thử nghiệm
ưu tiên theo tác động dự kiến, chi phí, thời gian, khả năng đảo ngược.
👉 Trình báo cáo, chờ "duyệt" để lưu.

### Checklist chất lượng
- [ ] Hồ sơ doanh nghiệp rõ sản phẩm/dịch vụ trước khi nghiên cứu web.
- [ ] Mỗi nhận định quan trọng có URL/tệp nguồn và ngày truy cập.
- [ ] Nhãn trạng thái và độ tin cậy đúng chuẩn; sổ nguồn qua kiểm tra script (hoặc soát tay).
- [ ] Giá đã chuẩn hóa cùng đơn vị; chất lượng ghi là "chỉ báo".
- [ ] Không gọi "viral" khi thiếu chỉ số; không sao chép nội dung đối thủ.
- [ ] Có 3 khoảng trống, 5 hành động, 3 thử nghiệm có phép đo.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** hồ sơ doanh nghiệp (`/ts-tao-ho-so-doanh-nghiep`). Nếu đã biết vài đối thủ, ghi tên hoặc link
Fanpage/website của họ. Nếu muốn xuất Google Sheets, kết nối Google Drive trước (`/ts-ket-noi-ung-dung`).

1. Gõ `/ts-phan-tich-doi-thu` kèm việc muốn biết (vd "so giá 5 tiệm bánh kem ở Đà Nẵng").
2. Trả lời các câu AI hỏi (tối đa 5 câu).
3. Xem danh sách đối thủ AI đề xuất: bỏ ai, thêm ai, rồi gõ "duyệt".
4. Chờ AI nghiên cứu (có thể vài phút). Nếu AI không truy cập được web, AI sẽ nhờ bạn dán link hoặc ảnh chụp.
5. Đọc tóm tắt 10 dòng, 3 khoảng trống, 5 hành động. Hỏi lại chỗ nào chưa rõ nguồn.
6. Gõ "duyệt" để nhận file Excel (hoặc Google Sheet) và lưu vào Bộ Não.
7. Dùng kết quả cho bước sau: định giá (`/ts-dinh-gia-offer`), viết quảng cáo (`/ts-viet-quang-cao`).

## Câu lệnh mẫu
- `/ts-phan-tich-doi-thu so sánh giá và ưu đãi của 5 tiệm bánh kem ở Đà Nẵng, xuất Excel`
- `/ts-phan-tich-doi-thu khóa học quay video bằng điện thoại: đối thủ làm content TikTok gì hút view?`
- `/ts-phan-tich-doi-thu spa Hồng ở Cần Thơ, xem đánh giá Google Maps của 6 spa gần đó`
- `/ts-phan-tich-doi-thu shop đồ bộ mặc nhà trên Shopee, so giá – biến thể – đánh giá 1 sao của 5 shop top`
- `/ts-phan-tich-doi-thu cập nhật báo cáo đối thủ tháng trước, chỉ xem giá và ưu đãi mới`

## Kết quả nhận được
- Hồ sơ doanh nghiệp tạm thời + câu hỏi còn thiếu.
- Báo cáo Excel/Google Sheet 5 trang: Hồ sơ DN · Sổ nguồn · So sánh · Content · Tổng hợp.
- Tóm tắt điều hành ≤ 10 dòng; 3 khoảng trống; 5 hành động ưu tiên; 3 thử nghiệm có phép đo.
- Danh sách giới hạn dữ liệu và việc cần nghiên cứu tiếp.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-phan-tich-doi-thu-<chu-de-khong-dau>/`.
2. Lưu báo cáo dạng chữ (tóm tắt điều hành, bảng so sánh, content, khoảng trống, hành động, thử nghiệm, giới hạn) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-phan-tich-doi-thu
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [doi-thu, nghien-cuu, <ngành>, <khu vực>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `bao-cao-doi-thu.xlsx` (hoặc đường dẫn Google Sheet), `so-nguon.csv`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Phân tích đối thủ <chủ đề>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-phan-tich-doi-thu · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Với mỗi đối thủ chính, đề xuất tạo/cập nhật `02-kien-thuc/doi-thu/<ten-doi-thu-khong-dau>.md` (kênh, giá,
   ưu đãi, điểm mạnh/yếu có nguồn, ngày cập nhật) để lần sau chỉ cần cập nhật. Nếu phát hiện làm thay đổi
   định vị/USP trong `01-ho-so/04-thuong-hieu-noi-dung.md`, đề xuất và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Chỉ dùng dữ liệu công khai hoặc được cấp quyền; không giả danh, không vượt đăng nhập, không thu thập
  thông tin cá nhân của khách hàng đối thủ.
- Không sao chép câu chữ, hình ảnh, nhận diện của đối thủ.
- Không bịa số liệu hay suy diễn doanh thu đối thủ; ghi rõ mức chắc chắn.
- Giá, lịch, ưu đãi thay đổi thường xuyên — luôn ghi ngày truy cập.

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` · `/ts-kiem-chung-ngach`
- Sau: `/ts-dinh-gia-offer` · `/ts-chien-luoc-marketing` · `/ts-viet-quang-cao` · `/ts-lich-noi-dung`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
