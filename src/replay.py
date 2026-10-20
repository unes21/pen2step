"""Offline replay of the executed shell on recorded backbone outputs.

Reads the JSONL written by src/generation_dump.py and re-executes every
candidate under an explicit set of shell mechanisms, so that each mechanism
can be switched on or off without another GPU run. Every mechanism that the
evaluation harness applies is listed here and nowhere else:

    extract   take the text after "ASSISTANT:" and strip a Markdown code fence
              (always on; without it no condition can execute at all)
    repair    AST repair operators: parse_fix, add_import, ensure_result
    arc       safe header: a failing threePointArc falls back to a straight line
    partial   partial-execution salvage: the program body runs inside
              try/except and objects built before the failure are kept
    discover  result discovery over nine variable names instead of `result`
    base      base-plate removal: among solid0, solid1, ... drop thin solids
              whose footprint is among the largest, fuse and re-centre the rest
    scale     scale recovery: rescale outputs with longest edge < 10 mm to the
              largest dimension read (or 100 mm when none is read)
    volsel    positive-volume check at selection (historical runs: off; the
              check was applied only at evaluation)

Selection among valid candidates: first valid candidate when no dimensions are
injected; otherwise the candidate minimising the summed relative error between
its largest sorted extents and the largest sorted injected dimensions.

Scoring: validity (openable, valid, positive volume), and Chamfer / F@tau under
three conventions: raw (mean-centred), aligned (best of the 24 axis rotations),
and aligned + scale-normalised (prediction rescaled to the ground-truth bounding-
box diagonal before alignment). Every part is also scored against the rescaled
ground truth (benchmark/real/manifest_rescaled.jsonl). The per-part self-ceiling
(ground truth against itself with independent surface samples) is recorded.

Usage:
    python -m src.replay --dump dump.jsonl --data benchmark/real --out results/replay
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from src import metrics
from src.code_repair import repair, split_after_assistant, strip_markdown

ALL = ("repair", "arc", "partial", "discover", "base", "scale")
CANDS = ["result", "solid", "shape", "part", "body", "model", "compound", "obj", "cad_result"]

ARC_HEADER = (
    "import cadquery as cq\n"
    "_o_tpa = cq.Workplane.threePointArc\n"
    "def _safe_tpa(self, p1, p2, forConstruction=False):\n"
    "    try:\n"
    "        return _o_tpa(self, p1, p2, forConstruction)\n"
    "    except Exception:\n"
    "        print('ARC_FALLBACK')\n"
    "        return self.lineTo(p2[0], p2[1], forConstruction)\n"
    "cq.Workplane.threePointArc = _safe_tpa\n"
)

BASE_BLOCK = '''
import re as _re
_ss = []
for _n in sorted([k for k in list(globals()) if _re.match(r'solid\\d+$', k)], key=lambda s: int(s[5:])):
    try:
        _o = globals()[_n]
        _sv = _o.val() if hasattr(_o, "val") else _o
        _bb0 = _sv.BoundingBox()
        _e = sorted([_bb0.xlen, _bb0.ylen, _bb0.zlen])
        _ss.append((_n, _sv, _e[0], _e[1] * _e[2]))
    except Exception:
        pass
if len(_ss) >= 2:
    _mth = max(s[2] for s in _ss)
    _mft = max(s[3] for s in _ss)
    _bases = [s for s in _ss if s[2] < 0.35 * _mth and s[3] > 0.6 * _mft]
    _keep = [s for s in _ss if s not in _bases]
    if _bases and _keep:
        _r = _keep[0][1]
        for _k in _keep[1:]:
            try:
                _r = _r.fuse(_k[1])
            except Exception:
                pass
        try:
            _c = _r.BoundingBox().center
            _r = _r.translate((-_c.x, -_c.y, -_c.z))
        except Exception:
            pass
        globals()['result'] = _r
        print("BASE_REMOVED " + ",".join(b[0] for b in _bases))
'''


def build_program(code: str, flags: frozenset, step_path: str, target_max) -> str:
    parts = [ARC_HEADER if "arc" in flags else ""]
    if "partial" in flags:
        parts.append("try:\n" + "\n".join("    " + ln for ln in code.splitlines())
                     + "\nexcept Exception as _e:\n    print('PARTIAL_EXEC', repr(_e))\n")
    else:
        parts.append(code + "\n")
    parts.append("import cadquery as cq\n")
    if "base" in flags:
        parts.append(BASE_BLOCK)
    names = CANDS if "discover" in flags else ["result"]
    parts.append(
        f"_final = None\nfor _nm in {names!r}:\n"
        "    if _nm in globals():\n        _final = globals()[_nm]\n"
        "        if _nm != 'result': print('RESULT_FROM ' + _nm)\n        break\n"
        "if _final is None:\n    raise NameError('no result object')\n"
        "_shp = _final.val() if hasattr(_final, 'val') else _final\n"
        "_bb = _shp.BoundingBox()\n_maxd = max(_bb.xlen, _bb.ylen, _bb.zlen)\n")
    if "scale" in flags:
        goal = 100.0 if target_max is None else float(target_max)
        parts.append(f"if _maxd < 10.0 and _maxd > 1e-9:\n    _shp = _shp.scale({goal!r} / _maxd)\n"
                     "    print('SCALED')\n")
    parts.append("_b2 = _shp.BoundingBox()\n"
                 "print('BBOX %.6f %.6f %.6f' % (_b2.xlen, _b2.ylen, _b2.zlen))\n"
                 f"cq.exporters.export(_shp, r'{step_path}')\n")
    return "".join(parts)


def prepare_code(text: str, flags: frozenset):
    if "repair" in flags:
        return repair(text)
    return strip_markdown(split_after_assistant(text)) + "\n", []


def run_candidate(args):
    """Execute one candidate program; cached by content hash."""
    text, flags, target_max, cache_dir, timeout = args
    flags = frozenset(flags)
    code, applied = prepare_code(text, flags)
    key = hashlib.sha256(json.dumps([code, sorted(flags), target_max]).encode()).hexdigest()[:24]
    meta_path = Path(cache_dir) / f"{key}.json"
    step_path = str(Path(cache_dir) / f"{key}.step")
    if meta_path.exists():
        return json.loads(meta_path.read_text())
    prog = build_program(code, flags, step_path, target_max)
    py = Path(cache_dir) / f"{key}.py"
    py.write_text(prog, encoding="utf-8")
    try:
        p = subprocess.run([sys.executable, str(py)], capture_output=True, text=True, timeout=timeout)
        out, err, rc = p.stdout or "", p.stderr or "", p.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "timeout", -1
    ok = rc == 0 and os.path.exists(step_path)
    bbox = None
    for ln in out.splitlines():
        if ln.startswith("BBOX"):
            bbox = [float(v) for v in ln.split()[1:4]]
    vol_ok = ok and metrics.step_is_valid(step_path)
    meta = {"ok": ok, "vol_ok": vol_ok, "bbox": bbox, "step": step_path if ok else None,
            "repairs": applied,
            "arc": out.count("ARC_FALLBACK") > 0, "partial": "PARTIAL_EXEC" in out,
            "discover": "RESULT_FROM" in out, "base": "BASE_REMOVED" in out,
            "scaled": "SCALED" in out, "error": None if ok else (err or out)[-300:]}
    meta_path.write_text(json.dumps(meta))
    return meta


def select(cands, dims, volsel):
    pool = [c for c in cands if (c["vol_ok"] if volsel else c["ok"])]
    if not pool:
        return None
    if not dims:
        return pool[0]
    tgt = sorted(dims)

    def score(c):
        b = sorted(c["bbox"]) if c["bbox"] else [0.0, 0.0, 0.0]
        n = min(len(b), len(tgt))
        return sum(abs(bi - ti) / max(ti, 1e-6) for bi, ti in zip(b[-n:], tgt[-n:]))
    return min(pool, key=score)


def score_pair(args):
    pred_step, gt_step = args
    out = {"valid": False}
    if pred_step is None or not metrics.step_is_valid(pred_step):
        return out
    pred, gt = metrics.load_shape(pred_step), metrics.load_shape(gt_step)
    try:
        pp = metrics._center(metrics.sample_surface(pred, 4000, seed=1))
        gp = metrics._center(metrics.sample_surface(gt, 4000, seed=2))
        if len(pp) == 0 or len(gp) == 0:
            out.update(valid=True, error="empty surface sample")
            return out
        diag = float(np.linalg.norm(metrics.bbox_dims(gt)))
        tau = 0.02 * max(diag, 1e-6)
        pa, _, _ = metrics.align_best_of_24(pp, gp)
        pdiag = float(np.linalg.norm(pp.max(0) - pp.min(0)))
        ps = pp * (diag / max(pdiag, 1e-9))
        psa, _, _ = metrics.align_best_of_24(ps, gp)
        out.update(valid=True,
                   F_raw=metrics.fscore(pp, gp, tau), CD_raw=metrics.chamfer_distance(pp, gp),
                   F_al=metrics.fscore(pa, gp, tau), CD_al=metrics.chamfer_distance(pa, gp),
                   F_al_sn=metrics.fscore(psa, gp, tau),
                   DimE=metrics.dimension_error(pred, gt), VolE=metrics.volume_error(pred, gt))
    except Exception as exc:
        out.update(valid=True, error=str(exc))
    return out


def self_ceiling(gt_step):
    gt = metrics.load_shape(gt_step)
    a = metrics._center(metrics.sample_surface(gt, 4000, seed=1))
    b = metrics._center(metrics.sample_surface(gt, 4000, seed=2))
    diag = float(np.linalg.norm(metrics.bbox_dims(gt)))
    return metrics.fscore(a, b, 0.02 * diag)


# Conditions: (prompt source, dimension source, N, mechanisms)
SHELL = frozenset(ALL)
CONDITIONS = {
    "raw_mv_bare":   ("mv", None, 1, frozenset()),
    "raw_mv":        ("mv", None, 1, frozenset({"arc", "partial", "discover", "base"})),
    "multiview_n1":  ("mv", None, 1, SHELL),
    "multiview_n3":  ("mv", None, 3, SHELL),
    "full_ocr":      ("ocr", "ocr", 3, SHELL),
    "full_ocr_naive": ("ocrn", "ocrn", 3, SHELL),
    "full_gt":       ("gt", "gt", 3, SHELL),
    # leave-one-mechanism-out from the single-candidate shell
    "n1_minus_repair":   ("mv", None, 1, SHELL - {"repair"}),
    "n1_minus_arc":      ("mv", None, 1, SHELL - {"arc"}),
    "n1_minus_partial":  ("mv", None, 1, SHELL - {"partial"}),
    "n1_minus_discover": ("mv", None, 1, SHELL - {"discover"}),
    "n1_minus_base":     ("mv", None, 1, SHELL - {"base"}),
    "n1_minus_scale":    ("mv", None, 1, SHELL - {"scale"}),
    # add-one-mechanism from bare
    "bare_plus_repair":  ("mv", None, 1, frozenset({"repair"})),
    "bare_plus_scale":   ("mv", None, 1, frozenset({"scale"})),
    "bare_plus_repair_scale": ("mv", None, 1, frozenset({"repair", "scale"})),
    "bare_plus_partial": ("mv", None, 1, frozenset({"partial"})),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", required=True)
    ap.add_argument("--data", default="benchmark/real")
    ap.add_argument("--out", default="results/replay")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--timeout", type=int, default=60)
    args = ap.parse_args()

    data, out = Path(args.data), Path(args.out)
    cache = out / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    recs = [json.loads(l) for l in Path(args.dump).read_text(encoding="utf-8").splitlines() if l.strip()]
    seeds = sorted({r["seed"] for r in recs})
    greedy = {(r["id"], r["key"]): r for r in recs if r["idx"] == 0}
    sampled = {(r["seed"], r["id"], r["key"], r["idx"]): r for r in recs if r["idx"] > 0}

    def texts(seed, pid, key, n):
        if (pid, key) not in greedy:
            key = "mv"
        g = greedy[(pid, key)]
        seq = [g] + [sampled[(seed, pid, key, i)] for i in range(1, n) if (seed, pid, key, i) in sampled]
        return key, g["dims"], [r["text"] for r in seq]

    gt_dirs = {}
    for tag, man in [("orig", "manifest.jsonl"), ("rescaled", "manifest_rescaled.jsonl")]:
        if not (data / man).exists():
            man = "manifest.jsonl"  # splits without undimensioned parts (equipment) have no rescaled variant
        d = out / f"gt_{tag}"
        d.mkdir(exist_ok=True)
        for l in (data / man).read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            m = json.loads(l)
            p = d / f"{m['id']}.step"
            if not p.exists():
                import cadquery as cq
                ns = {}
                exec(m["code"], ns)
                cq.exporters.export(ns["result"], str(p))
            gt_dirs.setdefault(m["id"], {})[tag] = str(p)
    items = json.loads(json.dumps([json.loads(l) for l in (data / "manifest.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip()]))

    jobs, index = [], []
    for seed in seeds:
        for cname, (pkey, dkey, n, flags) in CONDITIONS.items():
            for rec in items:
                pid = rec["id"]
                key, dims, tx = texts(seed, pid, pkey, n)
                dims = dims if (dkey and key == pkey) else []
                tmax = max(dims) if dims else None
                for ci, t in enumerate(tx[:n]):
                    jobs.append((t, sorted(flags), tmax, str(cache), args.timeout))
                    index.append((seed, cname, pid, ci, dims))
    print(f"{len(jobs)} candidate executions ({len(set(map(repr, jobs)))} distinct)", flush=True)
    with ProcessPoolExecutor(args.workers) as ex:
        metas = list(ex.map(run_candidate, jobs, chunksize=4))

    grouped = {}
    for (seed, cname, pid, ci, dims), m in zip(index, metas):
        grouped.setdefault((seed, cname, pid), {"dims": dims, "cands": []})["cands"].append(m)

    sel_rows, score_jobs = [], []
    for (seed, cname, pid), g in grouped.items():
        for volsel in (False, True):
            best = select(g["cands"], g["dims"], volsel)
            row = {"seed": seed, "condition": cname, "id": pid, "volsel": volsel,
                   "n_ok": sum(c["ok"] for c in g["cands"]),
                   "n_vol_ok": sum(c["vol_ok"] for c in g["cands"]),
                   "fired": {k: [bool(c.get(k)) for c in g["cands"]] for k in
                             ("arc", "partial", "discover", "base", "scaled")},
                   "repairs": [c["repairs"] for c in g["cands"]],
                   "selected_step": best["step"] if best else None}
            sel_rows.append(row)
            for tag in ("orig", "rescaled"):
                score_jobs.append((best["step"] if best else None, gt_dirs[pid][tag]))
    with ProcessPoolExecutor(args.workers) as ex:
        scores = list(ex.map(score_pair, score_jobs, chunksize=4))
    for i, row in enumerate(sel_rows):
        row["score_orig"], row["score_rescaled"] = scores[2 * i], scores[2 * i + 1]

    ceilings = {pid: {tag: self_ceiling(p) for tag, p in d.items()} for pid, d in gt_dirs.items()}
    (out / "replay_rows.json").write_text(json.dumps({"rows": sel_rows, "ceiling": ceilings,
                                                      "seeds": seeds}, indent=1), encoding="utf-8")
    print("written", out / "replay_rows.json")


if __name__ == "__main__":
    main()
