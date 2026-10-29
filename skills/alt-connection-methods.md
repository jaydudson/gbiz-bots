# Alt Connection Methods
Version: 1

Use this only when the client mentions an app or service the bot has no native Grok Bot connector for, asks about Zapier, Make or n8n, or wants background automation that runs without the bot thinking each time.

## When to use
- An app has no native connector, or the client asks how the bot could reach it.
- Not for recommending products of ours (that is a different skill) and not for picking tools for a new bot (that happens at build time).

## Required inputs and access
- The client's current tool list (already in their profile; see `client-profile`).
- No new access is needed to discuss options.

## Sequence of work
1. Check whether a native connector already exists for the app. If yes, use it and say the bot can work directly in it.
2. If not, explain the practical options in 3 to 4 short sentences:
   - A tool with an official MCP server or an API the bot can call directly.
   - An automation platform (Zapier, Make, n8n) for set-and-forget workflows that run without the bot deciding each time.
   - A human export or manual step, if neither exists.
3. If a free or freemium option fits, name the best one and its cost. Prices are indicative; check the vendor's own page before quoting a limit or price.
4. If a tool is region-limited, only suggest it when the client's country is known and matches. Read it from their profile; ask once if needed.
5. Do not push. Stop after the explanation unless the client wants to go ahead.

## How to validate
- The client understands the difference and does not feel sold to.
- No tool was installed or connected, and no account was created, without an explicit yes.

## What to return
- A short plain-English note (or nothing, if the topic was only background). Never a long comparison.
- When a referral link is used, one plain line: "We use a referral link where one exists - it often gives you a small benefit at no extra cost." Offer the plain link on request.

## What requires approval
- Connecting Zapier, Make, n8n, Notion or any new platform; creating any account or key; anything that spends money. Always ask first.
- Tools are third-party and used under their own terms. We do not control them.

## Token notes
Load only when relevant. Keep replies short. Prefer native connectors when they exist.
