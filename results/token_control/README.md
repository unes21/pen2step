# Token-budget control (2048 new tokens)

Greedy candidate of the 19 development and 8 case-study sheets regenerated with the token budget raised
from 512 to 2048; everything else as in the main recordings (pinned checkpoint, prompt without dimension
clause, repetition penalty 1.1). Recorded once on one A100 in bfloat16 (`environment.json`).

```bash
python -m src.token_budget_control --out results/token_control/dump_2048.jsonl   # GPU, once
python -m src.replay --dump results/token_control/dev/dump.jsonl --data benchmark/real --out results/token_control/dev
python -m src.replay --dump results/token_control/case/dump.jsonl --data benchmark/case_study --out results/token_control/case
python -m src.stats --rows results/token_control/dev/replay_rows.json --out results/token_control/dev/stats.json
python -m src.stats --rows results/token_control/case/replay_rows.json --trivial results/replay_case/trivial.json --out results/token_control/case/stats.json
```

`dev/dump.jsonl` and `case/dump.jsonl` are the two splits of `dump_2048.jsonl`. Result: all 27 generations
reach the 2048-token limit without an end-of-sequence token, and the bare model yields no valid STEP solid
(0 of 19 and 0 of 8); `summary.json` collects the counts. The first 512 tokens of every generation are
identical to the corresponding 512-token recording.
