# Custom Domain Setup — From .vercel.app to Your Own Domain

> The step most non-tech users get stuck on: replacing `your-page.vercel.app` with `yourbrand.com`. This covers buying a domain, pointing DNS, verifying, and SSL. DNS mechanics are in the shared `_chung/dns-basics-for-nontech.md` — this file only lists the specific records.

## The Big Picture
`yourbrand.com` → (DNS points it) → your Vercel page → (HTTPS auto) → live, professional.

## Step 1 — Do You Have a Domain?
- **No** → buy one. The AI can check availability + price with `check_domain_availability_and_price`. Buy at Vercel Domains (simplest — DNS auto-configured) or a VN registrar (Mắt Bão, PA Vietnam) / global (Namecheap, Cloudflare).
- **Yes** → go to Step 2.

## Step 2 — Add the Domain in Vercel
1. Open your project in Vercel → **Settings → Domains**.
2. Type your domain (`yourbrand.com`) → **Add**.
3. Vercel shows you the **DNS records** to add.

## Step 3 — Point DNS (the records)
> **If you bought the domain at Vercel:** skip this — Vercel configures DNS for you. Done.

> **If your domain is elsewhere:** add these at your registrar. How to add records = `_chung/dns-basics-for-nontech.md`.

Vercel typically asks for one of:
| For | Record | Value |
|-----|--------|-------|
| Root (`yourbrand.com`) | **A** | the IP Vercel shows (e.g. `76.76.21.21`) |
| `www` subdomain | **CNAME** | `cname.vercel-dns.com` (or what Vercel shows) |

Paste exactly what **your** Vercel screen shows (values can change — trust the screen, not this example).

## Step 4 — Verify + SSL
- Back in Vercel, it auto-checks the records. When it sees them → domain turns **Valid**.
- **HTTPS/SSL is automatic** — Vercel issues the certificate for free. Wait a few minutes.
- Propagation can take minutes to a couple hours (normal).

## Step 5 — Confirm
- Open `https://yourbrand.com` — it loads your page on HTTPS (padlock icon).
- Check both `yourbrand.com` and `www.yourbrand.com`.

## If You Get Stuck
| Problem | Fix |
|---------|-----|
| Vercel says "Invalid Configuration" | Records not added correctly — recheck value/type per the DNS basics file |
| Works on `www` but not root (or vice versa) | Add the missing record (both A for root and CNAME for www) |
| Still not working after 1-2 hours | DNS propagation delay; verify with dnschecker.org |
| No padlock / "not secure" | SSL still issuing — wait; if hours pass, re-add domain |

## Related
- DNS how-to (shared): `_chung/dns-basics-for-nontech.md`
- Email domain (Resend, different records): see `/ts-giao-hang-tu-dong` (Resend domain verification)
