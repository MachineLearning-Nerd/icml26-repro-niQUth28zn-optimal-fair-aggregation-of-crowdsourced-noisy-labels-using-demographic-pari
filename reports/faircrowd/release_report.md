Previous live judged score: `9/10`

Conservative projected score range after the proposed change: **9–10/10**

Best-supported possible new score: **10/10 (forecast only; not a judge result)**

# FairCrowd release report

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| C1 | 2 | 2 | HIGH | VERIFIED | Previously judged full-credit Monte Carlo regression reruns; tail remains sampling-noise limited. |
| C2 | 1 | 2 | HIGH | VERIFIED | Exact heterogeneous enumeration, positive Bayes/MV disagreement, both condition audits, reconstructed limit derivation, independent checker, and two controls. Remaining risk: no proof-assistant certificate. |
| C3 | 2 | 2 | HIGH | VERIFIED | All four Proposition 3.6 inequalities rerun and the zero-`η` mutation fails. |
| C4 | 2 | 2 | HIGH | VERIFIED | Four cases preserve the judged condition/convergence classification. Source audit limits the statement to the sufficient-condition interpretation. |
| C5 | 2 | 2 | HIGH | VERIFIED | Four fairness constraints and grid-loss comparisons rerun; unconstrained control fails. The comparator is a grid, not an exact LP. |

Current total score: **9/10**.

Conservative projected total score range: **9–10/10**.

Best-supported possible total: **10/10, forecast only**.

Claim 2 is the only claim changed since the previous judge result. No claim is
BLOCKED. The live judge may still retain 1/2 for Claim 2 if it does not accept
the reconstructed dominated-convergence derivation as sufficient support for
the asymptotic quantifier.

The exact publication action, once all remaining artifact gates pass, is a
text-only API upload to the existing Space `DineshAI/niQUth28zn`, followed by a
download and hash/traversal verification. No second Space will be created.

## Experiment tree

| Node | Branch | Result | Runtime / compute |
| --- | --- | --- | --- |
| Judged Monte Carlo baseline | `orx/judged-monte-carlo-baseline` | C1/C3/C4/C5 pass; C2 BLOCKED | local CPU, 27.438 s script |
| Exact heterogeneous Bayes verifier | `orx/exact-heterogeneous-bayes-verifier` | all five pass | local CPU, 39.794 s script |
| Evaluator-visible candidate | `orx/evaluator-visible-release-candidate` | all five plus cumulative checker/controls pass | local CPU, 41.007 s script |
| Release manifest and blind audit | `orx/release-manifest-and-blind-audit` | pending final unchanged-command regression | estimated one core, under 60 s |

Scientific winning SHA:
`10451115e7ef0ba33a07b7b1ea20a5aaca959e8f`.

## Evidence locations

- Internal contracts and raw evidence:
  `.openresearch/artifacts/claim_1` through `claim_5`
- Cumulative results and execution record:
  `.openresearch/artifacts/cumulative`
- Evaluator-facing additive overlay: `space_overlay`
- Illustrated report: `reports/faircrowd/report.md`
- Self-contained notebook: `notebooks/faircrowd_claim2.py`

## Protected Space and upload set

The judged snapshot contains 17 files. The materialized candidate contains 33
files; the complete judged path set is a subset of the candidate path set.
Every judged file outside the explicit overlay is byte-identical. Both blind
traversals passed.

Exact text-only upload allowlist:

```text
README.md
artifacts/claim2_checker.json
artifacts/claim2_exact.csv
artifacts/claim2_exact.json
artifacts/cumulative_checker.json
artifacts/cumulative_controls.json
artifacts/cumulative_results.json
logbook.json
pages/current-verification/page.md
pages/index.md
pyproject.toml
repro/check_claim2.py
repro/check_cumulative.py
repro/claim2_exact.py
repro/claim2_negative_control.py
repro/core.py
repro/cumulative_controls.py
repro/run_all.py
uv.lock
```

Per-file SHA-256 values are in `release/space-upload-sha256.txt`; blind audit
records are in `release/blind-audit-round1.json` and
`release/blind-audit-round2.json`.

## Compute and cost

All formal runs used the local backend because each was estimated to require
one CPU core and finish within five minutes. No GPU was used. Recorded script
runtimes are 27.438 s, 39.794 s, and 41.007 s before the final release
regression. Hugging Face compute cost is **$0.00**; no HF Job was required.

## Material command ledger

```text
orx projects --json
orx runs c0377804-f38a-45e7-a7f7-abd140d292a8
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx paper 2601.23221 --full
orx create-experiment ... --title "Judged Monte Carlo baseline" --run-command "uv run --frozen python repro/run_all.py"
orx exp run a6cf21ff-7b10-47e3-b2e4-81a4539e45ef --backend local
orx exp wait a6cf21ff-7b10-47e3-b2e4-81a4539e45ef --timeout 120
orx logs 7645fff7-b7b8-41ca-8b65-6ac0e9eedcf0
orx create-experiment ... --title "Exact heterogeneous Bayes verifier" --parent a6cf21ff-7b10-47e3-b2e4-81a4539e45ef
orx exp run 5ad38086-9e8d-44f3-8a73-a3592eb7c4f7 --backend local
orx exp wait 5ad38086-9e8d-44f3-8a73-a3592eb7c4f7 --timeout 120
orx logs ef64e820-54c9-46cd-9e9a-d74e5d6fb227
orx create-experiment ... --title "Evaluator-visible release candidate" --parent 5ad38086-9e8d-44f3-8a73-a3592eb7c4f7
orx exp run e815d9aa-3caf-4fff-91f2-d8b5b53f2c0f --backend local
orx exp wait e815d9aa-3caf-4fff-91f2-d8b5b53f2c0f --timeout 120
orx logs 6ce67aaa-3b66-4405-9b80-9f041841b194 --bytes 200000
uv run --frozen python repro/make_report_figures.py
uvx --from marimo marimo check notebooks/faircrowd_claim2.py
uv run --frozen marimo export html notebooks/faircrowd_claim2.py -o /tmp/faircrowd_claim2.html
```

The final release regression, audit, upload, and post-publication commands are
appended to the published report only through immutable manifests and the
final campaign handoff; forecast language is not converted into a judge score.
