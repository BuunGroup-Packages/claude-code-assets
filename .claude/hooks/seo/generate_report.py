#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Stop Hook: SEO Report Generator

Generates a summary report after SEO skill execution.
Runs on skill Stop event to provide final status.
"""
import json
import sys


def main() -> None:
    """Generate SEO summary report."""
    # Read stop hook data
    data = json.load(sys.stdin)

    # Stop hooks receive different data than PostToolUse
    # Just output a simple continue response
    response = {
        "continue": True
    }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
