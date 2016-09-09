#!/usr/bin/env bash

./scripts/python-zip-utils.sh

echo "-- Submitting prediction spark job"
LOGS=$INSIGHTEDGE_HOME/logs/python-demo-prediction.log
nohup $INSIGHTEDGE_HOME/bin/insightedge-submit \
   --name=insightedge_flight_prediction_python \
   --conf spark.insightedge.space.name=insightedge-space \
   --conf spark.insightedge.space.lookup.group=insightedge \
   --conf spark.insightedge.space.lookup.locator=127.0.0.1:4174 \
   --packages org.apache.spark:spark-streaming-kafka-assembly_2.10:1.6.0 \
   --jars ./java/target/java-pyhton-context-1.0-SNAPSHOT.jar \
   --py-files ./python/pydemo/util.zip \
   /code/insightedge-pyhton-demo/python/pydemo/flight_prediction_job.py > $LOGS 2>&1 &
echo "-- Waiting 5 seconds..."
sleep 5
echo "-- Job status: http://localhost:4040"
echo "-- Logs: $LOGS"
echo "-- Done."

