"""Write the 27 Pen2STEP sheets as a question file of the official CAD-Coder evaluation.

Run from the root of a CAD-Coder checkout. The official script reads images from
./inference/test100_images, so the 27 images are copied there with a "p2s_" prefix (none of the
official file names starts with it). The instruction is copied verbatim from the official
question file, so the prompt is exactly the one the official evaluation uses.

    python <pen2step>/tools/official_cadcoder/make_questions.py --pen2step <pen2step>
"""
import argparse
import json
import shutil
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--pen2step", required=True)
ap.add_argument("--name", default="pen2step_27")
a = ap.parse_args()
p2s = Path(a.pen2step)
inf = Path("inference")
official = [json.loads(l) for l in (inf / "cadquery_test_data_subset100.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
texts = {q["text"] for q in official}
assert len(texts) == 1, texts
text = texts.pop()
out = []
for split in ("real", "case_study"):
    data = p2s / "benchmark" / split
    for line in (data / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        src = data / rec["image_mv"]
        name = "p2s_" + src.name
        dst = inf / "test100_images" / name
        assert not dst.exists() or dst.read_bytes() == src.read_bytes(), dst
        shutil.copyfile(src, dst)
        out.append({"question_id": rec["id"], "image": name, "text": text, "category": "default",
                    "ground_truth": rec["code"]})
assert len(out) == 27, len(out)
(inf / f"{a.name}.jsonl").write_text("".join(json.dumps(q) + "\n" for q in out), encoding="utf-8")
print(f"wrote inference/{a.name}.jsonl with {len(out)} questions; prompt: {text!r}")
