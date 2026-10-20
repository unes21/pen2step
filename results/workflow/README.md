# Workflow study (time and blind supplier rating of RFQs)

Each participant performs two tasks on two different parts, in alternating order across participants
(first participant A then B, second B then A).

- Task A (current practice): sketch, photograph, write a short free-text request for quotation (RFQ).
- Task B (Pen2STEP): sketch, photograph, run Pen2STEP (prepared command; the participant only supplies
  the file), attach the generated CadQuery program and STEP file to the RFQ.

Two raters on the supplier side (a spare-parts dealer and a machine-shop engineer) rate every RFQ
blind (task hidden, random order): (1) could you quote from this RFQ without calling back? yes/no;
(2) estimated hours until a quote; (3) what is missing? (one line).

| File | Columns |
|---|---|
| `rfq_ratings.csv` | `rfq_id, task, part_id, rater, q1_quote_without_callback, q2_hours_to_quote, q3_missing` |
| `task_times.csv` | `participant, task, part_id, order, sketch_minutes, total_minutes, pen2step_runtime_s` (participant is a code such as P01; no names) |

```bash
python src/stats.py --workflow       # writes results/workflow/workflow_stats.json and prints the table
```

The analysis is descriptive only: counts and proportions with Wilson 95% intervals, medians and
interquartile ranges, rater agreement on question 1. No statistical model and no hypothesis test (n is small).
