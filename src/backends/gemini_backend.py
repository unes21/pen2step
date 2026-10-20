"""Gemini backend (google-genai Python SDK).

Candidate 0 at temperature 0, candidates 1..N-1 at T = 0.5, top-p 0.9, each with a per-call seed.
"""
from __future__ import annotations

from . import Generation


class GeminiBackend:
    def __init__(self, model: str, temperature: float = 0.5, top_p: float = 0.9, max_tokens: int = 16000):
        from google import genai  # pip install google-genai
        self.genai = genai
        self.client = genai.Client()   # credentials from GEMINI_API_KEY / GOOGLE_API_KEY
        self.model, self.temperature, self.top_p, self.max_tokens = model, temperature, top_p, max_tokens

    def generate(self, jpeg_bytes: bytes, instruction: str, idx: int, call_seed: int) -> Generation:
        types = self.genai.types
        settings = {"temperature": 0.0 if idx == 0 else self.temperature, "seed": call_seed,
                    "max_output_tokens": self.max_tokens}
        if idx > 0:
            settings["top_p"] = self.top_p
        r = self.client.models.generate_content(
            model=self.model,
            contents=[types.Part.from_bytes(data=jpeg_bytes, mime_type="image/jpeg"), instruction],
            config=types.GenerateContentConfig(**settings),
        )
        settings["candidate_index"] = idx
        um = getattr(r, "usage_metadata", None)
        usage = {"input_tokens": getattr(um, "prompt_token_count", None),
                 "output_tokens": getattr(um, "candidates_token_count", None)} if um else {}
        cand = r.candidates[0] if getattr(r, "candidates", None) else None
        stop = str(cand.finish_reason) if cand is not None and cand.finish_reason is not None else None
        return Generation(text=r.text or "", model=getattr(r, "model_version", None) or self.model,
                          settings=settings, usage=usage, stop_reason=stop,
                          request_id=getattr(r, "response_id", None))
