# Thư viện component & mẫu chữ — /ts-landing-page

> Chuyển từ SKILL.md gốc (phần code mẫu dài). AI đọc file này khi bắt đầu dựng HTML (Bước 5 trong SKILL.md).
> Quy tắc khi dùng:
> - Dịch **toàn bộ chữ hiển thị** sang tiếng Việt, đúng giọng trong `04-thuong-hieu-noi-dung.md` (nếu có).
> - Thay hết `{{...}}`. Thiếu bằng chứng thật → để `[CẦN BỔ SUNG: …]` trong bản nháp, KHÔNG bịa.
> - Không dùng emoji làm icon giao diện (xem `references/anti-ai-slop-checklist.md`) — dùng SVG.
> - Các khối dưới đây là "xương" an toàn; luôn biến tấu bố cục theo `references/design-data.md`
>   (Layout Variation Matrix) để trang không giống khuôn AI.
> - Khối thanh toán VietQR ở cuối file đã cập nhật đường dẫn ảnh QR mới nhất — chi tiết xem `/ts-gan-ma-qr`.

## Page Structure Template

Use this base HTML structure for all landing pages:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{PAGE_TITLE}}</title>
  <meta name="description" content="{{META_DESCRIPTION}}">

  <!-- Open Graph -->
  <meta property="og:title" content="{{OG_TITLE}}">
  <meta property="og:description" content="{{OG_DESCRIPTION}}">
  <meta property="og:image" content="{{OG_IMAGE}}">
  <meta property="og:type" content="website">

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  {{FONT_IMPORT}}

  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '{{PRIMARY}}',
            secondary: '{{SECONDARY}}',
            accent: '{{ACCENT}}'
          },
          fontFamily: {
            heading: [{{HEADING_FONT}}, 'sans-serif'],
            body: [{{BODY_FONT}}, 'sans-serif']
          }
        }
      }
    }
  </script>

  <style>
    body { font-family: {{BODY_FONT}}, sans-serif; }
    h1, h2, h3, h4, h5, h6 { font-family: {{HEADING_FONT}}, sans-serif; }
  </style>
</head>
<body class="bg-gray-50 text-gray-900">
  <!-- Page content here -->
</body>
</html>
```

---

## Component Library

### Navbar (Floating with CTA)
```html
<nav class="fixed top-0 w-full bg-white shadow-md z-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <div class="flex-shrink-0">
        <span class="text-2xl font-bold text-primary">{{BRAND_NAME}}</span>
      </div>
      <div class="hidden md:flex space-x-8">
        <a href="#features" class="text-gray-700 hover:text-primary">Features</a>
        <a href="#pricing" class="text-gray-700 hover:text-primary">Pricing</a>
        <a href="#faq" class="text-gray-700 hover:text-primary">FAQ</a>
      </div>
      <a href="#cta" class="bg-accent text-white px-6 py-2 rounded-lg hover:opacity-90 transition">
        {{CTA_TEXT}}
      </a>
    </div>
  </div>
</nav>
```

### Hero Section (Headline + Subheadline + CTA + Social Proof)
```html
<section class="pt-24 pb-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-primary/5 to-white">
  <div class="max-w-4xl mx-auto text-center">
    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
      {{HEADLINE}}
    </h1>
    <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
      {{SUBHEADLINE}}
    </p>
    <div class="flex flex-col sm:flex-row gap-4 justify-center mb-8">
      <a href="#cta" class="bg-accent text-white px-8 py-4 rounded-lg text-lg font-semibold hover:opacity-90 transition">
        {{CTA_PRIMARY}}
      </a>
      <a href="#features" class="bg-white border-2 border-primary text-primary px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary hover:text-white transition">
        {{CTA_SECONDARY}}
      </a>
    </div>
    <div class="flex items-center justify-center gap-6 text-sm text-gray-600">
      <!-- Chỉ hiện khi có số liệu THẬT. Không có → xóa cả khối này. -->
      <span>{{DIEM_DANH_GIA_THAT}}/5 từ {{SO_DANH_GIA_THAT}} đánh giá</span>
      <span>|</span>
      <span>{{SO_KHACH_THAT}}+ khách hàng</span>
    </div>
  </div>
</section>
```

### Features Grid (3-Column)
```html
<section id="features" class="py-16 px-4 sm:px-6 lg:px-8 bg-white">
  <div class="max-w-7xl mx-auto">
    <h2 class="text-3xl sm:text-4xl font-bold text-center mb-12">{{FEATURES_HEADLINE}}</h2>
    <div class="grid md:grid-cols-3 gap-8">
      <!-- Feature 1 -->
      <div class="text-center">
        <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-3xl">{{ICON_1}}</span>
        </div>
        <h3 class="text-xl font-semibold mb-2">{{FEATURE_1_TITLE}}</h3>
        <p class="text-gray-600">{{FEATURE_1_DESC}}</p>
      </div>
      <!-- Feature 2 -->
      <div class="text-center">
        <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-3xl">{{ICON_2}}</span>
        </div>
        <h3 class="text-xl font-semibold mb-2">{{FEATURE_2_TITLE}}</h3>
        <p class="text-gray-600">{{FEATURE_2_DESC}}</p>
      </div>
      <!-- Feature 3 -->
      <div class="text-center">
        <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <span class="text-3xl">{{ICON_3}}</span>
        </div>
        <h3 class="text-xl font-semibold mb-2">{{FEATURE_3_TITLE}}</h3>
        <p class="text-gray-600">{{FEATURE_3_DESC}}</p>
      </div>
    </div>
  </div>
</section>
```

### Testimonials (Grid)
```html
<section id="testimonials" class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
  <div class="max-w-7xl mx-auto">
    <h2 class="text-3xl sm:text-4xl font-bold text-center mb-12">What Our Customers Say</h2>
    <div class="grid md:grid-cols-3 gap-8">
      <!-- Testimonial 1 -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <p class="text-gray-700 mb-4">"{{TESTIMONIAL_1}}"</p>
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-gray-300 rounded-full"></div>
          <div>
            <p class="font-semibold">{{NAME_1}}</p>
            <p class="text-sm text-gray-600">{{ROLE_1}}</p>
          </div>
        </div>
      </div>
      <!-- Testimonial 2 -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <p class="text-gray-700 mb-4">"{{TESTIMONIAL_2}}"</p>
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-gray-300 rounded-full"></div>
          <div>
            <p class="font-semibold">{{NAME_2}}</p>
            <p class="text-sm text-gray-600">{{ROLE_2}}</p>
          </div>
        </div>
      </div>
      <!-- Testimonial 3 -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <p class="text-gray-700 mb-4">"{{TESTIMONIAL_3}}"</p>
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-gray-300 rounded-full"></div>
          <div>
            <p class="font-semibold">{{NAME_3}}</p>
            <p class="text-sm text-gray-600">{{ROLE_3}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

### Pricing Cards (3-Tier)
```html
<section id="pricing" class="py-16 px-4 sm:px-6 lg:px-8 bg-white">
  <div class="max-w-7xl mx-auto">
    <h2 class="text-3xl sm:text-4xl font-bold text-center mb-12">Simple, Transparent Pricing</h2>
    <div class="grid md:grid-cols-3 gap-8">
      <!-- Basic Tier -->
      <div class="border-2 border-gray-200 rounded-lg p-8 hover:border-primary transition">
        <h3 class="text-2xl font-bold mb-2">{{TIER_1_NAME}}</h3>
        <p class="text-4xl font-bold mb-6">{{TIER_1_PRICE}}<span class="text-lg text-gray-600">/month</span></p>
        <ul class="space-y-3 mb-8">
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_1_FEATURE_1}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_1_FEATURE_2}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_1_FEATURE_3}}</li>
        </ul>
        <a href="#cta" class="block w-full text-center bg-gray-200 text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition">
          Get Started
        </a>
      </div>
      <!-- Pro Tier (Popular) -->
      <div class="border-2 border-accent rounded-lg p-8 relative transform scale-105 shadow-xl">
        <span class="absolute -top-4 left-1/2 -translate-x-1/2 bg-accent text-white px-4 py-1 rounded-full text-sm font-semibold">
          Most Popular
        </span>
        <h3 class="text-2xl font-bold mb-2">{{TIER_2_NAME}}</h3>
        <p class="text-4xl font-bold mb-6">{{TIER_2_PRICE}}<span class="text-lg text-gray-600">/month</span></p>
        <ul class="space-y-3 mb-8">
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_2_FEATURE_1}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_2_FEATURE_2}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_2_FEATURE_3}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_2_FEATURE_4}}</li>
        </ul>
        <a href="#cta" class="block w-full text-center bg-accent text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition">
          Get Started
        </a>
      </div>
      <!-- Enterprise Tier -->
      <div class="border-2 border-gray-200 rounded-lg p-8 hover:border-primary transition">
        <h3 class="text-2xl font-bold mb-2">{{TIER_3_NAME}}</h3>
        <p class="text-4xl font-bold mb-6">{{TIER_3_PRICE}}<span class="text-lg text-gray-600">/month</span></p>
        <ul class="space-y-3 mb-8">
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_3_FEATURE_1}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_3_FEATURE_2}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_3_FEATURE_3}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_3_FEATURE_4}}</li>
          <li class="flex items-start"><span class="text-green-500 mr-2">✓</span>{{TIER_3_FEATURE_5}}</li>
        </ul>
        <a href="#cta" class="block w-full text-center bg-gray-200 text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition">
          Contact Sales
        </a>
      </div>
    </div>
  </div>
</section>
```

### FAQ Accordion (Vanilla JS)
```html
<section id="faq" class="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
  <div class="max-w-3xl mx-auto">
    <h2 class="text-3xl sm:text-4xl font-bold text-center mb-12">Frequently Asked Questions</h2>
    <div class="space-y-4">
      <!-- FAQ Item 1 -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <button class="faq-toggle w-full text-left p-6 font-semibold text-lg flex justify-between items-center hover:bg-gray-50 transition">
          {{FAQ_Q1}}
          <span class="faq-icon text-2xl">+</span>
        </button>
        <div class="faq-content hidden px-6 pb-6 text-gray-700">
          {{FAQ_A1}}
        </div>
      </div>
      <!-- FAQ Item 2 -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <button class="faq-toggle w-full text-left p-6 font-semibold text-lg flex justify-between items-center hover:bg-gray-50 transition">
          {{FAQ_Q2}}
          <span class="faq-icon text-2xl">+</span>
        </button>
        <div class="faq-content hidden px-6 pb-6 text-gray-700">
          {{FAQ_A2}}
        </div>
      </div>
      <!-- Add more FAQ items as needed -->
    </div>
  </div>
</section>

<script>
  document.querySelectorAll('.faq-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const content = btn.nextElementSibling;
      const icon = btn.querySelector('.faq-icon');
      content.classList.toggle('hidden');
      icon.textContent = content.classList.contains('hidden') ? '+' : '−';
    });
  });
</script>
```

### Footer
```html
<footer class="bg-gray-900 text-gray-300 py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-7xl mx-auto">
    <div class="grid md:grid-cols-4 gap-8 mb-8">
      <div>
        <h3 class="text-white font-bold text-xl mb-4">{{BRAND_NAME}}</h3>
        <p class="text-sm">{{BRAND_TAGLINE}}</p>
      </div>
      <div>
        <h4 class="text-white font-semibold mb-4">Product</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="#features" class="hover:text-white">Features</a></li>
          <li><a href="#pricing" class="hover:text-white">Pricing</a></li>
          <li><a href="#faq" class="hover:text-white">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4 class="text-white font-semibold mb-4">Company</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="#about" class="hover:text-white">About Us</a></li>
          <li><a href="#contact" class="hover:text-white">Contact</a></li>
          <li><a href="#blog" class="hover:text-white">Blog</a></li>
        </ul>
      </div>
      <div>
        <h4 class="text-white font-semibold mb-4">Connect</h4>
        <div class="flex gap-4">
          <a href="#" class="hover:text-white">Facebook</a>
          <a href="#" class="hover:text-white">Twitter</a>
          <a href="#" class="hover:text-white">LinkedIn</a>
        </div>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-center text-sm">
      <p>&copy; {{YEAR}} {{BRAND_NAME}}. All rights reserved.</p>
    </div>
  </div>
</footer>
```

### Khối thanh toán VietQR (SePay)
```html
<section id="thanh-toan" class="py-16 px-4 sm:px-6 lg:px-8 bg-white">
  <div class="max-w-2xl mx-auto text-center">
    <h2 class="text-3xl font-bold mb-6">Hoàn tất đơn hàng</h2>
    <p class="text-gray-600 mb-8">Mở ứng dụng ngân hàng, quét mã QR để chuyển khoản</p>

    <!-- Ảnh QR động. Đường dẫn chính thức hiện tại theo tài liệu SePay: https://vietqr.app/img
         (một số mẫu cũ dùng https://qr.sepay.vn/img — nếu ảnh không hiện thì đổi sang đường dẫn còn lại). -->
    <div class="bg-gray-50 p-8 rounded-lg inline-block">
      <img src="https://vietqr.app/img?acc={{SO_TAI_KHOAN}}&bank={{NGAN_HANG}}&amount={{SO_TIEN}}&des={{NOI_DUNG_CK}}&template=compact"
           alt="Mã QR chuyển khoản" class="w-64 h-64 mx-auto" loading="lazy">
    </div>

    <div class="mt-6 text-left max-w-sm mx-auto bg-gray-50 rounded-lg p-4 text-sm">
      <p><strong>Ngân hàng:</strong> {{NGAN_HANG}}</p>
      <p><strong>Số tài khoản:</strong> {{SO_TAI_KHOAN}}</p>
      <p><strong>Chủ tài khoản:</strong> {{CHU_TAI_KHOAN}}</p>
      <p><strong>Số tiền:</strong> {{SO_TIEN_HIEN_THI}}đ</p>
      <p><strong>Nội dung chuyển khoản:</strong> <span class="font-mono font-semibold">{{NOI_DUNG_CK}}</span></p>
    </div>
    <p class="text-xs text-gray-500 mt-3">Ghi đúng nội dung chuyển khoản để đơn được xác nhận nhanh.</p>
  </div>
</section>
```

---

## Công thức chữ (viết bằng tiếng Việt — con số phải có căn cứ thật)

### Tiêu đề chính
- **Lợi ích không kèm nỗi khổ:** `[Đạt kết quả] mà không cần [điều khách ngại]`
  - Ví dụ: "Tự quay video bán hàng đẹp bằng điện thoại — không cần thuê thợ quay"
- **Biến đổi:** `Từ [hiện trạng] đến [mong muốn] trong [thời gian]`
  - Ví dụ: "Từ chưa biết nhồi bột đến bán được mẻ bánh mì đầu tiên trong 21 ngày"
- **Câu hỏi gợi trúng:** `Bạn muốn [kết quả] mà [không mất điều quý]?`

### Tiêu đề phụ
- **Sản phẩm – lợi ích:** `[Sản phẩm] giúp [ai] [lợi ích] để [mục tiêu lớn hơn]`
- **Bằng chứng số đông (chỉ khi có số thật):** `Đã có [số thật]+ [ai] [kết quả thật]`

### Chữ trên nút
- **Động từ + lợi ích:** "Giữ chỗ học thử miễn phí", "Nhận bảng giá qua Zalo", "Đặt lịch soi da"
- **Giảm rủi ro:** "Dùng thử 7 ngày, không hợp hoàn tiền" (chỉ ghi khi chính sách là thật)
- Tránh nút chung chung: "Gửi", "Tìm hiểu thêm", "Bắt đầu".

### Mẩu bằng chứng (chỉ dùng số liệu thật)
- `[Số]+ khách đã mua` · `[Điểm]/5 từ [số] đánh giá trên [nơi]` · `Đã lên [báo/kênh]` · `Đối tác: [tên thật]`

---

## SEO Meta Template

### Title Tag (50-60 characters)
```
[Primary Keyword] - [Benefit] | [Brand]
```
Ví dụ: "Khóa học làm bánh mì tại nhà – Bán được sau 21 ngày | Tiệm bánh Mây"

### Meta Description (150-160 characters)
```
[Benefit statement]. [Social proof]. [CTA phrase].
```
Ví dụ: "Học làm bánh mì tại nhà qua video, có người sửa bài. [Bằng chứng thật]. Giữ chỗ học thử ngay."

### Open Graph
```html
<meta property="og:title" content="[Catchier version of title]">
<meta property="og:description" content="[Same as meta description or more compelling]">
<meta property="og:image" content="[URL to 1200x630px image]">
<meta property="og:type" content="website">
```
