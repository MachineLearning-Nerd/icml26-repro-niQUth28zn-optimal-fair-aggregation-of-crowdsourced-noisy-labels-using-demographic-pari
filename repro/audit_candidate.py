import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


HASH_LINK = re.compile(r"\]\(#/([a-z0-9-]+)\)")
HF_LINK = re.compile(
    r"https://huggingface\.co/spaces/DineshAI/niQUth28zn/(?:blob|resolve)/main/([^)]+)"
)
SECRET_PATTERNS = (
    re.compile(r"hf_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_candidate(baseline, overlay, candidate):
    if candidate.exists():
        shutil.rmtree(candidate)
    shutil.copytree(baseline, candidate, ignore=shutil.ignore_patterns(".git"))
    for source in overlay.rglob("*"):
        if not source.is_file():
            continue
        destination = candidate / source.relative_to(overlay)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def audit(baseline, overlay, candidate):
    opened = []
    failures = []

    baseline_files = {
        path.relative_to(baseline).as_posix()
        for path in baseline.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
    candidate_files = {
        path.relative_to(candidate).as_posix()
        for path in candidate.rglob("*")
        if path.is_file()
    }
    missing_old_paths = sorted(baseline_files - candidate_files)
    if missing_old_paths:
        failures.append(f"missing judged paths: {missing_old_paths}")

    overlay_paths = {
        path.relative_to(overlay).as_posix()
        for path in overlay.rglob("*")
        if path.is_file()
    }
    changed_unlisted = []
    for relative in sorted(baseline_files - overlay_paths):
        if sha256(baseline / relative) != sha256(candidate / relative):
            changed_unlisted.append(relative)
    if changed_unlisted:
        failures.append(f"unexpected changes to judged files: {changed_unlisted}")

    entrypoints = ["README.md", "logbook.json", "pages/index.md"]
    for relative in entrypoints:
        path = candidate / relative
        opened.append(relative)
        if not path.is_file():
            failures.append(f"missing entrypoint: {relative}")

    logbook = json.loads((candidate / "logbook.json").read_text())
    route_map = {
        child["slug"]: child["file"] for child in logbook["root"]["children"]
    }
    if logbook["root"]["children"][0]["slug"] != "current-verification":
        failures.append("current verification is not first in navigation")
    historical = route_map.get("verification-run")
    historical_title = next(
        (
            child["title"]
            for child in logbook["root"]["children"]
            if child["slug"] == "verification-run"
        ),
        "",
    )
    if historical != "pages/verification-run/page.md":
        failures.append("historical verifier path was not preserved")
    if historical_title != "Historical rejected baseline":
        failures.append("historical verifier label is not exact")

    queue = ["pages/index.md"]
    visited = set()
    while queue:
        relative = queue.pop(0)
        if relative in visited:
            continue
        visited.add(relative)
        opened.append(relative)
        text = (candidate / relative).read_text()
        for slug in HASH_LINK.findall(text):
            target = route_map.get(slug)
            if target is None:
                failures.append(f"unresolved route #{slug} from {relative}")
            elif target not in visited:
                queue.append(target)
        for target in HF_LINK.findall(text):
            opened.append(target)
            if not (candidate / target).is_file():
                failures.append(f"unresolved artifact/code link {target} from {relative}")

    current_page = (candidate / "pages/current-verification/page.md").read_text()
    required_phrases = (
        "Source and claim contracts",
        "Assumptions and numerical audit",
        "Cumulative raw evidence",
        "Independent checkers and negative controls",
        "Reproduction metadata and limitations",
        "Visibility matrix",
        "10451115e7ef0ba33a07b7b1ea20a5aaca959e8f",
        "uv run --frozen python repro/run_all.py",
    )
    for phrase in required_phrases:
        if phrase not in current_page:
            failures.append(f"current page missing: {phrase}")
    for claim in range(1, 6):
        if f"| C{claim} |" not in current_page:
            failures.append(f"visibility row missing for C{claim}")

    for relative in sorted(candidate_files):
        path = candidate / relative
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f"possible secret in {relative}")

    allowlist = sorted(overlay_paths)
    non_text = []
    for relative in allowlist:
        try:
            (overlay / relative).read_text()
        except UnicodeDecodeError:
            non_text.append(relative)
    if non_text:
        failures.append(f"non-text upload paths: {non_text}")

    return {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "opened_files": opened,
        "judged_file_count": len(baseline_files),
        "candidate_file_count": len(candidate_files),
        "old_file_set_is_subset": not missing_old_paths,
        "unchanged_judged_files_outside_overlay": not changed_unlisted,
        "upload_allowlist": allowlist,
        "upload_sha256": {
            relative: sha256(overlay / relative) for relative in allowlist
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    copy_candidate(args.baseline, args.overlay, args.candidate)
    report = audit(args.baseline, args.overlay, args.candidate)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
