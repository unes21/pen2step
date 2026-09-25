"""Token-level OCR precision and recall on the dimensioned real sheets.

A read value counts as correct when it equals an annotated dimension within
0.5 mm; each annotated dimension can be matched once. Reported for the naive
reader (no plausibility floor) and for the reader with the floor. On the
undimensioned sheets every read value is a false positive; their count is
reported separately.

Usage:
    python -m src.ocr_eval --data benchmark/real --out results/ocr_eval.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

from src import dimensions as dim_mod


def match(read, gold, tol=0.5):
    gold = list(gold)
    tp = 0
    for v in read:
        hit = next((g for g in gold if abs(g - v) <= tol), None)
        if hit is not None:
            tp += 1
            gold.remove(hit)
    return tp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="benchmark/real")
    ap.add_argument("--out", default="results/ocr_eval.json")
    args = ap.parse_args()
    data = Path(args.data)
    items = [json.loads(l) for l in (data / "manifest.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    rows, agg = [], {}
    for rec in items:
        img = Image.open(data / rec["image_mv"]).convert("RGB")
        gold = list(rec.get("annotated_dims") or [])
        for variant, kw in [("naive", {"min_max": 0.0}), ("floor", {})]:
            read = dim_mod.extract_dimensions(img, **kw)
            tp = match(read, gold)
            rows.append({"id": rec["id"], "has_dims": bool(gold), "variant": variant,
                         "read": read, "gold": gold, "tp": tp})
            a = agg.setdefault((variant, bool(gold)), {"read": 0, "gold": 0, "tp": 0, "sheets_with_reads": 0})
            a["read"] += len(read); a["gold"] += len(gold); a["tp"] += tp
            a["sheets_with_reads"] += bool(read)
            print(rec["id"], variant, "gold", gold, "read", read, "tp", tp, flush=True)
    summary = {}
    for (variant, has), a in agg.items():
        key = f"{variant}_{'D' if has else 'U'}"
        summary[key] = dict(a, precision=(a["tp"] / a["read"]) if a["read"] else None,
                            recall=(a["tp"] / a["gold"]) if a["gold"] else None)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps({"summary": summary, "rows": rows}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
