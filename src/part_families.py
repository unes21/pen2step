"""Prosedürel parametrik parça üreticileri.

Her üretici fonksiyon:
    girdi : random.Random örneği
    çıktı : (code: str, dims: dict)

`code` çalıştırılabilir, kendi kendine yeten CadQuery kodudur ve daima
`result` değişkenini tanımlar. Bu kod hem RENDER için (eskize çevrilir) hem de
EĞİTİM ETİKETİ olarak kullanılır — yani ground-truth tek kaynaktır.

`dims` parçanın gerçek milimetre boyutlarını içerir (boyut-farkında
değerlendirme ve metrikler için).

Tasarım kararı: STEP→kod ters mühendisliği zordur; bunun yerine kodu
parametreden üretip katı modeli koddan elde ederiz. Böylece etiket ile
geometri %100 tutarlıdır.
"""

from __future__ import annotations

import random
import textwrap


# ── Yardımcılar ────────────────────────────────────────────────────────────

def _mm(rng: random.Random, lo: int, hi: int, step: int = 5) -> int:
    """[lo, hi] aralığında `step`in katı, yuvarlak bir mm değeri seç."""
    n = (hi - lo) // step
    return lo + step * rng.randint(0, n)


def _dedent(code: str) -> str:
    return textwrap.dedent(code).strip() + "\n"


# ── Parça aileleri ───────────────────────────────────────────────────────────

def gen_box(rng: random.Random):
    L = _mm(rng, 30, 200)
    W = _mm(rng, 20, 150)
    H = _mm(rng, 10, 100)
    code = _dedent(f"""
        import cadquery as cq

        # Dikdörtgenler prizması (blok) {L} x {W} x {H} mm
        result = cq.Workplane("XY").box({L}, {W}, {H})
    """)
    return code, {"family": "box", "length": L, "width": W, "height": H}


def gen_cylinder(rng: random.Random):
    R = _mm(rng, 10, 80)
    H = _mm(rng, 15, 150)
    code = _dedent(f"""
        import cadquery as cq

        # Silindir: yarıçap {R} mm, yükseklik {H} mm
        result = cq.Workplane("XY").cylinder({H}, {R})
    """)
    return code, {"family": "cylinder", "radius": R, "height": H}


def gen_plate_hole(rng: random.Random):
    L = _mm(rng, 50, 200)
    W = _mm(rng, 40, 150)
    T = _mm(rng, 5, 30)
    D = _mm(rng, 8, min(L, W) // 2, step=2)
    code = _dedent(f"""
        import cadquery as cq

        # Ortasında delik olan plaka {L} x {W} x {T} mm, delik çapı {D} mm
        result = (
            cq.Workplane("XY")
            .box({L}, {W}, {T})
            .faces(">Z")
            .workplane()
            .hole({D})
        )
    """)
    return code, {"family": "plate_hole", "length": L, "width": W,
                  "thickness": T, "hole_d": D}


def gen_tube(rng: random.Random):
    Ro = _mm(rng, 25, 90)
    Ri = _mm(rng, 8, Ro - 8, step=2)
    H = _mm(rng, 20, 150)
    code = _dedent(f"""
        import cadquery as cq

        # Boru / halka: dış yarıçap {Ro} mm, iç yarıçap {Ri} mm, yükseklik {H} mm
        result = (
            cq.Workplane("XY")
            .circle({Ro})
            .circle({Ri})
            .extrude({H})
        )
    """)
    return code, {"family": "tube", "outer_r": Ro, "inner_r": Ri, "height": H}


def gen_l_bracket(rng: random.Random):
    L = _mm(rng, 60, 180)
    W = _mm(rng, 60, 180)
    t = _mm(rng, 8, 30)
    H = _mm(rng, 20, 120)
    code = _dedent(f"""
        import cadquery as cq

        # L-profil köşebent: kol {L}x{W} mm, et kalınlığı {t} mm, derinlik {H} mm
        result = (
            cq.Workplane("XY")
            .moveTo(0, 0)
            .lineTo({L}, 0)
            .lineTo({L}, {t})
            .lineTo({t}, {t})
            .lineTo({t}, {W})
            .lineTo(0, {W})
            .close()
            .extrude({H})
        )
    """)
    return code, {"family": "l_bracket", "arm_l": L, "arm_w": W,
                  "wall_t": t, "depth": H}


def gen_stepped_shaft(rng: random.Random):
    R1 = _mm(rng, 25, 70)
    H1 = _mm(rng, 20, 80)
    R2 = _mm(rng, 8, R1 - 5, step=2)
    H2 = _mm(rng, 20, 100)
    code = _dedent(f"""
        import cadquery as cq

        # Kademeli mil: alt R{R1}xH{H1}, üst R{R2}xH{H2} mm
        result = (
            cq.Workplane("XY")
            .circle({R1})
            .extrude({H1})
            .faces(">Z")
            .workplane()
            .circle({R2})
            .extrude({H2})
        )
    """)
    return code, {"family": "stepped_shaft", "r1": R1, "h1": H1,
                  "r2": R2, "h2": H2}


def gen_bolt_plate(rng: random.Random):
    L = _mm(rng, 80, 220)
    W = _mm(rng, 60, 180)
    T = _mm(rng, 6, 25)
    D = _mm(rng, 6, 16, step=2)
    m = _mm(rng, 10, 25)  # kenardan delik merkezine uzaklık
    code = _dedent(f"""
        import cadquery as cq

        # 4 köşe delikli bağlantı plakası {L}x{W}x{T} mm, delik {D} mm, kenar boşluğu {m} mm
        result = (
            cq.Workplane("XY")
            .box({L}, {W}, {T})
            .faces(">Z")
            .workplane()
            .rect({L} - 2 * {m}, {W} - 2 * {m}, forConstruction=True)
            .vertices()
            .hole({D})
        )
    """)
    return code, {"family": "bolt_plate", "length": L, "width": W,
                  "thickness": T, "hole_d": D, "margin": m}


def gen_slotted_plate(rng: random.Random):
    L = _mm(rng, 80, 200)
    W = _mm(rng, 50, 140)
    T = _mm(rng, 6, 25)
    SL = _mm(rng, 30, L - 30)
    SW = _mm(rng, 8, min(SL - 5, W - 20), step=2)
    code = _dedent(f"""
        import cadquery as cq

        # Yivli (slot) plaka {L}x{W}x{T} mm; slot uzunluk {SL} mm, genişlik {SW} mm
        result = (
            cq.Workplane("XY")
            .box({L}, {W}, {T})
            .faces(">Z")
            .workplane()
            .slot2D({SL}, {SW}, 0)
            .cutThruAll()
        )
    """)
    return code, {"family": "slotted_plate", "length": L, "width": W,
                  "thickness": T, "slot_l": SL, "slot_w": SW}


def gen_filleted_block(rng: random.Random):
    L = _mm(rng, 50, 180)
    W = _mm(rng, 40, 140)
    H = _mm(rng, 20, 100)
    r = _mm(rng, 4, max(4, min(L, W) // 4), step=2)
    code = _dedent(f"""
        import cadquery as cq

        # Dikey kenarları yuvarlatılmış blok {L}x{W}x{H} mm, köşe yarıçapı {r} mm
        result = (
            cq.Workplane("XY")
            .box({L}, {W}, {H})
            .edges("|Z")
            .fillet({r})
        )
    """)
    return code, {"family": "filleted_block", "length": L, "width": W,
                  "height": H, "fillet_r": r}


def gen_chamfered_block(rng: random.Random):
    L = _mm(rng, 50, 180)
    W = _mm(rng, 40, 140)
    H = _mm(rng, 20, 100)
    c = _mm(rng, 3, max(3, min(L, W) // 5), step=1)
    code = _dedent(f"""
        import cadquery as cq

        # Dikey kenarları pahlanmış blok {L}x{W}x{H} mm, pah {c} mm
        result = (
            cq.Workplane("XY")
            .box({L}, {W}, {H})
            .edges("|Z")
            .chamfer({c})
        )
    """)
    return code, {"family": "chamfered_block", "length": L, "width": W,
                  "height": H, "chamfer": c}


# ── Kayıt (registry) ─────────────────────────────────────────────────────────

FAMILIES = [
    gen_box,
    gen_cylinder,
    gen_plate_hole,
    gen_tube,
    gen_l_bracket,
    gen_stepped_shaft,
    gen_bolt_plate,
    gen_slotted_plate,
    gen_filleted_block,
    gen_chamfered_block,
]


def sample(rng: random.Random):
    """Rastgele bir parça ailesinden bir örnek üret → (code, dims)."""
    fn = rng.choice(FAMILIES)
    return fn(rng)
