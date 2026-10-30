# Choose Tools
Version: 1

Use this to pick a tool or app for a job from our current lists, at install and any time the client asks "what could do this?". Our two lists are the only source of tool suggestions and referral links.

## When to use
- At install, for the categories in your template's `setup.tool_categories`, but only for tools your template marks as needed now. Tools marked "later" wait until the client asks.
- Any time the client asks what tool or app could help with something, or asks to refresh the list.

## Required inputs and access
- Read the two lists from the repo root (the same root your template's skills come from): `tools/tools.csv` and `tools/apps.csv`. Read the header row first and use the columns it has. Never assume column names.
- The client's profile and existing tools (follow the client-profile skill). Never assume their country.
- Write access only to `/workspace/bot-setup/tools-seen.md` (tools offered, accepted or declined, with the date).

## Sequence of work
1. Fetch both lists. If they cannot be read, say so in one line, use a saved copy in `/workspace/bot-setup/` if there is one, and otherwise suggest nothing.
2. Keep only the rows for the category you need. Skip rows locked to a region that does not match the client.
3. Prefer a tool the client already uses. Otherwise choose the best for the job: free tier first, native connector or official MCP preferred. Offer at most one new tool per bot at install; the rest only when asked.
4. Offer it in plain English: what it does for this job, the free limit, the entry price (indicative), and that the client stays in control. If the row has a referral link, use it and add one plain line saying so. Best tool for the job always comes first.
5. Never set anything up, sign up or spend without the client's yes. On a yes, follow the install steps in your template.
6. Record what you offered and the answer in the file above. Do not offer a declined tool again.

## How to validate
- Every suggestion traces to a row in one of the two lists.
- No link came from anywhere else, and nothing was set up without a yes.

## What to return
- One short offer, or one line saying nothing fits or the client already has what is needed.

## What requires approval
- Signing up, installing, connecting an account, entering keys or spending anything.
- Never store passwords or keys in chat or files. Tools are third-party and used under the vendor's terms.
