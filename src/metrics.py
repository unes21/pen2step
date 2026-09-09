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

def evaluate(pred_step: str, gt_step: str, n_points: int = 4000) -> dict:
    """İki STEP dosyasını karşılaştır → metrik sözlüğü."""
    out = {
        "step_valid": False,
        "chamfer_mm": None,
        "chamfer_norm": None,
        "dim_error": None,
        "volume_error": None,
        "fscore": None,
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


def _main():
    ap = argparse.ArgumentParser(description="İki STEP dosyasını karşılaştır.")
    ap.add_argument("pred", help="Tahmin edilen .step")
    ap.add_argument("gt", help="Ground-truth .step")
    args = ap.parse_args()
    res = evaluate(args.pred, args.gt)
    print("\nMetrikler:")
    for k, v in res.items():
        print(f"  {k:18s}: {v}")


if __name__ == "__main__":
    _main()
