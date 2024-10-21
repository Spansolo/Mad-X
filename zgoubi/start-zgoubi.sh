#!/bin/bash

echo "starting zgoubi..."
docker run --rm -d --name zgoubi -v "$PWD":/home/vagrant/src/radiasoft/zgoubi radiasoft/beamsim sleep 10000000
echo "starting zgoubi... done"
