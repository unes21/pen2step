"""Case study (concrete placing boom MXR 32-4): ground-truth CadQuery models and reference sheets.

For each part: gt/<id>.py (CadQuery program), gt/<id>.step, and sheets/<id>.png, an A4 landscape
reference sheet (isometric view, front/top/side views, dimension table) that a person redraws by hand.

Dimension sources: "catalogue" = Putzmeister spare parts list 184400069 (MXR 32-4 / RS850);
"DIN" = the standard named in that list for the part; "representative" = diameter taken from the
mating catalogue bush, remaining sizes assumed (to be replaced by the manufacturer pin drawings).

Usage: python case_study/make_reference_sheets.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import cadquery as cq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parent
GT, SHEETS, TMP = ROOT / "gt", ROOT / "sheets", ROOT / "_render"
for p in (GT, SHEETS, TMP):
    p.mkdir(parents=True, exist_ok=True)

HEX = "import math\ndef hexagon(wp, s, h):\n    return wp.polygon(6, s / math.cos(math.pi / 6)).extrude(h)\n"

PARTS = [
    # id, name_tr, name_en, catalogue no, source, dims (label, mm), CadQuery code
    ("cs_01", "Burç DU-B 60x65x30", "Bush DU-B 60x65x30", "065993000", "catalogue",
     [("iç çap", 60), ("dış çap", 65), ("boy", 30)],
     "result = cq.Workplane('XY').circle(65 / 2).circle(60 / 2).extrude(30)"),
    ("cs_02", "Burç DU-B 50x55x30", "Bush DU-B 50x55x30", "043693005", "catalogue",
     [("iç çap", 50), ("dış çap", 55), ("boy", 30)],
     "result = cq.Workplane('XY').circle(55 / 2).circle(50 / 2).extrude(30)"),
    ("cs_03", "Burç DU-B Ø40x44x30", "Bush DU-B Ø40x44x30", "430423", "catalogue",
     [("iç çap", 40), ("dış çap", 44), ("boy", 30)],
     "result = cq.Workplane('XY').circle(44 / 2).circle(40 / 2).extrude(30)"),
    ("cs_04", "Burç 21x13x12", "Bush 21x13x12", "716572", "catalogue",
     [("dış çap", 21), ("iç çap", 13), ("boy", 12)],
     "result = cq.Workplane('XY').circle(21 / 2).circle(13 / 2).extrude(12)"),
    ("cs_05", "Plastik plaka 190x80x10", "Plastic plate 190x80x10", "651985", "catalogue",
     [("uzunluk", 190), ("genişlik", 80), ("kalınlık", 10)],
     "result = cq.Workplane('XY').box(190, 80, 10)"),
    ("cs_06", "Plastik plaka 144x55x5", "Plastic plate 144x55x5", "651987", "catalogue",
     [("uzunluk", 144), ("genişlik", 55), ("kalınlık", 5)],
     "result = cq.Workplane('XY').box(144, 55, 5)"),
    ("cs_07", "Altı köşe cıvata M8x25 DIN 933", "Hexagon head screw M8x25 DIN 933", "032338009", "DIN",
     [("anahtar ağzı", 13), ("baş yüksekliği", 5.3), ("gövde çapı", 8), ("gövde boyu", 25)],
     HEX + "result = hexagon(cq.Workplane('XY'), 13, 5.3).faces('<Z').workplane().circle(4).extrude(25)"),
    ("cs_08", "Altı köşe cıvata M10x25 DIN 933", "Hexagon head screw M10x25 DIN 933", "032357006", "DIN",
     [("anahtar ağzı", 17), ("baş yüksekliği", 6.4), ("gövde çapı", 10), ("gövde boyu", 25)],
     HEX + "result = hexagon(cq.Workplane('XY'), 17, 6.4).faces('<Z').workplane().circle(5).extrude(25)"),
    ("cs_09", "Altı köşe cıvata M12x30 DIN 933", "Hexagon head screw M12x30 DIN 933", "280646006", "DIN",
     [("anahtar ağzı", 19), ("baş yüksekliği", 7.5), ("gövde çapı", 12), ("gövde boyu", 30)],
     HEX + "result = hexagon(cq.Workplane('XY'), 19, 7.5).faces('<Z').workplane().circle(6).extrude(30)"),
    ("cs_10", "Altı köşe cıvata M10x130 DIN 931", "Hexagon head screw M10x130 DIN 931", "032157002", "DIN",
     [("anahtar ağzı", 17), ("baş yüksekliği", 6.4), ("gövde çapı", 10), ("gövde boyu", 130)],
     HEX + "result = hexagon(cq.Workplane('XY'), 17, 6.4).faces('<Z').workplane().circle(5).extrude(130)"),
    ("cs_11", "Kendinden kilitli somun M8 DIN 985", "Self-locking hex nut M8 DIN 985", "293146001", "DIN",
     [("anahtar ağzı", 13), ("yükseklik", 8), ("delik çapı", 8)],
     HEX + "result = hexagon(cq.Workplane('XY'), 13, 8).faces('>Z').workplane().hole(8)"),
    ("cs_12", "Kendinden kilitli somun M10 DIN 985", "Self-locking hex nut M10 DIN 985", "034106006", "DIN",
     [("anahtar ağzı", 17), ("yükseklik", 10), ("delik çapı", 10)],
     HEX + "result = hexagon(cq.Workplane('XY'), 17, 10).faces('>Z').workplane().hole(10)"),
    ("cs_13", "Pul A8,4 DIN 125", "Washer A8.4 DIN 125", "037107002", "DIN",
     [("iç çap", 8.4), ("dış çap", 16), ("kalınlık", 1.6)],
     "result = cq.Workplane('XY').circle(16 / 2).circle(8.4 / 2).extrude(1.6)"),
    ("cs_14", "Pul B10,5 DIN 125", "Washer B10.5 DIN 125", "037108001", "DIN",
     [("iç çap", 10.5), ("dış çap", 20), ("kalınlık", 2)],
     "result = cq.Workplane('XY').circle(20 / 2).circle(10.5 / 2).extrude(2)"),
    ("cs_15", "Yatak pimi Ø40 (temsili)", "Hinge pin Ø40 (representative)", "716642", "representative",
     [("pim çapı", 40), ("pim boyu", 150), ("baş çapı", 60), ("baş kalınlığı", 10), ("baş deliği", 13)],
     "head = cq.Workplane('XY').circle(30).extrude(10).faces('>Z').workplane().pushPoints([(22, 0)]).hole(13)\n"
     "result = head.faces('<Z').workplane().circle(20).extrude(150)"),
    ("cs_16", "Yatak pimi Ø50 (temsili)", "Hinge pin Ø50 (representative)", "716643", "representative",
     [("pim çapı", 50), ("pim boyu", 180), ("baş çapı", 75), ("baş kalınlığı", 12), ("baş deliği", 13)],
     "head = cq.Workplane('XY').circle(37.5).extrude(12).faces('>Z').workplane().pushPoints([(28, 0)]).hole(13)\n"
     "result = head.faces('<Z').workplane().circle(25).extrude(180)"),
    ("cs_17", "Yatak pimi Ø60 (temsili)", "Hinge pin Ø60 (representative)", "716645", "representative",
     [("pim çapı", 60), ("pim boyu", 200), ("baş çapı", 90), ("baş kalınlığı", 12), ("baş deliği", 13)],
     "head = cq.Workplane('XY').circle(45).extrude(12).faces('>Z').workplane().pushPoints([(34, 0)]).hole(13)\n"
     "result = head.faces('<Z').workplane().circle(30).extrude(200)"),
    ("cs_18", "Aks tutma plakası (temsili)", "Bolt locating plate (representative)", "716565", "representative",
     [("uzunluk", 80), ("genişlik", 40), ("kalınlık", 8), ("delik çapı", 9), ("delik aralığı", 50)],
     "result = cq.Workplane('XY').box(80, 40, 8).faces('>Z').workplane().pushPoints([(-25, 0), (25, 0)]).hole(9)"),
    ("cs_19", "Aks tutma plakası, yarıklı (temsili)", "Slotted bolt locating plate (representative)", "717005", "representative",
     [("uzunluk", 70), ("genişlik", 35), ("kalınlık", 6), ("yarık genişliği", 12), ("yarık derinliği", 20), ("delik çapı", 9)],
     "result = (cq.Workplane('XY').box(70, 35, 6).faces('>Z').workplane().pushPoints([(-20, 0)]).hole(9)"
     ".faces('>Z').workplane().center(25, 0).rect(20, 12).cutThruAll())"),
    ("cs_20", "Boru tutma braketi (temsili)", "Pipe holder bracket (representative)", "677053", "representative",
     [("taban", "100 x 60 x 8"), ("dikey kol yüksekliği", 90), ("kol kalınlığı", 8), ("boru deliği çapı", 40), ("taban delikleri", "2 x Ø11, 70 aralık")],
     "base = cq.Workplane('XY').box(100, 60, 8).faces('>Z').workplane().pushPoints([(-35, 0), (35, 0)]).hole(11)\n"
     "arm = cq.Workplane('XZ').center(0, 49).rect(60, 90).extrude(-8).translate((0, -26, 0))\n"
     "arm = arm.faces('<Y').workplane(centerOption='CenterOfMass').hole(40)\n"
     "result = base.union(arm)"),
]
SRC_TR = {"catalogue": "Putzmeister yedek parça listesi 184400069",
          "DIN": "Katalogdaki DIN standardı",
          "representative": "TEMSİLİ: çap eş burçtan, diğer ölçüler varsayım (DWG gelince güncellenecek)"}


def build(pid, code):
    ns = {"cq": cq}
    exec("import cadquery as cq\n" + code, ns)
    step = GT / f"{pid}.step"
    cq.exporters.export(ns["result"], str(step))
    (GT / f"{pid}.py").write_text("import cadquery as cq\n" + code + "\n", encoding="utf-8")
    return ns["result"]


def render(shape, out, direction, size=520, hidden=True):
    """Render one projection; the shape is scaled to a common size first so that line weights match
    across parts (display only: the ground-truth STEP and the dimension table are unscaled)."""
    bb = shape.val().BoundingBox()
    shape = cq.Workplane("XY").add(shape.val().scale(200.0 / max(bb.xlen, bb.ylen, bb.zlen)))
    svg = TMP / (out.stem + ".svg")
    cq.exporters.export(shape, str(svg), exportType="SVG", opt={
        "width": size, "height": size, "marginLeft": 25, "marginTop": 25, "showAxes": False,
        "projectionDir": direction, "strokeWidth": 1.4, "strokeColor": (0, 0, 0),
        "hiddenColor": (140, 140, 140), "showHidden": hidden})
    renderPM.drawToFile(svg2rlg(str(svg)), str(out), fmt="PNG", bg=0xFFFFFF)
    im = ImageOps.grayscale(Image.open(out))
    box = ImageOps.invert(im).getbbox()
    return im.crop(box) if box else im


def sheet(part, shape):
    pid, tr, en, cat, src, dims, _ = part
    views = {"İzometrik": render(shape, TMP / f"{pid}_iso.png", (1, -1, 1), 700, hidden=False),
             "Ön görünüş": render(shape, TMP / f"{pid}_front.png", (0, -1, 0)),
             "Üst görünüş": render(shape, TMP / f"{pid}_top.png", (0, 0, 1)),
             "Yan görünüş": render(shape, TMP / f"{pid}_side.png", (1, 0, 0))}
    fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
    fig.patch.set_facecolor("white")
    fig.text(0.04, 0.94, f"{pid}  ·  {tr}", fontsize=17, weight="bold")
    fig.text(0.04, 0.905, f"{en}  ·  Katalog no {cat}  ·  Ölçü kaynağı: {SRC_TR[src]}", fontsize=10,
             color="#b00020" if src == "representative" else "#444")
    slots = {"İzometrik": [0.03, 0.42, 0.42, 0.45], "Ön görünüş": [0.03, 0.05, 0.22, 0.33],
             "Üst görünüş": [0.27, 0.05, 0.22, 0.33], "Yan görünüş": [0.51, 0.05, 0.22, 0.33]}
    for name, rect in slots.items():
        ax = fig.add_axes(rect)
        ax.imshow(views[name], cmap="gray", vmin=0, vmax=255)
        ax.set_title(name, fontsize=11)
        ax.axis("off")
    ax = fig.add_axes([0.52, 0.45, 0.44, 0.40]); ax.axis("off")
    ax.text(0, 1, "Ölçüler (mm)", fontsize=13, weight="bold", va="top")
    for i, (k, v) in enumerate(dims):
        ax.text(0.02, 0.86 - i * 0.12, f"{k}", fontsize=12, va="top")
        ax.text(0.62, 0.86 - i * 0.12, f"{v}", fontsize=12, va="top", weight="bold")
    fig.text(0.77, 0.30, "Çizim talimatı:\nParçayı üç görünüşte (ön, üst, yan)\nelle çizin ve tablodaki ölçüleri\nçiziminize yazın.",
             fontsize=10.5, va="top", color="#333")
    out = SHEETS / f"{pid}.png"
    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out


def main():
    rows = []
    for part in PARTS:
        shape = build(part[0], part[6])
        sheet(part, shape)
        v = shape.val().Volume()
        rows.append({"id": part[0], "name_tr": part[1], "name_en": part[2], "catalogue_no": part[3],
                     "dimension_source": part[4], "dims": [[k, v_] for k, v_ in part[5]], "volume_mm3": round(v, 1)})
        print(part[0], part[4], round(v, 1))
    (ROOT / "parts.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
