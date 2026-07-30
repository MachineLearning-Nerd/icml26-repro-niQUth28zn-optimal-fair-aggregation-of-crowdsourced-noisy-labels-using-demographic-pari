# Reproduction: Optimal Fair Aggregation of Crowdsourced Noisy Labels

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-niQUth28zn-optimal-fair-aggregation-of-crowdsourced-noisy-labels-using-demographic-pari/blob/main/notebooks/faircrowd_claim2.py)

This reproduction targets Theorem 3.4’s claim that both Majority Vote and
Bayes-optimal aggregation converge to the ground-truth demographic-parity gap
under their respective skill conditions. The previous judged test used
homogeneous `p=0.75`, making Bayes effectively the same rule as MV. The new test
enumerates every vote pattern through `R=16` under heterogeneous,
group-dependent one-coin skills and a nonzero target `ΔDP(Y)=0.2`.

Observed at `R=16`: MV gap `0.0113028`, Bayes gap `0.0002601`; the rules still
disagree on probability mass `0.0189842`. The independent checker passes, the
homogeneous and no-signal controls fail as intended, and the four previously
accepted claims remain green. This is a CPU-only exact finite calculation plus
an audited symbolic derivation; it does not turn finite numerics into proof of a
limit.

- [Illustrated technical report](reports/faircrowd/report.md)
- [Release forecast, provenance, and gates](reports/faircrowd/release_report.md)
- [Self-contained marimo tutorial](notebooks/faircrowd_claim2.py)
- [Claim contract and raw evidence](.openresearch/artifacts/claim_2/)
- [Paper](https://arxiv.org/abs/2601.23221)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public landing page, report, and notebook | Not run as an experiment (publication surface) | Presentation only | — |
| [Judged Monte Carlo baseline](https://github.com/MachineLearning-Nerd/icml26-repro-niQUth28zn-optimal-fair-aggregation-of-crowdsourced-noisy-labels-using-demographic-pari/tree/orx/judged-monte-carlo-baseline) | Freeze the judged evidence and criticism | `uv run --frozen python repro/run_all.py` | C1/C3/C4/C5 pass; C2 blocked | Local CPU, 30 s |
| [Exact heterogeneous Bayes verifier](https://github.com/MachineLearning-Nerd/icml26-repro-niQUth28zn-optimal-fair-aggregation-of-crowdsourced-noisy-labels-using-demographic-pari/tree/orx/exact-heterogeneous-bayes-verifier) | Exercise Bayes independently, audit the limit derivation, add controls | `uv run --frozen python repro/run_all.py` | All five cumulative checks pass | Local CPU, 45 s |
| [Evaluator-visible candidate](https://github.com/MachineLearning-Nerd/icml26-repro-niQUth28zn-optimal-fair-aggregation-of-crowdsourced-noisy-labels-using-demographic-pari/tree/orx/evaluator-visible-release-candidate) | Add independent cumulative checking, per-claim controls, report, and notebook | `uv run --frozen python repro/run_all.py` | All five checks pass; cumulative checker passes; controls fail as intended | Local CPU, 47 s |
| [Release manifest and blind audit](https://github.com/MachineLearning-Nerd/icml26-repro-niQUth28zn-optimal-fair-aggregation-of-crowdsourced-noisy-labels-using-demographic-pari/tree/orx/release-manifest-and-blind-audit) | Additive Space overlay, manifests, and evaluator-blind traversal | `uv run --frozen python repro/run_all.py` | All five checks pass; blind traversal passes twice | Local CPU, 36 s orchestration |

## Reproduce

```bash
uv sync --frozen
uv run --frozen python repro/run_all.py
marimo edit notebooks/faircrowd_claim2.py
```

## Upstream workspace

ICML 2026 agent reproduction workspace for `niQUth28zn`.
