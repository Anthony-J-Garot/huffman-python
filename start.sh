#!/bin/bash

PYTHON=$(which python3)
MAIN="main.py"

# ------------------------- start code -----------------------------------

if [[ "$PYTHON" == "" ]]; then
    echo "Could not find python interpreter"
    exit 1
fi

$PYTHON $MAIN

