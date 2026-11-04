# DNS Basics for Non-Tech Users (Shared Utility)

> Shared across the kit. DNS shows up in TWO places — pointing a website domain (Vercel: A/CNAME) and verifying an email domain (Resend: SPF/DKIM/DMARC/MX). Rather than explain DNS twice, this file teaches it **once**. The Vercel domain guide and the Resend deliverability guide link here and only list the specific records they need.

## What Is DNS (plain words)
A domain (like `yourbrand.com`) is just a name. DNS is the "address book" that tells the internet what that name points to — your website, your email, etc. To make something work with your domain, you add **records** to this address book.

## Where Do I Manage DNS?
Wherever you **bought the domain** (the "registrar") — e.g. Vercel Domains, Mắt Bão, PA Vietnam, GoDaddy, Namecheap, Cloudflare. Log in there and look for a section called **DNS**, **DNS Records**, **Quản lý DNS**, or **Zone Editor**.

> If you bought the domain at Vercel, DNS is managed inside Vercel automatically — much less to do.

## The Record Types You'll Meet
| Record | Plain meaning | Used for |
|--------|---------------|----------|
| **A** | Points the name to a server's IP address | Website (Vercel root domain) |
| **CNAME** | Points a name to another name | Website (`www` / subdomains, Vercel) |
| **TXT** | A text note the internet can read | Email verification (SPF, DKIM, DMARC) |
| **MX** | Where email for this domain goes | Email (sometimes needed by Resend) |

You don't need to understand them deeply. You **copy the exact values** the service gives you and **paste them** into your DNS.

## How to Add a Record (the universal steps)
1. Log into your registrar → open the **DNS / Records** section.
2. Click **Add Record**.
3. Choose the **Type** (A, CNAME, TXT, or MX) — the service tells you which.
4. Fill in:
   - **Name / Host** — often `@` (means the root domain) or something like `www` or a code the service gives.
   - **Value / Target** — paste exactly what the service gave you.
   - **TTL** — leave default (or "Auto").
5. **Save**.
6. Repeat for each record the service lists.

## Then You Wait (propagation)
DNS changes aren't instant — they spread across the internet. Usually **minutes**, sometimes up to a few hours. This is normal.

## How to Check It Worked
- Come back to the service (Vercel or Resend) and click **Verify / Refresh** — it turns green when it sees your records.
- Or use a free checker like dnschecker.org — paste your domain, see if the record appears.

## If You Get Stuck
| Problem | Fix |
|---------|-----|
| Verify still failing after 1 hour | Double-check you pasted the value exactly (no extra spaces), and picked the right Type |
| "Record already exists" | You may have an old conflicting record — edit it instead of adding a duplicate |
| Not sure Name should be `@` or `www` | Follow exactly what the service shows; `@` = root domain |
| Bought domain elsewhere, not sure where DNS is | It's at your registrar (where you paid), not at Vercel/Resend |

## Where This Is Used
- **Website domain (Vercel):** command `/ts-dua-web-len-mang` — needs A / CNAME.
- **Email domain (Resend):** command `/ts-giao-hang-tu-dong` (or `/ts-bao-don-telegram` for confirmation emails) — needs TXT (SPF/DKIM/DMARC) + sometimes MX.

Learn it here once; each of those tells you only which records to add.
