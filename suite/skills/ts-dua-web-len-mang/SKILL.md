---
name: ts-dua-web-len-mang
description: "Gọi bằng /ts-dua-web-len-mang. Đưa trang web (file HTML, landing page) lên mạng bằng Vercel để có link thật dạng ten-trang.vercel.app hoặc tên miền riêng, có ổ khóa bảo mật. 3 cách: kéo thả không cần cài gì, AI chạy lệnh giúp, hoặc qua kết nối Vercel. Kèm cách cập nhật, quay lại bản cũ, gắn tên miền. Từ khóa: đưa web lên mạng, deploy, Vercel, có link trang, gắn tên miền, đăng trang lên internet, cập nhật trang, link landing page."
---

# /ts-dua-web-len-mang — Đưa trang web lên mạng, có link thật (Vercel)

> Biến file trang web trên máy bạn thành **link thật** (vd `banh-may.vercel.app` hoặc `banhmay.vn`) để gửi khách,
> gắn vào quảng cáo. AI lo phần kỹ thuật, bạn chỉ đăng ký tài khoản và bấm vài nút.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- Đã có file trang (`index.html`) từ `/ts-landing-page` hoặc tự làm, cần link để chia sẻ.
- Đã sửa trang, muốn cập nhật bản mới lên đúng link cũ.
- Bản mới bị lỗi, muốn quay lại bản trước.
- Muốn đổi link `.vercel.app` thành tên miền riêng (vd `tiembanhmay.vn`).

**Không dùng khi:** chưa có trang → `/ts-landing-page`; trang dựng trên LadiPage/Canva/WordPress (các nền tảng đó có
nút "Xuất bản" riêng) → làm theo hướng dẫn của nền tảng; cần gắn mã QR nhận tiền → `/ts-gan-ma-qr`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Hỏi rõ (1 lượt)
Theo `references/_chung/clarification-gate.md`:
1. File/thư mục trang nằm ở đâu? (vd `landing-banh-may/index.html`)
2. Lần đầu đưa lên hay **cập nhật** trang đã có link? (cập nhật → hỏi tên dự án / link cũ)
3. Đã có tài khoản Vercel chưa? Máy dùng **macOS hay Windows**?
4. Trang có **bán hàng / nhận tiền / quảng cáo sản phẩm** không? (ảnh hưởng gói Vercel — xem Bước 2)
5. Có muốn gắn tên miền riêng không? (có thể làm sau)

### Bước 2 — Báo trước về gói Vercel (bắt buộc nói rõ)
Theo quy định sử dụng của Vercel: gói **Hobby (miễn phí) chỉ dành cho dự án cá nhân, phi thương mại**. Trang có
nhận thanh toán, quảng cáo bán sản phẩm/dịch vụ được tính là **thương mại → cần gói Pro (trả phí)**.
- Trang bán hàng thật → nói rõ điều này, để người dùng chọn: nâng Pro, hoặc dùng dịch vụ khác (kiểm tra điều khoản trước).
- Trang thử nghiệm, trang cá nhân, trang xin ủng hộ → Hobby được.
- Giá gói và điều khoản thay đổi theo thời gian → mở `https://vercel.com/pricing` và
  `https://vercel.com/docs/limits/fair-use-guidelines` để kiểm tra bản mới nhất, không nói giá theo trí nhớ.

### Bước 3 — Kiểm tra file trước khi đưa lên
- [ ] Trang chính tên đúng `index.html` (chữ thường), nằm ở **gốc** thư mục.
- [ ] Tên file/thư mục viết thường, không dấu, không khoảng trắng (`cam-on.html`, `hinh-anh/logo.png`).
- [ ] Ảnh gọi bằng đường dẫn tương đối (`hinh-anh/hero.jpg`), không có `C:\...` hay `/Users/...`. Lưu ý Vercel phân biệt hoa/thường.
- [ ] Ảnh nén < 500KB/ảnh; script bên ngoài dùng `https://`.
- [ ] Không có khóa API, token, mật khẩu trong file (ai cũng xem được mã nguồn).
- [ ] Có `title`, `description`, ảnh chia sẻ `og:image`. Không còn `[CẦN BỔ SUNG]` hay `{{...}}`.
Lỗi nào sửa được thì AI sửa luôn và báo lại.

### Bước 4 — Chọn cách đưa lên
| Cách | Cần gì | Hợp với | Cập nhật sau này |
|---|---|---|---|
| **A. AI đưa lên qua kết nối Vercel** | Môi trường có kết nối/công cụ Vercel | Nhanh nhất, học viên không bấm gì | AI đưa lại → cùng link |
| **B. Kéo thả Vercel Drop** | Trình duyệt | Người không rành máy tính (khuyên dùng) | Kéo thư mục mới vào dự án trên trang quản lý |
| **C. AI chạy lệnh Vercel CLI** | Node.js + cửa sổ lệnh | AI có quyền chạy lệnh trên máy | Chạy lại 1 lệnh → cùng link |
| D. Qua GitHub | Tài khoản GitHub | Người đã quen Git | Tự động mỗi lần đẩy code |

Chi tiết cách D, cấu hình `vercel.json`, biến môi trường, lệnh tham khảo: `references/cau-hinh-va-xu-ly-loi.md`.
Trước khi làm thật, đọc `references/official-docs-index.md` và tài liệu chính thức — tài liệu mới nhất được ưu tiên hơn trí nhớ.

**Cách A — qua kết nối Vercel:** nếu đã kết nối Vercel, AI dùng công cụ đưa trang lên (deploy), đọc nhật ký lỗi khi
thất bại, liệt kê các bản cũ để quay lại. Học viên chỉ cần đăng nhập/cho phép kết nối một lần.

**Cách B — Vercel Drop (không cần cài gì):** xem các bước cho học viên ở mục Hướng dẫn. Không đăng nhập vẫn đưa lên được
nhưng link **tạm thời** (có đồng hồ đếm ngược) — phải bấm **Claim your project** và tạo tài khoản để giữ link.

**Cách C — Vercel CLI (AI chạy lệnh):** cần Node.js bản LTS (kiểm tra bằng `node --version`). Dùng `npx` để khỏi cài toàn máy.
```
macOS (Terminal):
  cd ~/Desktop/landing-banh-may
  npx vercel login            # mở trình duyệt để đăng nhập, chỉ làm 1 lần
  npx vercel --prod           # đưa lên bản chính thức, in ra link

Windows (PowerShell):
  cd $HOME\Desktop\landing-banh-may
  npx.cmd vercel login
  npx.cmd vercel --prod
```
- Lần đầu CLI hỏi vài câu: `Set up and deploy?` → **Y** · chọn tài khoản · `Link to existing project?` → **N** (lần đầu) ·
  tên dự án (chữ thường, gạch nối) · thư mục code → `./` · `Want to modify these settings?` → **N** (trang tĩnh không cần build).
- Windows báo "running scripts is disabled" → dùng `npx.cmd` như trên, hoặc mở **Command Prompt** thay PowerShell.
- Chưa có tài khoản mà cần link thử ngay: `npx vercel deploy --temporary` (link tạm, in ra link nhận dự án — **không chia sẻ link nhận**).

### Bước 5 — Kiểm tra sau khi lên mạng
- [ ] Link mở được, có ổ khóa (https) · [ ] Mở trên **điện thoại** đẹp, không vỡ bố cục
- [ ] Ảnh hiện đủ · [ ] Nút, link Zalo/điện thoại, form bấm được · [ ] Mã QR (nếu có) quét được bằng app ngân hàng
- [ ] Không còn chữ mẫu, chữ tiếng Anh sót · [ ] Thử dán link vào Messenger/Zalo xem ảnh chia sẻ hiện đúng

Lỗi thường gặp (chi tiết trong `references/cau-hinh-va-xu-ly-loi.md`):
| Hiện tượng | Nguyên nhân hay gặp | Cách sửa |
|---|---|---|
| 404 Not Found | Không có `index.html` ở gốc / sai chữ hoa | Đổi tên đúng `index.html`, đặt ở gốc thư mục |
| Ảnh không hiện | Đường dẫn tuyệt đối hoặc sai hoa/thường | Dùng `hinh-anh/ten-anh.jpg`, khớp đúng tên file |
| Build Failed | Vercel tưởng là dự án cần build | Framework: **Other**, Build Command & Install Command để trống, Output: `.` |
| Trang cũ vẫn hiện | Trình duyệt nhớ bản cũ | Tải lại mạnh: macOS `Cmd+Shift+R`, Windows `Ctrl+F5` |

### Bước 6 — Cập nhật, quay lại bản cũ, gắn tên miền
- **Cập nhật:** sửa file → đưa lên lại vào **cùng dự án** → link giữ nguyên (cách C: chạy lại `npx vercel --prod` trong
  cùng thư mục; cách B: kéo thư mục mới vào dự án trên trang quản lý). Xem `references/cap-nhat-va-quay-lai.md`.
- **Quay lại bản cũ:** trang quản lý Vercel → dự án → tab **Deployments** → chọn bản chạy tốt → nút **…** →
  **Promote to Production** (hoặc **Instant Rollback**, tùy giao diện).
- **Tên miền riêng:** dự án → **Settings → Domains** → nhập tên miền → **Add** → Vercel hiện bản ghi DNS cần thêm,
  thường là:
  | Cho | Loại | Giá trị (luôn chép theo màn hình Vercel) |
  |---|---|---|
  | `tenmien.vn` | A | IP Vercel đưa (vd `76.76.21.21`) |
  | `www.tenmien.vn` | CNAME | `cname.vercel-dns.com` (hoặc giá trị Vercel đưa) |
  Thêm ở nơi mua tên miền (Mắt Bão, PA Việt Nam, Nhân Hòa, Tenten, GoDaddy…), chờ vài phút đến vài giờ, ổ khóa https tự cấp miễn phí.
  Từng bước cho người không rành: `references/custom-domain-setup.md` và `references/_chung/dns-basics-for-nontech.md`.

### Bước 7 — Báo kết quả (CỔNG DUYỆT)
Trình: link chính thức · tên dự án · cách đã dùng · kết quả checklist Bước 5 · việc còn lại (tên miền, gói Pro).
> "Bạn mở link trên điện thoại kiểm tra giúp mình. Ổn thì gõ **duyệt** để lưu link vào Bộ Não."

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** thư mục trang (có `index.html`), email hoặc tài khoản Google/GitHub để đăng ký Vercel.

**1. Tạo tài khoản Vercel (5 phút, làm 1 lần)**
- Vào `https://vercel.com/signup`.
- Chọn loại gói: **Hobby** (cá nhân, phi thương mại) hoặc **Pro** (trang bán hàng thật — có trả phí, xem Bước 2).
- Nhập tên → bấm **Continue** → chọn **Continue with Google** (dễ nhất) hoặc **Continue with Email** rồi nhập mã gửi về email.
- Thấy trang quản lý (Dashboard) là xong. Không gửi mật khẩu hay mã xác nhận cho AI.

**2. Đưa trang lên bằng kéo thả (cách B — khuyên dùng)**
- Mở `https://vercel.com/drop` (đã đăng nhập).
- Mở thư mục chứa trang trên máy: **macOS** mở Finder · **Windows** mở File Explorer.
- Kéo **cả thư mục** (vd `landing-banh-may`) thả vào ô trên trang Vercel (hoặc bấm chọn **folder** để tải lên).
- Chọn tài khoản (team) → đặt tên dự án (chữ thường, không dấu, vd `banh-may`) → bấm **Deploy**.
- Chờ 10–60 giây → hiện link dạng `banh-may.vercel.app`. Bấm mở thử.
- Nếu làm khi chưa đăng nhập: bấm **Claim your project** trước khi hết giờ đếm ngược, nếu không link sẽ mất.

**3. Hoặc để AI làm (cách A/C):** nói "AI đưa lên giúp tôi". Nếu AI xin chạy lệnh, bạn bấm **Cho phép**; nếu trình duyệt
mở trang đăng nhập Vercel, bạn bấm **Confirm/Xác nhận**. Máy chưa có Node.js: tải bản **LTS** ở `https://nodejs.org`
— macOS mở file `.pkg`, Windows mở file `.msi`, bấm **Next/Continue** đến hết.

**4. Kiểm tra:** mở link trên điện thoại, bấm thử nút, form, mã QR. Gửi ảnh chụp màn hình cho AI nếu thấy lỗi.

**5. Gõ "duyệt"** để AI lưu link vào Bộ Não.

**6. (Tùy chọn) Gắn tên miền:** mua tên miền ở nhà cung cấp bạn tin dùng, nói AI "gắn tên miền … vào trang", AI chỉ từng ô cần điền.

## Câu lệnh mẫu
- `/ts-dua-web-len-mang đưa thư mục landing-banh-may lên mạng giúp tôi, tôi dùng Windows, chưa có tài khoản Vercel.`
- `/ts-dua-web-len-mang tôi vừa sửa giá trên trang spa Hồng, cập nhật lên đúng link cũ spa-hong.vercel.app.`
- `/ts-dua-web-len-mang trang khóa học bị vỡ ảnh sau khi cập nhật, quay lại bản hôm qua giúp tôi.`
- `/ts-dua-web-len-mang gắn tên miền tiembanhmay.vn mua ở Mắt Bão vào trang banh-may.vercel.app.`

## Kết quả nhận được
- Link trang chính thức (https) + tên dự án trên Vercel.
- Kết quả kiểm tra trước và sau khi đưa lên, lỗi đã sửa.
- Hướng dẫn cập nhật / quay lại bản cũ cho lần sau.
- (Nếu cần) bảng bản ghi DNS để gắn tên miền riêng.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-dua-web-len-mang-<chu-de-khong-dau>/`.
2. Lưu thông tin triển khai thành `ket-qua.md` (link chính thức, tên dự án Vercel, cách đưa lên, gói Hobby/Pro, tên miền và
   bản ghi DNS đã thêm, ngày, việc còn lại), mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-dua-web-len-mang
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `vercel.json` đã dùng. **Không lưu** mật khẩu, mã xác nhận, token, link nhận dự án (claim).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-dua-web-len-mang · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Đề xuất ghi link mới vào dòng **Website / landing page** trong `01-ho-so/05-muc-tieu-quy-tac-lien-he.md` (hỏi trước khi ghi đè link cũ).
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Đưa trang lên mạng là **công khai** — luôn trình link/thư mục sẽ đưa lên và chờ người dùng nói "duyệt".
- Không xin mật khẩu, mã OTP, token Vercel trong chat. Đăng nhập do học viên tự bấm trên trình duyệt.
- Không đưa khóa API, token, thông tin khách hàng vào file trang (ai cũng xem được).
- Trang bán hàng trên gói Hobby là trái quy định của Vercel → nói rõ để người dùng tự quyết.
- Link nhận dự án tạm thời (claim) ai có cũng chiếm được dự án → không chia sẻ, không lưu.
- Không xóa dự án/bản cũ khi chưa được người dùng đồng ý.

## Skill liên quan
- Trước: `/ts-landing-page` · `/ts-gan-ma-qr`
- Sau: `/ts-bao-don-telegram` · `/ts-giao-hang-tu-dong` · `/ts-viet-quang-cao` · `/ts-len-camp-facebook`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
