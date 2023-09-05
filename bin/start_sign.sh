#!/bin/bash

set -o errexit
#set -x

cd /home/krnl/krnl-sign

# do we have internet?
function checkInternet {
    curl -s --head  --request GET https://www.google.com | grep "200" > /dev/null
}

# wait for internet
while ! checkInternet; do
    sleep 5
done

git pull

sudo python3 -m pip install -e .

sudo python3 -m krnl_sign

exit 0