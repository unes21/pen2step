# Raw ablation output

**Start with [`PAPER_TABLES.md`](PAPER_TABLES.md)**: it maps every number in the
manuscript to the file it came from.

## replay/ (real split, every number in Tables 3 and 4)

| File | Content |
|---|---|
| `replay/dump.jsonl` | 238 recorded raw generations (seeds 0, 1, 2; A100, bfloat16, T = 0.5; 22 Sep 2026) |
| `replay/ocr_dims.json` | OCR dimension sets, with floor and naive (`#naive`) |
| `replay/replay_rows.json` | per part, seed and condition: selected candidate, mechanism firing, scores against original and rescaled ground truth |
| `replay/stats.json` | output of `src/stats.py` |
| `replay/trivial.json` | constant-box and ground-truth-bounding-box baselines |
| `replay/gallery_steps/` | the 19 predicted STEP solids shown in Figure 5 |
| `ocr_eval.json` | OCR token precision and recall (`src/ocr_eval.py`) |

## Earlier run (June 2026)

The JSON files below are the direct output of `src/run_baselines.py`. Only the synthetic
(`n50`) files back numbers in the paper (Table 2); the `n19` files are superseded by the
replay above and kept for the record.

Each JSON is the direct output of `src/run_baselines.py`. The `results` key holds the
per-condition aggregate; `raw` holds one record per part (validity, Chamfer, dimension
error, volume error, F-score, part family, dimensioned/undimensioned flag).

| File | Split | Conditions |
|---|---|---|
| `ablation_n19_multiview_fullocr_fullgt.json` | real, n = 19 | `multiview` (N=1), `full_ocr` (no floor), `full_gt` |
| `ablation_n19_rawmv_multiviewn3.json` | real, n = 19 | `raw_mv`, `multiview_n3` |
| `ablation_n19_analysis.md` | real, n = 19 | bootstrap 95% CIs, D/U subgroups, per-family results, McNemar and Wilcoxon tests |
| `ablation_n19_fullocr_withfloor.json` | real, n = 19 | `full_ocr` (with the m = 10 mm floor) |
| `ablation_n50_rawiso_repairiso_multiview_fullocr.json` | synthetic, n = 50 | `raw_iso`, `repair_iso`, `multiview`, `full_ocr` |
| `ablation_n50_full_gt.json` | synthetic, n = 50 | `full_gt` |
| `ablation_n50_multiview_n3.json` | synthetic, n = 50 | `multiview_n3` |
| `ablation_n2_raw_iso.json` | synthetic, n = 2 | early pilot, superseded |

Files are named after the conditions they contain because two different runs were
originally both called `ablation_n19.json`.

Regenerate the analysis with:

```
python -m src.analyze_results --json results/ablation_n19_rawmv_multiviewn3.json --pairs raw_mv:multiview_n3
```

## colab_drive_exports/

The ablations ran on Google Colab and wrote to `MyDrive/VeriCAD/results/` (VeriCAD was this
project's earlier working name, now Pen2STEP; the historical paths are kept verbatim). The Google Drive
export archives are preserved here unmodified, each in a folder tagged with its export
timestamp, together with the original `.zip`. They are the primary record; the JSON files in
this directory above are copies promoted out of them under explicit names.

| Export | Contains |
|---|---|
| `20260608_synthetic_n50/` | Table 2 rows: raw_iso, repair_iso, multiview, full_ocr (plus resume flags) |
| `20260615a_real_n19/` | superseded real-split run: multiview (N=1), full_gt, full_ocr without floor |
| `20260615b_real_n19_fullocr_floor/` | superseded real-split run: full_ocr with floor |
