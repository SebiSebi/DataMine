#!/bin/bash

pyv=$(python -c 'import sys; print(sys.version_info.major)' | sed 's/ *$//g')
if [ "$pyv" = "3" ]; then
	green -vvv --run-coverage tests/
else
	nosetests --verbosity=2
fi
