#!/bin/bash
# ELENA AI — Quick Installer for Termux & Linux
# Usage: bash install.sh

set -e

RESET="\033[0m"
GREEN="\033[92m"
YELLOW="\033[93m"
BLUE="\033[94m"
RED="\033[91m"
BOLD="\033[1m"

echo -e "\n${BLUE}${BOLD}🤖 ELENA AI v3.0 — Installer${RESET}\n"

# Detect environment
IS_TERMUX=false
if [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
    echo -e "  ${GREEN}✓ Terux terdeteksi${RESET}"
else
    echo -e "  ${GREEN}✓ Linux/macOS terdeteksi${RESET}"
fi

# Install Python if Termux
if [ "$IS_TERMUX" = true ]; then
    echo -e "  ${YELLOW}Menginstall Python...${RESET}"
    pkg install python python-pip -y -q
fi

# Install Python dependencies
echo -e "  ${YELLOW}Menginstall dependencies Python...${RESET}"
if [ "$IS_TERMUX" = true ]; then
    pip install requests --break-system-packages -q
else
    pip install requests -q 2>/dev/null || pip3 install requests -q
fi

echo -e "  ${GREEN}✓ requests terinstall${RESET}"

# Create alias (optional)
SHELL_RC=""
if [ -f "$HOME/.bashrc" ]; then SHELL_RC="$HOME/.bashrc"; fi
if [ -f "$HOME/.zshrc" ]; then SHELL_RC="$HOME/.zshrc"; fi

if [ -n "$SHELL_RC" ]; then
    SCRIPT_PATH="$(realpath elena.py)"
    if ! grep -q "alias elena=" "$SHELL_RC" 2>/dev/null; then
        echo "alias elena='python $SCRIPT_PATH'" >> "$SHELL_RC"
        echo -e "  ${GREEN}✓ Alias 'elena' ditambahkan ke $SHELL_RC${RESET}"
    fi
fi

echo -e "\n${GREEN}${BOLD}✅ Instalasi selesai!${RESET}"
echo -e "\n${YELLOW}Jalankan ELENA dengan:${RESET}"
echo -e "  ${BOLD}python elena.py${RESET}"
if [ -n "$SHELL_RC" ]; then
    echo -e "\n  atau setelah restart terminal:"
    echo -e "  ${BOLD}elena${RESET}"
fi
echo ""
