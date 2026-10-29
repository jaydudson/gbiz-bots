# Install Pack
Version: 1

Use this only when the client pastes an install prompt, says they bought bots, asks to add a bot they bought, or comes back after leaving an install unfinished.

This skill is fetched and followed from its link each time. Do not save it into the client's skill library.

## When to use
- A new client's first prompt, an existing client adding a Specialist, or a client resuming.
- Not for building or editing bots. Not for anything the client did not buy.

## Required inputs and access
- The manifest link from the prompt: the list of bots the client bought, each with its template link.
- Permission to fetch links and to write in `/workspace/bot-setup/`.
- Never assume a first-time client. Check what already exists before adding anything.

## Sequence of work
1. Read `/workspace/bot-setup/installed.md` if it exists. It is the receipt of everything already installed.
2. Fetch the manifest. For each bot, mark it installed, partly installed or not started.
3. Shared skills first (`client-profile`, `token-economy` and any a template names): apply the add-only rules below. Their files are at `skills/<id>.md` in the repo root, which is the template link without its trailing `bots/<id>/template.yaml`.
4. One bot at a time:
   - Fetch its `template.yaml` and follow its `install:` block.
   - Create or configure the bot from the template (its `description` field becomes its standing instructions).
   - Run its setup skill. Ask only for gaps, following `client-profile`.
   - Produce its first output and confirm with the client before the next bot.
5. Connectors: at most one new connector or tool set-up per bot. Mark the rest "later".
6. Keep the top of `installed.md` current: the manifest link, the time of last activity, and what is still to do.
7. If the client leaves with the install unfinished:
   - When they return after a few hours, ask on their next message, for example "When you are ready, you still have 3 bots to install. Shall we carry on?"
   - Keep one temporary reminder routine while anything is unfinished, at a falling cadence (about day 1, 3, 7, then weekly up to 4 weeks). Vary the wording each time and always give the number of bots left.
   - Delete the routine when everything is installed or the client says stop. After the last reminder, leave one line in `installed.md` so any bot can offer to resume later.

## Add-only rules (apply to every skill, every time)
Phase 1 (do now):
- Our content is wrapped in `<!-- pack:begin <id> v<n> -->` and `<!-- pack:end <id> -->`.
- Skill missing: add it whole, inside the markers.
- Client already has a skill with the same purpose: leave it untouched, skip ours, and tell the client in one plain line.
- Prompt and memory: add supplementary lines only. Never rewrite or remove the client's own instructions.

Phase 2 (parked, not enabled yet; do not do these):
- Add only what the client's skill lacks, as a marked supplement at the end.
- Refresh our own marked block, only if it still matches the hash recorded in `installed.md`.
- If the client edited or removed our block, treat it as theirs.

## How to validate
- List the skills now in the library and compare to what the manifest and templates promised. Every id must be present or recorded as skipped.
- `installed.md` has a row (kind, id, version, hash, date) for everything installed.

## What to return
- A short status in plain English: installed, skipped because the client already had their own, failed, still to do. No file contents, no long lists.

## What requires approval
- Adding a supplement to a skill the client already has.
- Refreshing a block the client edited.
- Connecting any account or tool; anything that spends money.
- Never delete or overwrite the client's skills, memory or files.
