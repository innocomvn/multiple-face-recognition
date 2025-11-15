#!/bin/bash

# Face Recognition Attendance System - Quick Start Script
# This script helps you start the application easily

echo "🚀 Starting Face Recognition Attendance System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}✅ Python found:${NC} $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Check if requirements are installed
if [ ! -f "venv/.installed" ]; then
    echo -e "${YELLOW}📥 Installing dependencies...${NC}"
    echo "This may take 5-10 minutes..."
    pip install -r requirements.txt

    if [ $? -eq 0 ]; then
        touch venv/.installed
        echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}📁 Checking directories...${NC}"
mkdir -p "Training images"
mkdir -p "Customer images"
echo -e "${GREEN}✅ Directories ready${NC}"

# Start the application
echo ""
echo -e "${GREEN}🎯 Starting application...${NC}"
echo ""
echo "============================================"
echo "  Access the application at:"
echo "  👉 http://localhost:5000"
echo "============================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app_improved.py
