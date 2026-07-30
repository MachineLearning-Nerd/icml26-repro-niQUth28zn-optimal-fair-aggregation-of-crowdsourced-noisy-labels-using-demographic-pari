# Claim 2 method

The finite model uses `P(Y=1|A=0)=0.4` and `P(Y=1|A=1)=0.6`, hence the target
DP gap is nonzero (`0.2`). Each group has a different heterogeneous 16-skill
block, periodically extended to define an infinite annotator sequence. Every
skill is at least `0.55`, so Equation (8) holds with margin `0.05`; periodic
non-random skills make the Equation (9) squared-deviation sum diverge.

For `R = 3, 5, 8, 12, 16`, all `2^R` vote patterns are enumerated. Their
probabilities under each truth value and group are computed exactly to floating
precision. Bayes uses the group prior and per-annotator log-likelihood weights;
MV uses the paper's tie rule.

The symbolic audit starts from the complete four-row Boolean truth table,
conditions it on each group, applies the DP triangle inequality, substitutes
Theorem 3.1's conditional error bound, and applies dominated convergence using
the `[0,1]` envelope and Lemma 3.3's almost-sure limit.
