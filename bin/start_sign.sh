#!/bin/bash

set -o errexit
#set -x

cd /home/krnl/krnl-sign
sudo python3 -m krnl_sign.startup

sudo python3 -m krnl_sign

exit 0