# Làm landing page theo ảnh mẫu / link tham khảo — /ts-landing-page

> Chuyển từ SKILL.md gốc. Dùng khi người dùng gửi ảnh chụp màn hình, ảnh thiết kế hoặc link một trang
> họ thích và muốn làm "giống phong cách này". Nguyên tắc: **học tinh thần, không sao chép** logo, ảnh,
> chữ có bản quyền của người khác. Luôn thêm chi tiết thật của doanh nghiệp Việt (giá VND, Zalo, địa chỉ).

### Phase 1: Visual Analysis (Read the Image)

Analyze the reference image across these 8 dimensions:

**1. Layout Architecture**
- Overall structure: single column, split-screen, asymmetric, grid-based?
- Section count and ordering (hero, features, pricing, etc.)
- Content width: full-bleed, contained (max-width), mixed?
- Vertical rhythm: section spacing (compact, normal, generous)?
- Breakpoint behavior: how might it adapt to mobile?

**2. Color Extraction**
- Primary brand color (dominant hue)
- Secondary color (supporting/accent)
- CTA button color (action color)
- Background colors per section (alternating? gradient? solid?)
- Text colors (heading vs body vs muted)
- Dark mode or light mode base?
- Special effects: gradients, overlays, glassmorphism?

Map extracted colors to closest Tailwind utilities:
```
primary: bg-[#HEX] or bg-blue-600
secondary: bg-[#HEX] or bg-indigo-500
accent/CTA: bg-[#HEX] or bg-orange-500
```

**3. Typography Assessment**
- Heading font style: sans-serif, serif, display, monospace?
- Body font style: clean sans, humanist, geometric?
- Heading weight: bold, extrabold, black?
- Size hierarchy: how much contrast between h1/h2/body?
- Letter spacing: tight, normal, wide?
- Line height: tight (1.2), normal (1.5), relaxed (1.75)?
- Special text treatments: gradient text, outlined text, rotated text?

Map to Google Fonts:
```
Heading: font-family: 'Inter', 'Poppins', 'Space Grotesk', etc.
Body: font-family: 'DM Sans', 'Open Sans', 'Nunito Sans', etc.
```

**4. Component Inventory**
List every UI component visible:
- Navigation (fixed? transparent? floating pill?)
- Hero type (centered text, split image+text, video background, animated)
- Cards (shadow, border, rounded, hover effects)
- Buttons (rounded, pill, ghost, gradient, icon+text)
- Forms (inline, stacked, multi-step)
- Badges/tags (pill, square, outline)
- Icons (line, filled, custom illustrations, emoji)
- Dividers (line, wave, angle, none)
- Footer (simple, multi-column, CTA footer)

**5. Spacing & Sizing Patterns**
- Section padding: py-12 (compact), py-20 (normal), py-32 (generous)?
- Card/element gaps: gap-4, gap-6, gap-8?
- Content max-width: max-w-4xl, max-w-6xl, max-w-7xl?
- Border radius: rounded-lg, rounded-xl, rounded-2xl, rounded-full?
- Shadow depth: shadow-sm, shadow-md, shadow-xl?

**6. Visual Effects & Animations**
- Background patterns (dots, grid, noise, blobs)
- Scroll animations (fade-in, slide-up, parallax)
- Hover effects (scale, shadow, color change, underline)
- Gradient usage (linear, radial, mesh)
- Blur/glassmorphism effects
- Floating/decorative elements
- Image treatments (rounded corners, shadows, overlays, masks)

**7. Content Density**
- Text-heavy vs visual-heavy ratio
- Number of CTAs visible
- Social proof density (testimonials, logos, stats)
- Whitespace philosophy (minimal, moderate, generous)

**8. Vietnamese Market Adaptation Notes**
- Does the design suit Vietnamese aesthetics?
- Font compatibility with Vietnamese diacritics?
- Payment section placement for VietQR?
- Trust signals appropriate for VN market?
- Mobile-first considerations for Vietnamese users?

### Phase 2: Design Mapping (Plan the Build)

After analysis, create a build plan:

```
DESIGN REFERENCE BUILD PLAN
============================
Template Base: [closest existing template or start fresh]
Layout: [layout description]
Color Scheme:
  - Primary: [color] → Tailwind: [class]
  - Secondary: [color] → Tailwind: [class]
  - CTA: [color] → Tailwind: [class]
  - Background: [color] → Tailwind: [class]
Font Pairing:
  - Heading: [font] → Google Fonts import
  - Body: [font] → Google Fonts import
Components Needed:
  1. [component] → [Tailwind approach]
  2. [component] → [Tailwind approach]
  ...
Special Effects:
  - [effect] → [CSS/Tailwind implementation]
Sections (top to bottom):
  1. [section name] — [brief description]
  2. [section name] — [brief description]
  ...
Estimated Complexity: [Low/Medium/High]
```

### Phase 3: Build (Generate HTML)

1. Start from closest template or build fresh
2. Apply color scheme via Tailwind config
3. Import correct Google Fonts
4. Build section by section, matching reference layout
5. Add special effects (gradients, animations, glassmorphism)
6. Implement responsive breakpoints
7. Add SePay/VietQR if payment needed
8. Run quality checklist

### Phase 4: Compare & Refine

After generating, compare output to reference:
- [ ] Overall layout matches reference structure
- [ ] Color scheme feels similar (exact match not required)
- [ ] Typography hierarchy matches
- [ ] Spacing and breathing room similar
- [ ] Key components present (nav, hero, features, CTA, footer)
- [ ] Special effects implemented (gradients, shadows, animations)
- [ ] Mobile responsive behavior appropriate
- [ ] Vietnamese market elements added where needed

### Important Notes for Design Reference Workflow
- **Match the spirit, not pixel-perfect**: Capture the feel, layout, and style — not every pixel
- **Respect copyright**: Don't copy logos, images, or proprietary content
- **Improve on weaknesses**: If reference has poor mobile UX or missing CTA, fix it
- **Add VN context**: Always adapt for Vietnamese market even if reference is Western
- **Stay Tailwind-native**: All styling via Tailwind utilities, no custom CSS unless absolutely necessary
- **Single-file output**: Keep everything in one HTML file for easy deployment

