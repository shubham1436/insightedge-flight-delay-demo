from __future__ import print_function

from pyspark import Row
from pyspark import SparkContext
from pyspark.mllib.tree import DecisionTree
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext

from util.commons import DF_SUFFIX, IE_FORMAT, Utils


def save_mapping(mapping, name, sqlc):
    to_save = []
    for k, v in mapping.iteritems():
        to_save.append(Row(key=k, integer_value=v))
    df = sqlc.createDataFrame(to_save)
    df.write.format(IE_FORMAT).mode("overwrite").save(name)


if __name__ == "__main__":
    sc = SparkContext(appName="Insightedge Python API example: train model")
    ssc = StreamingContext(sc, 3)
    sqlc = SQLContext(sc)

    text_rdd = sc.textFile("/code/insightedge-pyhton-demo/data/rita2014jan.csv")
    all_flights_rdd = text_rdd.map(lambda r: Utils.parse_flight(r))

    carrier_mapping = dict(all_flights_rdd.map(lambda flight: flight.carrier).distinct().zipWithIndex().collect())
    origin_mapping = dict(all_flights_rdd.map(lambda flight: flight.origin).distinct().zipWithIndex().collect())
    destination_mapping = dict(all_flights_rdd.map(lambda flight: flight.destination).distinct().zipWithIndex().collect())

    categorical_features_info = {0: 31,
                                 1: 7,
                                 4: len(carrier_mapping),
                                 6: len(origin_mapping),
                                 7: len(destination_mapping)}

    splits = text_rdd.randomSplit([0.7, 0.3])
    (text_rdd70, text_rdd30) = (splits[0], splits[1])
    training_data = text_rdd70.map(lambda r: Utils.parse_flight(r))\
        .map(lambda rdd: Utils.create_labeled_point(rdd, carrier_mapping, origin_mapping, destination_mapping))

    classes_count = 2
    impurity = "gini"
    max_depth = 9
    max_bins = 1000 #7000
    model = DecisionTree.trainClassifier(training_data, classes_count, categorical_features_info,
                                         impurity, max_depth, max_bins)

    Utils.save_model_to_grid(model, sc)
    save_mapping(carrier_mapping, DF_SUFFIX + ".CarrierMap", sqlc)
    save_mapping(origin_mapping, DF_SUFFIX + ".OriginMap", sqlc)
    save_mapping(destination_mapping, DF_SUFFIX + ".DestinationMap", sqlc)

    # Test model
    test_data = text_rdd30.map(lambda r: Utils.parse_flight(r))\
        .map(lambda rdd: Utils.create_labeled_point(rdd, carrier_mapping, origin_mapping, destination_mapping))
    predictions = model.predict(test_data.map(lambda x: x.features))
    labelsAndPredictions = test_data.map(lambda lp: lp.label).zip(predictions)
    testErr = float(labelsAndPredictions.filter(lambda x: x[0] != x[1]).count()) / test_data.count()
    #print(model.toDebugString())
    print("Test Error = {0}".format(testErr))

    # Save test data
    #test_data.coalesce(1, True).saveAsTextFile("/code/insightedge-pyhton-demo/data/testData3")

    # Save parsed data for testing
    # def flattern(p):
    #     l = p.features.toArray().tolist()
    #     l.insert(0, p.label)
    #     return ", ".join(str(e) for e in l)
    #
    # testData.map(lambda p: flattern(p)).coalesce(1, True).saveAsTextFile("/code/insightedge-pyhton-demo/data/testData2")

    # Previous
    # mldata85, mldata15 = mldata.filter(lambda x: x.label == 0.0).randomSplit([0.85, 0.15])
    # mldata1 = mldata.filter(lambda x: x.label != 0.0)
    # mldata2 = mldata15 + mldata1
    # splits = mldata.randomSplit([0.7, 0.3])
    #(trainingData, testData) = (splits[0], splits[1])

# def save_mapping(carrier_map, origin_map, destination_map, sqlc):
#     carriers = []
#     for k, v in carrier_map.iteritems():
#         carriers.append(Row(key=k, integer_value=v))
#     carrier_df = sqlc.createDataFrame(carriers)
#     carrier_df.write.format(IE_FORMAT).mode("overwrite").save(DF_SUFFIX + ".CarrierMap")
#
#     origins = []
#     for k, v in origin_map.iteritems():
#         origins.append(Row(key=k, integer_value=v))
#     origin_df = sqlc.createDataFrame(origins)
#     origin_df.write.format(IE_FORMAT).mode("overwrite").save(DF_SUFFIX + ".OriginMap")
#
#     destinations = []
#     for k, v in destination_map.iteritems():
#         destinations.append(Row(key=k, integer_value=v))
#     destination_df = sqlc.createDataFrame(destinations)
#     destination_df.write.format(IE_FORMAT).mode("overwrite").save(DF_SUFFIX + ".DestinationMap")
