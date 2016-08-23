#!/usr/bin/env bash

/home/dgurin/Downloads/gigaspaces-insightedge-1.0.0-premium/bin/insightedge-submit \
   --conf spark.insightedge.space.name=insightedge-space \
   --conf spark.insightedge.space.lookup.group=insightedge \
   --conf spark.insightedge.space.lookup.locator=127.0.0.1:4174 \
   --jars /code/insightedge-pyhton-demo/java/target/java-pyhton-context-1.0-SNAPSHOT.jar \
   --py-files /code/insightedge-pyhton-demo/python/pydemo/util.zip \
   /code/insightedge-pyhton-demo/python/pydemo/flight_model_training_job.py
