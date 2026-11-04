# Cấu trúc 5 tệp hồ sơ (mẫu chuẩn)

Ghi vào `01-ho-so/` của Bộ Não Thứ 2, **đúng tên tệp** dưới đây. Mỗi tệp mở đầu bằng frontmatter YAML.

| Tệp | Nội dung | Skill hay đọc |
|---|---|---|
| `01-ho-so-doanh-nghiep.md` | Tên, mô hình, khu vực, lịch sử, năng lực, bằng chứng | gần như mọi skill |
| `02-san-pham-dich-vu.md` | Từng sản phẩm/gói: giá, lợi ích, ưu đãi, CTA | bán hàng, quảng cáo, offer |
| `03-khach-hang-muc-tieu.md` | Nhóm khách, nỗi đau, mong muốn, rào cản, hành trình | content, quảng cáo, chiến lược |
| `04-thuong-hieu-noi-dung.md` | Giọng văn, xưng hô, màu, font, logo, nhân vật đại diện | content, ảnh, video AI |
| `05-muc-tieu-quy-tac-lien-he.md` | Mục tiêu, KPI, ngân sách, kênh, liên hệ, ID tài khoản QC | chiến lược, quảng cáo, báo cáo |

Quy ước chung:

- Dữ liệu thiếu ghi `[CẦN BỔ SUNG]`, giả định ghi `[GIẢ ĐỊNH]`, chưa được công bố ghi `[NỘI BỘ]`.
- `cap-nhat:` là ngày ghi tệp gần nhất (YYYY-MM-DD). `trang-thai:` = `chua-dien` (mẫu trống do
  `/ts-cai-dat-bo-nao` tạo) → `nhap` (đang soạn, chưa duyệt) → `da-xac-nhan` (người dùng đã duyệt).
- Mẫu dưới đây là bản **đầy đủ hơn** mẫu trống trong Bộ Não: giữ mọi mục của mẫu trống, chỉ thêm mục.
- Không lưu mật khẩu, OTP, token, số thẻ, dữ liệu nhạy cảm của khách.
- Liên kết chéo giữa các tệp bằng cú pháp Obsidian `[[01-ho-so/02-san-pham-dich-vu|Sản phẩm]]`.

---

## Mẫu 1 — `01-ho-so/01-ho-so-doanh-nghiep.md`

```markdown
---
loai: ho-so
tep: 01-ho-so-doanh-nghiep
cap-nhat: <YYYY-MM-DD>
trang-thai: nhap
---

# Hồ sơ doanh nghiệp — <Tên thương hiệu>

## Tóm tắt 1 câu
<Thương hiệu> giúp <khách hàng> <đạt kết quả> bằng <cách làm/sản phẩm>.

## Thông tin chung
| Mục | Nội dung |
|---|---|
| Tên thương hiệu | |
| Tên pháp lý (nếu có) | |
| Hình thức | cá nhân / hộ kinh doanh / công ty / thương hiệu cá nhân |
| Lĩnh vực | |
| Khu vực phục vụ | |
| Năm bắt đầu | |
| Quy mô đội ngũ | |
| Người sáng lập / người đại diện | |

## Mô hình kinh doanh tóm tắt
- Kiếm tiền từ đâu:
- Kênh bán chính:
- Đối tác quan trọng:

## Câu chuyện thương hiệu
<3–5 câu: vì sao bắt đầu, đã vượt qua điều gì, sứ mệnh.>

## Năng lực & bằng chứng (chỉ ghi điều có thật)
| Bằng chứng | Chi tiết | Được phép công khai? | Nguồn/tệp minh chứng |
|---|---|---|---|

## Điểm khác biệt (USP)
- …

## Liên kết
- Sản phẩm: [[01-ho-so/02-san-pham-dich-vu|Sản phẩm & dịch vụ]]
- Khách hàng: [[01-ho-so/03-khach-hang-muc-tieu|Khách hàng mục tiêu]]
```

## Mẫu 2 — `01-ho-so/02-san-pham-dich-vu.md`

```markdown
---
loai: ho-so
tep: 02-san-pham-dich-vu
cap-nhat: <YYYY-MM-DD>
trang-thai: nhap
---

# Sản phẩm & dịch vụ — <Tên thương hiệu>

## Bảng tổng quan
| Sản phẩm/gói | Loại | Giá bán | Giá gốc/neo | Chi phí mỗi đơn | Vai trò | Kết quả khách nhận được | Trạng thái |
|---|---|---|---|---|---|---|---|
| | | | | | chủ lực / mồi / nâng cấp / duy trì | | đang bán / sắp ra / ngừng |

## <Tên sản phẩm 1>
- **Mô tả ngắn / gồm những gì:**
- **Thời gian để khách thấy kết quả:**
- **Giá & điều kiện:** (đã gồm thuế/phí chưa, thời hạn ưu đãi)
- **Dành cho ai:**
- **Giải quyết vấn đề gì:**
- **Lợi ích chính (3 ý):**
- **Bằng chứng:**
- **Ưu đãi / quà tặng:**
- **Bảo hành / cam kết (chỉ ghi điều thật sự áp dụng):**
- **CTA chuẩn:** (vd "Nhắn 'TƯ VẤN' để nhận bảng giá")

## Câu hỏi thường gặp về sản phẩm
| Câu hỏi | Trả lời chuẩn |
|---|---|
```

## Mẫu 3 — `01-ho-so/03-khach-hang-muc-tieu.md`

```markdown
---
loai: ho-so
tep: 03-khach-hang-muc-tieu
cap-nhat: <YYYY-MM-DD>
trang-thai: nhap
---

# Khách hàng mục tiêu — <Tên thương hiệu>

## Nhóm khách chính
| Mục | Nội dung |
|---|---|
| Tên gọi nhóm | (vd "Mẹ bỉm bận rộn 28–38 tuổi") |
| Độ tuổi, giới tính | |
| Nghề nghiệp, thu nhập | |
| Nơi sống | |
| Bối cảnh hằng ngày | |

## Nỗi đau (trước khi mua)
1. …

## Mong muốn (sau khi mua)
1. …

## Rào cản khiến khách chần chừ
| Rào cản | Cách gỡ (bằng chứng/ưu đãi/giải thích) |
|---|---|

## Câu khách hay hỏi / hay nói (giữ nguyên lời khách)
- "…"

## Kênh khách hay dùng
- …

## Hành trình mua
Biết đến → quan tâm → hỏi/nhắn tin → so sánh → mua → dùng → giới thiệu/mua lại.
<Ghi điểm chạm cụ thể ở từng bước.>

## Nhóm khách phụ (nếu có)
- …
```

## Mẫu 4 — `01-ho-so/04-thuong-hieu-noi-dung.md`

```markdown
---
loai: ho-so
tep: 04-thuong-hieu-noi-dung
cap-nhat: <YYYY-MM-DD>
trang-thai: nhap
---

# Thương hiệu & nội dung — <Tên thương hiệu>

## Định vị
<1 câu: dành cho ai, khác biệt gì, vì sao tin.>

## Giọng văn
- **Tính cách:** (vd gần gũi, chân thành, dễ hiểu)
- **Nên dùng:** câu ngắn, ví dụ đời thường, …
- **Tránh:** từ lóng, cam kết tuyệt đối, …
- **Câu mẫu đúng giọng:** "…"

## Xưng hô
- Thương hiệu tự xưng: (mình / em / chúng tôi / tên riêng)
- Gọi khách: (bạn / anh chị / quý khách / mọi người)

## Màu thương hiệu
| Vai trò | Tên màu | Mã màu |
|---|---|---|
| Màu chính | | `#` |
| Màu phụ | | `#` |
| Màu nhấn / chữ | | `#` |
Bộ màu gốc: (đen vàng / gradient tím / xanh / cam vàng / đỏ cam / trắng cam / màu riêng)

## Font chữ (có dấu tiếng Việt)
- Tiêu đề:
- Nội dung:

## Logo
- Có logo: có / chưa
- Vị trí tệp: `03-tai-lieu-tho/dinh-kem/<ten-logo>.png`
- Quy tắc dùng: (nền sáng/tối, góc đặt, kích thước tối thiểu)

## Phong cách hình ảnh
- (vd ảnh thật, ánh sáng tự nhiên, nền sạch; tránh ảnh stock giả tạo)

## Nhân vật đại diện (dùng cho ảnh và video AI)
| Mục | Mô tả |
|---|---|
| Loại | chủ doanh nghiệp / nhân viên / nhân vật AI / không dùng người |
| Tên gọi | |
| Giới tính, độ tuổi | |
| Ngoại hình | dáng người, khuôn mặt, nước da, kiểu tóc, màu tóc |
| Trang phục mặc định | áo, quần, giày, phụ kiện (mô tả màu, chất liệu) |
| Giọng nói | vùng miền, tốc độ, cảm xúc |
| Ảnh tham chiếu | `03-tai-lieu-tho/dinh-kem/<anh>.jpg` hoặc [CẦN BỔ SUNG] |
| Mô tả tiếng Anh cho AI | (1 đoạn ngắn, vd "Vietnamese woman, early 30s, shoulder-length black hair, white blouse, beige trousers, nude flats, warm friendly smile") |

## Trụ cột nội dung (3–5 chủ đề chính)
1. …

## Kênh đang dùng & tần suất đăng
| Kênh | Tần suất | Mẫu bài hiệu quả nhất |
|---|---|---|

## Mẫu hook & CTA hay dùng
- Hook: …
- CTA: …

## Quy tắc nội dung
- Được nói: …
- Không được nói: …
- Quy định ngành cần tuân thủ: …
```

## Mẫu 5 — `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`

```markdown
---
loai: ho-so
tep: 05-muc-tieu-quy-tac-lien-he
cap-nhat: <YYYY-MM-DD>
trang-thai: nhap
---

# Mục tiêu, quy tắc & liên hệ — <Tên thương hiệu>

## Mục tiêu 30–90 ngày
| Mục tiêu | Con số | Hạn | Ghi chú |
|---|---|---|---|
| Doanh thu / tháng | | | |
| Lead (khách tiềm năng) / tháng | | | |
| Đơn hàng / tháng | | | |

## KPI theo dõi
| KPI | Mục tiêu | Cách đo | Tần suất xem |
|---|---|---|---|
| Chi phí mỗi lead (CPL) chấp nhận được | | | hằng tuần |
| Chi phí mỗi đơn (CPA) tối đa | | | hằng tuần |
| Tỷ lệ chốt (lead → đơn) — hiện tại / mục tiêu | | | hằng tuần |
| Số bài/video mỗi tuần | | | hằng tuần |

## Ngân sách quảng cáo
- Mỗi tháng: … (đồng)
- Phân bổ dự kiến: Facebook …% · TikTok …% · khác …%
- Ngưỡng dừng: (vd CPL vượt … đồng sau 3 ngày)

## Kênh ưu tiên
1. …
2. …
Lịch nội dung dự kiến: … bài/tuần.

## Thông tin liên hệ được phép đưa vào nội dung
| Kênh | Thông tin | Được công khai? |
|---|---|---|
| Điện thoại / Zalo | | |
| Website / landing page | | |
| Địa chỉ | | |
| Fanpage | | |
| Email | | |
| Giờ làm việc | | |

## Tài khoản quảng cáo & Trang (chỉ ID — KHÔNG ghi mật khẩu, token)
| Nền tảng | Tên tài khoản | ID |
|---|---|---|
| Meta — Tài khoản quảng cáo | | `act_...` |
| Meta — Fanpage (Page ID) | | |
| Instagram (nếu có) | | |
| TikTok Ads — Advertiser ID | | |
| TikTok — tài khoản kênh | | |
| Zalo OA | | |

## Quy tắc truyền thông & vận hành
- Những điều AI không được hứa với khách (giảm giá, hoàn tiền, kết quả…):
- Không cam kết tuyệt đối, không so sánh trực tiếp đối thủ (nếu người dùng chọn).
- Ai duyệt bài trước khi đăng:
- Ai nhận lead / xử lý khiếu nại:
- Thông tin chỉ dùng nội bộ: …
- Ngày xác nhận gần nhất: <YYYY-MM-DD>
```
