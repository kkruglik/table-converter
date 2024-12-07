#!/bin/bash

VENV_PATH="/Users/kirillkruglikov/table-converter/.venv"
PYTHON_SCRIPT="main"

if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

"$VENV_PATH/bin/python" -m "$PYTHON_SCRIPT"

if [ $? -eq 0 ]; then
    echo "Script executed successfully"
else
    echo "Error: Script execution failed"
    exit 1
fi