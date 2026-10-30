# Case study: spare parts of a concrete placing boom (Putzmeister MXR 32-4)

Twenty spare parts selected from the manufacturer's spare parts list of the MXR 32-4 / RS850
stationary placing boom. Only part numbers and dimensions from that list are used; no catalogue page
is reproduced.

| File | Content |
|---|---|
| `make_reference_sheets.py` | ground-truth CadQuery models (`gt/<id>.py`, `gt/<id>.step`), reference sheets (`sheets/<id>.png`) and `parts.json` |
| `parts.json` | id, names, catalogue number, dimension source, dimensions, volume |
| `reference_sheets_20.pdf` | the twenty reference sheets in one file (A4 landscape) |
| `sketches_raw/` | the two scanned sheets returned by the drawer (four parts per sheet) |
| `make_case_gallery.py` | Figure 7 of the paper (`figures/case_study_gallery.png`) |

Dimension sources: `catalogue` (complete geometry stated in the spare parts list: four bushes, two
wear plates), `DIN` (fasteners; nominal sizes from the DIN standard named in the list), and
`representative` (three hinge pins, two bolt locating plates, one bracket; the list gives no
dimensions, pin diameters match the mating bushes and the other sizes are assumed).

Eight parts (cs_01, cs_02, cs_03, cs_05, cs_07, cs_13, cs_18, cs_19) were drawn freehand by a
practising civil design engineer outside the author group, from the reference sheets, four parts per
A4 sheet, views unlabelled, captured with a scanning application. Each part was cut from its sheet
into `benchmark/case_study/images/<id>_mv.png` without further processing.

```bash
python case_study/make_reference_sheets.py
python -m src.generation_dump --data benchmark/case_study --seeds 0,1,2 --temperature 0.5 --out results/replay_case/dump.jsonl   # GPU, once
python -m src.replay --dump results/replay_case/dump.jsonl --data benchmark/case_study --out results/replay_case
python -m src.trivial_replay --gt results/replay_case --out results/replay_case/trivial.json
python -m src.stats --rows results/replay_case/replay_rows.json --trivial results/replay_case/trivial.json --out results/replay_case/stats.json
python case_study/make_case_gallery.py
```

The recorded generations (`results/replay_case/dump.jsonl`, 147 records) were produced on one A100
in bfloat16 with transformers 5.20.2 and PyTorch 2.11 (`results/replay_case/environment.json`),
a newer environment than the development run.
