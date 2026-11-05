"""Token-budget control: greedy candidate of every sheet with max_new_tokens = 2048.

Only the budget differs from src/generation_dump.py: same pinned checkpoint, prompt without dimension
clause, greedy decoding and repetition penalty. Candidate 0 is seed-independent, so one generation per
sheet is recorded (19 development + 8 case-study sheets). The output has the dump record layout, so
src/replay.py consumes it unchanged. Resumable.

Usage (GPU, once):
    python -m src.token_budget_control --out results/token_control/dump_2048.jsonl
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import accelerate
import torch
import transformers
from PIL import Image
from transformers import AutoProcessor, LlavaNextForConditionalGeneration, StoppingCriteria, StoppingCriteriaList

from src.prompt import build_prompt

MODEL_ID = "StoryGold/bella-v1.0-13b"
REVISION = "af7c325f8e5743d605fe199290081d6ee8024951"
MAX_NEW_TOKENS = 2048
REPETITION_PENALTY = 1.1


class Progress(StoppingCriteria):
    """Never stops generation; reports the rate during long offloaded runs."""

    def __init__(self, every=100):
        self.every, self.n, self.t0 = every, 0, time.time()

    def __call__(self, input_ids, scores, **kwargs):
        self.n += 1
        if self.n % self.every == 0:
            print(f"  {self.n} tok, {(time.time() - self.t0) / self.n:.2f} s/tok", flush=True)
        return torch.zeros(input_ids.shape[0], dtype=torch.bool, device=input_ids.device)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", default="benchmark/real,benchmark/case_study")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-gpu-gib", type=float, default=None,
                    help="cap GPU memory for weights on small GPUs; the rest is offloaded to CPU")
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {json.loads(l)["id"] for l in out.read_text(encoding="utf-8").splitlines() if l.strip()}
    env = {"python": platform.python_version(), "torch": torch.__version__,
           "transformers": transformers.__version__, "accelerate": accelerate.__version__,
           "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
           "model": MODEL_ID, "revision": REVISION, "max_new_tokens": MAX_NEW_TOKENS}
    out.with_name("environment.json").write_text(json.dumps(env, indent=2), encoding="utf-8")
    print("environment:", env, flush=True)
    processor = AutoProcessor.from_pretrained(MODEL_ID, revision=REVISION)
    mm = {0: f"{a.max_gpu_gib}GiB", "cpu": "24GiB"} if a.max_gpu_gib else None
    model = LlavaNextForConditionalGeneration.from_pretrained(
        MODEL_ID, revision=REVISION, torch_dtype=torch.bfloat16, device_map="auto", max_memory=mm,
        low_cpu_mem_usage=True)
    model.eval()
    eos = processor.tokenizer.eos_token_id
    prompt = build_prompt(dim_hint="", multiview=True)
    with out.open("a", encoding="utf-8") as fh:
        for split in a.splits.split(","):
            data = Path(split)
            items = [json.loads(l) for l in (data / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
                     if l.strip()]
            for rec in items:
                if rec["id"] in done:
                    continue
                img = Image.open(data / rec["image_mv"]).convert("RGB")
                inputs = processor(text=prompt, images=img, return_tensors="pt").to(model.device)
                t0 = time.time()
                with torch.inference_mode():
                    o = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS, do_sample=False,
                                       repetition_penalty=REPETITION_PENALTY, pad_token_id=eos,
                                       stopping_criteria=StoppingCriteriaList([Progress()]))
                n_new = int(o.shape[1] - inputs["input_ids"].shape[1])
                ended_eos = bool(o[0, -1].item() == eos)
                r = {"seed": 0, "id": rec["id"], "split": data.name, "key": "mv", "idx": 0, "dims": [],
                     "temperature": None, "call_seed": None, "new_tokens": n_new, "ended_eos": ended_eos,
                     "truncated": (not ended_eos) and n_new >= MAX_NEW_TOKENS, "gen_s": round(time.time() - t0, 1),
                     "text": processor.decode(o[0], skip_special_tokens=True)}
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                fh.flush()
                print(f"{rec['id']} {n_new} tok eos={ended_eos} {r['gen_s']}s", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
