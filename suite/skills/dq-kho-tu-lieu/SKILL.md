---
name: dq-kho-tu-lieu
description: "Lấy ảnh, video, nhạc, logo, nền thật của chủ trong Kho tư liệu trước khi thiết kế, dựng, đăng bài. Tìm bằng từ khóa, dùng tệp gốc."
group: Điều hành
---
# Dùng Kho tư liệu của chủ

Kho là nơi chủ để tư liệu thật của doanh nghiệp: ảnh sản phẩm, thương hiệu, B-roll, video đã quay, nhạc, hiệu ứng, nền, logo, video thành phẩm, feedback học viên, bài học. Kho nằm ngay trên máy chủ, không đưa lên mạng.

**Khi nào dùng (bắt buộc):** mọi việc cần ảnh, video, nhạc, logo, nền hay hình thật: thiết kế ảnh, banner, thumbnail, dựng clip, làm slide, soạn bài đăng có hình, quảng cáo, tư vấn khách cần ảnh mẫu. Xem kho TRƯỚC khi tự tạo hay tự tìm tư liệu ở nơi khác.

## Lệnh

```
B="{{BANG}}"
"{{PY}}" "$B" kho                                    # thư mục kho, các ngăn, số tệp
"{{PY}}" "$B" kho --tim "từ khóa"                    # tìm, không cần gõ dấu
"{{PY}}" "$B" kho --tim "từ khóa" --loai anh         # lọc theo ngăn
```

Ngăn (`--loai`): `anh` (ảnh sản phẩm, thương hiệu), `broll`, `video` (video đã quay), `am-thanh`, `hieu-ung`, `nen`, `logo`, `khac`, `thanh-pham` (video thành phẩm, quảng cáo đã làm), `feedback`, `bai-hoc`, `may` (thư mục chủ liên kết trên máy).
Mỗi kết quả có `ten`, `ngan`, `kieu`, `mo_ta`, `the` (thẻ), `duong_dan` (đọc thẳng được) và `tep_goc`. Cũng có thể đọc `MUC-LUC.md` ở gốc kho (đường dẫn trong kết quả lệnh `kho`), mỗi ngăn có mục lục riêng.

## Cách làm
1. Xác định cần loại tư liệu nào (ngăn nào).
2. Tìm bằng 2 đến 3 từ khóa khác nhau (tên sản phẩm, chủ đề, màu, tỉ lệ khung). Không thấy thì thử từ đồng nghĩa trước khi kết luận kho chưa có.
3. Xem thật: ảnh thì mở xem; video thì lấy vài khung bằng `ffmpeg` (lưu khung ra thư mục tạm, không lưu vào kho) hoặc đọc mô tả và thẻ.
4. Dùng tệp: đọc thẳng `duong_dan`. Cần sửa thì chép sang thư mục của việc rồi sửa bản chép.
5. Ghi rõ trong kết quả đã dùng tệp nào (đường dẫn đầy đủ).
6. Kho chưa có thứ cần: nói rõ cần loại gì, nhờ chủ bỏ thêm vào ngăn `00 - Bo vao day AI tu phan loai`, và làm tiếp phần không cần tư liệu đó. Không bịa ra tệp.

## Luật
- Tệp trong kho là tệp gốc của chủ: chỉ đọc. Không xóa, không đổi tên, không dời, không sửa đè.
- Không tải tệp của kho lên mạng, không đăng ở đâu, trừ khi việc đã được chủ duyệt đúng tệp đó.
- Tệp riêng tư (chuyển khoản, giấy tờ, tin nhắn cá nhân) không dùng để đăng.
- Lối tắt hỏng (không mở được tệp gốc): báo chủ, chuyển sang tệp khác.
- Nhạc: chỉ dùng nhạc trong kho; không tự tải nhạc có bản quyền.


## Google Drive trong Kho tư liệu (V3.34)
Trang Kho tư liệu có thẻ **Google Drive**: chủ nối Drive một lần, chọn hai thư mục.
- **Thư mục làm việc** (Drive → máy): tư liệu trong thư mục Drive này được chép về Kho trên máy, vào ngăn `12 - Thu muc lien ket tren may/Google Drive - <tên thư mục>/` (giữ nguyên cấu trúc thư mục con). **Lấy tư liệu thật ở đó** như mọi tư liệu khác trong Kho, ghi rõ đã dùng tệp nào. Tệp Google Docs/Slides được xuất PDF, Sheets xuất .xlsx. Tệp lớn hơn giới hạn chủ đặt (mặc định 500 MB) chưa được chép: nói chủ nếu cần.
- **Thư mục nhận kết quả** (máy → Drive): kết quả trong `03 - Ket qua` được tải lên thư mục Drive này theo ngày và tên việc (tự động hoặc khi chủ bấm). Khi chủ nhờ gửi một tệp cụ thể lên Drive: `tisa_drive_do op=thu_muc_kho` lấy mã thư mục nhận kết quả, rồi `op=tai_len duong_dan=<tệp> cha=<mã>` (hoặc `op=tai_thu_muc`).
- `tisa_drive_do op=thu_muc_kho` xem hai thư mục đã chọn và chế độ tự động. `op=dong_bo_kho viec=ve|len` bảo cầu nối chép về / tải lên ngay (chạy trong vài giây).
- Chưa nối Drive (`CHUA_DANG_NHAP`): nói chủ bấm **Kết nối Drive** ở trang Kho tư liệu (nút ⚡ nhờ TISA BOT kết nối tự động giao cho Đạt Đấu Nối), hoặc làm theo `dq-ho-tro-ket-noi` phần Google Drive. Không bao giờ in Client secret, token, mã xác thực ra chat.
- Chỉ chép về và tải lên: không xóa gì trên Drive hay trên máy.
