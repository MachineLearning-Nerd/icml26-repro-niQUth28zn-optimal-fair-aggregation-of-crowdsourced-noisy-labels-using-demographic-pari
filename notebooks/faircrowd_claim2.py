import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    return mo, np, plt


@app.cell
def _(mo):
    mo.md(
        r"""
        # Fair aggregation: when Bayes is genuinely different from Majority Vote

        **Observed evidence first.** Under heterogeneous group-dependent skills,
        the exact `R=16` gaps to the nonzero ground-truth DP gap `0.2` are
        **0.0113028 for MV** and **0.0002601 for Bayes**. The rules disagree on
        probability mass **0.0189842**, so this test independently exercises both
        aggregators.
        """
    )
    return


@app.cell
def _(np):
    crowd_size = np.array([3, 5, 8, 12, 16])
    mv_gap = np.array([0.0789648, 0.04937196656, 0.030145155599, 0.021489703522, 0.011302823311])
    bayes_gap = np.array([0.038, 0.00465820224, 0.006995762689, 0.000708629068, 0.000260052406])
    disagreement = np.array([0.16704, 0.084551070656, 0.076070078741, 0.033603422005, 0.018984189600])
    return bayes_gap, crowd_size, disagreement, mv_gap


@app.cell
def _(bayes_gap, crowd_size, mv_gap, plt):
    _figure, _axis = plt.subplots(figsize=(7, 4))
    _axis.semilogy(crowd_size, mv_gap, "o-", label="Majority Vote")
    _axis.semilogy(crowd_size, bayes_gap, "s-", label="Bayes-optimal")
    _axis.set(xlabel="Crowd size R", ylabel="Gap to ground-truth DP")
    _axis.grid(alpha=0.25)
    _axis.legend()
    _figure
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The implementation

        For every group and truth value, the verifier enumerates all `2^R` vote
        patterns. Majority Vote thresholds the count. Bayes uses

        \[
        \log\frac{P(Y=1\mid \tilde Y,A)}{P(Y=0\mid \tilde Y,A)}
        =
        \log\frac{q_A}{1-q_A}
        + \sum_r (2\tilde Y_r-1)\log\frac{p_r(A)}{1-p_r(A)}.
        \]

        Heterogeneous `p_r(A)` values make this a weighted decision rule rather
        than a disguised majority count.
        """
    )
    return


@app.cell
def _(crowd_size, disagreement, plt):
    _figure, _axis = plt.subplots(figsize=(7, 3.6))
    _axis.plot(crowd_size, disagreement, "o-", color="#7b2cbf")
    _axis.set(xlabel="Crowd size R", ylabel="P(Bayes ≠ MV)")
    _axis.grid(alpha=0.25)
    _figure
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## What the theorem needs beyond these points

        Finite numerics do not prove an asymptotic theorem. The reproduction
        separately audits the derivation from the pointwise error indicator to a
        two-group DP bound, substitutes Theorem 3.1, checks Conditions (8)/(9),
        and applies dominated convergence with envelope `1`.

        Controls: homogeneous equal skills intentionally collapse Bayes to MV;
        `p=0.5` intentionally violates the Bayes condition and leaves a constant
        `0.2` gap. Both controls exit nonzero.
        """
    )
    return


if __name__ == "__main__":
    app.run()
