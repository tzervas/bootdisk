import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Finding:
    severity: str  # BLOCKER | WARN | INFO
    title: str
    details: str


REQUIRED_SECTIONS = [
    "Problem",
    "Solution",
    "Functional Impact",
    "Testing",
]

OPTIONAL_STRONGLY_RECOMMENDED_SECTIONS = [
    "Rollback Plan",
    "Metrics",
    "Visualizations",
]

CONVENTIONAL_COMMIT_RE = re.compile(r"^(feat|fix|docs|refactor|test|chore|ci|build|perf|style)(\(.+\))?: .+")


def gh_api_request(path: str, method: str = "GET", body: Optional[dict] = None) -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        raise RuntimeError("Missing GITHUB_TOKEN or GITHUB_REPOSITORY")

    url = f"https://api.github.com/repos/{repo}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "bootdisk-pr-review-agent",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def pr_has_required_sections(pr_body: str) -> Tuple[bool, List[str]]:
    missing = []
    normalized = pr_body or ""

    for section in REQUIRED_SECTIONS:
        # Accept either markdown header or bold label
        pattern = re.compile(rf"(^|\n)\s*(#{1,6}\s*{re.escape(section)}\b|\*\*{re.escape(section)}\*\*)", re.IGNORECASE)
        if not pattern.search(normalized):
            missing.append(section)

    return (len(missing) == 0), missing


def score_visuals_and_metrics(pr_body: str) -> Dict[str, bool]:
    body = pr_body or ""
    return {
        "has_mermaid": "```mermaid" in body,
        "has_metrics": re.search(r"(^|\n)\s*(#{1,6}\s*Metrics\b|\*\*Metrics\*\*)", body, re.IGNORECASE) is not None,
        "has_visualizations": re.search(r"(^|\n)\s*(#{1,6}\s*Visualizations\b|\*\*Visualizations\*\*)", body, re.IGNORECASE) is not None,
        "has_rollback": re.search(r"(^|\n)\s*(#{1,6}\s*Rollback Plan\b|\*\*Rollback Plan\*\*)", body, re.IGNORECASE) is not None,
    }


def get_changed_files(pr_number: int) -> List[dict]:
    files: List[dict] = []
    page = 1

    while True:
        chunk = gh_api_request(f"/pulls/{pr_number}/files?per_page=100&page={page}")
        if not chunk:
            break
        files.extend(chunk)
        page += 1

    return files


def summarize_diff_metrics(files: List[dict]) -> Dict[str, int]:
    additions = sum(int(f.get("additions", 0)) for f in files)
    deletions = sum(int(f.get("deletions", 0)) for f in files)
    changed_files = len(files)

    binary_files = 0
    for f in files:
        # GitHub marks binary diffs by missing patch; we treat those as higher risk
        if f.get("patch") is None and f.get("status") in {"added", "modified"}:
            binary_files += 1

    return {
        "changed_files": changed_files,
        "additions": additions,
        "deletions": deletions,
        "binary_like_files": binary_files,
    }


def build_review_body(verdict: str, risk: str, findings: List[Finding], metrics: Dict[str, int], pr_url: str) -> str:
    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warns = [f for f in findings if f.severity == "WARN"]

    primary_concerns = blockers[:2] + warns[:1]

    lines: List[str] = []
    lines.append("### Summary")
    lines.append(f"- **Verdict:** `{verdict}`")
    lines.append(f"- **Risk:** {risk}")
    if primary_concerns:
        lines.append("- **Primary concerns:**")
        for f in primary_concerns:
            lines.append(f"  - {f.title}")
    else:
        lines.append("- **Primary concerns:** None")

    lines.append("")
    lines.append("### Metrics")
    lines.append(f"- Files changed: {metrics['changed_files']}")
    lines.append(f"- Lines added: {metrics['additions']}")
    lines.append(f"- Lines deleted: {metrics['deletions']}")
    if metrics.get("binary_like_files", 0) > 0:
        lines.append(f"- Binary-like files (no patch): {metrics['binary_like_files']} (review carefully)")

    lines.append("")
    lines.append("### Blocking Issues (must fix)")
    if blockers:
        for idx, f in enumerate(blockers, start=1):
            lines.append(f"{idx}. **{f.title}**\n   - {f.details}")
    else:
        lines.append("None")

    lines.append("")
    lines.append("### Non-blocking Improvements")
    if warns:
        for f in warns:
            lines.append(f"- **{f.title}** — {f.details}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("### Verification")
    lines.append("- Ensure CI is green")
    lines.append("- Run the most relevant local tests for touched areas")

    lines.append("")
    lines.append("### Visualizations")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    lines.append("  A[PR Opened/Updated] --> B[Quality Gates Action]")
    lines.append("  B --> C{Metadata OK?}")
    lines.append("  C -- No --> D[Request Changes]")
    lines.append("  C -- Yes --> E[Continue Review]\n(maintainers)")
    lines.append("```")

    lines.append("")
    lines.append(f"_Automated by PR Review Agent for {pr_url}_")

    return "\n".join(lines)


def main() -> int:
    pr_number_str = os.environ.get("PR_NUMBER")
    pr_title = os.environ.get("PR_TITLE") or ""
    pr_body = os.environ.get("PR_BODY") or ""
    pr_url = os.environ.get("PR_URL") or ""

    if not pr_number_str:
        print("Missing PR_NUMBER env var", file=sys.stderr)
        return 2

    pr_number = int(pr_number_str)

    findings: List[Finding] = []

    if not CONVENTIONAL_COMMIT_RE.match(pr_title.strip()):
        findings.append(Finding(
            severity="BLOCKER",
            title="PR title is not Conventional Commits format",
            details="Update the PR title to match `type(scope?): description` (e.g. `feat: add CI workflow`).",
        ))

    ok, missing = pr_has_required_sections(pr_body)
    if not ok:
        findings.append(Finding(
            severity="BLOCKER",
            title="PR description missing required sections",
            details=f"Add these sections to the PR body: {', '.join(missing)}.",
        ))

    extras = score_visuals_and_metrics(pr_body)
    if not extras["has_metrics"]:
        findings.append(Finding(
            severity="WARN",
            title="PR body missing Metrics section",
            details="Add a `Metrics` section (diffstat, test results, performance impacts, etc.).",
        ))
    if not extras["has_visualizations"]:
        findings.append(Finding(
            severity="WARN",
            title="PR body missing Visualizations section",
            details="Add a `Visualizations` section with Mermaid diagrams when it helps explain changes.",
        ))

    # Diff-based checks
    files = get_changed_files(pr_number)
    metrics = summarize_diff_metrics(files)

    if metrics.get("binary_like_files", 0) > 0:
        findings.append(Finding(
            severity="WARN",
            title="PR contains binary-like diffs",
            details="One or more files do not include patch data; ensure changes are reviewable or provide screenshots/artifacts.",
        ))

    # Lightweight guardrails
    if metrics["additions"] + metrics["deletions"] > 2000:
        findings.append(Finding(
            severity="WARN",
            title="Large PR",
            details="Consider splitting into smaller PRs for reviewability unless this is unavoidable.",
        ))

    verdict = "REQUEST_CHANGES" if any(f.severity == "BLOCKER" for f in findings) else "COMMENT_ONLY"
    risk = "High" if metrics["additions"] + metrics["deletions"] > 1500 else "Medium" if metrics["additions"] + metrics["deletions"] > 400 else "Low"

    review_body = build_review_body(verdict, risk, findings, metrics, pr_url)

    event = "REQUEST_CHANGES" if verdict == "REQUEST_CHANGES" else "COMMENT"

    gh_api_request(
        f"/pulls/{pr_number}/reviews",
        method="POST",
        body={
            "body": review_body,
            "event": event,
        },
    )

    print(f"Posted review: {verdict} (risk={risk})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
