.PHONY: all deps check help

all: deps
	@echo "✓ Setup complete"

deps:
	@echo "Installing dependencies..."
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@echo "✓ uv"
	@command -v playwright >/dev/null 2>&1 || { echo "Installing playwright..."; uv tool install playwright && playwright install chromium; }
	@echo "✓ playwright"

check:
	@command -v uv >/dev/null 2>&1 && echo "✓ uv" || echo "✗ uv"
	@command -v playwright >/dev/null 2>&1 && echo "✓ playwright" || echo "✗ playwright"

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "  all    Install dependencies (default)"
	@echo "  deps   Install uv and playwright"
	@echo "  check  Verify installation"
