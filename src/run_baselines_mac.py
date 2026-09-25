"""Mac (Apple Silicon) için ablasyon — FP16 + MPS backend.

bitsandbytes CUDA-only olduğundan bu script 4-bit yerine FP16 kullanır.
Gereksinim: ≥32 GB unified memory (13B FP16 ~26 GB alır).

Kurulum (Mac terminali):
    pip install torch torchvision          # Metal/MPS dahil
    pip install transformers accelerate
    pip install cadquery gradio pillow scipy svglib reportlab easyocr

Çalıştırma:
    python -m src.run_baselines_mac --data data --conditions raw_iso,full_ocr --limit 10

Windows sonuçlarıyla birleştirmek için:
    python -m src.merge_results --data data
"""

from __future__ import annotations
import os, sys, json, time, argparse, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch
from PIL import Image
from transformers import (
    LlavaNextForConditionalGeneration,
    AutoProcessor,
)
from src.framework import sketch_to_cad, FrameworkConfig
from src import dimensions as dim_mod, metrics

MODEL_ID = "StoryGold/bella-v1.0-13b"

# ── Koşullar (run_baselines.py ile aynı) ─────────────────────────────────────
from src.run_baselines import CONDITIONS, build_gt_step

def load_model_mac():
    """FP16 + MPS — bitsandbytes gerektirmez."""
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Cihaz: {device}")
    if device == "cpu":
        print("⚠ MPS bulunamadı, CPU kullanılıyor (çok yavaş olacak).")

    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = LlavaNextForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    ).to(device)
    model.eval()
    print(f"Model yüklendi (FP16, {device})")
    print(f"Bellek: {torch.mps.current_allocated_memory()/1e9:.1f} GB" if device=="mps" else "")
    return model, processor, device

@torch.inference_mode()
def generate_fn_mac(model, processor, device):
    def _gen(composed, prompt, i):
        inputs = processor(text=prompt, images=composed,
                           return_tensors="pt")
        inputs = {k: v.to(device) if hasattr(v, "to") else v
                  for k, v in inputs.items()}
        if device == "mps":
            # MPS için bazı tensor'ları float16'ya çevir
            if "pixel_values" in inputs:
                inputs["pixel_values"] = inputs["pixel_values"].half()

        kw = dict(max_new_tokens=512, repetition_penalty=1.1,
                  pad_token_id=processor.tokenizer.eos_token_id)
        if i == 0:
            kw["do_sample"] = False
        else:
            kw.update(do_sample=True, temperature=0.5, top_p=0.9)  # FrameworkConfig.temperature ile aynı
        out = model.generate(**inputs, **kw)
        return processor.decode(out[0], skip_special_tokens=True)
    return _gen


def run(data_dir, conditions, limit, offset=0):
    data = Path(data_dir)
    items = [json.loads(l) for l in
             (data/"manifest.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    items = [r for r in items if r.get("split") == "test"]
    if offset: items = items[offset:]
    if limit:  items = items[:limit]
    print(f"Test örneği: {len(items)} (offset={offset}) | koşullar: {conditions}")

    model, processor, device = load_model_mac()
    gen_fn = generate_fn_mac(model, processor, device)

    tmp  = Path(tempfile.mkdtemp(prefix="vericad_mac_"))
    work = tmp / "work"; work.mkdir()
    out_dir = data / "results"; out_dir.mkdir(exist_ok=True)

    summaries = {}
    for cond in conditions:
        spec   = CONDITIONS[cond]
        results = []
        t0     = time.time()
        print(f"\n=== KOŞUL: {cond} ===")
        for i, rec in enumerate(items):
            gt_step = str(tmp / f"gt_{i}.step")
            if not (os.path.exists(gt_step) or build_gt_step(rec["code"], gt_step)):
                continue
            img = Image.open(data / rec[spec["image"]]).convert("RGB")
            if   spec["ocr"] == "gt":   ocr_fn = lambda _img, d=rec.get("annotated_dims",[]): list(d)
            elif spec["ocr"] == "real": ocr_fn = lambda _img: dim_mod.extract_dimensions(_img)
            else:                       ocr_fn = lambda _img: []

            res  = sketch_to_cad([img], gen_fn, spec["cfg"], str(work), ocr_fn=ocr_fn)
            best = res["best"]
            m    = metrics.evaluate(best["step"], gt_step) if (best and best["step"]) else {"step_valid": False}
            m["family"] = rec.get("family", "?")
            results.append(m)
            if (i+1) % 5 == 0:
                print(f"  {i+1}/{len(items)}  ({(time.time()-t0)/(i+1):.1f} sn/örnek)")

        summaries[cond] = metrics.aggregate(results)

    batch_tag  = f"_mac_off{offset}_n{len(items)}"
    batch_file = out_dir / f"ablation{batch_tag}.json"
    batch_file.write_text(
        json.dumps({"offset": offset, "n": len(items), "results": summaries},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBatch kaydedildi → {batch_file}")
    print("Windows sonuçlarıyla birleştirmek için: python -m src.merge_results --data data")


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data",       default="data")
    ap.add_argument("--conditions", default="raw_iso,full_ocr")
    ap.add_argument("--limit",  type=int, default=10)
    ap.add_argument("--offset", type=int, default=0)
    args = ap.parse_args()
    from src.run_baselines import CONDITIONS as C
    conds = [c.strip() for c in args.conditions.split(",") if c.strip() in C] \
            if args.conditions != "all" else list(C.keys())
    run(args.data, conds, args.limit, args.offset)

if __name__ == "__main__":
    _main()
