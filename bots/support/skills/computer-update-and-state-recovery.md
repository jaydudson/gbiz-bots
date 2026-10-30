# Computer Update & State Recovery
Version: 1

## When to use
An official update is available, or the client is about to Update, Recover, or Reset the computer. Also use after a rebuild to help restore state.

## Required inputs and access
- Current list of skills
- Key folders under /workspace
- Official docs on what Update / Recover / Reset keep and lose

## Sequence of work
1. Pre-update audit:
   - List the folders currently under /workspace. These normally stay.
   - Note that bots, chats, and saved logins stay.
   - Quietly note any extra tools that were installed (these are the only things that need putting back).
   - Note any unsaved work.
   - State a clear, calm boundary: the important things stay; only extra tools need reinstalling if wanted.
   - Do not move or reorganise any folders.
2. Archive choice (interactive, guidance only):
   - After the audit, ask the client which items (if any) they want an external archive copy of. Offer a simple multi-choice or free text so they can pick specific folders, files, or “none / no archive”.
   - Let them choose any connector service they already have connected (Drive, Notion, GitHub, Dropbox, OneDrive, or whatever else is available), or attach the final file to this chat, or skip.
   - Once they choose, guide the copy step by step. Do not move or copy anything yourself without explicit approval for each action.
3. Guide the chosen action (Update preferred when available).
4. After the rebuild, check that bots and skills are still present. If any extra tools are missing, simply ask: “Want me to put the extra tools back?” If they say yes, handle the reinstall. Conversation history and saved bots/files/logins are normally kept.

## How to validate
The client has a clear list of what is at risk, has chosen what (if anything) to archive externally, and has a plan to protect or restore it. After the action, bots respond and key skills are available.

## What to return
Short audit summary with the boundary line, the client’s archive choices, recommended action, and post-action check list.

## What requires approval
Any Update, Recover, or Reset. Any file copy or move. Never proceed without explicit client approval.