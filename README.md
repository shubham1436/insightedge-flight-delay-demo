# insightedge-python-demo

Python API demo: real time flights delay prediction

### Running demo TODO 
 
1. Launch InsightEdge `./sbin/insightedge.sh --mode demo`

2. Launch Kafka with `./scripts/kafka-start.sh`

3. Submit model training job `./scripts/spark-model-training-job.sh`

4. Submit flight delay prediction job `./scripts/spark-flight-delay-prediction-job.sh`

5. Submit data to Kafka topic `./scripts/kafka-submit-data.sh`

6. Investigate results in Zeppelin: http://127.0.0.1:8090