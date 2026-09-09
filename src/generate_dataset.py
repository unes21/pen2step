"""Pen2STEP-Bench veri setini üretir.

Her örnek için:
    images/<split>/<id>.png   — el-çizimi stilinde eskiz (model girdisi)
    manifest.jsonl            — {id, image, code, dims, family, split} satırları

`code` ground-truth CadQuery kodudur (gerçek mm, `result` ile biter) ve hem
eğitim etiketi hem de değerlendirmede ground-truth katı kaynağıdır.

Kullanım:
    python -m src.generate_dataset --n 2000 --out data --seed 0
    python -m src.generate_dataset --n 30 --out data_smoke --no-hand-drawn   # hızlı test
"""

from __future__ import annotations

import os
import sys
import json
import time
import random
import argparse
import traceback
from pathlib import Path

# Paket olarak da, doğrudan da çalışsın
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import part_families
from src.render import render_sketch
from src.multiview import render_multiview_sample, bbox_dims


def _split_of(rng: random.Random, ratios) -> str:
    r = rng.random()
    train, val = ratios
    if r < train:
        return "train"
    if r < train + val:
        return "val"
    return "test"


def build_result(code: str):
    """Ground-truth kodu çalıştırıp `result` katısını döndür."""
    ns: dict = {}
    exec(code, ns)  # kod kendi ürettiğimiz güvenli şablon
    if "result" not in ns:
        raise RuntimeError("kod 'result' tanımlamadı")
    return ns["result"]


def generate(n: int, out: str, seed: int = 0, hand_drawn: bool = True,
             size: int = 512, ratios=(0.8, 0.1)):
    out_dir = Path(out)
    img_root = out_dir / "images"
    for sp in ("train", "val", "test"):
        (img_root / sp).mkdir(parents=True, exist_ok=True)

    manifest_path = out_dir / "manifest.jsonl"
    rng = random.Random(seed)

    written = 0
    attempts = 0
    family_counts: dict[str, int] = {}
    t0 = time.time()

    with manifest_path.open("w", encoding="utf-8") as mf:
        while written < n:
            attempts += 1
            if attempts > n * 4 + 50:
                print(f"[uyarı] çok fazla başarısız deneme, {written} örnekte durduruldu")
                break

            try:
                code, dims = part_families.sample(rng)
                result = build_result(code)
                # Çoklu-görünüm + boyut-anotasyonlu sayfa (ana girdi)
                img_mv, annotated = render_multiview_sample(
                    result, rng, size=max(280, size // 2), hand_drawn=hand_drawn)
                # Tek izometrik görünüm, anotasyonsuz (ablasyon: tek-görünüm baseline)
                img_iso = render_sketch(result, rng, size=size, hand_drawn=hand_drawn)
                xl, yl, zl = bbox_dims(result)
            except Exception:
                if attempts <= 5:
                    traceback.print_exc()
                continue

            split = _split_of(rng, ratios)
            sample_id = f"{written:06d}"
            rel_mv = f"images/{split}/{sample_id}_mv.png"
            rel_iso = f"images/{split}/{sample_id}_iso.png"
            img_mv.save(out_dir / rel_mv)
            img_iso.save(out_dir / rel_iso)

            rec = {
                "id": sample_id,
                "image": rel_mv,          # ana görsel = çoklu-görünüm sayfası
                "image_mv": rel_mv,
                "image_iso": rel_iso,
                "code": code,
                "dims": dims,
                "bbox": [round(xl, 3), round(yl, 3), round(zl, 3)],
                "annotated_dims": annotated,   # çizimdeki ölçü sayıları (ground-truth)
                "family": dims.get("family", "unknown"),
                "split": split,
            }
            mf.write(json.dumps(rec, ensure_ascii=False) + "\n")
            mf.flush()

            family_counts[rec["family"]] = family_counts.get(rec["family"], 0) + 1
            written += 1
            if written % 50 == 0 or written == n:
                rate = written / max(time.time() - t0, 1e-6)
                print(f"  {written}/{n}  ({rate:.1f} örnek/sn)")

    dt = time.time() - t0
    print(f"\n[bitti] {written} örnek yazıldı → {manifest_path}  ({dt:.0f} sn)")
    print("Aile dağılımı:")
    for fam, c in sorted(family_counts.items()):
        print(f"  {fam:18s}: {c}")

    # Özet meta
    (out_dir / "dataset_info.json").write_text(json.dumps({
        "n": written, "seed": seed, "hand_drawn": hand_drawn,
        "image_size": size, "ratios": {"train": ratios[0], "val": ratios[1],
                                        "test": round(1 - sum(ratios), 3)},
        "families": family_counts,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def _main():
    ap = argparse.ArgumentParser(description="Pen2STEP-Bench üretici")
    ap.add_argument("--n", type=int, default=2000, help="örnek sayısı")
    ap.add_argument("--out", default="data", help="çıktı klasörü")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--size", type=int, default=512, help="görüntü kenar uzunluğu")
    ap.add_argument("--no-hand-drawn", action="store_true",
                    help="el-çizimi artırımını kapat (temiz teknik çizim)")
    args = ap.parse_args()

    generate(args.n, args.out, seed=args.seed,
             hand_drawn=not args.no_hand_drawn, size=args.size)


if __name__ == "__main__":
    _main()
