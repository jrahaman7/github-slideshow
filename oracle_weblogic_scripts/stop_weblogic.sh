#!/bin/bash
echo "Stopping WebLogic Server..."
if [ -f "./weblogic.pid" ]; then
  rm ./weblogic.pid
  echo "WebLogic Server stopped successfully."
else
  echo "WebLogic Server is not running."
fi
exit 0
