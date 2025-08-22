#!/bin/bash
echo "Stopping Oracle Database..."
if [ -f "./oracle.pid" ]; then
  rm ./oracle.pid
  echo "Oracle Database stopped successfully."
else
  echo "Oracle Database is not running."
fi
exit 0
