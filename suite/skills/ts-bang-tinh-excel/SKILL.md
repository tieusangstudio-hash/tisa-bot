---
name: ts-bang-tinh-excel
description: "Gọi bằng /ts-bang-tinh-excel. Tạo, sửa và phân tích bảng tính Excel/CSV/Google Sheets chuyên nghiệp: chia sheet theo vai trò, công thức tự tính, danh sách chọn, bộ lọc, định dạng có điều kiện, biểu đồ và trang tổng quan; có mẫu sẵn cho CRM khách hàng, sổ thu chi, danh sách học viên, theo dõi quảng cáo, lịch nội dung. Từ khóa: tạo file excel, bảng tính, google sheets, công thức excel, dashboard, quản lý khách hàng, sổ thu chi, danh sách học viên, theo dõi quảng cáo."
---

# /ts-bang-tinh-excel — Tạo và sửa bảng tính Excel / Google Sheets

> Giúp bạn có file bảng tính gọn gàng, tự tính, khó nhập sai và nhìn là biết số: quản lý khách, thu chi,
> học viên, quảng cáo, KPI… Kết quả: file Excel (hoặc Google Sheets/CSV) có sheet hướng dẫn, công thức, danh sách chọn và trang tổng quan.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Cần một file quản lý mới: khách hàng (CRM), thu chi, đơn hàng, học viên, quảng cáo, lịch nội dung, KPI.
- Có file cũ lộn xộn, muốn sắp xếp lại, thêm công thức, chống nhập sai.
- Cần công thức cụ thể (cộng theo điều kiện, tra cứu, đếm trùng…) và giải thích dễ hiểu.
- Cần trang tổng quan (dashboard) có biểu đồ để xem nhanh mỗi tuần.

**Không dùng khi:** chỉ cần đọc/nhận xét số liệu có sẵn → `/ts-doc-so-lieu-hinh-anh`; báo cáo quảng cáo Facebook →
`/ts-bao-cao-facebook-ads`; phân tích doanh thu sâu → `/ts-phan-tich-doanh-thu`; cần app nhập liệu trên điện thoại → `/ts-tao-app`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Hiểu ai dùng và để quyết định gì
Hỏi tối đa 5 câu (gợi ý A-B-C-D):
- Bảng dùng để làm gì? (A) Quản lý khách hàng · (B) Thu chi · (C) Học viên/khách theo khóa · (D) Theo dõi quảng cáo · (E) Khác.
- Ai nhập, ai xem? Nhập trên máy tính hay điện thoại?
- Mỗi tuần/tháng cần nhìn ra con số gì để quyết định? (vd "tháng này lãi bao nhiêu", "khách nào cần gọi lại").
- Dữ liệu lấy từ đâu (gõ tay, xuất từ phần mềm, file cũ), đơn vị tiền, tần suất cập nhật.
- Dùng (A) Excel · (B) Google Sheets · (C) Chưa biết (gợi ý: nhiều người cùng nhập → Google Sheets; một người, làm offline → Excel).

### Bước 2 — Thiết kế cấu trúc (CỔNG DUYỆT 1)
Chia sheet theo vai trò: `HuongDan` · `DanhMuc` (Lookup) · `DuLieu` (Input) · `TinhToan` (Calculation, nếu cần) · `TongQuan` (Dashboard).
Mẫu cấu trúc chi tiết (cột, kiểu dữ liệu, validation, công thức) cho 5 loại hay dùng: `references/mau-cau-truc-sheet.md`
- CRM khách hàng · Sổ thu chi · Danh sách học viên · Theo dõi quảng cáo · Lịch nội dung.
- File CSV mẫu (dòng tiêu đề + 1 dòng giả định) trong `assets/mau-csv/` để mở thử bằng Excel/Google Sheets.

Trình bảng thiết kế: tên sheet → danh sách cột (tên, kiểu, ràng buộc) → các ô KPI ở `TongQuan` → biểu đồ (nếu có).
Chờ người dùng gõ **"duyệt cấu trúc"** hoặc sửa ("thêm cột nguồn khách", "bỏ cột email").

### Bước 3 — Dựng bảng đúng chuẩn
- **Dữ liệu dạng bảng sạch**: một dòng tiêu đề, một bản ghi mỗi dòng, không gộp ô trong vùng dữ liệu, không dòng trống giữa bảng.
- **Khóa chính** (Mã KH, Mã HV…) không trùng; ngày đúng kiểu ngày (dd/mm/yyyy), tiền đúng kiểu số (định dạng `#,##0`), phần trăm đúng kiểu %.
- Số điện thoại lưu dạng **văn bản** để giữ số 0 đầu.
- **Danh sách chọn** (Data validation) cho cột trạng thái, kênh, hạng mục — lấy từ `DanhMuc`.
- **Công thức thay số nhập tay**; không nhập số cố định vào công thức — đặt mục tiêu/ngưỡng ở ô riêng trong `HuongDan` và tham chiếu.
- Tỉ lệ tổng tính từ tổng gốc (vd CPM tổng = tổng chi ÷ tổng hiển thị × 1000), không lấy trung bình cộng cột tỉ lệ.
- Cố định dòng tiêu đề (Freeze panes), bật bộ lọc, định dạng có điều kiện (tô đỏ quá hạn, nợ, vượt ngưỡng).
- Thêm chú thích nhập liệu ở ô tiêu đề và sheet `HuongDan` ngắn (cách nhập, ý nghĩa cột, giả định).

### Bước 4 — Tạo file bằng công cụ của nền tảng
- Môi trường có công cụ tạo/sửa file Excel → tạo file `.xlsx` thật (có công thức, validation, định dạng, biểu đồ).
- Đã kết nối Google Sheets/Google Drive → tạo hoặc cập nhật bảng trên Google Sheets; **chỉ ghi đúng phạm vi được phép**.
- Có thể chạy Python → dùng thư viện bảng tính sẵn có của môi trường (nếu thiếu thư viện thì không tự cài khi chưa hỏi).
- Không có công cụ nào → giao file CSV cho từng sheet + danh sách công thức theo ô + hướng dẫn bấm từng bước để học viên tự dựng.
- **Không ghi đè tệp gốc** nếu người dùng không yêu cầu — lưu bản mới có hậu tố `-moi` hoặc ngày.

### Bước 5 — Trang tổng quan và biểu đồ
- Chỉ tạo biểu đồ khi giúp ra quyết định; mỗi biểu đồ ghi tên KPI và khoảng thời gian.
- Gợi ý: thu–chi theo tháng → cột; chi phí/kết quả theo ngày → đường; cơ cấu chi → cột ngang (dễ đọc hơn biểu đồ tròn khi nhiều hạng mục).
- Ô chọn kỳ (tháng/khoảng ngày) để dashboard tự đổi theo.

### Bước 6 — Kiểm tra trước khi giao
- Tính lại (recalculate), kiểm tra không còn lỗi `#REF!`, `#DIV/0!`, `#N/A`, `#VALUE!` (bọc `IFERROR` khi hợp lý).
- Thêm **ô kiểm tra**: số ô lỗi, tổng đối chiếu (tổng ở dashboard = tổng cột gốc), số khóa chính trùng.
- Nhập thử 2–3 dòng giả định, kiểm tra công thức chạy đúng, validation chặn giá trị sai, bộ lọc và freeze pane hoạt động.
- Kiểm tra hiển thị: cột đủ rộng, số không bị `####`, bản in vừa trang (nếu cần in).
- Xóa dữ liệu giả định trước khi giao (hoặc đánh dấu rõ "xóa khi dùng").

### Bước 7 — Giao file (CỔNG DUYỆT 2)
Gửi file + tóm tắt: các sheet, cột nào nhập tay, cột nào tự tính (đừng sửa), ô KPI nằm đâu, cách thêm dòng mới.
Danh sách giả định (vd "tiền tính bằng VND, chưa gồm thuế"). Chờ người dùng gõ **"duyệt"** để lưu vào Bộ Não.

### Checklist chất lượng trước khi giao
- [ ] Có sheet `HuongDan`; tách nhập liệu – tính toán – tổng quan.
- [ ] Không gộp ô trong vùng dữ liệu; một dòng tiêu đề; khóa chính không trùng.
- [ ] Ngày, tiền, %, số điện thoại đúng định dạng; có danh sách chọn cho trường phân loại.
- [ ] Không còn ô lỗi công thức; tổng đối chiếu "KHỚP".
- [ ] File gốc không bị ghi đè; dữ liệu giả định đã xóa hoặc đánh dấu.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** biết mình muốn theo dõi gì; danh sách cột muốn có (nếu nghĩ ra); file cũ (nếu có); dùng Excel hay Google Sheets.

1. Gõ `/ts-bang-tinh-excel` kèm 1 câu: bảng để làm gì, ai nhập (vd "file quản lý khách cho 2 nhân viên cùng nhập").
2. Trả lời các câu hỏi AI đưa ra (gợi ý A-B-C-D thì chọn chữ cái).
3. Xem bảng thiết kế cột. Sửa bằng lời: "thêm cột ngày sinh khách", "trạng thái thêm 'Hủy'". Gõ "duyệt cấu trúc".
4. Nhận file. Mở ra, đọc sheet `HuongDan` trước.
5. Nhập thử 2 dòng thật ở sheet dữ liệu, xem sheet `TongQuan` có tự đổi không. Có gì lạ thì chụp màn hình gửi AI.
6. Google Sheets: chia sẻ cho nhân viên quyền **Người chỉnh sửa** chỉ ở sheet nhập liệu; khóa sheet `TongQuan` (Dữ liệu → Bảo vệ trang tính).
7. Gõ **"duyệt"** để AI lưu mô tả file vào Bộ Não (lần sau sửa file, AI biết cấu trúc).

Mẹo: công thức báo lỗi dấu phẩy → máy bạn dùng dấu `;` thay cho `,` giữa các phần của công thức.

## Câu lệnh mẫu
- `/ts-bang-tinh-excel tạo file quản lý khách hàng cho shop mỹ phẩm online, có nhắc khách cần gọi lại`
- `/ts-bang-tinh-excel sổ thu chi tháng cho tiệm bánh Mây, có biểu đồ thu chi và tính lãi lỗ tự động`
- `/ts-bang-tinh-excel danh sách học viên khóa học quay video, theo dõi học phí còn nợ và số buổi tham gia`
- `/ts-bang-tinh-excel bảng theo dõi quảng cáo Facebook và TikTok theo ngày, tính chi phí/kết quả và ROAS`
- `/ts-bang-tinh-excel sửa file Excel này cho gọn, thêm công thức tính tổng theo nhân viên [đính kèm file]`

## Kết quả nhận được
- File Excel `.xlsx` hoặc Google Sheets (hoặc bộ CSV + hướng dẫn nếu không có công cụ tạo file).
- Sheet `HuongDan`, `DanhMuc`, `DuLieu`, `TongQuan` (và `TinhToan` khi cần) với công thức, danh sách chọn, định dạng có điều kiện.
- Trang tổng quan có KPI và biểu đồ theo kỳ chọn.
- Ô kiểm tra lỗi và tổng đối chiếu; danh sách giả định.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-bang-tinh-excel-<chu-de-khong-dau>/`.
2. Lưu mô tả bảng tính đã duyệt (mục đích, danh sách sheet, cột, công thức chính, ô KPI, giả định, nơi đặt file) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-bang-tinh-excel
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd excel, crm, thu-chi>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `<ten-file>.xlsx` hoặc đường link Google Sheets, các file CSV. Không lưu dữ liệu khách thật vào Bộ Não nếu người dùng không yêu cầu.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-bang-tinh-excel · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không ghi đè tệp gốc nếu người dùng không yêu cầu. Với Google Sheets, chỉ cập nhật đúng phạm vi được phép.
- Không nhập số cố định vào công thức; mục tiêu/ngưỡng đặt ở ô riêng.
- File chứa số điện thoại, địa chỉ khách là dữ liệu cá nhân: chia sẻ đúng người, đúng quyền; không đăng công khai link "ai cũng xem được".
- Không bịa số liệu để "lấp đầy" bảng; dữ liệu mẫu ghi rõ là giả định.
- Không xin mật khẩu tài khoản Google trong chat; kết nối Google Sheets qua `/ts-ket-noi-ung-dung`.

## Skill liên quan
- Trước: `/ts-doc-so-lieu-hinh-anh` · Sau: `/ts-phan-tich-doanh-thu`, `/ts-lap-lich-tu-dong` (nhắc cập nhật bảng hằng tuần), `/ts-tao-app`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
