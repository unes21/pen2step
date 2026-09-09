"""Boyut anotasyonu çıkarımı (OCR) + prompt enjeksiyonu.

Framework'ün "boyut körlüğünü giderme" sütunu: çizimin üzerine yazılmış ölçü
sayılarını (ör. "85", "40") okur ve frozen VLM'in prompt'una METİN kısıtı
olarak enjekte eder. Böylece model boyutu TAHMİN etmek yerine çizimde YAZAN
gerçek mm değerlerini kullanır.

OCR motoru: easyocr (offline; ilk çağrıda ~64 MB model iner). Yoksa modül
zarifçe devre dışı kalır (framework boyut-ipucu olmadan çalışır).

Tasarım notu: digit-only allowlist KULLANMIYORUZ — "ON"/"YAN" gibi görünüm
etiketlerini "01" gibi sayılara zorlamasın diye. Tam alfanümerik OCR yapıp
sonra yalnızca saf sayı token'larını süzüyoruz.
"""

from __future__ import annotations

import re

import numpy as np
from PIL import Image

_reader = None
_OCR_AVAILABLE = None


def ocr_available() -> bool:
    global _OCR_AVAILABLE
    if _OCR_AVAILABLE is None:
        try:
            import easyocr  # noqa: F401
            _OCR_AVAILABLE = True
        except Exception:
            _OCR_AVAILABLE = False
    return _OCR_AVAILABLE


def _get_reader(prefer_gpu: bool = True):
    """easyocr Reader'ı tek sefer yükle. GPU çok daha hızlı; sığmazsa CPU'ya düşer."""
    global _reader
    if _reader is None:
        import easyocr
        try:
            _reader = easyocr.Reader(["en"], gpu=prefer_gpu)
        except Exception:
            _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def _dedup(values, tol_ratio: float = 0.04):
    """Birbirine çok yakın değerleri tekille (OCR aynı sayıyı 2 kez görebilir)."""
    out = []
    for v in sorted(values):
        if not out or abs(v - out[-1]) > max(1.0, tol_ratio * v):
            out.append(v)
    return out


# conf_thr = 0.45 is the value used for every OCR run reported in the paper
# (synthetic 8 Jun 2026, real 15 Jun 2026). A later edit lowered the default to 0.30;
# that version never produced a published number, so 0.45 is restored here.
# If you re-run the ablation at 0.30, update the manuscript to match.
def extract_dimensions(image: Image.Image, conf_thr: float = 0.45,
                       lo: float = 1.0, hi: float = 10000.0,
                       upscale: float = 1.5, gpu: bool = False,
                       min_max: float = 10.0):
    """Görüntüdeki ölçü sayılarını çıkar → artan sıralı benzersiz mm listesi.

    OCR yoksa boş liste döner (framework boyut-ipucu olmadan devam eder).

    Makuliyet tabanı (min_max): A4'e çizilmiş bir parçanın EN BÜYÜK ölçüsü
    mm mertebesinde olamaz. Okunan setin maksimumu min_max'tan küçükse (izole
    "2" gibi kesik-çizgi/etiket gürültüsü) güvenilmez kabul edilip [] dönülür —
    yanlış küçük ölçeklemeyi (scale_recover'ın hatayı büyütmesini) önler.
    """
    if not ocr_available():
        return []

    reader = _get_reader(prefer_gpu=True)
    img = image.convert("RGB")
    if upscale and upscale != 1.0:
        img = img.resize((int(img.width * upscale), int(img.height * upscale)),
                         Image.LANCZOS)
    arr = np.array(img)

    try:
        results = reader.readtext(arr)
    except Exception:
        # GPU'da OOM olabilir (bella yüklü) → CPU okuyucuya düş ve tekrar dene
        global _reader
        try:
            import easyocr
            _reader = easyocr.Reader(["en"], gpu=False)
            results = _reader.readtext(arr)
        except Exception:
            return []

    # Önce yeterince güvenilir token'ları topla; cm birimi var mı tespit et.
    raw = []           # (değer, bu_token_cm_mi)
    drawing_is_cm = False
    for _box, txt, conf in results:
        if conf < conf_thr:
            continue
        low = txt.lower()
        tok_is_cm = ("cm" in low) or bool(re.search(r"\d\s*c", low))  # "10cm","10 cm","2c"
        if tok_is_cm:
            drawing_is_cm = True
        for tok in re.findall(r"\d+(?:[.,]\d+)?", txt):
            try:
                raw.append((float(tok.replace(",", ".")), tok_is_cm))
            except ValueError:
                continue

    # Çizimde herhangi bir yerde "cm" geçiyorsa tüm ölçüleri cm kabul et → mm'e çevir.
    found = []
    for val, tok_is_cm in raw:
        mm = val * 10.0 if (drawing_is_cm or tok_is_cm) else val
        if lo <= mm <= hi:
            found.append(mm)

    dims = _dedup(found)
    if not dims or max(dims) < min_max:
        return []
    return dims


def build_dimension_hint(dims) -> str:
    """Çıkarılan boyutları prompt'a eklenecek İngilizce kısıt cümlesine çevir."""
    if not dims:
        return ""
    nums = ", ".join(
        str(int(v)) if float(v).is_integer() else f"{v:g}" for v in dims
    )
    return (
        " The drawing is annotated with these dimensions in millimeters: "
        f"{nums}. Use these exact numeric values for the corresponding "
        "edges; do not invent other sizes."
    )
