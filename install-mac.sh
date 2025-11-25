#!/bin/bash
# Freqdict installer for macOS
# Run: curl -fsSL https://raw.githubusercontent.com/licht1stein/freqdict/v0.7/install-mac.sh | sh

set -e

REPO_URL="https://raw.githubusercontent.com/licht1stein/freqdict/v0.7"
INSTALL_DIR="$HOME/.local/share/freqdict"
WORKFLOW_DIR="$HOME/Library/Services"
WORKFLOW_NAME="Freqdict Here.workflow"

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

# Install antiword for .doc support
if ! command -v antiword &> /dev/null; then
    echo "Installing antiword (for .doc file support)..."
    brew install antiword
fi

# Download freqdict.py
echo "Downloading freqdict.py..."
mkdir -p "$INSTALL_DIR"
curl -fsSL "$REPO_URL/freqdict.py" -o "$INSTALL_DIR/freqdict.py"

# Create workflow directory structure
echo "Installing Finder Quick Action..."
mkdir -p "$WORKFLOW_DIR/$WORKFLOW_NAME/Contents"

# Download workflow files
curl -fsSL "$REPO_URL/Freqdict%20Here.workflow/Contents/Info.plist" \
    -o "$WORKFLOW_DIR/$WORKFLOW_NAME/Contents/Info.plist"
curl -fsSL "$REPO_URL/Freqdict%20Here.workflow/Contents/document.wflow" \
    -o "$WORKFLOW_DIR/$WORKFLOW_NAME/Contents/document.wflow"

echo ""
echo "Done! Right-click any folder in Finder and select:"
echo "  Quick Actions → Freqdict Here"
echo ""
echo "The frequency dictionary will be saved as frequency_dict.csv in that folder."
