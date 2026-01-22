#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Standardized error response format for all SEO validation hooks.
Ensures consistent, actionable feedback to guide the agent.

Usage:
    from lib.response import success, failure, MetaErrors
"""
from dataclasses import dataclass
from typing import Literal
import json


# =============================================================================
# CORE DATA STRUCTURES
# =============================================================================

@dataclass
class ValidationError:
    """
    Single validation error with complete fix instructions.
    
    Attributes:
        code: Unique error code (e.g., META001, SCHEMA002)
        severity: "error" (must fix) or "warning" (should fix)
        file: Exact file path
        line: Line number if applicable
        element: What element failed (e.g., "<title>")
        rule: Rule that was violated
        current: Current value (if any)
        expected: Expected value/format
        fix: Exact fix instruction for the agent
    """
    code: str
    severity: Literal["error", "warning"]
    file: str
    line: int | None
    element: str
    rule: str
    current: str | None
    expected: str
    fix: str
    
    def to_instruction(self) -> str:
        """Convert to agent instruction format."""
        parts = [f"[{self.code}] {self.element}"]
        
        if self.line:
            parts.append(f"at line {self.line}")
        
        parts.append(f"in {self.file}")
        
        instruction = " ".join(parts)
        instruction += f"\n  Rule: {self.rule}"
        
        if self.current:
            instruction += f"\n  Current: {self.current}"
        
        instruction += f"\n  Expected: {self.expected}"
        instruction += f"\n  Fix: {self.fix}"
        
        return instruction


@dataclass  
class ValidationResult:
    """
    Complete validation result with all errors and fix instructions.
    
    Attributes:
        success: True if all validations passed
        file: File that was validated
        validator: Which validator ran (meta, schema, ai, perf)
        errors: List of errors (must fix)
        warnings: List of warnings (should fix)
    """
    success: bool
    file: str
    validator: str
    errors: list[ValidationError]
    warnings: list[ValidationError]
    
    def to_hook_response(self) -> dict:
        """Convert to Claude hook JSON response."""
        if self.success:
            return {
                "decision": "continue",
                "hookSpecificOutput": {
                    "feedback": f"✓ {self.validator.upper()} validation passed for {self.file}"
                }
            }
        
        feedback = self._build_feedback()
        
        return {
            "hookSpecificOutput": {
                "feedback": feedback
            }
        }
    
    def _build_feedback(self) -> str:
        """Build complete, actionable feedback for agent."""
        lines = [
            f"✗ {self.validator.upper()} VALIDATION FAILED",
            f"File: {self.file}",
            f"Errors: {len(self.errors)} | Warnings: {len(self.warnings)}",
            "",
            "=" * 60,
            "FIX INSTRUCTIONS (execute in order):",
            "=" * 60,
        ]
        
        for i, error in enumerate(self.errors, 1):
            lines.append(f"\n{i}. {error.to_instruction()}")
        
        if self.warnings:
            lines.append("\n" + "-" * 60)
            lines.append("WARNINGS (recommended fixes):")
            lines.append("-" * 60)
            for i, warning in enumerate(self.warnings, 1):
                lines.append(f"\n{i}. {warning.to_instruction()}")
        
        lines.append("\n" + "=" * 60)
        lines.append("After fixing, save the file. Validation will re-run automatically.")
        
        return "\n".join(lines)


# =============================================================================
# RESPONSE HELPERS
# =============================================================================

def success(file: str, validator: str) -> str:
    """Return success response JSON."""
    result = ValidationResult(
        success=True,
        file=file,
        validator=validator,
        errors=[],
        warnings=[]
    )
    return json.dumps(result.to_hook_response())


def failure(
    file: str, 
    validator: str, 
    errors: list[ValidationError], 
    warnings: list[ValidationError] | None = None
) -> str:
    """Return failure response JSON with fix instructions."""
    result = ValidationResult(
        success=False,
        file=file,
        validator=validator,
        errors=errors,
        warnings=warnings or []
    )
    return json.dumps(result.to_hook_response())


def skip() -> str:
    """Return skip response (file not relevant)."""
    return json.dumps({"decision": "continue"})


def block(reason: str) -> str:
    """Return block response (prevent tool execution)."""
    return json.dumps({
        "hookSpecificOutput": {
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    })


# =============================================================================
# META TAG ERRORS
# =============================================================================

class MetaErrors:
    """Meta tag validation error templates."""
    
    @staticmethod
    def missing_title(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META001",
            severity="error",
            file=file,
            line=line,
            element="<title>",
            rule="Page must have exactly one <title> tag",
            current=None,
            expected="<title>Page Title | Site Name</title>",
            fix="Add <title> tag inside <head>. Format: 'Page Title | Site Name'. Max 60 characters."
        )
    
    @staticmethod
    def title_too_long(file: str, current: str, length: int, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META002",
            severity="error",
            file=file,
            line=line,
            element="<title>",
            rule="Title must be ≤60 characters",
            current=f"'{current[:50]}...' ({length} chars)",
            expected="≤60 characters",
            fix=f"Shorten title to 60 chars. Remove {length - 60} characters."
        )
    
    @staticmethod
    def title_too_short(file: str, current: str, length: int, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META003",
            severity="warning",
            file=file,
            line=line,
            element="<title>",
            rule="Title should be ≥10 characters for SEO",
            current=f"'{current}' ({length} chars)",
            expected="10-60 characters",
            fix=f"Expand title to at least 10 characters with relevant keywords."
        )
    
    @staticmethod
    def missing_description(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META004",
            severity="error",
            file=file,
            line=line,
            element='<meta name="description">',
            rule="Page must have meta description",
            current=None,
            expected='<meta name="description" content="...">',
            fix='Add <meta name="description" content="Your description here"> inside <head>. 150-160 characters recommended.'
        )
    
    @staticmethod
    def description_too_long(file: str, length: int, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META005",
            severity="warning",
            file=file,
            line=line,
            element='<meta name="description">',
            rule="Description should be ≤160 characters",
            current=f"({length} chars)",
            expected="≤160 characters",
            fix=f"Shorten description to 160 chars. Remove {length - 160} characters."
        )
    
    @staticmethod
    def description_too_short(file: str, length: int, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META006",
            severity="warning",
            file=file,
            line=line,
            element='<meta name="description">',
            rule="Description should be ≥120 characters",
            current=f"({length} chars)",
            expected="120-160 characters",
            fix=f"Expand description to 120+ chars. Add {120 - length} more characters."
        )
    
    @staticmethod
    def missing_canonical(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META007",
            severity="error",
            file=file,
            line=line,
            element='<link rel="canonical">',
            rule="Page must have canonical URL",
            current=None,
            expected='<link rel="canonical" href="https://...">',
            fix='Add <link rel="canonical" href="{FULL_PAGE_URL}"> inside <head>. Use absolute URL.'
        )
    
    @staticmethod
    def missing_viewport(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META008",
            severity="error",
            file=file,
            line=line,
            element='<meta name="viewport">',
            rule="Page must have viewport meta for mobile",
            current=None,
            expected='<meta name="viewport" content="width=device-width, initial-scale=1">',
            fix='Add <meta name="viewport" content="width=device-width, initial-scale=1"> inside <head>.'
        )
    
    @staticmethod
    def missing_og_title(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META009",
            severity="error",
            file=file,
            line=line,
            element='<meta property="og:title">',
            rule="Page must have Open Graph title",
            current=None,
            expected='<meta property="og:title" content="...">',
            fix='Add <meta property="og:title" content="{PAGE_TITLE}"> inside <head>.'
        )
    
    @staticmethod
    def missing_og_description(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META010",
            severity="error",
            file=file,
            line=line,
            element='<meta property="og:description">',
            rule="Page must have Open Graph description",
            current=None,
            expected='<meta property="og:description" content="...">',
            fix='Add <meta property="og:description" content="{DESCRIPTION}"> inside <head>.'
        )
    
    @staticmethod
    def missing_og_image(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META011",
            severity="error",
            file=file,
            line=line,
            element='<meta property="og:image">',
            rule="Page must have Open Graph image",
            current=None,
            expected='<meta property="og:image" content="https://...">',
            fix='Add <meta property="og:image" content="{ABSOLUTE_IMAGE_URL}"> inside <head>. Image: 1200x630px.'
        )
    
    @staticmethod
    def og_image_not_absolute(file: str, current: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META012",
            severity="error",
            file=file,
            line=line,
            element='<meta property="og:image">',
            rule="og:image must be absolute URL",
            current=current,
            expected="https://yourdomain.com/path/to/image.png",
            fix=f"Change og:image from relative '{current}' to absolute URL. Prepend your domain."
        )
    
    @staticmethod
    def missing_og_url(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META013",
            severity="error",
            file=file,
            line=line,
            element='<meta property="og:url">',
            rule="Page must have Open Graph URL",
            current=None,
            expected='<meta property="og:url" content="https://...">',
            fix='Add <meta property="og:url" content="{CANONICAL_URL}"> inside <head>.'
        )
    
    @staticmethod
    def missing_twitter_card(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META014",
            severity="error",
            file=file,
            line=line,
            element='<meta name="twitter:card">',
            rule="Page must have Twitter Card type",
            current=None,
            expected='<meta name="twitter:card" content="summary_large_image">',
            fix='Add <meta name="twitter:card" content="summary_large_image"> inside <head>.'
        )
    
    @staticmethod
    def missing_robots(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="META015",
            severity="warning",
            file=file,
            line=line,
            element='<meta name="robots">',
            rule="Page should have robots directive",
            current=None,
            expected='<meta name="robots" content="index, follow">',
            fix='Add <meta name="robots" content="index, follow"> inside <head>.'
        )


# =============================================================================
# SCHEMA ERRORS
# =============================================================================

class SchemaErrors:
    """JSON-LD schema validation error templates."""
    
    @staticmethod
    def invalid_json(file: str, error_msg: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="SCHEMA001",
            severity="error",
            file=file,
            line=line,
            element='<script type="application/ld+json">',
            rule="JSON-LD must be valid JSON",
            current=f"Parse error: {error_msg}",
            expected="Valid JSON object",
            fix=f"Fix JSON syntax error: {error_msg}. Check for missing commas, quotes, or brackets."
        )
    
    @staticmethod
    def missing_context(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="SCHEMA002",
            severity="error",
            file=file,
            line=line,
            element="@context",
            rule="JSON-LD must have @context",
            current=None,
            expected='"@context": "https://schema.org"',
            fix='Add "@context": "https://schema.org" as first property in JSON-LD object.'
        )
    
    @staticmethod
    def invalid_context(file: str, current: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="SCHEMA003",
            severity="error",
            file=file,
            line=line,
            element="@context",
            rule="@context must reference schema.org",
            current=current,
            expected='"https://schema.org"',
            fix=f"Change @context from '{current}' to 'https://schema.org'."
        )
    
    @staticmethod
    def missing_type(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="SCHEMA004",
            severity="error",
            file=file,
            line=line,
            element="@type",
            rule="JSON-LD must have @type",
            current=None,
            expected='"@type": "Organization|Article|Product|..."',
            fix='Add "@type": "YourSchemaType" to specify the schema type.'
        )
    
    @staticmethod
    def missing_required(file: str, schema_type: str, prop: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="SCHEMA005",
            severity="error",
            file=file,
            line=line,
            element=f"@type={schema_type}",
            rule=f"{schema_type} requires '{prop}' property",
            current=f"Missing: {prop}",
            expected=f'"{prop}": "..."',
            fix=f'Add "{prop}" property to {schema_type} schema. See schema.org/{schema_type} for format.'
        )
    
    @staticmethod
    def invalid_url(file: str, prop: str, current: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="SCHEMA006",
            severity="error",
            file=file,
            line=line,
            element=prop,
            rule=f"{prop} must be a valid absolute URL",
            current=current,
            expected="https://yourdomain.com/...",
            fix=f"Change '{prop}' from '{current}' to absolute URL starting with https://."
        )
    
    @staticmethod
    def missing_script_tag(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="SCHEMA007",
            severity="error",
            file=file,
            line=line,
            element='<script type="application/ld+json">',
            rule="Page should have JSON-LD structured data",
            current=None,
            expected='<script type="application/ld+json">{...}</script>',
            fix='Add <script type="application/ld+json"> with schema data inside <head> or end of <body>.'
        )


# =============================================================================
# AI SEO ERRORS
# =============================================================================

class AIErrors:
    """AI SEO validation error templates."""
    
    @staticmethod
    def missing_llms_txt(file: str) -> ValidationError:
        return ValidationError(
            code="AI001",
            severity="error",
            file=file,
            line=None,
            element="llms.txt",
            rule="Site should have /llms.txt for AI crawlers",
            current="File not found",
            expected="public/llms.txt or static/llms.txt",
            fix="Create llms.txt in public/static directory. Include site name, description, and key pages."
        )
    
    @staticmethod
    def llms_missing_section(file: str, section: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="AI002",
            severity="warning",
            file=file,
            line=line,
            element="llms.txt",
            rule=f"llms.txt should have '{section}' section",
            current=f"Missing: {section}",
            expected=f"## {section}",
            fix=f"Add '## {section}' section to llms.txt with relevant content."
        )
    
    @staticmethod
    def llms_missing_title(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="AI003",
            severity="error",
            file=file,
            line=line,
            element="llms.txt",
            rule="llms.txt must have site title on first line",
            current=None,
            expected="# Site Name",
            fix="Add '# Site Name' as first line of llms.txt."
        )
    
    @staticmethod
    def llms_missing_description(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="AI004",
            severity="error",
            file=file,
            line=line,
            element="llms.txt",
            rule="llms.txt must have site description",
            current=None,
            expected="> One-line description of your site",
            fix="Add '> Brief description' after the title in llms.txt."
        )
    
    @staticmethod
    def robots_blocks_ai(file: str, bot: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="AI005",
            severity="warning",
            file=file,
            line=line,
            element="robots.txt",
            rule=f"robots.txt blocks {bot}",
            current=f"User-agent: {bot}\\nDisallow: /",
            expected=f"User-agent: {bot}\\nAllow: /",
            fix=f"Change 'Disallow: /' to 'Allow: /' for {bot}, or remove the block entirely."
        )
    
    @staticmethod
    def missing_robots_txt(file: str) -> ValidationError:
        return ValidationError(
            code="AI006",
            severity="warning",
            file=file,
            line=None,
            element="robots.txt",
            rule="Site should have robots.txt",
            current="File not found",
            expected="public/robots.txt",
            fix="Create robots.txt in public directory with User-agent and Allow/Disallow rules."
        )


# =============================================================================
# PERFORMANCE ERRORS
# =============================================================================

class PerfErrors:
    """Performance/Core Web Vitals error templates."""
    
    @staticmethod
    def image_missing_dimensions(file: str, img_src: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF001",
            severity="error",
            file=file,
            line=line,
            element=f'<img src="{img_src[:30]}...">',
            rule="Images must have width and height attributes",
            current="Missing width/height",
            expected='<img src="..." width="..." height="...">',
            fix=f'Add width and height attributes to <img src="{img_src[:30]}..."> to prevent CLS.'
        )
    
    @staticmethod
    def image_missing_alt(file: str, img_src: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF002",
            severity="error",
            file=file,
            line=line,
            element=f'<img src="{img_src[:30]}...">',
            rule="Images must have alt attribute for accessibility",
            current="Missing alt",
            expected='<img src="..." alt="Description">',
            fix=f'Add descriptive alt attribute to <img src="{img_src[:30]}...">.'
        )
    
    @staticmethod
    def image_not_lazy(file: str, img_src: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF003",
            severity="warning",
            file=file,
            line=line,
            element=f'<img src="{img_src[:30]}...">',
            rule="Below-fold images should use lazy loading",
            current="No loading attribute",
            expected='<img src="..." loading="lazy">',
            fix=f'Add loading="lazy" to below-fold images for better LCP.'
        )
    
    @staticmethod
    def image_not_optimized(file: str, img_src: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF004",
            severity="warning",
            file=file,
            line=line,
            element=f'<img src="{img_src[:30]}...">',
            rule="Images should use modern formats (WebP/AVIF)",
            current=img_src.split(".")[-1] if "." in img_src else "unknown",
            expected=".webp or .avif format",
            fix=f"Convert image to WebP/AVIF format, or use <picture> with multiple sources."
        )
    
    @staticmethod
    def font_not_preloaded(file: str, font_url: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF005",
            severity="warning",
            file=file,
            line=line,
            element='<link rel="preload">',
            rule="Critical fonts should be preloaded",
            current=f"Font not preloaded: {font_url[:30]}...",
            expected='<link rel="preload" href="..." as="font" type="font/woff2" crossorigin>',
            fix=f'Add font preload: <link rel="preload" href="{font_url}" as="font" type="font/woff2" crossorigin>.'
        )
    
    @staticmethod
    def missing_font_display(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF006",
            severity="error",
            file=file,
            line=line,
            element="@font-face",
            rule="@font-face must have font-display property",
            current="Missing font-display",
            expected="font-display: swap;",
            fix="Add 'font-display: swap;' to @font-face rule to prevent FOIT."
        )
    
    @staticmethod
    def render_blocking_resource(file: str, resource: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF007",
            severity="warning",
            file=file,
            line=line,
            element=f"<script/link>",
            rule="Render-blocking resources should be deferred/async",
            current=resource[:50],
            expected='<script defer> or <link rel="preload">',
            fix=f"Add 'defer' or 'async' to script, or preload critical CSS."
        )
    
    @staticmethod
    def missing_meta_theme_color(file: str, line: int | None = None) -> ValidationError:
        return ValidationError(
            code="PERF008",
            severity="warning",
            file=file,
            line=line,
            element='<meta name="theme-color">',
            rule="Page should have theme-color for mobile browsers",
            current=None,
            expected='<meta name="theme-color" content="#ffffff">',
            fix='Add <meta name="theme-color" content="#YOUR_COLOR"> inside <head>.'
        )


# =============================================================================
# LIGHTHOUSE ERRORS
# =============================================================================

class LighthouseErrors:
    """Lighthouse validation error templates."""
    
    @staticmethod
    def score_below_target(file: str, category: str, score: int, target: int) -> ValidationError:
        return ValidationError(
            code=f"LH_{category.upper()[:4]}",
            severity="error",
            file=file,
            line=None,
            element=f"Lighthouse {category}",
            rule=f"{category} score must be ≥{target}",
            current=f"{score}/100",
            expected=f"≥{target}/100",
            fix=f"Improve {category} score by {target - score} points. Run Lighthouse for specific recommendations."
        )
    
    @staticmethod
    def server_not_running(url: str) -> ValidationError:
        return ValidationError(
            code="LH_CONN",
            severity="error",
            file=url,
            line=None,
            element="Dev Server",
            rule="Dev server must be running for validation",
            current="Connection refused",
            expected=f"Server running at {url}",
            fix=f"Start your dev server before running validation. Expected URL: {url}"
        )
