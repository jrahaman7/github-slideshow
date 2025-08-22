#!/bin/bash
if [ -f "./oracle.pid" ]; then
  echo "Oracle Database is running."
  exit 0
else
  echo "Oracle Database is not running."
  exit 1
fi
