"""Pen2STEP — frozen VLM çevresinde eğitimsiz (training-free) sketch→CAD framework.

Boru hattı:
    görseller (1..N)
      → çoklu-görünüm kompozisyonu          (multi-view füzyon sütunu)
      → OCR ile boyut çıkarımı + enjeksiyon  (boyut-farkındalık sütunu)
      → frozen VLM ile N aday kod üret
      → AST kod onarımı                      (sağlamlık)
      → izole çalıştırma + STEP              (yürütme-güdümlü seçim)
      → boyut recovery (normalize → mm)
      → en iyi geçerli adayı seç

`generate_fn` takılabilir (pluggable) — böylece model olmadan mock ile test
edilebilir. Gerçek kullanımda app.py / run_baselines bunu bella'ya bağlar.
"""

from __future__ import annotations

import os
import sys
import time
import subprocess
from dataclasses import dataclass, field

from PIL import Image

from src.prompt import build_prompt
from src.code_repair import repair, split_after_assistant, strip_markdown
from src.multiview import compose_user_images
from src import dimensions as dim_mod


@dataclass
class FrameworkConfig:
    n_candidates: int = 3            # üretilecek aday sayısı
    use_dimensions: bool = True      # OCR ile boyut enjeksiyonu
    use_repair: bool = True          # AST kod onarımı
    use_multiview_prompt: bool = True
    scale_recover: bool = True       # normalize çıktıyı mm'e ölçekle
    canonical_size: float = 100.0    # boyut okunamazsa en uzun kenar bu mm olur
    normalized_threshold: float = 10.0  # maxdim < bu → normalize kabul et
    remove_base_plate: bool = True   # CADCoder'ın eklediği ince taban levhasını ayıkla
    timeout: int = 60
    temperature: float = 0.4


# Model kodundan önce çalışır: dejenere yayları (eşdoğrusal 3 nokta → OCC hatası)
# düz çizgiye düşürür. Yuvarlatılmış köşelerde sık görülen hatayı kurtarır.
_SAFE_HEADER = (
    "import cadquery as cq\n"
    "_o_tpa = cq.Workplane.threePointArc\n"
    "def _safe_tpa(self, p1, p2, forConstruction=False):\n"
    "    try:\n"
    "        return _o_tpa(self, p1, p2, forConstruction)\n"
    "    except Exception:\n"
    "        return self.lineTo(p2[0], p2[1], forConstruction)\n"
    "cq.Workplane.threePointArc = _safe_tpa\n"
)


def _build_footer(step_path: str, target_max, canonical: float,
                  recover: bool, threshold: float, remove_base: bool = True) -> str:
    cands = ["result", "solid", "shape", "part", "body", "model",
             "compound", "obj", "cad_result"]
    target_repr = "None" if target_max is None else repr(float(target_max))
    return f"""
# ── STEP export + boyut recovery (framework) ──────────────────────────────
import cadquery as cq
import re as _re

# CADCoder bazen parçanın altına ince bir "ayak izi" levhası ekler; onu ayıkla.
# Model her katıyı solid0, solid1... adıyla bıraktığı için ayrı ayrı incelenebilir.
if {remove_base}:
    _ss = []
    for _n in sorted([k for k in list(globals()) if _re.match(r'solid\\d+$', k)],
                     key=lambda s: int(s[5:])):
        try:
            _o = globals()[_n]
            _sv = _o.val() if hasattr(_o, "val") else _o
            _bb0 = _sv.BoundingBox()
            _e = sorted([_bb0.xlen, _bb0.ylen, _bb0.zlen])
            _ss.append((_n, _sv, _e[0], _e[1] * _e[2]))   # (ad, katı, kalınlık, ayakizi)
        except Exception:
            pass
    if len(_ss) >= 2:
        _mth = max(s[2] for s in _ss)
        _mft = max(s[3] for s in _ss)
        # taban = en ince boyutu çok küçük VE ayak izi en büyüklerden biri
        _bases = [s for s in _ss if s[2] < 0.35 * _mth and s[3] > 0.6 * _mft]
        _keep = [s for s in _ss if s not in _bases]
        if _bases and _keep:
            _r = _keep[0][1]
            for _k in _keep[1:]:
                try:
                    _r = _r.fuse(_k[1])
                except Exception:
                    pass
            try:                          # parçayı orijine ortala (taban gidince köşede kalmasın)
                _c = _r.BoundingBox().center
                _r = _r.translate((-_c.x, -_c.y, -_c.z))
            except Exception:
                pass
            globals()['result'] = _r     # aşağıdaki _final seçimi bunu alır
            print("BASE_REMOVED " + ",".join(b[0] for b in _bases))

_cands = {cands}
_final = next((globals()[n] for n in _cands if n in globals()), None)
if _final is None:
    raise NameError("Uretilen kodda 3D nesne bulunamadi: " + str(_cands))
_shp = _final.val() if hasattr(_final, "val") else _final
_bb = _shp.BoundingBox()
_maxd = max(_bb.xlen, _bb.ylen, _bb.zlen)
if {recover} and _maxd < {threshold} and _maxd > 1e-9:
    _goal = {target_repr} if {target_repr} is not None else {canonical}
    _shp = _shp.scale(_goal / _maxd)
_b2 = _shp.BoundingBox()
print("BBOX %.4f %.4f %.4f" % (_b2.xlen, _b2.ylen, _b2.zlen))
cq.exporters.export(_shp, r"{step_path}")
"""


def execute(code: str, py_path: str, step_path: str, cfg: FrameworkConfig,
            target_max=None):
    """Kodu izole subprocess'te çalıştır → (ok, err, bbox|None)."""
    footer = _build_footer(step_path, target_max, cfg.canonical_size,
                           cfg.scale_recover, cfg.normalized_threshold,
                           cfg.remove_base_plate)
    # Gövdeyi try/except'e sar: kesik (truncated) son satır hata verirse, o ana
    # kadar kurulan geçerli `solid` kullanılır (footer onu bulur).
    indented = "\n".join("    " + ln for ln in code.splitlines())
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(_SAFE_HEADER)
        f.write("try:\n")
        f.write(indented)
        f.write("\nexcept Exception as _e:\n    print('PARTIAL_EXEC', repr(_e))\n")
        f.write(footer)

    try:
        proc = subprocess.run([sys.executable, py_path], capture_output=True,
                              text=True, timeout=cfg.timeout)
    except subprocess.TimeoutExpired:
        return False, f"timeout ({cfg.timeout}s)", None

    if proc.returncode != 0 or not os.path.exists(step_path):
        return False, (proc.stderr or proc.stdout or "bilinmeyen hata").strip(), None

    bbox = None
    for line in (proc.stdout or "").splitlines():
        if line.startswith("BBOX"):
            try:
                bbox = tuple(float(v) for v in line.split()[1:4])
            except Exception:
                pass
    return True, None, bbox


def _clean_only(raw: str) -> str:
    return strip_markdown(split_after_assistant(raw))


def sketch_to_cad(images, generate_fn, cfg: FrameworkConfig, work_dir: str,
                  ocr_fn=None):
    """Framework ana giriş noktası.

    images      : list[PIL.Image]  (tek veya çok görünüm)
    generate_fn : (composed_image, prompt, sample_idx) -> ham_metin
    ocr_fn      : (composed_image) -> list[float]  (None → dimensions.extract)
    work_dir    : geçici .py/.step dosyaları için klasör

    Döner: sonuç sözlüğü (composed, dims, candidates, best, ...).
    """
    os.makedirs(work_dir, exist_ok=True)
    log = {"steps": []}

    # 1) Kompozisyon
    if len(images) > 1:
        composed = compose_user_images(images)
        multiview = True
    else:
        composed = images[0].convert("RGB")
        multiview = cfg.use_multiview_prompt  # tek görsel zaten çok-görünüm sayfası olabilir
    log["steps"].append(f"compose: {len(images)} görsel → multiview={multiview}")

    # 2) Boyut OCR + enjeksiyon
    dims = []
    if cfg.use_dimensions:
        try:
            dims = ocr_fn(composed) if ocr_fn else dim_mod.extract_dimensions(composed)
        except Exception as exc:
            log["steps"].append(f"ocr hata: {exc}")
        log["steps"].append(f"ocr boyutlar: {dims}")
    hint = dim_mod.build_dimension_hint(dims) if dims else ""
    target_max = max(dims) if dims else None

    prompt = build_prompt(dim_hint=hint, multiview=multiview)

    # 3) N aday üret → onar → çalıştır
    candidates = []
    for i in range(cfg.n_candidates):
        t0 = time.time()
        try:
            raw = generate_fn(composed, prompt, i)
        except Exception as exc:
            log["steps"].append(f"aday {i}: üretim hatası {exc}")
            continue

        code, applied = repair(raw) if cfg.use_repair else (_clean_only(raw), [])
        py_path = os.path.join(work_dir, f"cand_{i}.py")
        step_path = os.path.join(work_dir, f"cand_{i}.step")
        ok, err, bbox = execute(code, py_path, step_path, cfg, target_max=target_max)

        cand = {
            "idx": i, "code": code, "repairs": applied, "valid": ok,
            "error": err, "bbox": bbox, "step": step_path if ok else None,
            "gen_time": round(time.time() - t0, 1),
        }
        candidates.append(cand)
        log["steps"].append(
            f"aday {i}: valid={ok} repairs={applied} bbox={bbox} ({cand['gen_time']}s)"
        )

    # 4) En iyi geçerli adayı seç
    valid = [c for c in candidates if c["valid"]]
    best = None
    if valid:
        if dims:
            # OCR boyutlarına en yakın bbox'a sahip adayı seç (tüm boyut seti uyumu)
            tgt = sorted(dims)

            def dim_score(c):
                b = sorted(c["bbox"]) if c["bbox"] else [0.0, 0.0, 0.0]
                n = min(len(b), len(tgt))
                bb, tt = b[-n:], tgt[-n:]  # en büyük n boyutu eşleştir
                return sum(abs(bi - ti) / max(ti, 1e-6) for bi, ti in zip(bb, tt))
            best = min(valid, key=dim_score)
        else:
            best = valid[0]

    return {
        "composed": composed,
        "multiview": multiview,
        "dims": dims,
        "hint": hint,
        "prompt": prompt,
        "candidates": candidates,
        "best": best,
        "n_valid": len(valid),
        "log": log,
    }
