import argparse
import json
import sys

import numpy as np

from claim2_exact import bayes_prediction, majority_prediction, vote_patterns


def homogeneous_control():
    patterns = vote_patterns(9)
    skills = np.full(9, 0.75)
    mv = majority_prediction(patterns)
    bayes = bayes_prediction(patterns, skills, prior=0.5)
    identical = bool(np.array_equal(mv, bayes))
    report = {
        "control": "homogeneous equal-skill distinctness",
        "expected_failure": "Bayes collapses to MV and cannot independently verify both methods",
        "bayes_identical_to_mv": identical,
        "status": "FAIL_AS_EXPECTED" if identical else "UNEXPECTED_PASS",
    }
    print(json.dumps(report, indent=2))
    return 1 if identical else 0


def no_signal_control():
    ground_dp = 0.2
    aggregate_dp = 0.0
    gap = abs(aggregate_dp - ground_dp)
    report = {
        "control": "Bayesian condition violation at p=0.5",
        "expected_failure": "Equation (9) sum is zero and a nonzero ground-truth DP is not recovered",
        "condition_9_partial_sum": 0.0,
        "ground_dp": ground_dp,
        "aggregate_dp": aggregate_dp,
        "gap_for_every_crowd_size": gap,
        "status": "FAIL_AS_EXPECTED" if gap > 0 else "UNEXPECTED_PASS",
    }
    print(json.dumps(report, indent=2))
    return 1 if gap > 0 else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("control", choices=("homogeneous", "no-signal"))
    args = parser.parse_args()
    if args.control == "homogeneous":
        return homogeneous_control()
    return no_signal_control()


if __name__ == "__main__":
    sys.exit(main())
