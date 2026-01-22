#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
PostToolUse Hook: JSON-LD Schema Validation

Validates JSON-LD structured data after file edit.

Trigger: Edit|Write|MultiEdit on schema-related files
Output: Success message or ordered list of fixes

Run with: uv run "$CLAUDE_PROJECT_DIR"/.claude/hooks/seo/post_schema_validate.py
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

from lib.response import success, failure, skip, SchemaErrors, ValidationError
from lib.validators import is_schema_file, is_meta_file, find_line_number


# =============================================================================
# CONFIGURATION
# =============================================================================

SCHEMA_REQUIRED_PROPS = {
    "Organization": ["name", "url"],
    "LocalBusiness": ["name", "address"],
    "Article": ["headline", "author", "datePublished"],
    "BlogPosting": ["headline", "author", "datePublished"],
    "NewsArticle": ["headline", "author", "datePublished"],
    "Product": ["name", "description"],
    "WebSite": ["name", "url"],
    "WebPage": ["name"],
    "BreadcrumbList": ["itemListElement"],
    "FAQPage": ["mainEntity"],
    "HowTo": ["name", "step"],
    "Recipe": ["name", "recipeIngredient", "recipeInstructions"],
    "Event": ["name", "startDate", "location"],
    "Person": ["name"],
    "VideoObject": ["name", "description", "thumbnailUrl", "uploadDate"],
}


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
    
    # Check if file might contain schema
    if not is_schema_file(file_path) and not is_meta_file(file_path):
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

    # Check if file actually contains JSON-LD
    if "application/ld+json" not in content and "@context" not in content:
        print(skip())
        return
    
    # Validate
    errors, warnings = validate_schemas(content, file_path)
    
    if errors:
        print(failure(file_path, "SCHEMA", errors, warnings))
    elif warnings:
        print(failure(file_path, "SCHEMA", [], warnings))
    else:
        print(success(file_path, "SCHEMA"))


# =============================================================================
# VALIDATION LOGIC
# =============================================================================

def validate_schemas(content: str, file_path: str) -> tuple[list[ValidationError], list[ValidationError]]:
    """
    Validate all JSON-LD schemas in content.
    
    Args:
        content: File content
        file_path: Path to file
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    lines = content.split("\n")
    
    # Extract all JSON-LD blocks
    schemas = extract_jsonld_blocks(content)
    
    if not schemas:
        # No JSON-LD found - not an error, file might be for other purposes
        return errors, warnings
    
    for i, (json_str, line_num) in enumerate(schemas):
        schema_errors, schema_warnings = validate_single_schema(
            json_str, file_path, line_num, i + 1, len(schemas)
        )
        errors.extend(schema_errors)
        warnings.extend(schema_warnings)
    
    return errors, warnings


def extract_jsonld_blocks(content: str) -> list[tuple[str, int]]:
    """
    Extract JSON-LD script blocks from content.
    
    Returns:
        List of (json_string, line_number) tuples
    """
    results = []
    
    # Pattern for script tags
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    
    for match in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
        json_str = match.group(1).strip()
        # Calculate line number
        line_num = content[:match.start()].count("\n") + 1
        results.append((json_str, line_num))
    
    # Also check for standalone JSON files
    if not results and content.strip().startswith("{"):
        results.append((content.strip(), 1))
    
    return results


def validate_single_schema(
    json_str: str, 
    file_path: str, 
    line_num: int,
    schema_index: int,
    total_schemas: int
) -> tuple[list[ValidationError], list[ValidationError]]:
    """
    Validate a single JSON-LD schema.
    
    Args:
        json_str: Raw JSON string
        file_path: Path to file
        line_num: Starting line number
        schema_index: Which schema (1-indexed)
        total_schemas: Total number of schemas in file
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    prefix = f"Schema {schema_index}" if total_schemas > 1 else "Schema"
    
    # Parse JSON
    try:
        schema = json.loads(json_str)
    except json.JSONDecodeError as e:
        errors.append(SchemaErrors.invalid_json(file_path, str(e), line_num))
        return errors, warnings
    
    # Handle @graph (multiple schemas in one)
    if "@graph" in schema:
        for j, item in enumerate(schema["@graph"]):
            if isinstance(item, dict):
                sub_errors, sub_warnings = validate_schema_object(
                    item, file_path, line_num, f"{prefix}[@graph][{j}]"
                )
                errors.extend(sub_errors)
                warnings.extend(sub_warnings)
        return errors, warnings
    
    # Validate single schema
    return validate_schema_object(schema, file_path, line_num, prefix)


def validate_schema_object(
    schema: dict, 
    file_path: str, 
    line_num: int,
    prefix: str
) -> tuple[list[ValidationError], list[ValidationError]]:
    """
    Validate a single schema object.
    
    Args:
        schema: Parsed schema dict
        file_path: Path to file
        line_num: Line number
        prefix: Error message prefix
        
    Returns:
        Tuple of (errors, warnings)
    """
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []
    
    # Check @context
    context = schema.get("@context")
    if not context:
        errors.append(SchemaErrors.missing_context(file_path, line_num))
    elif "schema.org" not in str(context):
        errors.append(SchemaErrors.invalid_context(file_path, str(context), line_num))
    
    # Check @type
    schema_type = schema.get("@type")
    if not schema_type:
        errors.append(SchemaErrors.missing_type(file_path, line_num))
        return errors, warnings
    
    # Handle array of types
    if isinstance(schema_type, list):
        schema_type = schema_type[0] if schema_type else None
    
    if not schema_type:
        return errors, warnings
    
    # Check required properties for known types
    required_props = SCHEMA_REQUIRED_PROPS.get(schema_type, [])
    
    for prop in required_props:
        if prop not in schema:
            errors.append(SchemaErrors.missing_required(
                file_path, schema_type, prop, line_num
            ))
    
    # Validate URL properties
    url_props = ["url", "image", "logo", "sameAs"]
    for prop in url_props:
        value = schema.get(prop)
        if value:
            if isinstance(value, str) and value and not value.startswith("http"):
                errors.append(SchemaErrors.invalid_url(
                    file_path, prop, value, line_num
                ))
            elif isinstance(value, dict) and value.get("@id"):
                if not value["@id"].startswith("http"):
                    errors.append(SchemaErrors.invalid_url(
                        file_path, f"{prop}.@id", value["@id"], line_num
                    ))
    
    return errors, warnings


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
