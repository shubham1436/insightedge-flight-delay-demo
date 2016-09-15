from pyspark import Row
from pyspark import SparkContext
from pyspark.mllib.tree import DecisionTreeModel
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from util.commons import IE_FORMAT, Utils


def load_mapping(mapping_name, sqlc):
    df = sqlc.read.format(IE_FORMAT).option("collection", mapping_name).load()
    return dict(df.map(lambda row: (row.key, row.integer_value)).collect())


def predict_and_save(rdd):
    try:
        if not rdd.isEmpty():
            parsed_flights = rdd.map(Utils.parse_grid_flight)
            labeled_points = parsed_flights.map(lambda flight: Utils.create_labeled_point(flight,
                                                                                          carrier_mapping.value,
                                                                                          origin_mapping.value,
                                                                                          destination_mapping.value))

            predictions = model.predict(labeled_points.map(lambda x: x.features))
            labels_and_predictions = labeled_points.map(lambda lp: lp.label).zip(predictions).zip(parsed_flights).map(to_row())

            df = sqlc.createDataFrame(labels_and_predictions)
            df.write.format(IE_FORMAT).mode("append").save("FlightWithPrediction")
    except:
        print("Could not process rdd")


def to_row():
    return lambda t: Row(actual=t[0][0],
                         prediction=t[0][1],
                         row_id=long(t[1].row_id),
                         streamed=t[1].streamed,
                         day_of_month=t[1].day_of_month,
                         day_of_week=t[1].day_of_week,
                         carrier=t[1].carrier,
                         tail_number=t[1].tail_number,
                         flight_number=t[1].flight_number,
                         origin_id=t[1].origin_id,
                         origin=t[1].origin,
                         destination_id=t[1].destination_id,
                         destination=t[1].destination,
                         scheduled_departure_time=t[1].scheduled_departure_time,
                         actual_departure_time=t[1].actual_departure_time,
                         departure_delay_minutes=t[1].departure_delay_minutes,
                         scheduled_arrival_time=t[1].scheduled_arrival_time,
                         actual_arrival_time=t[1].actual_arrival_time,
                         arrival_delay_minutes=t[1].arrival_delay_minutes,
                         crs_elapsed_flight_minutes=t[1].crs_elapsed_flight_minutes,
                         distance=t[1].distance)


if __name__ == "__main__":
    sc = SparkContext(appName="InsightEdge Python API Demo: prediction job")
    ssc = StreamingContext(sc, 3)
    sqlc = SQLContext(sc)

    zkQuorum = "localhost:2181"
    topic = "flights"

    model = DecisionTreeModel(Utils.load_model_from_grid("DecisionTreeFlightModel", sc))

    carrier_mapping = sc.broadcast(load_mapping("CarrierMap", sqlc))
    origin_mapping = sc.broadcast(load_mapping("OriginMap", sqlc))
    destination_mapping = sc.broadcast(load_mapping("DestinationMap", sqlc))

    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    lines.foreachRDD(predict_and_save)

    ssc.start()
    ssc.awaitTermination()
