#!/bin/bash
if [ -f "./weblogic.pid" ]; then
  echo "WebLogic Server is running."
  exit 0
else
  echo "WebLogic Server is not running."
  exit 1
fi
