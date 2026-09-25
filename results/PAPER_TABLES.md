# Provenance of every number in the paper

Every table in the manuscript is traced here to a file in this repository. The synthetic
split (Table 2) and the real hand-drawn split (Tables 3 and 4, Figures 5 and 6) were produced
by two different protocols, described separately below.

Sampling temperature for every run in the paper: **T = 0.5** (top-p 0.9, repetition penalty
1.1, at most 512 new tokens; candidate 0 greedy). The default in `src/framework.py`,
`src/run_baselines.py`, `src/generation_dump.py` and `app.py` is 0.5.

---

## Table 2 — synthetic split (n = 50)

Single unseeded run per condition, June 2026, Google Colab (A100, bfloat16). The runtime
guards (arc fallback, partial-execution salvage, result discovery, base-plate removal) were
active in every row, including `raw_iso`. Point sets are mean-centred, not pose-aligned;
Chamfer, DimE, VolE and F are averaged over valid solids only.

| Paper row | SVR | Cham. | DimE | VolE | F | Source |
|---|---|---|---|---|---|---|
| raw_iso | 0.260 | 73.6 | 0.992 | 1.000 | 0.000 | `ablation_n50_rawiso_repairiso_multiview_fullocr.json` |
| repair_iso | 0.520 | 37.9 | 0.430 | 1.359 | 0.083 | same file |
| multiview (N=1) | 0.540 | 50.0 | 0.620 | 0.968 | 0.040 | same file |
| multiview (N=3) | 0.980 | 49.3 | 0.614 | 0.944 | 0.062 | `ablation_n50_multiview_n3.json` |
| full_ocr | 0.880 | 49.8 | 0.433 | 0.868 | 0.061 | `ablation_n50_rawiso_repairiso_multiview_fullocr.json` |
| full_gt | 0.780 | 47.2 | 0.439 | 0.894 | 0.067 | `ablation_n50_full_gt.json` |

Origin: `colab_drive_exports/20260608_synthetic_n50/`.

---

## Real split: recorded generations and offline replay

The shell never feeds an execution result back into generation, so the text of a candidate
depends only on (sheet, prompt, candidate index, seed). The real-split numbers are therefore
produced in two steps.

1. **Generation (GPU, once).** `src/generation_dump.py` recorded 238 raw generations on
   22 September 2026 (Google Colab, one A100, bfloat16, library versions as resolved by pip on
   that date): seeds 0, 1, 2; candidates 0 to 2; prompt keys `mv` (no dimensions), `ocr`
   (OCR with plausibility floor), `ocrn` (naive OCR, only where it differs) and `gt`
   (annotated dimensions). Candidate 0 is greedy and recorded once. Every generation reached
   the 512-token limit.
   Output: [`replay/dump.jsonl`](replay/dump.jsonl), [`replay/ocr_dims.json`](replay/ocr_dims.json).
2. **Replay and scoring (CPU).** `src/replay.py` executes the recorded text under each shell
   configuration (CadQuery 2.7.0), selects, and scores against the original and the rescaled
   ground truth. `src/stats.py` computes every statistic with one convention;
   `src/trivial_replay.py` scores the two input-agnostic baselines.
   Outputs: [`replay/replay_rows.json`](replay/replay_rows.json) (per part, seed, condition),
   [`replay/stats.json`](replay/stats.json), [`replay/trivial.json`](replay/trivial.json).

```bash
python -m src.replay --dump results/replay/dump.jsonl
python -m src.stats
python -m src.trivial_replay
python -m src.ocr_eval
python tools/make_gallery.py --condition multiview_n3 --seed 0
python tools/make_fig_validity_fidelity.py
python tools/make_graphical_abstract.py
```

Statistical convention (real split): F-scores average all 19 parts with an invalid output
scored as 0, per-part values averaged over seeds; 95% CIs from 10,000 bootstrap resamples over
parts; exact Wilcoxon signed-rank for paired F (zero differences dropped, number of non-zero
pairs reported); exact McNemar per seed for paired validity; Wilson interval on pooled SVR.
Chamfer, DimE and VolE are averaged over valid solids only. "Aligned" = best of 24
axis-aligned rotations (minimum Chamfer). "Scale-norm." = prediction rescaled to the
ground-truth bounding-box diagonal before alignment. Measured F ceiling (ground truth against
itself, resampled): 0.959, range 0.857 to 0.996.

## Table 3 — real hand-drawn split (n = 19)

`stats.json` key → `orig.conditions.<name>` (and `rescaled.conditions.<name>` for the
rescaled-GT column); baselines from `trivial.json`.

| Paper row | Replay condition | Valid | F raw | F al. [95% CI] | F al. s-n | F al. rescaled | CD al.† | DimE† | VolE† |
|---|---|---|---|---|---|---|---|---|---|
| Bare model (N=1) | `raw_mv_bare` | 0/19 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | n/a | n/a |
| Runtime guards only (N=1) | `raw_mv` | 7/19 | 0.000 | 0.000 | 0.051 | 0.000 | 45.6 | 0.995 | 1.000 |
| Full shell (N=1) | `multiview_n1` | 19/19 | 0.083 | 0.093 [0.061, 0.127] | 0.126 | 0.072 | 23.8 | 0.590 | 1.208 |
| Full shell (N=3) | `multiview_n3` | 19/19 | 0.083 | 0.093 [0.061, 0.127] | 0.126 | 0.072 | 23.8 | 0.590 | 1.208 |
| + OCR dims, naive (N=3) | `full_ocr_naive` | 19/19 | 0.056 | 0.067 [0.038, 0.099] | 0.139 | 0.046 | 30.9 | 0.740 | 1.266 |
| + OCR dims, floor (N=3) | `full_ocr` | 19/19 | 0.086 | 0.088 [0.061, 0.120] | 0.121 | 0.067 | 23.0 | 0.575 | 1.032 |
| + GT dims, oracle (N=3) | `full_gt` | 19/19 | 0.111 | 0.122 [0.088, 0.155] | 0.124 | 0.100 | 20.8 | 0.466 | 0.801 |
| Constant 100×50×30 mm box | `constant_box` | 19/19 | 0.155 | 0.172 [0.122, 0.225] | 0.185 | 0.119 | 17.6 | 0.415 | 2.890 |
| GT bounding box | `gt_bbox` | 19/19 | 0.408 | 0.418 [0.304, 0.540] | 0.418 | 0.420 | 10.7 | 0.000 | 0.963 |

Valid counts are identical for seeds 0, 1, 2. Seed SD of mean aligned F: 0 (no dimensions,
greedy candidate selected everywhere), 0.0015 (OCR), 0.012 (GT). Selecting by positive
volume in addition to STEP export (`orig_volsel`) changes no selection.

Paired tests quoted in Sections 5.3 and 5.4 (`stats.json` → `orig.paired`; constant-box rows from `orig.vs_constant_box` and `rescaled.vs_constant_box`):

| Pair | Result |
|---|---|
| bare → full shell N=1 | McNemar p = 3.8e-6 per seed (19 discordant); Wilcoxon p = 8e-6, n = 18 |
| guards only → full shell N=1 | McNemar p = 4.9e-4 per seed (12 discordant) |
| full shell N=1 vs N=3 | identical |
| full shell vs + OCR (floor) | Wilcoxon p = 1.0, n = 3 |
| full shell vs + GT | +0.029 [0.003, 0.058], p = 0.094, n = 6 |
| + OCR (floor) vs + GT | +0.033, p = 0.031, n = 6 |
| naive vs floor OCR | +0.021 [−0.009, 0.057] for the floor, p = 0.074, n = 9 |
| full shell vs constant box | box higher by 0.079 [0.035, 0.127], p = 0.0033; shell above box on 6 of 19 |
| + OCR (floor) vs constant box | box higher by 0.083 [0.039, 0.132], p = 0.0020 |
| + GT vs constant box | box higher by 0.050 [−0.009, 0.111], p = 0.080 |
| full shell vs constant box, rescaled GT | box higher by 0.048 [0.007, 0.091], p = 0.054 |

## Table 4 — mechanism ablation (greedy candidate, N = 1, no dimensions)

| Paper row | Replay condition | Valid | F al. | F al. s-n |
|---|---|---|---|---|
| Bare model | `raw_mv_bare` | 0/19 | 0.000 | 0.000 |
| + partial-execution salvage only | `bare_plus_partial` | 0/19 | 0.000 | 0.000 |
| + scale recovery only | `bare_plus_scale` | 0/19 | 0.000 | 0.000 |
| + AST repair | `bare_plus_repair` | 10/19 | 0.000 | 0.079 |
| + AST repair and scale recovery | `bare_plus_repair_scale` | 10/19 | 0.048 | 0.078 |
| Full shell | `multiview_n1` | 19/19 | 0.093 | 0.126 |
| − AST repair | `n1_minus_repair` | 7/19 | 0.034 | 0.051 |
| − partial-execution salvage | `n1_minus_partial` | 10/19 | 0.048 | 0.078 |
| − result discovery | `n1_minus_discover` | 11/19 | 0.058 | 0.082 |
| − base-plate removal | `n1_minus_base` | 19/19 | 0.093 | 0.134 |
| − arc fallback | `n1_minus_arc` | 19/19 | 0.093 | 0.126 |
| − scale recovery | `n1_minus_scale` | 19/19 | 0.000 | 0.126 |

Firing counts (`stats.json` → `firing.multiview_n1`, divided by 3 seeds): result-variable
step of AST repair 19, parse fix 12, partial-execution salvage 9, result discovery 8, scale
recovery 19, base-plate removal 1, arc fallback 0.

## OCR token precision and recall (Section 5.4)

`python -m src.ocr_eval`: on the six dimensioned sheets (26 annotated values), floor
precision 5/8 = 0.63, naive precision 5/15 = 0.33, recall 5/26 = 0.19. The floor removes all
five spurious tokens (2 or 4 mm) accepted by the naive reader on four undimensioned sheets.

## Figures

| Figure | File | Script |
|---|---|---|
| 5 | `figures/prediction_gallery_replay.png` | `tools/make_gallery.py --condition multiview_n3 --seed 0` |
| 6 | `figures/fig_validity_fidelity_replay.png` | `tools/make_fig_validity_fidelity.py` |
| Graphical abstract | `figures/graphical_abstract.png` | `tools/make_graphical_abstract.py` |

---

## Superseded real-split files

`ablation_n19_*.json` come from an earlier unseeded run (June 2026) in a different library
environment and no longer back any number in the paper. That run gave the same guards-only
count (7 of 19) but 15 of 19 for the single-candidate full shell; greedy decoding is not
bit-reproducible across library and hardware versions. They are kept for the record.
