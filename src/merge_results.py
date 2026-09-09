"""Batch ablasyon sonuçlarını birleştir.

Her batch ayrı bir ablation_off{N}_n{K}.json dosyasına kaydedilir.
Bu script tümünü okuyup ağırlıklı ortalama ile ablation.json + ablation.md üretir.

Kullanım:
    python -m src.merge_results --data data
"""

from __future__ import annotations
import json, argparse
from pathlib import Path
from src.metrics import aggregate


def merge(data_dir: str):
    out_dir = Path(data_dir) / "results"
    # Tüm batch dosyalarını bul (hem offset'li hem offsetsiz)
    files = sorted(out_dir.glob("ablation_*.json"))
    if not files:
        print("[HATA] Henüz hiç batch dosyası yok.")
        return

    print(f"{len(files)} batch dosyası bulundu:")
    for f in files:
        print(f"  {f.name}")

    # Her koşul için tüm batch'lerin per-sample listelerini birleştir
    all_results: dict[str, list] = {}
    total_samples = 0
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        n = data.get("n", 0)
        total_samples = max(total_samples, data.get("offset", 0) + n)
        for cond, summary in data.get("results", {}).items():
            # summary = aggregate dict — geri genişletmek için n bilgisi kullan
            if cond not in all_results:
                all_results[cond] = []
            # aggregate'i mock per-sample listesine dönüştür (yaklaşık)
            # Gerçek per-sample listemiz yoksa summary'yi n×tekrarlayarak ağırlık veririz
            all_results[cond].append((n, summary))

    # Ağırlıklı ortalama
    conditions = list(all_results.keys())
    metrics_keys = ["step_validity_rate", "chamfer_mm", "chamfer_norm",
                    "dim_error", "volume_error", "fscore"]
    merged = {}
    for cond, batches in all_results.items():
        total_n    = sum(n for n, _ in batches)
        total_valid = sum(int(round(s.get("step_validity_rate", 0) * s.get("n", n)))
                         for n, s in batches)
        merged[cond] = {"n": total_n, "step_validity_rate": total_valid / total_n if total_n else 0}
        for k in metrics_keys[1:]:
            vals = [(s.get(k), n) for n, s in batches if s.get(k) is not None]
            if vals:
                weighted = sum(v * w for v, w in vals) / sum(w for _, w in vals)
                merged[cond][k] = weighted
            else:
                merged[cond][k] = None

    # Kaydet
    (out_dir / "ablation.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown tablo
    lines = [
        f"Toplam batch: {len(files)}  |  Toplam örnek: {sum(n for _,_,n in [(f,d,d.get('n',0)) for f,d in [(f, json.loads(f.read_text())) for f in files]])}",
        "",
        "| koşul | SVR | Chamfer(mm) | BoyutHata | HacimHata | F-score |",
        "|---|---|---|---|---|---|",
    ]
    for cond in conditions:
        s = merged[cond]
        def fmt(k):
            v = s.get(k)
            return f"{v:.3f}" if isinstance(v, float) else "-"
        lines.append(
            f"| {cond} | {fmt('step_validity_rate')} | {fmt('chamfer_mm')} "
            f"| {fmt('dim_error')} | {fmt('volume_error')} | {fmt('fscore')} |"
        )
    table = "\n".join(lines)
    (out_dir / "ablation.md").write_text(table, encoding="utf-8")

    print("\n=== BİRLEŞTİRİLMİŞ SONUÇLAR ===")
    print(table)
    print(f"\nKaydedildi → {out_dir / 'ablation.json'}")
    print(f"            → {out_dir / 'ablation.md'}")


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    args = ap.parse_args()
    merge(args.data)

if __name__ == "__main__":
    _main()
