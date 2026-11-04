# Post-Launch Operations — Keep It Running

> Everything's set up and selling. This is what to do when things drift or break over time — the "after it works" maintenance non-tech owners rarely get told about.

## The Periodic Check (do monthly)
- [ ] Make a small test purchase end-to-end (pay → notify → deliver) — the fastest way to catch silent breakage.
- [ ] Confirm payment notifications still arrive.
- [ ] Confirm delivery email still lands (and not in spam).
- [ ] Check the landing page still loads on mobile.
- [ ] Note any API keys / tokens nearing expiry.

## Common Failures & Fixes
| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Payments work but no notification | Bot token revoked, chat_id changed | Recheck Telegram token/chat_id (run `/ts-bao-don-telegram`) |
| Order paid but product not delivered | Delivery trigger broke, or payment webhook not firing | Test webhook first, then delivery step |
| Emails suddenly go to spam | Domain reputation / DNS drift | See `resend-deliverability.md` |
| "Unauthorized" / key errors | API key rotated or expired | Regenerate key, update it in config |
| Landing page down | Deploy/domain issue | run `/ts-dua-web-len-mang` (update / rollback) |

## Keys & Tokens Hygiene
- Store keys somewhere safe (not in public files/screenshots).
- If a key leaks → rotate it immediately (SePay key, bot token, Resend key).
- After rotating, update every place that used the old key, then test.

## When Something Breaks Mid-Sales
1. Don't panic — check the periodic-check list to isolate which stage failed.
2. Fix that one stage (payment / notification / delivery / page).
3. Re-run a test purchase to confirm the whole chain works again.

## Escalation Honesty
- Config/keys/triggers → the AI can fix with you.
- Bank linking, account verification, provider outages → that's SePay/Telegram/Vercel/Resend support, not something to brute-force.

## Related
- Email deliverability: `resend-deliverability.md`
- Deploy issues: run `/ts-dua-web-len-mang`
