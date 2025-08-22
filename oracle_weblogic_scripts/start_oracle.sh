#!/bin/bash
echo "Starting Oracle Database..."
# Simulate a startup process that takes a few seconds
sleep 3
# Create a PID file to signify the service is "running"
touch ./oracle.pid
echo "Oracle Database started successfully."
exit 0
