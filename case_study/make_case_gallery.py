"""Case-study figure: sketch photograph, ground truth and selected prediction (seed 0) for each part.

Usage: python case_study/make_case_gallery.py --condition full_gt
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from make_gallery import render as _render  # noqa: E402
import cadquery as cq  # noqa: E402


def render(step, png):
    """Render after scaling to a common size so that line weights match across parts (display only)."""
    shape = cq.importers.importStep(str(step)).val()
    bb = shape.BoundingBox()
    tmp = Path(png).with_suffix(".norm.step")
    cq.exporters.export(cq.Workplane("XY").add(shape.scale(200.0 / max(bb.xlen, bb.ylen, bb.zlen))), str(tmp))
    _render(tmp, png)


def crop(path):
    im = ImageOps.grayscale(Image.open(path).convert("RGB"))
    box = ImageOps.invert(im.point(lambda v: 255 if v > 200 else 0)).getbbox()
    return im.crop(box) if box else im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default=str(ROOT / "results/replay_case/replay_rows.json"))
    ap.add_argument("--conditions", default="multiview_n3,full_gt")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=str(ROOT / "figures/case_study_gallery.png"))
    a = ap.parse_args()
    conds = a.conditions.split(",")
    rows = json.loads(Path(a.rows).read_text(encoding="utf-8"))["rows"]
    man = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "benchmark/case_study/manifest.jsonl")
           .read_text(encoding="utf-8").splitlines() if l.strip()}
    rd = ROOT / "results/replay_case/renders"
    rd.mkdir(parents=True, exist_ok=True)
    ids = sorted(man)
    labels = {"multiview_n3": "Pen2STEP,\nno dimensions", "full_gt": "Pen2STEP,\nsketch dimensions"}
    ncol = 2 + len(conds)
    fig, ax = plt.subplots(len(ids), ncol, figsize=(2.3 * ncol, 1.55 * len(ids)), dpi=200)
    for i, pid in enumerate(ids):
        gt = rd / f"{pid}_gt.png"
        render(ROOT / f"results/replay_case/gt_orig/{pid}.step", gt)
        panels = [(crop(ROOT / "benchmark/case_study" / man[pid]["image_mv"]), "sketch"), (crop(gt), "ground truth")]
        for c in conds:
            sel = [r for r in rows if r["id"] == pid and r["condition"] == c and r["seed"] == a.seed and not r["volsel"]][0]
            p = rd / f"{pid}_{c}.png"
            if sel["selected_step"]:
                render(ROOT / sel["selected_step"], p)
                panels.append((crop(p), labels.get(c, c)))
            else:
                panels.append((None, labels.get(c, c)))
        for j, (im, title) in enumerate(panels):
            axx = ax[i, j]
            if im is not None:
                axx.imshow(im, cmap="gray", vmin=0, vmax=255)
            else:
                axx.text(0.5, 0.5, "no solid", ha="center", va="center", fontsize=7)
            if i == 0:
                axx.set_title(title, fontsize=7)
            axx.axis("off")
        ax[i, 0].text(-0.08, 0.5, pid, transform=ax[i, 0].transAxes, ha="right", va="center", fontsize=7)
    plt.tight_layout(pad=0.4)
    plt.savefig(a.out, facecolor="white")
    print(a.out)


if __name__ == "__main__":
    main()
