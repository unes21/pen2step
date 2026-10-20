"""CAD-spesifik değerlendirme metrikleri.

Bu metrikler makalenin 3. katkısıdır: el-çizimi → STEP problemi için
standartlaşmış bir değerlendirme protokolü literatürde yoktur.

Metrikler:
    STEP Geçerlilik Oranı (SVR) : üretilen kod açılabilir geçerli bir katı
                                  STEP veriyor mu? (compile + topoloji kontrolü)
    Chamfer Mesafesi (mm)       : üretilen yüzey ↔ ground-truth yüzey
    Boyut Hatası                : sınırlayıcı kutu (bbox) boyutlarının
                                  bağıl hatası — boyut-farkındalığın ölçütü
    Hacim Hatası                : bağıl hacim farkı
    IoU (voksel)                : hizalanmış katıların hacimsel örtüşmesi

Kullanım (CLI):
    python -m src.metrics pred.step gt.step
"""

from __future__ import annotations

import sys
import argparse

import numpy as np

import cadquery as cq

try:
    from scipy.spatial import cKDTree
    _HAVE_KDTREE = True
except Exception:  # pragma: no cover
    _HAVE_KDTREE = False


# ── Yükleme / geçerlilik ─────────────────────────────────────────────────────

def load_shape(path: str):
    """STEP dosyasını CadQuery Shape olarak yükle (başarısızsa None)."""
    try:
        wp = cq.importers.importStep(str(path))
        return wp.val()
    except Exception:
        return None


def step_is_valid(path: str) -> bool:
    """STEP açılabiliyor ve en az bir geçerli katı içeriyor mu?"""
    shp = load_shape(path)
    if shp is None:
        return False
    try:
        if not shp.isValid():
            return False
        # Hacmi pozitif bir katı olmalı
        return shp.Volume() > 1e-6
    except Exception:
        return False


# ── Yüzey örnekleme ──────────────────────────────────────────────────────────

def _as_shape(obj):
    return obj.val() if hasattr(obj, "val") else obj


def sample_surface(shape, n_points: int = 4000, tol: float = 0.2,
                   seed: int = 0) -> np.ndarray:
    """Katının yüzeyinden alan-ağırlıklı nokta bulutu örnekle (Nx3)."""
    shape = _as_shape(shape)
    verts, tris = shape.tessellate(tol)
    v = np.array([[p.x, p.y, p.z] for p in verts], dtype=np.float64)
    t = np.array(tris, dtype=np.int64)
    if len(t) == 0:
        return v

    a, b, c = v[t[:, 0]], v[t[:, 1]], v[t[:, 2]]
    areas = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    total = areas.sum()
    if total <= 0:
        return v
    probs = areas / total

    rs = np.random.RandomState(seed)
    idx = rs.choice(len(t), size=n_points, p=probs)
    u = rs.rand(n_points, 1)
    w = rs.rand(n_points, 1)
    over = (u + w) > 1.0
    u[over] = 1.0 - u[over]
    w[over] = 1.0 - w[over]
    pts = a[idx] + u * (b[idx] - a[idx]) + w * (c[idx] - a[idx])
    return pts


# ── Hizalama ─────────────────────────────────────────────────────────────────

def _center(pts: np.ndarray) -> np.ndarray:
    return pts - pts.mean(axis=0, keepdims=True)


# Küpün 24 uygun (determinant=+1, yansımasız) dönme rotasyonu — eksen
# permütasyonları + işaret kombinasyonları. Hakem yanıtı (A3): metrikler
# poza duyarlı; tahmin edilen katının GT'ye göre hangi eksene "baktığı"
# bilinmiyor (mean-centering konumu düzeltir ama yönelimi düzeltmez).
def _cube_rotations() -> list[np.ndarray]:
    from itertools import permutations, product
    mats = []
    for perm in permutations(range(3)):
        P = np.zeros((3, 3))
        for i, p in enumerate(perm):
            P[i, p] = 1.0
        for signs in product([1, -1], repeat=3):
            R = P * np.array(signs)[:, None]
            if abs(np.linalg.det(R) - 1.0) < 1e-6:  # sadece uygun rotasyonlar (yansıma yok)
                mats.append(R)
    assert len(mats) == 24, f"beklenen 24 rotasyon, bulunan {len(mats)}"
    return mats


_CUBE_ROTATIONS = _cube_rotations()


def align_best_of_24(pred_pts: np.ndarray, gt_pts: np.ndarray):
    """Tahmin nokta bulutunu, 24 eksen-hizalı rotasyon içinden GT'ye en yakın
    olanıyla döndürür (best-of-24 poz hizalama, A3).

    İki nokta kümesi de zaten merkezlenmiş (mean-centered) olmalı. Chamfer
    mesafesini en aza indiren rotasyonu seçer; döndürülmüş tahmin noktalarını
    ve seçilen rotasyon matrisini döndürür.

    Not: bu, tam ICP (iteratif en-yakın-nokta) DEĞİL, ayrık bir arama — eksen
    permütasyonu/işaret belirsizliğini (örn. bir kutunun hangi kenarının
    "uzunluk" sayıldığı) düzeltir, ama serbest açılı yanlış hizalamayı düzeltmez.
    """
    best_R = np.eye(3)
    best_d = chamfer_distance(pred_pts, gt_pts)
    for R in _CUBE_ROTATIONS:
        rotated = pred_pts @ R.T
        d = chamfer_distance(rotated, gt_pts)
        if d < best_d:
            best_d = d
            best_R = R
    return pred_pts @ best_R.T, best_R, best_d


# ── Metrikler ────────────────────────────────────────────────────────────────

def chamfer_distance(p: np.ndarray, q: np.ndarray) -> float:
    """Simetrik Chamfer mesafesi (ortalama en-yakın-komşu, her iki yön)."""
    if _HAVE_KDTREE:
        d1, _ = cKDTree(q).query(p)
        d2, _ = cKDTree(p).query(q)
    else:  # yavaş ama bağımsız yedek
        d1 = np.sqrt(((p[:, None, :] - q[None, :, :]) ** 2).sum(-1)).min(1)
        d2 = np.sqrt(((q[:, None, :] - p[None, :, :]) ** 2).sum(-1)).min(1)
    return float(d1.mean() + d2.mean())


def bbox_dims(shape) -> np.ndarray:
    """Sınırlayıcı kutu boyutları (artan sıralı, ölçeğe göre normalize edilebilir)."""
    bb = _as_shape(shape).BoundingBox()
    return np.sort(np.array([bb.xlen, bb.ylen, bb.zlen], dtype=np.float64))


def dimension_error(pred_shape, gt_shape) -> float:
    """Sıralı bbox boyutlarının ortalama bağıl hatası (boyut-farkındalık ölçütü)."""
    pd = bbox_dims(pred_shape)
    gd = bbox_dims(gt_shape)
    denom = np.clip(gd, 1e-6, None)
    return float(np.mean(np.abs(pd - gd) / denom))


def volume_error(pred_shape, gt_shape) -> float:
    """Bağıl hacim farkı."""
    pv = _as_shape(pred_shape).Volume()
    gv = _as_shape(gt_shape).Volume()
    return float(abs(pv - gv) / max(abs(gv), 1e-6))


def fscore(p: np.ndarray, q: np.ndarray, tau: float) -> float:
    """F-score@τ — 3D rekonstrüksiyonda standart metrik.

    precision = τ içinde gt'ye yakın tahmin noktası oranı
    recall    = τ içinde tahmine yakın gt noktası oranı
    Aynı şekil → ~1.0; farklı şekiller → düşük. (Voksel IoU'dan daha kararlı.)
    """
    if _HAVE_KDTREE:
        d_pq, _ = cKDTree(q).query(p)
        d_qp, _ = cKDTree(p).query(q)
    else:
        d_pq = np.sqrt(((p[:, None, :] - q[None, :, :]) ** 2).sum(-1)).min(1)
        d_qp = np.sqrt(((q[:, None, :] - p[None, :, :]) ** 2).sum(-1)).min(1)
    precision = float((d_pq < tau).mean())
    recall = float((d_qp < tau).mean())
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


# ── Üst seviye değerlendirme ─────────────────────────────────────────────────

def evaluate(pred_step: str, gt_step: str, n_points: int = 4000,
            align: bool = False) -> dict:
    """İki STEP dosyasını karşılaştır → metrik sözlüğü.

    align : True ise Chamfer/F-score, best-of-24 eksen-rotasyonu hizalamasından
            SONRA hesaplanır (A3, hakem yanıtı). DimE ve VolE zaten
            yönelimden bağımsızdır (sıralı bbox / hacim), bu yüzden
            align=True/False ile değişmez — sadece Chamfer ve F etkilenir.
            Geriye dönük uyumluluk için varsayılan False (makalenin ana
            tabloları bu kuralla üretildi); align=True ile yeniden koşmak
            §6 "Pose sensitivity" limitasyonunu doğrudan yanıtlar.
    """
    out = {
        "step_valid": False,
        "chamfer_mm": None,
        "chamfer_norm": None,
        "dim_error": None,
        "volume_error": None,
        "fscore": None,
        "aligned": align,
    }

    pred = load_shape(pred_step)
    gt = load_shape(gt_step)
    if gt is None:
        out["error"] = "ground-truth STEP yüklenemedi"
        return out
    out["step_valid"] = step_is_valid(pred_step)
    if pred is None or not out["step_valid"]:
        return out

    try:
        pp = sample_surface(pred, n_points, seed=1)
        gp = sample_surface(gt, n_points, seed=2)

        cpp, cgp = _center(pp), _center(gp)

        if align:
            cpp, R, _ = align_best_of_24(cpp, cgp)
            out["rotation_applied"] = not np.allclose(R, np.eye(3))

        # Ham (mm) Chamfer — merkezleyerek konum farkını ele (boyut korunur)
        ch_raw = chamfer_distance(cpp, cgp)
        out["chamfer_mm"] = ch_raw

        # Ölçek-normalize Chamfer (gt köşegenine böl) — şekil benzerliği
        diag = float(np.linalg.norm(bbox_dims(gt)))
        out["chamfer_norm"] = ch_raw / max(diag, 1e-6)

        out["dim_error"] = dimension_error(pred, gt)
        out["volume_error"] = volume_error(pred, gt)
        # F-score@τ, τ = gt köşegeninin %2'si (ölçek-uyumlu eşik)
        out["fscore"] = fscore(cpp, cgp, tau=0.02 * max(diag, 1e-6))
    except Exception as exc:  # pragma: no cover
        out["error"] = f"metrik hesaplanamadı: {exc}"

    return out


def aggregate(results: list[dict]) -> dict:
    """Çok sayıda örnek metriğini ortalama özet haline getir."""
    n = len(results)
    valid = [r for r in results if r.get("step_valid")]
    svr = len(valid) / n if n else 0.0

    def _mean(key):
        vals = [r[key] for r in valid if r.get(key) is not None]
        return float(np.mean(vals)) if vals else None

    return {
        "n": n,
        "step_validity_rate": svr,
        "chamfer_mm": _mean("chamfer_mm"),
        "chamfer_norm": _mean("chamfer_norm"),
        "dim_error": _mean("dim_error"),
        "volume_error": _mean("volume_error"),
        "fscore": _mean("fscore"),
    }


MANIFEST_REQUIRED = {"id": str, "image_mv": str, "family": str, "oem_no": str, "drawer_role": str,
                     "n_dims_annotated": int, "annotated_dims": list, "drawer_confidence": int,
                     "sketch_minutes": (int, float), "has_dims": bool, "split": str, "code": str}
DRAWER_ROLES = {"mechanic", "engineer", "student"}
CEILING_MIN = 0.85
SECOND_CHECK_TOL = 0.02


def selfcheck(split: str) -> int:
    """Checks every ground-truth model of a benchmark split (work package IP4).

    For each manifest row: required fields and value ranges; the CadQuery code builds a solid with
    positive volume; the committed benchmark/<split>/gt/<id>.step matches the code (volume within
    0.1%); the self F-score ceiling (two independent surface samples) is at least 0.85; and the
    independent second check (gt_second_check.csv) lists at least three dimensions, each within 2%.
    Returns the number of failed parts (0 = pass).
    """
    import csv
    import json
    import tempfile
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent / "benchmark" / split
    man = root / "manifest.jsonl"
    rows = [json.loads(l) for l in man.read_text(encoding="utf-8").splitlines() if l.strip()] if man.exists() else []
    if not rows:
        print(f"{man}: no parts yet")
        return 0
    checks = {}
    sc = root / "gt_second_check.csv"
    if sc.exists():
        with sc.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                checks.setdefault(r["part_id"], []).append(r)
    failed, tmp = 0, Path(tempfile.mkdtemp())
    seen = set()
    for m in rows:
        pid, errs = m.get("id", "?"), []
        if pid in seen:
            errs.append("duplicate id")
        seen.add(pid)
        for k, t in MANIFEST_REQUIRED.items():
            if k not in m:
                errs.append(f"missing {k}")
            elif not isinstance(m[k], t) or (t is int and isinstance(m[k], bool)):
                errs.append(f"{k} has type {type(m[k]).__name__}")
        if m.get("drawer_role") not in DRAWER_ROLES:
            errs.append(f"drawer_role {m.get('drawer_role')!r} not in {sorted(DRAWER_ROLES)}")
        if isinstance(m.get("n_dims_annotated"), int) and m["n_dims_annotated"] < 3:
            errs.append("fewer than 3 annotated dimensions")
        if isinstance(m.get("annotated_dims"), list) and len(m["annotated_dims"]) != m.get("n_dims_annotated"):
            errs.append("len(annotated_dims) != n_dims_annotated")
        if isinstance(m.get("drawer_confidence"), int) and not 1 <= m["drawer_confidence"] <= 5:
            errs.append("drawer_confidence outside 1..5")
        if m.get("split") != split:
            errs.append(f"split {m.get('split')!r} != {split!r}")
        if m.get("image_mv") and not (root / m["image_mv"]).exists():
            errs.append(f"image {m['image_mv']} not found")
        vol, ceil = None, None
        if isinstance(m.get("code"), str) and m["code"].strip():
            try:
                ns = {}
                exec(m["code"], ns)
                built = tmp / f"{pid}.step"
                cq.exporters.export(ns["result"], str(built))
                shape = load_shape(str(built))
                vol = shape.Volume()
                if not vol > 0:
                    errs.append("non-positive volume")
                committed = root / "gt" / f"{pid}.step"
                if not committed.exists():
                    errs.append(f"gt/{pid}.step not committed")
                else:
                    cv = load_shape(str(committed)).Volume()
                    if abs(cv - vol) > 1e-3 * max(vol, 1e-9):
                        errs.append(f"gt/{pid}.step volume {cv:.1f} != code volume {vol:.1f}")
                if not (root / "gt" / f"{pid}.py").exists():
                    errs.append(f"gt/{pid}.py not committed")
                a = _center(sample_surface(shape, 4000, seed=1))
                b = _center(sample_surface(shape, 4000, seed=2))
                ceil = fscore(a, b, 0.02 * float(np.linalg.norm(bbox_dims(shape))))
                if ceil < CEILING_MIN:
                    errs.append(f"self ceiling {ceil:.3f} < {CEILING_MIN}")
            except Exception as exc:  # noqa: BLE001 - report every failure, do not stop at the first
                errs.append(f"code failed: {exc!r}")
        c = checks.get(pid, [])
        if len(c) < 3:
            errs.append(f"second check lists {len(c)} dimensions (need 3)")
        for r in c:
            try:
                d = abs(float(r["measured_mm"]) - float(r["model_mm"])) / float(r["measured_mm"])
            except (KeyError, ValueError, ZeroDivisionError):
                errs.append(f"second check row unreadable: {r}")
                continue
            if d > SECOND_CHECK_TOL:
                errs.append(f"second check {r.get('dim_name')}: {100 * d:.1f}% > 2%")
        status = "ok  " if not errs else "FAIL"
        failed += bool(errs)
        v = f"{vol:.0f}" if vol is not None else "-"
        cs = f"{ceil:.3f}" if ceil is not None else "-"
        print(f"{status} {pid:12s} volume {v:>10s} mm3  ceiling {cs}  " + "; ".join(errs))
    print(f"{len(rows) - failed}/{len(rows)} parts pass")
    return failed


def _main():
    ap = argparse.ArgumentParser(description="İki STEP dosyasını karşılaştır, ya da bir bölümün GT modellerini denetle.")
    ap.add_argument("pred", nargs="?", help="Tahmin edilen .step")
    ap.add_argument("gt", nargs="?", help="Ground-truth .step")
    ap.add_argument("--split", default=None, help="benchmark split for --selfcheck (e.g. equipment)")
    ap.add_argument("--selfcheck", action="store_true", help="check every ground-truth model of --split")
    args = ap.parse_args()
    if args.selfcheck:
        sys.exit(1 if selfcheck(args.split or "equipment") else 0)
    if not (args.pred and args.gt):
        ap.error("pred and gt are required unless --selfcheck is given")
    res = evaluate(args.pred, args.gt)
    print("\nMetrikler:")
    for k, v in res.items():
        print(f"  {k:18s}: {v}")


if __name__ == "__main__":
    _main()
