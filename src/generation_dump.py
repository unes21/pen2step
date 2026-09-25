"""Record the raw backbone outputs once, so every shell configuration can be replayed offline.

The shell never feeds execution results back into generation, so the text a
candidate produces depends only on (image, prompt, candidate index, seed).
This script loads the backbone once and writes, for every real sheet and every
distinct prompt the evaluated conditions use, the raw decoded text of
candidates 0..N-1. Candidate 0 is greedy and seed-independent, so it is
generated once; candidates 1..N-1 are sampled with a per-call seed derived
from (seed, part id, prompt key, index) and are therefore reproducible.

Prompt keys:
    mv   no dimension clause (raw_mv, multiview, multiview_n3, and full_ocr /
         full_gt on sheets whose dimension set is empty)
    ocr  dimension clause from the OCR reader with the plausibility floor
    ocrn dimension clause from the naive OCR reader (no floor), only where it
         differs from the floored set (Table 4)
    gt   dimension clause from the annotated ground-truth dimensions

Output (append-only JSONL, resumable): one record per generation.

Usage (Colab, A100, bfloat16):
    python -m src.generation_dump --data benchmark/real --seeds 0,1,2 \
        --temperature 0.5 --out /content/drive/MyDrive/pen2step_dump/dump.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch
from PIL import Image
from transformers import AutoProcessor, LlavaNextForConditionalGeneration

from src import dimensions as dim_mod
from src.prompt import build_prompt

MODEL_ID = "StoryGold/bella-v1.0-13b"
MAX_NEW_TOKENS = 512
REPETITION_PENALTY = 1.1
TOP_P = 0.9


def _call_seed(seed: int, part_id: str, key: str, idx: int) -> int:
    h = hashlib.sha256(f"{seed}|{part_id}|{key}|{idx}".encode()).hexdigest()
    return int(h[:8], 16)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="benchmark/real")
    ap.add_argument("--manifest", default="manifest.jsonl")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=0.5)
    ap.add_argument("--model", default=MODEL_ID)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-gpu-gib", type=float, default=None,
                    help="cap GPU memory for weights (e.g. 18 on a 24 GB L4); the rest is offloaded to CPU")
    args = ap.parse_args()

    data = Path(args.data)
    items = [json.loads(l) for l in (data / args.manifest).read_text(encoding="utf-8").splitlines()
             if l.strip()]
    seeds = [int(s) for s in args.seeds.split(",")]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    done = set()
    if out.exists():
        for l in out.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                done.add((r["seed"], r["id"], r["key"], r["idx"]))
    print(f"resume: {len(done)} generations already recorded")

    # Dimension sets are computed once (OCR is deterministic and runs on the CPU).
    ocr_path = out.with_name("ocr_dims.json")
    if ocr_path.exists():
        ocr_dims = json.loads(ocr_path.read_text(encoding="utf-8"))
    else:
        ocr_dims = {}
        for rec in items:
            img = Image.open(data / rec["image_mv"]).convert("RGB")
            ocr_dims[rec["id"]] = dim_mod.extract_dimensions(img)
            ocr_dims[rec["id"] + "#naive"] = dim_mod.extract_dimensions(img, min_max=0.0)
            print("ocr", rec["id"], ocr_dims[rec["id"]], "naive", ocr_dims[rec["id"] + "#naive"])
        ocr_path.write_text(json.dumps(ocr_dims, indent=2), encoding="utf-8")

    import platform
    import transformers, accelerate
    env = {"python": platform.python_version(), "torch": torch.__version__,
           "transformers": transformers.__version__, "accelerate": accelerate.__version__,
           "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"}
    out.with_name("environment.json").write_text(json.dumps(env, indent=2), encoding="utf-8")
    print("environment:", env, flush=True)
    processor = AutoProcessor.from_pretrained(args.model)
    mm = {0: f"{args.max_gpu_gib}GiB", "cpu": "48GiB"} if args.max_gpu_gib else None
    model = LlavaNextForConditionalGeneration.from_pretrained(
        args.model, torch_dtype=torch.bfloat16, device_map="auto", max_memory=mm, low_cpu_mem_usage=True)
    print("device map:", sorted(set(map(str, getattr(model, "hf_device_map", {}).values()))), flush=True)
    model.eval()

    @torch.inference_mode()
    def generate(image, prompt, idx, call_seed):
        inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
        kw = dict(max_new_tokens=MAX_NEW_TOKENS, repetition_penalty=REPETITION_PENALTY,
                  pad_token_id=processor.tokenizer.eos_token_id)
        if idx == 0:
            kw["do_sample"] = False
        else:
            torch.manual_seed(call_seed)
            torch.cuda.manual_seed_all(call_seed)
            kw.update(do_sample=True, temperature=args.temperature, top_p=TOP_P)
        t0 = time.time()
        o = model.generate(**inputs, **kw)
        n_new = int(o.shape[1] - inputs["input_ids"].shape[1])
        return processor.decode(o[0], skip_special_tokens=True), n_new, round(time.time() - t0, 1)

    with out.open("a", encoding="utf-8") as fh:
        for seed in seeds:
            for rec in items:
                pid = rec["id"]
                img = Image.open(data / rec["image_mv"]).convert("RGB")
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
                    for idx in range(args.n):
                        if idx == 0 and seed != seeds[0]:
                            continue  # greedy: identical for every seed
                        if (seed, pid, key, idx) in done:
                            continue
                        cs = _call_seed(seed, pid, key, idx)
                        text, n_new, dt = generate(img, prompt, idx, cs)
                        r = {"seed": seed, "id": pid, "key": key, "idx": idx, "dims": dims,
                             "temperature": args.temperature if idx else None,
                             "call_seed": cs if idx else None, "new_tokens": n_new,
                             "truncated": n_new >= MAX_NEW_TOKENS, "gen_s": dt, "text": text}
                        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                        fh.flush()
                        print(f"seed{seed} {pid} {key} c{idx} {n_new} tok {dt}s", flush=True)
    print("DONE")


if __name__ == "__main__":
    main()
