# Using the toolshed when building a Grok Bot

The toolshed (`/workspace/toolshed`) is a list of verified free-tier tools for SME bots. It is maintained by tooly.
Other bots may read it but must not write to it.

## 1. What's in it
- `tools.csv`: things the **bot** calls (API, MCP, CLI, Grok plugin, SaaS). Up to 3 live rows per category.
- `apps.csv`: things a **human** installs (desktop apps, browser extensions, mobile apps).

tools.csv key columns:
| column | meaning |
|---|---|
| `category`, `sme_problem` | fixed category (see scripts/schema.py) and the business problem it solves |
| `type`, `mcp` | api, mcp, cli, plugin or saas; MCP server official, community or none |
| `grok_plugin_id` | set = native Grok Bot marketplace connector |
| `free_quota`, `quota_period` | e.g. `1,000 credits` / `month`; `pay_per_use: <fees>` = no fixed fee (counts as free) |
| `time_limited` | `none`, `trial_Nd`, `credits_expire` or `one_off_credit` (one-time credit, does not renew) |
| `card_required`, `paid_entry_usd`, `scale_pricing` | card needed for the free tier? First paid price (USD), and how pricing scales |
| `auth`, `token_notes` | key or OAuth setup. `token_notes` always starts `bot_access_free: <api\|mcp\|webhooks\|export joined by +, or none\|unknown>; ` (how a bot can read the tool on the FREE tier), then rate limits and token/credit tips |
| `rating_signals`, `best_for` | `signal, source, date`; when to pick it |
| `pricing_url`, `docs_url` | vendor pages (pricing_url is always clean) |
| `last_verified`, `verified_from`, `status` | date, source (pricing_page, docs or claim); status candidate, verified, tested, needs_review or deprecated |
| `referrer_benefit`, `referee_benefit`, `referral_terms_url`, `referral_link` | e.g. `30% rev 12mo`, `unpublished`, `none`; blank = no program known; referral_link is KT's own link |
| `notes` | at most 120 chars: `differentiator:`, region locks, `mcp unconfirmed`, `limits: <url>`, `superseded by <id> <date>` on swapped-out rows |

apps.csv adds `replaces`, `kind` (desktop, extension or mobile), `platforms`, `licence` (oss, freeware or freemium), `free_limits`,
`paid_upgrade_usd`, `download_url`, `repo_url` and `privacy_notes`. It has the same status, rating and referral columns.

## 2. Recipe for picking a new bot's tools
a. Break the bot's job into SME problems, then map each problem to a toolshed `category`.
b. Search the Grok Bot marketplace live: `SearchPlugins` for native connectors, `SearchBotTemplates` for template ideas.
c. Read the toolshed and filter by `category` and `sme_problem`. Prefer `tested` over `verified` over `candidate`.
   Skip `deprecated` and `needs_review` rows.
d. Rank highest the tools that are both a native plugin (`grok_plugin_id` set or found in step b) and a toolshed row.
e. If the bot must read the tool on the free tier, filter on the `bot_access_free:` tag (snippet in section 4); `none`/`unknown`
   means a paid plan or a human export. If there is no plugin, use the api, mcp or cli rows. State the `auth` and the key setup the user must do themselves.
   The bot never signs up or creates keys.
f. Suggest the matching `apps.csv` items (same SME problem) for the human to install.
g. Show the cost in every recommendation: `free_quota` per `quota_period`, `time_limited`, `card_required` and `paid_entry_usd`.
   Add `notes` when they hold a region lock or a caveat.
h. Link: use `referral_link` when it is set, otherwise `pricing_url`. Never use a referral link for the account owner's
   own sign-up, because vendors ban self-referral. When in doubt, use `pricing_url`.

Example line for a user:
`Tally (forms): unlimited forms + submissions (fair use), no time limit, card requirement unknown; paid from $24/mo. https://tally.so/pricing`

## 3. Rules
- **Read-only.** Never edit the CSVs. Send proposed changes to tooly, who applies them with `scripts/upsert.py`,
  which validates them and writes the changelog.
- **Freshness.** Quotas are true as of `last_verified`. If that date is more than about 60 days ago, re-check the vendor's
  `pricing_url` before quoting a limit or a price to a user.
- **Scope.** Prices are in USD and global. Regional differences and region locks are in `notes`.
  `verified_from=claim` means the figure is unconfirmed: say so.
- **Business tools only.** The cap is a hard 5 live rows per category (KT, 2026-10-29). Better finds replace the weakest row:
  the old row becomes `deprecated` with a `superseded by <id> <date>` note, so skip deprecated rows.

## 4. Snippet
```python
import csv, re
OK = {"tested": 0, "verified": 1, "candidate": 2}
rows = [r for r in csv.DictReader(open("/workspace/toolshed/tools.csv")) if r["category"] == "forms" and r["status"] in OK]
access = lambda r: set(re.match(r"bot_access_free: ([a-z+]+)", r["token_notes"]).group(1).split("+"))
bot_readable = [r for r in rows if access(r) & {"api", "mcp", "webhooks"}]  # a bot can pull data on the free tier
for r in sorted(rows, key=lambda r: (not r["grok_plugin_id"], OK[r["status"]])):
    print(r["name"], r["free_quota"], r["quota_period"], r["paid_entry_usd"], r["referral_link"] or r["pricing_url"])
```
csvkit: `csvgrep -c category -m forms tools.csv | csvgrep -c status -r '^(tested|verified)$' | csvcut -c name,free_quota,quota_period,paid_entry_usd,pricing_url`

## 5. Offloading bulk public-text work to Gemini (`scripts/gemini_offload.py`)
Stdlib only. It sends bulk, low-stakes, **public** text jobs (classify, tag, extract, summarise, translate) to the Gemini free tier.
Free-tier prompts may be used by Google and seen by human reviewers, so private data must never go there.
```bash
python3 scripts/gemini_offload.py --plan --task-type tag --prompt "Category for: {text}" items.jsonl     # decide, 0 calls
python3 scripts/gemini_offload.py --task-type tag --prompt "Category for: {text}" --out res.jsonl items.jsonl
python3 scripts/gemini_offload.py --savings      # running ESTIMATE of Grok tokens saved
```
- **Input:** JSONL `{id, text, source}`.
- **Output:** JSONL `{id, status ok|handed_back, reason, output}` plus a final `{"summary":...}` line.
- **Handed-back items must be done in Grok.** The reasons are `private_source`, `pii:<type>`, `daily_cap`, `rate_limited`, `server_error`, `api_error:<code>` and `no_key`.
- **Gate 1:** `source` must be one of web, vendor_page, public_listing or toolshed.
- **Gate 2:** a regex scan for emails, AU/international phones, cards (Luhn), TFN/ABN/ACN, IBAN, API keys/secrets and street addresses. Matched text is never logged.
- **Plan routes to Grok** for judgment or user-facing tasks, fewer than 20 eligible items, under 15k estimated tokens, more than 50% blocked, an exhausted daily cap, or no key. A real run refuses (exit 3) unless you pass `--force`.
- **Pacing:**
  - Starts at a 2 s gap. A 429 doubles it (max 60 s) and Retry-After is honoured. 20 straight successes shrink it by 10% (min 2 s).
  - A daily cap holds until midnight US Pacific.
  - State is kept in `scripts/state/gemini_pacing.json`.
- **Key:** `GEMINI_API_KEY` from the env, sent in the `x-goog-api-key` header. Never print it.
- **Default model:** `gemini-3.1-flash-lite`. Keys created after Google's cutoff get a 404 for `gemini-2.5-flash-lite`. The fallback is `--model gemini-3.5-flash-lite`.
