#!/bin/bash

# API endpoint for posting the status
API_URL="http://api.example.com/db_status"

# File containing the list of hosts
HOST_FILE="host_list"

# Check if host file exists
if [ ! -f "$HOST_FILE" ]; then
    echo "Host file not found: $HOST_FILE"
    exit 1
fi

# Loop through each host in the host file
while IFS= read -r HOST; do
    echo "Checking database status on $HOST..."

    # Simulate a database check command via SSH.
    # In a real script, you would replace this with your actual db check command.
    # This example randomly returns "OK" or "FAIL".
    DB_STATUS=$(ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$HOST" "if (( RANDOM % 2 == 0 )); then echo 'OK'; else echo 'FAIL'; fi")

    # If SSH fails, we'll get an empty status.
    if [ -z "$DB_STATUS" ]; then
        DB_STATUS="CONNECTION_ERROR"
    fi

    echo "Status of $HOST: $DB_STATUS"

    # Post the status to the API
    echo "Posting status to API..."
    curl -X POST -H "Content-Type: application/json" -d "{\"hostname\": \"$HOST\", \"status\": \"$DB_STATUS\"}" "$API_URL"
    echo -e "\n---------------------"

done < "$HOST_FILE"

echo "Database status check script finished."
