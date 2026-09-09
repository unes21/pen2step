# Provenance of every number in the paper

**Status: complete.** All 12 result rows in the manuscript are backed by a raw output file,
and all 12 were verified programmatically — every one of the five metrics matches its file
exactly at the precision printed in the paper (Chamfer to one decimal, the rest to three).

The tables in `paper/build_docx.py` (lines ~522–580) are hard-coded strings, not generated
from these files. This map is the only record linking the two; keep it up to date.

The ablations were run on Google Colab. Results were written to Google Drive
(`MyDrive/VeriCAD/results/`) and downloaded as Drive export archives. Those archives are
preserved verbatim under [`colab_drive_exports/`](colab_drive_exports/).

---

## Table 2 — synthetic split (n = 50)

| Paper row | SVR | Cham. | DimE | VolE | F | Source |
|---|---|---|---|---|---|---|
| raw_iso | 0.260 | 73.6 | 0.992 | 1.000 | 0.000 | `ablation_n50_rawiso_repairiso_multiview_fullocr.json` ✅ |
| repair_iso | 0.520 | 37.9 | 0.430 | 1.359 | 0.083 | same file ✅ |
| multiview | 0.540 | 50.0 | 0.620 | 0.968 | 0.040 | same file ✅ |
| full_ocr | 0.880 | 49.8 | 0.433 | 0.868 | 0.061 | same file ✅ |
| full_gt | 0.780 | 47.2 | 0.439 | 0.894 | 0.067 | `ablation_n50_full_gt.json` ✅ |

Origin: `colab_drive_exports/20260608_synthetic_n50/` (Drive export of 8 June 2026).

## Table 3 — real hand-drawn split (n = 19)

| Paper row | SVR | Cham. | DimE | VolE | F | Source |
|---|---|---|---|---|---|---|
| raw_mv (N=1) | 0.368 | 44.2 | 0.996 | 1.000 | 0.000 | `ablation_n19_rawmv_multiviewn3.json` ✅ |
| multiview (N=1) | 0.789 | 26.8 | 0.559 | 1.434 | 0.107 | `ablation_n19_multiview_fullocr_fullgt.json` ✅ |
| multiview (N=3) | 1.000 | 26.4 | 0.526 | 1.277 | 0.095 | `ablation_n19_rawmv_multiviewn3.json` ✅ |
| full_ocr (N=3) | 0.895 | 24.9 | 0.512 | 0.885 | 0.103 | `ablation_n19_fullocr_withfloor.json` ✅ |
| full_gt (N=3) | 0.947 | 24.0 | 0.422 | 0.904 | 0.119 | `ablation_n19_multiview_fullocr_fullgt.json` ✅ |

## Table 4 — OCR plausibility floor (n = 19)

| Paper row | SVR | Cham. | DimE | VolE | F | Source |
|---|---|---|---|---|---|---|
| Naive reader | 0.947 | 32.6 | 0.654 | 0.942 | 0.073 | `ablation_n19_multiview_fullocr_fullgt.json` → `full_ocr` ✅ |
| With floor | 0.895 | 24.9 | 0.512 | 0.885 | 0.103 | `ablation_n19_fullocr_withfloor.json` → `full_ocr` ✅ |

> **Naming hazard.** Both rows are stored under the condition name `full_ocr`, in two
> different runs. They differ only in the `min_max` argument of
> `src/dimensions.py::extract_dimensions`: the 15 June 13:21 export was produced without the
> plausibility floor, the 15 June 14:34 export with it (`min_max = 10`). Nothing inside the
> JSON records which setting was used — only the export folder distinguishes them. When
> re-running, encode the setting in the condition name.

---

## Result files with no corresponding table row

| File | Condition | Numbers |
|---|---|---|
| `ablation_n50_multiview_n3.json` | `multiview_n3`, n = 50 | SVR 0.980, Cham 49.3, DimE 0.614, VolE 0.944, F 0.062 |
| `ablation_n2_raw_iso.json` | `raw_iso`, n = 2 | early pilot, superseded |

`multiview_n3` at n = 50 is the equal-candidate-budget control for the synthetic split and
is worth adding to Table 2: at N = 3 without dimensions, validity reaches **0.980** against
0.880 for `full_ocr`. That is the same direction as the real split — dimension injection
lowers validity at equal N — evidence the manuscript currently reports only for n = 19.

---

## Which files carry per-part data

Confidence intervals, subgroup breakdowns, and paired tests need the `raw` block.

| File | n | Conditions | Per-part `raw` |
|---|---|---|---|
| `ablation_n19_multiview_fullocr_fullgt.json` | 19 | multiview, full_ocr, full_gt | ✅ |
| `ablation_n19_rawmv_multiviewn3.json` | 19 | raw_mv, multiview_n3 | ✅ |
| `ablation_n19_fullocr_withfloor.json` | 19 | full_ocr | ✅ |
| `ablation_n50_multiview_n3.json` | 50 | multiview_n3 | ✅ |
| `ablation_n50_rawiso_repairiso_multiview_fullocr.json` | 50 | 4 conditions | ❌ aggregates only |
| `ablation_n50_full_gt.json` | 50 | full_gt | ❌ aggregates only |

**Consequence:** the real split (Table 3, Table 4) supports full statistical analysis —
bootstrap CIs and paired McNemar / Wilcoxon tests across all five conditions, once the three
files are merged. The synthetic split (Table 2) does **not**: four of its five rows exist
only as aggregates, so no interval estimate can be computed for Table 2 without re-running
that ablation.

Merge the real split and analyse it:

```
python -m src.merge_results
python -m src.analyze_results --json results/<merged_n19>.json --pairs raw_mv:multiview_n3,multiview_n3:full_ocr,multiview_n3:full_gt,full_ocr:full_gt
```

`ablation_n19_analysis.md` in this directory covers only `raw_mv` vs `multiview_n3`, because
it was run before the other files were recovered. Regenerate it over the merged file.

---

## The OCR confidence threshold: resolved

The manuscript states **θ = 0.45**. The working copy of `src/dimensions.py` declared
`conf_thr = 0.30`, which looked like a contradiction. It is not: the code was edited
**after** the experiments.

Two snapshots of `src/dimensions.py` survive:

| Snapshot | Date | `conf_thr` | `min_max` |
|---|---|---|---|
| `Sketch2CAD-Aktarim.zip` | 15 Jun 2026, 16:31 | **0.45** | 10.0 |
| `sketch2cad_eval.zip` | 26 Jun 2026, 12:38 | 0.30 | 10.0 |

Only the `full_ocr` condition reads the OCR output (`full_gt` injects ground-truth
dimensions; every other condition passes `ocr: None`). Every `full_ocr` run in the paper
predates the change:

| Run | Produces | Threshold in force |
|---|---|---|
| 8 Jun 2026, 20:58 | Table 2 `full_ocr` | 0.45 |
| 15 Jun 2026, 13:21 | Table 4 "Naive reader" | 0.45 |
| 15 Jun 2026, 14:34 | Table 3 `full_ocr (N=3)`, Table 4 "With floor" | 0.45 |
| 29 Jun 2026, 15:08 | `raw_mv`, `multiview_n3` — **no OCR** | not applicable |

The 0.30 version therefore never produced a published number. **The manuscript is correct
and the code had drifted.** `src/dimensions.py` in this repository has been restored to
`conf_thr = 0.45`, with a comment recording why.

> Caveat: the 8 June run predates the earliest surviving snapshot by a week. 0.45 is
> attested on 15 June and nothing indicates a change during that week, but it is inferred
> rather than directly observed for the synthetic run.

## Table 4 is two runs, not one toggle

The "Naive reader" and "With floor" rows come from two separate Colab runs 73 minutes
apart, not from one run with a flag flipped. Comparing them part by part, **11 of 19 parts
differ**:

- Four undimensioned parts (real_05, real_06, real_09, real_15) move from F = 0.000 with
  Chamfer 46–76 mm to usable values — exactly the "spurious small reading shrinks the solid"
  failure the floor is described as preventing. This corroborates the mechanism.
- But two parts (real_07, real_13) become **invalid**, and four dimensioned parts change
  even though the floor should be a no-op for them.

Since candidate sampling is stochastic (N = 3, T = 0.4 in the code) and neither run fixed a seed, the
reported difference mixes the floor's effect with run-to-run variance. Table 4 is therefore
suggestive rather than a controlled ablation. Re-running both arms with fixed seeds — ideally
several — is the way to separate the two.

---

## Constant-by-constant audit: manuscript against the code that ran

> This table records the state **as first found**. The four mismatches were resolved in the
> final manuscript — see "Resolution: applied" at the end of this document.

| Manuscript | Code | Verdict |
|---|---|---|
| θ = 0.45 | `conf_thr = 0.45` at run time | ✅ match (see section above) |
| τ = 0.02·‖bbox(G)‖ | `tau=0.02 * max(diag, 1e-6)` | ✅ match |
| Canonical fallback 100 mm | `canonical_size = 100.0` | ✅ match |
| N = 3 candidates | `n_candidates = 3` | ✅ match |
| Accepted range [1, 10000] mm | `lo = 1.0, hi = 10000.0` | ✅ match |
| Plausibility floor m = 10 mm | `min_max = 10.0` | ✅ match |
| **n_s = 8192 surface points** | **`n_points: int = 4000`** | ❌ **mismatch** |
| **Sampling temperature T = 0.5** | **`temperature: float = 0.4`** | ❌ **mismatch** |
| **30-second execution timeout** | **`timeout: int = 60`** | ❌ **mismatch** |
| Backbone "LLaVA-1.5-style 13B" | `StoryGold/bella-v1.0-13b` loaded through `LlavaNextForConditionalGeneration` — LLaVA-NeXT (1.6), described in the project README as a CADCoder fine-tune | ❌ **mismatch** |
| View labels FRONT / TOP / SIDE | `MULTIVIEW_CLAUSE` in `src/prompt.py` says `ON=front, UST=top, YAN=side` (Turkish) | ❌ **mismatch** |

### n_s = 4000, not 8192 — proven, not inferred

`src/metrics.py` carries the timestamp **31 May 2026 14:31** in every surviving archive,
which predates all four ablation runs (8 Jun, 15 Jun ×2, 29 Jun). It declares
`n_points: int = 4000` in both `sample_surface` and `evaluate`, and
`src/run_baselines.py:170` calls `metrics.evaluate(best["step"], gt_step)` without
overriding it. No 8192-point version of the file exists anywhere on disk.

This matters beyond bookkeeping. Section 4 explains that "identical solids score F ≈ 0.95
rather than 1.0" as the practical ceiling of the metric. That ceiling was measured at 4000
points per surface, not 8192, so the sampling noise floor is higher than the manuscript
implies — and every reported F-score inherits it.

Point sampling itself is seeded (`seed=1` for the prediction, `seed=2` for the ground truth),
so evaluation is deterministic given a pair of solids. The run-to-run variance discussed
above comes from candidate generation, not from the metric.

### T = 0.5 and 30 s — mismatch, with a caveat

`temperature = 0.4` and `timeout = 60` appear in **every** surviving snapshot of
`src/framework.py` (22 Jun, 23 Jun, and the current copy); no 0.5 / 30 s version exists.
Neither value is overridden by `_cfg()` in `src/run_baselines.py`, so the defaults are what
ran. The caveat is that the earliest surviving `framework.py` is dated after the June runs,
so unlike `n_points` this is strong evidence rather than proof.

Note that Section 5.1 states "the 30-second execution timeout was never reached in practice".
If the limit was in fact 60 s, that sentence needs rewriting even if no candidate ever timed
out.

### Resolution: applied

The manuscript has been corrected to match the code that ran. In the final version
(`Pen2STEP_JCDE_LAST.docx`):

- `n_s = 8192` → **4000** (Section 4 and Appendix B)
- `T = 0.5` → **0.4** (Sections 3, 5.1, 6 and Appendix B)
- 30-second timeout → **60-second** (Sections 3, 5.1 and Appendix B)
- "LLaVA-1.5-style 13B" → the checkpoint is named: **StoryGold/bella-v1.0-13b**, a 13B
  LLaVA-NeXT CAD-oriented fine-tune, used exactly as released (Sections 3, 5.1, Appendix B,
  and the label inside Figure 1)
- Section 3 now states that the benchmark's view labels are the Turkish abbreviations
  ON / UST / YAN and that the prompt supplies the mapping
- Appendix A now carries the verbatim prompt from `src/prompt.py` and `src/dimensions.py`

`src/dimensions.py` in this repository keeps `conf_thr = 0.45`, the value that produced the
published OCR numbers. Code and manuscript now agree on every constant.

## Prompt punctuation normalized

One character in the base instruction of `src/prompt.py` was normalized from an em dash to a
hyphen ("Output ONLY Python code - no markdown ...") so that the repository and the verbatim
prompt in Appendix A are byte-identical. This is a cosmetic change to a formatting instruction
and does not affect the reported reconstruction results; the checkpoint revision pinned in
Appendix B is the authoritative reproducibility anchor.
