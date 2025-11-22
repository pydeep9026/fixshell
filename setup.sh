#!/bin/bash

set -e

echo "fixshell - Cloud Workstation Setup"
echo "==================================="
echo ""

INSTALL_DIR="$HOME/.local/fixshell"
BIN_DIR="$HOME/.local/bin"
REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Installing fixshell to $INSTALL_DIR..."

mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

echo "Copying files..."
cp -r "$REPO_DIR/fixshell" "$INSTALL_DIR/"
cp -r "$REPO_DIR/data" "$INSTALL_DIR/"
cp -r "$REPO_DIR/themes" "$INSTALL_DIR/" 2>/dev/null || true
cp "$REPO_DIR/fixshell_launcher.py" "$INSTALL_DIR/"

echo "Creating fixshell command..."
cat > "$BIN_DIR/fixshell" << 'EOF'
#!/bin/bash
python "$HOME/.local/fixshell/fixshell_launcher.py" "$@"
EOF

chmod +x "$BIN_DIR/fixshell"
chmod +x "$INSTALL_DIR/fixshell_launcher.py"

echo ""
echo "Adding $BIN_DIR to PATH..."

SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "export PATH.*$BIN_DIR" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# fixshell" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
        echo "✓ Added PATH to $SHELL_RC"
    else
        echo "✓ PATH already configured in $SHELL_RC"
    fi
else
    echo "⚠ Could not find shell config file"
    echo "Please add this to your shell config:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "==================================="
echo "✓ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Run: source $SHELL_RC"
echo "  2. Or restart your terminal"
echo "  3. Then type: fixshell"
echo ""
echo "To verify: fixshell --version"

