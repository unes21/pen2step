"""Graphical abstract (JCDE: at least 1250 x 500 px). Every number is read from results/replay/stats.json\nand results/replay/trivial.json; nothing is typed by hand.\n\nThe ground-truth and predicted renders are taken from results/replay/renders/ when present; otherwise they\nare rendered here from the released files (prediction: results/replay/gallery_steps/<pid>.step, ground\ntruth: the CadQuery code in benchmark/real/manifest.jsonl), so the script runs in a clean checkout.\n\nUsage: python tools/make_graphical_abstract.py --pid real_03\nOutputs: figures/graphical_abstract.png and figures/graphical_abstract.tiff (RGB, no alpha, 300 dpi)\n"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, FancyBboxPatch
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

INK, GREY, BLUE, ORANGE = "#1a1a1a", "#555555", "#2878d6", "#e8663d"


def photo(pid):
    """Grayscale input sheet with the illumination gradient divided out and the strokes darkened."""
    im = ImageOps.grayscale(Image.open(ROOT / f"benchmark/real/images/{pid}_mv.jpg"))
    bg = np.asarray(im.filter(ImageFilter.GaussianBlur(radius=150)), float) + 1
    flat = Image.fromarray(np.clip(np.asarray(im, float) / bg * 230, 0, 255).astype("uint8"))
    flat = ImageOps.autocontrast(flat, cutoff=(0.5, 2))
    flat = flat.point(lambda v: 255 if v > 190 else int(255 * (v / 255) ** 2.6))
    flat = flat.filter(ImageFilter.MinFilter(3))                       # thicken strokes for small display
    return crop_content(flat, pad=25, thr=60)


def crop_content(im, pad=10, thr=200):
    """Crop a white-background grayscale image to its dark content."""
    mask = im.filter(ImageFilter.MedianFilter(7)).point(lambda v: 255 if v > thr else 0)
    box = ImageOps.invert(mask).getbbox()
    if not box:
        return im
    l, t, r, b = box
    return im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))


def solid(path):
    """Render of a solid, cropped and with thicker lines."""
    im = ImageOps.grayscale(Image.open(path).convert("RGB"))
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.MinFilter(5))
    return crop_content(im, pad=12, thr=230)


def render_png(pid, which, renders):
    """Path to a render of the ground truth ('gt') or the selected prediction ('pred')."""
    p = Path(renders) / f"{pid}_{which}.png"
    if p.exists():
        return p
    from make_gallery import render  # needs CadQuery, svglib and reportlab
    import cadquery as cq
    tmp = Path(tempfile.mkdtemp())
    if which == "pred":
        step = ROOT / f"results/replay/gallery_steps/{pid}.step"
    else:
        man = {json.loads(l)["id"]: json.loads(l) for l in
               (ROOT / "benchmark/real/manifest.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
        ns = {}
        exec(man[pid]["code"], ns)
        step = tmp / f"{pid}_gt.step"
        cq.exporters.export(ns["result"], str(step))
    out = tmp / f"{pid}_{which}.png"
    render(step, out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", default=str(ROOT / "results/replay/stats.json"))
    ap.add_argument("--trivial", default=str(ROOT / "results/replay/trivial.json"))
    ap.add_argument("--pid", default="real_03")
    ap.add_argument("--renders", default=str(ROOT / "results/replay/renders"))
    ap.add_argument("--out", default=str(ROOT / "figures/graphical_abstract.png"))
    a = ap.parse_args()
    S = json.loads(Path(a.stats).read_text(encoding="utf-8"))
    C = S["orig"]["conditions"]
    n = S["n_parts"]
    n_seeds = len(S["seeds"])
    bare_valid = round(C["raw_mv_bare"]["SVR_mean"] * n)
    shell_valid = round(C["multiview_n3"]["SVR_mean"] * n)
    shell_f = C["multiview_n3"]["F_al_all"]
    box_f = json.loads(Path(a.trivial).read_text(encoding="utf-8"))["orig"]["constant_box"]["F_al"]

    fig = plt.figure(figsize=(13, 4.3), dpi=300)
    fig.patch.set_facecolor("white")

    def box(x, y, w, h, fc):
        fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.015",
                                          transform=fig.transFigure, fc=fc, ec="#bbbbbb", lw=1.2))

    def arrow(x):
        fig.add_artist(FancyArrow(x, 0.47, 0.016, 0, width=0.026, head_width=0.07, head_length=0.011,
                                  length_includes_head=True, transform=fig.transFigure, color=GREY))

    # 1. input photograph
    fig.text(0.108, 0.88, "Photo of a\nhand-drawn sheet", ha="center", va="center", fontsize=19,
             weight="bold", color=INK, linespacing=1.1)
    ax = fig.add_axes([0.008, 0.06, 0.2, 0.68])
    ax.imshow(photo(a.pid), cmap="gray", vmin=0, vmax=255)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#bbbbbb")
    arrow(0.212)

    # 2. deterministic shell
    box(0.233, 0.05, 0.283, 0.9, "#f5f5f3")
    fig.text(0.3745, 0.85, "Deterministic shell,\nno additional training", ha="center", va="center",
             fontsize=18, weight="bold", color=INK, linespacing=1.1)
    steps = ["OCR + multi-view canvas", "off-the-shelf CadQuery VLM", "AST repair + runtime guards",
             "sandboxed execution +\nscale recovery → STEP"]
    for i, st in enumerate(steps):
        fig.text(0.243, 0.635 - i * 0.16, f"{i + 1}  {st}", fontsize=16, va="center", color=INK,
                 linespacing=1.05)
    arrow(0.521)

    # 3. STEP output: ground truth and prediction
    for j, (which, cap, col) in enumerate([("pred", "Pen2STEP\noutput\n(valid STEP)", BLUE),
                                            ("gt", "ground\ntruth", GREY)]):
        x0 = 0.543 + j * 0.115
        axr = fig.add_axes([x0, 0.30, 0.105, 0.55])
        axr.imshow(solid(render_png(a.pid, which, a.renders)), cmap="gray", vmin=0, vmax=255)
        axr.axis("off")
        fig.text(x0 + 0.0525, 0.17, cap, ha="center", va="center", fontsize=15, color=col, linespacing=1.05,
                 weight="bold" if which == "pred" else "normal")

    # 4. findings
    box(0.776, 0.05, 0.216, 0.9, "#eef3fa")
    fig.text(0.884, 0.85, f"{n} real sheets,\n{n_seeds} seeds", ha="center", va="center", fontsize=18,
             weight="bold", color=INK, linespacing=1.1)
    fig.text(0.787, 0.68, "Valid STEP solids", fontsize=16, weight="bold", color=INK, va="center")
    fig.text(0.787, 0.585, f"bare model  {bare_valid}/{n}", fontsize=18, color=INK, va="center")
    fig.text(0.787, 0.495, f"with shell  {shell_valid}/{n}", fontsize=18, color=BLUE, va="center",
             weight="bold")
    fig.text(0.787, 0.37, "Aligned F-score", fontsize=16, weight="bold", color=INK, va="center")
    fig.text(0.787, 0.275, f"with shell  {shell_f:.2f}", fontsize=18, color=INK, va="center")
    fig.text(0.787, 0.185, f"constant box  {box_f:.2f}", fontsize=18, color=ORANGE, va="center")
    fig.text(0.884, 0.09, "executable, not yet\nthe right shape", ha="center", va="center", fontsize=14,
             style="italic", color=GREY, linespacing=1.05)

    out = Path(a.out)
    fig.savefig(out, dpi=300, facecolor="white")
    plt.close(fig)
    im = Image.open(out).convert("RGB")
    im.save(out)
    im.save(out.with_suffix(".tiff"), compression="tiff_lzw", dpi=(300, 300))
    print(out, im.size, im.mode)


if __name__ == "__main__":
    main()
