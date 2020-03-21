#!/bin/bash

PYTHONPATH=$PWD:$PYTHONPATH py.test --cov=./data_mine tests/
