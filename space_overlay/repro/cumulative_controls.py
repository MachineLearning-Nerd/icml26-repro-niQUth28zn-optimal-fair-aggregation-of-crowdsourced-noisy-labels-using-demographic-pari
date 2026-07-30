import json
import math
import sys
from pathlib import Path


def main():
    results = json.loads(Path("outputs/cumulative_results.json").read_text())
    claims = {claim["claim"]: claim for claim in results["claims"]}

    c1 = claims["C1"]["metrics"]
    doubled_exponent_violations = sum(
        error > math.exp(-2 * crowd_size * c1["theoretical_exponent"])
        for crowd_size, error in zip(c1["crowd_sizes"], c1["errors"])
    )

    c3_rows = claims["C3"]["metrics"]["rows"]
    zero_constant_violations = sum(row["observed_dp"] > 0 for row in c3_rows)

    c4_rows = claims["C4"]["metrics"]["rows"]
    random_case = next(row for row in c4_rows if row["case"] == "random")
    forced_random_convergence_fails = not random_case["converged"]

    unconstrained_dp_gap = claims["C5"]["metrics"]["unconstrained_dp_gap"]
    unconstrained_fails_eps_005 = unconstrained_dp_gap > 0.05

    controls = {
        "C1": {
            "mutation": "replace exp(-R K) by the too-small exp(-2 R K)",
            "violation_count": doubled_exponent_violations,
            "failed_as_expected": doubled_exponent_violations > 0,
        },
        "C2": claims["C2"]["metrics"]["negative_controls"],
        "C3": {
            "mutation": "replace the positive influence constant eta by zero",
            "violation_count": zero_constant_violations,
            "failed_as_expected": zero_constant_violations == len(c3_rows),
        },
        "C4": {
            "mutation": "declare the p=0.5 random crowd convergent",
            "observed_gap": random_case["gap"],
            "failed_as_expected": forced_random_convergence_fails,
        },
        "C5": {
            "mutation": "force beta=0 under epsilon=0.05",
            "unconstrained_dp_gap": unconstrained_dp_gap,
            "failed_as_expected": unconstrained_fails_eps_005,
        },
    }
    all_failed = all(
        control.get("failed_as_expected", True)
        if claim != "C2"
        else all(item["failed_as_expected"] for item in control.values())
        for claim, control in controls.items()
    )
    report = {
        "status": "FAIL_AS_EXPECTED" if all_failed else "UNEXPECTED_PASS",
        "controls": controls,
    }
    Path("outputs/cumulative_controls.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))
    return 1 if all_failed else 0


if __name__ == "__main__":
    sys.exit(main())
