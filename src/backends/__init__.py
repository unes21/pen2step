"""Frontier VLM backends for recording generations once (work package IP1).

Every backend receives the same instruction text as the open backbone (Appendix A of the paper,
taken from src/prompt.py without the LLaVA chat template) and one JPEG sheet, and returns the
decoded text together with the decoding settings that were actually applied. Nothing in the shell
or the replay depends on the backend: the recorded text is replayed offline by src/replay.py.

Decoding is not identical across providers, and each backend records what it really used:
  * open backbone (src/generation_dump.py): candidate 0 greedy, candidates 1..N-1 T = 0.5, top-p 0.9;
  * OpenAI and Gemini: candidate 0 at temperature 0, candidates 1..N-1 at T = 0.5, top-p 0.9 when
    the model accepts sampling parameters; reasoning models that reject them run at provider defaults;
  * Anthropic (Claude Opus 5.5 and later): sampling parameters are rejected by the API and thinking
    is always on, so every candidate runs at provider defaults; no greedy candidate exists.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Generation:
    text: str                      # decoded answer text only (no reasoning)
    model: str                     # model identifier returned by the provider
    settings: dict = field(default_factory=dict)   # decoding settings actually sent
    usage: dict = field(default_factory=dict)      # token counts reported by the provider
    stop_reason: str | None = None
    request_id: str | None = None


def instruction_text(prompt: str) -> str:
    """Strip the LLaVA chat template from a src.prompt.build_prompt() string."""
    marker = "USER: <image>\n"
    body = prompt.split(marker, 1)[1] if marker in prompt else prompt
    return body.rsplit(" ASSISTANT:", 1)[0]


def get_backend(name: str, model: str | None = None, **kw):
    if name == "anthropic":
        from .anthropic_backend import AnthropicBackend
        return AnthropicBackend(model=model or "claude-opus-5-5", **kw)
    if name == "openai":
        from .openai_backend import OpenAIBackend
        if not model:
            raise SystemExit("--model is required for the openai backend (e.g. a GPT-5 class model id)")
        return OpenAIBackend(model=model, **kw)
    if name == "gemini":
        from .gemini_backend import GeminiBackend
        if not model:
            raise SystemExit("--model is required for the gemini backend")
        return GeminiBackend(model=model, **kw)
    raise SystemExit(f"unknown backend {name!r} (anthropic | openai | gemini)")
