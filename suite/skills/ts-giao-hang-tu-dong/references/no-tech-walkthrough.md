# No-Tech Walkthrough — Automated Delivery

> For non-coders. After a customer pays, they automatically receive the product (download link / file / access). No manual sending.

## What You'll End Up With
Payment confirmed → customer instantly gets their digital product by email (Resend) and/or Telegram.

## Steps (tick as you go)

- [ ] **1. Prepare the product** — the file or access link you deliver (PDF, video link, course access, license key).
- [ ] **2. Pick the delivery channel:**
  - **Email (Resend)** — most professional; see `resend-email-delivery.md`.
  - **Telegram** — sends the file/link via bot.
- [ ] **3. Connect the trigger** — the AI links "payment confirmed" (SePay webhook) → "send product". You just confirm which product goes to which offer.
- [ ] **4. Set the delivery message** — what the customer sees: thank-you + the link/file + next steps.
- [ ] **5. Test end-to-end** — do a test purchase; confirm the product arrives.

## If You Get Stuck
| Problem | Fix |
|---------|-----|
| Product not delivered after payment | Trigger not linked — recheck payment webhook fires first |
| Email not arriving | Domain not verified on Resend, or in spam — see `resend-deliverability.md` |
| Wrong product sent | Offer→product mapping — ask AI to correct it |
| Link expires / broken | Use a stable host; ask AI to set a permanent link |

## How to Check It Works
Buy your own product with a small real payment. The product should arrive within seconds. If yes → done.

## When to Ask for Help
You provide the product + message text. The AI wires the automation. If email keeps landing in spam, that's the deliverability step (`resend-deliverability.md`), not a delivery-logic problem.
