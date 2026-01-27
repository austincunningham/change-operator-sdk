#!/bin/bash
# Uninstall script for Operator SDK Switcher GUI

echo "Uninstalling Operator SDK Switcher..."

rm -f ~/.local/share/applications/com.austincunningham.operatorsdk.desktop

# Update desktop database (if available)
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications 2>/dev/null || true
fi

echo "✓ Uninstalled successfully!"
