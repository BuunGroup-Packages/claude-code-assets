#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Stop Hook: SEO Assets Validation

Validates all required SEO image assets exist with correct dimensions.
Runs after seo-assets skill to verify complete asset generation.
"""
import json
import os
import struct
import sys
from pathlib import Path

# Add lib to path
hook_dir = Path(__file__).parent
if "CLAUDE_PROJECT_DIR" in os.environ:
    hook_dir = Path(os.environ["CLAUDE_PROJECT_DIR"]) / ".claude" / "hooks" / "seo"
sys.path.insert(0, str(hook_dir))


# =============================================================================
# CONFIGURATION
# =============================================================================

REQUIRED_ASSETS = {
    # Favicons
    "favicon.ico": None,  # Multi-size, skip dimension check
    "favicon-16x16.png": (16, 16),
    "favicon-32x32.png": (32, 32),

    # Apple
    "apple-touch-icon.png": (180, 180),

    # Android/PWA
    "android-chrome-192x192.png": (192, 192),
    "android-chrome-512x512.png": (512, 512),

    # OG
    "og-image.png": (1200, 630),
}

RECOMMENDED_ASSETS = {
    # Additional favicons
    "favicon.svg": None,
    "favicon-96x96.png": (96, 96),

    # Additional Apple
    "apple-touch-icon-152x152.png": (152, 152),
    "apple-touch-icon-120x120.png": (120, 120),

    # Maskable
    "maskable-icon-512x512.png": (512, 512),

    # MS Tiles
    "mstile-70x70.png": (70, 70),
    "mstile-150x150.png": (150, 150),
    "mstile-310x310.png": (310, 310),
    "mstile-310x150.png": (310, 150),

    # Twitter
    "twitter-image.png": (1200, 600),

    # Config files
    "site.webmanifest": None,
    "browserconfig.xml": None,
}


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    """Main hook entry point."""
    data = json.load(sys.stdin)

    # Find public directory
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    public_dir = find_public_dir(project_dir)

    if not public_dir:
        print(json.dumps({
            "continue": True,
            "message": "⚠️ No public directory found. Assets should be in public/"
        }))
        return

    errors = []
    warnings = []
    found = []

    # Check required assets
    for filename, expected_dims in REQUIRED_ASSETS.items():
        filepath = public_dir / filename

        if not filepath.exists():
            errors.append({
                "code": get_error_code(filename),
                "file": filename,
                "issue": f"Missing required asset: {filename}",
                "fix": f"Generate {filename} with seo-assets skill"
            })
        else:
            found.append(filename)
            # Check dimensions for PNG files
            if expected_dims and filename.endswith(".png"):
                actual_dims = get_png_dimensions(filepath)
                if actual_dims and actual_dims != expected_dims:
                    warnings.append({
                        "code": "ASSET008",
                        "file": filename,
                        "issue": f"Wrong dimensions: {actual_dims[0]}x{actual_dims[1]}",
                        "expected": f"{expected_dims[0]}x{expected_dims[1]}"
                    })

    # Check recommended assets (warnings only)
    for filename, expected_dims in RECOMMENDED_ASSETS.items():
        filepath = public_dir / filename

        if not filepath.exists():
            warnings.append({
                "code": "ASSET007",
                "file": filename,
                "issue": f"Missing recommended asset: {filename}",
                "fix": f"Consider adding {filename} for complete coverage"
            })
        else:
            found.append(filename)

    # Check manifest JSON syntax and required fields
    manifest_path = public_dir / "site.webmanifest"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())

            # Check required fields
            required_fields = ["name", "short_name", "icons", "theme_color", "background_color", "display"]
            for field in required_fields:
                if field not in manifest:
                    errors.append({
                        "code": "ASSET006",
                        "file": "site.webmanifest",
                        "issue": f"Missing required field: {field}",
                        "fix": f"Add '{field}' to site.webmanifest"
                    })

            # Check recommended fields (warnings)
            recommended_fields = ["description", "start_url", "scope", "lang", "orientation"]
            for field in recommended_fields:
                if field not in manifest:
                    warnings.append({
                        "code": "ASSET010",
                        "file": "site.webmanifest",
                        "issue": f"Missing recommended field: {field}",
                        "fix": f"Consider adding '{field}' to site.webmanifest"
                    })

            # Check icons have purpose
            if "icons" in manifest:
                has_any = any(icon.get("purpose") == "any" for icon in manifest["icons"])
                has_maskable = any(icon.get("purpose") == "maskable" for icon in manifest["icons"])

                if not has_any:
                    warnings.append({
                        "code": "ASSET011",
                        "file": "site.webmanifest",
                        "issue": "No icon with purpose 'any'",
                        "fix": "Add 'purpose': 'any' to at least one icon"
                    })

                if not has_maskable:
                    warnings.append({
                        "code": "ASSET007",
                        "file": "site.webmanifest",
                        "issue": "No icon with purpose 'maskable'",
                        "fix": "Add a maskable icon for Android adaptive icons"
                    })

        except json.JSONDecodeError as e:
            errors.append({
                "code": "ASSET006",
                "file": "site.webmanifest",
                "issue": f"Invalid JSON: {e}",
                "fix": "Fix JSON syntax in site.webmanifest"
            })

    # Build response
    if errors:
        message = format_errors(errors, warnings, found, public_dir)
        print(json.dumps({"continue": True, "message": message}))
    elif warnings:
        message = format_warnings(warnings, found, public_dir)
        print(json.dumps({"continue": True, "message": message}))
    else:
        print(json.dumps({
            "continue": True,
            "message": f"✓ SEO assets validated ({len(found)} files in {public_dir}/)"
        }))


# =============================================================================
# HELPERS
# =============================================================================

def find_public_dir(project_dir: str) -> Path | None:
    """Find the public directory."""
    candidates = ["public", "static", "dist"]

    for name in candidates:
        path = Path(project_dir) / name
        if path.is_dir():
            return path

    return None


def get_error_code(filename: str) -> str:
    """Get error code based on asset type."""
    if "favicon" in filename:
        return "ASSET002"
    elif "apple" in filename:
        return "ASSET003"
    elif "android" in filename:
        return "ASSET004"
    elif "og-image" in filename:
        return "ASSET005"
    else:
        return "ASSET002"


def get_png_dimensions(filepath: Path) -> tuple[int, int] | None:
    """Get PNG image dimensions without external dependencies."""
    try:
        with open(filepath, "rb") as f:
            # PNG signature + IHDR chunk
            data = f.read(24)
            if data[:8] != b'\x89PNG\r\n\x1a\n':
                return None
            # Width and height are at bytes 16-24
            width = struct.unpack(">I", data[16:20])[0]
            height = struct.unpack(">I", data[20:24])[0]
            return (width, height)
    except Exception:
        return None


def format_errors(errors: list, warnings: list, found: list, public_dir: Path) -> str:
    """Format error message."""
    lines = [
        "✗ SEO ASSETS VALIDATION FAILED",
        f"Checking: {public_dir}/",
        f"Found: {len(found)} | Missing: {len(errors)} | Warnings: {len(warnings)}",
        "",
        "MISSING REQUIRED ASSETS:",
    ]

    for err in errors:
        lines.append(f"  [{err['code']}] {err['file']}")
        lines.append(f"      Fix: {err['fix']}")

    if warnings:
        lines.append("")
        lines.append("WARNINGS:")
        for warn in warnings[:5]:  # Limit warnings shown
            lines.append(f"  [{warn['code']}] {warn['file']}: {warn['issue']}")
        if len(warnings) > 5:
            lines.append(f"  ... and {len(warnings) - 5} more")

    return "\n".join(lines)


def format_warnings(warnings: list, found: list, public_dir: Path) -> str:
    """Format warnings-only message."""
    lines = [
        f"✓ Required SEO assets present ({len(found)} files in {public_dir}/)",
        "",
        f"RECOMMENDATIONS ({len(warnings)}):",
    ]

    for warn in warnings[:5]:
        lines.append(f"  - {warn['file']}")

    if len(warnings) > 5:
        lines.append(f"  ... and {len(warnings) - 5} more")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
