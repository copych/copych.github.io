"""Validate prepared, upstream-verified firmware sites for static hosting."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys

root = Path(__file__).resolve().parents[1]
output = root / (sys.argv[1] if len(sys.argv) > 1 else "_site")
if output.resolve() != root / "_site":
    raise SystemExit("Output must be the hosting repository's _site directory")
if output.exists():
    raise SystemExit("Output exists; use a fresh checkout to avoid stale published files")
sites = sorted(root.glob("*/build-info.json"))
if not sites:
    raise SystemExit("No generated installer sites found; publishing raw source is not enough")
for manifest_path in sites:
    site = manifest_path.parent
    data = json.loads(manifest_path.read_text())
    assert data["channel"] == "attested development", "Only verified upstream builds may be hosted"
    assert data["sourceRepository"] == "copych/FM1-Ear-Trainer"
    assert data["sourceBranch"] == site.name
    assert re.fullmatch(r"[a-f0-9]{40}", data["sourceRevision"])
    assert data["sourceDirty"] is False
    assert data["product"] == "FM-1_327008"
    assert re.fullmatch(r"https://github.com/copych/FM1-Ear-Trainer/actions/runs/[0-9]+", data["workflowRun"])
    assert {"firmware/ear-trainer-dev.fwsc", "firmware/ear-trainer-dev-res.bin", "emu/melodee.wasm"} <= data["files"].keys()
    for name, expected in data["files"].items():
        path = (site / name).resolve()
        assert path.is_relative_to(site.resolve()), "Manifest path escapes its site"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
    for name in ("webapp/installer/index.html", "webapp/editor/index.html", "webapp/manual/index.html",
                 "emu/index.html", "firmware/ear-trainer-recovery-sources.zip"):
        assert (site / name).is_file(), name
    for path in site.rglob("*"):
        assert not path.is_symlink(), "Published sites must not contain symbolic links"
output.mkdir()
shutil.copyfile(root / "index.html", output / "index.html")
(output / ".nojekyll").touch()
for manifest_path in sites:
    shutil.copytree(manifest_path.parent, output / manifest_path.parent.name)
print("Prepared branch sites verified and assembled:", ", ".join(p.parent.name for p in sites))
