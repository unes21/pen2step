# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image
import os

# Figures are written next to this script (the repository figures/ folder).
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- pipeline schematic
# Simplified schematic of the shell (fig_pipeline.png). Figure 1 of the paper is the
# detailed diagram figures/fig_pipeline_v2.png, which this script does not generate.
fig, ax = plt.subplots(figsize=(9.2, 3.1))
ax.set_xlim(0, 16)
ax.set_ylim(0, 5)
ax.axis("off")

bw, bh = 2.7, 1.25
centers = {
    "I":  (1.8, 3.4), "C": (5.4, 3.4), "O": (9.0, 3.4), "V": (12.6, 3.4),
    "R":  (12.6, 1.1), "E": (9.0, 1.1), "S": (5.4, 1.1), "Out": (1.8, 1.1),
}
labels = {
    "I": "Multi-view\nsketches", "C": "Multi-view\ncomposition",
    "O": "Dimension\nOCR + inject", "V": "Backbone VLM\n(N candidates)",
    "R": "AST repair +\nruntime guards", "E": "Execute (60 s)\n& select",
    "S": "Scale\nrecovery", "Out": "STEP /\nB-rep solid",
}
io_nodes = {"I", "Out"}

# surrounding border
border = FancyBboxPatch((0.4, 0.2), 15.2, 4.6,
                        boxstyle="round,pad=0.02,rounding_size=0.18",
                        linewidth=1.0, edgecolor="0.45", facecolor="white")
ax.add_patch(border)

for k, (cx, cy) in centers.items():
    face = "0.84" if k in io_nodes else "0.965"
    edge = "0.15" if k in io_nodes else "0.45"
    lw = 1.3 if k in io_nodes else 0.9
    box = FancyBboxPatch((cx - bw / 2, cy - bh / 2), bw, bh,
                         boxstyle="round,pad=0.02,rounding_size=0.12",
                         linewidth=lw, edgecolor=edge, facecolor=face)
    ax.add_patch(box)
    ax.text(cx, cy, labels[k], ha="center", va="center",
            fontsize=10.5, fontweight=("bold" if k in io_nodes else "normal"),
            color="black", linespacing=1.15)

def arrow(a, b):
    ax1, ay1 = centers[a]; bx1, by1 = centers[b]
    # compute edge points
    if ay1 == by1:  # horizontal
        if bx1 > ax1:
            start = (ax1 + bw / 2, ay1); end = (bx1 - bw / 2, by1)
        else:
            start = (ax1 - bw / 2, ay1); end = (bx1 + bw / 2, by1)
    else:  # vertical
        start = (ax1, ay1 - bh / 2); end = (bx1, by1 + bh / 2)
    p = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                        linewidth=1.1, color="0.2", shrinkA=0, shrinkB=0)
    ax.add_patch(p)

for a, b in [("I", "C"), ("C", "O"), ("O", "V"), ("V", "R"),
             ("R", "E"), ("E", "S"), ("S", "Out")]:
    arrow(a, b)

plt.tight_layout(pad=0.2)
fig.savefig(os.path.join(OUT, "fig_pipeline.png"), dpi=220,
            bbox_inches="tight", facecolor="white")
plt.close(fig)

# ---------------------------------------------------------------- Equation
fig2 = plt.figure(figsize=(7.2, 1.15))
fig2.text(0.5, 0.5,
          r"$\mathrm{F}=\dfrac{2\,\mathrm{Pre}\cdot\mathrm{Rec}}"
          r"{\mathrm{Pre}+\mathrm{Rec}}, \qquad "
          r"\mathrm{Pre}=\mathbb{E}_{p\in P}[\,d(p,G)<\tau\,], \qquad "
          r"\mathrm{Rec}=\mathbb{E}_{q\in G}[\,d(q,P)<\tau\,]$",
          ha="center", va="center", fontsize=15, color="black")
fig2.savefig(os.path.join(OUT, "fig_eq_fscore.png"), dpi=220,
             bbox_inches="tight", facecolor="white")
plt.close(fig2)

# ---------------------------------------------------------------- report sizes
for name in ["fig_pipeline.png", "fig_eq_fscore.png"]:
    im = Image.open(os.path.join(OUT, name)); print(name, im.size)

ts = os.path.join(OUT, "fig_real_testset.png")
im = Image.open(ts); print("fig_real_testset.png", im.size, "ratio=%.4f" % (im.size[1] / im.size[0]))
print("done")
