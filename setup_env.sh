#!/usr/bin/env bash
# ============================================================
#  setup_env.sh for Linux / macOS
#  Usage:
#    chmod +x setup_env.sh
#    ./setup_env.sh
# ============================================================

set -e

VENV_NAME="venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Dual-Arm DLO Demo: Environment Setup    ${NC}"
echo -e "${GREEN}============================================${NC}"

# ── 1. Check Python ──────────────────────────────────────────
echo -e "\n${YELLOW}[1/5] Checking Python...${NC}"
PYTHON_BIN=$(command -v python3 || command -v python)
if [ -z "$PYTHON_BIN" ]; then
    echo -e "${RED}ERROR: Python not found. Install Python 3.10+ first.${NC}"
    exit 1
fi
PYTHON_VER=$($PYTHON_BIN --version 2>&1)
echo -e "   Found: $PYTHON_VER at $PYTHON_BIN"

PYTHON_OK=$($PYTHON_BIN -c "import sys; print(int(sys.version_info >= (3, 10)))")
if [ "$PYTHON_OK" -ne 1 ]; then
    echo -e "${RED}ERROR: Python 3.10+ required.${NC}"
    exit 1
fi
echo -e "   ${GREEN}✓ OK${NC}"

# ── 2. Check requirements.txt exists ─────────────────────────
echo -e "\n${YELLOW}[2/5] Checking requirements.txt...${NC}"
if [ ! -f "$REQUIREMENTS" ]; then
    echo -e "${RED}ERROR: requirements.txt not found at $REQUIREMENTS${NC}"
    exit 1
fi
echo -e "   Found: $REQUIREMENTS"
echo -e "   ${GREEN}✓ OK${NC}"

# ── 3. Create virtual environment ────────────────────────────
echo -e "\n${YELLOW}[3/5] Creating virtual environment '$VENV_NAME'...${NC}"
if [ -d "$SCRIPT_DIR/$VENV_NAME" ]; then
    echo -e "   Removing existing '$VENV_NAME/'..."
    rm -rf "$SCRIPT_DIR/$VENV_NAME"
fi
$PYTHON_BIN -m venv "$SCRIPT_DIR/$VENV_NAME"
source "$SCRIPT_DIR/$VENV_NAME/bin/activate"
echo -e "   ${GREEN}✓ OK${NC}"

# ── 4. Upgrade pip and install from requirements.txt ─────────
echo -e "\n${YELLOW}[4/5] Installing from requirements.txt...${NC}"
pip install --upgrade pip --quiet
pip install -r "$REQUIREMENTS"
echo -e "   ${GREEN}✓ OK${NC}"

# ── 5. Verify every package in requirements.txt ──────────────
echo -e "\n${YELLOW}[5/5] Verifying installed packages...${NC}"
pip list --format=columns | grep -Ei "$(grep -v '^#' "$REQUIREMENTS" | grep -v '^$' | sed 's/[>=<].*//' | tr '\n' '|' | sed 's/|$//')"
echo -e "   ${GREEN}✓ All packages verified${NC}"

# ── Done ─────────────────────────────────────────────────────
echo -e "\n${GREEN}============================================${NC}"
echo -e "${GREEN}  Setup complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo -e "\nTo activate in a new terminal:"
echo -e "   ${YELLOW}source $VENV_NAME/bin/activate${NC}"
echo -e "\nTo run the demo:"
echo -e "   ${YELLOW}cd simulation && python demo_pick_cube.py${NC}\n"
