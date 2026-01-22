#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
PostToolUse Hook: Sitemap Validation

Validates sitemap.xml structure and content.

Trigger: Edit|Write|MultiEdit on sitemap files
Output: Success message or ordered list of fixes
"""
import json
import os
import re
import sys
from pathlib import Path

# Add lib to path
hook_dir = Path(__file__).parent
if "CLAUDE_PROJECT_DIR" in os.environ:
    hook_dir = Path(os.environ["CLAUDE_PROJECT_DIR"]) / ".claude" / "hooks" / "seo"
sys.path.insert(0, str(hook_dir))

from lib.response import success, failure, skip, ValidationError


def main() -> None:
    """Main hook entry point."""
    data = json.load(sys.stdin)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if tool_name not in ("Edit", "Write", "MultiEdit"):
        print(skip())
        return

    # Only validate sitemap files
    if "sitemap" not in file_path.lower():
        print(skip())
        return

    # Read file (skip directories)
    path = Path(file_path)
    if not path.is_file():
        print(skip())
        return

    try:
        content = path.read_text()
    except (FileNotFoundError, PermissionError, OSError):
        print(skip())
        return

    errors, warnings = validate_sitemap(content, file_path)

    if errors:
        print(failure(file_path, "SITEMAP", errors, warnings))
    elif warnings:
        print(failure(file_path, "SITEMAP", [], warnings))
    else:
        print(success(file_path, "SITEMAP"))


def validate_sitemap(content: str, file_path: str) -> tuple[list, list]:
    """Validate sitemap.xml content."""
    errors = []
    warnings = []

    # Check XML declaration
    if not content.strip().startswith("<?xml"):
        errors.append(ValidationError(
            code="SITEMAP001",
            severity="error",
            file=file_path,
            line=1,
            element="sitemap.xml",
            rule="Sitemap must be valid XML",
            current="Missing XML declaration",
            expected='<?xml version="1.0" encoding="UTF-8"?>',
            fix="Add XML declaration at the start of the file."
        ))

    # Check urlset namespace
    if "xmlns=" not in content or "sitemaps.org" not in content:
        errors.append(ValidationError(
            code="SITEMAP002",
            severity="error",
            file=file_path,
            line=None,
            element="<urlset>",
            rule="Sitemap must have proper namespace",
            current="Missing or invalid namespace",
            expected='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            fix="Add xmlns attribute to urlset element."
        ))

    # Check for URLs
    urls = re.findall(r'<loc>([^<]+)</loc>', content)

    if not urls:
        errors.append(ValidationError(
            code="SITEMAP003",
            severity="error",
            file=file_path,
            line=None,
            element="<url>",
            rule="Sitemap must contain at least one URL",
            current="No URLs found",
            expected="<url><loc>https://...</loc></url>",
            fix="Add at least one URL entry."
        ))

    # Check URLs are absolute
    for url in urls:
        if not url.startswith("http"):
            line = find_line(content, url)
            errors.append(ValidationError(
                code="SITEMAP003",
                severity="error",
                file=file_path,
                line=line,
                element=f"<loc>{url[:50]}...</loc>" if len(url) > 50 else f"<loc>{url}</loc>",
                rule="Sitemap URLs must be absolute",
                current=url,
                expected="https://yourdomain.com/...",
                fix="Use absolute URLs starting with https://."
            ))

    # Check for lastmod (warning)
    if "<lastmod>" not in content:
        warnings.append(ValidationError(
            code="SITEMAP004",
            severity="warning",
            file=file_path,
            line=None,
            element="<lastmod>",
            rule="Sitemap should include lastmod dates",
            current="No lastmod elements found",
            expected="<lastmod>2026-01-22</lastmod>",
            fix="Add lastmod element to each URL for better crawling."
        ))

    return errors, warnings


def find_line(content: str, search: str) -> int | None:
    """Find line number containing search string."""
    for i, line in enumerate(content.split("\n"), 1):
        if search in line:
            return i
    return None


if __name__ == "__main__":
    main()
