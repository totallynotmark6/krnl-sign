#!/bin/bash

set -o errexit
#set -x

cd "$(dirname $0)"
BIN_DIR="${PWD}"
PROG_DIR="${BIN_DIR%/*}"
TOP_DIR="${PROG_DIR%/*}"

sudo python3 -m krnl_sign

exit 0