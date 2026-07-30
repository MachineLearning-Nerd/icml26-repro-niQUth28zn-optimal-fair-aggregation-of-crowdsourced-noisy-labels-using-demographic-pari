import json
import os
import platform
import subprocess
import time
from pathlib import Path

import numpy as np

import core


OUTPUT_DIR = Path("outputs")
Q = (0.65, 0.35)


def claim_result(claim_id, anchor, status, metrics, limitations):
    return {
        "claim": claim_id,
        "anchor": anchor,
        "status": status,
        "metrics": metrics,
        "limitations": limitations,
    }


def check_claim_1():
    sensitive, labels = core.sample_population(60_000, 0.5, Q, seed=1)
    ground_dp = Q[1] - Q[0]
    skill = 0.82
    exponent = core.k_mv([skill])
    crowd_sizes = [3, 5, 8, 12, 20, 30]
    errors = []
    gaps = []
    for crowd_size in crowd_sizes:
        votes = core.annotator_labels(
            sensitive, labels, np.full(crowd_size, skill), seed=crowd_size
        )
        prediction = core.majority_vote(votes)
        errors.append(float((prediction != labels).mean()))
        gaps.append(abs(core.delta_dp(prediction, sensitive) - ground_dp))
    error_slope = float(np.polyfit(crowd_sizes[:-1], np.log(errors[:-1]), 1)[0])
    gap_slope = float(np.polyfit(crowd_sizes[:-2], np.log(gaps[:-2]), 1)[0])
    passed = (
        error_slope < -0.7 * exponent
        and gap_slope < -0.15
        and gaps[-1] < gaps[0] / 5
    )
    return claim_result(
        "C1",
        "Proposition 3.2",
        "VERIFIED" if passed else "BLOCKED",
        {
            "crowd_sizes": crowd_sizes,
            "errors": errors,
            "dp_gaps": gaps,
            "theoretical_exponent": exponent,
            "error_log_slope": error_slope,
            "gap_log_slope": gap_slope,
        },
        "Historical Monte Carlo baseline; the tail is limited by sampling noise.",
    )


def bayes_homogeneous(votes, skill):
    vote_llr = np.where(
        votes == 1,
        np.log(skill / (1 - skill)),
        np.log((1 - skill) / skill),
    )
    return (vote_llr.sum(axis=1) > 0).astype(np.int8)


def check_claim_2():
    sensitive, labels = core.sample_population(40_000, 0.5, Q, seed=2)
    ground_dp = Q[1] - Q[0]
    rows = []
    predictions = {}
    passed = True
    for method in ("MajorityVote", "Bayesian"):
        method_rows = []
        for crowd_size in (4, 40):
            skill = 0.75
            votes = core.annotator_labels(
                sensitive, labels, np.full(crowd_size, skill), seed=crowd_size
            )
            if method == "MajorityVote":
                prediction = core.majority_vote(votes)
            else:
                prediction = bayes_homogeneous(votes, skill)
            predictions[(method, crowd_size)] = prediction
            gap = abs(core.delta_dp(prediction, sensitive) - ground_dp)
            method_rows.append({"crowd_size": crowd_size, "gap": gap})
        ratio = method_rows[-1]["gap"] / max(method_rows[0]["gap"], 1e-12)
        passed &= method_rows[-1]["gap"] < 0.03 and ratio < 0.4
        rows.append({"method": method, "values": method_rows, "ratio": ratio})
    identical = bool(
        np.array_equal(predictions[("MajorityVote", 40)], predictions[("Bayesian", 40)])
    )
    return claim_result(
        "C2",
        "Theorem 3.4",
        "BLOCKED",
        {"methods": rows, "bayes_identical_to_mv_at_r40": identical},
        "The homogeneous p=0.75 setup makes Bayesian vote identical to majority vote; "
        "this baseline intentionally preserves the live judge's criticism.",
    )


def check_claim_3():
    rows = []
    passed = True
    for crowd_size in (6, 10, 20, 40):
        skills = np.random.default_rng(crowd_size).uniform(0.6, 0.85, crowd_size)
        sensitive, labels = core.sample_population(
            40_000, 0.5, Q, seed=2 + crowd_size
        )
        votes = core.annotator_labels(
            sensitive,
            labels,
            skills,
            seed=crowd_size,
            bias=np.full(crowd_size, 0.05),
        )
        observed = abs(core.delta_dp(core.majority_vote(votes), sensitive))
        bound, epsilon_r, individual_sum = core.prop36_bound(votes, sensitive)
        holds = observed <= bound + 0.01
        passed &= holds
        rows.append(
            {
                "crowd_size": crowd_size,
                "observed_dp": observed,
                "bound": bound,
                "epsilon_r": epsilon_r,
                "individual_gap_sum": individual_sum,
                "holds": holds,
            }
        )
    return claim_result(
        "C3",
        "Proposition 3.6",
        "VERIFIED" if passed else "BLOCKED",
        {"rows": rows, "eta": core.ETA},
        "Historical Monte Carlo regression of the judged evidence.",
    )


def check_claim_4():
    sensitive, labels = core.sample_population(40_000, 0.5, Q, seed=5)
    ground_dp = Q[1] - Q[0]
    cases = [
        ("competent", 0.75, 40),
        ("weak_competent", 0.65, 60),
        ("random", 0.50, 40),
        ("adversarial", 0.40, 40),
    ]
    rows = []
    passed = True
    for name, skill, crowd_size in cases:
        skills = np.full(crowd_size, skill)
        eps = max(skill - 0.5, 0.01)
        condition, met = core.competent_majority(skills, eps, lower_bound=0.0)
        votes = core.annotator_labels(sensitive, labels, skills, seed=crowd_size)
        gap = abs(core.delta_dp(core.majority_vote(votes), sensitive) - ground_dp)
        converged = gap < 0.06
        passed &= converged == met
        rows.append(
            {
                "case": name,
                "skill": skill,
                "crowd_size": crowd_size,
                "condition_value": condition,
                "condition_met": met,
                "gap": gap,
                "converged": converged,
            }
        )
    return claim_result(
        "C4",
        "Condition (8), Lemma 3.3",
        "VERIFIED" if passed else "BLOCKED",
        {"rows": rows},
        "Historical homogeneous-skill Monte Carlo regression.",
    )


def check_claim_5():
    rng = np.random.default_rng(3)
    sample_count = 40_000
    sensitive = (rng.random(sample_count) < 0.5).astype(np.int8)
    score = rng.normal(0, 1, sample_count) + 0.8 * sensitive
    signal = 1 / (1 + np.exp(-score))
    labels = (rng.random(sample_count) < signal).astype(np.int8)
    posterior = np.clip(signal + rng.normal(0, 0.25, sample_count), 0, 1)
    rows = []
    passed = True
    for epsilon in (0.02, 0.05, 0.10, 0.20):
        prediction, beta, dp_gap = core.faircrowd(
            posterior, sensitive, np.array([0.5, 0.5]), epsilon
        )
        best_accuracy = 0.0
        for threshold_1 in np.linspace(0.2, 0.8, 121):
            for threshold_0 in np.linspace(0.2, 0.8, 121):
                thresholds = np.where(sensitive == 1, threshold_1, threshold_0)
                candidate = (posterior > thresholds).astype(np.int8)
                if abs(core.delta_dp(candidate, sensitive)) <= epsilon:
                    best_accuracy = max(
                        best_accuracy, core.accuracy(candidate, labels)
                    )
        observed_accuracy = core.accuracy(prediction, labels)
        fair = dp_gap <= epsilon
        near_grid_optimal = observed_accuracy >= best_accuracy - 0.015
        passed &= fair and near_grid_optimal
        rows.append(
            {
                "epsilon": epsilon,
                "beta": beta,
                "dp_gap": dp_gap,
                "accuracy": observed_accuracy,
                "grid_optimal_accuracy": best_accuracy,
                "accuracy_gap": best_accuracy - observed_accuracy,
            }
        )
    return claim_result(
        "C5",
        "Theorem 4.1",
        "VERIFIED" if passed else "BLOCKED",
        {"rows": rows},
        "Historical Monte Carlo baseline uses a 121x121 threshold grid, not an exact LP.",
    )


def git_sha():
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()


def main():
    started = time.perf_counter()
    OUTPUT_DIR.mkdir(exist_ok=True)
    claims = [
        check_claim_1(),
        check_claim_2(),
        check_claim_3(),
        check_claim_4(),
        check_claim_5(),
    ]
    runtime = time.perf_counter() - started
    metadata = {
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "logical_cpu_count": os.cpu_count(),
        "affinity_cpu_count": len(os.sched_getaffinity(0))
        if hasattr(os, "sched_getaffinity")
        else None,
        "estimated_required_cores": 1,
        "selected_compute": "recorded by orx run metadata",
        "runtime_seconds": runtime,
        "seeds": [1, 2, 3, 5],
        "environment": "uv.lock, Python 3.12",
    }
    result = {
        "paper": "2601.23221",
        "baseline_space_revision": "eee6b5ec719b769b952bd978850bffba2ba590c3",
        "claims": claims,
        "metadata": metadata,
        "all_regressions_pass": all(
            claim["status"] == "VERIFIED"
            for claim in claims
            if claim["claim"] != "C2"
        ),
        "claim_2_expected_blocked": claims[1]["status"] == "BLOCKED",
    }
    (OUTPUT_DIR / "baseline_results.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print("RUN_METADATA_JSON=" + json.dumps(metadata, sort_keys=True))
    print("BASELINE_RESULTS_JSON")
    print(json.dumps(result, indent=2))
    if not result["all_regressions_pass"] or not result["claim_2_expected_blocked"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
