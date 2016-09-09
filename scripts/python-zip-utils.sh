#!/usr/bin/env bash

echo "-- Zipping python utils"
PYTHON_DEMO_HOME=$(dirname "$0")

pushd $PYTHON_DEMO_HOME/..

cd ./python/pydemo
zip -r util.zip util

popd
