#!/bin/bash
# --- Script to activate virtual environment and run Python script ---

echo "Activating the virtual environment..."

# Check if the activate script exists
if [ ! -f venv/bin/activate ]; then
    echo "Error: Virtual environment 'venv' not found or 'venv/bin/activate' is missing."
    echo "Please create the virtual environment first (e.g., python -m venv venv)."
    # Exit with an error code
    exit 1
fi

# Activate the virtual environment
# Use 'source' or '.' to run the activate script in the current shell context
source venv/bin/activate

# Check if activation was successful (optional, activate script usually handles errors)
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate the virtual environment."
    exit 1
fi

echo "Virtual environment activated."
echo "Running the Python script 'main.py'..."

# Execute the Python script
python main.py

# Store the exit status of the python command
PYTHON_EXIT_STATUS=$?

echo "Python script finished."

# --- Pause to keep the terminal window open ---
# This mimics the 'pause' behavior of the Windows script.
# Useful if you double-click the script in a GUI file manager.
# If running from an already open terminal, this might not be necessary.
echo ""
read -p "Press Enter to finish..."

# Exit with the same status code as the python script
exit $PYTHON_EXIT_STATUS