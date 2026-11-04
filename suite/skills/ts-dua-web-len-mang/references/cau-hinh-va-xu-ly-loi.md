# Cấu hình, xử lý lỗi & lệnh tham khảo — /ts-dua-web-len-mang

> Chuyển từ SKILL.md gốc (phần kỹ thuật dài). AI đọc khi cần: cấu hình `vercel.json`, đưa lên bằng Git,
> biến môi trường, sửa lỗi, lệnh CLI. Giao diện và lệnh của Vercel thay đổi thường xuyên — khi làm thật,
> đọc `official-docs-index.md` và tài liệu chính thức trước; tài liệu mới nhất luôn được ưu tiên.
> Mẫu cấu hình đầy đủ: `templates/vercel-config.json` trong thư mục skill.

## Deploy without an account (temporary)
- Browser: https://vercel.com/drop — drop a file, folder or `.zip` while logged out → live URL + **Claim your project**
  button + countdown. Static sites only; ≤100 MB per file, ≤1 GB total. Claim before it expires or it is gone.
- CLI: `vercel deploy --temporary` (or `npx vercel deploy --temporary`) → prints a claim URL
  ("Claim it to keep it live (don't share this link)"). Redeploy with the same command until it expires.
  Not available in CI or in a folder already linked to a Vercel project.
- Docs: https://vercel.com/docs/drop · https://vercel.com/docs/deployments/deploy-without-logging-in

## Hobby vs commercial use
Vercel Fair Use Guidelines: **Hobby teams are restricted to non-commercial personal use only.** Commercial usage
(any payment collection from visitors, advertising the sale of a product or service, affiliate-first sites, ads…)
requires **Pro** or Enterprise. Asking for donations is not commercial. Source: https://vercel.com/docs/limits/fair-use-guidelines
→ Always tell the user before they publish a selling page; let them choose Pro or another host.

## Other deploy methods

### Method 2: Git Deploy (Auto-deploy on Push)

**Best For:** Team collaboration, automated workflows, production sites

**Step-by-Step:**

1. **Push Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/repo.git
   git push -u origin main
   ```

2. **Connect to Vercel Dashboard**
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select your repository
   - Click "Import"

3. **Configure Project**
   - Framework Preset: Other (for static HTML)
   - Build Command: Leave empty
   - Output Directory: . (current directory)
   - Install Command: Leave empty

4. **Deploy**
   - Click "Deploy"
   - Wait 20-60 seconds
   - Get live URL

**Auto-Deploy Feature:**
- Every push to `main` branch → automatic production deploy
- Every push to other branches → preview deploy
- Pull requests get unique preview URLs

### Method 3: Drag & Drop

**Best For:** Non-technical users, quick testing, one-time deploys

**Step-by-Step:**

1. Go to https://vercel.com/new
2. Drag project folder to upload area
3. Wait for upload to complete
4. Click "Deploy"
5. Done - get live URL

**Limitations:**
- No auto-deploy on code changes
- Manual re-upload required for updates
- Not recommended for production

## Project Structure for Static Sites

```
my-landing-page/
├── index.html           ← Main landing page (REQUIRED)
├── thank-you.html       ← Post-purchase redirect (optional)
├── privacy-policy.html  ← Legal pages (optional)
├── terms.html
├── assets/
│   ├── images/
│   │   ├── hero-image.jpg
│   │   ├── product-photo.png
│   │   └── favicon.ico
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
└── vercel.json          ← Configuration file (optional)
```

**File Naming Rules:**
- Main page MUST be named `index.html`
- Use lowercase, hyphens for spaces: `thank-you.html`
- No spaces or special characters in file names

## vercel.json Configuration

Create `vercel.json` in your project root for advanced settings:

### Basic Configuration
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Security Headers
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

### Redirects
```json
{
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    },
    {
      "source": "/promo",
      "destination": "/special-offer",
      "permanent": false
    }
  ]
}
```

### Clean URLs (open `/cam-on` instead of `/cam-on.html`)
```json
{ "cleanUrls": true }
```

### Complete Production Config
See `templates/vercel-config.json` (in this skill folder) for full example

## Environment Variables

### When to Use
- API keys for third-party services
- Payment gateway tokens
- Analytics tracking IDs
- Feature flags

### How to Set

1. **Via Dashboard:**
   - Project → Settings → Environment Variables
   - Add key-value pairs
   - Select environments: Production, Preview, Development

2. **Via CLI:**
   ```bash
   vercel env add PAYMENT_API_KEY
   # Paste value when prompted
   ```

### Access in HTML (Client-Side)
```html
<script>
  // Environment variables are NOT available in static HTML
  // For security, use server functions or build-time replacement
</script>
```

### Best Practices
- Never expose API keys in client-side code
- Use environment-specific values
- Rotate keys regularly
- Document required variables in README

## Troubleshooting

### Error: "404 Not Found"

**Cause:** Missing `index.html` file
**Fix:** Ensure main file is named exactly `index.html`

```bash
# Check file name
ls
# Should show: index.html (not Index.html or home.html)
```

### Error: "Build Failed"

**Cause:** Build command configured for static HTML
**Fix:** Remove build settings

1. Go to Project Settings → General
2. Build Command: Leave empty
3. Output Directory: `.`
4. Install Command: Leave empty

### Error: "DNS Not Propagating"

**Cause:** DNS changes take time
**Fix:** Wait and verify

- Wait 24-48 hours maximum
- Check https://dnschecker.org
- Verify DNS records match Vercel requirements
- Contact domain registrar support if stuck

### Error: "Images Not Loading"

**Cause:** Incorrect file paths
**Fix:** Use relative paths

```html
<!-- ❌ Wrong -->
<img src="/Users/admin/project/image.jpg">
<img src="C:\project\image.jpg">

<!-- ✅ Correct -->
<img src="./assets/images/hero.jpg">
<img src="assets/images/hero.jpg">
```

### Error: "Site Loads Locally But Not on Vercel"

**Cause:** Case-sensitive file paths
**Fix:** Match exact file names

```html
<!-- Local (Windows): Works with any case -->
<img src="Assets/Images/Hero.jpg">

<!-- Vercel (Linux): Case-sensitive -->
<img src="assets/images/hero.jpg">
```

### Check Deployment Logs

```bash
# View recent deployment logs
vercel logs

# View specific deployment
vercel logs [deployment-url]
```

### Testing Commands
```bash
# Check SSL certificate
curl -I https://your-site.vercel.app

# Test page load time
curl -o /dev/null -s -w '%{time_total}\n' https://your-site.vercel.app
```

## Advanced Features

### Custom Error Pages

Create `404.html` for custom not-found page:
```html
<!DOCTYPE html>
<html>
<head>
  <title>Page Not Found</title>
</head>
<body>
  <h1>404 - Page Not Found</h1>
  <a href="/">Go Home</a>
</body>
</html>
```

### Analytics Integration

Add to `index.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Form Handling

Use form submission services:
- Formspree: https://formspree.io
- Netlify Forms (alternative platform)
- Web3Forms: https://web3forms.com

Example:
```html
<form action="https://formspree.io/f/your-form-id" method="POST">
  <input type="email" name="email" required>
  <button type="submit">Submit</button>
</form>
```

## Reference Links

- Official Docs: https://vercel.com/docs
- CLI Reference: https://vercel.com/docs/cli
- Platform Limits: https://vercel.com/docs/limits
- Status Page: https://vercel-status.com
- Community: https://github.com/vercel/vercel/discussions

## Quick Commands Reference

```bash
# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# List deployments
vercel list

# View logs
vercel logs

# Remove deployment
vercel remove [deployment-url]

# Link local project to Vercel project
vercel link

# Pull environment variables
vercel env pull

# Check CLI version
vercel --version

# Get help
vercel --help
```
