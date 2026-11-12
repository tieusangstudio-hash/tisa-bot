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
- Ảnh, video, tệp: lưu vào thư mục kết quả của việc (`tai-nguyen/`) rồi `anh JOB tep` để anh xem ngay trên bảng.
- Không đổi phần của người khác. Không gọi `xong` cho cả việc: đó là việc của Tâm.
- **Kết quả của phần nào là của người làm phần đó.** `--out-file` chỉ chứa sản phẩm và lời bàn giao của phần mình. Không chép lại, không tóm tắt lại kết quả của người khác, không dán lại báo cáo tổng. Cần dựa vào phần trước thì ghi một câu "dùng bản của <tên>".
- `--append` chỉ để báo tiến độ, một dòng ngắn, không gửi lại cùng một dòng. Bảng cất tiến độ riêng, không lẫn vào kết quả.
- Khối BÀN GIAO tối đa 3 dòng (sản phẩm ở đâu, chuyển cho ai, cần chủ quyết gì), không nhắc lại nội dung vừa nộp.
- Khoá nằm trong `~/.config/doi-quan/.env`; không in, không chép khoá đi đâu.
