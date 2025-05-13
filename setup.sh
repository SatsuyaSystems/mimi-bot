#!/bin/bash
# --- Setup and Run Script for Linux ---

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Checking for virtual environment..."

# Check if the 'venv' directory exists
if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' not found. Creating it..."
    # Create the virtual environment
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment 'venv' already exists."
fi

echo "Activating the virtual environment..."

# Check if the activate script exists inside the venv
if [ ! -f venv/bin/activate ]; then
    echo "Error: Virtual environment 'venv/bin/activate' not found."
    echo "Ensure the virtual environment was created successfully."
    exit 1
fi

# Activate the virtual environment
# Use 'source' or '.' to run the activate script in the current shell context
source venv/bin/activate

echo "Virtual environment activated."

echo "Installing/Updating dependencies from requirements.txt..."

# Install or update dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed/updated."
else
    echo "Warning: requirements.txt not found. Skipping dependency installation."
fi

echo "Installing Playwright browsers..."

# Install Playwright browsers
playwright install --with-deps
echo "Playwright browsers installed."

echo "Running the Python script 'main.py'..."

# Execute the Python script
# The 'set -e' at the top means this script will exit if main.py fails
python main.py

echo "Python script finished."

# --- Pause to keep the terminal window open ---
# This mimics the 'pause' behavior of the Windows script.
# Useful if you double-clicking the script in a GUI file manager.
# If running from an already open terminal, this might not be necessary.
echo ""
read -p "Press Enter to finish..."

# Script exits successfully if all commands ran without error (due to set -e)
# If main.py exited with an error code, the script would have exited there.