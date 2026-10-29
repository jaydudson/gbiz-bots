# Client Profile
Version: 1

Use this only before asking the client any set-up or background question, and when recording an answer so other bots need not ask again.

## When to use
- During a bot's first-run set-up, or any time it needs a fact about the client's business.
- Works the same for a new client, an existing client with their own notes, and a client adding a bot later.

## Required inputs and access
- Read access to the bot's own memory, the facts shared across the client's bots (name, time zone), and any profile or notes already on the shared computer.
- Write access only to `/workspace/bot-setup/client-profile-onboarding.md`.

## Sequence of work
1. Look in this order, reading only: platform shared facts; the client's existing profile or notes and this bot's own memory; our file `/workspace/bot-setup/client-profile-onboarding.md` if it exists.
2. List what this bot needs (its template's `ask_only_if_unknown`). Remove everything already known.
3. If nothing is missing, ask nothing. Say in one line what you already know and carry on.
4. Ask only the gaps, at most 3 questions in one turn, in plain English. Give the reason only if the client asks.
5. Record each answer in our file, adding or changing only this bot's own keys. Create the file only if it does not exist. Add a pointer ("see the client's own profile at ...") instead of copying facts that live elsewhere. The first time the file is created, say in one plain line: "I'll keep your answers in one place on your computer so your other bots don't ask again."
6. If the client says they keep notes or a profile somewhere else, offer once to add the answer there too. Never touch their files without a yes.

## How to validate
- No question was asked whose answer was already available.
- Nothing outside our file was created, edited or deleted.

## What to return
- One line: what you already knew, what you asked, what you stored.

## What requires approval
- Never edit or overwrite the client's own profile, notes or memory. The client's version always wins.
- Never store passwords, keys, financial or government identifiers.
- Never assume the client's country, currency or jurisdiction. Ask or read it.
