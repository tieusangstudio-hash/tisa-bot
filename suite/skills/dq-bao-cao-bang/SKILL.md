---
name: "Báo lên bảng"
description: "Mọi nhân sự Đội Quân AI báo tiến độ, gắn ảnh và kết quả phần việc của mình lên Bảng giao việc."
group: Điều hành
---
# Báo lên bảng giao việc

Dùng khi việc được giao có **mã việc** (dạng `job-...`) và **số phần** trên Bảng giao việc. Chủ theo dõi tiến độ ở đó, nên mọi thay đổi phải báo lên ngay.

```bash
B="{{BANG}}"
"{{PY}}" "$B" lay JOB                                   # xem yêu cầu và phần của mình
"{{PY}}" "$B" phan JOB N --state run --pct 10           # bắt đầu
"{{PY}}" "$B" phan JOB N --pct 60 --append "Đã xong bước 2/3"
"{{PY}}" "$B" anh JOB "thu-muc/tai-nguyen/anh.png" --title "Ảnh 1080x1350"
"{{PY}}" "$B" phan JOB N --state done --out-file ket-qua.md   # xong, không cần duyệt
"{{PY}}" "$B" phan JOB N --state duyet --out-file ket-qua.md  # xong, chờ anh duyệt (đăng, gửi, chi tiền)
"{{PY}}" "$B" phan JOB N --state owner --append "Anh cần nộp: ..."  # thiếu thứ chỉ anh có
"{{PY}}" "$B" phan JOB N --state err --append "Lý do"         # kẹt, nói thật
```

Chủ nhắn hỏi trong khung Trao đổi của việc (sự kiện `tin-nhan` có `msg_id`): trả lời bằng
`"{{PY}}" "$B" tra-loi MSG_ID --from <mã của mình> --text-file tra-loi.md` (thêm `--chua-xong` nếu còn làm tiếp).

Quy tắc:
- Báo `run` khi bắt đầu, báo tiến độ khi xong mỗi bước lớn, báo kết quả cuối bằng nội dung thật (không viết "đã xong" khi chưa có sản phẩm).
- Ảnh: lưu vào thư mục kết quả của việc (`tai-nguyen/`) rồi `anh JOB tep` để anh xem ngay trên bảng.
- Video, âm thanh, Word, PDF, slide, Excel, CSV: xem mục **BÀN GIAO KẾT QUẢ** bên dưới. Không được báo xong khi tệp chưa lên bảng.
- Không đổi phần của người khác. Không gọi `xong` cho cả việc: đó là việc của Tâm.
- **Kết quả của phần nào là của người làm phần đó.** `--out-file` chỉ chứa sản phẩm và lời bàn giao của phần mình. Không chép lại, không tóm tắt lại kết quả của người khác, không dán lại báo cáo tổng. Cần dựa vào phần trước thì ghi một câu "dùng bản của <tên>".
- `--append` chỉ để báo tiến độ, một dòng ngắn, không gửi lại cùng một dòng. Bảng cất tiến độ riêng, không lẫn vào kết quả.
- Khối BÀN GIAO tối đa 3 dòng (sản phẩm ở đâu, chuyển cho ai, cần chủ quyết gì), không nhắc lại nội dung vừa nộp.
- Khoá nằm trong `~/.config/doi-quan/.env`; không in, không chép khoá đi đâu.

## BÀN GIAO KẾT QUẢ (video, ảnh, tài liệu, trang tính)

Việc giao ra **tệp** (video, hình, nhạc, Word, PDF, slide, Excel, CSV) thì anh phải **bấm vào xem được và tải về được** ngay trên bảng. Chỉ viết "đã dựng xong video" trong báo cáo là chưa đủ.

```bash
B="{{BANG}}"
"{{PY}}" "$B" ban-giao JOB "/duong/dan/video.mp4" "/duong/dan/bao-cao.xlsx"   # đưa tệp vào thư mục của việc để anh Xem, Tải về
"{{PY}}" "$B" drive JOB "/duong/dan/bao-cao.xlsx"                             # in thư mục Drive chuẩn và tên tệp chuẩn
"{{PY}}" "$B" link JOB --title "Báo cáo tuần 46" --url "https://drive.google.com/..." --kind sheet   # gắn link Drive (kind: doc | sheet | file)
```

1. **Trước khi báo `--state done` hoặc `--state duyet`**, chạy `ban-giao` cho mọi tệp thành phẩm, kể cả video lớn (video không cần tải lên mạng, `ban-giao` là đủ để anh xem và tải ở TISA BOT). Ảnh vẫn dùng `anh` để hiện trong khung ảnh.
2. Trong `--out-file` ghi **tên tệp** và vài chữ nói tệp đó là gì, không dán lại nội dung dài.
3. **Tài liệu, trang tính, slide, PDF: đưa lên Google Drive** nếu TISA BOT đang nối Google Drive và có quyền tạo tệp:
   - Chạy `drive JOB tep` để lấy đúng **thư mục Drive** và **tên tệp** (không tự đặt khác). Cấu trúc cố định: `TISA BOT - Kết quả đội AI / 01 Tài liệu | 02 Trang tính | 03 Trình chiếu | 04 PDF / năm / tháng`.
   - Thư mục nào chưa có thì tạo đúng tên đó (tìm trước, có rồi thì dùng, không tạo trùng). Tải tệp lên, lấy link chia sẻ nội bộ của tệp.
   - Chạy `link JOB --title ... --url <link Drive> --kind doc|sheet|file` để link hiện trên đầu kết quả.
   - Tệp trên Drive ghi thêm mã việc `JOB` vào mô tả để sau này tìm lại.
4. **Chưa nối Google Drive hoặc thiếu quyền**: vẫn `ban-giao` tệp trên máy, và ghi thẳng một dòng "Chưa đưa lên Drive vì chưa nối Google Drive" vào phần bàn giao. Không được nói đã lên Drive khi chưa có link thật.
5. Không đăng công khai, không chia sẻ ra ngoài tổ chức, không xóa tệp cũ trên Drive.
