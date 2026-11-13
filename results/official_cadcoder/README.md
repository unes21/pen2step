# Official CAD-Coder evaluation on the Pen2STEP sheets

The official evaluation of CAD-Coder (github.com/anniedoris/CAD-Coder, commit in `cadcoder_commit.txt`)
run unchanged on one A100 (13 November 2026), first on its own 100-sample test subset and then on the
27 Pen2STEP sheets (19 development, 8 case study) with the official prompt, greedy decoding
(temperature 0), 3450 new tokens and conv-mode vicuna_v1. Script: `tools/official_cadcoder/run_colab.sh` as of commit 07144ce (`pen2step_commit.txt`); the later revision d3a6bd2 only adds resuming, an early copy of the raw outputs and a 120 s limit per generated program, and was not used for these results.

| Test set | Generations | Valid code | Valid STL/STEP | Reached 3450 tokens |
|---|---|---|---|---|
| CAD-Coder subset (100) | 100 | 1.00 | 1.00 (IoU 0.674) | 0 |
| Pen2STEP development (19) | 19 | 17/19 | 15/19 | 4 |
| Pen2STEP case study (8) | 8 | 7/8 | 7/8 | 1 |

"Valid code" and "valid STL" are the official criteria of `scripts/generate_model_cad.py` (the program
runs; the program plus an export of the variable `solid` writes an STL and a STEP file). No Pen2STEP shell
stage is involved.

Files: `inference_results/<set>/merge.jsonl` (raw decoded text, official format), `tokens.jsonl` (output
tokens recovered by re-tokenising the decoded text with the CAD-Coder tokenizer, and the limit flag:
within 10 tokens of 3450), `results.csv` and `cad_gen_results.txt` (official validity), `model_code/`
and `model_step/` (executed programs and STEP solids), `cad_iou_results.txt` (official IoU, subset only),
`environment_*.txt` and `pip_freeze_*.txt` (library versions: Python 3.10.22, torch 2.1.2+cu121,
transformers 4.37.2; CadQuery 2.7.0 from pip instead of conda-forge), `run.log`.

Deviations from the README: CadQuery installed with pip; the CAD step was run with `--parallel` as in the
README. No program was time-limited in this run.
