"""Claude backend (Anthropic Python SDK).

On Claude Opus 5.5 the API rejects temperature / top_p / top_k and thinking cannot be disabled, so
no sampling parameter is sent and every candidate runs at provider defaults; candidate diversity
comes from the provider's own sampling. The reasoning effort is fixed by --effort and recorded.

Server-side refusal fallback is OFF by default: a fallback would let a different model answer the
request, which would break per-backend attribution of the recorded generations. A refusal is
recorded as an empty text with stop_reason "refusal" and enters the replay as a failed candidate.
"""
from __future__ import annotations

import base64

from . import Generation


class AnthropicBackend:
    def __init__(self, model: str = "claude-opus-5-5", effort: str = "low", max_tokens: int = 16000):
        import anthropic  # pip install anthropic
        self.client = anthropic.Anthropic()   # credentials from ANTHROPIC_API_KEY or `ant auth login`
        self.model, self.effort, self.max_tokens = model, effort, max_tokens

    def generate(self, jpeg_bytes: bytes, instruction: str, idx: int, call_seed: int) -> Generation:
        settings = {"max_tokens": self.max_tokens, "effort": self.effort, "thinking": "adaptive (always on)",
                    "temperature": "provider default (not settable)", "top_p": "provider default (not settable)",
                    "seed": "not supported", "candidate_index": idx}
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            output_config={"effort": self.effort},
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                             "data": base64.standard_b64encode(jpeg_bytes).decode("utf-8")}},
                {"type": "text", "text": instruction},
            ]}],
        )
        text = "" if msg.stop_reason == "refusal" else "".join(
            b.text for b in msg.content if b.type == "text")
        usage = {"input_tokens": msg.usage.input_tokens, "output_tokens": msg.usage.output_tokens}
        return Generation(text=text, model=msg.model, settings=settings, usage=usage,
                          stop_reason=msg.stop_reason, request_id=getattr(msg, "_request_id", None))
