"""13 ölçüsüz gerçek parçanın ground-truth ölçeğini kanonik 100 mm'den ayrıştır.

Hakem yanıtı A5 (limitasyon "Coupling between the benchmark and the fallback
scale"): ölçüsüz parçaların GT'si şu anda en uzun kenarı ~100 mm olacak
şekilde ELLE kurulmuş — framework'ün kanonik geri-dönüş değeriyle (100 mm)
BİREBİR aynı. Bu, ölçüsüz alt-kümedeki yüksek başarıyı yapı gereği (by
construction) sağlıyor olabilir.

Bu script, o 13 parçanın kodunu ORANTIYI KORUYARAK bağımsız, tohumlu-rastgele
bir hedef en-uzun-kenara ölçekler (m mm ~ U[40, 250], 100'e yakın olması
zorunlu DEĞİL) ve yeni bir manifest üretir. Ölçülü 6 parçanın kodu
DEĞİŞMEZ — onların GT ölçeği zaten çizimdeki gerçek mm değerlerinden geliyor,
kanonik geri-dönüşle bir ilgisi yok.

Kullanım:
    python -m benchmark.real.rescale_undimensioned
    # çıktı: benchmark/real/manifest_rescaled.jsonl + rescale_report.md

Yeniden değerlendirme (GPU koşusundan sonra, ayrı bir adım):
    python -m src.run_baselines --data benchmark/real --manifest manifest_rescaled.jsonl ...
(veya klasörü kopyalayıp manifest.jsonl olarak kullanın — bkz. README notu.)
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).resolve().parent
MANIFEST_IN = HERE / "manifest.jsonl"
MANIFEST_OUT = HERE / "manifest_rescaled.jsonl"
REPORT_OUT = HERE / "rescale_report.md"

SEED = 42
TARGET_RANGE_MM = (40.0, 250.0)  # kanonik 100 mm'e yakın olması ZORUNLU değil


def bbox_longest_edge(code: str) -> float:
    ns: dict = {}
    exec(code, ns)
    r = ns["result"]
    shp = r.val() if hasattr(r, "val") else r
    bb = shp.BoundingBox()
    return max(bb.xlen, bb.ylen, bb.zlen)


def build_rescaled_code(code: str, factor: float) -> str:
    """Orijinal kodun sonuna, `result`'ı `factor` ile ölçekleyen satırlar ekler.

    `result` bir Workplane olabileceğinden önce .val() ile Shape'e iniyoruz
    (Shape.scale mevcut, Workplane.scale değil).
    """
    return (code.rstrip() +
            f"\n_r0 = result.val() if hasattr(result, 'val') else result"
            f"\nresult = _r0.scale({factor!r})\n")


def main():
    rng = random.Random(SEED)
    recs = [json.loads(l) for l in MANIFEST_IN.read_text(encoding="utf-8").splitlines() if l.strip()]

    report_rows = []
    out_recs = []
    for rec in recs:
        rec = dict(rec)  # kopya
        if rec.get("has_dims"):
            out_recs.append(rec)
            report_rows.append((rec["id"], rec["family"], True, None, None, None))
            continue

        old_edge = bbox_longest_edge(rec["code"])
        target = rng.uniform(*TARGET_RANGE_MM)
        factor = target / old_edge if old_edge > 1e-9 else 1.0

        new_code = build_rescaled_code(rec["code"], factor)
        new_edge = bbox_longest_edge(new_code)  # doğrula

        rec["code"] = new_code
        rec["_original_longest_edge_mm"] = round(old_edge, 2)
        rec["_target_longest_edge_mm"] = round(target, 2)
        rec["_rescale_factor"] = round(factor, 4)
        out_recs.append(rec)
        report_rows.append((rec["id"], rec["family"], False, round(old_edge, 1),
                            round(target, 1), round(factor, 3)))

    MANIFEST_OUT.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in out_recs) + "\n",
        encoding="utf-8")

    lines = ["# GT ölçek ayrıştırma raporu (A5)",
             "",
             f"Tohum={SEED}, hedef aralık=[{TARGET_RANGE_MM[0]:.0f}, {TARGET_RANGE_MM[1]:.0f}] mm. "
             "Ölçülü 6 parça değişmedi (zaten çizimdeki gerçek mm ile ölçekli).",
             "",
             "| id | family | has_dims | eski en-uzun-kenar (mm) | yeni hedef (mm) | ölçek çarpanı |",
             "|---|---|---|---|---|---|"]
    for rid, fam, has_dims, old, new, fac in report_rows:
        if has_dims:
            lines.append(f"| {rid} | {fam} | evet | (değişmedi) | (değişmedi) | 1.0 |")
        else:
            lines.append(f"| {rid} | {fam} | hayır | {old} | {new} | {fac} |")
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")

    n_resc = sum(1 for r in report_rows if not r[2])
    print(f"{n_resc} ölçüsüz parça yeniden ölçeklendi (tohum={SEED}).")
    print(f"Yeni manifest → {MANIFEST_OUT}")
    print(f"Rapor        → {REPORT_OUT}")


if __name__ == "__main__":
    main()
