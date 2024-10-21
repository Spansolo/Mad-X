#!/bin/bash

user=${1:-vagrant}
shift
cmd=${*:-/bin/bash}

echo "executing command \"$cmd\" in zgoubi container as user \"$user\"..."
docker exec -it -u "$user" zgoubi $cmd
echo "executing command \"$cmd\" in zgoubi container as user \"$user\"... done"
