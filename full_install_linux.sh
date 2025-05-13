#!/bin/bash
# --- Script to setup, clone, and run Mimi-Bot on Linux ---

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Checking for Python..."
# Check if python3 command is available
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "WARNING: python3 was not found."
    echo "Please install Python 3 using your distribution's package manager (e.g., sudo apt update && sudo apt install python3 python3-venv)."
    echo "Script will continue, but subsequent steps may fail if Python is required."
    echo ""
    sleep 5
else
    echo "Python 3 found."
fi

echo "Checking for Git..."
# Check if git command is available
if ! command -v git &> /dev/null; then
    echo ""
    echo "WARNING: git was not found."
    echo "Please install Git using your distribution's package manager (e.g., sudo apt update && sudo apt install git)."
    echo "Script will continue, but git clone will fail."
    echo ""
    sleep 5
else
    echo "Git found."
fi

REPO_URL="https://github.com/SatsuyaSystems/mimi-bot.git"
REPO_DIR="mimi-bot"

echo "Cloning the repository $REPO_URL..."

# Check if the target directory already exists
if [ -d "$REPO_DIR" ]; then
    echo "Directory \"$REPO_DIR\" already exists. Skipping clone."
    echo "If you want to re-clone, please delete the \"$REPO_DIR\" folder first."
else
    # Perform the git clone command
    git clone "$REPO_URL"
    # Check if git clone was successful (set -e handles this, but explicit check is also fine)
    # if [ $? -ne 0 ]; then
    #     echo ""
    #     echo "ERROR: Git clone failed. Please check your Git installation and network connection."
    #     echo "Script will exit."
    #     echo ""
    #     read -p "Press Enter to finish..."
    #     exit 1
    # fi
    echo "Repository cloned successfully."
fi

echo "Navigating into the repository directory..."
cd "$REPO_DIR"
# Check if changing directory was successful (set -e handles this)
# if [ $? -ne 0 ]; then
#     echo ""
#     echo "ERROR: Failed to change directory to \"$REPO_DIR\"."
#     echo "Script will exit."
#     echo ""
#     read -p "Press Enter to finish..."
#     exit 1
# fi
echo "Inside $REPO_DIR directory."

echo "Running setup.sh..."
# Make setup.sh executable if it's not already
if [ -f "setup.sh" ]; then
    chmod +x setup.sh
    # Execute the setup script
    ./setup.sh
    # Check if setup.sh was successful (set -e handles this)
    # if [ $? -ne 0 ]; then
    #     echo ""
    #     echo "WARNING: setup.sh reported an error. Check its output for details."
    #     echo "Script will attempt to continue with start.sh."
    #     echo ""
    #     sleep 5
    # fi
else
    echo "Warning: setup.sh not found in $REPO_DIR. Skipping setup."
    sleep 5
fi


echo "Running start.sh..."
# Make start.sh executable if it's not already
if [ -f "start.sh" ]; then
    chmod +x start.sh
    # Execute the start script
    ./start.sh
    # Check if start.sh was successful (set -e handles this)
    # if [ $? -ne 0 ]; then
    #     echo ""
    #     echo "WARNING: start.sh reported an error. Check its output for details."
    #     echo ""
    #     sleep 5
    # fi
else
    echo "Warning: start.sh not found in $REPO_DIR. Skipping start."
    sleep 5
fi

echo "--- Script finished ---"

# Pause to keep the terminal window open
echo ""
read -p "Press Enter to finish..."

# Script exits with the status of the last command (or exits early due to set -e)
