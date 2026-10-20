"""Record frontier-VLM generations once (work package IP1); every condition is then replayed offline.

Same record layout as src/generation_dump.py, so src/replay.py consumes the output unchanged:
seeds x sheets x prompt keys {mv, ocr, ocrn, gt} x candidates 0..N-1, candidate 0 recorded once
(seed-independent), one API call per record. The run is resumable: records already in the output
file are skipped, so an interrupted run never pays twice. Provenance (backend, model id returned by
the provider, decoding settings actually applied, dates, library version) is merged into
results/replay/provenance.json. No API key is written anywhere.

Usage:
    python -m src.generation_dump_api --backend anthropic \
        --data benchmark/real --out results/replay/generations_anthropic.jsonl
    python -m src.generation_dump_api --backend openai --model <gpt-5-class-id> \
        --data benchmark/equipment --out results/replay_equipment/generations_openai.jsonl
    python -m src.generation_dump_api --backend anthropic --dry-run      # cost estimate, no calls
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.backends import get_backend, instruction_text
from src.prompt import build_prompt


def _call_seed(seed: int, part_id: str, key: str, idx: int) -> int:
    h = hashlib.sha256(f"{seed}|{part_id}|{key}|{idx}".encode()).hexdigest()
    return int(h[:8], 16)


def plan(items, ocr_dims, seeds, n):
    """Yield (seed, pid, image_path, key, dims, instruction, idx) for every record to collect."""
    from src import dimensions as dim_mod
    for seed in seeds:
        for rec in items:
            pid = rec["id"]
            prompts = {"mv": ([], build_prompt(dim_hint="", multiview=True))}
            if ocr_dims.get(pid):
                d = ocr_dims[pid]
                prompts["ocr"] = (d, build_prompt(dim_mod.build_dimension_hint(d), multiview=True))
            dn = ocr_dims.get(pid + "#naive") or []
            if dn and dn != (ocr_dims.get(pid) or []):
                prompts["ocrn"] = (dn, build_prompt(dim_mod.build_dimension_hint(dn), multiview=True))
            if rec.get("annotated_dims"):
                d = list(rec["annotated_dims"])
                prompts["gt"] = (d, build_prompt(dim_mod.build_dimension_hint(d), multiview=True))
            for key, (dims, prompt) in prompts.items():
                for idx in range(n):
                    if idx == 0 and seed != seeds[0]:
                        continue  # candidate 0 is recorded once, as in src/generation_dump.py
                    yield seed, pid, rec["image_mv"], key, dims, instruction_text(prompt), idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", required=True, choices=["anthropic", "openai", "gemini"])
    ap.add_argument("--model", default=None, help="provider model id (default for anthropic: claude-opus-5-5)")
    ap.add_argument("--data", default="benchmark/real")
    ap.add_argument("--manifest", default="manifest.jsonl")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--effort", default="low", help="anthropic output_config.effort / openai reasoning_effort")
    ap.add_argument("--out", required=True)
    ap.add_argument("--provenance", default="results/replay/provenance.json")
    ap.add_argument("--dry-run", action="store_true", help="count the calls that would be made and exit")
    a = ap.parse_args()

    data, out = Path(a.data), Path(a.out)
    items = [json.loads(l) for l in (data / a.manifest).read_text(encoding="utf-8").splitlines() if l.strip()]
    seeds = [int(s) for s in a.seeds.split(",")]
    out.parent.mkdir(parents=True, exist_ok=True)

    ocr_path = out.with_name("ocr_dims.json")
    if ocr_path.exists():
        ocr_dims = json.loads(ocr_path.read_text(encoding="utf-8"))
    else:  # deterministic, CPU only; identical to src/generation_dump.py
        from PIL import Image
        from src import dimensions as dim_mod
        ocr_dims = {}
        for rec in items:
            img = Image.open(data / rec["image_mv"]).convert("RGB")
            ocr_dims[rec["id"]] = dim_mod.extract_dimensions(img)
            ocr_dims[rec["id"] + "#naive"] = dim_mod.extract_dimensions(img, min_max=0.0)
        ocr_path.write_text(json.dumps(ocr_dims, indent=2), encoding="utf-8")

    done = set()
    if out.exists():
        for l in out.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                done.add((r["seed"], r["id"], r["key"], r["idx"]))
    todo = [p for p in plan(items, ocr_dims, seeds, a.n) if (p[0], p[1], p[3], p[6]) not in done]
    print(f"{len(done)} recorded, {len(todo)} calls to make ({a.backend}, {len(items)} sheets)", flush=True)
    if a.dry_run or not todo:
        return

    kw = {"max_tokens": a.max_tokens}
    if a.backend == "anthropic":
        kw["effort"] = a.effort
    elif a.backend == "openai":
        kw["reasoning_effort"] = a.effort
    be = get_backend(a.backend, a.model, **kw)
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    models_seen = set()
    with out.open("a", encoding="utf-8") as fh:
        for seed, pid, image, key, dims, instruction, idx in todo:
            cs = _call_seed(seed, pid, key, idx)
            t0 = time.time()
            g = be.generate((data / image).read_bytes(), instruction, idx, cs)
            models_seen.add(g.model)
            r = {"seed": seed, "id": pid, "key": key, "idx": idx, "dims": dims, "backend": a.backend,
                 "model": g.model, "settings": g.settings, "call_seed": cs if idx else None,
                 "usage": g.usage, "stop_reason": g.stop_reason, "request_id": g.request_id,
                 "gen_s": round(time.time() - t0, 1), "text": g.text}
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"seed{seed} {pid} {key} c{idx} {g.stop_reason} {g.usage.get('output_tokens')} tok", flush=True)

    prov_path = Path(a.provenance)
    prov = json.loads(prov_path.read_text(encoding="utf-8")) if prov_path.exists() else {}
    import importlib.metadata as md
    lib = {"anthropic": "anthropic", "openai": "openai", "gemini": "google-genai"}[a.backend]
    try:
        lib_version = md.version(lib)
    except md.PackageNotFoundError:
        lib_version = None
    prov[f"{a.backend}|{out.as_posix()}"] = {
        "backend": a.backend, "requested_model": a.model or getattr(be, "model", None),
        "provider_models_returned": sorted(models_seen), "generations_file": out.as_posix(),
        "data": data.as_posix(), "seeds": seeds, "n_candidates": a.n, "max_tokens": a.max_tokens,
        "effort": a.effort, "decoding_note": sys.modules[type(be).__module__].__doc__.strip().splitlines()[0],
        "run_started_utc": started, "run_finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(), "sdk": {lib: lib_version}}
    prov_path.parent.mkdir(parents=True, exist_ok=True)
    prov_path.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print("provenance ->", prov_path)


if __name__ == "__main__":
    main()
