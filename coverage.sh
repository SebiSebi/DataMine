#!/bin/bash

pyv=$(python -c 'import sys; print(sys.version_info.major)' | sed 's/ *$//g')
if [ "$pyv" = "3" ]; then
	codecov
else
	echo "Coverage is not reported for Python 2"
fi
