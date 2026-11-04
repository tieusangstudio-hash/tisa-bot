---
name: ts-gan-ma-qr
description: "Gọi bằng /ts-gan-ma-qr. Gắn mã VietQR (SePay) vào landing page hoặc trang bán hàng để khách mở app ngân hàng quét là chuyển đúng số tiền, đúng nội dung: 4 kiểu đặt QR (khối thanh toán, thẻ bảng giá, cửa sổ bật lên khi bấm Mua, QR đổi theo gói), kèm thông tin chuyển khoản, nút chép nội dung. Không cần máy chủ. Từ khóa: gắn mã QR, VietQR, QR chuyển khoản, nhúng QR vào trang, SePay QR, QR thanh toán, mã QR ngân hàng, nút mua ngay."
---

# /ts-gan-ma-qr — Gắn mã VietQR SePay vào trang

> Thêm mã QR chuyển khoản vào trang của bạn: khách mở app ngân hàng, quét là **tự điền sẵn** ngân hàng, số tài khoản,
> số tiền và nội dung. Chỉ là một ảnh — không cần máy chủ, trang tĩnh nào cũng gắn được.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Đã có landing page (từ `/ts-landing-page` hoặc tự làm) và muốn thêm chỗ thanh toán bằng QR.
- Bảng giá có nhiều gói, mỗi gói cần 1 QR đúng số tiền.
- Muốn nút "Mua ngay" bấm vào là hiện QR (cửa sổ bật lên).
- Muốn in QR (standee) đặt ở quầy/cửa hàng.
- QR trên trang bị lỗi: không hiện, sai số tiền, quét không được.

**Không dùng khi:** muốn trang **tự biết** khách đã trả tiền và tự chuyển sang trang cảm ơn → `/ts-cai-thanh-toan`;
muốn có tiền là báo điện thoại → `/ts-bao-don-telegram`; chưa có trang → `/ts-landing-page`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Hỏi rõ (1 lượt)
Theo `references/_chung/clarification-gate.md`:
1. Trang cần gắn ở đâu? (file `index.html`, thư mục, hoặc LadiPage/Canva/WordPress)
2. Ngân hàng, số tài khoản nhận, tên chủ tài khoản (số tài khoản là thông tin công khai để nhận tiền — không phải mật khẩu).
3. Sản phẩm/gói và **số tiền** từng gói (hoặc để khách tự nhập — chỉ dùng cho ủng hộ/đặt cọc linh hoạt).
4. Nội dung chuyển khoản muốn khách ghi: tên gói (vd `KHOABANH`) hay mã đơn riêng từng khách (cần `/ts-cai-thanh-toan`).
5. Kiểu đặt QR: A. Khối thanh toán riêng · B. QR trong thẻ bảng giá · C. Bấm "Mua ngay" hiện cửa sổ QR · D. QR in standee.
6. Đã liên kết tài khoản này với SePay chưa? (chưa liên kết vẫn tạo được QR, nhưng sẽ không tự đối soát/báo đơn)

### Bước 2 — Tạo đường dẫn ảnh QR
```
https://vietqr.app/img?acc=<SỐ_TK>&bank=<NGÂN_HÀNG>&amount=<SỐ_TIỀN>&des=<NỘI_DUNG>&template=<KIỂU>
```
| Tham số | Bắt buộc | Ghi chú |
|---|---|---|
| `acc` | Có | Số tài khoản (chữ, số; ≤ 19 ký tự) |
| `bank` | Có | Tên ngân hàng theo danh sách `https://vietqr.app/banks.json` (tên ngắn, mã, BIN hoặc tên gọi khác), vd `Vietcombank`, `MBBank`, `Techcombank`, `BIDV`, `ACB` |
| `amount` | Không | Số nguyên VND, **không** dấu chấm/phẩy (`690000`). Bỏ trống → khách tự nhập |
| `des` | Không | Nội dung chuyển khoản: chữ và số **không dấu**, không khoảng trắng, ngắn (vd `KHOABANH690`) |
| `template` | Không | Trống = QR có logo VietQR · `compact` = gọn, có logo NAPAS/ngân hàng · `qronly` = chỉ mã QR · `standee` = in để quầy |
| `showinfo`, `holder`, `store` | Không | Hiện thông tin tài khoản, tên chủ TK (IN HOA không dấu), tên cửa hàng ngay trên ảnh |
| `download` | Không | `true` → bấm link là tải ảnh về (dùng để in) |

- Tài liệu SePay hiện dùng `https://vietqr.app/img`; nhiều mẫu cũ dùng `https://qr.sepay.vn/img` với **cùng tham số**.
  Luôn mở thử link ảnh trong trình duyệt; không hiện thì đổi sang đường dẫn còn lại và đọc lại tài liệu SePay
  (`https://docs.sepay.vn/tao-qr-code-vietqr-dong.html`) — tài liệu mới nhất được ưu tiên.
- Chưa chắc tên ngân hàng → mở `banks.json`, tìm đúng tên. Sai tên ngân hàng là lỗi hay gặp nhất.

### Bước 3 — Chọn mẫu và gắn vào trang
Code đầy đủ 4 mẫu (HTML + Tailwind + JavaScript): `references/mau-nhung-qr.md`. Bảng tra nhanh, 5 hàm JavaScript tiện ích,
xử lý lỗi chi tiết: `references/sepay-embed-guide.md`.

| Mẫu | Dùng khi | Ghi chú |
|---|---|---|
| 1. Khối thanh toán | Trang 1 sản phẩm, 1 giá | QR + bảng thông tin chuyển khoản bên dưới |
| 2. QR tạo bằng JavaScript | Nhiều sản phẩm, khách chọn gói/số lượng | Đổi gói → đổi số tiền & nội dung trên QR |
| 3. Thẻ bảng giá có QR | 2–3 gói giá | Mỗi thẻ 1 QR `template=compact` |
| 4. Cửa sổ bật lên | Muốn trang gọn, bấm "Mua ngay" mới hiện QR | Đóng bằng nút X hoặc bấm ra ngoài |

Mọi mẫu **luôn** có: số tiền to rõ (định dạng `690.000đ`) · tên ngân hàng · số tài khoản · tên chủ tài khoản ·
nội dung chuyển khoản + **nút "Chép"** · dòng "Mở app ngân hàng → Quét QR → Kiểm tra nội dung → Xác nhận" ·
liên hệ Zalo hỗ trợ · `alt="Mã QR chuyển khoản"` · `loading="lazy"`. Chữ hiển thị 100% tiếng Việt.

Trang trên LadiPage/Canva/WordPress: thêm phần tử **Ảnh**, dán link ảnh QR vào ô đường dẫn ảnh (hoặc tải ảnh QR về bằng
`download=true` rồi tải lên); thêm khối chữ ghi thông tin chuyển khoản.

### Bước 4 — Trình bản nháp (CỔNG DUYỆT 1)
Trình: link ảnh QR từng gói · đoạn code/khối sẽ thêm và **vị trí** trên trang · chữ hướng dẫn hiển thị.
> "Bạn mở thử link ảnh QR, quét bằng app ngân hàng (chưa cần bấm chuyển) xem đúng tên chủ tài khoản, số tiền, nội dung chưa.
> Đúng thì gõ **duyệt** để mình gắn vào trang."

### Bước 5 — Gắn & kiểm tra
- [ ] QR hiện trên điện thoại và máy tính; quét bằng 2 app ngân hàng khác nhau → đúng **tên chủ TK, số tiền, nội dung**.
- [ ] Số tiền trên QR khớp số tiền in trên trang và bảng giá.
- [ ] Nút "Chép" chép đúng nội dung; cửa sổ bật lên đóng được trên điện thoại.
- [ ] Không có khóa API/token trong trang (QR chỉ chứa thông tin nhận tiền công khai).
- [ ] Đưa trang lên lại bằng `/ts-dua-web-len-mang` và kiểm tra trên link thật.

| Lỗi | Cách sửa |
|---|---|
| Ảnh QR không hiện | Sai `bank` → tra `banks.json`; sai số TK; thử đổi `vietqr.app/img` ↔ `qr.sepay.vn/img` |
| Sai số tiền | `amount` có dấu chấm/phẩy hoặc số lẻ → dùng số nguyên `690000` |
| Nội dung bị mất/sai | Có dấu tiếng Việt, khoảng trắng, ký tự đặc biệt → viết liền không dấu, mã hóa URL |
| Quét không được | Ảnh quá nhỏ (< 200px) hoặc bị kéo méo → để vuông, ≥ 256px trên điện thoại |

### Bước 6 — Gợi ý bước tiếp
Muốn tự xác nhận đơn → `/ts-cai-thanh-toan` · có tiền là báo điện thoại → `/ts-bao-don-telegram` ·
tự gửi sản phẩm → `/ts-giao-hang-tu-dong`.

**CỔNG DUYỆT 2:** "QR đã gắn và kiểm tra xong. Gõ **duyệt** để lưu cấu hình vào Bộ Não."

### Ví dụ minh họa (dữ liệu giả định)
*Tiệm bánh Mây*, khóa học 690.000đ, tài khoản Vietcombank 0123456789 (số giả):
`https://vietqr.app/img?acc=0123456789&bank=Vietcombank&amount=690000&des=KHOABANH690&template=compact`

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** tên ngân hàng, số tài khoản, tên chủ tài khoản (đúng như trên app ngân hàng), giá từng gói, file trang hoặc
quyền chỉnh trang trên LadiPage/Canva/WordPress. (Nên có tài khoản SePay đã liên kết ngân hàng — xem `/ts-cai-thanh-toan`.)

1. Gõ `/ts-gan-ma-qr` kèm: trang nào, ngân hàng nào, giá bao nhiêu.
2. Chọn kiểu đặt QR (A-B-C-D).
3. AI gửi link ảnh QR → bấm mở trên điện thoại hoặc máy tính → mở app ngân hàng → **Quét QR** → xem tên chủ tài khoản,
   số tiền, nội dung đã đúng chưa → **thoát ra, chưa cần chuyển**.
4. Gõ **duyệt** để AI gắn vào trang.
   - File HTML: AI sửa file giúp, rồi bạn mở `index.html` xem (macOS: Finder → nhấp đúp; Windows: File Explorer → nhấp đúp).
   - LadiPage/Canva/WordPress: AI đưa link ảnh + đoạn chữ, bạn thêm phần tử **Ảnh** → dán link → thêm khối chữ → **Lưu/Xuất bản**.
5. Đưa trang lên lại (`/ts-dua-web-len-mang`), mở link trên điện thoại, quét thử lần cuối (có thể chuyển thử 2.000đ).
6. Gõ **duyệt** để lưu vào Bộ Não.

## Câu lệnh mẫu
- `/ts-gan-ma-qr gắn QR Vietcombank vào trang bán khóa học làm bánh 690k, đặt ở cuối trang, có nút chép nội dung.`
- `/ts-gan-ma-qr bảng giá 3 gói chăm sóc da 990k, 1.990k, 3.490k của spa Hồng — mỗi gói 1 QR trong thẻ giá.`
- `/ts-gan-ma-qr nút Mua ngay trên trang nến thơm bấm vào thì hiện cửa sổ QR 390k, tài khoản MBBank.`
- `/ts-gan-ma-qr tạo QR standee cho quầy quán cà phê, khách tự nhập số tiền, tải ảnh về để in.`

## Kết quả nhận được
- Link ảnh QR cho từng gói (đã kiểm tra tham số).
- Khối HTML đã gắn vào trang (hoặc link ảnh + đoạn chữ để dán vào LadiPage/Canva/WordPress).
- Checklist kiểm tra QR + bảng xử lý lỗi.
- Gợi ý bước tiếp: tự xác nhận đơn, báo đơn, giao hàng tự động.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-gan-ma-qr-<chu-de-khong-dau>/`.
2. Lưu cấu hình đã gắn thành `ket-qua.md` (trang đã gắn + link trang, ngân hàng + 4 số cuối tài khoản, bảng gói – số tiền –
   nội dung chuyển khoản – link ảnh QR, kiểu đặt QR, ngày kiểm tra), mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-gan-ma-qr
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `khoi-qr.html` (đoạn code đã gắn). Không lưu mật khẩu, OTP, khóa API.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-gan-ma-qr · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Luôn để người dùng **quét thử và xác nhận tên chủ tài khoản** trước khi gắn — sai số tài khoản là mất tiền của khách.
- QR chỉ chứa thông tin nhận tiền (công khai). Không bao giờ đặt khóa API, token webhook trong trang.
- Không dùng QR của người khác, không đổi số tài khoản trên trang của người khác.
- Số tiền và nội dung trên QR phải khớp giá niêm yết; đổi giá thì cập nhật cả QR.
- Không có tự xác nhận (chỉ QR tĩnh) → ghi rõ trên trang "Shop xác nhận đơn trong … phút qua Zalo", tránh khách hoang mang.
- Đưa trang có QR lên mạng là hành động công khai → chờ người dùng nói "duyệt".

## Skill liên quan
- Trước: `/ts-landing-page` · `/ts-cai-thanh-toan`
- Sau: `/ts-dua-web-len-mang` · `/ts-bao-don-telegram` · `/ts-giao-hang-tu-dong`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
