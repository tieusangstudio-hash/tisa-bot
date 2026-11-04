# No-Tech Walkthrough — Telegram Order Notifications

> For non-coders. Get an alert on your phone the moment an order comes in. UI wording may change slightly — look for similar text.

## What You'll End Up With
An order is paid → your phone buzzes with a Telegram message showing the order details.

## Steps (tick as you go)

- [ ] **1. Install Telegram** on your phone if you don't have it.
- [ ] **2. Create a bot** — in Telegram, search **@BotFather**, start it, send `/newbot`, follow prompts (name + username ending in `bot`). It gives you a **bot token** (a long string). Copy it safely.
- [ ] **3. Get your chat ID** — message your new bot once, then ask the AI to fetch your chat ID (it uses `getUpdates`). Or search **@userinfobot** and start it — it shows your ID.
- [ ] **4. Give AI the token + chat ID** — the AI wires them into your payment webhook so paid orders trigger a message.
- [ ] **5. Test** — trigger a test order / payment; confirm the message arrives.

## If You Get Stuck
| Problem | Fix |
|---------|-----|
| BotFather didn't give a token | Re-run `/newbot`, pick a different username (must end in `bot`) |
| No message arrives | Wrong chat ID, or you never messaged the bot first — message it, recheck ID |
| Message arrives late | Normal if server is waking; usually seconds |
| Token leaked | Ask BotFather to `/revoke` and issue a new one |

## How to Check It Works
Send a test message via the bot (AI can trigger it). If it lands on your phone → done.

## Customer Email (optional, via Resend)
Telegram notifies **you** (the owner). To also email the **customer** an order confirmation, see `resend-email-confirmation.md`.

## When to Ask for Help
Steps 1-3 are all yours (no code). Step 4 the AI handles. If the bot never responds even after messaging it, recreate the bot.
