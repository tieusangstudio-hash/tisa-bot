# Resend Deliverability — Verify Domain & Stay Out of Spam

> Getting transactional email to actually land in the inbox. Covers domain verification (SPF/DKIM/DMARC), spam avoidance, and templates. DNS how-to is shared: `_chung/dns-basics-for-nontech.md` — this file lists only the email-specific records.

## Why This Matters
Send from `you@yourbrand.com` (verified) instead of a generic address → emails look legit and reach the inbox. Skip this → order confirmations and product deliveries land in spam.

## Step 1 — Add Your Sending Domain in Resend
1. Resend dashboard → **Domains → Add Domain** → enter `yourbrand.com`.
2. Resend generates a set of **DNS records** for you to add.

## Step 2 — Add the DNS Records
Add these at your registrar (how = `_chung/dns-basics-for-nontech.md`). Resend gives the exact values — paste them exactly.

| Purpose | Record type | What it does |
|---------|-------------|--------------|
| **SPF** | TXT | Says which servers may send mail for your domain |
| **DKIM** | TXT (or CNAME) | Cryptographically signs your mail (proves it's really you) |
| **DMARC** | TXT | Policy telling inboxes what to do with fakes |
| **MX** (if asked) | MX | Mail routing (only if Resend requests) |

> Trust the values on **your** Resend screen, not any example — they're unique to your domain.

## Step 3 — Verify
- Back in Resend, click **Verify**. Green = done. May take minutes to a couple hours (DNS propagation).
- MCP-first: if the Resend MCP is connected, the AI can help check status and send a test.

## Step 4 — Send a Test
- Send one real email to yourself. Confirm it lands in **Inbox**, not Spam/Promotions.

## Staying Out of Spam
- **Verified domain** (above) is the #1 factor.
- Warm up a new domain — don't blast hundreds of emails on day one.
- Avoid spammy words in subject ("FREE!!!", excessive caps/emoji).
- Keep transactional emails clean and relevant (confirmation, delivery — not marketing blasts).
- Include a real from-name and a way to reply.

## Transactional Templates (use these types)
- **Order confirmation** — see `resend-email-confirmation.md`
- **Product delivery** — run `/ts-giao-hang-tu-dong`
- **Receipt** — amount, order id, date, support contact.

## If You Get Stuck
| Problem | Fix |
|---------|-----|
| Verify never turns green | Record value/type wrong — recheck per DNS basics; wait for propagation |
| Emails still in spam after verify | Warm up slowly; clean content; ensure SPF+DKIM+DMARC all pass |
| DKIM fails | Often a pasted-value error (line breaks/spaces) — re-copy exactly |

## Related
- Shared DNS how-to: `_chung/dns-basics-for-nontech.md`
- Website domain (Vercel, different records): run `/ts-dua-web-len-mang`
