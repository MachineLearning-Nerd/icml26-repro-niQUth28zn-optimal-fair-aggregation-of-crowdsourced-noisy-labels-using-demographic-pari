import json
import sys
from pathlib import Path


def main():
    results = json.loads(Path("outputs/cumulative_results.json").read_text())
    claims = {claim["claim"]: claim for claim in results["claims"]}
    failures = []

    claim_1 = claims["C1"]
    metrics_1 = claim_1["metrics"]
    if claim_1["status"] != "VERIFIED":
        failures.append("C1 status")
    if metrics_1["error_log_slope"] >= -0.7 * metrics_1["theoretical_exponent"]:
        failures.append("C1 error exponent")
    if metrics_1["gap_log_slope"] >= -0.15:
        failures.append("C1 DP-gap slope")

    claim_2 = claims["C2"]
    if claim_2["status"] != "VERIFIED":
        failures.append("C2 status")
    if claim_2["metrics"]["decision_disagreement_probability"] <= 1e-4:
        failures.append("C2 Bayes/MV distinctness")
    if claim_2["metrics"]["independent_checker_exit_code"] != 0:
        failures.append("C2 independent checker")

    claim_3 = claims["C3"]
    if claim_3["status"] != "VERIFIED":
        failures.append("C3 status")
    for row in claim_3["metrics"]["rows"]:
        if row["observed_dp"] > row["bound"] + 0.01:
            failures.append(f"C3 bound R={row['crowd_size']}")

    claim_4 = claims["C4"]
    if claim_4["status"] != "VERIFIED":
        failures.append("C4 status")
    for row in claim_4["metrics"]["rows"]:
        if row["condition_met"] != row["converged"]:
            failures.append(f"C4 condition {row['case']}")

    claim_5 = claims["C5"]
    if claim_5["status"] != "VERIFIED":
        failures.append("C5 status")
    for row in claim_5["metrics"]["rows"]:
        if row["dp_gap"] > row["epsilon"] + 1e-12:
            failures.append(f"C5 fairness eps={row['epsilon']}")
        if row["accuracy_gap"] > 0.015:
            failures.append(f"C5 loss eps={row['epsilon']}")

    report = {
        "checker": "independent cumulative-results checker",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "claims_checked": list(claims),
    }
    Path("outputs/cumulative_checker.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
