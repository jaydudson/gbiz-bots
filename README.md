# gbiz-bots

Ready-made bot templates and skills. A client's own bot installs them from the raw links here, using the short prompt the client receives after purchase. Nothing here needs to be read by a person.

| Folder | What it holds |
|--------|---------------|
| `bots/<bot-id>/` | One bot: `template.yaml`, plus its `skills/` and `references/` |
| `skills/` | Skills shared by several bots |
| `packs/` | Pack manifests and starter prompts |
| `tools/` | The current list of free and freemium tools, refreshed weekly |
| `index.json` | Generated list of every bot and shared skill, with versions |

This repo is generated. Do not edit it by hand: changes are made in the private source repo and published with a script, and every push is checked automatically. `tools/` is the only exception; it is updated on a routine.

Third-party tools are used under their own terms. Prices shown are indicative and in USD; always check the vendor's own page.
