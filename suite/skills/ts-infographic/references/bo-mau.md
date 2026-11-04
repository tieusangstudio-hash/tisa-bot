# 6 bộ màu infographic

Dùng cho `/ts-infographic`. Mỗi bộ màu đã được định nghĩa sẵn trong `templates/danh-sach-buoc.html`;
chỉ cần đổi thuộc tính `data-mau` trên thẻ `<body>`.

Nếu `01-ho-so/04-thuong-hieu-noi-dung.md` có màu thương hiệu: chọn bộ màu gần nhất, rồi ghi đè 3 biến
`--nhan`, `--nhan-tieu-de`, `--chu-tren-nhan` trong khối `<style id="mau-thuong-hieu">` của mẫu.

## Bảng tóm tắt

| Mã `data-mau` | Tên gọi | Cảm giác | Hợp với |
|---|---|---|---|
| `den-vang` | Đen vàng | Sang, mạnh, nổi bật trên bảng tin | Kiến thức kinh doanh, tài chính, bất động sản, mẹo nhanh |
| `gradient-tim` | Gradient tím | Hiện đại, sáng tạo, công nghệ | AI, công cụ số, khóa học online, sự kiện |
| `xanh` | Xanh | Tin cậy, rõ ràng, chuyên nghiệp | Giáo dục, y tế, dịch vụ, quy trình, hướng dẫn |
| `cam-vang` | Cam vàng | Vui, năng lượng, gần gũi | Ăn uống, bán lẻ, mẹ và bé, khuyến mãi |
| `do-cam` | Đỏ cam | Khẩn, nóng, kêu gọi hành động | Cảnh báo lỗi sai, ưu đãi có hạn, "đừng làm điều này" |
| `trang-cam` | Trắng cam | Sạch, nhẹ, dễ đọc lâu | Danh sách dài, checklist, nội dung nhiều chữ |

## Chi tiết mã màu

### 1. Đen vàng — `den-vang`
| Vai trò | Biến CSS | Mã màu |
|---|---|---|
| Nền | `--nen` | gradient tỏa `#2A2410` → `#111111` |
| Chữ trên nền / chữ phụ | `--chu-nen` / `--chu-nen-phu` | `#FFFFFF` / `#BDBDBD` |
| Chữ nhấn trong tiêu đề | `--nhan-tieu-de` | `#FFC400` |
| Thẻ / viền thẻ | `--the` / `--vien` | `#1C1C1C` / `#2E2E2E` |
| Chữ trong thẻ / phụ | `--chu-the` / `--chu-the-phu` | `#FFFFFF` / `#CFCFCF` |
| Màu nhấn (ô số, đường kẻ) | `--nhan` | `#FFC400` |
| Chữ trên màu nhấn | `--chu-tren-nhan` | `#111111` |

### 2. Gradient tím — `gradient-tim`
| Vai trò | Biến CSS | Mã màu |
|---|---|---|
| Nền | `--nen` | gradient `#1E0B3B` → `#4C1D95` → `#7E22CE` |
| Chữ trên nền / chữ phụ | `--chu-nen` / `--chu-nen-phu` | `#FFFFFF` / `#E9D5FF` |
| Chữ nhấn trong tiêu đề | `--nhan-tieu-de` | `#F0ABFC` |
| Thẻ / viền thẻ | `--the` / `--vien` | trắng trong suốt 10% / 20% |
| Chữ trong thẻ / phụ | `--chu-the` / `--chu-the-phu` | `#FFFFFF` / `#E9D5FF` |
| Màu nhấn | `--nhan` | `#F0ABFC` |
| Chữ trên màu nhấn | `--chu-tren-nhan` | `#2E1065` |

### 3. Xanh — `xanh`
| Vai trò | Biến CSS | Mã màu |
|---|---|---|
| Nền | `--nen` | gradient `#E3EEFF` → `#FFFFFF` |
| Chữ trên nền / chữ phụ | `--chu-nen` / `--chu-nen-phu` | `#0B2545` / `#44546A` |
| Chữ nhấn trong tiêu đề | `--nhan-tieu-de` | `#1D4ED8` |
| Thẻ / viền thẻ | `--the` / `--vien` | `#FFFFFF` / `#CFE0FA` |
| Chữ trong thẻ / phụ | `--chu-the` / `--chu-the-phu` | `#0B2545` / `#44546A` |
| Màu nhấn | `--nhan` | `#1D4ED8` |
| Chữ trên màu nhấn | `--chu-tren-nhan` | `#FFFFFF` |

### 4. Cam vàng — `cam-vang`
| Vai trò | Biến CSS | Mã màu |
|---|---|---|
| Nền | `--nen` | gradient `#FFC400` → `#FF8A00` |
| Chữ trên nền / chữ phụ | `--chu-nen` / `--chu-nen-phu` | `#2B1600` / `#4A2A00` |
| Chữ nhấn trong tiêu đề | `--nhan-tieu-de` | `#8A1C00` |
| Thẻ / viền thẻ | `--the` / `--vien` | `#FFFFFF` / nâu 10% |
| Chữ trong thẻ / phụ | `--chu-the` / `--chu-the-phu` | `#2B1600` / `#5C4630` |
| Màu nhấn | `--nhan` | `#FF6A00` |
| Chữ trên màu nhấn | `--chu-tren-nhan` | `#FFFFFF` |

### 5. Đỏ cam — `do-cam`
| Vai trò | Biến CSS | Mã màu |
|---|---|---|
| Nền | `--nen` | gradient `#B91C1C` → `#FF5A1F` |
| Chữ trên nền / chữ phụ | `--chu-nen` / `--chu-nen-phu` | `#FFFFFF` / `#FFE4D6` |
| Chữ nhấn trong tiêu đề | `--nhan-tieu-de` | `#FFE08A` |
| Thẻ / viền thẻ | `--the` / `--vien` | `#FFFFFF` / đen 6% |
| Chữ trong thẻ / phụ | `--chu-the` / `--chu-the-phu` | `#2A0A0A` / `#5B3A33` |
| Màu nhấn | `--nhan` | `#E02424` |
| Chữ trên màu nhấn | `--chu-tren-nhan` | `#FFFFFF` |

### 6. Trắng cam — `trang-cam`
| Vai trò | Biến CSS | Mã màu |
|---|---|---|
| Nền | `--nen` | `#FFFFFF` |
| Chữ trên nền / chữ phụ | `--chu-nen` / `--chu-nen-phu` | `#1F1F1F` / `#5E5E5E` |
| Chữ nhấn trong tiêu đề | `--nhan-tieu-de` | `#FF6B00` |
| Thẻ / viền thẻ | `--the` / `--vien` | `#FFF4EC` / `#FFD8BF` |
| Chữ trong thẻ / phụ | `--chu-the` / `--chu-the-phu` | `#1F1F1F` / `#5E5E5E` |
| Màu nhấn | `--nhan` | `#FF6B00` |
| Chữ trên màu nhấn | `--chu-tren-nhan` | `#FFFFFF` |

## Quy tắc dùng màu

1. **Một loạt ảnh – một bộ màu.** Đăng carousel/loạt bài thì giữ nguyên bộ màu để người xem nhận ra thương hiệu.
2. **Màu nhấn chỉ cho thứ quan trọng:** số thứ tự, 1–3 chữ trong tiêu đề, đường kẻ. Không tô màu nhấn cả đoạn văn.
3. **Độ tương phản:** chữ nội dung phải đọc rõ trên điện thoại ở độ sáng thấp. Khi đổi màu thương hiệu, kiểm tra chữ
   trên màu nhấn (`--chu-tren-nhan`): màu nhấn sáng (vàng, hồng nhạt) → chữ đậm; màu nhấn đậm (xanh, đỏ) → chữ trắng.
4. **Không dùng quá 2 màu nổi** trên một ảnh (ngoài đen/trắng/xám).
5. **Đỏ cam dùng có chừng mực:** hợp nội dung cảnh báo, ưu đãi có hạn thật; dùng thường xuyên sẽ gây mệt mắt.
