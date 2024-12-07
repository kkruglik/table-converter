#!/bin/bash

# Change to the script's directory
cd "$(dirname "$0")" || exit


# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python first."
    echo "Press any key to exit..."
    read -n 1 -s
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install or upgrade table-converter if not installed
if ! pip show table-converter &> /dev/null; then
    echo "Installing table-converter..."
    pip install git+https://github.com/kkruglik/table-converter
fi

# Run table-converter in current directory
table-converter

# Keep terminal window open to see any errors
echo "Press any key to exit..."
read -n 1 -s