# 05 - Tư duy xây dựng và code web có hệ thống, và bước ra quyết định trước khi nhận việc

Ngày: 19/11/2026. Nguồn đã đọc: https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md ; https://claude.com/resources/articles/improving-frontend-design-through-skills ; https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics (chỉ đọc qua kết quả tìm kiếm, cần xác minh nguyên văn) ; https://github.com/pbakaus/impeccable ; https://docs.astro.build/en/concepts/why-astro/ ; https://developers.cloudflare.com/workers/static-assets/ ; https://developers.cloudflare.com/workers/static-assets/headers/ ; https://developers.cloudflare.com/pages/ ; https://developers.cloudflare.com/d1/ ; https://developers.cloudflare.com/workers/configuration/versions-and-deployments/rollbacks/ ; https://web.dev/articles/vitals ; https://web.dev/articles/browser-level-image-lazy-loading ; https://web.dev/articles/choose-the-right-image-format ; https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html ; https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html ; https://developers.google.com/search/docs/fundamentals/seo-starter-guide ; https://developers.google.com/search/docs/appearance/structured-data/local-business ; https://ogp.me/ ; https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP ; https://git-scm.com/docs/git-revert ; https://github.com/GoogleChrome/lighthouse ; https://github.com/dequelabs/axe-core. Tệp nội bộ đối chiếu (đọc trực tiếp): `overlay/server/tisa_web_mau.py` (gói Web CRM + Lead Page), `overlay/suite/agents/tisa-quan-tri-web.md`, `assets/goi/them/tisa-thiet-ke-web/` (kỹ năng thiết kế giao diện), `nghien-cuu-dau-noi/70-cloudflare-deploy-web.md`.

Quy ước: "cần xác minh" là chưa đọc được nguồn gốc hoặc nguồn mâu thuẫn. Chỗ ghi "kiến thức chung" là điều phổ biến trong nghề, chưa đọc lại trang gốc hôm nay.

## 3. Tư duy xây dựng web có hệ thống

### 3.1 Thứ tự làm (không nhảy cóc)
| # | Bước | Đầu ra | Chủ cần duyệt? |
|---|---|---|---|
| 1 | Mục tiêu và đối tượng: một việc chính khách phải làm (để lại số, nhắn Zalo, mua, đặt lịch), khách là ai, đến từ kênh nào, xem bằng máy gì | 1 câu mục tiêu + 3 số đo thành công (vd số lead/tuần) | Có |
| 2 | Kiến trúc thông tin: danh sách trang, menu, đường đi từ trang đến việc chính. Ít trang thì tốt | Sơ đồ trang 1 dòng mỗi trang | Có |
| 3 | Wireframe: phác từng trang bằng chữ/ASCII, mỗi khối một mục đích | Wireframe điện thoại trước, máy tính sau | Có |
| 4 | Design tokens: 4 đến 6 màu có tên, 1 đến 2 phông, thang cỡ chữ, thang khoảng cách, bo góc, bóng | `DESIGN.md` hoặc `tokens.css` | Xem nhanh |
| 5 | Component: nút, thẻ, form, menu, khối hero, bảng giá, hỏi đáp. Làm một lần, dùng lại | Thư viện nhỏ trong `components.css` | Không |
| 6 | Nội dung THẬT: chữ viết từ hồ sơ sản phẩm, ảnh thật, giá, cam kết thật. Không để lorem ipsum đến bước 7 | Tệp nội dung đã duyệt | Có |
| 7 | Code: mobile-first, HTML ngữ nghĩa, CSS biến, JS tối thiểu | Mã chạy cục bộ | Không |
| 8 | Kiểm thử: Lighthouse, axe, form, 3 cỡ màn hình, điện thoại thật (mục 3.9) | Báo cáo ngắn | Xem kết quả |
| 9 | Triển khai: bản xem thử `workers.dev` trước, chủ duyệt rồi mới gắn tên miền | Địa chỉ thật + hướng dẫn sửa | Có (trước khi gắn tên miền) |

### 3.2 Chọn công nghệ theo mức độ (đi từ đơn giản nhất)
| Mức | Khi nào | Công nghệ | Đưa lên |
|---|---|---|---|
| 1 | 1 đến 5 trang, ít đổi, không lưu dữ liệu | HTML/CSS/JS thuần, không bước build | Workers Static Assets |
| 2 | Trên 5 trang, dùng chung header/footer, có blog hoặc nội dung dạng markdown, SEO quan trọng | Astro. Tài liệu Astro: mặc định gửi rất ít JavaScript, chỉ các "đảo" tương tác mới nạp mã, dùng được React/Vue/Svelte | build ra `dist/` rồi Static Assets |
| 3 | Phần tương tác nặng (công cụ tính, bảng điều khiển, ứng dụng) | Vite + React | Static Assets (đặt `not_found_handling = "single-page-application"` nếu là SPA) |
| 4 | Cần lưu form, API, webhook (vd thanh toán), đăng nhập, việc chạy định kỳ | Thêm Worker, kèm D1 (SQL kiểu SQLite) hoặc KV/R2 | Worker + `assets`; `run_worker_first` cho đường `/api/*` |

Cloudflare: một yêu cầu khớp tệp tĩnh thì phục vụ luôn mà không chạy mã Worker; không khớp thì chuyển cho Worker nếu có, không có thì 404 (theo tài liệu Static Assets). Trang tài liệu Pages đọc hôm nay có thông báo khuyên dự án MỚI bắt đầu bằng Workers và có hướng dẫn chuyển từ Pages sang Workers, nên mặc định của TISA: Workers Static Assets (khớp hạ tầng hiện có, xem `70-cloudflare-deploy-web.md`). Tài liệu D1 nói có trên cả gói Free và Paid, có Time Travel khôi phục trong 30 ngày; hạn mức gói Free cụ thể: cần xác minh.
Cấu hình tối thiểu:
```jsonc
// wrangler.jsonc
{ "name": "ten-web", "compatibility_date": "2026-11-01",
  "assets": { "directory": "./public", "not_found_handling": "404-page" } }
```

### 3.3 Cấu trúc thư mục chuẩn
```
ten-web/
  README.md          # cách sửa, cách đưa lên, tên miền, người giữ khóa. KHÔNG ghi khóa
  DESIGN.md          # tokens + quy tắc giao diện của web này
  wrangler.jsonc
  package.json       # chỉ khi có bước build
  .gitignore         # node_modules, dist, .env, .dev.vars
  public/            # (hoặc src/ nếu dùng Astro/Vite) thứ được phát đi
    index.html   gioi-thieu/index.html   lien-he/index.html   404.html
    _headers  robots.txt  sitemap.xml  favicon.svg
    assets/css/{tokens.css, base.css, components.css}
    assets/js/main.js
    assets/img/      # WebP/AVIF, SVG cho biểu tượng, có width/height
    assets/fonts/    # woff2 đã cắt tập ký tự
  worker/            # chỉ khi mức 4: src/index.js, migrations/
```
Mỗi trang một thư mục có `index.html` để đường dẫn đẹp (`/lien-he/`), không dấu, không khoảng trắng.

### 3.4 CSS biến và mobile-first
```css
:root{
  --mau-chinh:#0b5fa5; --mau-nhan:#f59e0b; --nen:#ffffff; --chu:#1b1f24; --chu-phu:#4a5560;
  --r:12px; --kc-1:.5rem; --kc-2:1rem; --kc-3:2rem; --kc-4:4rem;
  --co-0:1rem; --co-1:1.25rem; --co-2:1.75rem; --co-3:2.5rem; --rong:68rem;
}
body{margin:0;font:var(--co-0)/1.6 "Phông Của Chủ",system-ui,sans-serif;color:var(--chu);background:var(--nen)}
.khung{max-width:var(--rong);margin-inline:auto;padding-inline:var(--kc-2)}   /* mặc định là điện thoại */
@media (min-width:48rem){ .luoi{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--kc-3)} }  /* mở rộng dần */
@media (prefers-reduced-motion:reduce){ *{animation:none!important;transition:none!important} }
```
Nguyên tắc: viết kiểu cho điện thoại trước, chỉ dùng `min-width` để mở rộng; mọi màu, cỡ, khoảng cách lấy từ biến; không giá trị "ma thuật" rải rác.  Tên biến dùng chữ không dấu.

### 3.5 Truy cập (accessibility) cơ bản
- Tương phản: chữ thường tối thiểu 4.5:1, chữ lớn (18pt trở lên, hoặc 14pt đậm) tối thiểu 3:1 (WCAG 2.2). Thành phần giao diện thường được hiểu là 3:1 (theo tiêu chí 1.4.11; trang đã đọc không nêu thẳng con số, cần xác minh).
- Vùng bấm: WCAG 2.2 AA yêu cầu tối thiểu 24x24 px (có ngoại lệ); mức nâng cao 44x44 px. Kỹ năng `tisa-thiet-ke-web` đã chọn 44 px cho điện thoại, giữ như vậy.
- Mỗi ô form có `<label for>` thật (không chỉ placeholder); cỡ chữ ô nhập từ 16px (iPhone tự phóng to nếu nhỏ hơn: lời trong kỹ năng nội bộ, cần xác minh).
- Focus nhìn thấy được (`:focus-visible`), không xóa viền focus mà không thay thế; dùng được bằng bàn phím.
- Một `<h1>`, các tiêu đề không nhảy cấp; `lang="vi"`; ảnh có `alt` mô tả đúng; ảnh trang trí `alt=""`.
- Tôn trọng `prefers-reduced-motion`. Không video tự phát tiếng, không popup chặn nội dung.
- axe-core bắt được trung bình khoảng 57% lỗi WCAG theo README của nó, nên vẫn phải duyệt tay.

### 3.6 Hiệu năng
- Mục tiêu Core Web Vitals (ở phân vị 75, theo web.dev): LCP không quá 2,5 giây, INP không quá 200 ms, CLS không quá 0,1.
- Ảnh: dùng WebP hoặc AVIF (nén tốt hơn JPEG, kèm bản JPEG/PNG dự phòng khi cần); SVG cho logo và biểu tượng; luôn đặt `width` và `height` để khỏi nhảy bố cục; `loading="lazy"` chỉ cho ảnh dưới màn hình đầu, KHÔNG cho ảnh lớn nhất ở đầu trang (ảnh đó dùng `fetchpriority="high"`).
- Phông: tự host, định dạng woff2, cắt tập ký tự (nhớ giữ nhóm ký tự tiếng Việt), `font-display: swap`, tối đa 2 họ, mỗi họ vài độ đậm (kiến thức chung; kiểm tra chuỗi "Ặ Ở Ữ ệ ợ ỳ" như kỹ năng nội bộ dặn).
- Không thư viện thừa: một hiệu ứng nhỏ thì viết CSS, đừng nạp jQuery, thư viện icon cả bộ, slider nặng. Ngân sách khởi điểm của TISA (kỹ năng nội bộ): tổng ảnh ban đầu dưới 1 MB, mỗi ảnh dưới khoảng 300 KB.
- Bên thứ ba (pixel quảng cáo, chat, bản đồ) nạp sau, đo lại sau khi gắn.

### 3.7 SEO cơ bản (theo hướng dẫn của Google)
- Mỗi trang: `<title>` riêng, ngắn, đúng nội dung; `meta description` 1 đến 2 câu, riêng cho từng trang; `<link rel="canonical">`; `lang="vi"`; địa chỉ đường dẫn có chữ có nghĩa, không dấu.
- Thẻ chia sẻ Open Graph: 4 thẻ bắt buộc là `og:title`, `og:type`, `og:image`, `og:url`; nên thêm `og:description` (theo ogp.me). Ảnh chia sẻ đặt bằng địa chỉ đầy đủ.
- Dữ liệu cấu trúc schema.org dạng JSON-LD, dùng loại cụ thể nhất. Với `LocalBusiness`, Google ghi bắt buộc `name` và `address`; nên thêm `telephone`, `openingHoursSpecification`, `geo`, `url`, `priceRange`. CHỈ thêm `review`/`aggregateRating` khi có đúng điều kiện của Google (trang của chính doanh nghiệp tự chấm điểm cho mình thì không hợp lệ; mặc nhiên không bịa). Kiểm bằng Rich Results Test.
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness","name":"<TÊN THẬT>",
 "address":{"@type":"PostalAddress","streetAddress":"<...>","addressLocality":"<...>","addressCountry":"VN"},
 "telephone":"+84<SỐ THẬT>","url":"https://<tên-miền>/"}
</script>
```
- `sitemap.xml` liệt kê các trang quan trọng, `robots.txt` trỏ tới sitemap; sau khi lên mạng gửi sitemap vào Search Console. Sitemap không bắt buộc nhưng giúp Google tìm trang.
- Ảnh có `alt`; nội dung quan trọng nằm trong HTML, không chỉ trong ảnh.

### 3.8 Bảo mật cơ bản
- **Tệp `_headers`** trong thư mục tài sản (không có đuôi). Giới hạn theo tài liệu: tối đa 100 luật, mỗi dòng tối đa 2.000 ký tự; header trùng tên sẽ nối bằng dấu phẩy (nguy hiểm với `Cache-Control`). QUAN TRỌNG: `_headers` KHÔNG áp dụng cho phản hồi do mã Worker tạo ra, nên với phần `/api/*` hoặc SSR phải tự gắn header trong `Response`.
```
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy-Report-Only: default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'; object-src 'none'
```
- CSP: nên chạy `Content-Security-Policy-Report-Only` trước để thấy cái gì bị chặn mà web vẫn chạy (theo MDN), sửa xong mới đổi thành `Content-Security-Policy`. Script nội tuyến (`<script>...</script>`, `onclick=`) bị chặn khi đã có `script-src`; tránh `'unsafe-inline'`; với web tĩnh dùng tệp `.js` riêng hoặc hash. Pixel Facebook/TikTok, Zalo, bản đồ cần được liệt kê rõ trong CSP.
- **Không để khóa trong mã.** Mã chạy trong trình duyệt ai cũng đọc được. Khóa và token chỉ ở Worker: `wrangler secret put TEN`; chạy thử cục bộ dùng tệp `.dev.vars` hoặc `.env` đã nằm trong `.gitignore` (kiến thức chung của Wrangler). Không dán khóa vào chat hay tệp ghi chú.
- Form: kiểm tra phía máy chủ (không chỉ ở trình duyệt), có ô bẫy (honeypot) và giới hạn tần suất, ô đồng ý và trang chính sách quyền riêng tư vì thu số điện thoại là dữ liệu cá nhân; không đưa dữ liệu khách vào nhật ký công khai.
- HTTPS sẵn có khi dùng Cloudflare; không nhúng tài nguyên `http://`.

### 3.9 Kiểm thử
1. `npx lighthouse <url> --form-factor=mobile --output=html` và bản `--preset=desktop`; mục tiêu khởi điểm: truy cập, SEO, thực hành tốt cao, hiệu năng đạt ngưỡng Web Vitals ở mục 3.6 (mức điểm cụ thể do chủ và cộng sự thống nhất cho từng web, cần xác minh con số).
2. axe-core (hoặc kiểm tay: bàn phím Tab qua toàn trang, phóng chữ 200%, đọc thử bằng VoiceOver).
3. Xem ở 390, 768, 1280 px và nhìn bằng mắt (script không thay được): có thanh cuộn ngang không, chữ tràn, nút bị cắt, bảng giá có đọc được không.
4. Form: gửi một khách thử thật, thấy khách vào đúng nơi (CRM/Zalo), rồi xóa khách thử; thử để trống, thử số sai; kiểm thông báo lỗi nói rõ sai gì.
5. Liên kết: không hỏng, nút gọi/Zalo mở đúng số, ảnh chia sẻ hiện đúng khi dán link vào Zalo/Facebook.
6. Điện thoại THẬT ít nhất một iPhone hoặc Android với mạng 4G: mở bằng địa chỉ thật, không phải `localhost`.
7. Chạy kỹ năng nội bộ `soat-trang.mjs` (và `--dang` trước khi đăng thật) cho Lead/Sale Page, rồi `scripts/kiem-web.py` trên địa chỉ thật.

### 3.10 Git và cách quay lại bản cũ
- `git init`, commit nhỏ, thông điệp rõ ("đổi màu nút", không phải "sửa"); trước mỗi lần đưa lên: `git tag -a v2026-11-19 -m "bản đưa lên lần 1"`. Nhánh riêng cho thay đổi lớn.
- Hoàn tác bản đã commit: `git revert <mã>` tạo một commit mới đảo ngược thay đổi, giữ nguyên lịch sử (theo tài liệu git); tránh `git reset --hard` vì mất thay đổi chưa commit.
- Quay lại bản ĐANG CHẠY nhanh nhất: Cloudflare Dashboard, Workers & Pages, chọn Worker, mục Deployments, ba chấm cạnh phiên bản, Rollback; hoặc `npx wrangler rollback` (chọn trong tối đa 100 phiên bản gần nhất). Lưu ý theo tài liệu: rollback KHÔNG hoàn tác dữ liệu ở D1/KV/R2 (cấu trúc dữ liệu đổi giữa hai bản thì mã cũ có thể lỗi), bị chặn nếu tài nguyên đã bị xóa, và cần thời gian lan ra các điểm. D1 có Time Travel để khôi phục dữ liệu.
- Trước khi sửa DNS luôn xuất và lưu bản ghi cũ (luật của cộng sự); trước khi di chuyển web ghi lại bản đang chạy để quay lại được.

### 3.11 Tránh "AI-slop": giao diện nhìn là biết do AI làm
Các nguồn đã đọc (kỹ năng frontend-design hiện tại của Anthropic trên GitHub, bài "Improving frontend design through Skills", Impeccable) chỉ ra cùng một nguyên nhân: mô hình hay chọn lối an toàn giống nhau, nên các web ra giống nhau. Danh sách dấu hiệu thay đổi theo phiên bản của kỹ năng; đây là phần chung:
| Dấu hiệu | Vì sao lộ | Làm có gu hơn |
|---|---|---|
| Gradient tím sang xanh trên nền trắng, hoặc nền đen với một màu nhấn neon | Mặc định quen mắt | Chọn màu từ nhận diện thật của chủ, một màu chủ đạo chiếm ưu thế + một màu nhấn sắc nét |
| Một phông cho mọi thứ (Inter, Roboto, Arial, phông hệ thống) | Không có cá tính | Chọn có chủ ý 1 họ phông (hoặc 2 họ khác hẳn nhau), tương phản độ đậm và cỡ. Phông phải có đủ dấu tiếng Việt: thử "Ặ Ở Ữ ệ ợ ỳ" trước. Chủ đã có phông thương hiệu thì dùng phông đó |
| Lưới thẻ giống hệt nhau, một bo góc cho mọi thứ, bóng mờ đều, thẻ lồng trong thẻ | Rập khuôn SaaS | Cho khối quan trọng nhất to hơn, đổi nhịp; chỉ làm thẻ khi nội dung thật là một nhóm đồng loại |
| Ô icon bo vuông phía trên mỗi tiêu đề; emoji làm icon | Trang trí rỗng; emoji thay đổi theo máy | Dùng bộ SVG nhất quán (kỹ năng nội bộ dặn không dùng emoji làm biểu tượng trên trang bán hàng), chỉ thêm icon khi giúp quét nhanh |
| Mỗi khối đều hiệu ứng trượt lên và mờ dần; nhãn chữ in hoa dãn chữ phía trên tiêu đề; "A · B · C"; mũi tên "→" cuối mọi nút; số to kèm nhãn nhỏ | Công thức lặp | Một khoảnh khắc chuyển động có chủ ý (vd lúc vào trang), còn lại tĩnh; bỏ nhãn thừa; chữ rõ ràng |
| Chữ xám trên nền màu, tương phản yếu | Khó đọc, trượt WCAG | Kiểm tương phản bằng công cụ |
| Ảnh stock người mẫu nước ngoài, lời chứng thực, đếm ngược, "đã có N khách" bịa | Mất tin ngay, có thể vi phạm quy định | Ảnh thật của chủ (công trình, sản phẩm, đội ngũ); chưa có thì để ô trống rõ ràng; không bịa số |
Cách làm (rút từ kỹ năng của Anthropic, viết lại): (1) xác định chủ đề từ ngành và khách thật của chủ; (2) lập kế hoạch 2 lượt: lượt 1 là token (4 đến 6 màu có tên, phông và vai trò, ý tưởng bố cục bằng wireframe chữ), lượt 2 là soát xem có chỗ nào giống mặc định thì sửa; (3) khối đầu trang mở bằng thứ đặc trưng nhất của nghề (BĐS: ảnh công trình thật); (4) chọn MỘT thứ để người xem nhớ, phần còn lại im lặng và kỷ luật; (5) dựng xong thì chụp, soát, rồi bỏ đi một thành phần thừa; (6) chạy `npx impeccable detect` (62 quy tắc, không cần khóa) như một lượt soát nhanh. Cẩn thận: "tránh" không phải "cấm". Nếu chủ đã có bộ nhận diện hoặc yêu cầu cụ thể thì làm đúng yêu cầu; bản thân kỹ năng cũng nói khi đề bài chỉ rõ hướng thì làm theo hướng đó.

## 4. Bước ra quyết định trước khi nhận một yêu cầu làm web

### 4.1 Câu cần hỏi chủ (một lượt ngắn, tối đa 5 câu; phần còn lại tự quyết và ghi giả định)
Trước hết đọc bộ não để khỏi hỏi lại điều đã có (sản phẩm, khách hàng, thương hiệu, giá, Zalo). Rồi hỏi phần còn thiếu:
1. **Việc chính** của trang: khách làm gì sau khi xem (để lại số, nhắn Zalo, mua ngay, đặt lịch, chỉ đọc)? Đo thành công bằng gì?
2. **Khách và kênh:** khách là ai, đến từ Facebook, TikTok, Zalo hay Google; xem bằng điện thoại hay máy tính?
3. **Thứ thật đang có:** logo, màu, ảnh thật, giá, cam kết, giấy phép, đánh giá thật, số Zalo/điện thoại, chính sách. Cái nào chưa có thì cộng sự nói rõ sẽ để trống, không bịa.
4. **Tên miền và web hiện tại:** đã có tên miền chưa, ai đang quản DNS; có web đang chạy không (không đụng, không đổi DNS khi chưa được đồng ý rõ).
5. **Mẫu và hạn chế:** thích web nào làm mẫu (cho xem URL), không muốn giống ai, hạn chót, có tốn tiền gì (tên miền, ảnh, gói Cloudflare) thì chủ phải duyệt.
Nếu cần hỏi thêm lượt hai: số trang, cần thanh toán hay đăng nhập không, khách để lại thông tin sẽ lưu ở đâu (CRM trên máy hay đám mây), ai sẽ sửa nội dung về sau, có cần tiếng Anh không.

### 4.2 Gói web mẫu TISA BOT hay dựng mới
Gói **Web CRM + Lead Page** (gói `tisa.web-crm-lead` của Học Viện TISA; đọc trong `overlay/server/tisa_web_mau.py`): một bộ gồm thư mục `crm/` (Node.js) và `lead/` (trang tĩnh); cài một lần qua trình cài gói của TISA BOT; chạy ngay trên máy chủ (nghe 127.0.0.1, cần Node từ 22.13 trở lên theo mã); nhân bản được thêm 3, 4, 5 trang Lead/Sale (chép `lead/` thành `lead-2`, `lead-3`...), cùng đổ khách vào CRM của bộ; chatbot ghi khách vào CRM hoặc lấy số trong CRM để kết bạn Zalo và nhắn chăm sóc; trang Lead được TISA BOT phát ở `/tisa-web/trang/<slug>/`, form gửi về `/tisa-web/crm-form/<bộ>` chỉ nhận ghi, có giới hạn tần suất, CRM không lộ ra ngoài.
| Tình huống | Chọn |
|---|---|
| Cần bắt khách để lại số, 1 đến 5 trang bán hàng/lead cùng một khuôn, muốn nối ngay CRM và Zalo, chủ ít kỹ thuật | **Gói mẫu**, rồi đổi giao diện bằng kỹ năng `tisa-thiet-ke-web` (8 chủ đề). Luật cứng: không đổi thuộc tính form, `lead-config.js`, cách nối CRM |
| Muốn trang đẹp hơn nhưng vẫn là lead/sale | Gói mẫu làm nền, giữ phần logic, thay giao diện theo thương hiệu |
| Web giới thiệu nhiều trang, có blog/tin tức, hoặc cần SEO mạnh | Dựng mới: Astro (mức 2) |
| Cửa hàng/giỏ hàng, đặt lịch, đăng nhập, thành viên | Dựng mới: mức 4 (Worker + D1) hoặc dùng dịch vụ có sẵn, báo chủ phần tiền và rủi ro |
| Giao diện khác hẳn khuôn lead (công cụ, bảng điều khiển) | Dựng mới: Vite + React hoặc HTML thuần |
| Cần CRM chung nhiều người dùng ở đám mây | Dựng mới trên Worker + D1 (gói mẫu chạy CRM trên máy chủ) |
| Chủ chỉ cần sửa chữ/ảnh một web đã có | Sửa trên mã sẵn có, không dựng lại; hỏi trước xem bản mới nhất nằm ở thư mục nào để khỏi sửa nhầm bản cũ |
Điểm cần xác minh: khi đưa trang Lead của gói mẫu lên Cloudflare (không còn ở localhost), địa chỉ nhận form (`crmEndpoint`) phải trỏ tới nơi nhận được từ internet; bộ `soat-trang.mjs --dang` coi `crmEndpoint` còn localhost là LỖI. Cách nối đúng giữa web công khai và CRM trên máy cần hỏi đội gói trước khi hứa với chủ.

### 4.3 Việc phải xong trước khi nói "xong"
Chủ đã duyệt bản xem thử; không còn chữ mẫu và số giả; form thử đã chạy và khách thử đã xóa; Lighthouse và truy cập đạt mức đã thống nhất; có tệp `README.md` (cách sửa, cách đưa lên, nơi mã nguồn, nơi giữ khóa không ghi khóa); có thẻ Git và biết cách rollback; hồ sơ web đã ghi vào bộ não. Những việc chỉ người thật làm được (đăng nhập, mật khẩu, mã OTP, thanh toán, mua tên miền, đổi nameserver, đồng ý cấp quyền) thì dừng và nói đúng một việc chủ cần làm.
