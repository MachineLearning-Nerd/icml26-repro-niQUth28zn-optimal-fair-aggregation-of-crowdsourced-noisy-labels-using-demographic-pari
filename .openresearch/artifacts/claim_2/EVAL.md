# Claim 2 evaluator contract

Run the inherited project command:

```bash
uv run --frozen python repro/run_all.py
```

The command prints raw Claim 2 JSON, the independent checker output, both
negative-control outputs, cumulative results for Claims 1–5, runtime, CPU
allocation, seeds, and Git SHA. It exits nonzero if the exact Claim 2 contract,
either destructive control, or any previously accepted claim fails.
