# Pen2STEP

**Training-free conversion of hand-drawn engineering sketches to parametric CAD models using a frozen vision-language model.**

Pen2STEP takes a photograph of a hand-drawn multi-view engineering sheet and returns an
editable parametric solid exported to STEP. No component is trained or fine-tuned here: a
frozen open-weight vision-language model is wrapped in a deterministic engineering shell
that performs multi-view composition, OCR-based dimension extraction and prompt injection,
N-candidate sampling, AST-level repair, execution-guided selection, and metric scale recovery.

This repository holds everything behind the manuscript: the pipeline, the Pen2STEP-Bench
benchmark including the original photographs, the verified ground-truth models, the raw
ablation output, the analysis scripts, the figures, and the manuscript build scripts.

> **Status:** the manuscript is under review. Every result row in the manuscript is backed by
> a raw output file under [`results/`](results/) and was verified against it; see
> [`results/PAPER_TABLES.md`](results/PAPER_TABLES.md) for the number-by-number provenance.

---

## The backbone

| | |
|---|---|
| Checkpoint | `StoryGold/bella-v1.0-13b` |
| Architecture | LLaVA-NeXT (LLaVA 1.6) Vicuna 13B, via `LlavaNextForConditionalGeneration` |
| Precision, experiments | `torch.bfloat16` (`src/run_baselines.py`) |
| Precision, interactive demo | 4-bit NF4, ~9 GB VRAM (`app.py`) |
| Weight updates | **None.** The checkpoint is used exactly as released. |

The checkpoint is a third-party CAD-oriented fine-tune of LLaVA-NeXT. Pen2STEP performs no
training, fine-tuning, or adapter fitting at any stage; all task-specific behaviour lives in
the deterministic shell and in the injected prompt (`src/prompt.py`).

`src/run_baselines.py` accepts `--model`, so the shell runs against any
`LlavaNext`-compatible checkpoint without code changes.

---

## Installation

Python 3.11 recommended. A CUDA GPU with >= 16 GB VRAM is needed for the 13B backbone;
dataset synthesis, metrics, analysis, and figures all run on CPU.

```bash
python -m venv venv
```

Windows: `venv\Scripts\activate` — Linux/macOS: `source venv/bin/activate`

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

```bash
pip install -r requirements.txt
```

`easyocr` downloads a ~64 MB recognition model on first call. Without it the pipeline still
runs, but the dimension pathway is disabled and every part falls back to the canonical
100 mm longest edge.

---

## Reproducing the results

### Real hand-drawn split (n = 19)

The 19 evaluation images, the original camera photographs, and the verified ground-truth
CadQuery models all ship with this repository under `benchmark/real/`.

Every real-split number in the paper (Tables 3 and 4, Figures 5 and 6) comes from recorded
generations replayed offline. The shell never feeds an execution result back into generation,
so the raw text of each candidate is recorded once on a GPU and every shell configuration is
then re-executed on the CPU on identical model outputs. The recorded generations (seeds 0, 1,
2; A100, bfloat16, T = 0.5) ship in `results/replay/dump.jsonl`, so no GPU is needed to
reproduce the tables:

```bash
python -m src.replay --dump results/replay/dump.jsonl
python -m src.trivial_replay
python -m src.stats
python -m src.ocr_eval
```

To record new generations (GPU):

```bash
python -m src.generation_dump --data benchmark/real --seeds 0,1,2 --temperature 0.5 --out results/replay_new/dump.jsonl
```

`results/PAPER_TABLES.md` maps every number in the paper to its file and key.
`benchmark/real/manifest_rescaled.jsonl` reassigns the 13 undimensioned parts an independent
longest edge in [40, 250] mm (seed 42) and is scored alongside the original ground truth.

The earlier live driver is kept; it generates and executes in one pass (GPU):

```bash
python -m src.run_baselines --data benchmark/real --conditions raw_mv,multiview_n3 --limit 19
```

Seven conditions are defined in `src/run_baselines.py`; `--conditions all` runs every one.
"Runtime guards" are arc fallback, partial-execution salvage, result discovery and
base-plate removal (Section 3 of the paper); they are active in every condition of this driver:

| Condition | Input view | Shell | Dimensions | Candidates |
|---|---|---|---|---|
| `raw_iso` | isometric | runtime guards only | none | 1 |
| `repair_iso` | isometric | AST repair + scale recovery | none | 1 |
| `multiview` | composed sheet | full | none | 1 |
| `multiview_n3` | composed sheet | full | none | 3 |
| `full_ocr` | composed sheet | full | OCR | 3 |
| `full_gt` | composed sheet | full | ground truth | 3 |
| `raw_mv` | composed sheet | runtime guards only | none | 1 |

`raw_iso` and `repair_iso` need an `image_iso` field, which the real split does not have;
`raw_mv` is the corresponding baseline there. Results are written to `<data-dir>/results/`.

### Synthetic split (n = 50)

The synthetic images are regenerated rather than stored — the full pool is ~1.2 GB and
generation is deterministic given the seed. The manifest describing the pool **is** tracked,
at `benchmark/synthetic/manifest.jsonl`.

```bash
python -m src.generate_dataset --n 3000 --out data --seed 0
```

```bash
python -m src.run_baselines --data data --conditions all --limit 50
```

A 12-sample smoke test that needs no GPU:

```bash
python -m src.generate_dataset --n 12 --out data_smoke
```

### Statistical analysis

Bootstrap 95% confidence intervals, dimensioned/undimensioned subgroups, per-family
results, and paired McNemar / Wilcoxon tests:

```bash
python -m src.analyze_results --json results/ablation_n19_rawmv_multiviewn3.json --pairs raw_mv:multiview_n3
```

### Figures

```bash
python figures/gen_figs.py
python tools/make_gallery.py --condition multiview_n3 --seed 0
python tools/make_fig_validity_fidelity.py
python tools/make_graphical_abstract.py
```

All write into `figures/`; none depends on an absolute path.

### Interactive demo

```bash
python app.py
```

Gradio interface at `http://127.0.0.1:7860`. Sample inputs are in `examples/`.

---

## Repository layout

```
src/                          pipeline, metrics, ablation driver, analysis
app.py                        Gradio demo (4-bit)
S2CAD.py                      earlier single-image demo, kept for reference
tools/make_colab_zip.py       packages the repo for a Colab run
tools/make_gpu_bundle.py      packages the files needed by src/generation_dump.py
tools/make_*.py               figure scripts (gallery, Figure 6, graphical abstract)

benchmark/
  real/images/                19 evaluation images consumed by the pipeline
  real/raw_photographs/       19 original camera JPEGs - the primary record
  real/manifest.jsonl         id, family, ground-truth code, annotated dims, D/U flag
  real/gt_models.py           verified ground-truth CadQuery model per part
  real/verification/          contact sheets used to check the ground truth
  build_real_eval.py          builds the evaluation split from the photographs
  synthetic/manifest.jsonl    descriptor of the 6000-sample synthetic pool
  synthetic/dataset_info.json generation parameters

results/                      every raw ablation file, plus PAPER_TABLES.md
results/replay/               recorded generations, replay rows, statistics (real split)
figures/                      paper figures and the script that regenerates them
notebooks/                    Colab notebooks for hosted-GPU runs
examples/                     sample sketches for the demo
```

## Not tracked

| Excluded | Why |
|---|---|
| `data/images/` (~1.2 GB) | Deterministically regenerable with `--seed 0`; the manifest is tracked |
| Model weights | Fetched from Hugging Face at runtime |
| Literature PDFs | Third-party copyrighted material |

---

## Licence

Code under the MIT Licence (`LICENSE`); benchmark images, manifests, and ground-truth
models under CC BY 4.0.

## Citation

See `CITATION.cff`.
