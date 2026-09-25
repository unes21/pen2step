"""Trivial baselines scored with exactly the replay scorer (src/replay.score_pair).

constant_box : a fixed 100 x 50 x 30 mm box for every sheet (no image information)
gt_bbox      : a box with the ground truth's own bounding-box extents (correct scale,
               no shape information beyond extents)

Usage: python -m src.trivial_replay --gt results/replay --out results/replay/trivial.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cadquery as cq
import numpy as np

from src import metrics
from src.replay import score_pair


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", default="results/replay")
    ap.add_argument("--out", default="results/replay/trivial.json")
    a = ap.parse_args()
    root = Path(a.gt)
    work = root / "trivial"
    work.mkdir(parents=True, exist_ok=True)
    const = work / "constant_box.step"
    cq.exporters.export(cq.Workplane("XY").box(100, 50, 30), str(const))
    res = {}
    for tag in ("orig", "rescaled"):
        rows = {"constant_box": {}, "gt_bbox": {}}
        for gt in sorted((root / f"gt_{tag}").glob("*.step")):
            pid = gt.stem
            bb = metrics.load_shape(str(gt)).BoundingBox()
            p = work / f"bbox_{tag}_{pid}.step"
            cq.exporters.export(cq.Workplane("XY").box(bb.xlen, bb.ylen, bb.zlen), str(p))
            rows["constant_box"][pid] = score_pair((str(const), str(gt)))
            rows["gt_bbox"][pid] = score_pair((str(p), str(gt)))
        summ = {}
        for name, r in rows.items():
            summ[name] = {k: float(np.mean([v[k] for v in r.values() if v.get(k) is not None]))
                          for k in ("F_raw", "F_al", "F_al_sn", "CD_al", "DimE", "VolE")}
            summ[name]["SVR"] = float(np.mean([bool(v.get("valid")) for v in r.values()]))
            summ[name]["per_part_F_al"] = {pid: v.get("F_al") for pid, v in r.items()}
        res[tag] = summ
        for name, s in summ.items():
            print(tag, name, {k: round(v, 3) for k, v in s.items() if k != "per_part_F_al"})
    Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
