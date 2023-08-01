#!/bin/bash

PYTHON=$(which python3)
SRC_DIR="src/"
MAIN="main.py"

# ------------------------- start code -----------------------------------

if [[ "$PYTHON" == "" ]]; then
    echo "Could not find python interpreter"
    exit 1
fi

{
    cd "$SRC_DIR" || exit 1

    $PYTHON $MAIN
}

