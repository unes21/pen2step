"""GPU koşuları için minimal yükleme paketi oluşturur (A6, A7a, A7b).

İçerik:
    src/                                tüm framework + harness kodu (düzeltmelerle)
    benchmark/real/manifest.jsonl       orijinal 19 parça
    benchmark/real/manifest_rescaled.jsonl  A5: GT ölçek ayrıştırılmış manifest
    benchmark/real/images/*.jpg         19 çok-görünüm görseli

Çıktı: pen2step_gpu_bundle.zip (bu script'in yanında)

Kullanım: python tools/make_gpu_bundle.py
"""
from __future__ import annotations
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "pen2step_gpu_bundle.zip"


def main():
    files: list[tuple[Path, str]] = []

    for p in (ROOT / "src").glob("*.py"):
        files.append((p, f"src/{p.name}"))

    re_dir = ROOT / "benchmark" / "real"
    for name in ["manifest.jsonl", "manifest_rescaled.jsonl", "rescale_report.md"]:
        p = re_dir / name
        if p.exists():
            files.append((p, f"benchmark/real/{name}"))
    for p in (re_dir / "images").glob("*.jpg"):
        files.append((p, f"benchmark/real/images/{p.name}"))

    req = ROOT / "requirements.txt"
    if req.exists():
        files.append((req, "requirements.txt"))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc in files:
            z.write(src, arc)

    mb = OUT.stat().st_size / 1e6
    print(f"wrote {OUT.name}  ({mb:.1f} MB, {len(files)} files)")


if __name__ == "__main__":
    main()
