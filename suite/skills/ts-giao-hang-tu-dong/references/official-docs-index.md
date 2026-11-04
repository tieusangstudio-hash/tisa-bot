# Official Docs Index — Delivery (Telegram + Resend + webhook)

> Authoritative documentation for the delivery toolstack. **Fetch before setup/API instructions** — don't rely on memory.

## When to Fetch (token-aware)
- **Fetch** when setting up automated delivery, needing an endpoint, or troubleshooting.
- **Don't fetch** for general questions. Live docs override prior knowledge.

## Resend (digital product delivery via email)
| Topic | URL |
|-------|-----|
| Docs home | https://resend.com/docs |
| Send email (with attachment/link) | https://resend.com/docs/api-reference/emails/send-email |
| Attachments | https://resend.com/docs/dashboard/emails/attachments |
| Domain verification (DNS) | https://resend.com/docs/dashboard/domains/introduction |

> MCP: prefer Resend MCP to send delivery emails if connected.

## Telegram (delivery notification / file push)
| Topic | URL |
|-------|-----|
| Bot API | https://core.telegram.org/bots/api |
| sendDocument (send file) | https://core.telegram.org/bots/api#senddocument |

## SePay (payment confirmation triggers delivery)
| Topic | URL |
|-------|-----|
| Webhook | https://docs.sepay.vn/tich-hop-webhooks.html |

## What to Extract When Fetched
- Resend: how to attach files / include download links; verified `from` requirement.
- Trigger chain: payment webhook (SePay) → send delivery (Resend/Telegram).

## Cross-References
- Automated flow: `automated-delivery-workflow.md`
- Delivery methods: `digital-product-delivery-methods.md`
- Email delivery detail: `resend-email-delivery.md`
- No-tech steps: `no-tech-walkthrough.md`
