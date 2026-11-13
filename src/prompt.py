"""Prompt constants shared by the interactive demo and the ablation driver.

Single source of truth: `app.py` and `src/run_baselines.py` must issue byte-identical
instructions, otherwise the demo and the reported numbers are not comparable.

No weight of the backbone is updated anywhere in this repository. These strings are the
entire task-specific conditioning of the frozen model; everything else is deterministic.
"""

INSTRUCTION = (
    "Look at this hand-drawn technical sketch and identify the geometric shape. "
    "Write SHORT CadQuery Python code using simple primitives: "
    "cq.Workplane('XY').box(), .cylinder(), .extrude(), .union(), .cut(). "
    "Estimate reasonable round integer dimensions in millimeters. "
    "Output ONLY Python code - no markdown, no backticks, no explanation. "
    "Keep the code under 30 lines. "
    "Store the final shape in a variable called 'result'. "
    "Example for a box: result = cq.Workplane('XY').box(100, 50, 30)"
)

CHAT_TEMPLATE = (
    "A chat between a curious user and an artificial intelligence assistant. "
    "The assistant gives helpful, detailed, and polite answers to the user's questions. "
    "USER: <image>\n{instruction} ASSISTANT:"
)

# Çoklu-görünüm açıklaması (framework'ün multi-view füzyon sütunu)
MULTIVIEW_CLAUSE = (
    " The image is a technical drawing sheet showing multiple labeled "
    "orthographic views (ON=front, UST=top, YAN=side) of the SAME single "
    "part. Combine ALL views to infer the correct 3D geometry."
)


def build_prompt(dim_hint: str = "", multiview: bool = False) -> str:
    """Modele verilecek tam prompt dizesini döndürür (cevap kısmı hariç).

    dim_hint  : OCR ile çıkarılan boyutların enjekte edileceği cümle (opsiyonel).
    multiview : Girdi çoklu-görünüm sayfası ise açıklama eklenir.
    """
    instr = INSTRUCTION
    if multiview:
        instr += MULTIVIEW_CLAUSE
    if dim_hint:
        instr += dim_hint
    return CHAT_TEMPLATE.format(instruction=instr)


# ── Kısa/minimal talimat (hakem yanıtı, A7a) ─────────────────────────────────
# Düzeltme: CAD-Coder'ın (Doris et al., 2025) resmî çıkarım istemi kamuya açıktır:
# github.com/anniedoris/CAD-Coder, inference/cadquery_test_data_subset100.jsonl
# ("Generate the CADQuery code needed to create the CAD for the provided image.
# Just the code, no other words.", conv-mode vicuna_v1, sıcaklık 0, 3450 token;
# scripts/v1_5/eval/test_gencadcode.sh). Daha önce burada yazan "kamuya açık değil"
# notu yanlıştı. Resmî istemle resmî betiğin bu çizimlerdeki sonucu için bkz.
# tools/official_cadcoder/. Aşağıdaki kısa talimat resmî istem DEĞİLDİR; yalnız
# bizim 80 kelimelik talimatımızın etkisini sınamak için yazılmış bir varyanttır.
SHORT_INSTRUCTION = (
    "Generate CadQuery Python code for this CAD shape. "
    "Store the final shape in a variable called 'result'."
)


def build_short_prompt(multiview: bool = False) -> str:
    """Kısa/minimal talimat varyantı (native-prompt ablasyonu, A7a).

    Ana INSTRUCTION'dan farklı olarak: primitif listesi, uzunluk sınırı, ve
    markdown yasağı yok — CAD-Coder'ın kendi kısa örnek kullanım stiline
    (bkz. HF Space placeholder: "create a rectangular plate ...") daha yakın.
    Resmî CAD-Coder istemi değildir (bkz. yukarıdaki not ve tools/official_cadcoder/).
    """
    instr = SHORT_INSTRUCTION
    if multiview:
        instr += MULTIVIEW_CLAUSE
    return CHAT_TEMPLATE.format(instruction=instr)
