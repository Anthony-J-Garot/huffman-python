#!/bin/bash

# pylint runner script
#
# See .pylintrc for exceptions. This was generated using:
#    $ pylint --generate-rcfile > .pylintrc

PYLINT=/usr/local/bin/pylint
PYLINT_OPTS="-j 0 -v -f colorized"
SRC=./src
TESTS=./src/tests
# This gets rid of the myriad import-error messages
export PYTHONPATH=$SRC

# First argument is the directory on which to run pylint
run_pylint() {
    ON_DIR="$1"

	# Default to the SRC directory, which contains the tests, so ignore those
    if [[ "$ON_DIR" == "" ]]; then
        ON_DIR=$SRC
		PYLINT_OPTS="$PYLINT_OPTS --ignore=tests"
    fi

    echo "Running pylint on [$ON_DIR]"

    $PYLINT $PYLINT_OPTS $(find "$ON_DIR" -name "*.py")
}

# ------- Begin code ---------------------------------------------------------

if [[ ! -f $PYLINT ]]; then
    echo "pylint not found."
    exit 1
fi

clear

case "$1" in
src)
    run_pylint "$SRC"
    ;;
tests)
    run_pylint "$TESTS"
    ;;
*)
    run_pylint
    ;;
esac
