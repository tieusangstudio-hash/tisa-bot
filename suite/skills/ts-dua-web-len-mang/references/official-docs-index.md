# Official Docs Index — Vercel

> Authoritative documentation for deployment. **Fetch before setup/API instructions** — don't rely on memory. Vercel's UI and CLI change often.

## MCP-First (important)
Vercel has an **official MCP** (connector). If it is connected in your environment, prefer it over telling the user to click through the dashboard (tool names may differ by version):
| Task | MCP tool |
|------|----------|
| Deploy the current project | `deploy_to_vercel` |
| Check domain availability + price | `check_domain_availability_and_price` |
| Read build logs (debug a failed deploy) | `get_deployment_build_logs` |
| List deployments (for rollback) | `list_deployments` |
| Get a deployment's status | `get_deployment` |

If the MCP is not connected, fall back to the manual walkthrough. Never leave the user stuck.

## When to Fetch Docs (token-aware)
- **Fetch** when deploying for real, configuring a domain, or troubleshooting.
- **Don't fetch** for general questions. Live docs override prior knowledge.

## Vercel Docs
| Topic | URL |
|-------|-----|
| Docs home | https://vercel.com/docs |
| Deploying | https://vercel.com/docs/deployments/overview |
| Custom domains | https://vercel.com/docs/projects/domains |
| Adding a domain | https://vercel.com/docs/projects/domains/add-a-domain |
| DNS records | https://vercel.com/docs/projects/domains/managing-dns-records |
| CLI | https://vercel.com/docs/cli |
| Vercel Drop (drag & drop, no CLI) | https://vercel.com/docs/drop |
| Deploy without an account (temporary + claim) | https://vercel.com/docs/deployments/deploy-without-logging-in |
| Fair use / Hobby is non-commercial only | https://vercel.com/docs/limits/fair-use-guidelines |
| Pricing | https://vercel.com/pricing |

## Cross-References
- No-tech steps: `no-tech-walkthrough.md`
- After deploy (update/rollback/debug): `cap-nhat-va-quay-lai.md`
- Custom domain + DNS: `custom-domain-setup.md`
- DNS basics (shared): `_chung/dns-basics-for-nontech.md`
