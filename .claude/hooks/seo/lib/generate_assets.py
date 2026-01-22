#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///
"""
SEO Assets Generator

Generates all required SEO image assets from a source logo.
Creates favicons, apple-touch-icons, android icons, OG images, and manifests.

Usage:
    uv run generate_assets.py --logo public/logo.png --color "#3B82F6"
    uv run generate_assets.py --logo public/logo.svg --output public/
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


# Asset definitions: (filename, width, height)
FAVICONS = [
    ("favicon-16x16.png", 16, 16),
    ("favicon-32x32.png", 32, 32),
    ("favicon-96x96.png", 96, 96),
]

APPLE_ICONS = [
    ("apple-touch-icon.png", 180, 180),
    ("apple-touch-icon-120x120.png", 120, 120),
    ("apple-touch-icon-152x152.png", 152, 152),
]

ANDROID_ICONS = [
    ("android-chrome-192x192.png", 192, 192),
    ("android-chrome-512x512.png", 512, 512),
    ("maskable-icon-512x512.png", 512, 512),
]

MS_TILES = [
    ("mstile-70x70.png", 70, 70),
    ("mstile-150x150.png", 150, 150),
    ("mstile-310x310.png", 310, 310),
    ("mstile-310x150.png", 310, 150),
]

OG_IMAGES = [
    ("og-image.png", 1200, 630),
    ("twitter-image.png", 1200, 600),
]


def find_logo(project_dir: Path) -> Path | None:
    """Find source logo in project."""
    candidates = [
        "public/logo.svg",
        "public/logo.png",
        "public/brand.svg",
        "public/brand.png",
        "public/icon.svg",
        "public/icon.png",
        "src/assets/logo.svg",
        "src/assets/logo.png",
        "assets/logo.svg",
        "assets/logo.png",
    ]

    for candidate in candidates:
        path = project_dir / candidate
        if path.exists():
            return path

    return None


def generate_with_pillow(logo_path: Path, output_dir: Path, assets: list) -> list:
    """Generate assets using Pillow."""
    try:
        from PIL import Image
    except ImportError:
        return []

    generated = []
    img = Image.open(logo_path)

    # Convert to RGBA if needed
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    for filename, width, height in assets:
        output_path = output_dir / filename

        # Resize maintaining aspect ratio and center
        resized = img.copy()
        resized.thumbnail((width, height), Image.Resampling.LANCZOS)

        # Create canvas and paste centered
        canvas = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        x = (width - resized.width) // 2
        y = (height - resized.height) // 2
        canvas.paste(resized, (x, y), resized if resized.mode == "RGBA" else None)

        # Save
        canvas.save(output_path, "PNG")
        generated.append(filename)

    return generated


def generate_with_imagemagick(logo_path: Path, output_dir: Path, assets: list) -> list:
    """Generate assets using ImageMagick."""
    if not shutil.which("convert"):
        return []

    generated = []

    for filename, width, height in assets:
        output_path = output_dir / filename

        cmd = [
            "convert", str(logo_path),
            "-resize", f"{width}x{height}",
            "-gravity", "center",
            "-background", "white",
            "-extent", f"{width}x{height}",
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            generated.append(filename)

    return generated


def generate_favicon_ico(output_dir: Path) -> bool:
    """Generate favicon.ico from PNG sources."""
    # Check if we have the source PNGs
    sizes = ["favicon-16x16.png", "favicon-32x32.png"]
    sources = [output_dir / s for s in sizes if (output_dir / s).exists()]

    if not sources:
        return False

    # Try ImageMagick
    if shutil.which("convert"):
        cmd = ["convert"] + [str(s) for s in sources] + [str(output_dir / "favicon.ico")]
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0

    # Try Pillow
    try:
        from PIL import Image
        imgs = [Image.open(s) for s in sources]
        imgs[0].save(
            output_dir / "favicon.ico",
            format="ICO",
            sizes=[(16, 16), (32, 32)]
        )
        return True
    except Exception:
        return False


def create_manifest(output_dir: Path, name: str, color: str) -> None:
    """Create site.webmanifest."""
    manifest = {
        "name": name,
        "short_name": name,
        "description": f"{name} - Progressive Web App",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait-primary",
        "lang": "en",
        "theme_color": color,
        "background_color": "#ffffff",
        "icons": [
            {
                "src": "/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/android-chrome-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/maskable-icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable"
            }
        ]
    }

    (output_dir / "site.webmanifest").write_text(json.dumps(manifest, indent=2))


def create_browserconfig(output_dir: Path, color: str) -> None:
    """Create browserconfig.xml."""
    xml = f'''<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square70x70logo src="/mstile-70x70.png"/>
      <square150x150logo src="/mstile-150x150.png"/>
      <square310x310logo src="/mstile-310x310.png"/>
      <wide310x150logo src="/mstile-310x150.png"/>
      <TileColor>{color}</TileColor>
    </tile>
  </msapplication>
</browserconfig>'''

    (output_dir / "browserconfig.xml").write_text(xml)


def main():
    parser = argparse.ArgumentParser(description="Generate SEO assets")
    parser.add_argument("--logo", help="Path to source logo")
    parser.add_argument("--output", default="public", help="Output directory (must be public/ root, not a subdirectory)")
    parser.add_argument("--name", default="Site", help="Site name for manifest")
    parser.add_argument("--color", default="#3B82F6", help="Theme color (hex)")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    project_dir = Path.cwd()
    output_dir = Path(args.output)

    # CRITICAL: Assets MUST go in public/ root for browser discovery
    # Not in subdirectories like public/images/logo/
    output_resolved = output_dir.resolve()
    if output_resolved.name not in ("public", "static", "dist"):
        warning = (
            f"⚠️  WARNING: Output directory is '{output_dir}'\n"
            "   SEO assets should be in the root of public/, not a subdirectory!\n"
            "   Browsers expect favicon.ico, apple-touch-icon.png etc at /favicon.ico\n"
            "   Recommended: --output public\n"
        )
        if not args.json:
            print(warning)

    # Find logo
    if args.logo:
        logo_path = Path(args.logo)
    else:
        logo_path = find_logo(project_dir)

    if not logo_path or not logo_path.exists():
        result = {"error": "No source logo found", "searched": [
            "public/logo.svg", "public/logo.png", "src/assets/logo.*"
        ]}
        if args.json:
            print(json.dumps(result))
        else:
            print(f"✗ {result['error']}")
            print("  Searched:", ", ".join(result["searched"]))
        sys.exit(1)

    # Ensure output dir exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect all assets to generate
    all_assets = FAVICONS + APPLE_ICONS + ANDROID_ICONS + MS_TILES + OG_IMAGES
    generated = []

    # Try Pillow first, then ImageMagick
    generated = generate_with_pillow(logo_path, output_dir, all_assets)

    if not generated:
        generated = generate_with_imagemagick(logo_path, output_dir, all_assets)

    if not generated:
        result = {"error": "No image processor available. Install: pip install pillow OR apt install imagemagick"}
        if args.json:
            print(json.dumps(result))
        else:
            print(f"✗ {result['error']}")
        sys.exit(1)

    # Generate favicon.ico
    if generate_favicon_ico(output_dir):
        generated.append("favicon.ico")

    # Create config files
    create_manifest(output_dir, args.name, args.color)
    generated.append("site.webmanifest")

    create_browserconfig(output_dir, args.color)
    generated.append("browserconfig.xml")

    # Report
    result = {
        "success": True,
        "logo": str(logo_path),
        "output": str(output_dir),
        "generated": generated,
        "count": len(generated)
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"✓ Generated {len(generated)} assets from {logo_path}")
        print(f"  Output: {output_dir}")
        for f in generated:
            print(f"    - {f}")


if __name__ == "__main__":
    main()
