"""Figure 6: validity and pose-aligned fidelity on the real split (replay run), with trivial baselines."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "results/replay/stats.json").read_text(encoding="utf-8"))
T = json.loads((ROOT / "results/replay/trivial.json").read_text(encoding="utf-8"))["orig"]
C = S["orig"]["conditions"]
ceil = S["ceiling_F"]["orig"]

rows = [("bare model  (N = 1)", C["raw_mv_bare"]["SVR_mean"], C["raw_mv_bare"]["F_al_all"]),
        ("runtime guards only  (N = 1)", C["raw_mv"]["SVR_mean"], C["raw_mv"]["F_al_all"]),
        ("full shell  (N = 1)", C["multiview_n1"]["SVR_mean"], C["multiview_n1"]["F_al_all"]),
        ("full shell  (N = 3)", C["multiview_n3"]["SVR_mean"], C["multiview_n3"]["F_al_all"]),
        ("+ OCR dimensions  (N = 3)", C["full_ocr"]["SVR_mean"], C["full_ocr"]["F_al_all"]),
        ("+ GT dimensions  (N = 3)", C["full_gt"]["SVR_mean"], C["full_gt"]["F_al_all"]),
        ("constant 100×50×30 box", T["constant_box"]["SVR"], T["constant_box"]["F_al"]),
        ("GT bounding box", T["gt_bbox"]["SVR"], T["gt_bbox"]["F_al"])]

BLUE, ORANGE, GREY = "#2878d6", "#e8663d", "#c8c8c2"
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=248)
ys = list(range(len(rows)))[::-1]
for y, (lab, svr, f) in zip(ys, rows):
    ax.plot([f, svr], [y, y], color=GREY, lw=3, zorder=1)
    ax.scatter([svr], [y], s=70, color=BLUE, zorder=3, edgecolor="white", linewidth=1)
    ax.scatter([f], [y], s=60, color=ORANGE, marker="D", zorder=3, edgecolor="white", linewidth=1)
    ax.text(f, y - 0.36, f"{f:.3f}", ha="center", va="center", fontsize=8.5, color="#444")
ax.axhspan(-0.6, 1.5, color="#f3f3ef", zorder=0)
ax.text(0.62, 1.33, "input-agnostic baselines", ha="center", va="center", fontsize=8.5, color="#666")
ax.axvline(ceil, color=ORANGE, ls="--", lw=1.6)
ax.text(ceil - 0.01, len(rows) - 0.35, f"measured F-score ceiling  {ceil:.2f}", ha="right", fontsize=9, color=ORANGE)
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=10)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.8, len(rows) - 0.1)
ax.set_xlabel("rate  /  score", fontsize=10.5)
ax.grid(axis="x", color="#c8c8c2", lw=0.8)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.scatter([], [], s=70, color=BLUE, label="STEP Validity Rate")
ax.scatter([], [], s=60, color=ORANGE, marker="D", label="F-score@τ, pose-aligned (all 19 parts)")
ax.legend(loc="upper center", bbox_to_anchor=(0.45, 1.12), ncol=2, frameon=False, fontsize=10)
plt.tight_layout()
out = ROOT / "figures/fig_validity_fidelity_replay.png"
plt.savefig(out, facecolor="white")
print(out)
