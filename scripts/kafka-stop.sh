#!/usr/bin/env bash

source ./scripts/kill-process.sh

grepKill ZooKeeper config/zookeeper.properties
grepKill Kafka config/server.properties
echo "-- Done."