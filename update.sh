#!/bin/bash

echo "Updating fixshell installation..."
echo "=================================="
echo ""

INSTALL_DIR="$HOME/.local/fixshell"
BIN_DIR="$HOME/.local/bin"
REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "❌ fixshell not found at $INSTALL_DIR"
    echo "Run ./setup.sh first to install."
    exit 1
fi

# First, try to update from git (stash local changes if needed)
echo "Updating code from git..."
cd "$REPO_DIR"

# Check if there are local changes
if ! git diff --quiet; then
    echo "⚠ Local changes detected. Stashing them..."
    git stash
    STASHED=1
else
    STASHED=0
fi

# Pull latest changes
git pull origin main

# Restore stashed changes if any
if [ $STASHED -eq 1 ]; then
    echo "⚠ Restoring local changes (you may need to merge manually)..."
    git stash pop || true
fi

echo ""
echo "Copying updated files to installation..."
cp -r "$REPO_DIR/fixshell" "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$REPO_DIR/data" "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$REPO_DIR/themes" "$INSTALL_DIR/" 2>/dev/null || true
cp "$REPO_DIR/fixshell_launcher.py" "$INSTALL_DIR/" 2>/dev/null || true

echo ""
echo "✓ Update complete!"
echo ""
echo "Restart fixshell or open a new terminal to use the updated version."




