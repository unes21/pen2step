# Pen2STEP-Bench-Equipment

Hand-drawn three-view sheets of physical heavy-equipment spare parts, drawn by people outside the
author group (site mechanics, site engineers, students) under one fixed protocol, with ground-truth
CadQuery models built independently of the sketches. This split is collected after the development
split (`benchmark/real`, drawn by the authors) and does not change any result reported on it.

Status: collection in progress (branch `equipment`). Every number about this split is produced by
the scripts below; no number is typed by hand.

## Part families (24 to 36 parts, 6 families x 4 to 6)

pins and bushings; flanged shafts and couplings; bolts and wear plates; brackets and mounts;
hydraulic fittings and adapters; track and ground-engaging parts. Every part is physically
available; the OEM part number is recorded when it exists.

## Drawing session protocol (identical for every drawer)

- Materials: the part, plain A4 paper, ballpoint pen, caliper and tape measure. No example drawing,
  template or system output is shown.
- Printed instruction at the top of the sheet: draw the part in three views (front, top, side) as if
  ordering it from a supplier, write the dimensions you measured, label the views in your own language.
  No other guidance; questions are answered with "as you see fit".
- Start and end time are recorded (`sketch_minutes`); the drawer rates "could a part be made from this
  drawing?" from 1 to 5 (`drawer_confidence`).
- Photograph: phone camera, single frame, ambient light, no scanner app or correction, paper on the
  table (same condition as the development split). File name `images/equip_XX_mv.jpg`.
- At most four parts per drawer. No drawer identity is stored; `drawers.csv` holds role and date only.

## Files

| File | Content |
|---|---|
| `manifest.jsonl` | one row per sheet (schema below) |
| `parts.csv` | `part_id, family, oem_no, source, supplier_drawing, notes` |
| `drawers.csv` | `role, session_date, n_sheets, consent_signed` (no names) |
| `gt_measurements.csv` | every measured value: `part_id, dim_name, value_mm, tool, tolerance_mm, source` (caliper ±0.05 mm, tape ±1 mm; source = OEM drawing or measurement) |
| `gt_second_check.csv` | independent check of three main dimensions per model: `part_id, dim_name, model_mm, measured_mm, checker_role` |
| `gt/<id>.py`, `gt/<id>.step` | ground-truth CadQuery model and its STEP export |
| `images/equip_XX_mv.jpg` | the photographed sheet |

Manifest row fields: `id`, `image_mv`, `family`, `oem_no`, `drawer_role` (mechanic / engineer /
student), `n_dims_annotated` (at least 3), `annotated_dims` (the values written on the sheet, in mm,
transcribed exactly; used by the ground-truth-dimension condition), `drawer_confidence` (1 to 5),
`sketch_minutes`, `has_dims` (true), `split` ("equipment"), `code` (the ground-truth CadQuery program).

## Ground-truth rules

Preferred source: the OEM or supplier drawing; otherwise caliper measurement of the part. The person
who models a part has not drawn it and models it without seeing the sketch. Every model must export
to STEP with positive volume and reach a self F-score ceiling of at least 0.85; the second checker
measures three main dimensions on the physical part and returns the model if any differs by more
than 2%.

```bash
python src/metrics.py --split equipment --selfcheck      # all checks above; exit code 1 on any failure
```

## Replay (no new generation needed for the shell configurations)

```bash
# open backbone (GPU, once)
python -m src.generation_dump --data benchmark/equipment --out results/replay_equipment/dump.jsonl
# frontier backends (API, once; resumable; --dry-run prints the number of calls)
python -m src.generation_dump_api --backend anthropic --data benchmark/equipment \
    --out results/replay_anthropic_equipment/generations_anthropic.jsonl
# offline replay, baselines and statistics
python -m src.replay --dump results/replay_equipment/dump.jsonl --data benchmark/equipment --out results/replay_equipment
python -m src.trivial_replay --gt results/replay_equipment --out results/replay_equipment/trivial.json
python src/stats.py --split equipment
python src/stats.py --backend anthropic --split equipment
python tools/make_paper_tables.py --backends open,anthropic,openai --split equipment --out results/PAPER_TABLES_equipment.md
```

All equipment parts carry dimensions, so no rescaled manifest exists; `src/replay.py` then scores the
"rescaled" column against the same ground truth.
