# insightedge-python-demo

Python API demo: real time flights delay prediction

### Running demo
Before running the demo you need to install [Maven](http://www.scala-sbt.org/) and [Sbt](http://www.scala-sbt.org/).

#### TODO Need to install [Numpy](http://www.numpy.org/)???

1. Set INSIGHTEDGE_HOME and KAFKA_HOME env vars
```bash
export INSIGHTEDGE_HOME="path/to/insightedge"
export KAFKA_HOME="path/to/kafka"
```
2. Install InsightEdge into maven repo `$INSIGHTEDGE_HOME/sbin/insightedge-maven.sh`

3. Launch InsightEdge `$INSIGHTEDGE_HOME/sbin/insightedge.sh --mode demo`

4. Launch Kafka with `./scripts/kafka-start.sh`

5. Submit model training job `./scripts/spark-model-training-job.sh`

6. Submit flight delay prediction job `./scripts/spark-flight-delay-prediction-job.sh`. Please note that this is endless job.

7. In separate terminal tab submit data to Kafka topic `./scripts/kafka-submit-data.sh`. In the console you will see rows which were sent to the Kafka topic.

8. Run web application `sbt web/run`

9. Investigate results in Zeppelin(http://127.0.0.1:8090) and in web app(http://localhost:9000)

- To shutdown InsightEdge run `$INSIGHTEDGE_HOME/sbin/insightedge.sh --mode shutdown`
- To shutdown Kafka run `./scripts/kafka-stop.sh`
- To stop prediction Spark job `./scripts/spark-stop-prediction-job.sh`