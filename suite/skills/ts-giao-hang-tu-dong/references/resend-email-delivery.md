# Resend — Digital Product Delivery by Email

> Deliver the purchased product (link/file) to the customer automatically by email using Resend. Transactional, professional, trackable. Pairs with SePay payment trigger.

## Why Resend for Delivery
- Transactional email built for exactly this (order → send product).
- Deliverability tools (see `resend-deliverability.md`) keep it out of spam.
- Works with a verified sending domain so emails come from `you@yourbrand.com`.

## MCP-First
If the **Resend MCP** is connected, the AI sends and tests emails directly — no raw API handling for the user. If not, it uses the API with your key (fetch `official-docs-index.md` for the current endpoint).

## Setup Flow
1. **Create a Resend account** + get an API key (resend.com).
2. **Verify your sending domain** — required to send from your brand address and avoid spam. Full DNS steps in `resend-deliverability.md`.
3. **Connect the trigger** — payment confirmed (SePay webhook) → AI calls Resend to send the product email.
4. **Compose the delivery email** — thank-you + download link/attachment + next steps.
5. **Test** — buy your own product; confirm email + link work.

## Delivery Content Checklist
- [ ] Clear subject ("Your [product] is ready ✓")
- [ ] The actual link or attachment (stable, non-expiring)
- [ ] What to do next (how to access/use)
- [ ] Support contact (Zalo/email) if they need help
- [ ] From a verified domain address (not a generic one)

## Attachments vs Links
- **Small file (<a few MB)** → attach directly.
- **Large / course / access** → send a stable link (Drive, hosting, or your platform).

## If It Fails
| Problem | Fix |
|---------|-----|
| Email not sent | API key / domain not verified — recheck |
| Lands in spam | See `resend-deliverability.md` (SPF/DKIM/DMARC) |
| Link broken | Use permanent hosting; AI can regenerate |

## Cross-References
- Deliverability + DNS: `resend-deliverability.md`
- Shared DNS basics: `_chung/dns-basics-for-nontech.md`
- Official docs: `official-docs-index.md`
