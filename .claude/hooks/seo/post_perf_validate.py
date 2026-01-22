#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
PostToolUse Hook: Performance/Core Web Vitals Validation

Validates images, fonts, and other performance-related elements.

Trigger: Edit|Write|MultiEdit on layout/component files
Output: Success message or ordered list of fixes

Run with: uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/post_perf_validate.py
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

from lib.response import success, failure, skip, PerfErrors, ValidationError
from lib.validators import is_meta_file, find_line_number


# =============================================================================
# CONFIGURATION
# =============================================================================

# File patterns that should be checked for performance
PERF_FILE_PATTERNS = [
    "layout", "page", "component", "template", "view",
    "head", "base", "app", "root", "index"
]

# Image extensions
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".avif"]

# Modern image formats (preferred)
MODERN_FORMATS = [".webp", ".avif"]


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
    
    # Check if file should be validated for performance
    if not should_validate_perf(file_path):
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
    errors, warnings = validate_performance(content, file_path)
    
    if errors:
        print(failure(file_path, "PERF", errors, warnings))
    elif warnings:
        print(failure(file_path, "PERF", [], warnings))
    else:
        print(success(file_path, "PERF"))


# =============================================================================
# FILE DETECTION
# =============================================================================

def should_validate_perf(file_path: str) -> bool:
    """Check if file should be validated for performance."""
    path_lower = file_path.lower()
    
    # Check file patterns
    if any(pattern in path_lower for pattern in PERF_FILE_PATTERNS):
        return True
    
    # Check for HTML/template files
    if any(path_lower.endswith(ext) for ext in [".html", ".astro", ".tsx", ".jsx", ".vue", ".svelte"]):
        return True
    
    # Check for CSS files (font-display)
    if path_lower.endswith(".css"):
        return True
    
    return False


# =============================================================================
# VALIDATION LOGIC
# =============================================================================

def validate_performance(content: str, file_path: str) -> tuple[list[ValidationError], list[ValidationError]]:
    """
    Validate performance-related elements.
    
    Args:
        content: File content
        file_path: Path to file
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    lines = content.split("\n")
    
    # === IMAGE VALIDATION ===
    img_errors, img_warnings = validate_images(content, file_path, lines)
    errors.extend(img_errors)
    warnings.extend(img_warnings)
    
    # === FONT VALIDATION (CSS files) ===
    if file_path.lower().endswith(".css"):
        font_errors, font_warnings = validate_fonts(content, file_path, lines)
        errors.extend(font_errors)
        warnings.extend(font_warnings)
    
    # === PRELOAD VALIDATION ===
    preload_errors, preload_warnings = validate_preloads(content, file_path, lines)
    errors.extend(preload_errors)
    warnings.extend(preload_warnings)
    
    # === THEME COLOR (optional) ===
    if is_meta_file(file_path):
        if 'name="theme-color"' not in content and "name='theme-color'" not in content:
            warnings.append(PerfErrors.missing_meta_theme_color(file_path))
    
    return errors, warnings


# =============================================================================
# IMAGE VALIDATION
# =============================================================================

def validate_images(content: str, file_path: str, lines: list[str]) -> tuple[list[ValidationError], list[ValidationError]]:
    """Validate image elements for performance."""
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    # Find all img tags
    img_pattern = r'<img\s+([^>]*)/?>'
    
    for match in re.finditer(img_pattern, content, re.IGNORECASE | re.DOTALL):
        attrs = match.group(1)
        line_num = content[:match.start()].count("\n") + 1
        
        # Extract src
        src_match = re.search(r'src=["\']([^"\']*)["\']', attrs)
        src = src_match.group(1) if src_match else "unknown"
        
        # Check for width/height
        has_width = re.search(r'\bwidth\s*=', attrs, re.IGNORECASE)
        has_height = re.search(r'\bheight\s*=', attrs, re.IGNORECASE)
        
        if not has_width or not has_height:
            errors.append(PerfErrors.image_missing_dimensions(file_path, src, line_num))
        
        # Check for alt
        has_alt = re.search(r'\balt\s*=', attrs, re.IGNORECASE)
        if not has_alt:
            errors.append(PerfErrors.image_missing_alt(file_path, src, line_num))
        
        # Check for loading="lazy" (warning for non-hero images)
        has_loading = re.search(r'\bloading\s*=', attrs, re.IGNORECASE)
        # Skip if it looks like a hero/above-fold image
        is_hero = any(x in attrs.lower() for x in ["hero", "banner", "logo", "above"])
        
        if not has_loading and not is_hero:
            warnings.append(PerfErrors.image_not_lazy(file_path, src, line_num))
        
        # Check for modern format (warning)
        if src and not any(src.lower().endswith(fmt) for fmt in MODERN_FORMATS):
            if any(src.lower().endswith(fmt) for fmt in [".jpg", ".jpeg", ".png"]):
                warnings.append(PerfErrors.image_not_optimized(file_path, src, line_num))
    
    # Also check for Image components (React/Next.js/Astro)
    component_pattern = r'<(Image|Img|Picture)\s+([^>]*)/?>'
    
    for match in re.finditer(component_pattern, content, re.IGNORECASE | re.DOTALL):
        component = match.group(1)
        attrs = match.group(2)
        line_num = content[:match.start()].count("\n") + 1
        
        # Extract src
        src_match = re.search(r'src=\{?["\']?([^"\'}\s]*)["\']?\}?', attrs)
        src = src_match.group(1) if src_match else "unknown"
        
        # Check for alt (still required for components)
        has_alt = re.search(r'\balt\s*=', attrs, re.IGNORECASE)
        if not has_alt:
            errors.append(PerfErrors.image_missing_alt(file_path, f"{component}: {src}", line_num))
    
    return errors, warnings


# =============================================================================
# FONT VALIDATION
# =============================================================================

def validate_fonts(content: str, file_path: str, lines: list[str]) -> tuple[list[ValidationError], list[ValidationError]]:
    """Validate @font-face rules for performance."""
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    # Find all @font-face rules
    fontface_pattern = r'@font-face\s*\{([^}]*)\}'
    
    for match in re.finditer(fontface_pattern, content, re.IGNORECASE | re.DOTALL):
        rule_content = match.group(1)
        line_num = content[:match.start()].count("\n") + 1
        
        # Check for font-display
        if "font-display" not in rule_content.lower():
            errors.append(PerfErrors.missing_font_display(file_path, line_num))
    
    return errors, warnings


# =============================================================================
# PRELOAD VALIDATION
# =============================================================================

def validate_preloads(content: str, file_path: str, lines: list[str]) -> tuple[list[ValidationError], list[ValidationError]]:
    """Validate critical resource preloading."""
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    # Check if this is a head/layout file
    if not is_meta_file(file_path):
        return errors, warnings
    
    # Look for font URLs that should be preloaded
    font_pattern = r'url\(["\']?([^"\')\s]+\.(woff2?|ttf|otf))["\']?\)'
    
    for match in re.finditer(font_pattern, content, re.IGNORECASE):
        font_url = match.group(1)
        line_num = content[:match.start()].count("\n") + 1
        
        # Check if this font is preloaded
        if f'href="{font_url}"' not in content and f"href='{font_url}'" not in content:
            # Not preloaded via link tag
            if 'rel="preload"' not in content or font_url not in content:
                warnings.append(PerfErrors.font_not_preloaded(file_path, font_url, line_num))
    
    # Check for render-blocking scripts (without async/defer)
    script_pattern = r'<script\s+([^>]*)src=["\']([^"\']*)["\']([^>]*)>'
    
    for match in re.finditer(script_pattern, content, re.IGNORECASE):
        before_src = match.group(1)
        src = match.group(2)
        after_src = match.group(3)
        attrs = before_src + after_src
        line_num = content[:match.start()].count("\n") + 1
        
        # Check for async or defer
        has_async = re.search(r'\basync\b', attrs, re.IGNORECASE)
        has_defer = re.search(r'\bdefer\b', attrs, re.IGNORECASE)
        has_type_module = re.search(r'type=["\']module["\']', attrs, re.IGNORECASE)
        
        if not has_async and not has_defer and not has_type_module:
            # This is a render-blocking script
            warnings.append(PerfErrors.render_blocking_resource(file_path, src, line_num))
    
    return errors, warnings


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
