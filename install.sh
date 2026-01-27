#!/bin/bash
# Install script for Operator SDK Switcher GUI

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Operator SDK Switcher..."
echo "Install path: $SCRIPT_DIR"

# Create applications directory if it doesn't exist
mkdir -p ~/.local/share/applications

# Create the desktop file with correct paths
cat > ~/.local/share/applications/com.austincunningham.operatorsdk.desktop << EOF
[Desktop Entry]
Name=Operator SDK Switcher
Comment=Switch between Operator SDK versions
Exec=python3 ${SCRIPT_DIR}/main.py
Icon=${SCRIPT_DIR}/icon.svg
Terminal=false
Type=Application
Categories=Development;Utility;
StartupWMClass=com.austincunningham.operatorsdk
EOF

# Make files executable
chmod +x ~/.local/share/applications/com.austincunningham.operatorsdk.desktop
chmod +x "$SCRIPT_DIR/choperator-sdk.sh"

# Update desktop database (if available)
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications 2>/dev/null || true
fi

echo ""
echo "✓ Installation complete!"
echo ""
echo "You can now find 'Operator SDK Switcher' in your application menu."
echo "Or run directly with: python3 ${SCRIPT_DIR}/main.py"
