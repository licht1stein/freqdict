#!/bin/bash
# Freqdict installer for macOS
# Run: bash install-mac.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.local/share/freqdict"
WORKFLOW_DIR="$HOME/Library/Services"

echo "Installing Freqdict..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    if [ -f "$HOME/.local/bin/uv" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    elif [ -f "$HOME/.cargo/bin/uv" ]; then
        export PATH="$HOME/.cargo/bin:$PATH"
    else
        echo "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi

# Copy freqdict.py
echo "Installing freqdict.py to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_DIR/freqdict.py" "$INSTALL_DIR/"

# Install workflow
echo "Installing Finder Quick Action..."
mkdir -p "$WORKFLOW_DIR"
cp -R "$SCRIPT_DIR/Freqdict Here.workflow" "$WORKFLOW_DIR/"

echo ""
echo "Done! Right-click any folder in Finder and select:"
echo "  Quick Actions → Freqdict Here"
echo ""
echo "The frequency dictionary will be saved as frequency_dict.csv in that folder."
