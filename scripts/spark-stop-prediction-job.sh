#!/usr/bin/env bash

source ./scripts/kill-process.sh

grepKill "InsightEdge Spark prediction job" "insightedge_flight_prediction_python"
echo "-- Done."