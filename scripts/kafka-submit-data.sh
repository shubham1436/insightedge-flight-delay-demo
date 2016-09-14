#!/usr/bin/env bash

#TODO as param
DELAY=2
TEST_DATA="./data/test/part-00000"

awk -v delay="$DELAY" '{ print NR ",1," $0; system("sleep "delay);}' $TEST_DATA | tee >($KAFKA_HOME/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic flights)