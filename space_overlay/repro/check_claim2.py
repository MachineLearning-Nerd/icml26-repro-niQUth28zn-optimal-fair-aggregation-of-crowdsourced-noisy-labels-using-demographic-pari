import csv
import json
import sys
from pathlib import Path


def close(left, right, tolerance=1e-12):
    return abs(left - right) <= tolerance


def main():
    json_path = Path("outputs/claim2_exact.json")
    csv_path = Path("outputs/claim2_exact.csv")
    evidence = json.loads(json_path.read_text())
    with csv_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    failures = []
    if len(rows) != 5:
        failures.append("expected five exact crowd-size rows")
    for row in rows:
        ground_dp = float(row["ground_dp"])
        mv_dp = float(row["mv_dp"])
        bayes_dp = float(row["bayes_dp"])
        if not close(float(row["mv_gap"]), abs(mv_dp - ground_dp)):
            failures.append(f"MV gap mismatch at R={row['crowd_size']}")
        if not close(float(row["bayes_gap"]), abs(bayes_dp - ground_dp)):
            failures.append(f"Bayes gap mismatch at R={row['crowd_size']}")
        if float(row["mv_condition_min"]) <= 1:
            failures.append(f"MV condition not met at R={row['crowd_size']}")
        if float(row["bayes_condition_partial_sum_min"]) <= 0:
            failures.append(f"Bayes partial sum is not positive at R={row['crowd_size']}")

    initial = rows[0]
    final = rows[-1]
    if float(final["mv_gap"]) >= float(initial["mv_gap"]):
        failures.append("MV exact gap did not shrink")
    if float(final["bayes_gap"]) >= float(initial["bayes_gap"]):
        failures.append("Bayes exact gap did not shrink")
    if float(final["mv_gap"]) >= 0.02:
        failures.append("MV exact final gap is not below 0.02")
    if float(final["bayes_gap"]) >= 0.005:
        failures.append("Bayes exact final gap is not below 0.005")
    if not any(
        float(row["decision_disagreement_probability"]) > 1e-4 for row in rows
    ):
        failures.append("Bayes was not independently exercised from MV")

    proof_steps = evidence["proof_audit"]["source_steps"]
    if not all(step["passed"] for step in proof_steps):
        failures.append("symbolic derivation certificate contains a failed step")

    report = {
        "checker": "independent CSV and proof-certificate checker",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "rows_checked": len(rows),
        "bayes_distinct_from_mv": any(
            float(row["decision_disagreement_probability"]) > 1e-4 for row in rows
        ),
        "final_mv_gap": float(final["mv_gap"]),
        "final_bayes_gap": float(final["bayes_gap"]),
        "proof_steps_checked": len(proof_steps),
    }
    Path("outputs/claim2_checker.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
