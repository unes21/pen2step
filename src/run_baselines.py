"""Ablasyon değerlendirme harness'i (eğitimsiz framework).

Pen2STEP framework'ünün her bileşeninin katkısını ölçer. Test setindeki her
örnek için seçilen KOŞUL'la kod üretir → STEP → ground-truth STEP ile
src.metrics üzerinden karşılaştırır.

KOŞULLAR (ablasyon satırları):
    raw_iso     : tek izometrik görsel, framework YOK (ham bella)        → temel
    repair_iso  : tek görsel + AST kod onarımı + boyut recovery
    multiview   : çoklu-görünüm sayfası + multiview prompt + onarım
    full_ocr    : çoklu-görünüm + OCR boyut enjeksiyonu + 3 aday seçimi   → tam framework
    full_gt     : full ama ground-truth ölçüler enjekte (boyut üst sınırı)
    raw_mv      : çoklu-görünüm sayfası, framework YOK (onarım/scale yok) → GERÇEK SET TEMEL
                  (gerçek sette image_iso olmadığı için raw_iso yerine bu kullanılır;
                   çevre kabuğun -onarım+scale- katkısını gerçek veride izole eder)
    multiview_n3: multiview ile birebir aynı ama n_candidates=3            → eşit-N kontrol
                  (full_ocr/full_gt'nin best-of-3 avantajını kısıt kalitesinden ayırır)

Manifest'i DOĞRUDAN okur (train/ bağımlılığı yok).

Kullanım:
    python -m src.run_baselines --data data --conditions all --limit 100
    python -m src.run_baselines --data data --conditions raw_iso,full_ocr --limit 50
"""

from __future__ import annotations

import os
import sys
import json
import time
import argparse
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch
import cadquery as cq
from PIL import Image

from transformers import (
    LlavaNextForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
)

from src.framework import sketch_to_cad, FrameworkConfig
from src import dimensions as dim_mod
from src import metrics

MODEL_ID = "StoryGold/bella-v1.0-13b"


# ── Koşul tanımları ──────────────────────────────────────────────────────────

def _cfg(**kw):
    base = dict(use_repair=True, use_multiview_prompt=True, scale_recover=True,
                use_dimensions=False, n_candidates=1)
    base.update(kw)
    return FrameworkConfig(**base)


CONDITIONS = {
    "raw_iso":    {"image": "image_iso", "ocr": None,
                   "cfg": _cfg(use_repair=False, use_multiview_prompt=False,
                               scale_recover=False)},
    "repair_iso": {"image": "image_iso", "ocr": None,
                   "cfg": _cfg(use_multiview_prompt=False)},
    "multiview":  {"image": "image_mv", "ocr": None, "cfg": _cfg()},
    "full_ocr":   {"image": "image_mv", "ocr": "real",
                   "cfg": _cfg(use_dimensions=True, n_candidates=3)},
    "full_gt":    {"image": "image_mv", "ocr": "gt",
                   "cfg": _cfg(use_dimensions=True, n_candidates=3)},
    # Hakem yanıtı: gerçek-veri temeli (image_iso yok) ve eşit-N kontrolü.
    "raw_mv":     {"image": "image_mv", "ocr": None,
                   "cfg": _cfg(use_repair=False, scale_recover=False,
                               n_candidates=1)},
    "multiview_n3": {"image": "image_mv", "ocr": None,
                     "cfg": _cfg(n_candidates=3)},
    # Hakem yanıtı (A7a): raw_mv'nin düşük geçerliliğinin ne kadarı özel/uzun
    # talimatımızdan (80 kelime, primitif listesi, format kısıtları) kaynaklanıyor?
    # Kısa/minimal talimat + kabuk YOK, aksi hâlde raw_mv ile birebir aynı.
    # NOT: bu, CAD-Coder'ın kendi eğitim prompt'unun yeniden üretimi DEĞİLDİR
    # (kamuya açık kaynaklarda belgelenmemiş) — bkz. src/prompt.py üst notu.
    "raw_mv_shortprompt": {"image": "image_mv", "ocr": None,
                           "cfg": _cfg(use_repair=False, scale_recover=False,
                                       n_candidates=1, use_short_prompt=True)},
}


# ── Model ────────────────────────────────────────────────────────────────────

def load_model(model_id: str = MODEL_ID, temperature: float = 0.5, seed: int | None = None):
    # bfloat16 (4-bit bitsandbytes + device_map, accelerate dispatch ile uyumsuzdu)
    # İkinci-backbone genelleme testi için --model ile değiştirilebilir.
    # Örnekleme sıcaklığı parametre olarak alınır (varsayılan 0.5, makaledeki
    # tüm koşular ve FrameworkConfig.temperature ile aynı).
    print(f"Model yükleniyor: {model_id}  (temperature={temperature}, seed={seed})")
    if seed is not None:
        torch.manual_seed(seed)
    processor = AutoProcessor.from_pretrained(model_id)
    model = LlavaNextForConditionalGeneration.from_pretrained(
        model_id, torch_dtype=torch.bfloat16, device_map="auto", low_cpu_mem_usage=True,
    )
    model.eval()

    @torch.inference_mode()
    def generate_fn(composed, prompt, i):
        inputs = processor(text=prompt, images=composed,
                           return_tensors="pt").to(model.device)
        kw = dict(max_new_tokens=512,  # ablasyon için hız: basit parçalar ~200 token
                  repetition_penalty=1.1,
                  pad_token_id=processor.tokenizer.eos_token_id)
        if i == 0:
            kw["do_sample"] = False
        else:
            kw.update(do_sample=True, temperature=temperature, top_p=0.9)
        out = model.generate(**inputs, **kw)
        return processor.decode(out[0], skip_special_tokens=True)

    return generate_fn


# ── Ground-truth STEP (manifest kodundan) ────────────────────────────────────

def build_gt_step(code: str, path: str) -> bool:
    try:
        ns = {}
        exec(code, ns)
        result = ns.get("result")
        if result is None:
            return False
        cq.exporters.export(result, path)
        return os.path.exists(path)
    except Exception:
        return False


# ── Değerlendirme ────────────────────────────────────────────────────────────

def run(data_dir: str, conditions, limit: int, offset: int = 0, model_id: str = MODEL_ID,
        seed: int | None = None, temperature: float = 0.5, save_steps: bool = True,
        tag: str = "", manifest_name: str = "manifest.jsonl"):
    data = Path(data_dir)
    manifest = data / manifest_name
    items = [json.loads(l) for l in manifest.read_text(encoding="utf-8").splitlines() if l.strip()]
    items = [r for r in items if r.get("split") == "test"]
    if offset:
        items = items[offset:]
    if limit:
        items = items[:limit]
    print(f"Test örneği: {len(items)}  (offset={offset})  |  koşullar: {conditions}"
          f"  |  seed={seed}  |  T={temperature}")

    if seed is not None:
        import random
        random.seed(seed)
        try:
            import numpy as np
            np.random.seed(seed)
        except Exception:
            pass

    generate_fn = load_model(model_id, temperature=temperature, seed=seed)
    tmp = Path(tempfile.mkdtemp(prefix="vericad_eval_"))
    work = tmp / "work"
    work.mkdir()

    # Kalıcı STEP arşivi: poz-hizalı yeniden-skorlama (A3) tahmin edilen
    # katıya ihtiyaç duyuyor; eskiden bunlar tempdir'de skorlanıp atılıyordu.
    steps_root = None
    if save_steps:
        seed_tag = f"_seed{seed}" if seed is not None else ""
        steps_root = out_steps = data / "results" / "predicted_steps" / f"{tag}{seed_tag}".strip("_")
        steps_root.mkdir(parents=True, exist_ok=True)

    summaries = {}
    raw_all = {}
    for cond in conditions:
        spec = CONDITIONS[cond]
        results = []
        t0 = time.time()
        print(f"\n=== KOŞUL: {cond} ===")
        cond_step_dir = None
        if steps_root is not None:
            cond_step_dir = steps_root / cond
            cond_step_dir.mkdir(parents=True, exist_ok=True)
        for i, rec in enumerate(items):
            gt_step = str(tmp / f"gt_{i}.step")
            if not (os.path.exists(gt_step) or build_gt_step(rec["code"], gt_step)):
                continue

            img = Image.open(data / rec[spec["image"]]).convert("RGB")

            if spec["ocr"] == "gt":
                ocr_fn = lambda _img, _d=rec.get("annotated_dims", []): list(_d)
            elif spec["ocr"] == "real":
                ocr_fn = lambda _img: dim_mod.extract_dimensions(_img)
            else:
                ocr_fn = lambda _img: []

            res = sketch_to_cad([img], generate_fn, spec["cfg"], str(work), ocr_fn=ocr_fn)
            best = res["best"]
            pred_step_saved = None
            if best and best["step"]:
                m = metrics.evaluate(best["step"], gt_step)
                if cond_step_dir is not None and os.path.exists(best["step"]):
                    part_id = rec.get("id") or f"idx{i}"
                    pred_step_saved = str(cond_step_dir / f"{part_id}.step")
                    try:
                        import shutil
                        shutil.copy(best["step"], pred_step_saved)
                        gt_saved = str(cond_step_dir / f"{part_id}.gt.step")
                        shutil.copy(gt_step, gt_saved)
                    except Exception as exc:
                        print(f"  UYARI: STEP kopyalanamadı ({part_id}): {exc}")
            else:
                m = {"step_valid": False}
            m["family"] = rec.get("family", "?")
            m["id"] = rec.get("id")
            m["has_dims"] = bool(rec.get("annotated_dims"))
            if pred_step_saved:
                m["pred_step"] = pred_step_saved
            results.append(m)

            if (i + 1) % 10 == 0:
                print(f"  {i+1}/{len(items)}  ({(time.time()-t0)/(i+1):.1f} sn/örnek)")

        summaries[cond] = metrics.aggregate(results)
        raw_all[cond] = results

    # Çıktı — batch dosyası (offset ile ayrı kaydedilir, merge_results.py birleştirir)
    out_dir = data / "results"
    out_dir.mkdir(exist_ok=True)
    seed_tag = f"_seed{seed}" if seed is not None else ""
    tag_part = f"_{tag}" if tag else ""
    batch_tag = f"{tag_part}{seed_tag}_off{offset}_n{len(items)}" if offset else f"{tag_part}{seed_tag}_n{len(items)}"
    batch_file = out_dir / f"ablation{batch_tag}.json"
    (batch_file).write_text(
        json.dumps({"offset": offset, "n": len(items), "seed": seed, "temperature": temperature,
                    "model_id": model_id, "results": summaries, "raw": raw_all},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBatch kaydedildi → {batch_file}")

    # Markdown tablo
    cols = ["step_validity_rate", "chamfer_mm", "dim_error", "volume_error", "fscore"]
    lines = ["| koşul | SVR | Chamfer(mm) | BoyutHata | HacimHata | F-score |",
             "|---|---|---|---|---|---|"]
    for cond in conditions:
        s = summaries[cond]
        def f(k):
            v = s.get(k)
            return f"{v:.3f}" if isinstance(v, float) else "-"
        lines.append(f"| {cond} | {f('step_validity_rate')} | {f('chamfer_mm')} "
                     f"| {f('dim_error')} | {f('volume_error')} | {f('fscore')} |")
    table = "\n".join(lines)
    (out_dir / "ablation.md").write_text(table, encoding="utf-8")

    print("\n" + "=" * 60)
    print("ABLASYON SONUÇLARI")
    print("=" * 60)
    print(table)
    print(f"\nKaydedildi → {out_dir}")


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data",       default="data")
    ap.add_argument("--conditions", default="all",
                    help="virgülle ayrık koşullar veya 'all'")
    ap.add_argument("--limit",  type=int, default=100)
    ap.add_argument("--offset", type=int, default=0,
                    help="test setinin kaçıncı örnekten başlayacağı (batch için)")
    ap.add_argument("--model", default=MODEL_ID,
                    help="ikinci-backbone genelleme testi için HF model kimliği")
    ap.add_argument("--seed", type=int, default=None,
                    help="tohum (A6: tohumlu tekrarlar için, ör. --seed 0..4)")
    ap.add_argument("--temperature", type=float, default=0.5,
                    help="örnekleme sıcaklığı (FrameworkConfig.temperature ile eşleşmeli)")
    ap.add_argument("--no-save-steps", action="store_true",
                    help="tahmin edilen STEP dosyalarını kalıcı kaydetme (varsayılan: kaydet)")
    ap.add_argument("--tag", default="",
                    help="çıktı dosya adına eklenecek etiket (ör. 'native_prompt', 'model2')")
    ap.add_argument("--manifest", default="manifest.jsonl",
                    help="A5: 'manifest_rescaled.jsonl' ile ölçüsüz GT'lerin "
                         "kanonik geri-dönüşten ayrıştırılmış hâlini kullan")
    args = ap.parse_args()

    if args.conditions == "all":
        conds = list(CONDITIONS.keys())
    else:
        conds = [c.strip() for c in args.conditions.split(",") if c.strip() in CONDITIONS]
    if not conds:
        ap.error(f"geçerli koşul yok. Seçenekler: {list(CONDITIONS.keys())}")
    run(args.data, conds, args.limit, offset=args.offset, model_id=args.model,
        seed=args.seed, temperature=args.temperature, save_steps=not args.no_save_steps,
        tag=args.tag, manifest_name=args.manifest)


if __name__ == "__main__":
    _main()
