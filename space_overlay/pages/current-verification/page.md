# Current verification — exact heterogeneous Bayes plus cumulative regressions

**Current verifier:** repository commit
`10451115e7ef0ba33a07b7b1ea20a5aaca959e8f`, run with:

```bash
uv run --frozen python repro/run_all.py
```

This page and the linked code supersede the equal-skill verification at judged
Space revision `eee6b5ec719b769b952bd978850bffba2ba590c3`. The old file is
preserved unchanged as **Historical rejected baseline**.

## Source and claim contracts

Paper source: [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2601.23221),
retrieved with an explicit browser User-Agent on `2026-07-30T07:22:08Z`.
SHA-256:
`f6a147f01856d20e54047311773d98e90123be014ee8372b2fdac3c9f9c44835`.

| Claim | Exact source anchor and quantifier | Contract used here |
| --- | --- | --- |
| C1 | Proposition 3.2, `#S3.Thmtheorem2`, every `R∈N*` and `φ∈{φ*,φMV}`: `|ΔDP(ŶRφ)−ΔDP(Y)| ≤ Σa E[e^(−R Kφ(a,X))|A=a]`. | The judged Monte Carlo regression must have error slope compatible with `K_MV` and a materially shrinking DP gap. |
| C2 | Theorem 3.4, `#S3.Thmtheorem4`: under Condition 8 for MV and Condition 9 for Bayes, `lim R→∞ ΔDP(ŶRφ)=ΔDP(Y)` for each named rule. | Audit both conditions and the limit derivation; exactly enumerate heterogeneous finite cases in which Bayes and MV make different decisions. |
| C3 | Proposition 3.6, `#S3.Thmtheorem6`, every `R≥1`: `ΔDP(MV) ≤ ε(R) Σr ΔDP(Ỹr)`, with `η≈0.4688`. | Recompute both sides for `R=6,10,20,40`; every observed value must lie below its bound. |
| C4 | Section 3 interpretation after Condition 8: with adversarial lower bound `C=0`, the sufficient guarantee requires `g1,R/R > 1/(1+2ε)`. | Cases meeting the implemented condition must converge under the tested horizon; random/adversarial controls must not. This is a finite audit of the paper's sufficient-condition interpretation, not a proof of logical necessity. |
| C5 | Theorem 4.1, `#S4.Thmtheorem1`: the dual minimizer defines the optimal binary `ε`-fair classifier. | At four `ε` values, output DP must be at most `ε` and accuracy must be within `0.015` of the exhaustive `121×121` threshold-grid optimum. |

## Assumptions and numerical audit for Claim 2

The model is binary, one-coin, and conditionally independent across
annotators. `P(Y=1|A=0)=0.4`, `P(Y=1|A=1)=0.6`, so the target DP gap is
`0.2`. Each group uses the periodically extended heterogeneous 16-skill block
stored in the raw JSON; all skills are at least `0.55`.

| R | patterns exhausted | MV gap to target | Bayes gap to target | `P(Bayes decision ≠ MV decision)` | min Condition 9 partial sum |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 8 | 0.078964800 | 0.038000000 | 0.167040000 | 0.1725 |
| 5 | 32 | 0.049371967 | 0.004658202 | 0.084551071 | 0.3175 |
| 8 | 256 | 0.030145156 | 0.006995763 | 0.076070079 | 0.4764 |
| 12 | 4,096 | 0.021489704 | 0.000708629 | 0.033603422 | 0.7924 |
| 16 | 65,536 | **0.011302823** | **0.000260052** | **0.018984190** | **1.0669** |

For each group, the MV Condition 8 value is `1.1 > 1`. Periodic extension
makes the positive squared-skill deviations in Condition 9 sum to infinity.
Bayes uses Equation 4 with group prior odds, annotator-specific
log-likelihood weights, and the paper's `posterior ≥ 1/2` tie rule:

```python
posterior_log_odds = prior_log_odds + (
    (2 * patterns - 1) * skill_log_odds
).sum(axis=1)
bayes_prediction = posterior_log_odds >= 0
```

The verifier exhausts the Boolean indicator inequality, then checks the
derivation graph: conditional expectation, DP triangle inequality, Theorem 3.1
substitution, Lemma 3.3 Conditions 8/9, and dominated convergence with
envelope `1`. The finite enumeration is corroboration; the limit conclusion
comes from this reconstructed derivation.

## Cumulative raw evidence

| Claim | Key observed evidence | Current status |
| --- | --- | --- |
| C1 | `K_MV=0.263477`; error log-slope `−0.290894`; DP-gap log-slope `−0.179105`; gaps `0.05107→0.00453`. | VERIFIED |
| C2 | At `R=16`, MV gap `0.0113028`, Bayes gap `0.0002601`, decision-disagreement mass `0.0189842`. | VERIFIED |
| C3 | Observed/bound: `0.1827/0.2581`, `0.2228/0.3368`, `0.2455/0.3728`, `0.2918/0.5769`. | VERIFIED |
| C4 | Condition/gap: `p=.75: 1.5/.00395`; `p=.65: 1.3/.00216`; `p=.50: 0/.29907`; `p=.40: 0/.53902`. | VERIFIED |
| C5 | For `ε=.02,.05,.10,.20`, DP gaps `.01975,.04985,.09999,.19338`; grid accuracy gaps `.002875,.00210,.00250,.00455`. | VERIFIED |

Download:
[cumulative JSON](https://huggingface.co/spaces/DineshAI/niQUth28zn/resolve/main/artifacts/cumulative_results.json),
[Claim 2 JSON](https://huggingface.co/spaces/DineshAI/niQUth28zn/resolve/main/artifacts/claim2_exact.json),
[Claim 2 CSV](https://huggingface.co/spaces/DineshAI/niQUth28zn/resolve/main/artifacts/claim2_exact.csv).

Executable source:
[fixed entrypoint](https://huggingface.co/spaces/DineshAI/niQUth28zn/blob/main/repro/run_all.py),
[exact enumerator](https://huggingface.co/spaces/DineshAI/niQUth28zn/blob/main/repro/claim2_exact.py),
[Claim 2 checker](https://huggingface.co/spaces/DineshAI/niQUth28zn/blob/main/repro/check_claim2.py),
[cumulative checker](https://huggingface.co/spaces/DineshAI/niQUth28zn/blob/main/repro/check_cumulative.py),
[controls](https://huggingface.co/spaces/DineshAI/niQUth28zn/blob/main/repro/cumulative_controls.py),
[locked environment](https://huggingface.co/spaces/DineshAI/niQUth28zn/blob/main/uv.lock).

## Independent checkers and negative controls

The independent Claim 2 checker read the CSV and proof certificate:

```json
{"status":"PASS","failures":[],"rows_checked":5,
 "bayes_distinct_from_mv":true,"proof_steps_checked":6}
```

The cumulative independent checker returned `PASS` for
`["C1","C2","C3","C4","C5"]`.

Every deliberately broken control exited nonzero:

| Claim | Mutation | Expected failure observed |
| --- | --- | --- |
| C1 | Replace `exp(−R K)` with too-small `exp(−2R K)`. | 4 violations |
| C2 | Equal `p=.75`, prior `.5`, while demanding Bayes/MV distinctness. | Bayes identical to MV |
| C2 | All `p=.5` while demanding recovery of nonzero target DP. | Condition 9 sum `0`; gap `0.2` |
| C3 | Replace positive `η` by `0`. | 4 violations |
| C4 | Declare the `p=.5` random crowd convergent. | observed gap `0.299067` |
| C5 | Force unconstrained `β=0` at `ε=.05`. | DP gap `0.193383` |

Download:
[checker output](https://huggingface.co/spaces/DineshAI/niQUth28zn/resolve/main/artifacts/cumulative_checker.json),
[control output](https://huggingface.co/spaces/DineshAI/niQUth28zn/resolve/main/artifacts/cumulative_controls.json).
The entrypoint exits nonzero if a claim, independent checker, or intended
control behavior fails.

## Reproduction metadata and limitations

- Environment: `uv.lock`, Python `3.12.11`; fixed command shown at top.
- Scientific run SHA: `10451115e7ef0ba33a07b7b1ea20a5aaca959e8f`.
- Deterministic Monte Carlo seeds: `1,2,3,5`; Claim 2 uses exhaustive
  enumeration and no random seed.
- Compute estimate: 1 CPU core, 45–60 seconds. Selected local CPU under the
  campaign rule.
- Actual report: 8 logical CPUs visible, affinity unavailable; implementation
  is single-threaded; script runtime `41.007319` seconds.
- Claims 1, 3, 4, and 5 remain the judged Monte Carlo regressions. Claim 2 is
  exact only through `R=16`; it is not presented as finite proof of a limit.
- Dominated convergence and Lemma 3.3 are audited mathematical rules, not a
  Lean/Coq certificate.
- Claim 5 compares against a dense threshold grid, not an exact LP solver.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | This page | Yes | Yes | Yes | PASS | fails as intended | Proposition 3.2 / Eq. 7 | VERIFIED |
| C2 | This page | Yes | Yes | Yes | PASS | both fail as intended | Theorem 3.4 / Conditions 8–9 | VERIFIED |
| C3 | This page | Yes | Yes | Yes | PASS | fails as intended | Proposition 3.6 / Eq. 10 | VERIFIED |
| C4 | This page | Yes | Yes | Yes | PASS | fails as intended | Condition 8 interpretation | VERIFIED |
| C5 | This page | Yes | Yes | Yes | PASS | fails as intended | Theorem 4.1 | VERIFIED |
