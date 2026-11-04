---
name: ts-tro-ly-may-tinh
description: "Gọi bằng /ts-tro-ly-may-tinh. Đọc ảnh chụp màn hình, giải thích giao diện và lỗi, rồi hỗ trợ thao tác trên máy tính/trình duyệt theo 3 chế độ: HƯỚNG DẪN (chỉ từng bước), LÀM CÙNG (AI chỉ, bạn bấm), THỰC HIỆN (AI tự bấm khi có quyền điều khiển); luôn dừng ở đăng nhập, thanh toán, mã OTP. Dùng trên macOS và Windows. Từ khóa: đọc màn hình, chụp màn hình, máy báo lỗi, hướng dẫn bấm, thao tác giúp, điều khiển máy tính, làm giúp trên web, cài đặt máy."
---

# /ts-tro-ly-may-tinh — Trợ lý thao tác máy tính

> Gửi ảnh màn hình hoặc nói việc cần làm, AI giải thích đang thấy gì và giúp bạn làm từng bước — hoặc tự làm giúp khi đã được cấp quyền,
> luôn dừng lại trước những bước nhạy cảm. Kết quả: hướng dẫn đánh số mỗi bước một hành động, hoặc việc đã làm xong kèm bằng chứng và cách hoàn tác.

**Loại Bộ Não:** CHỈ LƯU (chỉ lưu khi người dùng yêu cầu)

## Khi nào dùng
- Máy hoặc trang web hiện thông báo lỗi, không biết là gì, làm gì tiếp.
- Không tìm thấy nút/cài đặt trong Facebook, Ads Manager, Canva, Google Drive, Zalo PC, Windows, macOS…
- Muốn được hướng dẫn từng bước khi làm việc mới trên máy (xuất file, đổi cài đặt, tải ứng dụng chính thức).
- Muốn AI tự thao tác giúp việc lặp lại trên trình duyệt (điền form, sao chép dữ liệu) khi môi trường có công cụ điều khiển máy/trình duyệt.

**Không dùng khi:** đã có kết nối chính thức làm được việc đó (vd đọc Google Sheets, số liệu quảng cáo) → dùng kết nối qua
`/ts-ket-noi-ung-dung` sẽ an toàn và nhanh hơn; chỉ cần đọc số liệu trong ảnh → `/ts-doc-so-lieu-hinh-anh`; cần tự động theo lịch → `/ts-lap-lich-tu-dong`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

(Riêng skill này chỉ lưu khi người dùng yêu cầu.)

## Quy trình AI thực hiện

Nguyên tắc: **ưu tiên API hoặc công cụ chuyên dụng khi có; chỉ dùng điều khiển giao diện (bấm, gõ) khi cần.**

### Bước 1 — Xác định bối cảnh
Hỏi phần chưa rõ (gợi ý A-B-C-D):
- Hệ điều hành: (A) Windows · (B) macOS · (C) Điện thoại · (D) Không biết (AI đoán từ ảnh, hỏi xác nhận).
- Ứng dụng/trang web đang mở, mục tiêu cần đạt ("xuất file báo cáo", "tắt thông báo", "sửa lỗi không đăng được bài").
- Trạng thái hiện tại: gửi ảnh chụp màn hình.

Cách chụp màn hình (hướng dẫn nếu người dùng chưa biết):
- Windows: `Windows + Shift + S` (chọn vùng) hoặc phím `PrtScn`.
- macOS: `Cmd + Shift + 4` (chọn vùng) hoặc `Cmd + Shift + 3` (cả màn hình).

### Bước 2 — Đọc màn hình
- Mô tả điều quan sát được: ứng dụng, tiêu đề cửa sổ, thông báo lỗi (chép nguyên văn), các nút đang thấy.
- Ghi rõ phần chưa chắc: mờ, bị cắt, quá nhỏ. **Ảnh mờ/bị cắt/giao diện không khớp → xin ảnh mới thay vì đoán vị trí nút.**
- Giải thích lỗi bằng lời dễ hiểu, nêu 1–3 nguyên nhân khả dĩ (ghi là giả thuyết) và cách kiểm tra.
- Ảnh có mật khẩu, OTP, số thẻ, thông tin cá nhân → nhắc người dùng che/xóa và không chép lại.

### Bước 3 — Chọn một trong 3 chế độ
| Chế độ | Ai bấm | Khi nào dùng |
|---|---|---|
| `HƯỚNG DẪN` | Người dùng tự làm theo danh sách bước | Mặc định; khi không có công cụ điều khiển hoặc người dùng muốn tự học |
| `LÀM CÙNG` | AI chỉ từng bước, người dùng bấm rồi gửi ảnh mới, AI kiểm tra và chỉ bước tiếp | Việc dễ sai, giao diện hay thay đổi, người dùng chưa quen |
| `THỰC HIỆN` | AI tự bấm/gõ qua công cụ điều khiển máy/trình duyệt đã được cấp quyền | Môi trường có công cụ điều khiển, việc lặp lại, người dùng đồng ý rõ ràng |

Hỏi người dùng chọn (gợi ý dựa trên tình huống). Chế độ THỰC HIỆN chỉ dùng khi môi trường thật sự có công cụ điều khiển máy/trình duyệt và người dùng đã cấp quyền.

### Bước 4 — Thực hiện theo chế độ
**HƯỚNG DẪN:** đánh số từng bước, **mỗi bước chỉ một hành động**, ghi đúng tên nút như trên màn hình (kèm vị trí: "góc trên bên phải").
Có khác biệt Windows/macOS thì ghi cả hai. Ví dụ:
1. Bấm biểu tượng **bánh răng** (Cài đặt) ở góc trên bên phải.
2. Chọn **Quyền riêng tư**.
3. …

**LÀM CÙNG:** đưa 1–3 bước → chờ người dùng làm và gửi ảnh → kiểm tra đúng chưa → bước tiếp. Sai thì hướng dẫn quay lại.

**THỰC HIỆN:** vòng lặp ngắn **quan sát → hành động → kiểm tra**:
- Trước thao tác: xác định dữ liệu có thể bị thay đổi và cách quay lại trạng thái trước (nếu có).
- Trước khi nhập dữ liệu: kiểm tra đúng trường, đúng tài khoản, đúng trang.
- Sau mỗi bước quan trọng: chụp/đọc lại màn hình xác nhận kết quả.
- Giao diện khác dự kiến → dừng, mô tả và hỏi người dùng.

### Bước 5 — Cổng an toàn (bắt buộc dừng)
AI **dừng lại và trao quyền cho người dùng** khi gặp:
- **Đăng nhập** (nhập mật khẩu, quét mã, xác minh danh tính) → người dùng tự nhập, AI không xem/không ghi.
- **Thanh toán** (nhập thẻ, xác nhận mua, nạp tiền, bật quảng cáo tốn tiền).
- **Mã OTP / mã xác thực 2 lớp** → không bao giờ yêu cầu người dùng đọc mã cho AI.
- **Quyền hệ thống** (cấp quyền ứng dụng, quyền quản trị, cài phần mềm, tắt diệt virus).
- **Dữ liệu nhạy cảm** (thông tin cá nhân khách, giấy tờ, tài chính).

AI **không tự**: gửi nội dung/tin nhắn, mua hàng, xóa dữ liệu, đổi mật khẩu, cài phần mềm, cấp quyền, đăng nhập hoặc xác nhận giao dịch.
Ở bước cuối có tác động ra bên ngoài, nêu **chính xác** thao tác sắp làm ("Bấm nút **Đăng** để đăng bài lên Trang Tiệm bánh Mây") và chờ người dùng gõ **"đồng ý"**.

### Bước 6 — Báo kết quả, xác minh và hoàn tác
- Chế độ HƯỚNG DẪN: danh sách bước + dấu hiệu nhận biết đã làm đúng.
- Chế độ THỰC HIỆN: báo **thao tác đã làm**, **bằng chứng kiểm tra** (ảnh/màn hình sau khi làm, khi công cụ cho phép), **bước còn chờ** người dùng.
- Khi có thay đổi dữ liệu: bàn giao nhật ký thao tác (bước, thời gian, kết quả), cảnh báo nếu có, và **cách hoàn tác**.
- Không để mật khẩu, OTP, token hoặc thông tin thanh toán xuất hiện trong nhật ký/chat.

### Checklist chất lượng trước khi giao
- [ ] Đã xác định hệ điều hành, ứng dụng, mục tiêu; ảnh đủ rõ hoặc đã xin ảnh mới.
- [ ] Mỗi bước hướng dẫn chỉ một hành động, đúng tên nút.
- [ ] Đã dừng ở mọi bước đăng nhập, thanh toán, OTP, quyền hệ thống, dữ liệu nhạy cảm.
- [ ] Hành động có tác động ra ngoài đã được người dùng "đồng ý" trước.
- [ ] Có bằng chứng kết quả và cách hoàn tác (chế độ THỰC HIỆN).

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** mở sẵn ứng dụng/trang web đang gặp vấn đề; biết chụp màn hình (Windows: `Windows + Shift + S`; macOS: `Cmd + Shift + 4`);
nếu muốn AI tự thao tác, môi trường AI của bạn cần có tính năng điều khiển máy tính/trình duyệt và bạn phải bật quyền cho nó.

1. Gõ `/ts-tro-ly-may-tinh` kèm 1 câu việc cần làm, đính kèm ảnh chụp màn hình hiện tại.
2. Trả lời câu hỏi AI: Windows hay macOS, đang dùng ứng dụng gì.
3. Chọn chế độ: **A. HƯỚNG DẪN** (tôi tự làm) · **B. LÀM CÙNG** (chỉ từng bước, tôi gửi ảnh) · **C. THỰC HIỆN** (AI làm giúp, nếu có quyền).
4. Làm theo từng bước. Thấy màn hình khác với mô tả → chụp ảnh gửi ngay, đừng bấm đoán.
5. Gặp ô mật khẩu, mã OTP, thanh toán → **bạn tự nhập**, không đọc mã cho AI, không dán vào chat.
6. Khi AI hỏi "đồng ý" trước bước cuối (đăng, gửi, lưu thay đổi) → đọc kỹ rồi mới trả lời.
7. Muốn lưu lại hướng dẫn để lần sau làm lại: gõ **"lưu lại"** (AI lưu vào Bộ Não nếu có).

## Câu lệnh mẫu
- `/ts-tro-ly-may-tinh Windows báo lỗi này khi mở file Excel khách hàng, là gì và sửa sao? [đính kèm ảnh]`
- `/ts-tro-ly-may-tinh hướng dẫn tôi xuất danh sách đơn hàng từ trang quản trị shop ra file Excel trên macOS`
- `/ts-tro-ly-may-tinh làm cùng tôi: đổi ảnh đại diện Fanpage spa Hồng, tôi gửi ảnh từng bước`
- `/ts-tro-ly-may-tinh tự điền giúp 10 dòng học viên khóa quay video từ file này vào form Google, dừng trước khi bấm Gửi`

## Kết quả nhận được
- Giải thích màn hình/lỗi bằng lời dễ hiểu, phần chắc chắn và phần còn nghi vấn.
- Chế độ HƯỚNG DẪN: danh sách bước đánh số, mỗi bước một hành động, có ghi chú Windows/macOS.
- Chế độ LÀM CÙNG: hướng dẫn theo vòng, kiểm tra qua ảnh sau mỗi bước.
- Chế độ THỰC HIỆN: việc đã làm, bằng chứng, bước còn chờ, nhật ký thao tác và cách hoàn tác.

## Bước cuối — Lưu vào Bộ Não Thứ 2

> Riêng skill này: chỉ lưu khi người dùng **yêu cầu** (vd gõ "lưu lại"). Không yêu cầu thì bỏ qua toàn bộ bước này.

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-tro-ly-may-tinh-<chu-de-khong-dau>/`.
2. Lưu hướng dẫn thao tác đã làm thành công (các bước, hệ điều hành, ứng dụng, lỗi gặp và cách xử lý, cách hoàn tác) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-tro-ly-may-tinh
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd huong-dan, windows, sua-loi>]
   ---
   ```
   Kèm theo các file phụ (nếu có): ảnh minh họa các bước (đã che thông tin cá nhân, mật khẩu, OTP). Không lưu nhật ký có thông tin đăng nhập hay thanh toán.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-tro-ly-may-tinh · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không tự gửi nội dung, mua hàng, xóa dữ liệu, đổi mật khẩu, cài phần mềm, cấp quyền, đăng nhập hoặc xác nhận giao dịch.
- Không yêu cầu người dùng gửi mật khẩu/mã OTP trong hội thoại; không ghi các thông tin này vào nhật ký.
- Dừng ngay nếu giao diện khác dự kiến, xuất hiện đăng nhập, thanh toán, quyền hệ thống hoặc dữ liệu nhạy cảm.
- Không đoán vị trí nút khi ảnh mờ; xin ảnh mới.
- Chỉ tải phần mềm từ trang chính thức của hãng; cảnh báo nếu trang/ứng dụng có dấu hiệu lừa đảo (địa chỉ lạ, đòi mã OTP, đòi chuyển tiền).
- Trước thao tác có thể làm mất dữ liệu, nhắc người dùng sao lưu.

## Skill liên quan
- Trước: `/ts-ket-noi-ung-dung` (nếu có cách kết nối chính thức) · Sau: `/ts-doc-so-lieu-hinh-anh`, `/ts-lap-lich-tu-dong`, `/ts-tao-app`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
