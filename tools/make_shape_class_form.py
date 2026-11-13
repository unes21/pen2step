"""Blind second rating of the coarse shape class (Sections 5.5 and 6.4).

Pairs every ground-truth render with the predicted solid that the paper judges (development set: full shell
N = 3, no dimensions, seed 0; case study: the same without dimensions and with sketch dimensions), shuffles
the pairs with a fixed seed and hides part and condition behind a pair code. The rater fills in the CSV form;
the key stays with the authors.

    python tools/make_shape_class_form.py --out results/shape_class_rating
"""
import argparse
import csv
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent.parent
CLASSES = "flat plate | prismatic block | solid cylinder | hollow ring or tube | bolt with a distinct head | other"

ap = argparse.ArgumentParser()
ap.add_argument("--out", default=str(ROOT / "results/shape_class_rating"))
ap.add_argument("--seed", type=int, default=2026)
a = ap.parse_args()
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)
dev = ROOT / "results/replay/renders"
case = ROOT / "results/replay_case/renders"
pairs = [(f"real_{i:02d}", "development, no dimensions", dev / f"real_{i:02d}_gt.png", dev / f"real_{i:02d}_pred.png")
         for i in range(1, 20)]
for pid in ("cs_01", "cs_02", "cs_03", "cs_05", "cs_07", "cs_13", "cs_18", "cs_19"):
    pairs.append((pid, "case study, no dimensions", case / f"{pid}_gt.png", case / f"{pid}_multiview_n3.png"))
    pairs.append((pid, "case study, sketch dimensions", case / f"{pid}_gt.png", case / f"{pid}_full_gt.png"))
for p in pairs:
    assert p[2].exists() and p[3].exists(), p
random.Random(a.seed).shuffle(pairs)
codes = [f"P{i + 1:02d}" for i in range(len(pairs))]

with PdfPages(out / "shape_class_form.pdf") as pdf:
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.08, 0.92, "Coarse shape class: blind rating form", fontsize=16, weight="bold")
    fig.text(0.08, 0.86, "\n".join([
        f"{len(pairs)} pairs. Left: ground truth. Right: predicted solid. Both are isometric line drawings",
        "with hidden edges in grey; size is not comparable (each drawing is scaled to fit).",
        "",
        "For every pair write in shape_class_form.csv:",
        "  gt_class and pred_class, one of:",
        f"    {CLASSES}",
        "  match = yes if the two classes are the same, otherwise no.",
        "",
        "Judge the kind of shape only (plate, block, cylinder, ring, bolt), not dimensions, holes or details.",
        "Do not consult the paper, the sketches or another rater before finishing.",
    ]), fontsize=10, va="top", family="monospace")
    pdf.savefig(fig)
    plt.close(fig)
    per_page = 4
    for k in range(0, len(pairs), per_page):
        fig, axes = plt.subplots(per_page, 2, figsize=(8.27, 11.69))
        for r in range(per_page):
            for c in range(2):
                axes[r][c].axis("off")
            if k + r >= len(pairs):
                continue
            _, _, g, p = pairs[k + r]
            axes[r][0].imshow(mpimg.imread(g))
            axes[r][1].imshow(mpimg.imread(p))
            axes[r][0].set_title(f"{codes[k + r]}  ground truth", fontsize=10, loc="left")
            axes[r][1].set_title(f"{codes[k + r]}  prediction", fontsize=10, loc="left")
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

with (out / "shape_class_form.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["pair", "gt_class", "pred_class", "match", "comment"])
    for c in codes:
        w.writerow([c, "", "", "", ""])
with (out / "shape_class_key.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["pair", "part", "condition"])
    for c, (pid, cond, _, _) in zip(codes, pairs):
        w.writerow([c, pid, cond])
print(f"{len(pairs)} pairs -> {out}")
