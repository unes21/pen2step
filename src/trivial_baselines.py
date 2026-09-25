"""Basit (trivial) taban çizgileri — hakem yanıtı A7c.

Hakem: "SVR herhangi bir katıyı ödüllendirir; sabit bir box(100,50,30) SVR'de
%100 alır; hizalanmış F'i ~0.1 ise, boru hattı hiçbir şekil bilgisi katmıyor
demektir." Bu script iki taban çizgisini GERÇEK 19 parçalık sette (hem
orijinal hem A5'in ölçek-ayrıştırılmış GT'lerinde) çalıştırır:

    constant_box   : her girdi için AYNI sabit box(100,50,30) tahmini
                     (prompt'taki örnek — modelin "hiçbir şey öğrenmediği"
                     durumun alt sınırı)
    gt_bbox        : ground-truth'un KENDİ sınırlayıcı-kutusu boyutlarında
                     bir box (şekil bilgisi yok, sadece doğru ÖLÇEK — DimE/VolE
                     için üst sınır, F/Chamfer için hâlâ yanlış TOPOLOJİ)

Tamamen CPU'da çalışır, GPU/VLM gerekmez — mevcut ground-truth STEP'lere
karşı skorlanır. Hem hizasız hem poz-hizalı (best-of-24) sonuç raporlanır.

Kullanım:
    python -m src.trivial_baselines --manifest benchmark/real/manifest.jsonl
    python -m src.trivial_baselines --manifest benchmark/real/manifest_rescaled.jsonl
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import cadquery as cq

from src import metrics


def build_gt_step(code: str, path: str) -> bool:
    try:
        ns = {}
        exec(code, ns)
        result = ns.get("result")
        if result is None:
            return False
        cq.exporters.export(result, path)
        return True
    except Exception:
        return False


def run(manifest_path: str):
    recs = [json.loads(l) for l in Path(manifest_path).read_text(encoding="utf-8").splitlines()
            if l.strip()]

    tmp = Path(tempfile.mkdtemp(prefix="trivial_baseline_"))
    variants = {"constant_box": [], "gt_bbox": []}

    for i, rec in enumerate(recs):
        gt_path = str(tmp / f"gt_{i}.step")
        if not build_gt_step(rec["code"], gt_path):
            print(f"  UYARI: GT inşa edilemedi ({rec.get('id')})")
            continue

        gt_shape = metrics.load_shape(gt_path)
        gt_bb = gt_shape.BoundingBox()

        # 1) sabit kutu (prompt örneği: 100x50x30)
        const_path = str(tmp / f"const_{i}.step")
        cq.exporters.export(cq.Workplane("XY").box(100, 50, 30), const_path)

        # 2) GT'nin kendi bbox boyutlarında bir kutu (şekil değil, ölçek doğru)
        bbox_path = str(tmp / f"bbox_{i}.step")
        cq.exporters.export(
            cq.Workplane("XY").box(gt_bb.xlen, gt_bb.ylen, gt_bb.zlen), bbox_path)

        for name, pred_path in [("constant_box", const_path), ("gt_bbox", bbox_path)]:
            raw = metrics.evaluate(pred_path, gt_path, align=False)
            aligned = metrics.evaluate(pred_path, gt_path, align=True)
            row = {
                "id": rec.get("id"), "family": rec.get("family"),
                "has_dims": bool(rec.get("has_dims")),
                "step_valid": raw["step_valid"],
                "fscore_raw": raw["fscore"], "fscore_aligned": aligned["fscore"],
                "chamfer_raw": raw["chamfer_mm"], "chamfer_aligned": aligned["chamfer_mm"],
                "dim_error": raw["dim_error"], "volume_error": raw["volume_error"],
            }
            variants[name].append(row)

    def summarize(rows):
        n = len(rows)
        valid = [r for r in rows if r["step_valid"]]
        def _mean(key):
            vals = [r[key] for r in valid if r.get(key) is not None]
            return sum(vals) / len(vals) if vals else None
        return {
            "n": n, "n_valid": len(valid), "svr": len(valid) / n if n else 0.0,
            "fscore_raw": _mean("fscore_raw"), "fscore_aligned": _mean("fscore_aligned"),
            "chamfer_raw": _mean("chamfer_raw"), "chamfer_aligned": _mean("chamfer_aligned"),
            "dim_error": _mean("dim_error"), "volume_error": _mean("volume_error"),
        }

    print(f"\n{'taban çizgisi':16s} {'SVR':>6s} {'F(ham)':>8s} {'F(hizalı)':>10s} "
          f"{'Cham(hizalı)':>13s} {'DimE':>7s} {'VolE':>7s}")
    summary = {}
    for name, rows in variants.items():
        s = summarize(rows)
        summary[name] = {**s, "rows": rows}
        print(f"{name:16s} {s['svr']:6.3f} {s['fscore_raw']:8.3f} {s['fscore_aligned']:10.3f} "
              f"{s['chamfer_aligned']:13.2f} {s['dim_error']:7.3f} {s['volume_error']:7.3f}")

    out_path = Path(manifest_path).with_name(
        f"trivial_baselines_{Path(manifest_path).stem}.json")
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nKaydedildi → {out_path}")


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()
    run(args.manifest)


if __name__ == "__main__":
    _main()
