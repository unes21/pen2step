"""CadQuery katı modeli → el-çizimi stilinde teknik eskiz.

Boru hattı:
    1. CadQuery'nin SVG dışa aktarıcısı ile izometrik projeksiyon + gizli-çizgi
       kaldırma (hidden line removal) yapılır → temiz teknik çizgi resmi.
    2. svglib + reportlab ile SVG raster (PNG/PIL) görüntüye çevrilir
       (Windows-dostu; cairo gerektirmez).
    3. Elastik deformasyon + hafif afin sarsıntı + çizgi gürültüsü ile
       "el çizimi" estetiği uygulanır (sim-to-real domain augmentation).

Bu, "sentetik eskiz + el-çizimi artırımı" stratejisidir; eğitim için büyük
ölçekli veri sağlar. Gerçek el çizimlerinden oluşan küçük test seti ile
birlikte kullanılır (bkz. PAPER_PLAN.md, domain gap tartışması).
"""

from __future__ import annotations

import io
import os
import math
import random
import tempfile

import numpy as np
from PIL import Image

import cadquery as cq

# SVG → raster (Windows-dostu, cairo'suz)
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

try:
    from scipy.ndimage import gaussian_filter, map_coordinates
    _HAVE_SCIPY = True
except Exception:  # pragma: no cover
    _HAVE_SCIPY = False


# Birkaç izometrik-benzeri bakış yönü (veri çeşitliliği için)
_PROJECTIONS = [
    (1, 1, 1),
    (1, -1, 1),
    (-1, 1, 1),
    (1, 1, 0.6),
    (1.2, 0.8, 1),
    (0.8, 1.2, 1),
]


def _shape_of(result):
    """Workplane veya Shape kabul et, dışa aktarılabilir nesneyi döndür."""
    return result


def export_svg(result, path: str, rng: random.Random, size: int = 600):
    """Katı modeli teknik çizgi SVG'sine aktar."""
    pdir = rng.choice(_PROJECTIONS)
    stroke = round(rng.uniform(0.5, 1.1), 2)
    show_hidden = rng.random() < 0.25  # bazen gizli çizgileri de göster
    opts = {
        "width": size,
        "height": size,
        "marginLeft": 30,
        "marginTop": 30,
        "showAxes": False,
        "projectionDir": pdir,
        "strokeWidth": stroke,
        "strokeColor": (0, 0, 0),
        "hiddenColor": (0, 0, 0),
        "showHidden": show_hidden,
    }
    cq.exporters.export(result, path, exportType="SVG", opt=opts)


def svg_to_pil(svg_path: str, target: int = 512) -> Image.Image:
    """SVG dosyasını beyaz zeminli gri-tonlu PIL görüntüsüne çevir."""
    drawing = svg2rlg(svg_path)
    if drawing is None:
        raise RuntimeError(f"SVG ayrıştırılamadı: {svg_path}")

    # Hedef piksel boyutuna ölçekle
    w = max(drawing.width, 1.0)
    h = max(drawing.height, 1.0)
    scale = float(target) / max(w, h)
    drawing.width = w * scale
    drawing.height = h * scale
    drawing.scale(scale, scale)

    # reportlab → PIL (sürüm farklarına karşı iki yol)
    try:
        pil = renderPM.drawToPIL(drawing, dpi=72, bg=0xFFFFFF)
    except Exception:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tmp_png = tf.name
        try:
            renderPM.drawToFile(drawing, tmp_png, fmt="PNG", bg=0xFFFFFF)
            pil = Image.open(tmp_png).convert("RGB")
            pil.load()
        finally:
            try:
                os.remove(tmp_png)
            except OSError:
                pass

    return pil.convert("L")


def _pad_square(img: Image.Image, size: int, fill: int = 255) -> Image.Image:
    """Görüntüyü orantısını koruyarak kareye doldur ve boyutlandır."""
    img.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("L", (size, size), fill)
    ox = (size - img.width) // 2
    oy = (size - img.height) // 2
    canvas.paste(img, (ox, oy))
    return canvas


def _elastic(arr: np.ndarray, alpha: float, sigma: float,
             rng: random.Random) -> np.ndarray:
    """Elastik deformasyon — çizgilere el-titremesi görünümü kazandırır."""
    if not _HAVE_SCIPY:
        return arr
    rs = np.random.RandomState(rng.randint(0, 2**31 - 1))
    shape = arr.shape
    dx = gaussian_filter((rs.rand(*shape) * 2 - 1), sigma, mode="constant") * alpha
    dy = gaussian_filter((rs.rand(*shape) * 2 - 1), sigma, mode="constant") * alpha
    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    indices = (np.reshape(y + dy, (-1, 1)), np.reshape(x + dx, (-1, 1)))
    out = map_coordinates(arr, indices, order=1, mode="constant", cval=255.0)
    return out.reshape(shape)


def _hand_drawn(img: Image.Image, rng: random.Random) -> Image.Image:
    """El çizimi artırımları: elastik wobble + hafif döndürme + gürültü."""
    arr = np.asarray(img, dtype=np.float32)

    # 1) Elastik wobble
    alpha = rng.uniform(10.0, 26.0)
    sigma = rng.uniform(6.0, 11.0)
    arr = _elastic(arr, alpha, sigma, rng)

    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="L")

    # 2) Küçük döndürme (çizim hizası mükemmel değildir)
    angle = rng.uniform(-4.0, 4.0)
    img = img.rotate(angle, resample=Image.BILINEAR, fillcolor=255, expand=False)

    # 3) Hafif gürültü + kontrast (kağıt/kalem dokusu hissi)
    arr = np.asarray(img, dtype=np.float32)
    noise = np.random.RandomState(rng.randint(0, 2**31 - 1)).normal(
        0, rng.uniform(2.0, 7.0), arr.shape
    )
    arr = np.clip(arr + noise, 0, 255)

    return Image.fromarray(arr.astype(np.uint8), mode="L")


def render_sketch(result, rng: random.Random, size: int = 512,
                  hand_drawn: bool = True) -> Image.Image:
    """Katı modeli el-çizimi stilinde RGB eskize çevir (model girdisi formatı)."""
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
        svg_path = tf.name
    try:
        export_svg(result, svg_path, rng, size=max(600, size))
        gray = svg_to_pil(svg_path, target=int(size * 1.15))
    finally:
        try:
            os.remove(svg_path)
        except OSError:
            pass

    gray = _pad_square(gray, size)
    if hand_drawn:
        gray = _hand_drawn(gray, rng)
        gray = _pad_square(gray, size)  # döndürme sonrası yeniden ortala

    return gray.convert("RGB")


# ── Ortografik (standart) görünümler ─────────────────────────────────────────
# Mühendislik çiziminin üç temel görünümü. Sonda ile doğrulanmış yönler:
#   ÜST  (0,0,1)  → XY düzlemi (delik/desen burada görünür)
#   ÖN   (0,1,0)  → XZ düzlemi
#   YAN  (1,0,0)  → YZ düzlemi
STANDARD_VIEWS = [
    ("ON",  (0, 1, 0)),
    ("UST", (0, 0, 1)),
    ("YAN", (1, 0, 0)),
]


def export_svg_view(result, path: str, projection, size: int = 480,
                    stroke: float = 0.8, show_hidden: bool = False):
    """Sabit (deterministik) bir projeksiyon yönünden teknik çizgi SVG'si."""
    opts = {
        "width": size,
        "height": size,
        "marginLeft": 25,
        "marginTop": 25,
        "showAxes": False,
        "projectionDir": projection,
        "strokeWidth": stroke,
        "strokeColor": (0, 0, 0),
        "hiddenColor": (0, 0, 0),
        "showHidden": show_hidden,
    }
    cq.exporters.export(result, path, exportType="SVG", opt=opts)


def render_view(result, projection, size: int = 420,
                hand_drawn: bool = False, rng: random.Random | None = None
                ) -> Image.Image:
    """Katı modeli verilen yönden gri-tonlu görünüme çevir (anotasyonsuz)."""
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
        svg_path = tf.name
    try:
        export_svg_view(result, svg_path, projection, size=max(480, size))
        gray = svg_to_pil(svg_path, target=int(size * 1.1))
    finally:
        try:
            os.remove(svg_path)
        except OSError:
            pass

    gray = _pad_square(gray, size)
    if hand_drawn and rng is not None:
        gray = _hand_drawn(gray, rng)
        gray = _pad_square(gray, size)
    return gray
