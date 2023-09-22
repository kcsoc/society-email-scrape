#!/bin/sh

# Function to activate virtual environment or create it if not exists
activate_virtualenv() {
    if [ ! -d "./env" ]; then
        python3 -m venv env || {
            echo "Error: Unable to create virtual environment."
            exit 1
        }
    fi

    source ./env/bin/activate || {
        echo "Error: Unable to activate virtual environment."
        exit 1
    }

    pip3 install -r requirements.txt || {
        echo "Error: Unable to install requirements in the virtual environment."
        exit 1
    }
}

# Main script

echo "Starting the script..."

# Activate the virtual environment
activate_virtualenv

# Process universities from unis.yml in parallel
while read line; do
    university_name="${line%%:*}"
    university_url="${line#*:}"

    (
        echo "Processing $university_name..."
        python main.py "$university_url" > "docs/output/$university_name.csv" && 
        echo "Completed $university_name."
    ) &
done < unis.yml

# Wait for all background processes to finish
wait

# Deactivate the virtual environment
deactivate || echo "Warning: Could not deactivate the virtual environment."

echo "Script completed."
