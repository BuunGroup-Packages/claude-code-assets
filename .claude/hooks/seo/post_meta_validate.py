#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
PostToolUse Hook: Meta Tag Validation

Validates meta tags after file edit. Returns precise fix instructions.

Trigger: Edit|Write|MultiEdit on meta-related files
Output: Success message or ordered list of fixes

Run with: uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/post_meta_validate.py
"""
import json
import os
import sys
from pathlib import Path

# Add lib to path - supports both direct run and CLAUDE_PROJECT_DIR
hook_dir = Path(__file__).parent
if "CLAUDE_PROJECT_DIR" in os.environ:
    hook_dir = Path(os.environ["CLAUDE_PROJECT_DIR"]) / ".claude" / "hooks" / "seo"
sys.path.insert(0, str(hook_dir))

from lib.response import success, failure, skip, MetaErrors, ValidationError
from lib.validators import (
    is_meta_file, 
    detect_framework,
    find_head_line,
    find_line_number,
    extract_tag_content,
    extract_meta_content,
)


# =============================================================================
# CONFIGURATION
# =============================================================================

TITLE_MIN = 10
TITLE_MAX = 60
DESC_MIN = 120
DESC_MAX = 160

# Non-descriptive link text patterns (case-insensitive)
NON_DESCRIPTIVE_LINKS = [
    "learn more",
    "read more",
    "click here",
    "here",
    "more",
    "link",
    "this",
    "more info",
    "info",
    "details",
    "see more",
    "view more",
    "continue",
    "continue reading",
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
    
    # Check if file is meta-related
    if not is_meta_file(file_path):
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
    
    # Validate
    errors, warnings = validate_meta(content, file_path)
    
    if errors:
        print(failure(file_path, "META", errors, warnings))
    elif warnings:
        # Warnings only - still success but with feedback
        print(failure(file_path, "META", [], warnings))
    else:
        print(success(file_path, "META"))


# =============================================================================
# VALIDATION LOGIC
# =============================================================================

def validate_meta(content: str, file_path: str) -> tuple[list[ValidationError], list[ValidationError]]:
    """
    Validate all meta tags in content.
    
    Args:
        content: File content
        file_path: Path to file
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    framework = detect_framework(file_path, content)
    lines = content.split("\n")
    head_line = find_head_line(lines)
    
    # === TITLE ===
    title, title_line = extract_tag_content(content, "title")
    
    if not title and not has_framework_title(content, framework):
        errors.append(MetaErrors.missing_title(file_path, head_line))
    elif title:
        if len(title) > TITLE_MAX:
            errors.append(MetaErrors.title_too_long(file_path, title, len(title), title_line))
        elif len(title) < TITLE_MIN:
            warnings.append(MetaErrors.title_too_short(file_path, title, len(title), title_line))
    
    # === META DESCRIPTION ===
    desc, desc_line = extract_meta_content(content, "description")
    
    if not desc and not has_framework_description(content, framework):
        errors.append(MetaErrors.missing_description(file_path, head_line))
    elif desc:
        if len(desc) > DESC_MAX:
            warnings.append(MetaErrors.description_too_long(file_path, len(desc), desc_line))
        elif len(desc) < DESC_MIN:
            warnings.append(MetaErrors.description_too_short(file_path, len(desc), desc_line))
    
    # === VIEWPORT ===
    viewport, _ = extract_meta_content(content, "viewport")
    if not viewport:
        errors.append(MetaErrors.missing_viewport(file_path, head_line))
    
    # === CANONICAL ===
    if not has_canonical(content, framework):
        errors.append(MetaErrors.missing_canonical(file_path, head_line))
    
    # === OPEN GRAPH ===
    og_title, _ = extract_meta_content(content, "og:title", "property")
    if not og_title and not has_framework_og(content, framework):
        errors.append(MetaErrors.missing_og_title(file_path, head_line))
    
    og_desc, _ = extract_meta_content(content, "og:description", "property")
    if not og_desc and not has_framework_og(content, framework):
        errors.append(MetaErrors.missing_og_description(file_path, head_line))
    
    og_image, og_image_line = extract_meta_content(content, "og:image", "property")
    if not og_image and not has_framework_og(content, framework):
        errors.append(MetaErrors.missing_og_image(file_path, head_line))
    elif og_image and not og_image.startswith("http"):
        errors.append(MetaErrors.og_image_not_absolute(file_path, og_image, og_image_line))
    
    og_url, _ = extract_meta_content(content, "og:url", "property")
    if not og_url and not has_framework_og(content, framework):
        errors.append(MetaErrors.missing_og_url(file_path, head_line))
    
    # === TWITTER CARD ===
    twitter_card, _ = extract_meta_content(content, "twitter:card")
    if not twitter_card and not has_framework_twitter(content, framework):
        errors.append(MetaErrors.missing_twitter_card(file_path, head_line))
    
    # === ROBOTS (warning only) ===
    robots, _ = extract_meta_content(content, "robots")
    if not robots:
        warnings.append(MetaErrors.missing_robots(file_path, head_line))

    # === NON-DESCRIPTIVE LINK TEXT ===
    bad_links = find_non_descriptive_links(content, lines)
    for link_text, link_line in bad_links:
        errors.append(MetaErrors.non_descriptive_link(file_path, link_text, link_line))

    return errors, warnings


# =============================================================================
# LINK TEXT VALIDATION
# =============================================================================

def find_non_descriptive_links(content: str, lines: list[str]) -> list[tuple[str, int]]:
    """
    Find links with non-descriptive text.

    Returns:
        List of (link_text, line_number) tuples
    """
    import re

    bad_links = []

    # Pattern to match <a ...>text</a> or {children} in JSX
    # Handles: <a href="...">Learn more</a>
    # Handles: <Link to="...">Click here</Link>
    link_pattern = re.compile(
        r'<(?:a|Link|NavLink)\s[^>]*>([^<]+)</(?:a|Link|NavLink)>',
        re.IGNORECASE
    )

    for i, line in enumerate(lines, 1):
        for match in link_pattern.finditer(line):
            link_text = match.group(1).strip()

            # Check if link text is non-descriptive
            if link_text.lower() in NON_DESCRIPTIVE_LINKS:
                bad_links.append((link_text, i))

    return bad_links


# =============================================================================
# FRAMEWORK-SPECIFIC CHECKS
# =============================================================================

def has_framework_title(content: str, framework: str) -> bool:
    """Check for framework-specific title patterns."""
    import re
    
    patterns = {
        "astro": [r'title\s*[=:]\s*[{"\'\`]', r'<title\s+set:html'],
        "nextjs": [r'metadata\s*[=:][^}]*title', r'generateMetadata'],
        "tanstack": [r'createRootRoute[^}]*head[^}]*title'],
        "nuxt": [r'useHead\([^)]*title', r'useSeoMeta\([^)]*title'],
        "sveltekit": [r'<svelte:head>[^<]*<title'],
        "vite": [r'Helmet[^>]*>[^<]*title', r'<title>'],
    }
    
    for pattern in patterns.get(framework, patterns["vite"]):
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            return True
    return False


def has_framework_description(content: str, framework: str) -> bool:
    """Check for framework-specific description patterns."""
    import re
    
    patterns = {
        "astro": [r'description\s*[=:]\s*[{"\'\`]'],
        "nextjs": [r'metadata\s*[=:][^}]*description', r'generateMetadata'],
        "tanstack": [r'createRootRoute[^}]*head[^}]*meta[^}]*description'],
        "nuxt": [r'useHead\([^)]*description', r'useSeoMeta\([^)]*description'],
    }
    
    for pattern in patterns.get(framework, []):
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            return True
    return False


def has_canonical(content: str, framework: str) -> bool:
    """Check for canonical URL."""
    import re
    
    # Direct HTML check
    if re.search(r'rel=["\']canonical["\']', content, re.IGNORECASE):
        return True
    
    # Framework-specific
    patterns = {
        "astro": [r'canonical\s*[=:]'],
        "nextjs": [r'alternates\s*[=:][^}]*canonical', r'metadataBase'],
        "nuxt": [r'useHead\([^)]*link[^)]*canonical'],
    }
    
    for pattern in patterns.get(framework, []):
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            return True
    return False


def has_framework_og(content: str, framework: str) -> bool:
    """Check for framework-specific Open Graph patterns."""
    import re
    
    patterns = {
        "astro": [r'og\s*[=:]\s*\{', r'openGraph\s*[=:]'],
        "nextjs": [r'openGraph\s*[=:]'],
        "nuxt": [r'useSeoMeta\([^)]*og'],
    }
    
    for pattern in patterns.get(framework, []):
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            return True
    return False


def has_framework_twitter(content: str, framework: str) -> bool:
    """Check for framework-specific Twitter Card patterns."""
    import re
    
    patterns = {
        "astro": [r'twitter\s*[=:]\s*\{'],
        "nextjs": [r'twitter\s*[=:]'],
        "nuxt": [r'useSeoMeta\([^)]*twitter'],
    }
    
    for pattern in patterns.get(framework, []):
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            return True
    return False


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
