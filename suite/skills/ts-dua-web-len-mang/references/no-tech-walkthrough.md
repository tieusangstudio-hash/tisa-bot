# No-Tech Walkthrough — Publish Your Landing Page (Vercel)

> For non-coders. Get your landing page live on the internet with a real link. The AI does most of this **for you via the Vercel MCP** — you barely touch anything.

## What You'll End Up With
Your landing page live at a public link (e.g. `your-page.vercel.app`) — shareable, on HTTPS.

## The Easy Path (AI does it)
If the Vercel MCP is connected, the AI **deploys for you** using `deploy_to_vercel`. You just:

- [ ] **1. Have the landing page file ready** (from `/ts-landing-page`).
- [ ] **2. Connect Vercel** — log in / connect your Vercel account once (free tier is fine).
- [ ] **3. Say "deploy it"** — the AI runs the deploy and gives you the live link.
- [ ] **4. Open the link** — check it looks right on phone + desktop.

## Manual Fallback (no MCP)
| Method | How |
|--------|-----|
| Drag & drop | Go to https://vercel.com/drop → drag your folder (or a .zip) → Deploy |
| GitHub | Push the file to a GitHub repo → import it in Vercel |

The AI walks you through whichever fits.

## If You Get Stuck
| Problem | Fix |
|---------|-----|
| Deploy failed | AI reads the build log (`get_deployment_build_logs`) and fixes it |
| Page looks broken live | Usually a missing file/image path — AI checks and redeploys |
| Want to change it | Edit → deploy again (it overwrites the same link) — see `cap-nhat-va-quay-lai.md` |
| Ugly `.vercel.app` link | Use your own domain — see `custom-domain-setup.md` |

## How to Check It Works
Open the live link on your phone (not just desktop). If it loads and looks right → published.

## What's Next (don't stop here)
- **Change it later / roll back?** → `cap-nhat-va-quay-lai.md`
- **Want your own domain (not .vercel.app)?** → `custom-domain-setup.md`
