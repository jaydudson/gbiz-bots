# Grok Bot storage and durability reference

## Official recommendation
The durable place for project files, reports, CSVs, notes, and outputs is `/workspace` with clear project folders.

Source: https://docs.x.ai/grok-bot/computer-and-apps

Files, browser state, and supported sign-ins are designed to survive normal computer updates and recovery. Treat temporary directories, manually installed packages, and uncommitted application state as replaceable. Copy important results into the shared workspace or attach them to the conversation.

## What survives
| Asset | Survives Update | Survives Reset | Notes |
|-------|-----------------|----------------|-------|
| Files under `/workspace` | Yes (normally) | Yes if already in the last saved snapshot | Official durable area. Shared by all bots. |
| Bot profiles, skills, conversation history | Yes | Yes (chats always; skills usually) | Stored outside the pure computer snapshot. |
| Installed packages / CLIs | No | No | Always reinstall after Update / Recover / Reset. |
| Temporary or cache folders | No | No | Treat as disposable. |
| Very recent unsaved work | Depends | Can be lost if computer could not be reached to save first | Snapshot rule. |

Conversations are stored outside the computer and survive even a Reset.

## Recommended sustainable shape (low-risk)
Do not move existing folders. That risks breaking running bots or routines.

Going forward:
- Keep new durable working files in clear project folders under `/workspace` (example: `/workspace/bills`).
- For anything critical, also keep a copy in a connected service (Google Drive, Notion, GitHub for text) or attach the final file to the conversation.
- Installed tools are always replaceable.
- Bot instructions and skills are platform-managed; still keep an external copy of any critical process.

## Implications
- Inside `/workspace`: normally survives Update and is the place the docs tell bots to keep durable work. Still subject to the snapshot rule.
- Outside `/workspace`: higher chance of being dropped on Update / Recover / Reset. Not the recommended durable location.

## Guidance for Support bot
Stay guidance-only and least-destructive.
- List folders currently under `/workspace`.
- Note that these normally survive an Update.
- Note that bots, chats, and saved logins are safer still.
- Flag installed packages that would need reinstalling.
- Do not move folders.
- Offer to help inventory or suggest an external copy for critical items, but do not proactively relocate anything.
- Lookback for the update-watch routine = 2× the current interval.
