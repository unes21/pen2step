"""Gerçek el-çizimi test seti için ground-truth CadQuery modelleri.

19 parça. Ölçülü olanlar (mm) çizimdeki gerçek değerlerle; ölçüsüz olanlar
orantıdan tahmin (en uzun kenar ~100 mm kanonik ölçeğe getirilir, çünkü
framework ölçüsüz çıktıyı kanonik 100 mm'e ölçekler).

cm cinsinden çizilen #01 ve #03 → mm'e çevrildi (×10).
"""

import cadquery as cq

# Her parça: (kod_str, family, annotated_dims_mm)
# annotated_dims: çizimde YAZAN ölçüler (mm). Ölçüsüzlerde [].

PARTS = {}

# ── 01: L/kademeli blok (cm: 8,5,3,2 → mm) ───────────────────────────────────
PARTS["01"] = ('''import cadquery as cq
# L-profil blok 80x50x50 mm (cm ölçülerden), Y boyunca 50 derinlik
result = (
    cq.Workplane("XZ")
    .polyline([(0,0),(80,0),(80,20),(30,20),(30,50),(0,50)])
    .close()
    .extrude(50)
)
''', "stepped_block", [20, 30, 50, 80])

# ── 02: Köşebent/L-braket + delik (mm: 60,40,50,6, delik) ────────────────────
PARTS["02"] = ('''import cadquery as cq
# Açı köşebenti: yatay 60x40x6 + dikey 6x40x50, yatay kanatta delik d12
horiz = cq.Workplane("XY").box(60, 40, 6, centered=(False, True, False))
horiz = (horiz.faces(">Z").workplane(centerOption="CenterOfBoundBox")
         .center(10, 0).hole(12))
vert = cq.Workplane("XY").box(6, 40, 50, centered=(False, True, False))
result = horiz.union(vert)
''', "bracket_hole", [6, 12, 40, 50, 60])

# ── 03: U-kanal (cm: 2,5,2 / 3,2 / 10 → mm) ──────────────────────────────────
PARTS["03"] = ('''import cadquery as cq
# U-kanal: uzunluk 100, dış kesit 90x50, et 20 (U açıklığı yukarı)
outer = cq.Workplane("YZ").box(90, 50, 100, centered=(True, False, True))
cut   = (cq.Workplane("YZ").workplane(offset=-60)
         .center(0, 20).box(50, 40, 120, centered=(True, False, True)))
result = outer.cut(cut)
''', "u_channel", [20, 30, 50, 90, 100])

# ── 04: T-blok (ölçüsüz) ─────────────────────────────────────────────────────
PARTS["04"] = ('''import cadquery as cq
# T-profil blok, derinlik 60. Flanş 100x20, gövde 30x50 aşağı
result = (
    cq.Workplane("XZ")
    .polyline([(0,80),(100,80),(100,60),(65,60),(65,0),(35,0),(35,60),(0,60)])
    .close()
    .extrude(60)
)
''', "t_block", [])

# ── 05: 2 kademeli merdiven blok (ölçüsüz) ───────────────────────────────────
PARTS["05"] = ('''import cadquery as cq
# 2 basamaklı merdiven, derinlik 70
result = (
    cq.Workplane("XZ")
    .polyline([(0,0),(100,0),(100,33),(66,33),(66,66),(33,66),(33,100),(0,100)])
    .close()
    .extrude(70)
)
''', "staircase", [])

# ── 06: Pahlı blok (ölçüsüz) ─────────────────────────────────────────────────
PARTS["06"] = ('''import cadquery as cq
# Bir üst köşesi pahlı blok 100x70x60
result = (
    cq.Workplane("XZ")
    .polyline([(0,0),(100,0),(100,45),(70,70),(0,70)])
    .close()
    .extrude(60)
)
''', "chamfer_block", [])

# ── 07: Kademeli blok 2-step (ölçüsüz) ───────────────────────────────────────
PARTS["07"] = ('''import cadquery as cq
# Tek kademeli (L) blok 100x60, derinlik 60
result = (
    cq.Workplane("XZ")
    .polyline([(0,0),(100,0),(100,30),(45,30),(45,60),(0,60)])
    .close()
    .extrude(60)
)
''', "stepped_block", [])

# ── 08: Yuvarlatılmış ince plaka (ölçüsüz) ───────────────────────────────────
PARTS["08"] = ('''import cadquery as cq
# Köşeleri yuvarlatılmış ince plaka 100x100x10, köşe R20
result = cq.Workplane("XY").box(100, 100, 10).edges("|Z").fillet(20)
''', "rounded_plate", [])

# ── 09: Kare boru (ölçüsüz) ──────────────────────────────────────────────────
PARTS["09"] = ('''import cadquery as cq
# Dik kare boru: dış 60x60, iç 40x40, yükseklik 100
outer = cq.Workplane("XY").box(60, 60, 100)
result = outer.faces(">Z").workplane().rect(40, 40).cutThruAll()
''', "square_tube", [])

# ── 10: Eksen delikli silindir / boru (ölçüsüz) ──────────────────────────────
PARTS["10"] = ('''import cadquery as cq
# Boru: dış çap 30, uzunluk 100, eksende delik d10 (X ekseni boyunca)
result = (cq.Workplane("YZ").circle(15).extrude(100)
          .faces(">X").workplane().hole(10))
''', "tube", [])

# ── 11: Kademeli mil + eksen deliği (ölçüsüz) ────────────────────────────────
PARTS["11"] = ('''import cadquery as cq
# 3 çaplı kademeli mil (X ekseni), eksende delik d8
s = cq.Workplane("YZ").circle(20).extrude(30)
s = s.faces(">X").workplane().circle(14).extrude(40)
s = s.faces(">X").workplane().circle(9).extrude(30)
result = s.faces(">X").workplane().hole(8)
''', "stepped_shaft", [])

# ── 12: Silindir kafalı cıvata / cap screw (ölçüsüz) ─────────────────────────
PARTS["12"] = ('''import cadquery as cq
# Silindirik kafa d36 h24 + gövde d20 h76 (X ekseni)
head = cq.Workplane("YZ").circle(18).extrude(24)
result = head.faces(">X").workplane().circle(10).extrude(76)
''', "cap_screw", [])

# ── 13: Kısa boru / kalın rondela (ölçüsüz) ──────────────────────────────────
PARTS["13"] = ('''import cadquery as cq
# Kısa silindir (rondela): dış d80, yükseklik 30, eksende delik d40
result = (cq.Workplane("XY").circle(40).extrude(30)
          .faces(">Z").workplane().hole(40))
''', "washer", [])

# ── 14: Kama yuvalı silindir (ölçüsüz) ───────────────────────────────────────
PARTS["14"] = ('''import cadquery as cq
# Dik silindir d60 h80, eksende delik d16, yanında kama yuvası (slot)
s = cq.Workplane("XY").circle(30).extrude(80).faces(">Z").workplane().hole(16)
key = cq.Workplane("XY").box(12, 40, 80, centered=(True, False, False)).translate((0, 18, 0))
result = s.cut(key)
''', "keyed_cylinder", [])

# ── 15: Flanşlı burç (ölçüsüz) ───────────────────────────────────────────────
PARTS["15"] = ('''import cadquery as cq
# Flanşlı burç: flanş d80 kalınlık 15 + gövde d50 uzunluk 60, delik d24 (X)
flange = cq.Workplane("YZ").circle(40).extrude(15)
body = flange.faces(">X").workplane().circle(25).extrude(60)
result = body.faces(">X").workplane().hole(24)
''', "flanged_bushing", [])

# ── 16: Yuvalı çubuk (ölçüsüz) ───────────────────────────────────────────────
PARTS["16"] = ('''import cadquery as cq
# Silindir çubuk d50 uzunluk 100 (X), eksende delik d16
result = (cq.Workplane("YZ").circle(25).extrude(100)
          .faces(">X").workplane().hole(16))
''', "rod", [])

# ── 17: Koni/huni + delik (mm: 40,30,50,20) ──────────────────────────────────
PARTS["17"] = ('''import cadquery as cq
# Kesik koni: büyük d40 → küçük d28, uzunluk 50 (X), eksende delik d16
cone = (cq.Workplane("YZ").circle(20)
        .workplane(offset=50).circle(14).loft(combine=True))
result = cone.faces(">X").workplane().hole(16)
''', "cone_hole", [16, 20, 30, 40, 50])

# ── 18: Rondela / halka (mm: 40,16,6) ────────────────────────────────────────
PARTS["18"] = ('''import cadquery as cq
# Düz rondela: dış d40, iç d16, kalınlık 6
result = (cq.Workplane("XY").circle(20).extrude(6)
          .faces(">Z").workplane().hole(16))
''', "washer", [6, 16, 40])

# ── 19: Altıgen cıvata (mm: 24,14,10,30) ─────────────────────────────────────
PARTS["19"] = ('''import cadquery as cq
# Altıgen kafa (anahtar ağzı 24, yük 10) + gövde d14 uzunluk 30 (X)
head = cq.Workplane("YZ").polygon(6, 24/0.866).extrude(10)
result = head.faces(">X").workplane().circle(7).extrude(30)
''', "hex_bolt", [10, 14, 24, 30])


if __name__ == "__main__":
    import traceback
    ok, bad = [], []
    for k, (code, fam, dims) in PARTS.items():
        ns = {}
        try:
            exec(code, ns)
            r = ns["result"]
            bb = r.val().BoundingBox()
            print(f"{k} {fam:18s} OK  bbox=({bb.xlen:.0f},{bb.ylen:.0f},{bb.zlen:.0f})  dims={dims}")
            ok.append(k)
        except Exception as e:
            print(f"{k} {fam:18s} HATA: {e}")
            bad.append(k)
    print(f"\n{len(ok)} OK, {len(bad)} hata: {bad}")
