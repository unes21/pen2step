"""Çoklu görünüm (multi-view) kompozisyonu ve boyut-anotasyonlu eskiz üretimi.

İki kullanım:
  1. SENTETİK ÜRETİM: bir katı modelden 3 ortografik görünüm (ön/üst/yan) üret,
     her görünüme gerçek mm boyutlarını yaz, tek bir teknik çizim sayfası olarak
     birleştir. Ground-truth boyutlar bilindiği için OCR ve boyut-farkında
     üretim DEĞERLENDİRİLEBİLİR.
  2. KULLANICI GİRDİSİ: kullanıcının yüklediği birden çok fotoğrafı (parçanın
     farklı açıları) tek bir etiketli sayfaya birleştir → frozen VLM'e ver.

Bu, framework'ün "çoklu görünüm füzyonu" ve "boyut anotasyonu" sütunlarının
temelini oluşturur (bkz. PAPER_PLAN.md).
"""

from __future__ import annotations

import random

from PIL import Image, ImageDraw, ImageFont

from src.render import render_view, STANDARD_VIEWS


# ── Yazı tipi ────────────────────────────────────────────────────────────────

def _font(size: int):
    for name in ("arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


# ── Görünüm → hangi mm boyutu yatay/dikey ────────────────────────────────────
# Sonda ile doğrulanmış: ON=(0,1,0) X-Z; UST=(0,0,1) X-Y; YAN=(1,0,0) Y-Z
def _view_dims(label: str, xl: float, yl: float, zl: float):
    return {
        "ON":  (xl, zl),
        "UST": (xl, yl),
        "YAN": (yl, zl),
    }[label]


def bbox_dims(result):
    shp = result.val() if hasattr(result, "val") else result
    bb = shp.BoundingBox()
    return bb.xlen, bb.ylen, bb.zlen


# ── Tek görünümü boyut anotasyonu ile çerçevele ──────────────────────────────

_VIEW_TR = {"ON": "ON", "UST": "UST", "YAN": "YAN"}


def _annotate_panel(view_img: Image.Image, label: str,
                    h_mm: float, v_mm: float) -> Image.Image:
    """Bir görünüm görüntüsünü etiket + yatay/dikey boyut yazısıyla çerçevele.

    Boyut sayıları büyük ve beyaz kutu içinde çizilir → OCR güvenilirliği yüksek.
    """
    s = view_img.size[0]
    pad_l, pad_b, pad_t, pad_r = 88, 64, 36, 26
    W, H = s + pad_l + pad_r, s + pad_b + pad_t
    cell = Image.new("L", (W, H), 255)
    cell.paste(view_img, (pad_l, pad_t))
    d = ImageDraw.Draw(cell)
    f_lab = _font(22)
    f_dim = _font(30)

    # Görünüm etiketi (üst)
    d.text((pad_l, 4), _VIEW_TR.get(label, label), fill=0, font=f_lab)

    x0, y0 = pad_l, pad_t
    x1, y1 = pad_l + s, pad_t + s

    def boxed(cx, cy, txt, font):
        tb = d.textbbox((0, 0), txt, font=font)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        d.rectangle([cx - tw // 2 - 6, cy - th // 2 - 5,
                     cx + tw // 2 + 6, cy + th // 2 + 6], fill=255)
        d.text((cx - tw // 2, cy - th // 2 - tb[1]), txt, fill=0, font=font)

    # Yatay boyut (alt): tanık çizgileri + boyut çizgisi + sayı
    yb = y1 + 34
    d.line([(x0, y1 + 8), (x0, yb + 6)], fill=0, width=1)
    d.line([(x1, y1 + 8), (x1, yb + 6)], fill=0, width=1)
    d.line([(x0, yb), (x1, yb)], fill=0, width=1)
    boxed((x0 + x1) // 2, yb, f"{round(h_mm)}", f_dim)

    # Dikey boyut (sol): tanık çizgileri + boyut çizgisi + sayı (yatay yazı)
    xv = x0 - 42
    d.line([(x0 - 8, y0), (xv - 6, y0)], fill=0, width=1)
    d.line([(x0 - 8, y1), (xv - 6, y1)], fill=0, width=1)
    d.line([(xv, y0), (xv, y1)], fill=0, width=1)
    boxed(xv - 22, (y0 + y1) // 2, f"{round(v_mm)}", f_dim)

    return cell


# ── Satır halinde birleştir ──────────────────────────────────────────────────

def _compose_row(cells, title: str | None = None, gap: int = 16) -> Image.Image:
    H = max(c.height for c in cells)
    W = sum(c.width for c in cells) + gap * (len(cells) - 1) + 2 * gap
    top = 34 if title else gap
    canvas = Image.new("L", (W, H + top), 255)
    if title:
        ImageDraw.Draw(canvas).text((gap, 8), title, fill=0, font=_font(22))
    x = gap
    for c in cells:
        canvas.paste(c, (x, top))
        x += c.width + gap
    return canvas


# ── SENTETİK: katı → boyut-anotasyonlu 3 görünüm sayfası ─────────────────────

def render_multiview_sample(result, rng: random.Random, size: int = 360,
                            hand_drawn: bool = True, annotate: bool = True):
    """Katı modelden boyut-anotasyonlu 3-görünüm teknik çizim sayfası üret.

    Döner: (RGB görüntü, anote_edilmiş_sayılar: list[int])
    """
    xl, yl, zl = bbox_dims(result)
    cells = []
    annotated = set()
    for label, pdir in STANDARD_VIEWS:
        view = render_view(result, pdir, size=size, hand_drawn=hand_drawn, rng=rng)
        if annotate:
            h_mm, v_mm = _view_dims(label, xl, yl, zl)
            cells.append(_annotate_panel(view, label, h_mm, v_mm))
            annotated.update({round(h_mm), round(v_mm)})
        else:
            cells.append(view)
    sheet = _compose_row(cells, title=None)
    return sheet.convert("RGB"), sorted(annotated)


# ── KULLANICI GİRDİSİ: birden çok fotoğrafı tek sayfaya birleştir ────────────

def compose_user_images(images, labels=None, cell: int = 460) -> Image.Image:
    """Kullanıcının yüklediği N görüntüyü tek etiketli sayfaya birleştir."""
    if labels is None:
        labels = [f"Gorunum {i+1}" for i in range(len(images))]
    cells = []
    f = _font(22)
    for img, lab in zip(images, labels):
        g = img.convert("L")
        g.thumbnail((cell, cell), Image.LANCZOS)
        c = Image.new("L", (cell, cell + 34), 255)
        c.paste(g, ((cell - g.width) // 2, 34 + (cell - g.height) // 2))
        ImageDraw.Draw(c).text((8, 6), lab, fill=0, font=f)
        cells.append(c)
    return _compose_row(cells, title=None).convert("RGB")
