# Mẫu cấu trúc bảng tính (dùng cho /ts-bang-tinh-excel)

Mỗi workbook nên có các sheet theo vai trò:

| Sheet | Vai trò | Ai sửa |
|---|---|---|
| `HuongDan` | Cách dùng, giải thích cột, giả định, người phụ trách | Người tạo |
| `DanhMuc` | Danh sách chọn (trạng thái, nguồn, nhóm chi…) | Quản lý |
| `DuLieu` (Input) | Mỗi dòng 1 bản ghi, nhập hằng ngày | Nhân viên |
| `TinhToan` (Calculation) | Công thức trung gian (nếu cần) | Không ai sửa tay |
| `TongQuan` (Dashboard) | KPI, bảng tóm tắt, biểu đồ | Không ai sửa tay |

Quy ước: một dòng tiêu đề, không gộp ô (merge) trong vùng dữ liệu, không để dòng trống giữa bảng, định dạng vùng dữ liệu thành **Bảng** (Excel: Ctrl+T / Cmd+T; Google Sheets: Định dạng → Chuyển đổi thành bảng nếu có) để công thức tự mở rộng.

Công thức dưới đây viết theo kiểu Excel/Google Sheets, dấu phân cách đối số là `,`. Máy cài định dạng Việt Nam có thể dùng `;` thay cho `,`.

---

## 1. CRM khách hàng (quản lý khách tiềm năng và khách mua)

**Sheet `KhachHang`**

| Cột | Kiểu | Ràng buộc / validation | Ghi chú |
|---|---|---|---|
| Mã KH | Chữ | Duy nhất, vd `KH0001` | Khóa chính |
| Ngày tạo | Ngày | dd/mm/yyyy | |
| Họ tên | Chữ | Bắt buộc | |
| Số điện thoại | Chữ | Định dạng văn bản (giữ số 0 đầu), 10 số | Dữ liệu cá nhân — hạn chế chia sẻ |
| Kênh | Danh sách | Facebook, Zalo, TikTok, Website, Giới thiệu, Khác | |
| Nhu cầu | Chữ | | |
| Trạng thái | Danh sách | Mới, Đang tư vấn, Hẹn lại, Đã mua, Không mua | |
| Giá trị dự kiến | Tiền | ≥ 0 | |
| Người phụ trách | Danh sách | Lấy từ `DanhMuc` | |
| Lần liên hệ gần nhất | Ngày | | |
| Hẹn liên hệ tiếp | Ngày | | |
| Ghi chú | Chữ | | |

Công thức gợi ý:
- Kiểm tra trùng số điện thoại (cột phụ): `=IF(COUNTIF(D:D, D2)>1, "TRÙNG", "")`
- Quá hạn liên hệ (cột phụ): `=IF(AND(K2<>"", K2<TODAY(), G2<>"Đã mua", G2<>"Không mua"), "QUÁ HẠN", "")`
- Định dạng có điều kiện: tô đỏ dòng "QUÁ HẠN", tô xanh "Đã mua".

**Sheet `TongQuan`**: số khách theo trạng thái `=COUNTIF(KhachHang!G:G, "Đã mua")`; tỉ lệ chốt = Đã mua ÷ (Đã mua + Không mua); số khách theo kênh; doanh thu dự kiến đang tư vấn `=SUMIF(KhachHang!G:G, "Đang tư vấn", KhachHang!H:H)`.

---

## 2. Sổ thu chi

**Sheet `ThuChi`**

| Cột | Kiểu | Validation |
|---|---|---|
| Ngày | Ngày | |
| Loại | Danh sách | Thu, Chi |
| Hạng mục | Danh sách | Thu: Bán hàng, Học phí, Khác · Chi: Nhập hàng, Quảng cáo, Lương, Mặt bằng, Vận chuyển, Khác |
| Diễn giải | Chữ | |
| Số tiền | Tiền | > 0 (luôn nhập số dương) |
| Hình thức | Danh sách | Tiền mặt, Chuyển khoản, Ví điện tử |
| Chứng từ | Chữ/link | Link ảnh hóa đơn |
| Tháng | Công thức | `=TEXT(A2, "yyyy-mm")` |

**Sheet `TongQuan`** (ô B1 chọn tháng, vd `2026-11`):
- Tổng thu: `=SUMIFS(ThuChi!E:E, ThuChi!B:B, "Thu", ThuChi!H:H, B1)`
- Tổng chi: `=SUMIFS(ThuChi!E:E, ThuChi!B:B, "Chi", ThuChi!H:H, B1)`
- Lãi/lỗ: `=TongThu - TongChi`
- Chi theo hạng mục: `=SUMIFS(ThuChi!E:E, ThuChi!B:B, "Chi", ThuChi!C:C, A5, ThuChi!H:H, $B$1)`
- Biểu đồ: cột thu–chi theo tháng; tròn hoặc cột ngang cho cơ cấu chi.
- Ô kiểm tra: số dòng thiếu số tiền `=COUNTIFS(ThuChi!A:A, "<>", ThuChi!E:E, "")`.

---

## 3. Danh sách học viên / khách hàng dịch vụ theo khóa

**Sheet `HocVien`**

| Cột | Kiểu | Validation / công thức |
|---|---|---|
| Mã HV | Chữ | Duy nhất |
| Họ tên | Chữ | |
| Số điện thoại | Chữ | Giữ số 0 đầu |
| Email | Chữ | Có chứa "@" |
| Khóa học | Danh sách | Lấy từ `DanhMuc` |
| Ngày đăng ký | Ngày | |
| Học phí | Tiền | Tra từ `DanhMuc`: `=XLOOKUP(E2, DanhMuc!A:A, DanhMuc!B:B, "")` (Excel cũ dùng `VLOOKUP`) |
| Giảm giá | Tiền | ≥ 0 |
| Phải đóng | Công thức | `=G2-H2` |
| Đã đóng | Tiền | |
| Còn nợ | Công thức | `=I2-J2` |
| Trạng thái học phí | Công thức | `=IF(K2<=0, "Đủ", IF(J2>0, "Một phần", "Chưa đóng"))` |
| Số buổi tham gia | Số | |
| Ghi chú | Chữ | |

**Sheet `TongQuan`**: số học viên mỗi khóa `=COUNTIF(HocVien!E:E, A2)`, tổng học phí đã thu, tổng còn nợ, danh sách còn nợ (dùng bộ lọc hoặc `=FILTER(HocVien!B:K, HocVien!K:K>0)`).

---

## 4. Theo dõi quảng cáo theo ngày

**Sheet `QuangCao`** (mỗi dòng = 1 ngày × 1 chiến dịch)

| Cột | Kiểu | Công thức |
|---|---|---|
| Ngày | Ngày | |
| Nền tảng | Danh sách | Facebook, TikTok, Google, Zalo |
| Chiến dịch | Chữ | |
| Chi tiêu | Tiền | |
| Hiển thị | Số | |
| Click | Số | |
| Kết quả (tin nhắn/lead/đơn) | Số | |
| Đơn chốt | Số | Nhập từ CRM |
| Doanh thu | Tiền | Nhập từ CRM |
| CPM | Công thức | `=IFERROR(D2/E2*1000, "")` |
| CTR | Công thức | `=IFERROR(F2/E2, "")` (định dạng %) |
| CPC | Công thức | `=IFERROR(D2/F2, "")` |
| Chi phí/kết quả | Công thức | `=IFERROR(D2/G2, "")` |
| Tỉ lệ chốt | Công thức | `=IFERROR(H2/G2, "")` |
| ROAS | Công thức | `=IFERROR(I2/D2, "")` |

**Sheet `TongQuan`**: ô chọn khoảng ngày; tổng chi, tổng kết quả, chi phí/kết quả theo nền tảng (`SUMIFS` chia `SUMIFS`, không lấy trung bình của cột tỉ lệ); biểu đồ đường chi phí/kết quả theo ngày; định dạng có điều kiện tô đỏ khi chi phí/kết quả > mục tiêu (ô mục tiêu đặt ở `HuongDan`).

Lưu ý: tỉ lệ tổng phải tính từ tổng gốc (vd CPM tổng = tổng chi ÷ tổng hiển thị × 1000), **không** lấy trung bình cộng cột CPM.

---

## 5. Lịch nội dung

| Ngày đăng | Kênh | Trụ cột | Chủ đề | Định dạng | Hook | CTA | Người làm | Trạng thái (Ý tưởng/Đang làm/Chờ duyệt/Đã đăng) | Link bài | Tương tác |

Định dạng có điều kiện theo trạng thái; ô kiểm tra số bài trong tuần `=COUNTIFS(A:A, ">="&B1, A:A, "<"&B1+7)`.

---

## Ô kiểm tra lỗi nên có trong mọi workbook

- Số ô lỗi công thức: `=SUMPRODUCT(--ISERROR(TinhToan!A2:Z1000))`
- Tổng đối chiếu: tổng ở `TongQuan` = tổng cột gốc → `=IF(ABS(TongQuan!B3-SUM(DuLieu!E:E))<1, "KHỚP", "LỆCH")`
- Số dòng có khóa chính bị trùng: `=SUMPRODUCT((A2:A1000<>"")*(COUNTIF(A2:A1000, A2:A1000)>1))` (kết quả phải bằng 0)
