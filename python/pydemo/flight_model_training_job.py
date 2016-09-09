from __future__ import print_function

import sys

from pyspark import Row
from pyspark import SparkContext
from pyspark.mllib.tree import DecisionTree
from pyspark.sql import SQLContext

from util.commons import IE_FORMAT, Utils


def save_mapping(mapping, name, sqlc):
    to_save = []
    for k, v in mapping.iteritems():
        to_save.append(Row(key=k, integer_value=v))
    df = sqlc.createDataFrame(to_save)
    df.write.format(IE_FORMAT).mode("overwrite").save(name)


if __name__ == "__main__":
    sc = SparkContext(appName="InsightEdge Python API example: train model")
    sqlc = SQLContext(sc)

    text_rdd = sc.textFile("/code/insightedge-pyhton-demo/data/flights_jan_2014.csv")
    all_flights_rdd = text_rdd.map(lambda r: Utils.parse_flight(r))

    # TODO broadcast variables
    carrier_mapping = dict(all_flights_rdd.map(lambda flight: flight.carrier).distinct().zipWithIndex().collect())
    origin_mapping = dict(all_flights_rdd.map(lambda flight: flight.origin).distinct().zipWithIndex().collect())
    destination_mapping = dict(all_flights_rdd.map(lambda flight: flight.destination).distinct().zipWithIndex().collect())

    categorical_features_info = {0: 31,
                                 1: 7,
                                 4: len(carrier_mapping),
                                 6: len(origin_mapping),
                                 7: len(destination_mapping)}

    splits = text_rdd.randomSplit([0.7, 0.3])
    (training_rdd, test_rdd) = (splits[0], splits[1])
    training_data = training_rdd.map(Utils.parse_flight).map(lambda rdd: Utils.create_labeled_point(rdd, carrier_mapping, origin_mapping, destination_mapping))

    classes_count = 2
    impurity = "gini"
    max_depth = 9
    max_bins = 7000
    model = DecisionTree.trainClassifier(training_data, classes_count, categorical_features_info,
                                         impurity, max_depth, max_bins)

    Utils.save_model_to_grid(model, sc)
    save_mapping(carrier_mapping, "CarrierMap", sqlc)
    save_mapping(origin_mapping, "OriginMap", sqlc)
    save_mapping(destination_mapping, "DestinationMap", sqlc)

    # Test model
    test_data = test_rdd.map(lambda r: Utils.parse_flight(r)) \
        .map(lambda rdd: Utils.create_labeled_point(rdd, carrier_mapping, origin_mapping, destination_mapping))
    predictions = model.predict(test_data.map(lambda x: x.features))
    labelsAndPredictions = test_data.map(lambda lp: lp.label).zip(predictions)
    testErr = float(labelsAndPredictions.filter(lambda x: x[0] != x[1]).count()) / test_data.count()
    print("Test Error = {0}".format(testErr))

    # Save test data
    test_data_output = sys.argv[1]
    test_data.coalesce(1, True).saveAsTextFile(test_data_output)