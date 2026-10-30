# gbiz-bots

Ready-made bot templates and skills. A client's own bot installs them from the raw links here, using the short prompt the client receives after purchase. Nothing here needs to be read by a person.

| Folder | What it holds |
|--------|---------------|
| `bots/<bot-id>/` | One bot: `template.yaml`, plus its `skills/` and `references/` |
| `skills/` | Skills shared by several bots, and `install-pack.md`, the installer a bot follows from its link |
| `packs/` | `<pack>.yaml`: the bots in a pack, in install order. `<pack>.start.txt`: the short prompt a client pastes into their first bot |
| `tools/` | Lists of free and freemium tools and apps (`tools.csv`, `apps.csv`), refreshed on a routine |
| `index.json` | Generated list of every bot and shared skill, with versions and the source commit |

This repo is generated. Do not edit it by hand: changes are made in the private source repo and published with a script, and every push is checked automatically. `tools/` is the only exception; it is updated on a routine.

Third-party tools are used under their own terms. Prices shown are indicative and in USD; always check the vendor's own page.
