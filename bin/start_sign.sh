#!/bin/bash

set -o errexit
#set -x

cd /home/krnl/krnl-sign

git pull

sudo python3 -m pip install -e .

sudo python3 -m krnl_sign

exit 0