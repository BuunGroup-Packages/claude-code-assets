#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Lighthouse Runner

Runs Lighthouse audit and returns clean JSON results.
Handles WSL/Linux chrome flags automatically.

Usage:
    uv run lighthouse.py --url http://localhost:3000
    uv run lighthouse.py --url http://localhost:3000 --target 90
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_lighthouse(url: str, target_score: int = 100) -> dict:
    """
    Run Lighthouse audit and return results.

    Args:
        url: URL to audit
        target_score: Minimum score target (0-100)

    Returns:
        Dict with scores and issues
    """
    # Chrome flags for headless/WSL
    chrome_flags = "--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"

    # Output file
    output_path = Path("/tmp/lighthouse-report.json")

    # Run lighthouse
    cmd = [
        "npx", "lighthouse", url,
        "--output=json",
        f"--output-path={output_path}",
        f"--chrome-flags={chrome_flags}",
        "--only-categories=performance,accessibility,best-practices,seo",
        "--quiet"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
    except subprocess.TimeoutExpired:
        return {"error": "Lighthouse timeout after 120s"}
    except FileNotFoundError:
        return {"error": "npx/lighthouse not found. Run: npm install -g lighthouse"}

    # Parse results
    if not output_path.exists():
        return {"error": f"Lighthouse failed: {result.stderr[:200]}"}

    try:
        report = json.loads(output_path.read_text())
    except json.JSONDecodeError:
        return {"error": "Invalid Lighthouse JSON output"}

    # Extract scores
    categories = report.get("categories", {})
    scores = {
        "performance": int((categories.get("performance", {}).get("score") or 0) * 100),
        "accessibility": int((categories.get("accessibility", {}).get("score") or 0) * 100),
        "best-practices": int((categories.get("best-practices", {}).get("score") or 0) * 100),
        "seo": int((categories.get("seo", {}).get("score") or 0) * 100),
    }

    # Check against target
    passed = all(score >= target_score for score in scores.values())

    # Extract failing audits
    audits = report.get("audits", {})
    issues = []

    for audit_id, audit in audits.items():
        score = audit.get("score")
        if score is not None and score < 1:
            issues.append({
                "id": audit_id,
                "title": audit.get("title", audit_id),
                "score": int(score * 100),
                "description": audit.get("description", "")[:100]
            })

    # Sort by score (worst first)
    issues.sort(key=lambda x: x["score"])

    return {
        "url": url,
        "target": target_score,
        "passed": passed,
        "scores": scores,
        "issues": issues[:15],  # Top 15 issues
        "issue_count": len(issues)
    }


def format_report(result: dict) -> str:
    """Format result as readable report."""
    if "error" in result:
        return f"✗ LIGHTHOUSE ERROR\n{result['error']}"

    lines = []

    # Header
    status = "✓ PASSED" if result["passed"] else "✗ FAILED"
    lines.append(f"{status} - Lighthouse Audit")
    lines.append(f"URL: {result['url']}")
    lines.append(f"Target: {result['target']}")
    lines.append("")

    # Scores
    lines.append("SCORES:")
    for category, score in result["scores"].items():
        indicator = "✓" if score >= result["target"] else "✗"
        lines.append(f"  {indicator} {category}: {score}/100")
    lines.append("")

    # Issues
    if result["issues"]:
        lines.append(f"TOP ISSUES ({result['issue_count']} total):")
        for issue in result["issues"][:10]:
            lines.append(f"  - [{issue['score']}] {issue['title']}")

    return "\n".join(lines)


def validate_localhost(url: str) -> bool:
    """Check if URL is localhost/127.0.0.1."""
    localhost_patterns = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "[::1]",
    ]
    return any(pattern in url.lower() for pattern in localhost_patterns)


def main():
    parser = argparse.ArgumentParser(description="Run Lighthouse audit")
    parser.add_argument("--url", default="http://localhost:3000", help="URL to audit (must be localhost)")
    parser.add_argument("--target", type=int, default=100, help="Target score (0-100)")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    # Enforce localhost - Lighthouse should run against local dev server
    if not validate_localhost(args.url):
        error_msg = (
            "✗ ERROR: Lighthouse must run against localhost\n"
            f"  Provided: {args.url}\n"
            "  Use: http://localhost:3000 or http://localhost:4321\n"
            "\n"
            "Start your dev server first:\n"
            "  npm run dev\n"
            "  pnpm dev\n"
            "  yarn dev"
        )
        if args.json:
            print(json.dumps({"error": "URL must be localhost", "url": args.url}))
        else:
            print(error_msg)
        sys.exit(1)

    result = run_lighthouse(args.url, args.target)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))

    # Exit code based on pass/fail
    sys.exit(0 if result.get("passed", False) else 1)


if __name__ == "__main__":
    main()
