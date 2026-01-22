"""
SEO Validation Hook Library

Shared utilities for all SEO validation hooks.
"""
from .response import (
    ValidationError,
    ValidationResult,
    success,
    failure,
    skip,
    block,
    MetaErrors,
    SchemaErrors,
    AIErrors,
    PerfErrors,
    LighthouseErrors,
)

__all__ = [
    "ValidationError",
    "ValidationResult",
    "success",
    "failure",
    "skip",
    "block",
    "MetaErrors",
    "SchemaErrors",
    "AIErrors",
    "PerfErrors",
    "LighthouseErrors",
]
