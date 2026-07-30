# Limitations and deviations

- Exact Bayes enumeration stops at `R=16`; it is scoped corroboration, not the
  reason for the asymptotic verdict.
- The reconstructed derivation invokes dominated convergence and the paper's
  Lemma 3.3 as named mathematical rules. It is machine-audited but not a Lean or
  Coq proof.
- `X` is empty in the finite experiment, matching the paper's synthetic regime.
- Skills are deterministic periodic sequences rather than random finite draws,
  making the infinite conditions auditable without selecting sample size from
  the convergence formula.
- No official implementation was available; the code is clean-room from the
  displayed equations.
