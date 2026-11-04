# Official Docs Index — Telegram + Resend

> Authoritative documentation links for the notification toolstack. **Fetch before giving setup/API instructions** — do not rely on memory for API details.

## When to Fetch (token-aware)
- **Fetch** when: setting up a bot, needing a specific API method, webhook payload, or troubleshooting.
- **Don't fetch** for general questions.
- **Rule:** live docs override prior knowledge on conflict.

## Telegram Bot (order notifications to the shop owner)
| Topic | URL |
|-------|-----|
| Bot API reference | https://core.telegram.org/bots/api |
| Bot intro / BotFather | https://core.telegram.org/bots |
| sendMessage method | https://core.telegram.org/bots/api#sendmessage |
| getUpdates / webhooks | https://core.telegram.org/bots/api#getupdates |

## Resend (email confirmation to the customer)
| Topic | URL |
|-------|-----|
| Docs home | https://resend.com/docs |
| Send email API | https://resend.com/docs/api-reference/emails/send-email |
| Node/SDK quickstart | https://resend.com/docs/send-with-nodejs |
| Domain verification (DNS) | https://resend.com/docs/dashboard/domains/introduction |

> MCP note: if the Resend MCP is connected, prefer it to send/test emails instead of raw API.

## What to Extract When Fetched
- Telegram: bot token format, chat_id retrieval, message formatting (Markdown/HTML).
- Resend: API key usage, `from` address requirements (verified domain), payload schema.

## Cross-References
- No-tech step-by-step: `no-tech-walkthrough.md`
- Email confirmation setup: `resend-email-confirmation.md`
- Message templates: `notification-message-templates.md`
