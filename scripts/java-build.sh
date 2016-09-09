#!/usr/bin/env bash

echo "-- Building java helper jar"
PYTHON_DEMO_HOME=$(dirname "$0")

pushd $PYTHON_DEMO_HOME/..

cd ./java
mvn clean package

popd


