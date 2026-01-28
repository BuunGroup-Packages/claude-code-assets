.PHONY: all deps deps-wsl check help

all: deps
	@echo "✓ Setup complete"

deps:
	@echo "Installing dependencies..."
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@echo "✓ uv"
	@command -v playwright >/dev/null 2>&1 || { echo "Installing playwright..."; uv tool install playwright && playwright install chromium; }
	@echo "✓ playwright"
	@command -v lighthouse >/dev/null 2>&1 || { echo "Installing lighthouse..."; npm install -g lighthouse; }
	@echo "✓ lighthouse"
	@npm list -g terser >/dev/null 2>&1 || { echo "Installing terser..."; npm install -g terser; }
	@echo "✓ terser"

deps-wsl:
	@echo "Installing WSL dependencies..."
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@echo "✓ uv"
	@command -v chromium-browser >/dev/null 2>&1 || { echo "Installing chromium..."; sudo apt install -y chromium-browser; }
	@echo "✓ chromium-browser"
	@command -v convert >/dev/null 2>&1 || { echo "Installing imagemagick..."; sudo apt install -y imagemagick; }
	@echo "✓ imagemagick"
	@command -v lighthouse >/dev/null 2>&1 || { echo "Installing lighthouse..."; npm install -g lighthouse; }
	@echo "✓ lighthouse"
	@npm list -g terser >/dev/null 2>&1 || { echo "Installing terser..."; npm install -g terser; }
	@echo "✓ terser"
	@grep -q "CHROME_PATH" ~/.bashrc || echo 'export CHROME_PATH=$$(which chromium-browser)' >> ~/.bashrc
	@echo "✓ CHROME_PATH set in .bashrc"
	@echo ""
	@echo "Run: source ~/.bashrc"

check:
	@command -v uv >/dev/null 2>&1 && echo "✓ uv" || echo "✗ uv"
	@command -v playwright >/dev/null 2>&1 && echo "✓ playwright" || echo "✗ playwright"
	@command -v lighthouse >/dev/null 2>&1 && echo "✓ lighthouse" || echo "✗ lighthouse"
	@npm list -g terser >/dev/null 2>&1 && echo "✓ terser" || echo "✗ terser (needed for Vite build)"
	@command -v convert >/dev/null 2>&1 && echo "✓ imagemagick" || echo "- imagemagick (for seo-assets)"
	@command -v chromium-browser >/dev/null 2>&1 && echo "✓ chromium-browser" || echo "- chromium-browser (WSL)"
	@test -n "$$CHROME_PATH" && echo "✓ CHROME_PATH=$$CHROME_PATH" || echo "- CHROME_PATH not set"

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "  all       Install dependencies (default)"
	@echo "  deps      Install uv, playwright, lighthouse, terser"
	@echo "  deps-wsl  Install for WSL (chromium, imagemagick + env vars)"
	@echo "  check     Verify installation"
	@echo ""
	@echo "Dependencies:"
	@echo "  uv          - Python package runner"
	@echo "  playwright  - Browser automation"
	@echo "  lighthouse  - SEO/performance audits"
	@echo "  terser      - JS minifier (Vite builds)"
	@echo "  imagemagick - Image processing (seo-assets)"
