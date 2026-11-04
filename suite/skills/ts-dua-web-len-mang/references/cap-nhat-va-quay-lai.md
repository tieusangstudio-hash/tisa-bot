# Deploy Lifecycle — After You Publish

> "Deployed... now what?" This covers the full life of a live page: publish, update, roll back, and debug failures. MCP-first — the AI does the heavy lifting.

## 1. Publish (MCP-first)
- AI uses `deploy_to_vercel` to publish the landing page → returns a live link.
- No CLI/Git needed for the user. Fallback: drag-and-drop or GitHub import (see `no-tech-walkthrough.md`).

## 2. After Deploy — What You Can Do
| Want to… | How |
|----------|-----|
| See it live | Open the returned link (check on phone + desktop) |
| Update the page | Edit the file → deploy again → **same link updates** (no new link) |
| See past versions | AI uses `list_deployments` to show deployment history |
| Roll back | Pick a previous good deployment from the list → promote it |
| Debug a failed deploy | AI uses `get_deployment_build_logs` to read the error and fix it |

## 3. Updating a Live Page
1. Change the HTML/content.
2. Ask the AI to redeploy.
3. The same URL now serves the new version. Old visitors get the update automatically.

> Tip: deploying doesn't create a new link each time for the same project — it updates in place.

## 4. When a Deploy Fails
The AI diagnoses instead of guessing:
1. `get_deployment_build_logs` (errorsOnly) → read the actual failure.
2. Common causes: missing file/asset, bad path, wrong project settings.
3. Fix → redeploy → confirm live.

## 5. Rolling Back (something broke)
1. `list_deployments` → find the last version that worked.
2. Promote/redeploy that one.
3. Live site returns to the good state while you fix the new version.

## Checklist After Every Deploy
- [ ] Link opens on mobile
- [ ] Images/assets load
- [ ] CTA / payment button works
- [ ] Looks right (no broken layout)

## Next
- Want your own domain instead of `.vercel.app`? → `custom-domain-setup.md`
