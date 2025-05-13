#!/bin/bash
# --- Script to update the current Git repository ---

echo "Updating the current Git repository..."

# Optional: Navigate to the script's directory
# This ensures the script runs within the directory it's located in.
# Uncomment the following two lines if you place the script in the repo root
# and want it to automatically navigate there before running git pull.
# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# cd "$SCRIPT_DIR"


# Perform the git pull command
# The '-v' flag provides verbose output, which is often helpful.
git pull -v

# Check the exit code of the git pull command
if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred during the git pull operation."
    echo "Please check the output above for details."
    # You might want to exit with a non-zero status in case of error
    # exit 1
else
    echo ""
    echo "Git pull completed successfully."
fi

# --- Optional: Pause at the end ---
# Uncomment the following line if you want the script to wait for user input before the terminal closes
# (Useful if you're double-clicking the script in a GUI file manager and want to see the output)
# read -p "Press Enter to finish..."

# Exit successfully (optional, usually the default if no error occurred)
# exit 0