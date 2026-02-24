#!/usr/bin/env bash
# Install mprocs — terminal multiplexer for parallel agent swarms
# https://github.com/pvolok/mprocs

set -euo pipefail

if command -v mprocs &>/dev/null; then
  echo "mprocs $(mprocs --version 2>&1) already installed"
  exit 0
fi

echo "Installing mprocs..."

if command -v cargo &>/dev/null; then
  cargo install mprocs
elif command -v brew &>/dev/null; then
  brew install mprocs
elif command -v npm &>/dev/null; then
  npm install -g mprocs
else
  echo "No supported package manager found (cargo, brew, npm). Install manually:"
  echo "  https://github.com/pvolok/mprocs#installation"
  exit 1
fi

echo "mprocs $(mprocs --version 2>&1) installed"
