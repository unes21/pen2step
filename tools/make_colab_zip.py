"""Build a minimal upload bundle for running the new baseline / equal-N
conditions (raw_mv, multiview_n3) on Google Colab Pro.

Contents (kept small so it uploads in seconds):
    src/                       all framework + harness code
    data/real_eval/            19 real three-view sheets + manifest  (~4.4 MB)
    data/manifest.jsonl        synthetic manifest
    data/images/test/*_mv.png  ONLY the first 50 test multi-view images (~10 MB)

Output: pen2step_eval.zip  (next to this script)

Run:  python make_colab_zip.py
"""
from __future__ import annotations
import json
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "pen2step_eval.zip"
SYN_LIMIT = 50  # must match the --limit used for the synthetic equal-N run


def main():
    files: list[tuple[Path, str]] = []  # (absolute path, arcname)

    # 1) source code
    for p in (ROOT / "src").glob("*.py"):
        files.append((p, f"src/{p.name}"))

    # 2) real eval set (manifest + all images)
    re_dir = ROOT / "data" / "real_eval"
    files.append((re_dir / "manifest.jsonl", "data/real_eval/manifest.jsonl"))
    for p in (re_dir / "images").iterdir():
        if p.is_file():
            files.append((p, f"data/real_eval/images/{p.name}"))

    # 3) synthetic manifest + first SYN_LIMIT test multi-view images
    syn_manifest = ROOT / "data" / "manifest.jsonl"
    files.append((syn_manifest, "data/manifest.jsonl"))
    rows = [json.loads(l) for l in syn_manifest.read_text(encoding="utf-8").splitlines() if l.strip()]
    test = [r for r in rows if r.get("split") == "test"][:SYN_LIMIT]
    missing = 0
    for r in test:
        rel = r["image_mv"]                    # e.g. images/test/000007_mv.png
        src = ROOT / "data" / rel
        if src.exists():
            files.append((src, f"data/{rel}"))
        else:
            missing += 1

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc in files:
            z.write(src, arc)

    mb = OUT.stat().st_size / 1e6
    print(f"wrote {OUT.name}  ({mb:.1f} MB, {len(files)} files)")
    if missing:
        print(f"WARNING: {missing} synthetic test images not found; "
              f"synthetic equal-N run may skip those samples.")


if __name__ == "__main__":
    main()
