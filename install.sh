#!/usr/bin/env bash
set -euo pipefail

echo "=== Agentic OS Installer ==="
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux)   OS="linux" ;;
    Darwin)  OS="macos" ;;
    *)       echo "Unsupported OS: $OS"; exit 1 ;;
esac
echo "Detected OS: $OS"

# Check Python
if command -v python3 &>/dev/null; then
    echo "Python: $(python3 --version)"
else
    echo "ERROR: Python 3.10+ required. Install via: sudo apt install python3"
    exit 1
fi

# Install uv into bin/ if not present
BIN_DIR="bin"
UV="$BIN_DIR/uv"
if [ -x "$UV" ]; then
    echo "uv: $($UV --version)"
else
    echo "Installing uv to $BIN_DIR/..."
    mkdir -p "$BIN_DIR"
    curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$PWD/$BIN_DIR" sh
    if [ ! -x "$UV" ]; then
        echo "ERROR: uv installation failed. Install manually: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    echo "uv: $($UV --version)"
    # Remove shell helper scripts — we reference bin/uv directly
    rm -f "$BIN_DIR/env" "$BIN_DIR/env.fish"
fi

# Create virtual environment
VENV_DIR=".venv"
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists at $VENV_DIR/"
else
    echo "Creating virtual environment..."
    "$UV" venv "$VENV_DIR" --python 3.12
    echo "Created $VENV_DIR/"
fi

# Install Python deps into venv
echo "Installing Python dependencies..."
"$UV" pip install --python "$VENV_DIR/bin/python3" -r requirements.txt --quiet

# Check Node.js (for opencode)
if command -v node &>/dev/null; then
    echo "Node.js: $(node --version)"
else
    echo "WARNING: Node.js not found. opencode requires Node 18+."
    echo "  Install via: curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash - && sudo apt install -y nodejs"
fi

# Check opencode
if command -v opencode &>/dev/null; then
    echo "opencode: $(opencode --version 2>/dev/null || echo 'installed')"
else
    echo "WARNING: opencode not found. Install via: npm install -g @opencode/cli"
fi

# Check Hermes
if command -v hermes &>/dev/null; then
    echo "Hermes: found"
else
    echo "WARNING: Hermes Agent not found. Install via: curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
fi

# Check agy (Antigravity CLI)
if command -v agy &>/dev/null; then
    echo "agy (Antigravity): found"
else
    echo "WARNING: agy CLI not found. Install via: curl -fsSL https://antigravity.ai/install | bash"
fi

# Create required directories
mkdir -p backups audit

# Initialize git if not already
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    grep -qxF "audit/*" .gitignore || echo "audit/*" >> .gitignore
    grep -qxF "backups/*.tar.gz" .gitignore || echo "backups/*.tar.gz" >> .gitignore
    grep -qxF "data/settings.json" .gitignore || echo "data/settings.json" >> .gitignore
fi

echo ""
echo "=== Installation complete! ==="
echo ""
echo "Next steps:"
echo "  1. Edit data/settings.json with your API keys"
echo "  2. Run ./start.sh to launch the dashboard"
echo "  3. Open http://127.0.0.1:8080 in your browser"
