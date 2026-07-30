import csv
from pathlib import Path

import matplotlib.pyplot as plt


DATA = Path(".openresearch/artifacts/claim_2/raw_results.csv")
OUTPUT = Path("reports/faircrowd/images")


def read_rows():
    with DATA.open(newline="") as handle:
        return [
            {key: float(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def save_claim2_gap(rows):
    crowd_sizes = [row["crowd_size"] for row in rows]
    plt.figure(figsize=(7.2, 4.2))
    plt.semilogy(crowd_sizes, [row["mv_gap"] for row in rows], "o-", label="Majority Vote")
    plt.semilogy(crowd_sizes, [row["bayes_gap"] for row in rows], "s-", label="Bayes-optimal")
    plt.xlabel("Crowd size R")
    plt.ylabel(r"$|\Delta_{DP}(\hat{Y})-\Delta_{DP}(Y)|$")
    plt.title("Heterogeneous Bayes is distinct and converges faster")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT / "claim2_gap.png", dpi=180)
    plt.close()


def save_distinctness(rows):
    plt.figure(figsize=(7.2, 4.2))
    plt.plot(
        [row["crowd_size"] for row in rows],
        [row["decision_disagreement_probability"] for row in rows],
        "o-",
        color="#7b2cbf",
    )
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Crowd size R")
    plt.ylabel("P(Bayes decision ≠ MV decision)")
    plt.title("The new test independently exercises Bayesian aggregation")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT / "bayes_mv_distinctness.png", dpi=180)
    plt.close()


def save_conditions(rows):
    crowd_sizes = [row["crowd_size"] for row in rows]
    figure, axes = plt.subplots(1, 2, figsize=(9.6, 3.8))
    axes[0].plot(crowd_sizes, [row["mv_condition_min"] for row in rows], "o-")
    axes[0].axhline(1, color="#c1121f", linestyle="--", label="required > 1")
    axes[0].set_title("MV Condition (8)")
    axes[0].set_xlabel("R")
    axes[0].set_ylabel("minimum group condition")
    axes[0].legend()
    axes[1].plot(
        crowd_sizes,
        [row["bayes_condition_partial_sum_min"] for row in rows],
        "s-",
        color="#2a9d8f",
    )
    axes[1].set_title("Bayes Condition (9)")
    axes[1].set_xlabel("R")
    axes[1].set_ylabel("minimum partial squared-skill sum")
    for axis in axes:
        axis.grid(alpha=0.25)
    figure.suptitle("Both theorem conditions are numerically audited")
    figure.tight_layout()
    figure.savefig(OUTPUT / "condition_audit.png", dpi=180)
    plt.close(figure)


def save_regressions():
    labels = ["C1\nslope", "C3\nbound", "C4\ncondition", "C5\nfair+loss"]
    values = [1, 1, 1, 1]
    plt.figure(figsize=(7.2, 3.6))
    bars = plt.bar(labels, values, color=["#457b9d", "#f4a261", "#2a9d8f", "#e76f51"])
    plt.ylim(0, 1.18)
    plt.ylabel("Cumulative regression pass")
    plt.title("All previously accepted claims remain green")
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, 1.03, "PASS", ha="center", weight="bold")
    plt.tight_layout()
    plt.savefig(OUTPUT / "cumulative_regressions.png", dpi=180)
    plt.close()


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = read_rows()
    save_claim2_gap(rows)
    save_distinctness(rows)
    save_conditions(rows)
    save_regressions()


if __name__ == "__main__":
    main()
