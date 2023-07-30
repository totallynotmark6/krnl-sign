#!/bin/bash

set -o errexit
#set -x

cd /home/krnl/krnl-sign
git pull || true

sudo python3 -m krnl_sign

exit 0