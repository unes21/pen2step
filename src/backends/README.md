# Frontier VLM arm (work package IP1)

Records the raw generations of frontier vision-language models once and replays every shell
configuration offline, exactly as for the open backbone. No condition is ever re-generated; after
the recording, no further API call is made.

```bash
pip install -r requirements-frontier.txt
export ANTHROPIC_API_KEY=...   # or `ant auth login`; OPENAI_API_KEY; GEMINI_API_KEY
python -m src.generation_dump_api --backend anthropic --dry-run --out results/replay/generations_anthropic.jsonl
python -m src.generation_dump_api --backend anthropic --out results/replay/generations_anthropic.jsonl
python -m src.generation_dump_api --backend openai --model <gpt-5-class id> --out results/replay/generations_openai.jsonl
python -m src.replay --dump results/replay/generations_anthropic.jsonl --out results/replay_anthropic
python src/stats.py --backend anthropic
python tools/make_paper_tables.py --backends open,anthropic,openai --out results/PAPER_TABLES_frontier.md
```

The real split needs 238 calls per backend (`--dry-run` prints the count for any split). Runs are
resumable; recorded calls are never repeated. Keys are read from the environment only and are never
written to any file; `results/replay/provenance.json` records the backend, the model id returned by
the provider, the decoding settings actually applied, run dates and the SDK version.

## Prompt and decoding

The instruction text is identical to the open backbone (Appendix A, `src/prompt.py`, without the
LLaVA chat template), and the same sheet JPEG is sent. Decoding cannot be identical across providers,
and the paper must say so:

| Backend | Candidate 0 | Candidates 1..N-1 | Seed |
|---|---|---|---|
| open backbone | greedy | T = 0.5, top-p 0.9 | per call |
| OpenAI / Gemini | temperature 0 | T = 0.5, top-p 0.9 | per call |
| OpenAI reasoning models that reject sampling parameters | provider default | provider default | none |
| Anthropic (Claude Opus 5.5) | provider default | provider default | not supported |

On Claude Opus 5.5 the API rejects temperature and top-p and thinking is always on; reasoning depth
is fixed by `--effort` (default `low`) and recorded. Candidate 0 is recorded once and shared across
seeds for every backend, as for the open backbone, so the replay code is unchanged.

The token limit is 16,000 (`--max-tokens`) instead of the open backbone's 512: thinking and
reasoning tokens count against the limit on frontier models, and 512 would truncate them before any
code is written. This difference is recorded and must be reported.

Refusal fallback to another model is deliberately not enabled for the Anthropic backend: it would
let a different model answer a request and break per-backend attribution. A refusal is recorded with
`stop_reason: "refusal"` and an empty text, and enters the replay as a failed candidate.
