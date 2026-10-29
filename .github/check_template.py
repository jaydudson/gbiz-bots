"""Check bot templates against ops/template-structure-v1.md.

Usage:
    python ops/tools/check_template.py            # every bot in ops/bots, plus shared skills
    python ops/tools/check_template.py <bot-id>   # one bot (folder name, with or without underscore)
    python check_template.py --root <dir>         # check another tree with the same layout (the public repo)

Exit code 0 = all pass, 1 = at least one error. Deterministic: no network, no model.
Templates without `built_from` are treated as legacy v1 and get the core checks only.
"""
import re
import sys
from pathlib import Path

import yaml

ARGS = sys.argv[1:]
if "--root" in ARGS:  # the published repo runs this with --root . (same bots/ and skills/ layout)
    i = ARGS.index("--root")
    OPS = Path(ARGS[i + 1]).resolve()
    del ARGS[i:i + 2]
else:
    OPS = Path(__file__).resolve().parent.parent
BOTS = OPS / "bots"
SHARED = OPS / "skills"
EM_DASH = chr(0x2014)
UNIVERSES = {"primer", "specialist", "promo", "custom", "internal"}
AUTONOMY = {"L0", "L1", "L2", "L3"}
V11_FIELDS = [
    "name", "title", "universe", "category", "version", "built_from", "autonomy",
    "job", "deliverable", "anti_jobs", "approval_never", "setup", "no_data",
    "working_style", "token_efficiency", "skills", "share_safe",
]
VERSION_LINE = re.compile(r"^Version:\s*\d+\s*$")


def skill_version_error(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2 or not lines[0].startswith("# "):
        return "line 1 must be '# Title'"
    if not VERSION_LINE.match(lines[1]):
        return "line 2 must be 'Version: <integer>'"
    return None


def em_dash_errors(folder):
    errs = []
    for f in folder.rglob("*"):
        if f.is_file() and f.suffix.lower() in {".md", ".yaml", ".yml", ".txt"}:
            if EM_DASH in f.read_text(encoding="utf-8", errors="ignore"):
                errs.append(f"em dash in {f.relative_to(OPS)}")
    return errs


def check_bot(folder):
    errors, notes = [], []
    tpl = folder / "template.yaml"
    if not tpl.exists():
        return None, ["no template.yaml (skipped)"]
    try:
        data = yaml.safe_load(tpl.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"template.yaml does not parse: {exc}"], []

    bot_id = folder.name.lstrip("_").replace("_", "-")
    internal = folder.name.startswith("_")
    if data.get("id") != bot_id:
        errors.append(f"id '{data.get('id')}' does not equal folder name '{bot_id}'")

    strict = "built_from" in data
    if not strict:
        notes.append("legacy v1 template (retrofit pending): core checks only")

    if not internal and not str(data.get("install") or "").strip():
        errors.append("missing install block (bot must fetch and install its own skills)")
    if not internal and len(data.get("approval_never") or []) < 3:
        errors.append("approval_never needs at least 3 entries")

    listed = set()
    for sk in data.get("skills") or []:
        sid, src = sk.get("id"), sk.get("source", "new")
        if src == "shared":
            p = SHARED / f"{sid}.md"
        else:
            p = folder / (sk.get("path") or "")
            listed.add(p.resolve())
        if not p.exists():
            errors.append(f"skill '{sid}' not found at {p.relative_to(OPS)}")
        else:
            msg = skill_version_error(p)
            if msg:
                errors.append(f"skill '{sid}': {msg}")
    for ref in data.get("references") or []:
        p = folder / (ref.get("path") or "")
        listed.add(p.resolve())
        if not p.exists():
            errors.append(f"reference '{ref.get('id')}' not found at {p.relative_to(OPS)}")

    for sub in ("skills", "references"):
        d = folder / sub
        if d.is_dir():
            for f in d.rglob("*"):
                if f.is_file() and f.resolve() not in listed:
                    errors.append(f"{f.relative_to(OPS)} exists but is not listed in template.yaml")

    if strict:
        for field in V11_FIELDS:
            if field not in data:
                errors.append(f"missing required field '{field}'")
        if data.get("universe") not in UNIVERSES:
            errors.append(f"universe must be one of {sorted(UNIVERSES)}")
        if data.get("autonomy") not in AUTONOMY:
            errors.append(f"autonomy must be one of {sorted(AUTONOMY)}")
        if not data.get("anti_jobs"):
            errors.append("anti_jobs must not be empty")
        setup = data.get("setup") or {}
        if not setup.get("check_first"):
            errors.append("setup.check_first is required")
        if len(setup.get("ask_only_if_unknown") or []) > 3:
            errors.append("setup.ask_only_if_unknown has more than 3 questions")

    errors += em_dash_errors(folder)
    return errors, notes


def check_shared():
    errors = []
    for f in sorted(SHARED.glob("*.md")):
        msg = skill_version_error(f)
        if msg:
            errors.append(f"shared skill {f.name}: {msg}")
    return errors


def check_names(folders):
    """Skill ids must be unique across the universe and never equal a bot id.

    All of a client's skills share one library, whichever folder they shipped in.
    """
    errors, owners = [], {}
    bot_ids = {p.name.lstrip("_").replace("_", "-") for p in folders}
    for f in SHARED.glob("*.md"):
        owners.setdefault(f.stem.lstrip("_"), []).append(f"ops/skills/{f.name}")
    for folder in folders:
        tpl = folder / "template.yaml"
        if not tpl.exists():
            continue
        data = yaml.safe_load(tpl.read_text(encoding="utf-8")) or {}
        for sk in data.get("skills") or []:
            if sk.get("source", "new") != "shared":
                owners.setdefault(sk.get("id"), []).append(f"{folder.name}/{sk.get('path')}")
    for sid, where in sorted(owners.items()):
        if len(where) > 1:
            errors.append(f"skill id '{sid}' used more than once: {', '.join(where)}")
        if sid in bot_ids:
            errors.append(f"skill id '{sid}' equals a bot id")
    return errors


def main():
    wanted = ARGS[0].lstrip("_").replace("-", "_") if ARGS else None
    folders = sorted(p for p in BOTS.iterdir() if p.is_dir())
    if wanted:
        folders = [p for p in folders if p.name.lstrip("_").replace("-", "_") == wanted]
        if not folders:
            print(f"no bot folder named {wanted}")
            return 1
    failed = False
    for folder in folders:
        errors, notes = check_bot(folder)
        if errors is None:
            print(f"SKIP  {folder.name}: {notes[0]}")
            continue
        status = "FAIL" if errors else "PASS"
        failed = failed or bool(errors)
        print(f"{status}  {folder.name}")
        for n in notes:
            print(f"      note: {n}")
        for e in errors:
            print(f"      - {e}")
    if not wanted:
        shared_errors = check_shared()
        print(f"{'FAIL' if shared_errors else 'PASS'}  shared skills")
        for e in shared_errors:
            print(f"      - {e}")
        failed = failed or bool(shared_errors)
        name_errors = check_names(folders)
        print(f"{'FAIL' if name_errors else 'PASS'}  unique skill names")
        for e in name_errors:
            print(f"      - {e}")
        failed = failed or bool(name_errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
