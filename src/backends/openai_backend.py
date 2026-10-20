"""OpenAI backend (openai Python SDK, Chat Completions with an image data URL).

Candidate 0 is requested at temperature 0 and candidates 1..N-1 at T = 0.5, top-p 0.9 with a
per-call seed. GPT-5 class reasoning models reject sampling parameters; with --no-sampling-params
(or automatically after such a rejection) they run at provider defaults, and this is recorded.
"""
from __future__ import annotations

import base64

from . import Generation


class OpenAIBackend:
    def __init__(self, model: str, temperature: float = 0.5, top_p: float = 0.9, max_tokens: int = 16000,
                 reasoning_effort: str | None = "low", sampling_params: bool = True):
        from openai import OpenAI  # pip install openai
        self.client = OpenAI()     # credentials from OPENAI_API_KEY
        self.model, self.temperature, self.top_p = model, temperature, top_p
        self.max_tokens, self.reasoning_effort, self.sampling_params = max_tokens, reasoning_effort, sampling_params

    def _call(self, kw):
        import openai
        try:
            return self.client.chat.completions.create(**kw), kw
        except openai.BadRequestError as e:
            # reasoning models: sampling parameters / reasoning_effort unsupported -> retry without them
            msg = str(e).lower()
            dropped = {k: kw.pop(k) for k in ("temperature", "top_p", "seed", "reasoning_effort")
                       if k in kw and k in msg}
            if not dropped:
                raise
            return self.client.chat.completions.create(**kw), kw

    def generate(self, jpeg_bytes: bytes, instruction: str, idx: int, call_seed: int) -> Generation:
        url = "data:image/jpeg;base64," + base64.standard_b64encode(jpeg_bytes).decode("utf-8")
        kw = {"model": self.model, "max_completion_tokens": self.max_tokens,
              "messages": [{"role": "user", "content": [
                  {"type": "image_url", "image_url": {"url": url}},
                  {"type": "text", "text": instruction}]}]}
        if self.reasoning_effort:
            kw["reasoning_effort"] = self.reasoning_effort
        if self.sampling_params:
            kw.update(temperature=0.0 if idx == 0 else self.temperature, seed=call_seed)
            if idx > 0:
                kw["top_p"] = self.top_p
        r, sent = self._call(kw)
        settings = {k: sent[k] for k in ("max_completion_tokens", "temperature", "top_p", "seed", "reasoning_effort")
                    if k in sent}
        settings["candidate_index"] = idx
        settings.setdefault("temperature", "provider default")
        u = r.usage
        usage = {"input_tokens": u.prompt_tokens, "output_tokens": u.completion_tokens} if u else {}
        return Generation(text=r.choices[0].message.content or "", model=r.model, settings=settings,
                          usage=usage, stop_reason=r.choices[0].finish_reason, request_id=r.id)
