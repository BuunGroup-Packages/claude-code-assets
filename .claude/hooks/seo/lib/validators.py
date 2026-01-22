#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Shared validation utilities for SEO hooks.

Provides framework detection, line finding, and pattern matching.
"""
import re
from pathlib import Path


# =============================================================================
# FRAMEWORK DETECTION
# =============================================================================

FRAMEWORK_FILE_PATTERNS = {
    "astro": [".astro"],
    "nextjs": ["_app.tsx", "_app.jsx", "layout.tsx", "layout.jsx", "page.tsx", "page.jsx"],
    "tanstack": ["__root.tsx", "root.tsx", "routeTree.gen.ts"],
    "nuxt": [".vue", "nuxt.config"],
    "sveltekit": [".svelte", "svelte.config"],
    "vite": [".tsx", ".jsx"],  # Default for React
}

FRAMEWORK_CONTENT_PATTERNS = {
    "astro": [r"---[\s\S]*?---", r"Astro\.props", r"<slot\s*/?>"],
    "nextjs": [r"next/head", r"next/image", r"getServerSideProps", r"getStaticProps", r"metadata\s*="],
    "tanstack": [r"createFileRoute", r"createRootRoute", r"@tanstack/react-router"],
    "nuxt": [r"useHead\(", r"useSeoMeta\(", r"defineNuxtConfig"],
    "sveltekit": [r"<svelte:head>", r"\$app/"],
    "vite": [r"react-helmet", r"@vitejs/plugin-react"],
}


def detect_framework(file_path: str, content: str | None = None) -> str:
    """
    Detect framework from file path and optionally content.
    
    Args:
        file_path: Path to the file
        content: Optional file content for deeper detection
        
    Returns:
        Framework name: astro, nextjs, tanstack, nuxt, sveltekit, vite
    """
    path_lower = file_path.lower()
    
    # Check file extension/name patterns
    for framework, patterns in FRAMEWORK_FILE_PATTERNS.items():
        for pattern in patterns:
            if pattern in path_lower:
                return framework
    
    # Check content patterns if provided
    if content:
        for framework, patterns in FRAMEWORK_CONTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content):
                    return framework
    
    # Default to vite/react
    return "vite"


def detect_framework_from_package_json(project_root: str = ".") -> str | None:
    """
    Detect framework from package.json dependencies.
    
    Args:
        project_root: Path to project root
        
    Returns:
        Framework name or None if not detected
    """
    import json
    
    pkg_path = Path(project_root) / "package.json"
    if not pkg_path.exists():
        return None
    
    try:
        pkg = json.loads(pkg_path.read_text())
    except (json.JSONDecodeError, IOError):
        return None
    
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    
    if "astro" in deps:
        return "astro"
    if "next" in deps:
        return "nextjs"
    if "@tanstack/react-router" in deps or "@tanstack/start" in deps:
        return "tanstack"
    if "nuxt" in deps:
        return "nuxt"
    if "@sveltejs/kit" in deps:
        return "sveltekit"
    if "vite" in deps:
        return "vite"
    
    return None


# =============================================================================
# FILE TYPE DETECTION
# =============================================================================

META_FILE_INDICATORS = [
    "layout", "head", "seo", "meta", "base", "_app", "_document", 
    "root", "basehead", "defaulthead"
]

SCHEMA_FILE_INDICATORS = [
    "schema", "jsonld", "json-ld", "structured", "ld+json"
]

AI_FILE_INDICATORS = [
    "llms", "robots", "sitemap"
]


def is_meta_file(file_path: str) -> bool:
    """Check if file likely contains meta tags."""
    path_lower = file_path.lower()
    return any(ind in path_lower for ind in META_FILE_INDICATORS)


def is_schema_file(file_path: str) -> bool:
    """Check if file likely contains JSON-LD schema."""
    path_lower = file_path.lower()
    return any(ind in path_lower for ind in SCHEMA_FILE_INDICATORS) or file_path.endswith(".json")


def is_ai_file(file_path: str) -> bool:
    """Check if file is AI SEO related (llms.txt, robots.txt)."""
    path_lower = file_path.lower()
    return any(ind in path_lower for ind in AI_FILE_INDICATORS)


def is_seo_file(file_path: str) -> bool:
    """Check if file is any SEO-related file."""
    return is_meta_file(file_path) or is_schema_file(file_path) or is_ai_file(file_path)


# =============================================================================
# LINE NUMBER UTILITIES
# =============================================================================

def find_line_number(lines: list[str], search_str: str) -> int | None:
    """
    Find line number containing search string.
    
    Args:
        lines: List of file lines
        search_str: String to search for
        
    Returns:
        Line number (1-indexed) or None
    """
    search_lower = search_str.lower()[:50]
    for i, line in enumerate(lines, 1):
        if search_lower in line.lower():
            return i
    return None


def find_element_line(lines: list[str], element: str) -> int | None:
    """
    Find line number of HTML element.
    
    Args:
        lines: List of file lines
        element: Element to find (e.g., "<head", "<title")
        
    Returns:
        Line number (1-indexed) or None
    """
    element_lower = element.lower()
    for i, line in enumerate(lines, 1):
        if element_lower in line.lower():
            return i
    return None


def find_head_line(lines: list[str]) -> int | None:
    """Find line number of <head> tag."""
    return find_element_line(lines, "<head")


def find_body_line(lines: list[str]) -> int | None:
    """Find line number of <body> tag."""
    return find_element_line(lines, "<body")


# =============================================================================
# CONTENT EXTRACTION
# =============================================================================

def extract_tag_content(content: str, tag: str) -> tuple[str | None, int | None]:
    """
    Extract content and line number of an HTML tag.
    
    Args:
        content: Full file content
        tag: Tag name (e.g., "title")
        
    Returns:
        Tuple of (content, line_number) or (None, None)
    """
    pattern = rf'<{tag}[^>]*>([^<]*)</{tag}>'
    match = re.search(pattern, content, re.IGNORECASE)
    
    if not match:
        return None, None
    
    tag_content = match.group(1).strip()
    
    # Find line number
    lines = content[:match.start()].split("\n")
    line_num = len(lines)
    
    return tag_content, line_num


def extract_meta_content(content: str, name: str, attr: str = "name") -> tuple[str | None, int | None]:
    """
    Extract content attribute from meta tag.
    
    Args:
        content: Full file content
        name: Meta name/property value
        attr: Attribute name ("name" or "property")
        
    Returns:
        Tuple of (content, line_number) or (None, None)
    """
    # Try both attribute orders
    patterns = [
        rf'<meta[^>]*{attr}=["\']?{name}["\']?[^>]*content=["\']([^"\']*)["\']',
        rf'<meta[^>]*content=["\']([^"\']*)["\'][^>]*{attr}=["\']?{name}["\']?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            meta_content = match.group(1).strip()
            lines = content[:match.start()].split("\n")
            return meta_content, len(lines)
    
    return None, None


def extract_jsonld(content: str) -> list[tuple[dict, int]]:
    """
    Extract all JSON-LD scripts from content.
    
    Args:
        content: Full file content
        
    Returns:
        List of (parsed_json, line_number) tuples
    """
    import json
    
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
    
    results = []
    for match in matches:
        json_str = match.group(1).strip()
        lines = content[:match.start()].split("\n")
        line_num = len(lines)
        
        try:
            parsed = json.loads(json_str)
            results.append((parsed, line_num))
        except json.JSONDecodeError:
            # Return raw string for error reporting
            results.append(({"_raw": json_str, "_error": True}, line_num))
    
    return results


# =============================================================================
# URL VALIDATION
# =============================================================================

def is_absolute_url(url: str) -> bool:
    """Check if URL is absolute (starts with http:// or https://)."""
    return url.startswith("http://") or url.startswith("https://")


def is_valid_url(url: str) -> bool:
    """Basic URL validation."""
    if not url:
        return False
    
    # Must be absolute for SEO
    if not is_absolute_url(url):
        return False
    
    # Basic format check
    pattern = r'^https?://[a-zA-Z0-9][-a-zA-Z0-9]*(\.[a-zA-Z0-9][-a-zA-Z0-9]*)+(/.*)?$'
    return bool(re.match(pattern, url))
