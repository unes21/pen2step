"""Kayıtlı tahmin+GT STEP çiftlerini poz-hizalı (best-of-24) yeniden skorla.

Hakem yanıtı A3: Chamfer/F-score yönelime duyarlı (mean-centering sadece
konumu düzeltir, dönmeyi düzeltmez). run_baselines.py artık her koşulun
tahmin edilen VE kullandığı ground-truth STEP dosyalarını kalıcı olarak
<data>/results/predicted_steps/<tag>/<condition>/<id>.step (+.gt.step)
altına kaydediyor. Bu script o dosyaları TEKRAR ÜRETMEDEN (GPU gerekmez,
sadece CPU + cadquery) hem orijinal (hizasız) hem de hizalı kuralla
yeniden skorlar, ikisini yan yana raporlar.

Kullanım:
    python -m src.rescore_pose_aligned --dir data/results/predicted_steps/seed0
    python -m src.rescore_pose_aligned --dir data/results/predicted_steps/seed0 --out results/pose_aligned_seed0.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src import metrics


def rescore_dir(root: Path) -> dict:
    """root/<condition>/<id>.step + <id>.gt.step çiftlerini tara ve skorla."""
    out = {}
    for cond_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        cond = cond_dir.name
        rows = []
        for pred_path in sorted(cond_dir.glob("*.step")):
            if pred_path.name.endswith(".gt.step"):
                continue
            part_id = pred_path.stem
            gt_path = cond_dir / f"{part_id}.gt.step"
            if not gt_path.exists():
                print(f"  UYARI: {gt_path} yok, atlanıyor ({cond}/{part_id})")
                continue
            raw = metrics.evaluate(str(pred_path), str(gt_path), align=False)
            aligned = metrics.evaluate(str(pred_path), str(gt_path), align=True)
            rows.append({
                "id": part_id,
                "step_valid": raw["step_valid"],
                "chamfer_mm_raw": raw["chamfer_mm"],
                "chamfer_mm_aligned": aligned["chamfer_mm"],
                "fscore_raw": raw["fscore"],
                "fscore_aligned": aligned["fscore"],
                "rotation_applied": aligned.get("rotation_applied"),
                "dim_error": raw["dim_error"],   # yönelimden bağımsız, aynı
                "volume_error": raw["volume_error"],
            })
            print(f"  {cond}/{part_id}: F {raw['fscore']} -> {aligned['fscore']}"
                  f"  (rotation_applied={aligned.get('rotation_applied')})")
        if rows:
            valid = [r for r in rows if r["step_valid"]]

            def _mean(key):
                vals = [r[key] for r in valid if r.get(key) is not None]
                return sum(vals) / len(vals) if vals else None

            out[cond] = {
                "n": len(rows), "n_valid": len(valid),
                "fscore_raw_mean": _mean("fscore_raw"),
                "fscore_aligned_mean": _mean("fscore_aligned"),
                "chamfer_raw_mean": _mean("chamfer_mm_raw"),
                "chamfer_aligned_mean": _mean("chamfer_mm_aligned"),
                "pct_rotated": (sum(1 for r in valid if r.get("rotation_applied")) / len(valid)
                                if valid else None),
                "rows": rows,
            }
    return out


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True,
                    help="run_baselines.py --tag ile üretilen predicted_steps/<tag> klasörü")
    ap.add_argument("--out", default=None, help="sonuç JSON yolu (varsayılan: <dir>/pose_aligned.json)")
    args = ap.parse_args()

    root = Path(args.dir)
    if not root.exists():
        ap.error(f"klasör yok: {root}")

    result = rescore_dir(root)
    out_path = Path(args.out) if args.out else root / "pose_aligned.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 70)
    print("ÖZET — Hizasız vs Poz-Hizalı (best-of-24)")
    print("=" * 70)
    print(f"{'koşul':22s} {'n_valid':>8s} {'F(ham)':>8s} {'F(hizalı)':>10s} {'%rotated':>9s}")
    for cond, s in result.items():
        fr = s["fscore_raw_mean"]; fa = s["fscore_aligned_mean"]; pr = s["pct_rotated"]
        print(f"{cond:22s} {s['n_valid']:8d} {fr:8.3f} {fa:10.3f} {(pr or 0)*100:8.1f}%"
              if fr is not None and fa is not None else f"{cond:22s} (veri yok)")
    print(f"\nKaydedildi → {out_path}")


if __name__ == "__main__":
    _main()
