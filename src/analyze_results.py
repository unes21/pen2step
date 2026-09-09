"""Per-sample istatistiksel analiz (hakem yanıtı: deneysel titizlik + önem).

run_baselines.py'ın ürettiği ablation JSON'undaki 'raw' per-sample dizilerinden:
  - her koşul için bootstrap %95 güven aralığı (SVR, F, Chamfer, DimE, VolE)
  - aile (family) bazında SVR ve F dökümü
  - ölçülü (has_dims) vs ölçüsüz alt-küme F/SVR (önem: OCR'ın işe yaradığı yer)
  - iki koşul arası eşlemeli testler (validite için McNemar, F için Wilcoxon)

Sayı ÜRETMEZ; yalnızca gerçek per-sample sonuçları özetler.

Kullanım:
    python -m src.analyze_results --json data/real_eval/results/ablation_n19.json
    python -m src.analyze_results --json <dosya> --pairs multiview_n3:full_ocr,raw_mv:multiview_n3
"""
from __future__ import annotations

import json
import argparse
from pathlib import Path

import numpy as np

try:
    from scipy.stats import wilcoxon, binomtest
    _SCIPY = True
except Exception:
    _SCIPY = False


def _boot_ci(vals, B: int = 10000, seed: int = 0):
    vals = [v for v in vals if v is not None]
    if not vals:
        return (float("nan"), float("nan"), float("nan"), 0)
    arr = np.asarray(vals, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(B, len(arr)))
    means = arr[idx].mean(axis=1)
    return (float(arr.mean()),
            float(np.percentile(means, 2.5)),
            float(np.percentile(means, 97.5)),
            len(arr))


def per_condition(raw):
    svr = [1.0 if r.get("step_valid") else 0.0 for r in raw]
    f = [float(r.get("fscore", 0.0)) if r.get("step_valid") else 0.0 for r in raw]
    valid = [r for r in raw if r.get("step_valid")]
    cham = [r.get("chamfer_mm") for r in valid]
    dime = [r.get("dim_error") for r in valid]
    vole = [r.get("volume_error") for r in valid]
    return {
        "n": len(raw), "n_valid": len(valid),
        "SVR": _boot_ci(svr), "F": _boot_ci(f),
        "Chamfer": _boot_ci(cham), "DimE": _boot_ci(dime), "VolE": _boot_ci(vole),
    }


def by_group(raw, key):
    groups = {}
    for r in raw:
        groups.setdefault(r.get(key), []).append(r)
    out = {}
    for g, rows in sorted(groups.items(), key=lambda kv: str(kv[0])):
        svr = np.mean([1.0 if r.get("step_valid") else 0.0 for r in rows])
        f = np.mean([float(r.get("fscore", 0.0)) if r.get("step_valid") else 0.0 for r in rows])
        out[g] = {"n": len(rows), "SVR": float(svr), "F": float(f)}
    return out


def paired(a_raw, b_raw):
    """a,b aligned by id. McNemar on validity, Wilcoxon on F (valid-in-both)."""
    a = {r["id"]: r for r in a_raw}
    b = {r["id"]: r for r in b_raw}
    ids = [i for i in a if i in b]
    va = [bool(a[i].get("step_valid")) for i in ids]
    vb = [bool(b[i].get("step_valid")) for i in ids]
    b01 = sum(1 for x, y in zip(va, vb) if (not x) and y)   # a invalid, b valid
    b10 = sum(1 for x, y in zip(va, vb) if x and (not y))   # a valid, b invalid
    if _SCIPY and (b01 + b10) > 0:
        p_val = binomtest(min(b01, b10), b01 + b10, 0.5).pvalue
    else:
        p_val = float("nan")
    # Wilcoxon on F over samples valid in BOTH
    fa = [float(a[i].get("fscore", 0.0)) for i in ids if a[i].get("step_valid") and b[i].get("step_valid")]
    fb = [float(b[i].get("fscore", 0.0)) for i in ids if a[i].get("step_valid") and b[i].get("step_valid")]
    if _SCIPY and len(fa) >= 1 and any(x != y for x, y in zip(fa, fb)):
        try:
            p_f = float(wilcoxon(fa, fb).pvalue)
        except Exception:
            p_f = float("nan")
    else:
        p_f = float("nan")
    return {"n_pairs": len(ids), "val_b01": b01, "val_b10": b10,
            "mcnemar_p": p_val, "wilcoxon_F_p": p_f, "n_F_pairs": len(fa)}


def _fmt(ci):
    m, lo, hi, n = ci
    if n == 0:
        return "n/a"
    return f"{m:.3f} [{lo:.3f}, {hi:.3f}]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--pairs", default="",
                    help="virgülle ayrık A:B eşleştirmeleri, örn. multiview_n3:full_ocr")
    args = ap.parse_args()

    data = json.loads(Path(args.json).read_text(encoding="utf-8"))
    raw = data["raw"]
    conds = list(raw.keys())

    lines = [f"# Analiz: {Path(args.json).name}  (n={data.get('n','?')})", ""]
    lines.append("## Koşul başına bootstrap %95 GA")
    lines.append("| koşul | SVR [95% GA] | F [95% GA] | Chamfer(mm) [95% GA] | DimE [95% GA] | n_valid |")
    lines.append("|---|---|---|---|---|---|")
    for c in conds:
        s = per_condition(raw[c])
        lines.append(f"| {c} | {_fmt(s['SVR'])} | {_fmt(s['F'])} | {_fmt(s['Chamfer'])} "
                     f"| {_fmt(s['DimE'])} | {s['n_valid']}/{s['n']} |")

    lines.append("\n## Ölçülü (has_dims) vs ölçüsüz alt-küme")
    lines.append("| koşul | grup | n | SVR | F |")
    lines.append("|---|---|---|---|---|")
    for c in conds:
        g = by_group(raw[c], "has_dims")
        for k in sorted(g, key=lambda x: not x):  # True önce
            lab = "ölçülü" if k else "ölçüsüz"
            lines.append(f"| {c} | {lab} | {g[k]['n']} | {g[k]['SVR']:.3f} | {g[k]['F']:.3f} |")

    lines.append("\n## Aile bazında (SVR / F)")
    for c in conds:
        fam = by_group(raw[c], "family")
        lines.append(f"\n**{c}**")
        lines.append("| family | n | SVR | F |")
        lines.append("|---|---|---|---|")
        for g, v in fam.items():
            lines.append(f"| {g} | {v['n']} | {v['SVR']:.3f} | {v['F']:.3f} |")

    if args.pairs:
        lines.append("\n## Eşlemeli testler")
        lines.append("| A | B | McNemar p (validite) | Wilcoxon p (F) | b01/b10 |")
        lines.append("|---|---|---|---|---|")
        for pair in args.pairs.split(","):
            a, b = pair.split(":")
            if a in raw and b in raw:
                r = paired(raw[a], raw[b])
                lines.append(f"| {a} | {b} | {r['mcnemar_p']:.4g} | {r['wilcoxon_F_p']:.4g} "
                             f"| {r['val_b01']}/{r['val_b10']} |")

    if not _SCIPY:
        lines.append("\n> not: scipy yok, eşlemeli test p-değerleri hesaplanmadı.")

    out_md = Path(args.json).with_name(Path(args.json).stem + "_analysis.md")
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nKaydedildi → {out_md}")


if __name__ == "__main__":
    main()
