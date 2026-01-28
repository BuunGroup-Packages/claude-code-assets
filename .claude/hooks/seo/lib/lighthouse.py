#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Lighthouse Runner

Runs Lighthouse audit and returns clean JSON results.
Handles WSL/Linux chrome flags automatically.
Saves reports to reports/seo/ and cleans up temp files.

Usage:
    uv run lighthouse.py --url http://localhost:3000
    uv run lighthouse.py --url http://localhost:3000 --target 90
"""
import argparse
import glob
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_lighthouse_temp_dirs(project_root: Path | None = None) -> list[Path]:
    """Find lighthouse temp directories to clean up."""
    temp_dirs = []

    # Windows native: AppData\Local\lighthouse.*
    if platform.system() == "Windows":
        appdata = os.environ.get("LOCALAPPDATA", "")
        if appdata:
            pattern = os.path.join(appdata, "lighthouse.*")
            temp_dirs.extend(Path(p) for p in glob.glob(pattern))

    # WSL: Windows AppData is at /mnt/c/Users/<user>/AppData/Local/
    wsl_appdata_pattern = "/mnt/c/Users/*/AppData/Local/lighthouse.*"
    temp_dirs.extend(Path(p) for p in glob.glob(wsl_appdata_pattern))

    # Linux/WSL: /tmp/lighthouse.*
    tmp_pattern = "/tmp/lighthouse.*"
    temp_dirs.extend(Path(p) for p in glob.glob(tmp_pattern))

    # Chrome user data dirs
    chrome_patterns = [
        "/tmp/.org.chromium.Chromium.*",
        "/tmp/.com.google.Chrome.*",
        "/tmp/puppeteer_dev_chrome_profile-*",
    ]
    for pattern in chrome_patterns:
        temp_dirs.extend(Path(p) for p in glob.glob(pattern))

    # WSL BUG: Lighthouse sometimes creates dirs with Windows paths IN the project!
    # e.g., "C:\Users\sacha\AppData\Local\lighthouse.12345" as a literal folder name
    if project_root:
        for item in project_root.iterdir():
            name = item.name
            # Match: C:\...\lighthouse.* or anything starting with C: containing lighthouse
            if name.startswith("C:") and "lighthouse" in name.lower():
                temp_dirs.append(item)
            # Also catch partial paths
            if "AppData" in name and "lighthouse" in name.lower():
                temp_dirs.append(item)

    return temp_dirs


def cleanup_lighthouse_temp(project_root: Path | None = None) -> int:
    """Clean up lighthouse temp directories. Returns count of cleaned dirs."""
    cleaned = 0
    for temp_dir in get_lighthouse_temp_dirs(project_root):
        try:
            if temp_dir.is_dir():
                shutil.rmtree(temp_dir)
                cleaned += 1
            elif temp_dir.is_file():
                temp_dir.unlink()
                cleaned += 1
        except (PermissionError, OSError):
            pass  # Skip if can't delete
    return cleaned


def get_project_root() -> Path:
    """Get project root directory (parent of .claude/)."""
    # Script is at: PROJECT/.claude/hooks/seo/lib/lighthouse.py
    # Go up: lib -> seo -> hooks -> .claude -> PROJECT
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent.parent.parent
    return project_root


def get_report_path(project_dir: Path) -> Path:
    """Get path for saving report inside the project."""
    reports_dir = project_dir / "reports" / "seo"
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return reports_dir / f"lighthouse-{timestamp}.json"


def run_lighthouse(url: str, target_score: int = 100, project_dir: Path | None = None) -> dict:
    """
    Run Lighthouse audit and return results.

    Args:
        url: URL to audit
        target_score: Minimum score target (0-100)
        project_dir: Project directory for saving reports

    Returns:
        Dict with scores and issues
    """
    # Chrome flags for headless/WSL
    chrome_flags = "--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"

    # Output file - temp location for initial run
    temp_output = Path("/tmp/lighthouse-report.json")

    # Final report path
    if project_dir:
        output_path = get_report_path(project_dir)
    else:
        output_path = temp_output

    # Run lighthouse (always write to temp first)
    cmd = [
        "npx", "lighthouse", url,
        "--output=json",
        f"--output-path={temp_output}",
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
        cleanup_lighthouse_temp(project_dir)
        return {"error": "Lighthouse timeout after 120s"}
    except FileNotFoundError:
        return {"error": "npx/lighthouse not found. Run: npm install -g lighthouse"}

    # Clean up lighthouse temp directories (AppData\Local\lighthouse.*, /tmp/lighthouse.*, project junk)
    cleaned_count = cleanup_lighthouse_temp(project_dir)

    # Parse results
    if not temp_output.exists():
        return {"error": f"Lighthouse failed: {result.stderr[:200]}"}

    try:
        report = json.loads(temp_output.read_text())
    except json.JSONDecodeError:
        return {"error": "Invalid Lighthouse JSON output"}

    # Copy to final report location if project_dir provided
    report_saved_to = None
    if project_dir and output_path != temp_output:
        shutil.copy(temp_output, output_path)
        report_saved_to = str(output_path)
        # Clean up temp file
        temp_output.unlink(missing_ok=True)

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

    result_data = {
        "url": url,
        "target": target_score,
        "passed": passed,
        "scores": scores,
        "issues": issues[:15],  # Top 15 issues
        "issue_count": len(issues),
        "cleaned_temp_dirs": cleaned_count,
    }

    if report_saved_to:
        result_data["report_path"] = report_saved_to

    return result_data


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
        lines.append("")

    # Report location
    if "report_path" in result:
        lines.append(f"Report saved: {result['report_path']}")

    # Cleanup info
    if result.get("cleaned_temp_dirs", 0) > 0:
        lines.append(f"Cleaned up {result['cleaned_temp_dirs']} temp directories")

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
    parser.add_argument("--no-save", action="store_true", help="Don't save report to reports/seo/")

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

    # Determine project directory for saving reports
    # Reports go to PROJECT/reports/seo/ (derived from script location)
    project_dir = None
    if not args.no_save:
        project_dir = get_project_root()

    result = run_lighthouse(args.url, args.target, project_dir)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))

    # Exit code based on pass/fail
    sys.exit(0 if result.get("passed", False) else 1)


if __name__ == "__main__":
    main()
