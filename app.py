import os
import sys
import time
from pathlib import Path

import torch
import gradio as gr
from PIL import Image
from transformers import (
    LlavaNextForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
)

# ─── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"
WORK_DIR = BASE_DIR / "outputs" / "_work"
OUTPUT_DIR.mkdir(exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BASE_DIR))
from src.framework import sketch_to_cad, FrameworkConfig
from src import dimensions as dim_mod

MODEL_ID = "StoryGold/bella-v1.0-13b"

# ─── GPU bilgisi ──────────────────────────────────────────────────────────────

print("=" * 60)
print("Pen2STEP — SKETCH → CAD (training-free framework)")
print("=" * 60)

cuda_ok = torch.cuda.is_available()
print(f"CUDA  : {'✓' if cuda_ok else '✗  (GPU BULUNAMADI)'}")
if cuda_ok:
    dev = torch.cuda.get_device_properties(0)
    print(f"GPU   : {dev.name}  ({dev.total_memory / 1e9:.1f} GB)")
print(f"OCR   : {'✓ easyocr' if dim_mod.ocr_available() else '✗ (boyut okuma devre dışı — pip install easyocr)'}")

# ─── Model yükleme (açılışta bir kez) ─────────────────────────────────────────

print(f"\nModel yükleniyor : {MODEL_ID}")
print("İlk çalıştırmada ~26 GB indirilecek, lütfen bekleyin...\n")

_bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = LlavaNextForConditionalGeneration.from_pretrained(
    MODEL_ID,
    quantization_config=_bnb,
    device_map="auto",
    low_cpu_mem_usage=True,
)
model.eval()

print("\n[HAZIR] Model yüklendi — Gradio arayüzü başlatılıyor...\n")


# ─── Frozen VLM üretim fonksiyonu (framework'e takılır) ───────────────────────

@torch.inference_mode()
def _generate(composed_image, prompt, sample_idx: int) -> str:
    inputs = processor(
        text=prompt, images=composed_image, return_tensors="pt"
    ).to(model.device)
    kw = dict(
        max_new_tokens=1280,         # kodu tamamlamaya yeter; foto küçültme ile KV rahat
        repetition_penalty=1.15,     # tekrarlayan döngüleri (ramble) baskıla
        pad_token_id=processor.tokenizer.eos_token_id,
    )
    if sample_idx == 0:
        kw["do_sample"] = False                      # ilk aday: deterministik
    else:
        kw.update(do_sample=True, temperature=0.5, top_p=0.9)  # çeşitlilik
    out = model.generate(**inputs, **kw)
    return processor.decode(out[0], skip_special_tokens=True)


def _ocr(composed_image):
    return dim_mod.extract_dimensions(composed_image)


# ─── Gradio ana işleyici ──────────────────────────────────────────────────────

def _resize_max(img, max_side=1280):
    """En uzun kenarı max_side'a indir — telefon fotoğrafları çok büyük; VLM token
    sayısı ve KV cache patlayıp üretimi yavaşlatıyor. 1280px OCR için yeterli."""
    w, h = img.size
    m = max(w, h)
    if m > max_side:
        s = max_side / m
        img = img.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    return img


def _collect_images(files, webcam_img):
    images = []
    if files:
        for fp in files:
            try:
                images.append(_resize_max(Image.open(fp).convert("RGB")))
            except Exception:
                pass
    if webcam_img is not None:
        images.append(_resize_max(webcam_img.convert("RGB")))
    return images


def _step_to_stl(step_path, out_path):
    """Üretilen STEP'i 3B önizleme için STL'e çevir (gr.Model3D gösterir)."""
    if not step_path or not os.path.exists(step_path):
        return None
    try:
        import cadquery as cq
        cq.exporters.export(cq.importers.importStep(step_path), str(out_path))
        return str(out_path) if os.path.exists(out_path) else None
    except Exception:
        return None


def process(files, webcam_img, n_candidates, use_dims):
    # çıktı sırası: composed, code, dims, status, step, py, model3d(STL)
    images = _collect_images(files, webcam_img)
    if not images:
        yield (None, "", "", "⚠  En az bir görsel yükleyin (veya webcam ile çekin).",
               None, None, None)
        return

    nv = "çoklu görünüm" if len(images) > 1 else "tek görsel"
    yield (None, "", "",
           f"⏳  {len(images)} görsel ({nv}) işleniyor — OCR + {int(n_candidates)} aday üretiliyor...\n"
           "(RTX 4080 Laptop'ta aday başına ~1–3 dk)",
           None, None, None)

    cfg = FrameworkConfig(
        n_candidates=int(n_candidates),
        use_dimensions=bool(use_dims),
        use_repair=True,
        scale_recover=True,
    )

    try:
        res = sketch_to_cad(images, _generate, cfg, str(WORK_DIR), ocr_fn=_ocr)
    except Exception as exc:
        yield (None, "", "", f"❌  Framework hatası: {exc}", None, None, None)
        return

    composed = res["composed"]
    dims_txt = (", ".join(str(int(d)) if float(d).is_integer() else f"{d:g}"
                          for d in res["dims"]) + " mm") if res["dims"] else "(boyut okunamadı)"

    best = res["best"]
    if best is None:
        # Hiç geçerli aday yok → ilk adayın kodunu + hatasını göster
        first = res["candidates"][0] if res["candidates"] else None
        code = first["code"] if first else ""
        err = first["error"] if first else "aday üretilemedi"
        yield (composed, code, dims_txt,
               f"❌  {len(res['candidates'])} adayın hiçbiri geçerli STEP üretmedi.\n"
               f"Son hata: {str(err)[:300]}", None, None, None)
        return

    # Başarılı: kodu + STEP'i kaydet
    ts = int(time.time() * 1000)
    py_out = OUTPUT_DIR / f"vericad_{ts}.py"
    py_out.write_text("import cadquery as cq\n\n" + best["code"], encoding="utf-8")

    # 3B önizleme için STL üret (gr.Model3D)
    stl_out = _step_to_stl(best["step"], OUTPUT_DIR / f"vericad_{ts}.stl")

    bb = best["bbox"]
    bb_txt = f"{bb[0]:.1f} × {bb[1]:.1f} × {bb[2]:.1f} mm" if bb else "?"
    kb = os.path.getsize(best["step"]) / 1024 if best["step"] else 0
    repairs = ", ".join(best["repairs"]) if best["repairs"] else "yok"

    status = (
        f"✓ STEP hazır — {kb:.1f} KB  •  boyut: {bb_txt}\n"
        f"Seçilen aday: #{best['idx']+1}/{len(res['candidates'])}  "
        f"(geçerli: {res['n_valid']})  •  onarım: {repairs}\n"
        f"Okunan ölçüler: {dims_txt}"
    )
    yield (composed, best["code"], dims_txt, status, best["step"], str(py_out), stl_out)


# ─── Gradio arayüzü ───────────────────────────────────────────────────────────

_css = """
#title { text-align:center; font-family:'Courier New',monospace; }
#subtitle { text-align:center; opacity:0.7; }
"""

with gr.Blocks(theme=gr.themes.Monochrome(), title="Pen2STEP — SKETCH → CAD", css=_css) as demo:

    gr.Markdown("# ⚙  Pen2STEP  ·  SKETCH → CAD", elem_id="title")
    gr.Markdown(
        "Çoklu görünüm + boyut-farkında, eğitimsiz framework  ·  "
        "el çizimi → CadQuery → STEP",
        elem_id="subtitle",
    )

    with gr.Row():
        with gr.Column(scale=1):
            files_in = gr.File(
                label="Görünümler  (parçanın 1+ açısını yükle: ön / üst / yan)",
                file_count="multiple",
                file_types=["image"],
                type="filepath",
            )
            webcam_in = gr.Image(
                sources=["webcam"], type="pil",
                label="…veya webcam ile çek (opsiyonel, listeye eklenir)",
                height=200,
            )
            with gr.Row():
                use_dims = gr.Checkbox(
                    value=True, label="Boyut yazılarını OCR ile oku")
                n_cand = gr.Slider(
                    1, 5, value=3, step=1,
                    label="Aday sayısı (kalite ↔ hız) — 3 en doğru, 1 en hızlı")
            btn = gr.Button("▶   KOD ÜRET", variant="primary", size="lg")
            composed_out = gr.Image(label="Modele giden birleşik görüntü", height=240)

        with gr.Column(scale=1):
            status_box = gr.Textbox(label="Durum", interactive=False, lines=3)
            model3d_out = gr.Model3D(
                label="Üretilen 3B model  (döndür: sürükle · yakınlaştır: tekerlek)",
                height=300, clear_color=[0.96, 0.97, 0.99, 1.0],
                camera_position=(80, 65, 320))  # otomatik kamera bazı parçaları kaçırıyor
            dims_box = gr.Textbox(label="Okunan ölçüler (OCR)", interactive=False, lines=1)
            code_box = gr.Code(language="python", label="Üretilen CadQuery Kodu", lines=12)
            with gr.Row():
                dl_step = gr.File(label="⬇  STEP İndir (.step)")
                dl_py = gr.File(label="⬇  Kod İndir (.py)")

    btn.click(
        fn=process,
        inputs=[files_in, webcam_in, n_cand, use_dims],
        outputs=[composed_out, code_box, dims_box, status_box, dl_step, dl_py, model3d_out],
    )

if __name__ == "__main__":
    # Yerel: çalıştırınca tarayıcıda otomatik açılır → http://localhost:7860
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False, inbrowser=True)
