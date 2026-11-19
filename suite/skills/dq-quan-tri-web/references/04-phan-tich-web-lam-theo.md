# 04 - Phân tích web mẫu để làm theo, và ranh giới đạo đức, pháp lý

Ngày: 19/11/2026. Nguồn đã đọc: https://github.com/VoltAgent/awesome-design-md ; https://github.com/VoltAgent/awesome-claude-design ; https://github.com/google-labs-code/design.md ; https://github.com/dembrandt/dembrandt ; https://github.com/dembrandt/dembrandt-skills ; https://github.com/arvindrk/extract-design-system ; https://github.com/JCodesMore/ai-website-cloner-template ; https://docs.firecrawl.dev/developer-guides/cookbooks/brand-style-guide-generator-cookbook ; https://github.com/firecrawl/firecrawl ; https://github.com/ChromeDevTools/chrome-devtools-mcp ; https://github.com/microsoft/playwright-mcp ; https://playwright.dev/docs/screenshots ; https://github.com/GoogleChrome/lighthouse ; https://developers.google.com/speed/docs/insights/v5/get-started ; https://github.com/simonw/shot-scraper ; https://github.com/projectwallace/css-analyzer ; https://github.com/abi/screenshot-to-code ; https://developers.figma.com/docs/figma-mcp-server/ ; https://github.com/dequelabs/axe-core ; https://github.com/pbakaus/impeccable ; https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md ; Luật Sở hữu trí tuệ số 50/2005/QH11 (bản PDF https://mirrors.creativecommons.org/international/vn/IP-Law-2005-(Vietnamese).pdf) ; kết quả tìm kiếm về bản quyền website (nguồn là blog công ty luật, chỉ để tham khảo). Tệp nội bộ đối chiếu: `assets/goi/them/tisa-thiet-ke-web/SKILL.md`, `overlay/suite/agents/tisa-quan-tri-web.md`.

Quy ước: số sao và giấy phép lấy từ trang GitHub vào ngày 19/11/2026, sao thay đổi hằng ngày nên chỉ là cỡ tham khảo. Chỗ nào ghi "cần xác minh" là chưa đọc được nguồn gốc.

## 1. Quy trình 10 bước: từ một web mẫu đến bản làm theo của chủ

| # | Bước | Làm gì | Công cụ | Ra gì |
|---|---|---|---|---|
| 0 | Cho phép | Hỏi chủ thích điểm nào của web mẫu. Xem robots.txt và điều khoản của web đó. Chạy nhẹ, không dồn dập | Trình duyệt | Ghi chú mục đích, URL, ngày |
| 1 | Chụp toàn trang | Chụp ở 375, 768, 1280, 1920 px. Cuộn hết trang trước để ảnh lazy-load kịp tải, tắt animation khi chụp, tắt banner cookie nếu che | Playwright `fullPage: true` (đã đọc trong tài liệu Playwright) | `full-375.png`... |
| 2 | Dựng sơ đồ khối | Liệt kê từng khối từ trên xuống: header, hero, bằng chứng, lợi ích, giá, hỏi đáp, form, footer. Ghi chiều cao, khối nào dính (sticky/fixed), thứ tự h1-h3, nút kêu gọi hành động | Đoạn `page.evaluate` bên dưới, hoặc cây truy cập của Playwright MCP | Danh sách khối |
| 3 | Rút design tokens | Màu chữ, màu nền, phông, cỡ chữ, khoảng cách, bo góc, đổ bóng, đọc bằng `getComputedStyle`; có biến CSS `:root` thì lấy luôn | Script bên dưới, hoặc dembrandt, extract-design-system, Firecrawl `branding` | `tokens.json` |
| 4 | Quy về thang | Gom cỡ chữ về thang (vd 14/16/20/28/40), khoảng cách về bội của 4 hoặc 8, màu về 1 màu chính + 1 nhấn + nền + chữ + 3 màu trạng thái | Tự làm, kiểm tương phản bằng `--wcag` của dembrandt hoặc `lint` của design.md | Bảng tokens sạch |
| 5 | Xem hành vi | Hover/focus (so sánh style trước và sau `page.hover`), menu điện thoại (bấm nút hamburger), carousel, hiệu ứng hiện khi cuộn, form (ô nào, kiểm lỗi ra sao), popup. Quay video ngắn nếu cần | Playwright (`hover`, `click`, `recordVideo`: kiến thức chung, tự thử), Chrome DevTools MCP | Danh sách hành vi |
| 6 | Đo tốc độ | Lighthouse điện thoại và máy tính; ghi LCP, INP, CLS, dung lượng, số request. Dùng làm "ngân sách" cho bản của mình, không cần thua | Lighthouse CLI, PageSpeed Insights API, Chrome DevTools MCP | Bảng số đo |
| 7 | Viết đặc tả | Gói bước 2 đến 6 thành một tệp `DESIGN.md` + sơ đồ khối (mẫu ở mục 1.3) | Mẫu 9 phần của awesome-design-md, hoặc định dạng design.md | `DESIGN.md` |
| 8 | Đổi theo thương hiệu chủ | Lập bảng ánh xạ: màu, phông, ảnh, icon, giọng chữ, nội dung. Mọi thứ nhận diện đều lấy của chủ. Chữ viết lại từ hồ sơ sản phẩm thật | Bộ não (hồ sơ thương hiệu) | Bảng ánh xạ |
| 9 | Dựng và đối chiếu | Dựng bản của chủ, chụp đặt cạnh web mẫu: nếu nhìn thoáng qua có thể nhầm là cùng một web thì phải đổi thêm (xem luật mục 2). Rồi chạy Lighthouse, axe, kiểm điện thoại | Lighthouse, axe-core, `soat-trang.mjs` (kỹ năng `tisa-thiet-ke-web`) | Bản xem thử |
| 10 | Lưu hồ sơ | Ghi URL mẫu, ngày, điều học được, điều đã đổi, điều cố ý không lấy | `ghi-chep-web.py` (nội bộ TISA BOT) | Hồ sơ trong bộ não |

Hạn chế cần nói với chủ: trang vẽ bằng canvas/WebGL không phân tích được bằng DOM (theo README dembrandt); trang nặng JavaScript cần chờ tải xong; chế độ tối phải bật riêng; style kéo từ domain khác có thể không đọc được qua `styleSheets` (nhưng `getComputedStyle` vẫn đọc được giá trị cuối cùng).

### 1.1 Script rút tokens và chụp 4 độ rộng (đã tự chạy thử trên trang cục bộ)
Cần Node 18 trở lên: `npm i playwright && npx playwright install chromium`. Chạy: `node rut-tokens.mjs https://trang-mau.vn ra`. Cũng có thể dán phần trong `page.evaluate` vào Console của trình duyệt nếu máy chưa có Playwright.
```js
// rut-tokens.mjs  (chỉ dùng cho trang được phép, hoặc trang của chính chủ)
import { chromium } from 'playwright';
import fs from 'node:fs';
const [url, out = 'ra'] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
for (const w of [375, 768, 1280, 1920]) {
  const page = await browser.newPage({ viewport: { width: w, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: '*{animation:none!important;transition:none!important}' });
  await page.evaluate(async () => {            // cuộn để kích hoạt lazy-load
    for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
    scrollTo(0, 0);
  });
  await page.screenshot({ path: `${out}/full-${w}.png`, fullPage: true });
  if (w === 1280) {
    const t = await page.evaluate(() => {
      const m = { color: {}, bg: {}, font: {}, size: {}, radius: {}, shadow: {}, gap: {} };
      const add = (k, v) => v && (m[k][v] = (m[k][v] || 0) + 1);
      for (const el of document.querySelectorAll('body *')) {
        const s = getComputedStyle(el);
        if (s.display === 'none') continue;
        if ([...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) {
          add('color', s.color); add('font', s.fontFamily.split(',')[0]); add('size', s.fontSize);
        }
        if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') add('bg', s.backgroundColor);
        if (s.borderRadius !== '0px') add('radius', s.borderRadius);
        if (s.boxShadow !== 'none') add('shadow', s.boxShadow);
        for (const p of ['paddingTop', 'paddingLeft', 'rowGap']) if (!/^(0px|normal)$/.test(s[p])) add('gap', s[p]);
      }
      const top = o => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, 8);
      const res = Object.fromEntries(Object.entries(m).map(([k, v]) => [k, top(v)]));
      res.sections = [...document.querySelectorAll('header,nav,section,footer')].map(e => ({
        tag: e.tagName, h: Math.round(e.getBoundingClientRect().height),
        heading: (e.querySelector('h1,h2,h3')?.textContent || '').trim().slice(0, 50),
        sticky: /sticky|fixed/.test(getComputedStyle(e).position) }));
      return res;
    });
    fs.writeFileSync(`${out}/tokens.json`, JSON.stringify(t, null, 2));
  }
  await page.close();
}
await browser.close();
```
Kết quả đếm "giá trị nào xuất hiện nhiều nhất"; người làm vẫn phải nhìn ảnh để biết đâu là màu chính, đâu là màu nhấn.

### 1.2 Đo tốc độ
```bash
npx lighthouse https://trang-mau.vn --preset=desktop --output=html --output=json --output-path=./lh-desktop
npx lighthouse https://trang-mau.vn --form-factor=mobile --only-categories=performance,accessibility,seo,best-practices --output=html --output-path=./lh-mobile
```
Cờ `--preset`, `--form-factor`, `--only-categories`, `--output`, `--output-path` có trong README Lighthouse; README nói cần Node 22 trở lên. PageSpeed Insights API v5 (`https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=...`) trả `lighthouseResult` (số đo giả lập) và `loadingExperience` (số đo người dùng thật); Google nói sẽ bỏ dữ liệu CrUX khỏi API này, nên dữ liệu thật dùng CrUX API riêng. Có cần khóa hay không khi dùng nhẹ: cần xác minh.

### 1.3 Mẫu đặc tả `DESIGN.md` (9 phần theo awesome-design-md, viết lại ngắn)
1 Không khí tổng thể; 2 Màu và vai trò (chính, nhấn, nền, chữ, trạng thái, kèm tỉ lệ tương phản); 3 Chữ (phông, thang cỡ, độ đậm, dòng cao); 4 Thành phần (nút, thẻ, form, menu: kích thước, bo góc, bóng, trạng thái hover/focus/disabled); 5 Bố cục (lưới, độ rộng tối đa, nhịp khoảng cách); 6 Độ nổi (bóng, lớp); 7 Nên và không nên; 8 Hành vi theo cỡ màn hình (điểm gãy, menu điện thoại); 9 Gợi ý cho cộng sự dựng. Thêm phần của TISA: **bảng ánh xạ mẫu sang thương hiệu chủ** và **điều cố ý không lấy**.

### 1.4 Danh sách công cụ và repo đáng dùng (17 mục)
| # | Tên | URL | Sao (19/11/2026) | Giấy phép | Dùng cho gì |
|---|---|---|---|---|---|
| 1 | dembrandt | https://github.com/dembrandt/dembrandt | khoảng 4,0k | MIT | CLI Playwright, rút logo, màu, chữ, khoảng cách, bóng, chuyển động, breakpoint. Xuất JSON, DTCG (`--dtcg`), `--design-md`, Tailwind v4 (`--tailwind`), shadcn (`--shadcn`), `--wcag`, `--mobile`, `--dark-mode`, `--crawl`. Có MCP. README nhắc: chỉ chạy trên web cho phép hoặc của mình, không dùng để tái tạo nhận diện của người khác. Công cụ chính nên dùng cho bước 3 |
| 2 | dembrandt-skills | https://github.com/dembrandt/dembrandt-skills | khoảng 196 | MIT | 45 kỹ năng UX/design system cho agent (bố cục, a11y WCAG 2.2, hiệu năng). Hai kỹ năng đọc web sống cần engine dembrandt. Cài: `npx skills add dembrandt/dembrandt-skills --all` |
| 3 | extract-design-system | https://github.com/arvindrk/extract-design-system | khoảng 291 | MIT | Kỹ năng + CLI + MCP, Playwright rút tokens của 1 trang, xuất `tokens.json` (W3C) và `tokens.css`. Tác giả nói chỉ để khởi tạo, không phải bản sao điểm ảnh. `npx skills add arvindrk/extract-design-system` |
| 4 | Firecrawl, định dạng `branding` | https://docs.firecrawl.dev/developer-guides/cookbooks/brand-style-guide-generator-cookbook ; https://github.com/firecrawl/firecrawl | repo khoảng 203k | Lõi AGPL-3.0, SDK MIT | `scrape(url, {formats:["branding"]})` trả màu (chính, phụ, nhấn, nền, chữ), phông, cỡ chữ, khoảng cách cơ sở, bo góc, logo. Cần khóa API (đặt bằng biến môi trường, không ghi vào mã). Trường nào cũng có thể thiếu. Dùng được trên bản tự host hay không: cần xác minh |
| 5 | awesome-design-md (VoltAgent) | https://github.com/VoltAgent/awesome-design-md | khoảng 128k | MIT | 84 tệp DESIGN.md của các thương hiệu lớn, 9 phần, kèm `preview.html`. Dùng để HỌC cách viết đặc tả và xem cách chia tầng. Repo nói tệp là giá trị CSS công khai "như hiện có", không nhận quyền sở hữu nhận diện của site nào |
| 6 | awesome-claude-design (VoltAgent) | https://github.com/VoltAgent/awesome-claude-design | khoảng 4,6k | MIT | 68 DESIGN.md cho Claude Design. Repo nói rõ đây là cảm hứng, không phải hệ thống chính thức, không liên kết với các hãng, nên dùng để làm hệ thống ORIGINAL chứ không nhái gần nguyên |
| 7 | design.md (Google Labs) | https://github.com/google-labs-code/design.md | khoảng 29k | Apache-2.0 | Quy chuẩn định dạng: token YAML + chữ giải thích. Có `lint` (kiểm tham chiếu, tương phản WCAG) và `export` (Tailwind, DTCG). Ghi chú alpha, định dạng có thể đổi |
| 8 | Chrome DevTools MCP | https://github.com/ChromeDevTools/chrome-devtools-mcp | khoảng 58k | Apache-2.0 | Cho agent điều khiển Chrome thật: trace hiệu năng, mạng, ảnh chụp, console. Cài: plugin (`/plugin marketplace add ChromeDevTools/chrome-devtools-mcp`) hoặc khai báo MCP chạy `npx -y chrome-devtools-mcp@latest`. Có công cụ chạy Lighthouse hay không: cần xác minh (README không nêu) |
| 9 | Playwright MCP | https://github.com/microsoft/playwright-mcp | khoảng 39,9k | Apache-2.0 | Điều khiển trình duyệt qua cây truy cập (không dựa ảnh), tốt để lấy cấu trúc. `claude mcp add playwright npx @playwright/mcp@latest`, cần Node 20+ |
| 10 | Lighthouse | https://github.com/GoogleChrome/lighthouse | khoảng 31,2k | Apache-2.0 | Chấm hiệu năng, truy cập, SEO, thực hành tốt. Xuất html/json/csv. Cần Node 22+ |
| 11 | shot-scraper | https://github.com/simonw/shot-scraper | khoảng 2,6k | Apache-2.0 | Chụp ảnh trang và chạy JavaScript lấy dữ liệu bằng một lệnh (`pip install shot-scraper && shot-scraper install`). Các cờ độ rộng/chọn phần tử chưa đọc, xem tài liệu của nó, cần xác minh |
| 12 | css-analyzer (Project Wallace) | https://github.com/projectwallace/css-analyzer | khoảng 367 | MIT | Đưa CSS vào, ra thống kê: màu, cỡ chữ, bo góc, bóng, độ đặc hiệu, độ phức tạp. Hợp để kiểm tính nhất quán token trong CSS của chính mình |
| 13 | ai-website-cloner-template | https://github.com/JCodesMore/ai-website-cloner-template | khoảng 39,5k | MIT | Lệnh `/clone-website <url>`: lập bản đồ, quan sát, dựng Next.js 16 + Tailwind v4, so sánh. CHỈ NÊN dùng để HỌC quy trình (map, observe, build, compare). README của nó nhắc logo, tài sản thương hiệu và chữ gốc thuộc chủ của chúng, đừng trình bày thiết kế người khác như của mình, có site cấm cào trong điều khoản. Không dùng để xuất bản bản sao |
| 14 | screenshot-to-code | https://github.com/abi/screenshot-to-code | khoảng 81,3k | MIT | Ảnh chụp, mockup, Figma sang HTML/Tailwind/React/Vue. Cần khóa của OpenAI, Anthropic hoặc Gemini. Hợp để dựng nháp từ SKETCH của chủ hoặc mockup của mình; với web người khác thì chỉ lấy bố cục |
| 15 | Figma MCP server | https://developers.figma.com/docs/figma-mcp-server/ | (không phải repo) | dịch vụ của Figma | Lấy biến, thành phần, bố cục từ file Figma CỦA CHỦ hay của nhà thiết kế thuê. Server máy tính cần ghế Dev/Full; ghi vào canvas cần server từ xa. Có gói trả phí |
| 16 | Impeccable (+ `impeccable detect`) | https://github.com/pbakaus/impeccable | khoảng 113k | Apache-2.0 | 24 lệnh thiết kế, và bộ dò 62 quy tắc "AI slop" chạy được bằng `npx impeccable detect`, không cần khóa. Dùng để soát bản của mình ở bước 9 (xem tệp 05) |
| 17 | axe-core | https://github.com/dequelabs/axe-core | khoảng 7,9k | MPL-2.0 | Soát truy cập tự động; README nói bắt được trung bình khoảng 57% lỗi WCAG, phần còn lại phải xem tay |

Ghi chú chọn: bước 3 ưu tiên dembrandt (đã có MCP, xuất được DESIGN.md và Tailwind), dự phòng bằng script ở 1.1 khi máy học viên không cài được. Kỹ năng frontend-design chính thức của Anthropic nằm ở https://github.com/anthropics/skills (đã đọc nội dung, chưa đọc số sao, giấy phép: cần xác minh), xem tệp 05.

## 2. Đạo đức và pháp lý ở mức thực dụng

Đây không phải tư vấn pháp lý. Các nguồn pháp lý về website đã tìm chủ yếu là blog công ty luật, nhiều nguồn Mỹ và Anh, nên chỉ dùng để định hướng.

**Điều nhìn chung đúng ở các nguồn:** (a) ý tưởng, cách làm, thể loại bố cục chung không được bảo hộ, còn cách thể hiện cụ thể (chữ, ảnh, video, mã nguồn, bố cục độc đáo) thì có; (b) sao chép chữ, ảnh, mã nguồn là vi phạm rõ nhất; (c) "look and feel" tổng thể là vùng tranh cãi, tùy vụ việc; (d) nhãn hiệu, logo, tên thương hiệu là một lớp riêng, không liên quan đến việc bố cục có được phép hay không.

**Luật Việt Nam (Luật SHTT 50/2005/QH11, đã sửa đổi 2009, 2019, 2022; bản đọc là bản gốc 2005, cần xác minh bản hợp nhất hiện hành):** Điều 14 liệt kê tác phẩm được bảo hộ, trong đó có tác phẩm tạo hình và mỹ thuật ứng dụng, chương trình máy tính, văn học (chữ), nhiếp ảnh; Điều 14.3 yêu cầu tác phẩm do tác giả tự sáng tạo, không sao chép. Điều 15.3 nói các đối tượng như quy trình, hệ thống, phương pháp hoạt động, khái niệm, nguyên lý, số liệu không thuộc phạm vi bảo hộ quyền tác giả. Suy ra thực dụng: học nguyên tắc và công thức thì ổn; chép nguyên trang, nguyên mã, nguyên ảnh thì không. Một nguồn luật sư nêu rằng chỉ sao chép màu và bố cục chung thì khả năng vi phạm thấp, nhưng chép gần như nguyên header, thanh điều hướng vẫn đáng lo (cần xác minh, nguồn là blog tư vấn).

**Quy tắc cộng sự phải theo (ngắn):**
1. Được học: thứ tự các khối, tỉ lệ khoảng trắng, nhịp chữ, kiểu thẻ, cách đặt nút gọi hành động, cách chia lưới, hành vi tương tác (menu, sticky), ý tưởng bố cục.
2. Không chép: chữ và giọng viết (viết lại 100% từ hồ sơ sản phẩm thật của chủ), ảnh, video, icon độc quyền, logo, tên thương hiệu, lời chứng thực, số liệu, bảng giá của người khác. Không tải ảnh của họ về dùng, không hotlink.
3. Không chép mã nguồn: không lấy nguyên tệp CSS/JS/HTML của họ. Tokens (số liệu như màu, cỡ chữ) có thể tham khảo, nhưng cấu trúc mã tự viết lại, đặt tên lớp theo hệ của mình.
4. Đổi tối thiểu năm thứ cùng lúc: bảng màu, phông, ảnh, icon, chữ. Phần bố cục thì đổi ít nhất thứ tự hoặc số khối nếu bản mẫu rất đặc trưng. Không dùng cùng lúc "đúng bảng màu + đúng phông + đúng bố cục + đúng cách đặt tên".
5. Kiểm tra cạnh nhau (bước 9): nếu người ngoài nhìn thoáng qua có thể tưởng cùng một web, phải đổi thêm.
6. Không giả mạo: không dùng tên miền, tên hay logo gần giống, không để khách tưởng đó là web của hãng khác, không làm trang giống để lừa. Chủ nói "làm giống hệt web X" thì từ chối phần giống hệt, đề xuất làm theo phong cách và đổi nhận diện.
7. Đặc biệt thận trọng với đối thủ trực tiếp cùng khu vực, cùng ngành: học cấu trúc chung của ngành nhưng làm khác một điểm dễ nhớ.
8. Phông: Google Fonts đa số là OFL 1.1 (một số họ dùng Apache hoặc Ubuntu Font License) nên dùng thương mại và tự host được, giữ tệp giấy phép đi kèm; mỗi họ phông xem tệp giấy phép riêng (theo trang tài liệu của Google và kho google/fonts; trang FAQ chưa đọc được trực tiếp, cần xác minh). Phông trả phí của web mẫu thì không dùng, chọn phông thay thế hợp lệ có đủ dấu tiếng Việt.
9. Ảnh: dùng ảnh thật của chủ hoặc ảnh có giấy phép rõ; ảnh tạo bằng AI không chứa chữ, không chứa mặt người thật. Ghi nguồn ảnh vào hồ sơ web.
10. Đọc điều khoản và robots.txt của web mẫu; không cào hàng loạt; không dùng cờ lách phát hiện bot (stealth của dembrandt chỉ dành cho ủy quyền). Chỉ lấy thứ công khai, không đăng nhập hộ, không vượt tường trả phí.
11. Khi dùng DESIGN.md của thương hiệu lớn từ các bộ sưu tập (mục 5, 6): chỉ làm tài liệu học và điểm khởi đầu, rồi thay token bằng của chủ; ghi trong hồ sơ rằng bản cuối là thiết kế của chủ.
12. Ghi hồ sơ: lưu URL mẫu, ngày, điều học và điều đã đổi. Khi chủ hỏi "có sao chép không", cộng sự trả lời được.
