"""VLM çıktısı CadQuery kodunun kural-tabanlı (AST) onarımı.

Frozen modelin tipik hataları (bu projede gözlemlendi) onarılır:
  * markdown ``` çiti / "ASSISTANT:" öneki
  * eksik `import cadquery as cq`
  * sonuç değişkeni `result` yerine `solid`/`shape`/... → result'a ata
  * sonuç bir atama değil çıplak ifade → `result = <ifade>`
  * üretim ortada kesilmiş (kapanmamış parantez) → ayrıştırılabilir hale getir

`repair()` (onarılmış_kod, uygulanan_onarımlar) döndürür; uygulanan onarım
listesi ablasyon/loglama için kullanılır.
"""

from __future__ import annotations

import ast

_RESULT_CANDIDATES = ["result", "solid", "shape", "part", "body",
                      "model", "compound", "obj", "cad_result"]


def split_after_assistant(text: str) -> str:
    if "ASSISTANT:" in text:
        text = text.split("ASSISTANT:", 1)[1]
    return text.strip()


def strip_markdown(text: str) -> str:
    t = text.strip()
    if t.startswith("```python"):
        t = t[len("```python"):]
    elif t.startswith("```"):
        t = t[3:]
    if t.endswith("```"):
        t = t[:-3]
    return t.strip()


def ensure_import(code: str):
    if "import cadquery" in code:
        return code, False
    return "import cadquery as cq\n" + code, True


def _balance_brackets(code: str):
    """Kapanmamış (), [], {} varsa sona kapatıcıları ekle (kesik üretim onarımı)."""
    pairs = {")": "(", "]": "[", "}": "{"}
    opens = {"(": 0, "[": 0, "{": 0}
    in_str = None
    for ch in code:
        if in_str:
            if ch == in_str:
                in_str = None
            continue
        if ch in ("'", '"'):
            in_str = ch
        elif ch in opens:
            opens[ch] += 1
        elif ch in pairs:
            opens[pairs[ch]] = max(0, opens[pairs[ch]] - 1)
    closers = ")" * opens["("] + "]" * opens["["] + "}" * opens["{"]
    if closers:
        return code.rstrip() + closers + "\n", True
    return code, False


def make_parseable(code: str):
    """Kodu ayrıştırılabilir yap: önce parantez dengele, olmazsa son satırları at."""
    try:
        ast.parse(code)
        return code, False
    except SyntaxError:
        pass
    balanced, changed = _balance_brackets(code)
    if changed:
        try:
            ast.parse(balanced)
            return balanced, True
        except SyntaxError:
            pass
    # Son satırları teker teker atarak ayrıştırılabilir parçayı bul
    lines = code.split("\n")
    while lines:
        lines.pop()
        candidate = "\n".join(lines)
        if not candidate.strip():
            break
        cand2, _ = _balance_brackets(candidate)
        try:
            ast.parse(cand2)
            return cand2, True
        except SyntaxError:
            continue
    return code, False


def ensure_result(code: str):
    """`result` tanımlı değilse: bilinen aday değişkeni ya da son ifadeyi ata."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code, False

    assigned = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    assigned.append(t.id)

    if "result" in assigned:
        return code, False

    # Bilinen aday isimlerden birini result'a ata
    for cand in _RESULT_CANDIDATES[1:]:
        if cand in assigned:
            return code.rstrip() + f"\nresult = {cand}\n", True

    # Son üst-seviye düğüm çıplak bir ifadeyse onu result yap
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr = tree.body[-1]
        try:
            seg = ast.get_source_segment(code, expr)
        except Exception:
            seg = None
        if seg:
            lines = code.split("\n")
            start = expr.lineno - 1
            end = getattr(expr, "end_lineno", expr.lineno)
            new_lines = lines[:start] + [f"result = {seg}"] + lines[end:]
            return "\n".join(new_lines), True

    # Son çare: en son atanan ismi result yap
    if assigned:
        return code.rstrip() + f"\nresult = {assigned[-1]}\n", True

    return code, False


def repair(raw: str):
    """Tam onarım hattı. Döner: (kod, uygulanan_onarimlar: list[str])."""
    applied = []
    code = split_after_assistant(raw)
    code = strip_markdown(code)

    code, ch = make_parseable(code)
    if ch:
        applied.append("parse_fix")

    code, ch = ensure_import(code)
    if ch:
        applied.append("add_import")

    code, ch = ensure_result(code)
    if ch:
        applied.append("ensure_result")

    return code.strip() + "\n", applied
