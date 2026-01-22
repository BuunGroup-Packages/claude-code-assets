#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
PostToolUse Hook: AI SEO Validation

Validates llms.txt and robots.txt for AI crawler access.

Trigger: Edit|Write|MultiEdit on AI SEO files (llms.txt, robots.txt)
Output: Success message or ordered list of fixes

Run with: uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/post_ai_validate.py
"""
import json
import os
import re
import sys
from pathlib import Path

# Add lib to path - supports both direct run and CLAUDE_PROJECT_DIR
hook_dir = Path(__file__).parent
if "CLAUDE_PROJECT_DIR" in os.environ:
    hook_dir = Path(os.environ["CLAUDE_PROJECT_DIR"]) / ".claude" / "hooks" / "seo"
sys.path.insert(0, str(hook_dir))

from lib.response import success, failure, skip, AIErrors, ValidationError
from lib.validators import is_ai_file


# =============================================================================
# CONFIGURATION
# =============================================================================

AI_BOTS = [
    "GPTBot",
    "ClaudeBot", 
    "PerplexityBot",
    "Google-Extended",
    "Amazonbot",
    "anthropic-ai",
    "Bytespider",
    "CCBot",
    "ChatGPT-User",
    "cohere-ai",
]

LLMS_TXT_REQUIRED_SECTIONS = [
    "About",
]

LLMS_TXT_RECOMMENDED_SECTIONS = [
    "Key Pages",
    "Contact",
]


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main() -> None:
    """Main hook entry point."""
    data = json.load(sys.stdin)
    
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    
    # Only validate after Edit/Write
    if tool_name not in ("Edit", "Write", "MultiEdit"):
        print(skip())
        return
    
    # Check if file is AI SEO related
    if not is_ai_file(file_path):
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

    # Route to appropriate validator
    file_name = path.name.lower()
    
    if "llms" in file_name:
        errors, warnings = validate_llms_txt(content, file_path)
    elif "robots" in file_name:
        errors, warnings = validate_robots_txt(content, file_path)
    else:
        print(skip())
        return
    
    if errors:
        print(failure(file_path, "AI-SEO", errors, warnings))
    elif warnings:
        print(failure(file_path, "AI-SEO", [], warnings))
    else:
        print(success(file_path, "AI-SEO"))


# =============================================================================
# LLMS.TXT VALIDATION
# =============================================================================

def validate_llms_txt(content: str, file_path: str) -> tuple[list[ValidationError], list[ValidationError]]:
    """
    Validate llms.txt file structure and content.
    
    Args:
        content: File content
        file_path: Path to file
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    lines = content.strip().split("\n")
    
    if not lines:
        errors.append(AIErrors.llms_missing_title(file_path, 1))
        return errors, warnings
    
    # Check for title (# Site Name)
    first_line = lines[0].strip()
    if not first_line.startswith("#"):
        errors.append(AIErrors.llms_missing_title(file_path, 1))
    
    # Check for description (> One line description)
    has_description = False
    for i, line in enumerate(lines[:5], 1):  # Check first 5 lines
        if line.strip().startswith(">"):
            has_description = True
            break
    
    if not has_description:
        errors.append(AIErrors.llms_missing_description(file_path, 2))
    
    # Check for required sections
    content_lower = content.lower()
    for section in LLMS_TXT_REQUIRED_SECTIONS:
        if f"## {section.lower()}" not in content_lower:
            # Find approximate line to add it
            line_num = len(lines) // 2  # Middle of file
            errors.append(AIErrors.llms_missing_section(file_path, section, line_num))
    
    # Check for recommended sections (warnings)
    for section in LLMS_TXT_RECOMMENDED_SECTIONS:
        if f"## {section.lower()}" not in content_lower:
            warnings.append(AIErrors.llms_missing_section(file_path, section))
    
    # Check content length
    if len(content) < 100:
        warnings.append(ValidationError(
            code="AI007",
            severity="warning",
            file=file_path,
            line=None,
            element="llms.txt",
            rule="llms.txt should have substantive content (≥100 chars)",
            current=f"{len(content)} characters",
            expected="≥100 characters",
            fix="Add more descriptive content about your site, key pages, and what AI assistants should know."
        ))
    
    return errors, warnings


# =============================================================================
# ROBOTS.TXT VALIDATION
# =============================================================================

def validate_robots_txt(content: str, file_path: str) -> tuple[list[ValidationError], list[ValidationError]]:
    """
    Validate robots.txt for AI crawler configuration.
    
    Args:
        content: File content
        file_path: Path to file
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    lines = content.split("\n")
    content_lower = content.lower()
    
    # Parse robots.txt into user-agent blocks
    blocks = parse_robots_txt(content)
    
    # Check each AI bot
    for bot in AI_BOTS:
        bot_lower = bot.lower()
        
        # Check if bot is explicitly blocked
        if bot_lower in blocks:
            rules = blocks[bot_lower]
            if is_blocked(rules):
                # Find line number
                line_num = find_user_agent_line(lines, bot)
                warnings.append(AIErrors.robots_blocks_ai(file_path, bot, line_num))
        
        # Check if wildcard blocks this bot
        elif "*" in blocks:
            rules = blocks["*"]
            if is_blocked(rules) and bot_lower not in blocks:
                # Bot might be blocked by wildcard
                warnings.append(ValidationError(
                    code="AI008",
                    severity="warning",
                    file=file_path,
                    line=find_user_agent_line(lines, "*"),
                    element="robots.txt",
                    rule=f"Wildcard User-agent may block {bot}",
                    current="User-agent: *\\nDisallow: /",
                    expected=f"Add explicit allow for {bot}",
                    fix=f"Add 'User-agent: {bot}\\nAllow: /' before the wildcard block to allow AI crawlers."
                ))
    
    # Check for sitemap reference
    if "sitemap:" not in content_lower:
        warnings.append(ValidationError(
            code="AI009",
            severity="warning",
            file=file_path,
            line=None,
            element="robots.txt",
            rule="robots.txt should reference sitemap",
            current=None,
            expected="Sitemap: https://yourdomain.com/sitemap.xml",
            fix="Add 'Sitemap: https://yourdomain.com/sitemap.xml' at the end of robots.txt."
        ))
    
    return errors, warnings


def parse_robots_txt(content: str) -> dict[str, list[str]]:
    """
    Parse robots.txt into user-agent blocks.
    
    Returns:
        Dict mapping user-agent to list of rules
    """
    blocks: dict[str, list[str]] = {}
    current_agent = None
    
    for line in content.split("\n"):
        line = line.strip().lower()
        
        if line.startswith("user-agent:"):
            current_agent = line.split(":", 1)[1].strip()
            if current_agent not in blocks:
                blocks[current_agent] = []
        elif current_agent and (line.startswith("disallow:") or line.startswith("allow:")):
            blocks[current_agent].append(line)
    
    return blocks


def is_blocked(rules: list[str]) -> bool:
    """Check if rules result in blocking root."""
    for rule in rules:
        if rule.startswith("disallow:"):
            path = rule.split(":", 1)[1].strip()
            if path == "/" or path == "":
                # Check if there's a subsequent allow
                return True
    return False


def find_user_agent_line(lines: list[str], agent: str) -> int | None:
    """Find line number of user-agent directive."""
    agent_lower = agent.lower()
    for i, line in enumerate(lines, 1):
        if line.lower().strip().startswith("user-agent:"):
            if agent_lower in line.lower():
                return i
    return None


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
