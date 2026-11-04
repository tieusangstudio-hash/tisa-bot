# No-Tech Walkthrough — SePay Payment

> For users who don't code. Step-by-step to accept VietQR payments. UI wording may differ slightly over time — look for the button with similar text. When a real API detail is needed, the AI fetches `official-docs-index.md` first.

## What You'll End Up With
Customer scans a QR → pays via bank app → you get money + an automatic notification. No manual checking.

## Steps (tick as you go)

- [ ] **1. Create a SePay account** — go to my.sepay.vn, sign up, log in.
- [ ] **2. Connect your bank** — in the dashboard, add the bank account that receives money. Follow SePay's on-screen bank-linking.
- [ ] **3. Get your API key** — find "API" / "Cấu hình" / "Tích hợp" in the dashboard, generate a key. Copy it somewhere safe (treat like a password).
- [ ] **4. Set the webhook URL** — this is the address SePay calls when money arrives. If your landing page is on Vercel, it's usually `https://your-site/api/webhook`. Paste it in SePay's webhook settings. (The AI generates the webhook handler for you.)
- [ ] **5. Test with a small amount** — pay yourself 2.000đ via the QR. Confirm the notification fires.

## If You Get Stuck
| Problem | Fix |
|---------|-----|
| QR doesn't show | Amount/params wrong — ask the AI to regenerate the QR link |
| No notification after paying | Webhook URL wrong or not reachable — recheck the URL, confirm the site is live |
| "Unauthorized" errors | API key mismatch — regenerate and re-paste |
| Money arrives but no order match | Transaction content parsing — ask AI to fix order-matching logic |

## How to Check It Works
Pay yourself a tiny amount. Within seconds you should see the payment recorded / notification sent. If yes → done.

## When to Ask for Help
You can do steps 1-3 yourself. Steps 4-5 (webhook) the AI handles the code — you just paste the URL. If your bank won't link or verification fails, that's a SePay support issue, not something to force.
