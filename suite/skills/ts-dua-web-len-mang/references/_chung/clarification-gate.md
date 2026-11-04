# Cổng hỏi rõ trước khi làm (dùng chung)

> Cơ chế dùng chung cho mọi skill quan trọng. Không phải skill riêng, không có lệnh riêng. Mỗi skill gọi
> nó ở bước hỏi đầu tiên.

## Mục đích

Trước khi làm việc quan trọng (trang bán hàng, landing page, cài thanh toán, giao hàng…), AI hỏi người dùng
theo **từng lượt 2–4 câu cho tới khi đủ thông tin** — không đoán mò. Có điểm dừng để không hỏi mãi.

Người dùng vẫn gõ lệnh như bình thường; cổng này tự chạy trước.

## Cách hoạt động

### Hỏi theo lượt
1. **Lượt 1** — hỏi 2–4 câu quan trọng nhất (thiếu là không làm được).
2. **Đối chiếu** — so câu trả lời với danh sách cần có của skill (xem `clarification-checklists.md`,
   hoặc phần "Bước 1" trong SKILL.md).
3. **Lượt 2 (nếu cần)** — hỏi tiếp phần còn trống. Không hỏi lại điều đã trả lời.
4. **Dừng** khi có MỘT trong các điều sau:
   - Đã đủ thông tin bắt buộc, HOẶC
   - Người dùng nói "đủ rồi / cứ làm đi", HOẶC
   - Đã hỏi **3 lượt** (giới hạn cứng) → làm tiếp và ghi rõ giả định.
5. **Xác nhận** — trước khi làm, tóm tắt 1 đoạn "Mình hiểu là…" để người dùng kiểm tra nhanh.

### Cách hỏi (không gây phiền)
- Gộp các câu liên quan vào cùng một lượt.
- Ưu tiên câu **bắt buộc** trước câu **tối ưu** (có thì tốt hơn).
- Cho phép "không biết / bỏ qua" — ghi thành giả định, không hỏi lại.
- **Không hỏi** điều đã biết từ Bộ Não Thứ 2, từ file đang mở hoặc câu trả lời trước.
- Mỗi câu chỉ một quyết định. Có thể đưa lựa chọn A-B-C-D cho dễ trả lời.

### Ghi giả định
Khi bỏ qua hoặc đã hết 3 lượt, ghi rõ:
> *Giả định: coi đây là bán lẻ cho cá nhân, giá dưới 500.000đ vì bạn chưa nói. Sai thì bạn nhắn mình sửa.*

## Hai kiểu giao diện

Viết câu hỏi chạy được ở cả hai môi trường:
- **Có khung chọn đáp án:** đưa 2–4 lựa chọn cho mỗi câu.
- **Chỉ có chữ (mặc định):** hỏi thành danh sách đánh số ngắn gọn.

## Ví dụ

**Người dùng:** `/ts-landing-page làm trang bán khóa học làm bánh`

**Lượt 1:**
> Trước khi làm trang, cho mình hỏi nhanh để khỏi đoán:
> 1. Bạn muốn khách làm **một** việc gì: A. Mua ngay · B. Để lại số điện thoại · C. Nhắn Zalo?
> 2. Khách đến trang từ đâu: A. Quảng cáo Facebook · B. TikTok · C. Bài đăng / nhóm Zalo?
> 3. Bạn có bằng chứng thật nào (phản hồi học viên, ảnh thành phẩm, số học viên)?

**Người dùng:** "Mua ngay, từ quảng cáo Facebook, có 15 ảnh phản hồi."

**Xác nhận:**
> Mình hiểu: trang bán khóa học làm bánh, khách đến từ quảng cáo Facebook, nút chính là "Mua ngay",
> có 15 ảnh phản hồi thật để đặt cạnh lời hứa. Mình bắt đầu làm nhé.
