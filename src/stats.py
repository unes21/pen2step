"""Every number, interval and p-value reported for the real split, from one script.

Input: results/replay/replay_rows.json (src/replay.py) and, for the constant-box
comparison, results/replay/trivial.json (src/trivial_replay.py).

Conventions, applied uniformly:
  * all 19 parts enter every mean and every paired test; a part without a valid,
    scoreable solid contributes F = 0 (valid-only means are reported alongside);
  * a condition's value per part is its mean over the seeds;
  * SVR: mean +- SD over seeds; Wilson 95% interval on the pooled count;
  * validity: exact McNemar test on each seed (p reported per seed);
  * F: exact Wilcoxon signed-rank test on the 19 per-part seed means, zero
    differences dropped (n_pairs = parts with a non-zero difference);
  * 95% bootstrap interval (10,000 resamples of parts) for mean F.

Usage:
    python -m src.stats --rows results/replay/replay_rows.json --out results/replay/stats.json
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import binomtest, wilcoxon

METRICS = ("F_raw", "F_al", "F_al_sn", "CD_al", "DimE", "VolE")


def wilson(k, n, z=1.959964):
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (c - h, c + h)


def boot(v, B=10000, seed=0):
    v = np.asarray(v, float)
    rng = np.random.default_rng(seed)
    m = v[rng.integers(0, len(v), (B, len(v)))].mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def table(rows, gt="orig", volsel=False):
    """per condition -> per part -> per seed -> dict(valid, metrics)."""
    T = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        if r["volsel"] != volsel:
            continue
        s = r[f"score_{gt}"]
        ok = bool(s.get("valid")) and "F_al" in s
        T[r["condition"]][r["id"]][r["seed"]] = {"valid": bool(s.get("valid")), "scored": ok,
                                                 **{m: s.get(m) for m in METRICS}}
    return T


def summarize(T, cond, seeds, parts):
    per_seed_svr = [np.mean([T[cond][p][s]["valid"] for p in parts]) for s in seeds]
    k = sum(T[cond][p][s]["valid"] for p in parts for s in seeds)
    out = {"SVR_mean": float(np.mean(per_seed_svr)), "SVR_sd": float(np.std(per_seed_svr, ddof=1)) if len(seeds) > 1 else 0.0,
           "SVR_per_seed": [float(x) for x in per_seed_svr], "n_valid_per_seed": [int(round(x * len(parts))) for x in per_seed_svr],
           "SVR_wilson_pooled": wilson(k, len(parts) * len(seeds))}
    for m in METRICS:
        allp, validp = [], []
        for p in parts:
            vals = [T[cond][p][s][m] for s in seeds]
            if m.startswith("F"):
                allp.append(np.mean([v if v is not None else 0.0 for v in vals]))
            good = [v for v in vals if v is not None]
            if good:
                validp.append(np.mean(good))
        if m.startswith("F"):
            out[f"{m}_all"] = float(np.mean(allp))
            out[f"{m}_all_ci"] = boot(allp)
            out[f"{m}_all_seed_sd"] = float(np.std([np.mean([T[cond][p][s][m] or 0.0 for p in parts]) for s in seeds], ddof=1)) if len(seeds) > 1 else 0.0
        out[f"{m}_valid"] = float(np.mean(validp)) if validp else None
        out[f"{m}_n_valid_parts"] = len(validp)
    return out


def paired(T, a, b, seeds, parts):
    mc = []
    for s in seeds:
        va = [T[a][p][s]["valid"] for p in parts]
        vb = [T[b][p][s]["valid"] for p in parts]
        b01 = sum((not x) and y for x, y in zip(va, vb))
        b10 = sum(x and (not y) for x, y in zip(va, vb))
        p = binomtest(min(b01, b10), b01 + b10, 0.5).pvalue if b01 + b10 else 1.0
        mc.append({"seed": s, "a_only": b10, "b_only": b01, "p": float(p)})
    fa = np.array([np.mean([T[a][p][s]["F_al"] or 0.0 for s in seeds]) for p in parts])
    fb = np.array([np.mean([T[b][p][s]["F_al"] or 0.0 for s in seeds]) for p in parts])
    d = fb - fa
    nz = int((np.abs(d) > 1e-12).sum())
    pw = float(wilcoxon(fa, fb, zero_method="wilcox", method="exact").pvalue) if nz else 1.0
    return {"mcnemar_per_seed": mc, "wilcoxon_F_al_p": pw, "n_pairs": nz,
            "mean_diff_F_al": float(d.mean()), "diff_ci": boot(d)}


PAIRS = [("raw_mv_bare", "raw_mv"), ("raw_mv_bare", "multiview_n1"), ("raw_mv", "multiview_n1"),
         ("multiview_n1", "multiview_n3"), ("multiview_n3", "full_ocr"), ("multiview_n3", "full_gt"),
         ("full_ocr", "full_gt"), ("full_ocr_naive", "full_ocr")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default="results/replay/replay_rows.json")
    ap.add_argument("--out", default="results/replay/stats.json")
    ap.add_argument("--trivial", default="results/replay/trivial.json",
                    help="src/trivial_replay.py output; adds paired tests against the constant box")
    args = ap.parse_args()
    D = json.loads(Path(args.rows).read_text(encoding="utf-8"))
    rows, seeds = D["rows"], D["seeds"]
    parts = sorted({r["id"] for r in rows})
    res = {"seeds": seeds, "n_parts": len(parts),
           "ceiling_F": {g: float(np.mean([D["ceiling"][p][g] for p in parts])) for g in ("orig", "rescaled")},
           "ceiling_F_min": {g: float(min(D["ceiling"][p][g] for p in parts)) for g in ("orig", "rescaled")}}
    for gt in ("orig", "rescaled"):
        for volsel in (False, True):
            T = table(rows, gt, volsel)
            key = f"{gt}{'_volsel' if volsel else ''}"
            res[key] = {"conditions": {c: summarize(T, c, seeds, parts) for c in T},
                        "paired": {f"{a}|{b}": paired(T, a, b, seeds, parts) for a, b in PAIRS if a in T and b in T}}
    # mechanism firing counts on the selected candidate and on all candidates, seed 0 view for single-candidate rows
    fire = defaultdict(lambda: defaultdict(int))
    for r in rows:
        if r["volsel"]:
            continue
        c = r["condition"]
        for k, v in r["fired"].items():
            fire[c][f"{k}_any_candidate"] += int(any(v))
            fire[c][f"{k}_candidates"] += int(sum(v))
        fire[c]["candidates"] += len(r["fired"]["arc"])
        for rep_list in r["repairs"]:
            for op in rep_list:
                fire[c][f"repair_{op}"] += 1
        fire[c]["part_seed_rows"] += 1
    res["firing"] = {c: dict(v) for c, v in fire.items()}
    # input-agnostic baseline: constant box against the shell configurations (same convention)
    tv = Path(args.trivial)
    if tv.exists():
        box = json.loads(tv.read_text(encoding="utf-8"))
        for gt in ("orig", "rescaled"):
            if gt not in box:
                continue
            fb = np.array([box[gt]["constant_box"]["per_part_F_al"][p] for p in parts])
            T = table(rows, gt, False)
            vs = {}
            for c in ("multiview_n1", "multiview_n3", "full_ocr", "full_gt"):
                fa = np.array([np.mean([T[c][p][s]["F_al"] or 0.0 for s in seeds]) for p in parts])
                d = fb - fa
                nz = int((np.abs(d) > 1e-12).sum())
                vs[c] = {"mean_diff_box_minus_cond": float(d.mean()), "diff_ci": boot(d), "n_pairs": nz,
                         "wilcoxon_F_al_p": float(wilcoxon(fa, fb, zero_method="wilcox", method="exact").pvalue) if nz else 1.0,
                         "parts_cond_above_box": int((fa > fb).sum())}
            res[gt]["vs_constant_box"] = vs
    Path(args.out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    o = res["orig"]["conditions"]
    for c, s in o.items():
        print(f"{c:24s} SVR {s['SVR_mean']:.3f}+-{s['SVR_sd']:.3f}  F_al(all) {s['F_al_all']:.3f}  F_raw(all) {s['F_raw_all']:.3f}  F_al_sn {s['F_al_sn_all']:.3f}")
    for k, v in res["orig"]["paired"].items():
        print(k, [m["p"] for m in v["mcnemar_per_seed"]], "wilcoxon", round(v["wilcoxon_F_al_p"], 4), "n", v["n_pairs"])


if __name__ == "__main__":
    main()
