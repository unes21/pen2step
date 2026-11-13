"""Score the official CAD-Coder outputs (results/official_cadcoder) with the repository's replay scorer.

Every number of Tables 2-4 and A1 of the benchmark paper comes from this script. Conditions:

    official     program + export of `solid` (CAD-Coder criterion: runs and writes the file)
    strict       the same STEP file also opens as a valid positive-volume shape (src.metrics.step_is_valid)
    rescale100   export of `solid`, longest edge rescaled to 100 mm (flags discover + scale)
    shell        full shell of src/replay.py, canonical 100 mm
    shell_typed  full shell, longest edge rescaled to the largest dimension written on the sheet
    result_only  the earlier configuration's export step (variable `result` only, no shell)
    shell_minus_<m>  leave-one-mechanism-out of the full shell

Usage: python tools/score_official.py --out results/official_cadcoder/score
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.stats import binomtest, fisher_exact, wilcoxon

from src import metrics
from src.replay import SHELL, run_candidate, score_pair, self_ceiling
from src.stats import boot, wilson

OFF = ROOT / "results/official_cadcoder/inference_results"
SPLITS = {"real": ROOT / "benchmark/real", "case_study": ROOT / "benchmark/case_study"}
COND_FLAGS = {
    "rescale100": frozenset({"discover", "scale"}),
    "shell": SHELL,
    "shell_typed": SHELL,
    "result_only": frozenset(),
    "shell_minus_repair": SHELL - {"repair"},
    "shell_minus_partial": SHELL - {"partial"},
    "shell_minus_base": SHELL - {"base"},
}


def run_official(args):
    """CAD-Coder criterion (scripts/generate_model_cad.py): the program runs, and the program followed by exports
    of `solid` to STL and STEP runs and writes the STL. Strict: the STEP also opens as a positive-volume solid."""
    pid, code, work, timeout = args
    work = Path(work)
    if "```python" in code:
        code = re.sub(r"```[a-zA-Z]*\n|```", "", code)
    out = {"id": pid}
    stl, step = work / f"{pid}.stl", work / f"{pid}.step"
    for f in (stl, step):
        if f.exists():
            f.unlink()
    exp = (f"\nimport cadquery as cq\ncq.exporters.export(solid, r'{stl}')\n"
           f"\nimport cadquery as cq\ncq.exporters.export(solid, r'{step}')\n")
    for tag, body in (("runs", code), ("official", code + exp)):
        py = work / f"{pid}_{tag}.py"
        py.write_text(body, encoding="utf-8")
        try:
            p = subprocess.run([sys.executable, str(py)], capture_output=True, text=True, timeout=timeout)
            ok, err = p.returncode == 0, (p.stderr or "")[-300:]
        except subprocess.TimeoutExpired:
            ok, err = False, "timeout"
        out[tag] = ok
        out[tag + "_error"] = None if ok else err
    out["step_written"] = step.exists()
    out["official"] = out["official"] and stl.exists()
    out["strict"] = out["official"] and step.exists() and metrics.step_is_valid(str(step))
    out["volume"] = None
    if step.exists():
        try:
            out["volume"] = float(metrics.load_shape(str(step)).Volume())
        except Exception:
            pass
    out["step"] = str(step) if out["official"] else None
    if out["strict"]:
        bb = metrics.bbox_dims(metrics.load_shape(str(step)))
        out["extents"] = sorted(float(x) for x in bb)
    return out


def n_solids(code):
    return len(set(re.findall(r"^\s*(solid\d+)\s*=", code, flags=re.M)))


def load_merge(split):
    return {json.loads(l)["question_id"]: json.loads(l)["text"]
            for l in (OFF / split / "merge.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "results/official_cadcoder/score"))
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()
    out = Path(a.out)
    (out / "official").mkdir(parents=True, exist_ok=True)
    (out / "cache").mkdir(exist_ok=True)
    (out / "gt").mkdir(exist_ok=True)

    import cadquery as cq
    man, gt = {}, {}
    for split, data in SPLITS.items():
        for l in (data / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
            if l.strip():
                m = json.loads(l)
                man[m["id"]] = m
                p = out / "gt" / f"{m['id']}.step"
                if not p.exists():
                    ns = {}
                    exec(m["code"], ns)
                    cq.exporters.export(ns["result"], str(p))
                gt[m["id"]] = str(p)
    const = out / "gt" / "_constant_box.step"
    cq.exporters.export(cq.Workplane("XY").box(100, 50, 30), str(const))

    texts = load_merge("pen2step_27")
    toks = {json.loads(l)["question_id"]: json.loads(l) for l in
            (OFF / "pen2step_27" / "tokens.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    sub = load_merge("cadquery_test_data_subset100")
    sub_toks = [json.loads(l)["output_tokens_retokenised"] for l in
                (OFF / "cadquery_test_data_subset100" / "tokens.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = sorted(texts, key=lambda i: (not i.startswith("real"), i))
    assert len(ids) == 27 and set(ids) == set(man)

    with ProcessPoolExecutor(a.workers) as ex:
        off = {r["id"]: r for r in ex.map(run_official, [(i, texts[i], str(out / "official"), a.timeout) for i in ids])}
        (out / "official_subset").mkdir(exist_ok=True)
        offsub = list(ex.map(run_official, [(str(k), v, str(out / "official_subset"), a.timeout) for k, v in sub.items()]))
        jobs, index = [], []
        for c, fl in COND_FLAGS.items():
            for i in ids:
                tmax = None
                if c == "shell_typed" and man[i].get("has_dims") and man[i].get("annotated_dims"):
                    tmax = float(max(man[i]["annotated_dims"]))
                jobs.append((texts[i], sorted(fl), tmax, str(out / "cache"), a.timeout))
                index.append((c, i))
        metas = list(ex.map(run_candidate, jobs, chunksize=2))
        cond = {}
        for (c, i), m in zip(index, metas):
            cond.setdefault(c, {})[i] = m
        pairs = [(off[i]["step"] if off[i]["strict"] else None, gt[i]) for i in ids]
        for c in ("rescale100", "shell", "shell_typed"):
            pairs += [(cond[c][i]["step"] if cond[c][i]["vol_ok"] else None, gt[i]) for i in ids]
        pairs += [(str(const), gt[i]) for i in ids]
        bbsteps = []
        for i in ids:
            bb = metrics.load_shape(gt[i]).BoundingBox()
            p = out / "gt" / f"_bbox_{i}.step"
            cq.exporters.export(cq.Workplane("XY").box(bb.xlen, bb.ylen, bb.zlen), str(p))
            bbsteps.append((str(p), gt[i]))
        pairs += bbsteps
        scores = list(ex.map(score_pair, pairs, chunksize=2))
        ceil = dict(zip(ids, ex.map(self_ceiling, [gt[i] for i in ids])))

    names = ["released", "rescale100", "shell", "shell_typed", "constant_box", "gt_bbox"]
    S = {n: dict(zip(ids, scores[k * 27:(k + 1) * 27])) for k, n in enumerate(names)}

    def F(n, i, key):
        s = S[n][i]
        return float(s.get(key) or 0.0) if s.get("valid") else 0.0

    res = {"environment": {"python": sys.version.split()[0], "cadquery": cq.__version__}, "per_sheet": {}, "sets": {}}
    for i in ids:
        t = texts[i]
        e = off[i].get("extents")
        g = sorted(float(x) for x in metrics.bbox_dims(metrics.load_shape(gt[i])))
        res["per_sheet"][i] = {
            "tokens": toks[i]["output_tokens_retokenised"], "reached_limit": toks[i]["reached_limit"],
            "solids": n_solids(t), "runs": off[i]["runs"], "official": off[i]["official"], "strict": off[i]["strict"],
            "runs_error": off[i]["runs_error"], "official_error": off[i]["official_error"],
            "F_sn_released": F("released", i, "F_al_sn") if off[i]["strict"] else None,
            "flat_ratio": (e[0] / e[2]) if e and e[2] > 0 else None, "gt_flat_ratio": g[0] / g[2],
            "valid": {c: bool(cond[c][i]["vol_ok"]) for c in COND_FLAGS},
            "shell_error": cond["shell"][i]["error"], "ceiling": ceil[i],
            "F": {n: {"F_al": F(n, i, "F_al"), "F_al_sn": F(n, i, "F_al_sn")} for n in names},
        }
    P = res["per_sheet"]

    def wil(x, y):
        x, y = np.array(x), np.array(y)
        nz = int(np.sum(x != y))
        return (float(wilcoxon(x, y, zero_method="wilcox", method="exact").pvalue) if nz else 1.0), nz

    for tag, sel in (("development", [i for i in ids if i.startswith("real")]), ("case_study", [i for i in ids if i.startswith("cs")]),
                     ("all", ids)):
        n = len(sel)
        d = {"n": n}
        for c in ("runs", "official", "strict"):
            k = sum(P[i][c] for i in sel)
            d[c] = k
            d[c + "_wilson"] = wilson(k, n)
        d["median_tokens"] = float(np.median([P[i]["tokens"] for i in sel]))
        d["reached_limit_within10"] = sum(P[i]["reached_limit"] for i in sel)
        d["cut_at_3450"] = sum(P[i]["tokens"] >= 3450 for i in sel)
        d["median_solids"] = float(np.median([P[i]["solids"] for i in sel]))
        d["solids_range"] = [min(P[i]["solids"] for i in sel), max(P[i]["solids"] for i in sel)]
        d["valid"] = {c: sum(P[i]["valid"][c] for i in sel) for c in COND_FLAGS}
        for nme in names:
            for key in ("F_al", "F_al_sn"):
                v = [P[i]["F"][nme][key] for i in sel]
                d[f"{nme}_{key}"] = float(np.mean(v))
                d[f"{nme}_{key}_ci"] = list(boot(np.array(v)))
        for nme in ("released", "rescale100", "shell", "shell_typed"):
            key = "F_al_sn" if nme == "released" else "F_al"
            for box in ("constant_box", "gt_bbox"):
                bkey = "F_al_sn" if nme == "released" else "F_al"
                x = [P[i]["F"][nme][key] for i in sel]
                y = [P[i]["F"][box][bkey] for i in sel]
                p, nz = wil(x, y)
                d[f"{nme}_vs_{box}"] = {"model_above": sum(a > b for a, b in zip(x, y)), "p": p, "n_nonzero": nz}
        for a_, b_, key in (("shell_typed", "shell", "F_al"), ("shell", "rescale100", "F_al_sn"), ("shell", "released", "F_al_sn")):
            p, nz = wil([P[i]["F"][a_][key] for i in sel], [P[i]["F"][b_][key] for i in sel])
            d[f"{a_}_vs_{b_}_{key}"] = {"p": p, "n_nonzero": nz}
        b01 = sum((not P[i]["strict"]) and P[i]["valid"]["shell"] for i in sel)
        b10 = sum(P[i]["strict"] and not P[i]["valid"]["shell"] for i in sel)
        d["mcnemar_shell_vs_strict"] = {"shell_only": b01, "strict_only": b10,
                                        "p": float(binomtest(min(b01, b10), b01 + b10, 0.5).pvalue) if b01 + b10 else 1.0}
        fl = [P[i]["flat_ratio"] for i in sel if P[i]["strict"]]
        d["flat_below_5pct"] = sum(r < 0.05 for r in fl)
        d["valid_strict_for_flat"] = len(fl)
        d["median_flat_ratio"] = float(np.median(fl)) if fl else None
        d["gt_flat_below_5pct"] = sum(P[i]["gt_flat_ratio"] < 0.05 for i in sel)
        d["median_gt_flat_ratio"] = float(np.median([P[i]["gt_flat_ratio"] for i in sel]))
        d["ceiling_mean"] = float(np.mean([P[i]["ceiling"] for i in sel]))
        res["sets"][tag] = d

    ks = {c: sum(r[c] for r in offsub) for c in ("runs", "official", "strict")}
    res["subset100"] = {"n": len(offsub), **ks, "median_tokens": float(np.median(sub_toks)),
                        "median_solids": float(np.median([n_solids(t) for t in sub.values()])),
                        "strict_failures": [r["id"] for r in offsub if not r["strict"]]}
    al = res["sets"]["all"]
    res["fisher_strict"] = float(fisher_exact([[al["strict"], 27 - al["strict"]], [ks["strict"], 100 - ks["strict"]]])[1])
    res["fisher_official"] = float(fisher_exact([[al["official"], 27 - al["official"]], [ks["official"], 100 - ks["official"]]])[1])
    (out / "scores.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "per_sheet"}, indent=1))


if __name__ == "__main__":
    main()
