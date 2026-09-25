"""Graphical abstract (JCDE: at least 1250 x 500 px). Numbers are read from results/replay/stats.json.

Usage: python tools/make_graphical_abstract.py --pid real_10 --out figures/graphical_abstract.png
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", default=str(ROOT / "results/replay/stats.json"))
    ap.add_argument("--pid", default="real_10")
    ap.add_argument("--renders", default=str(ROOT / "results/replay/renders"))
    ap.add_argument("--out", default=str(ROOT / "figures/graphical_abstract.png"))
    a = ap.parse_args()
    S = json.loads(Path(a.stats).read_text(encoding="utf-8"))["orig"]["conditions"]
    bare, shell3 = S["raw_mv_bare"], S["multiview_n3"]
    box_f = json.loads((ROOT / "results/replay/trivial.json").read_text(encoding="utf-8"))["orig"]["constant_box"]["F_al"]

    fig = plt.figure(figsize=(13, 5.2), dpi=120)
    fig.patch.set_facecolor("white")

    def box(x, y, w, h, fc):
        fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.015",
                                          transform=fig.transFigure, fc=fc, ec="#bbbbbb", lw=1))

    ax = fig.add_axes([0.02, 0.18, 0.25, 0.66]); ax.axis("off")
    ax.imshow(mpimg.imread(ROOT / f"benchmark/real/images/{a.pid}_mv.jpg"))
    fig.text(0.145, 0.88, "Phone photo of a hand-drawn\nthree-view sheet", ha="center", va="bottom", fontsize=12, weight="bold")

    box(0.30, 0.14, 0.33, 0.72, "#f5f5f3")
    fig.text(0.465, 0.80, "Deterministic shell, no additional training", ha="center", fontsize=12.5, weight="bold")
    steps = ["multi-view canvas + OCR dimension clause",
             "off-the-shelf image-to-CadQuery VLM, N = 3",
             "AST repair + runtime guards",
             "sandboxed execution, selection, scale recovery",
             "CadQuery program + STEP solid"]
    for i, s in enumerate(steps):
        fig.text(0.32, 0.70 - i * 0.11, f"{i + 1}.  {s}", fontsize=11.5, va="center")
    fig.add_artist(matplotlib.patches.FancyArrow(0.274, 0.5, 0.012, 0, head_length=0.008, width=0.01, transform=fig.transFigure, color="#555"))
    fig.add_artist(matplotlib.patches.FancyArrow(0.637, 0.5, 0.012, 0, head_length=0.008, width=0.01, transform=fig.transFigure, color="#555"))

    box(0.665, 0.14, 0.32, 0.72, "#eef3fa")
    fig.text(0.825, 0.80, "19 real sheets, 3 seeds", ha="center", fontsize=12.5, weight="bold")
    n = 19
    fig.text(0.685, 0.66, f"Valid STEP solids", fontsize=11.5, weight="bold")
    fig.text(0.685, 0.58, f"bare model   {round(bare['SVR_mean'] * n)} / {n}", fontsize=12)
    fig.text(0.685, 0.51, f"with shell    {round(shell3['SVR_mean'] * n)} / {n}", fontsize=12)
    fig.text(0.685, 0.38, "Shape fidelity (aligned F-score)", fontsize=11.5, weight="bold")
    fig.text(0.685, 0.30, f"with shell    {shell3['F_al_all']:.2f}", fontsize=12)
    fig.text(0.685, 0.24, f"constant box  {box_f:.2f}   (ignores the input)", fontsize=12)
    fig.text(0.685, 0.155, "Validity is solved by the shell;\nshape recovery is not.", fontsize=11, style="italic")
    fig.savefig(a.out, dpi=120, facecolor="white")
    print(a.out)


if __name__ == "__main__":
    main()
