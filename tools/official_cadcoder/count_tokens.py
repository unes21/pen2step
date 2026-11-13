"""Add output token counts and the limit flag to the merge.jsonl files of the official evaluation.

The official loader (llava/eval/model_vqa_loader.py) stores only the decoded text, decoded with
skip_special_tokens=True and stripped. The number of generated tokens is therefore recovered by
re-tokenising that text with the CAD-Coder tokenizer (no special tokens added). A generation that
reaches max_new_tokens = 3450 cannot have emitted the end-of-sequence token, so a re-tokenised count
within LIMIT_MARGIN of 3450 is flagged as reaching the limit; re-tokenisation can differ from the
generated sequence by a few tokens at word boundaries. Writes <dir>/tokens.jsonl and prints a summary.

    python count_tokens.py inference/inference_results/CAD-Coder/<split> [...]
"""
import json
import sys
from pathlib import Path

from transformers import AutoTokenizer

MAX_NEW = 3450
LIMIT_MARGIN = 10
tok = AutoTokenizer.from_pretrained("CADCODER/CAD-Coder", use_fast=False)
for d in map(Path, sys.argv[1:]):
    rows = [json.loads(l) for l in (d / "merge.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    out = []
    for r in rows:
        n = len(tok(r["text"], add_special_tokens=False).input_ids)
        out.append({"question_id": r["question_id"], "output_tokens_retokenised": n,
                    "reached_limit": n >= MAX_NEW - LIMIT_MARGIN, "text": r["text"]})
    (d / "tokens.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out), encoding="utf-8")
    ns = [x["output_tokens_retokenised"] for x in out]
    print(f"{d}: {len(out)} generations, tokens min {min(ns)} median {sorted(ns)[len(ns) // 2]} max {max(ns)}, "
          f"reached limit {sum(x['reached_limit'] for x in out)}")
