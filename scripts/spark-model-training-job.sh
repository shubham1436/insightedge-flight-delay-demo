#!/usr/bin/env bash

./scripts/java-build.sh

./scripts/python-zip-utils.sh

echo "-- Submitting model training Spark job"
$INSIGHTEDGE_HOME/bin/insightedge-submit \
   --conf spark.insightedge.space.name=insightedge-space \
   --conf spark.insightedge.space.lookup.group=insightedge \
   --conf spark.insightedge.space.lookup.locator=127.0.0.1:4174 \
   --jars ./java/target/java-pyhton-context-1.0-SNAPSHOT.jar \
   --py-files ./python/pydemo/util.zip \
   ./python/pydemo/flight_model_training_job.py
echo "-- Done."
