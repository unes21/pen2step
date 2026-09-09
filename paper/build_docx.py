# -*- coding: utf-8 -*-
import re
from docx import Document
from docx.shared import Pt, Cm, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# fig_pipeline.png and fig_eq_fscore.png live in figures/ (regenerate with gen_figs.py)
import os as _os
# Repository-relative locations (was: absolute paths on the original author machine).
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_REPO = _os.path.dirname(_HERE)
SCRATCH = _os.path.join(_REPO, "figures")
FIGDIR = _os.path.join(_REPO, "figures")
OUT = _os.path.join(_HERE, "Pen2STEP.docx")

SERIF = "Times New Roman"
MONO = "Consolas"
BODY = 11
CONTENT_CM = 16.0  # A4 (21cm) minus 2.5cm margins each side

doc = Document()

# ---- page setup: A4, 2.5cm margins ----
sec = doc.sections[0]
sec.page_width = Mm(210); sec.page_height = Mm(297)
sec.top_margin = Cm(2.5); sec.bottom_margin = Cm(2.5)
sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)

# ---- base styles ----
normal = doc.styles["Normal"]
normal.font.name = SERIF
normal.font.size = Pt(BODY)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.08
# make sure complex/east-asian also map to serif
rpr = normal.element.get_or_add_rPr().get_or_add_rFonts()
rpr.set(qn("w:ascii"), SERIF); rpr.set(qn("w:hAnsi"), SERIF); rpr.set(qn("w:cs"), SERIF)

for sid, size in (("Heading 1", 14), ("Heading 2", 12)):
    st = doc.styles[sid]
    st.font.name = SERIF; st.font.size = Pt(size); st.font.bold = True
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.space_before = Pt(12 if size == 14 else 8)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.keep_with_next = True

# --------------------------------------------------------------- helpers
def add_runs(p, text, size=BODY, font=SERIF):
    """Mini markup: **bold**, `mono`."""
    for part in re.split(r"(\*\*.*?\*\*|`.*?`)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = p.add_run(part[2:-2]); r.bold = True
            r.font.name = font; r.font.size = Pt(size)
        elif part.startswith("`") and part.endswith("`"):
            r = p.add_run(part[1:-1]); r.font.name = MONO; r.font.size = Pt(size - 0.5)
        else:
            r = p.add_run(part); r.font.name = font; r.font.size = Pt(size)

def body(text, justify=True, space_after=6, size=BODY):
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(space_after)
    add_runs(p, text, size=size)
    return p

def h1(text):
    p = doc.add_paragraph(style="Heading 1"); p.add_run(text); return p

def h2(text):
    p = doc.add_paragraph(style="Heading 2"); p.add_run(text); return p

def bullet(text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    add_runs(p, text)
    return p

def caption(label, text, before=4, after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(label); r.bold = True; r.font.name = SERIF; r.font.size = Pt(9.5)
    r2 = p.add_run(" " + text); r2.font.name = SERIF; r2.font.size = Pt(9.5)
    return p

def add_image(path, width_cm, caption_label=None, caption_text=None):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))
    if caption_label:
        cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        cp.paragraph_format.space_after = Pt(8)
        r = cp.add_run(caption_label); r.bold = True; r.font.name = SERIF; r.font.size = Pt(9.5)
        r2 = cp.add_run(" " + caption_text); r2.font.name = SERIF; r2.font.size = Pt(9.5)

def _set_borders(table):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge, sz in (("top", "8"), ("bottom", "8")):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), sz)
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000"); b.append(e)
    for edge in ("left", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge); e.set(qn("w:val"), "none")
        e.set(qn("w:sz"), "0"); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "auto"); b.append(e)
    tblPr.append(b)

def _cell_bottom(cell, sz="6"):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    e = OxmlElement("w:bottom")
    e.set(qn("w:val"), "single"); e.set(qn("w:sz"), sz)
    e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000"); b.append(e)
    tcPr.append(b)

def add_table(headers, rows, widths_cm, bold_cells=None, size=9.5, mono_first=True):
    bold_cells = bold_cells or set()
    ncol = len(headers)
    t = doc.add_table(rows=1, cols=ncol)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False; t.allow_autofit = False
    _set_borders(t)
    # header
    for j, htext in enumerate(headers):
        c = t.rows[0].cells[j]
        c.width = Cm(widths_cm[j]); c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        _cell_bottom(c, "6")
        para = c.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.space_after = Pt(2); para.paragraph_format.space_before = Pt(2)
        r = para.add_run(htext); r.bold = True; r.font.name = SERIF; r.font.size = Pt(size)
    # body rows
    for i, row in enumerate(rows):
        cells = t.add_row().cells
        for j, val in enumerate(row):
            c = cells[j]; c.width = Cm(widths_cm[j]); c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            para = c.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.space_after = Pt(2); para.paragraph_format.space_before = Pt(2)
            r = para.add_run(val)
            r.font.name = MONO if (j == 0 and mono_first) else SERIF
            r.font.size = Pt(size)
            if (i, j) in bold_cells:
                r.bold = True
    return t

def add_algorithm():
    lines = [
        ("Require:", " sketch images ℐ, frozen VLM g, config c"),
        ("1:", "  x ← Compose(ℐ)"),
        ("2:", "  D ← OCR(x)                      ▷ plausibility floor applied"),
        ("3:", "  p ← BuildPrompt(D, c.multiview)"),
        ("4:", "  C ← ∅"),
        ("5:", "  for i ← 0 … N−1 do"),
        ("6:", "      r ← g(x, p, i)"),
        ("7:", "      k ← ASTRepair(r)"),
        ("8:", "      (ok, s) ← ExecuteIsolated(k, D, c)"),
        ("9:", "      if ok then  C ← C ∪ {s}"),
        ("10:", "  end for"),
        ("11:", "  return SelectBest(C, D)"),
    ]
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False; t.allow_autofit = False
    # full border box
    tblPr = t._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "bottom", "left", "right"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "6")
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), "808080"); b.append(e)
    tblPr.append(b)
    cell = t.rows[0].cells[0]; cell.width = Cm(CONTENT_CM)
    cell.margins = None
    # title line
    p0 = cell.paragraphs[0]; p0.paragraph_format.space_after = Pt(3)
    r = p0.add_run("Algorithm 1.  Pen2STEP inference (training-free)")
    r.bold = True; r.font.name = SERIF; r.font.size = Pt(10)
    for tag, txt in lines:
        p = cell.add_paragraph(); p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
        rt = p.add_run(tag); rt.bold = True; rt.font.name = MONO; rt.font.size = Pt(9)
        rx = p.add_run(txt); rx.font.name = MONO; rx.font.size = Pt(9)
    return t

# =====================================================================
# Title block
# =====================================================================
title = doc.add_paragraph(); title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(10)
r = title.add_run("Pen2STEP: Training-Free Conversion of Hand-Drawn "
                  "Engineering Sketches to Parametric CAD Models via a "
                  "Frozen Vision-Language Model")
r.bold = True; r.font.name = SERIF; r.font.size = Pt(17)

# authors
au = doc.add_paragraph(); au.alignment = WD_ALIGN_PARAGRAPH.CENTER
au.paragraph_format.space_after = Pt(6)
def author(p, name, sup):
    r = p.add_run(name); r.font.name = SERIF; r.font.size = Pt(12)
    rs = p.add_run(sup); rs.font.name = SERIF; rs.font.size = Pt(12); rs.font.superscript = True
author(au, "Cem Baytın", "1"); au.add_run("    ").font.size = Pt(12)
author(au, "Ayberk Göker Üneş", "2"); au.add_run("    ").font.size = Pt(12)
author(au, "Onur Behzat Tokdemir", "3,4,*"); au.add_run("    ").font.size = Pt(12)
author(au, "Fethi Kadıoğlu", "5")

# affiliations
affs = [
    ("1", "Graduate Student, Istanbul Technical University, Istanbul, Türkiye."),
    ("2", "Graduate Student, Istanbul Technical University, Civil Engineering Department, "
          "34469, Istanbul, Türkiye; Email: unes21@itu.edu.tr; ORCID: 0009-0000-3407-4778."),
    ("3", "Assoc. Prof., Istanbul Technical University, Civil Engineering Department, "
          "34469, Istanbul, Türkiye."),
    ("4", "Vice Chair, Artificial Intelligence and Data Science Research Center, "
          "Istanbul Technical University, Türkiye; Email: otokdemir@itu.edu.tr; ORCID: 0000-0002-4101-8560."),
    ("5", "Prof., Istanbul Technical University, Civil Engineering Department, "
          "34469, Istanbul, Türkiye; Email: fkadioglu@itu.edu.tr; ORCID: 0000-0001-7049-1704."),
    ("*", "Corresponding author."),
]
for sup, txt in affs:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1); p.paragraph_format.line_spacing = 1.0
    rs = p.add_run(sup); rs.font.superscript = True; rs.font.name = SERIF; rs.font.size = Pt(8.5)
    rr = p.add_run(" " + txt); rr.font.name = SERIF; rr.font.size = Pt(8.5)

# rule line under header
hr = doc.add_paragraph(); hr.paragraph_format.space_before = Pt(6); hr.paragraph_format.space_after = Pt(6)
pPr = hr._p.get_or_add_pPr(); pbdr = OxmlElement("w:pBdr")
bot = OxmlElement("w:bottom"); bot.set(qn("w:val"), "single"); bot.set(qn("w:sz"), "6")
bot.set(qn("w:space"), "1"); bot.set(qn("w:color"), "808080"); pbdr.append(bot); pPr.append(pbdr)

# abstract
ap = doc.add_paragraph(); ap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
ap.paragraph_format.left_indent = Cm(0.4); ap.paragraph_format.right_indent = Cm(0.4)
ap.paragraph_format.space_after = Pt(6)
rb = ap.add_run("Abstract.  "); rb.bold = True; rb.font.name = SERIF; rb.font.size = Pt(10)
abs = ("Converting a hand-drawn engineering sketch into an editable parametric CAD model "
       "remains a long-standing challenge in design automation. Supervised approaches depend "
       "on large paired corpora that are scarce for free-hand drawings, and fine-tuning "
       "vision-language models requires task-specific data that is even harder to collect. "
       "This paper presents Pen2STEP, a training-free pipeline that wraps a frozen open-weight "
       "vision-language model (VLM) inside a deterministic engineering shell composed of "
       "multi-view composition, OCR-based dimension extraction and prompt injection, sampling of "
       "N candidate CadQuery programs, abstract-syntax-tree (AST) repair, execution-guided solid "
       "selection, and metric scale recovery. No model weights are updated at any stage. The paper "
       "also introduces Pen2STEP-Bench, a synthetic dimension-annotated multi-view dataset together "
       "with 19 genuinely hand-drawn parts paired with verified ground-truth solids, and a "
       "reproducible five-metric evaluation protocol covering STEP validity, Chamfer distance, "
       "dimension error, volume error, and F-score@τ. On 19 real hand-drawn sketches, the deterministic "
       "wrapper raises the STEP Validity Rate from 37% for the bare frozen model to 90% with automatic "
       "dimension OCR and up to 100% under three-candidate sampling, while geometric fidelity remains the "
       "open problem. A component-wise ablation isolates AST repair and candidate sampling as the drivers "
       "of validity, shows that dimension grounding improves geometric fidelity rather than validity, and "
       "identifies handwritten-dimension OCR as the main remaining bottleneck. The code, benchmark data, "
       "and ground-truth models are released.")
ra = ap.add_run(abs); ra.font.name = SERIF; ra.font.size = Pt(10)

kp = doc.add_paragraph(); kp.paragraph_format.left_indent = Cm(0.4); kp.paragraph_format.right_indent = Cm(0.4)
kp.paragraph_format.space_after = Pt(10)
rk = kp.add_run("Keywords:  "); rk.bold = True; rk.font.name = SERIF; rk.font.size = Pt(10)
rk2 = kp.add_run("sketch-to-CAD; training-free inference; vision-language models; "
                 "program synthesis; CadQuery; design automation.")
rk2.font.name = SERIF; rk2.font.size = Pt(10)

# =====================================================================
# 1. Introduction
# =====================================================================
h1("1.  Introduction")
body("Every mechanical design begins with a sketch. Turning that sketch into a parametric and "
     "editable CAD model is slow, error-prone, and requires expertise that many engineers, and "
     "most non-specialists, do not have. Automating the sketch-to-CAD step would shorten the design "
     "cycle, lower the barrier to digital fabrication, and reduce the cost of early-stage decisions, "
     "which account for an estimated 70 to 80% of total project cost [17]. The difficulty of this step "
     "is widely recognized. Camba et al. [1] identify it as the central open problem in sketch-based "
     "modeling for engineering, and Wu et al. [13] map the broader landscape of AI-driven CAD "
     "generation across point clouds, images, and text.")
body("Existing approaches fall into two groups. The first group consists of supervised generative "
     "methods. SkexGen [6] autoregressively generates CAD construction sequences; Free2CAD [2] groups "
     "freehand strokes into extrusion commands; Sketch2Seq [3] recognizes diverse feature types such as "
     "extrude, cut, fillet, and chamfer with a trained graph attention network; CADrawer [4] generates "
     "CadQuery programs autoregressively from 3D sketches; and Text2CAD [5] produces parametric "
     "sequences from text prompts. Each of these methods depends on large paired training datasets, "
     "which are scarce for free-hand drawings and effectively nonexistent for dimension-annotated "
     "multi-view sheets.")
body("The second group consists of approaches based on vision-language and large language models. "
     "Large vision-language models can emit code directly from an image [9, 10], and frozen VLMs can be "
     "adapted to new tasks without any parameter update [12]. Applying this capability to CAD requires "
     "controlling three known failure modes: hallucinated syntax, scale blindness, and limited "
     "multi-view reasoning. Man [17] benchmarks frontier VLMs on CAD code generation and reports "
     "frequent compilation errors and scale failures, even for the strongest models, when they are run "
     "without external scaffolding. Large language models also tend to underperform on domain-specific "
     "syntax [11], and MMCode [10] confirms persistent gaps on visually rich code generation tasks.")
body("The present study follows the VLM-wrapper direction and develops it to its natural conclusion. "
     "Pen2STEP keeps the VLM entirely frozen and concentrates all engineering effort in the "
     "deterministic shell that surrounds it.")
body("Three points distinguish this work from prior art. First, to the authors' knowledge Pen2STEP is "
     "the first system to produce an editable parametric model, namely executable CadQuery exported to a "
     "STEP B-rep, directly from a photograph of a hand-drawn multi-view engineering sheet, with no "
     "training and no vectorization or stroke-order preprocessing; the closest prior systems require "
     "either trained models, vectorized stroke input, or clean 3D sketches, and the closest training-free "
     "study reports CAD code rather than verified solids and fails on metric scale without a shell. "
     "Second, the deterministic shell is not a single trick but a set of individually ablatable stages, "
     "and the analysis separates their roles, which yields the transferable finding that STEP validity is "
     "a wrapper problem whereas geometric fidelity is a dimension-reading problem. Third, the released "
     "Pen2STEP-Bench, a dimension-annotated multi-view dataset with verified ground-truth solids and a "
     "five-metric protocol, is a reusable artifact that the field currently lacks. Section 2.6 positions "
     "Pen2STEP against the closest systems along these axes.")
body("This paper makes three contributions. First, it presents a training-free sketch-to-CAD framework "
     "built around a frozen open-weight VLM, with individually ablatable stages: multi-view composition, "
     "OCR injection, AST repair, and scale recovery. Second, it introduces Pen2STEP-Bench, a synthetic "
     "dimension-annotated multi-view dataset paired with 19 hand-drawn parts (6 dimensioned and 13 "
     "undimensioned) and verified ground-truth solids. Third, it defines a reproducible five-metric "
     "evaluation protocol and reports a component-wise ablation that quantifies the contribution and "
     "failure mode of each stage on both synthetic and real data.")

# =====================================================================
# 2. Related Work
# =====================================================================
h1("2.  Related Work")
h2("2.1.  Sketch-based CAD generation")
body("The field of sketch-based modeling [1] has explored two broad directions: geometry-rule "
     "optimization over vectorized strokes and deep-learning reconstruction. Free2CAD [2] groups "
     "freehand strokes into extrusion operations but requires a specific stroke order and handles only "
     "prismatic shapes. Sketch2Seq [3] advances this line by classifying diverse CAD features through a "
     "multi-branch graph attention network trained on 91K samples of vectorized CAD sketches with "
     "stroke-level labels. CADrawer [4] generates CadQuery programs autoregressively from 3D "
     "architectural sketches using a fine-tuned transformer. All three require either large annotated "
     "training sets or clean vectorized input, and none accepts a raw JPEG photograph of a hand-drawn "
     "multi-view engineering sheet. Willis et al. [19] study synthetic sketch generation as a way to "
     "bootstrap CAD learning, which highlights the data-scarcity problem that the frozen-backbone "
     "approach adopted here sidesteps entirely. Fan et al. [20] release a history-based parametric "
     "sketch dataset with advanced engineering commands, which underlines the growing interest in richer "
     "CAD representations.")
h2("2.2.  Generative CAD via language and code")
body("Text2CAD [5] generates sequential CAD designs from text prompts through a fine-tuned LLM. "
     "SkexGen [6] uses disentangled codebooks for autoregressive construction sequences. UniCAD [7] "
     "introduces a unified benchmark across several modalities and tasks, which exposes the "
     "fragmentation of current evaluation pipelines. ParaCAD-RL [8] trains through reinforcement "
     "learning with compiler verification to generate executable CadQuery from text, which can be "
     "viewed as a supervised counterpart to the zero-shot approach taken here. Man [17] benchmarks "
     "frontier VLMs on image-conditioned CAD code generation and confirms that, without external repair "
     "and execution feedback, even the strongest frozen models fail systematically on metric scale. "
     "Learning CAD primitives from hand-drawn sketches via adversarial networks [22] offers a further "
     "direction, although it remains limited to simple primitives and requires paired sketch data.")
h2("2.3.  3D reconstruction from free-hand sketches")
body("Deep3DSketch-im [15] and SketchSampler [14] produce high-fidelity 3D meshes from single freehand "
     "sketches using learned point-cloud or mesh decoders. DOGREAT3D [16] combines diffusion models "
     "with geometric refinement for complex mechanical part reconstruction from multi-view images. "
     "These methods yield visually compelling outputs, but they produce non-parametric representations "
     "such as meshes and voxels rather than editable B-rep solids exportable to STEP [25], which is the "
     "standard required for downstream manufacturing and CAM toolchains.")
h2("2.4.  Training-free VLM adaptation")
body("Li et al. [12] show that context-aware label propagation can match or exceed fine-tuned VLMs in "
     "zero-shot and few-shot settings without any weight update. Guo et al. [9] demonstrate zero-shot "
     "visual question answering with entirely frozen LLMs by bridging images to text prompts. Both "
     "results support the decision to keep the VLM frozen and to invest in the deterministic wrapper "
     "rather than in task-specific fine-tuning.")
h2("2.5.  Evaluation metrics")
body("Goranci et al. [21] study efficient algorithms for Chamfer distance; the standard static "
     "symmetric variant is used in this study. F-score@τ provides a precision-recall balance that is "
     "robust to outlier vertices and that is more stable than voxel IoU for B-rep solids of varying "
     "complexity, as observed across the present benchmark.")

h2("2.6.  Positioning relative to prior work")
body("Table 1 places Pen2STEP against the closest sketch-based and code-based CAD systems along five "
     "axes that matter for the target setting: whether the method is training-free, the required input, "
     "the output representation, whether absolute dimensions are read, and whether a benchmark is "
     "released. Pen2STEP is the only entry that is simultaneously training-free, accepts a photograph "
     "of a hand-drawn multi-view sheet, returns an editable parametric STEP solid, reads dimensions, and "
     "releases its benchmark. The comparison is one of scope rather than a direct accuracy ranking, since "
     "the other systems target different inputs and report on different corpora; their accuracy is not "
     "directly comparable to results obtained from raw photographs of free-hand sheets.")
caption("Table 1.", "Positioning of Pen2STEP against the closest sketch- and code-based CAD systems. "
        "Pen2STEP is the only system that is training-free, accepts a photograph of a hand-drawn "
        "multi-view sheet, outputs an editable parametric STEP solid, reads dimensions, and releases a "
        "benchmark.")
add_table(
    ["Method", "Train-free", "Input", "Output", "Dim-aware", "Bench."],
    [["Pen2STEP (ours)", "Yes", "Photo of hand-drawn multi-view sheet", "Parametric STEP B-rep", "Yes (OCR)", "Yes"],
     ["Free2CAD [2]", "No", "Ordered freehand strokes (vector)", "Extrusion commands", "No", "No"],
     ["Sketch2Seq [3]", "No", "Vectorized sketch (91K labels)", "Feature sequence", "No", "No"],
     ["CADrawer [4]", "No", "Clean 3D sketch", "CadQuery program", "No", "No"],
     ["Text2CAD [5]", "No", "Text prompt", "CAD sequence", "Partial", "Yes"],
     ["VisionCAD [17]", "Yes (no shell)", "Single image", "CAD code (scale fails)", "No", "Yes"]],
    [2.9, 1.8, 4.2, 3.6, 1.7, 1.8],
    bold_cells={(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)},
    size=8.5, mono_first=False)
doc.add_paragraph().paragraph_format.space_after = Pt(2)

# Figure 1
add_image(SCRATCH + r"\fig_pipeline.png", CONTENT_CM,
          "Figure 1.",
          "The Pen2STEP pipeline. The VLM (top right) is entirely frozen, and every surrounding "
          "stage is a deterministic, training-free module. OCR-extracted dimensions are injected as "
          "textual constraints; AST repair and execution-guided selection handle VLM syntax errors; "
          "and scale recovery restores metric units.")

# =====================================================================
# 3. The Pen2STEP Framework
# =====================================================================
h1("3.  The Pen2STEP Framework")
body("Figure 1 shows the complete pipeline. Given one or more sketch images, Pen2STEP returns a "
     "valid STEP solid, or a failure flag, without updating any model weight.")
h2("3.1.  Multi-view composition")
body("A single orthographic view is geometrically ambiguous, and VLMs struggle to reason consistently "
     "across several separate images [10]. All available views, whether front, top, and side panels or "
     "a single annotated A4 sheet, are therefore composed into one labelled canvas on a white "
     "background with panel text labels. This composition preserves cross-view correspondence while "
     "keeping the input within the single-image processing path of the model.")
h2("3.2.  Dimension OCR and prompt injection")
body("VLMs are scale-blind: they can infer plausible proportions but not absolute sizes [17]. Metric "
     "scale is therefore recovered directly from the drawing. An offline OCR engine [24] reads the "
     "annotated canvas, and only pure-numeric tokens above a confidence threshold θ = 0.45 are kept. "
     "These tokens are filtered to the range [1, 10000] mm and injected into the VLM prompt as an "
     "explicit constraint (“use these exact millimetre values for the corresponding edges; do not "
     "invent other sizes”).")
body("A plausibility floor protects this pathway against spurious readings. A part drawn on A4 cannot "
     "realistically have a largest dimension of only a few millimetres. If the maximum OCR reading "
     "falls below m = 10 mm, the entire reading set is treated as unreliable and discarded. This rule "
     "suppresses false positives from stray ticks and line-end markers, a known problem for "
     "general-purpose OCR on engineering drawings [24], and it also catches centimetre annotations that "
     "are misread as millimetres, for example 8 cm parsed as 8 mm.")
h2("3.3.  Candidate generation and AST repair")
body("The composed image and the prompt are passed to a frozen open-weight VLM (LLaVA-1.5-style, 13B) "
     "that generates N candidate CadQuery [23] programs (i = 0 greedy, i > 0 sampled at temperature "
     "0.5). Raw VLM output is often almost valid Python, which is consistent with reports that LLMs "
     "struggle with domain-specific syntax [11, 18]. Each candidate then passes through an AST-level "
     "repair stage that (i) balances parentheses, brackets, and quotes; (ii) strips trailing lines that "
     "cause parse failures; (iii) renames a bare result expression to the expected variable; and "
     "(iv) inserts a missing `import cadquery as cq` header.")
h2("3.4.  Execution-guided selection")
body("Each repaired program is executed in a sandboxed subprocess with a 30-second timeout. Candidates "
     "that raise exceptions, time out, or yield no positive-volume solid are discarded. Among the "
     "survivors, the candidate whose bounding-box extents best match the OCR dimension set is selected, "
     "using the minimum ℓ¹ error over sorted extents. When no reliable dimensions are available, the "
     "first valid candidate is taken.")
h2("3.5.  Scale recovery")
body("A footer appended at execution time inspects the bounding-box diagonal. If the largest extent of "
     "the solid is below 10 mm, the solid is scaled uniformly so that its longest edge equals the "
     "maximum OCR dimension, falling back to a canonical 100 mm when the OCR readings were discarded. "
     "The scaled B-rep is then exported to STEP [25].")
add_algorithm()
doc.add_paragraph().paragraph_format.space_after = Pt(2)

# =====================================================================
# 4. Pen2STEP-Bench
# =====================================================================
h1("4.  Pen2STEP-Bench")
h2("4.1.  Synthetic split")
body("Parts are generated procedurally from parametric families, namely blocks, cylinders, L-profiles, "
     "T-profiles, and stepped shafts, and each part is rendered as a three-view orthographic sheet with "
     "bounding-box extents printed as ground-truth dimension annotations. Mild hand-drawing "
     "augmentation, including stroke jitter, line-width variation, and a paper-texture overlay, narrows "
     "the sim-to-real gap. Every sample carries its generating CadQuery code, which yields exact "
     "ground-truth solids.")
h2("4.2.  Real hand-drawn split")
body("Nineteen parts were produced by hand by four of the authors, in black ink on A4 paper, each as a "
     "three-view orthographic sheet (Figure 2). Six parts carry millimetre dimensions (dimensioned, D); "
     "the remaining 13 are deliberately left undimensioned (U) to reflect the common practice of "
     "omitting annotations. A ground-truth CadQuery model was authored and visually verified for every "
     "part, and all 19 compile to valid solids. Undimensioned parts are scaled so that their longest "
     "edge is approximately 100 mm, which matches the canonical fallback of the framework.")
h2("4.3.  Evaluation protocol")
body("Let P and G be point sets, with n_s = 8192 points each, sampled uniformly from the predicted and "
     "the ground-truth surfaces and both mean-centred. Five complementary metrics are reported:")
bullet("**SVR**: STEP Validity Rate, the fraction of inputs that yield an openable, positive-volume solid.")
bullet("**Chamfer** (d_CD, mm): symmetric mean nearest-neighbour distance [21].")
bullet("**DimE**: mean relative error of the sorted bounding-box extents against ground truth.")
bullet("**VolE**: relative error of the predicted volume against the ground-truth volume.")
bullet("**F@τ**: F-score at threshold τ = 0.02·‖bbox(G)‖, defined as")
add_image(SCRATCH + r"\fig_eq_fscore.png", 14.0)
body("following standard practice in 3D reconstruction evaluation. Because the surface sampling is "
     "stochastic, identical solids score F ≈ 0.95 rather than 1.0, which is the practical ceiling. "
     "Failed predictions contribute F = 0 and d_CD = ∞, which penalises invalid outputs without "
     "discarding samples.")

# =====================================================================
# 5. Experiments
# =====================================================================
h1("5.  Experiments")
h2("5.1.  Setup")
body("The backbone is a frozen open-weight LLaVA-1.5-style 13B vision-language model loaded in "
     "`bfloat16` on a single GPU. OCR runs on the CPU to preserve VRAM, and CadQuery [23] executes in "
     "isolated subprocesses. Five cumulative conditions are ablated: `raw_iso` (a single isometric "
     "view, with no wrapper), `repair_iso` (AST repair and scale recovery added), `multiview` (the "
     "three-view prompt added), `full_ocr` (OCR dimensions added, N = 3), and `full_gt` (ground-truth "
     "dimensions injected, N = 3), which serves as an oracle upper bound on the dimension pathway. Two "
     "further conditions support the analysis on real data: `raw_mv`, the composed three-view sheet "
     "passed to the frozen model with no deterministic shell, which serves as the real-data baseline "
     "since the real parts have no single isometric image; and `multiview_n3`, identical to `multiview` "
     "but with N = 3, which serves as an equal-N control.")
body("The fixed hyperparameters are set conservatively, and the two most influential ones are ablated "
     "rather than assumed. The candidate budget N is the dominant inference-time control, and its effect "
     "is reported directly by the N = 1 against N = 3 rows of Table 3, which show that most of the "
     "validity gain from sampling is already captured at N = 3. The OCR plausibility floor m = 10 mm is "
     "ablated in Table 4. The remaining values follow common practice: the OCR confidence threshold "
     "θ = 0.45 retains high-precision numeric tokens without discarding faint handwritten digits, and the "
     "sampling temperature T = 0.5 introduces candidate diversity without the degeneracy observed at "
     "higher temperatures. The 30-second execution timeout was never reached in practice.")
body("All results in this paper use the same frozen model in bfloat16; the batch evaluations were "
     "produced on a single NVIDIA A100 GPU, and the same configuration runs offline on a consumer laptop "
     "GPU, since no training is performed at any stage. The model revision, the deterministic shell, the "
     "benchmark, the ground-truth solids, and the evaluation scripts are released, and the metrics "
     "reported here are latency-insensitive and therefore not hardware-dependent.")
h2("5.2.  Synthetic ablation (n = 50)")
body("Table 2 reports the cumulative results, and three patterns can be observed.")
body("First, AST repair is the dominant contributor. Adding repair to the raw baseline nearly doubles "
     "the SVR (0.26 → 0.52) and halves the Chamfer distance, which confirms that raw VLM output is "
     "syntactically broken in roughly half of the cases. This finding is consistent with LLM-DSL "
     "benchmarks [10, 11] showing that domain-specific syntax is consistently harder than "
     "general-purpose code.")
body("Second, OCR dimension injection lifts the SVR to 0.88. With N = 3 candidates and grounded "
     "dimension constraints, the model produces compilable and well-scaled code more reliably.")
body("Third, full_gt does not dominate full_ocr at n = 50. At this sample size the gap falls within "
     "run-to-run noise, and both conditions indicate that correct metric scale improves DimE and VolE "
     "more than it improves raw validity.")

caption("Table 2.", "Synthetic ablation (n = 50). The pipeline is cumulative; arrows indicate the "
        "preferred direction. The best value per column is in bold.")
add_table(
    ["Condition", "SVR ↑", "Cham. ↓", "DimE ↓", "VolE ↓", "F ↑"],
    [["raw_iso", "0.260", "73.6", "0.992", "1.000", "0.000"],
     ["repair_iso", "0.520", "37.9", "0.430", "1.359", "0.083"],
     ["multiview", "0.540", "50.0", "0.620", "0.968", "0.040"],
     ["full_ocr", "0.880", "49.8", "0.433", "0.868", "0.061"],
     ["full_gt", "0.780", "47.2", "0.439", "0.894", "0.067"]],
    [3.6, 2.48, 2.48, 2.48, 2.48, 2.48],
    bold_cells={(3, 1), (1, 2), (1, 3), (2, 4), (1, 5)})
doc.add_paragraph().paragraph_format.space_after = Pt(2)

h2("5.3.  Real hand-drawn results (n = 19)")
body("Table 3 separates the contribution of the deterministic wrapper from those of candidate sampling "
     "and dimension grounding. The frozen model applied to the composed sheet with no wrapper (raw_mv) "
     "produces a valid STEP solid for only 36.8% of inputs and reaches F = 0.000. Adding the "
     "deterministic shell (multiview, N = 1) raises validity to 78.9% and F to 0.107, which isolates AST "
     "repair and scale recovery as the main drivers of validity on real data, in agreement with the "
     "synthetic ablation.")
body("Raising the candidate budget of that same configuration to N = 3 (multiview, N = 3) lifts validity "
     "to 100% on the 19-part set. The validity advantage previously attributed to dimension injection is "
     "therefore largely a best-of-N effect: at equal N = 3, the no-dimension configuration is at least "
     "as valid as the dimensioned ones (1.000 versus 0.895 for full_ocr and 0.947 for full_gt). "
     "Dimension constraints slightly reduce validity, because they add ways for a candidate to be "
     "rejected.")
body("At equal candidate budget, dimension grounding instead improves geometric fidelity. Moving from no "
     "dimensions to OCR to ground truth steadily lowers DimE (0.526, 0.512, 0.422) and Chamfer (26.4, "
     "24.9, 24.0 mm) and raises F (0.095, 0.103, 0.119). The gain from automatic OCR is small "
     "(F = 0.095 to 0.103), whereas ground-truth dimensions deliver the full improvement (F = 0.119). "
     "This identifies handwritten-dimension OCR, rather than the backbone or the wrapper, as the binding "
     "constraint on accuracy.")
caption("Table 3.", "Real hand-drawn set (n = 19), with the no-wrapper baseline (raw_mv) and an "
        "equal-N control (multiview at N = 3). N is the number of sampled candidates; full_gt is the "
        "correct-dimension oracle. The best value per column is in bold.")
add_table(
    ["Condition", "SVR ↑", "Cham. ↓", "DimE ↓", "VolE ↓", "F ↑"],
    [["raw_mv (N=1)", "0.368", "44.2", "0.996", "1.000", "0.000"],
     ["multiview (N=1)", "0.789", "26.8", "0.559", "1.434", "0.107"],
     ["multiview (N=3)", "1.000", "26.4", "0.526", "1.277", "0.095"],
     ["full_ocr (N=3)", "0.895", "24.9", "0.512", "0.885", "0.103"],
     ["full_gt (N=3)", "0.947", "24.0", "0.422", "0.904", "0.119"]],
    [4.0, 2.4, 2.4, 2.4, 2.4, 2.4],
    bold_cells={(2, 1), (4, 2), (4, 3), (3, 4), (4, 5)})
doc.add_paragraph().paragraph_format.space_after = Pt(2)

h2("5.4.  OCR robustness on handwriting")
body("Hand-drawn annotations challenge OCR in two ways: false positives on undimensioned sheets, where "
     "stray ticks are misread as small digits, and unit ambiguity, where centimetre annotations are "
     "misinterpreted as millimetres. Without the plausibility floor, spurious readings of 2 mm or less "
     "cause scale recovery to shrink the predicted solids to millimetre size, which collapses the "
     "F-score to zero for several parts. Table 4 quantifies the effect: the F-score improves by 41% "
     "(0.073 → 0.103) and the Chamfer distance drops by 24% (32.6 → 24.9 mm). The small decrease in "
     "SVR (0.947 → 0.895) reflects cases in which an unreliable reading happened to guide the model "
     "toward a valid program; removing it forces a fallback to the no-dimension path with N = 3.")
caption("Table 4.", "Effect of the OCR plausibility floor on full_ocr (n = 19). The best value per "
        "column is in bold.")
add_table(
    ["Variant", "SVR", "Cham. ↓", "DimE ↓", "F ↑"],
    [["Naive reader", "0.947", "32.6", "0.654", "0.073"],
     ["With floor", "0.895", "24.9", "0.512", "0.103"]],
    [4.6, 2.85, 2.85, 2.85, 2.85],
    bold_cells={(1, 2), (1, 3), (1, 4)})
doc.add_paragraph().paragraph_format.space_after = Pt(2)

kf = doc.add_paragraph(); kf.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
kf.paragraph_format.space_before = Pt(4); kf.paragraph_format.space_after = Pt(6)
add_runs(kf, "**Key finding.** Wrapped with multi-view composition, AST repair, execution feedback and "
             "three-candidate sampling, a frozen VLM produces a valid STEP solid for up to 100% of the "
             "19 real hand-drawn sketches, and for 90% with automatic dimension OCR, against 37% for the "
             "bare model. STEP validity is therefore largely solved by the deterministic wrapper, while "
             "geometric fidelity (F-score near 0.12) remains the open problem. At equal candidate "
             "budget, dimension grounding improves fidelity but not validity, and automatic OCR captures "
             "only a small part of the improvement available from correct dimensions, which makes "
             "handwritten-dimension OCR the highest-value target for future work.")

h2("5.5.  Qualitative results")
body("Figure 2 shows all 19 parts. Prismatic parts, such as blocks, plates, and stepped shafts, and "
     "simple revolves, such as tubes and flanges, are reconstructed faithfully. Chamfers, tapers, "
     "hexagonal cross-sections, and undercuts remain the main failure modes, which is consistent with "
     "the pretraining distribution of the backbone.")
add_image(FIGDIR + r"\fig_real_testset.png", CONTENT_CM,
          "Figure 2.",
          "The 19-part real hand-drawn test set. Each panel pairs the input sketch (left) with the "
          "ground-truth CAD model (right). Dimensioned (D) and undimensioned (U) parts are labelled.")

# =====================================================================
# 6. Discussion
# =====================================================================
h1("6.  Discussion")
h2("6.1.  Backbone ceiling")
body("The frozen 13B VLM represents mid-2024 open-weight capabilities. Stronger backbones, or models "
     "with deeper exposure to engineering drawings during pretraining, would benefit the pipeline "
     "directly at zero training cost. UniCAD [7] and ParaCAD-RL [8] illustrate how quickly the field is "
     "advancing, and the training-free design naturally inherits future backbone improvements.")
h2("6.2.  The handwriting-OCR bottleneck")
body("At equal candidate budget (N = 3), automatic OCR raises F from 0.095 with no dimensions to only "
     "0.103, whereas ground-truth dimensions reach 0.119. The gap between full_gt and full_ocr "
     "(ΔF = 0.016, Δd_CD = 0.9 mm on n = 19) therefore quantifies the headroom available from better "
     "OCR, and the small gap between full_ocr and the no-dimension configuration shows how little of "
     "that headroom current OCR recovers. Unit-aware reading (cm against mm), spatial grouping of "
     "dimension annotations, and specialised handwriting recognition [24] are the most direct paths "
     "forward.")
h2("6.3.  Comparison with supervised methods")
body("Sketch2Seq [3] requires 91K training samples and vectorized stroke input, and CADrawer [4] "
     "requires a fine-tuned transformer and clean 3D sketch input. Both outperform Pen2STEP on their "
     "respective benchmarks, but neither accepts a JPEG photograph of a hand-drawn sheet without a "
     "preprocessing pipeline, which is precisely the target input here. Pen2STEP and supervised "
     "methods are therefore complementary: the approach proposed here fills the zero-infrastructure "
     "niche, while supervised methods excel when training data and structured input are available.")
h2("6.4.  Evaluation caveats")
body("The best-of-N confound is now controlled directly. Running the no-dimension configuration at "
     "N = 3 (Table 3) shows that its validity matches or exceeds the dimensioned configurations, so the "
     "earlier validity ordering reflected candidate budget rather than constraint quality. The remaining "
     "caveat is sample size: at n = 19, a difference of one part corresponds to roughly 0.05 SVR, so the "
     "small inversions among the N = 3 conditions fall within run-to-run variance, and a larger real set "
     "is the priority for future evaluation.")
h2("6.5.  Practical significance")
body("Even with geometric fidelity still open, the result has practical value. A valid, editable "
     "parametric solid is a usable starting point for a designer, who can correct a few dimensions far "
     "faster than modelling a part from scratch, whereas a mesh or a point cloud cannot be edited "
     "parametrically at all. Because the backbone is frozen and used offline, the pipeline runs on a "
     "single laptop with no training data, no annotation effort, and no cloud dependency, which is the "
     "setting in which supervised sketch-to-CAD systems are hardest to deploy. The contribution is thus "
     "a deployable lower bound that improves automatically as open VLMs and handwriting OCR advance.")

# =====================================================================
# 7. Conclusion
# =====================================================================
h1("7.  Conclusion")
body("This study shows that disciplined inference-time engineering around a frozen VLM, combining "
     "multi-view composition, OCR dimension grounding, AST repair, execution-guided selection, and "
     "scale recovery, produces a valid parametric CAD solid for up to 100% of the 19 real inputs under "
     "three-candidate sampling, against 37% for the bare frozen model, with no training and no "
     "preprocessing infrastructure beyond a camera phone. Alongside Pen2STEP-Bench and a reproducible "
     "five-metric protocol, the ablation credits AST repair and candidate sampling with the validity "
     "gains, shows that dimension grounding improves geometric fidelity rather than validity, and "
     "identifies handwritten-dimension OCR as the next frontier, since geometric accuracy (F-score near "
     "0.12) remains well below the practical ceiling. The code, benchmark data, and ground-truth models "
     "are released to support reproduction and future work.")

# =====================================================================
# References
# =====================================================================
h1("References")
refs = [
 "Camba, J. D., Company, P., & Naya, F. (2022). Sketch-based modeling in mechanical engineering design: Current status and opportunities. Computer-Aided Design, 150, 103283.",
 "Li, C., Pan, H., Bousseau, A., & Mitra, N. J. (2022). Free2CAD: Parsing freehand drawings into CAD commands. ACM Transactions on Graphics (SIGGRAPH), 41(4).",
 "Sun, Y., Li, J., Xu, Z., Zhang, J., Liu, X., Zhang, D., & Lu, G. (2025). Sketch2Seq: Reconstruct CAD models from feature-based sketch segmentation. IEEE Transactions on Visualization and Computer Graphics, 31(10), 8214.",
 "Li, Y., Manfredi, G., Kriel, H., Hao, C., Xu, X., Bousseau, A., & Ritchie, D. (2026). CADrawer: Autoregressive CAD generation from 3D sketches. Computer Graphics Forum (Eurographics).",
 "Khan, M. S., Sinha, S., Sheikh, T. U., Stricker, D., Ali, S. A., & Afzal, M. Z. (2024). Text2CAD: Generating sequential CAD designs from beginner-to-expert level text prompts. Advances in Neural Information Processing Systems (NeurIPS).",
 "Xu, X., Willis, K. D. D., Lambourne, J. G., Cheng, C.-Y., Jayaraman, P. K., & Furukawa, Y. (2022). SkexGen: Autoregressive generation of CAD construction sequences with disentangled codebooks. Proceedings of the International Conference on Machine Learning (ICML).",
 "Chen, J., Jin, S., Sun, H., Liu, W., & Qian, C. (2026). UniCAD: A unified benchmark and universal model for multi-modal multi-task CAD. arXiv preprint arXiv:2606.05058.",
 "Maniyar, S. (2026). ParaCAD-RL: Parametric CAD code generation via feature tree convention and compiler-verified reinforcement learning. arXiv preprint.",
 "Guo, J., Li, J., Li, D., Tiong, A. M. H., Li, B., Tao, D., & Hoi, S. (2023). From images to textual prompts: Zero-shot visual question answering with frozen large language models. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).",
 "Li, K., Tian, Y., Hu, Q., Luo, Z., Huang, Z., & Ma, J. (2024). MMCode: Benchmarking multimodal large language models in code generation with visually rich programming problems. Findings of the Association for Computational Linguistics: EMNLP.",
 "Joel, S., Wu, J., & Fard, F. (2024). A survey on LLM-based code generation for low-resource and domain-specific programming languages. arXiv preprint arXiv:3770084.",
 "Li, Y., Su, Y., Goodge, A., Jia, K., & Xu, X. (2025). Efficient and context-aware label propagation for zero-/few-shot training-free adaptation of vision-language models. Proceedings of the International Conference on Learning Representations (ICLR).",
 "Wu, W., Wu, K., Xing, S., Li, Y., Fu, X.-M., Chen, F., & Liu, L. (2026). AI-driven generation of 3D CAD models: A survey. Computational Visual Media, 12(3), 575–614.",
 "Gao, C., Wang, X., Yu, Q., Sheng, L., Zhang, J., Han, X., Song, Y.-Z., & Xu, D. (2024). 3D reconstruction from a single sketch via view-dependent depth sampling. IEEE Transactions on Pattern Analysis and Machine Intelligence, 46(12), 9661.",
 "Chen, T., Cao, R., Li, Z., Zang, Y., & Sun, L. (2024). Deep3DSketch-im: Rapid high-fidelity AI 3D model generation by single freehand sketches. Frontiers of Information Technology & Electronic Engineering, 25(1), 149–159.",
 "Liang, X., Wang, Z., Liu, J., Liu, A., & Chen, C.-H. (2026). DOGREAT3D: Multimodal 3D reconstruction of complex mechanical parts with diffusion models and geometric refinement strategies. Journal of Manufacturing Systems, 86, 586–599.",
 "Man, K. Y. B. (2025). From sketch to CAD code: Multimodal AI for controllable design generation [Master’s thesis]. Massachusetts Institute of Technology.",
 "Gulwani, S. (2010). Dimensions in program synthesis. Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), invited talk.",
 "Willis, K. D. D., Jayaraman, P. K., Lambourne, J. G., Chu, H., & Pu, Y. (2021). Engineering sketch generation for computer-aided design. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW).",
 "Fan, R., He, F., Liu, Y., & Lin, J. (2025). A history-based parametric CAD sketch dataset with advanced engineering commands. Computer-Aided Design, 182, 103848.",
 "Goranci, G., Jiang, S. H.-C., Kiss, P., Szilagyi, E., & Yang, Q. (2025). Fully dynamic algorithms for Chamfer distance. Advances in Neural Information Processing Systems (NeurIPS).",
 "Learning CAD primitives from hand-drawn sketches via generative neural network. (2024). SSRN preprint. (Author names redacted in preprint.)",
 "CadQuery Developers. (2024). CadQuery: A Python parametric CAD scripting framework. https://github.com/CadQuery/cadquery",
 "JaidedAI. (2023). EasyOCR: Ready-to-use OCR with 80+ languages. https://github.com/JaidedAI/EasyOCR",
 "International Organization for Standardization. (2016). ISO 10303-21: Industrial automation systems and integration. Product data representation and exchange (STEP).",
]
for i, ref in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("[%d]  " % i); r.font.name = SERIF; r.font.size = Pt(9.5)
    r2 = p.add_run(ref); r2.font.name = SERIF; r2.font.size = Pt(9.5)

doc.save(OUT)
print("saved:", OUT)
