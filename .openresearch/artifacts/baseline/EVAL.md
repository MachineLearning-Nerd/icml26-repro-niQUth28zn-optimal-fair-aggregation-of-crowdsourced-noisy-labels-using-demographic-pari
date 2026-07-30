# Baseline evaluation contract

The fixed command is:

```bash
uv run --frozen python repro/run_all.py
```

It reruns all five judged checks and exits nonzero unless Claims 1, 3, 4, and 5
pass and Claim 2 remains explicitly blocked for the known homogeneous-skill
Bayes-equals-MV reason.
