#!/bin/bash
# RecruitIQ — Setup & Run Script
set -e

echo ""
echo "═══════════════════════════════════════════"
echo "  🎯  RecruitIQ — AI Resume Screener Setup"
echo "═══════════════════════════════════════════"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required. Please install it."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo ""
    echo "→ Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "→ Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r backend/requirements.txt

echo "→ Downloading spaCy language model..."
python3 -m spacy download en_core_web_sm --quiet

echo ""
echo "═══════════════════════════════════════════"
echo "  ✅  Setup complete!"
echo "═══════════════════════════════════════════"
echo ""
echo "  Starting server at http://localhost:5000"
echo "  Press Ctrl+C to stop."
echo ""

cd backend && python3 app.py
