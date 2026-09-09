"""Pen2STEP — Q1 araştırma altyapısı.

Modüller:
    prompt          : Inference ve eğitimde ortak kullanılan prompt sabitleri.
    part_families   : Prosedürel parametrik parça üreticileri (ground-truth kod + boyut).
    render          : CadQuery katı modeli → el-çizimi stilinde teknik eskiz.
    generate_dataset: Pen2STEP-Bench veri setini üretir.
    metrics         : CAD-spesifik değerlendirme metrikleri (SVR, Chamfer, boyut hatası).
    run_baselines   : Model karşılaştırma harness'i.
"""
