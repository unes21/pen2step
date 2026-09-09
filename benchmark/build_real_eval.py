"""Gerçek el-çizimi test setini kur: görselleri ön-işle + manifest.jsonl yaz.

Çıktı: data/real_eval/  (kendine yeten --data kökü)
    images/real_NN_mv.jpg   (EXIF düzeltilmiş, en uzun kenar 1600px)
    manifest.jsonl          (split=test, code=GT, annotated_dims, family)

run_baselines GT STEP'i rec["code"]'dan kendisi üretir; image_mv'yi okur.
Gerçek veride çalıştırılacak koşullar: multiview, full_ocr, full_gt
(hepsi image_mv kullanır; image_iso yok).
"""
import os, json, glob
from PIL import Image, ImageOps
from gt_models import PARTS

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(SRC, "..", "data", "real_eval"))
IMG = os.path.join(OUT, "images")
os.makedirs(IMG, exist_ok=True)

# kaynak jpg'ler ad sırasına göre = PARTS 01..19 sırası
src_jpgs = sorted(glob.glob(os.path.join(SRC, "20260615_*.jpg")))
keys = list(PARTS.keys())
assert len(src_jpgs) == len(keys), f"{len(src_jpgs)} jpg != {len(keys)} parça"

MAXSIDE = 1600
lines = []
for key, jpg in zip(keys, src_jpgs):
    code, fam, dims = PARTS[key]
    # görsel ön-işle
    im = Image.open(jpg)
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    s = MAXSIDE / max(w, h)
    if s < 1:
        im = im.resize((round(w*s), round(h*s)), Image.LANCZOS)
    rel = f"images/real_{key}_mv.jpg"
    im.save(os.path.join(OUT, rel), quality=90)
    rec = {
        "id": f"real_{key}",
        "image": rel,
        "image_mv": rel,
        "code": code,
        "annotated_dims": dims,
        "family": fam,
        "has_dims": bool(dims),
        "split": "test",
    }
    lines.append(json.dumps(rec, ensure_ascii=False))
    print(f"{key} {fam:18s} dims={dims if dims else '-'}  {im.size}")

with open(os.path.join(OUT, "manifest.jsonl"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

n_dim = sum(1 for k in keys if PARTS[k][2])
print(f"\n→ {OUT}")
print(f"   {len(keys)} parça ({n_dim} ölçülü, {len(keys)-n_dim} ölçüsüz)")
print(f"   manifest.jsonl + images/ hazır")
