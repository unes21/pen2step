"""Figure 5: ground truth and selected prediction for every real sheet (replay run).

Usage: python tools/make_gallery.py --condition multiview_n3 --seed 0
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cadquery as cq
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parent.parent


def render(step, png, size=360):
    shape = cq.importers.importStep(str(step))
    svg = str(png).replace(".png", ".svg")
    cq.exporters.export(shape, svg, exportType="SVG", opt={
        "width": size, "height": size, "marginLeft": 20, "marginTop": 20, "showAxes": False,
        "projectionDir": (1, 1, 1), "strokeWidth": 0.8, "strokeColor": (0, 0, 0),
        "hiddenColor": (150, 150, 150), "showHidden": True})
    renderPM.drawToFile(svg2rlg(svg), str(png), fmt="PNG", bg=0xFFFFFF)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default=str(ROOT / "results/replay/replay_rows.json"))
    ap.add_argument("--condition", default="multiview_n3")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=str(ROOT / "figures/prediction_gallery_replay.png"))
    a = ap.parse_args()
    D = json.loads(Path(a.rows).read_text(encoding="utf-8"))
    man = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "benchmark/real/manifest.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip()}
    sel = {r["id"]: r for r in D["rows"] if r["condition"] == a.condition and r["seed"] == a.seed and not r["volsel"]}
    rd = ROOT / "results/replay/renders"
    rd.mkdir(parents=True, exist_ok=True)
    keep = ROOT / "results/replay/gallery_steps"
    keep.mkdir(parents=True, exist_ok=True)
    ids = sorted(sel)
    for pid in ids:
        render(ROOT / f"results/replay/gt_orig/{pid}.step", rd / f"{pid}_gt.png")
        s = sel[pid]["selected_step"]
        if s:
            shutil.copy(s, keep / f"{pid}.step")
            render(s, rd / f"{pid}_pred.png")
    ncols, nrows = 4, 5
    fig, ax = plt.subplots(nrows, ncols * 2, figsize=(ncols * 2 * 1.3, nrows * 1.5))
    for k in range(nrows * ncols):
        r, c = divmod(k, ncols)
        g, p = ax[r, 2 * c], ax[r, 2 * c + 1]
        if k < len(ids):
            pid = ids[k]
            du = "D" if man[pid].get("annotated_dims") else "U"
            g.imshow(mpimg.imread(rd / f"{pid}_gt.png")); g.set_title(f"{pid} ({du})\nGT", fontsize=6)
            valid = sel[pid]["score_orig"].get("valid")
            if sel[pid]["selected_step"] and (rd / f"{pid}_pred.png").exists():
                p.imshow(mpimg.imread(rd / f"{pid}_pred.png"))
                p.set_title("Pred" if valid else "Pred (zero volume)", fontsize=6)
            else:
                p.text(0.5, 0.5, "no solid", ha="center", va="center", fontsize=7)
        g.axis("off"); p.axis("off")
    plt.tight_layout(pad=0.3)
    plt.savefig(a.out, dpi=200, bbox_inches="tight")
    print(a.out)


if __name__ == "__main__":
    main()
