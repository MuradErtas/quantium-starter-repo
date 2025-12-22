#!/bin/bash
# Script to activate virtual environment and run pytest test suite
# Returns exit code 0 if tests pass, 1 if they fail

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found in venv/"
    exit 1
fi

# Activate virtual environment
# Try Unix-style activation first (for Linux/Mac/WSL)
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
# Try Windows-style activation (for Git Bash on Windows or WSL accessing Windows venv)
elif [ -f "venv/Scripts/activate" ]; then
    # In WSL, we can access Windows Python directly
    if [ -f "/mnt/c/Windows/System32/cmd.exe" ]; then
        # We're in WSL, use Windows Python directly
        PYTHON_PATH="$(find venv/Scripts -name 'python.exe' 2>/dev/null | head -1)"
        if [ -n "$PYTHON_PATH" ]; then
            export PATH="$(dirname "$PYTHON_PATH"):$PATH"
        else
            echo "Error: Could not find Python in venv/Scripts/"
            exit 1
        fi
    else
        source venv/Scripts/activate
    fi
else
    echo "Error: Could not find virtual environment activation script"
    exit 1
fi

# Run pytest and capture exit code
echo "Running test suite..."
# Use python -m pytest if we're in WSL with Windows venv, otherwise use pytest directly
if [ -n "$PYTHON_PATH" ]; then
    "$PYTHON_PATH" -m pytest test_sales_app.py -v
else
    pytest test_sales_app.py -v
fi

# pytest returns 0 on success, non-zero on failure
# Capture and return the exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Tests failed!"
    exit 1
fi

