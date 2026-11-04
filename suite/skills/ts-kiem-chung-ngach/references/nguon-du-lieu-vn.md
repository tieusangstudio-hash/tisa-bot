# Nguồn dữ liệu Việt Nam để kiểm chứng ngách

Dùng cho `/ts-kiem-chung-ngach`. Mục tiêu: mỗi nhận định quan trọng có **≥ 3 nguồn độc lập**
(khác nền tảng hoặc khác người đăng), ghi **link + ngày kiểm tra**. Không có số thật thì ghi
"ước lượng" và nói rõ cách ước lượng.

## 1. Bảng nguồn theo tiêu chí

| Tiêu chí | Nên tìm ở đâu | Tìm cái gì (tín hiệu) |
|---|---|---|
| Mức độ đau | Nhóm Facebook, bình luận TikTok/YouTube, Threads, đánh giá 1–3 sao trên sàn | Bài than phiền, câu hỏi lặp lại, cảm xúc mạnh ("mệt quá", "mất tiền oan") |
| Khả năng chi trả | Shopee/Lazada/Tiki/TikTok Shop, Unica/Gitiho/Edumall, trang bán của đối thủ | Giá bán, số đã bán, số đánh giá, có gói cao cấp không |
| Nhu cầu tìm kiếm | Google (gợi ý tự động, "Mọi người cũng hỏi"), Google Trends, YouTube, thanh tìm kiếm TikTok | Số kết quả, gợi ý từ khóa, video nhiều view theo từ khóa |
| Xu hướng | Google Trends (khu vực Việt Nam, 2–5 năm), báo chí, báo cáo thị trường công khai | Đường quan tâm tăng/giảm, theo mùa hay đều |
| Mức cạnh tranh | Google, sàn, Unica/Gitiho, Thư viện quảng cáo Meta (Ads Library), TikTok | Số người bán, chất lượng, ai chạy quảng cáo lâu (đang có lời) |
| Kênh tiếp cận | Nhóm Facebook (số thành viên, số bài/ngày), Zalo (nhóm, OA), TikTok hashtag, kênh YouTube | Nơi khách tụ tập, có cho đăng bài không, mức tương tác |
| Phù hợp người làm | Hồ sơ trong Bộ Não, kết quả thật của người làm | Kinh nghiệm, chứng nhận, khách cũ, nguồn hàng |

## 2. Mẹo tìm kiếm cho từng nền tảng

**Google**
- Gõ cụm từ khách hay gõ (không phải từ ngữ chuyên môn): `cách …`, `… có tốt không`, `… giá bao nhiêu`,
  `… lừa đảo`, `… review`.
- Xem mục "Mọi người cũng hỏi" và gợi ý cuối trang → đó là câu hỏi thật của khách.
- Tìm trong một trang: `site:shopee.vn <từ khóa>`, `site:facebook.com/groups <từ khóa>`,
  `site:unica.vn <từ khóa>`, `site:gitiho.com <từ khóa>`.

**Google Trends** (trends.google.com)
- Chọn Quốc gia: Việt Nam, thời gian: 5 năm qua. So sánh 2–3 từ khóa cùng lúc.
- Ghi lại: đang tăng / đi ngang / giảm / theo mùa (đỉnh tháng nào).

**Sàn TMĐT (Shopee, Lazada, Tiki, TikTok Shop)**
- Lọc "Bán chạy". Ghi 5–10 sản phẩm đầu: giá, "đã bán", số đánh giá, điểm sao.
- Đọc đánh giá 1–3 sao: đó là nỗi đau chưa được giải → cơ hội khác biệt.
- Lưu ý: "đã bán" có thể bị làm đẹp; dùng để so sánh tương đối, không coi là doanh thu chính xác.

**Nền tảng khóa học (Unica, Gitiho, Edumall…)**
- Tìm theo chủ đề: số khóa, giá niêm yết, giá khuyến mãi, số học viên, ngày cập nhật.
- Nhiều khóa nhưng ít học viên → cầu yếu hoặc chất lượng kém; ít khóa mà nhiều học viên → cầu mạnh.

**Nhóm Facebook**
- Tìm theo từ khóa ngành + "cộng đồng", "hội", tên khu vực. Ghi: số thành viên, số bài mới/ngày.
- Tìm trong nhóm bằng ô tìm kiếm: từ khóa nỗi đau ("bị", "lỗi", "không được", "tư vấn giúp").

**TikTok / YouTube**
- Gõ từ khóa, xem 20 video đầu: view, ngày đăng, số bình luận. Đọc bình luận nhiều like nhất.
- Video mới (dưới 3 tháng) mà nhiều view → nhu cầu đang nóng.
- Có thể dùng `/ts-nghien-cuu-youtube` để lấy số liệu YouTube chính xác hơn.

**Threads, Zalo**
- Threads: tìm từ khóa, xem bài than phiền và câu hỏi. Zalo: nhóm cộng đồng, Zalo OA của đối thủ
  (số người quan tâm). Nhiều nhóm Zalo kín → ghi "không truy cập được", không đoán.

**Thư viện quảng cáo Meta (Ads Library)**
- Tìm theo tên đối thủ/từ khóa, quốc gia Việt Nam. Quảng cáo chạy liên tục > 30 ngày thường là quảng cáo
  có lời → chứng tỏ có khách chịu trả tiền.

## 3. Thế nào là "nguồn độc lập"

- Khác nền tảng (Google + Shopee + nhóm Facebook) **hoặc** khác người đăng trên cùng nền tảng.
- 3 bài cùng một người/một trang đăng lại = 1 nguồn.
- Bài quảng cáo của chính người bán chỉ chứng minh "có người bán", không chứng minh "có người mua".

## 4. Cách ghi nguồn

```
- [Mức độ đau] 40+ bình luận than video ít view — https://… — kiểm tra 2026-11-04
- [Khả năng chi trả] Khóa 599k, 1.200 học viên — https://… — kiểm tra 2026-11-04
```

Không mở được trang (bắt đăng nhập, bị chặn) → ghi "không truy cập được", không tự điền số.

## 5. Số lượng tra cứu tối thiểu

Ít nhất **6 lượt tìm kiếm** khác nhau, phủ tối thiểu 4 nhóm nguồn:
1. Google (từ khóa nỗi đau) · 2. Google Trends · 3. Sàn TMĐT hoặc nền tảng khóa học ·
4. Nhóm Facebook/Threads · 5. TikTok/YouTube · 6. Đối thủ (trang bán, quảng cáo).

Nếu môi trường **không có công cụ tìm kiếm web**: nói rõ cho người dùng, đưa danh sách 6 truy vấn để họ tự
tìm và dán kết quả (ảnh chụp/link) vào. Không được chấm điểm khi chưa có dữ liệu thật — ghi "tạm tính" nếu
buộc phải ước lượng.

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
