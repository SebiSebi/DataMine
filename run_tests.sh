#!/bin/bash

pyv=$(python -c 'import sys; print(sys.version_info.major)' | sed 's/ *$//g')
echo "Running tests for Python major version: ${pyv}"
green -vvv --run-coverage tests/
