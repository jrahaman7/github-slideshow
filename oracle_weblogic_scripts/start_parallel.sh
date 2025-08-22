#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Function to handle errors and prompt the user
handle_error() {
    local service_name=$1
    echo "Error: $service_name failed to start."
    while true; do
        read -p "Continue with error? (Y/N): " choice
        case "$choice" in
            [Yy]* ) echo "Continuing with errors..."; return 0;;
            [Nn]* ) echo "Exiting."; exit 1;;
            * ) echo "Please answer Y or N.";;
        esac
    done
}

# --- Start services in parallel ---
echo "--- Starting services in parallel... ---"
./start_oracle.sh &
./start_weblogic.sh &

# Wait for all background jobs to finish
wait

# --- Check Oracle status ---
./check_oracle_status.sh
if [ $? -ne 0 ]; then
    handle_error "Oracle Database"
fi

# --- Check WebLogic status ---
./check_weblogic_status.sh
if [ $? -ne 0 ]; then
    handle_error "WebLogic Server"
fi

echo "--- Parallel startup process complete. ---"
exit 0
