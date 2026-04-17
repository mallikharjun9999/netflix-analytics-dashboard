#!/usr/bin/env bash
# ============================================================
#  NetflixIQ — Setup Script
#  Run: bash setup.sh
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${RED}"
echo "  ███╗   ██╗███████╗████████╗███████╗██╗     ██╗██╗  ██╗██╗ ██████╗ "
echo "  ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║     ██║╚██╗██╔╝██║██╔═══██╗"
echo "  ██╔██╗ ██║█████╗     ██║   █████╗  ██║     ██║ ╚███╔╝ ██║██║   ██║"
echo "  ██║╚██╗██║██╔══╝     ██║   ██╔══╝  ██║     ██║ ██╔██╗ ██║██║▄▄ ██║"
echo "  ██║ ╚████║███████╗   ██║   ██║     ███████╗██║██╔╝ ██╗██║╚██████╔╝"
echo "  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝╚═╝ ╚══▀▀═╝ "
echo -e "${NC}"
echo -e "${CYAN}  Netflix Analytics Dashboard — Setup${NC}"
echo -e "  ─────────────────────────────────────────────"
echo ""

# ── Step 1: Python check ──
echo -e "${YELLOW}[1/5] Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Python not found. Please install Python 3.9+."
    exit 1
fi
PYVER=$($PYTHON --version 2>&1)
echo -e "${GREEN}    ✔ Found $PYVER${NC}"

# ── Step 2: Virtual environment ──
echo ""
echo -e "${YELLOW}[2/5] Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
    echo -e "${GREEN}    ✔ Virtual environment created${NC}"
else
    echo -e "${GREEN}    ✔ Virtual environment already exists${NC}"
fi

# Activate
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# ── Step 3: Install dependencies ──
echo ""
echo -e "${YELLOW}[3/5] Installing dependencies...${NC}"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo -e "${GREEN}    ✔ All dependencies installed${NC}"

# ── Step 4: Migrate database ──
echo ""
echo -e "${YELLOW}[4/5] Running database migrations...${NC}"
python manage.py migrate --run-syncdb 2>/dev/null || python manage.py migrate
echo -e "${GREEN}    ✔ Database ready${NC}"

# ── Step 5: Start server ──
echo ""
echo -e "${YELLOW}[5/5] Starting development server...${NC}"
echo ""
echo -e "${GREEN}  ════════════════════════════════════════${NC}"
echo -e "${GREEN}   NetflixIQ is running!${NC}"
echo -e "${GREEN}   Open: http://127.0.0.1:8000${NC}"
echo -e "${GREEN}  ════════════════════════════════════════${NC}"
echo ""
echo -e "  Press ${RED}CTRL+C${NC} to stop the server."
echo ""
python manage.py runserver
