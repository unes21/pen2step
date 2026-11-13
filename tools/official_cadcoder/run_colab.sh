#!/usr/bin/env bash
# Official CAD-Coder evaluation, unchanged, on its own 100-sample test subset and on the 27 Pen2STEP sheets.
# Colab, one A100. Everything is written to /content/official_eval (zipped at the end).
#   bash /content/pen2step/tools/official_cadcoder/run_colab.sh
set -u
unset UV_SYSTEM_PYTHON
OUT=/content/official_eval
mkdir -p "$OUT"
exec > >(tee -a "$OUT/run.log") 2>&1
cd /content
pip -q install uv
[ -d CAD-Coder ] || git clone -q https://github.com/anniedoris/CAD-Coder
[ -d pen2step ] || git clone -q -b equipment https://github.com/unes21/pen2step
P2S=/content/pen2step/tools/official_cadcoder
cd /content/CAD-Coder
git rev-parse HEAD > "$OUT/cadcoder_commit.txt"
git -C /content/pen2step rev-parse HEAD > "$OUT/pen2step_commit.txt"

# llava environment as in the CAD-Coder README (Python 3.10, pinned versions from pyproject.toml)
[ -d /content/venv_llava ] || uv venv -q -p 3.10 /content/venv_llava
source /content/venv_llava/bin/activate
uv pip install -q --python /content/venv_llava/bin/python -e . datasets "peft==0.10.0" protobuf || { echo "llava install failed"; exit 1; }
python -c "import sys;assert sys.version_info[:2]==(3,10),sys.version" || exit 1
python -c "import torch,transformers;print('llava env: torch',torch.__version__,'transformers',transformers.__version__,'cuda',torch.version.cuda,torch.cuda.get_device_name(0))" | tee "$OUT/environment_llava.txt"
uv pip freeze --python /content/venv_llava/bin/python > "$OUT/pip_freeze_llava.txt"
nvidia-smi > "$OUT/nvidia_smi.txt"

python "$P2S/make_questions.py" --pen2step /content/pen2step
for SPLIT in cadquery_test_data_subset100 pen2step_27; do
  M=inference/inference_results/CAD-Coder/$SPLIT/merge.jsonl
  N=$(wc -l < "inference/$SPLIT.jsonl")
  if [ -f "$M" ] && [ "$(wc -l < "$M")" -eq "$N" ]; then echo "$SPLIT already generated ($N)"; continue; fi
  start=$(date +%s)
  bash ./scripts/v1_5/eval/test_gencadcode.sh "CADCODER/CAD-Coder" "$SPLIT"
  echo "$SPLIT generation seconds: $(( $(date +%s) - start ))"
done
python "$P2S/count_tokens.py" inference/inference_results/CAD-Coder/cadquery_test_data_subset100 inference/inference_results/CAD-Coder/pen2step_27 | tee "$OUT/token_summary.txt"
deactivate
# Save the raw generations before the CPU-heavy CAD step.
mkdir -p "$OUT/raw"
for SPLIT in cadquery_test_data_subset100 pen2step_27; do
  cp "inference/inference_results/CAD-Coder/$SPLIT/merge.jsonl" "$OUT/raw/${SPLIT}_merge.jsonl"
  cp "inference/inference_results/CAD-Coder/$SPLIT/tokens.jsonl" "$OUT/raw/${SPLIT}_tokens.jsonl"
done
cp inference/pen2step_27.jsonl "$OUT/raw/"
(cd /content && rm -f official_eval_raw.zip && zip -qr official_eval_raw.zip official_eval && echo "raw zip saved")

# cad_iou environment (CadQuery from pip instead of conda-forge)
[ -d /content/venv_cad ] || uv venv -q -p 3.10 /content/venv_cad
source /content/venv_cad/bin/activate
uv pip install -q --python /content/venv_cad/bin/python cadquery trimesh plyfile pandas tqdm scipy || { echo "cad install failed"; exit 1; }
python -c "import cadquery,OCP;print('cad env: cadquery',cadquery.__version__)" | tee "$OUT/environment_cad.txt"
uv pip freeze --python /content/venv_cad/bin/python > "$OUT/pip_freeze_cad.txt"
# The official script runs every generated program with "python" and no time limit; a program that never
# finishes would stall the run, so "python" on PATH is wrapped with a 120 s limit (a timed-out program
# exits non-zero and counts as invalid, as any failing program does). Sequential mode (the script's own
# default without --parallel) keeps the notebook server responsive.
mkdir -p /content/pywrap
printf '#!/bin/bash
exec timeout 120 /content/venv_cad/bin/python "$@"
' > /content/pywrap/python
chmod +x /content/pywrap/python
for SPLIT in cadquery_test_data_subset100 pen2step_27; do
  PATH=/content/pywrap:$PATH nice -n 10 /content/venv_cad/bin/python scripts/generate_model_cad.py --dataset_name "$SPLIT" --model_tested CADCODER/CAD-Coder --code_language cadquery --pc_reps 3 > "$OUT/generate_$SPLIT.log" 2>&1
  echo "== $SPLIT"; cat "inference/inference_results/CAD-Coder/$SPLIT/cad_gen_results.txt"
done
python scripts/compute_iou.py --model_path CADCoder/CAD-Coder --test_set_name cadquery_test_data_subset100 > "$OUT/iou_subset100.log" 2>&1 \
  && cat inference/inference_results/CAD-Coder/cadquery_test_data_subset100/cad_iou_results.txt
deactivate

cp inference/pen2step_27.jsonl "$OUT/"
cp -r inference/inference_results/CAD-Coder "$OUT/inference_results"
rm -rf "$OUT"/inference_results/*/model_point_cloud_* "$OUT"/inference_results/*/model_stl
cd /content && rm -f official_eval.zip && zip -qr official_eval.zip official_eval && ls -la official_eval.zip
echo ALL_DONE
