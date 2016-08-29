
### Intro & Use case
In this post we will show how to you can use InsightEdge to do a real time prediction for flights delay.
We will create a solution based on a decision tree algorithm described by Carol McDonald in her MapR [blog post](https://www.mapr.com/blog/apache-spark-machine-learning-tutorial).
 
Why would you do a flight delay prediction?
For clients it gives a more accurate expectation about flight time thus gives an ability to plan their time accordingly.
For airlines companies it shows where they can minimize flight delays thereby minimize expenses and increase customers satisfaction.  

Building solution on top of the InsightEdge allows it to be distributed and easy scalable...

### Architecture

The following slide shows us one the possible solutions which suits for our task.

![Architecture](img/architecture.png)

For the hardest part, prediction, we are going to use Spark Machine Learning technology.
For performing real time predictions we are going to se Spark Streaming technology combined with Apache Kafka which will simulate endless and continuous data flow.
Streamed data will be processed by decision tree model and results are saved into Data Grid for future usage.

The solution consist from two parts(Spark jobs):
- Model training
- Flight delay prediction

Let's see jobs in details. All code is available on [github](https://github.com/InsightEdge/insightedge-python-demo)

#### 'Model training' Spark job

Model training job is one-time job which designed to do model initial training and store it in the InsightEdge data grid so the model can be used during the second job.
We won't drill deep in details of machine learning algorithms and decision tree model training, you can familiarize yourself with it in Carol McDonald's blog post mentioned earlier.

Job consists of next simple steps:

1. Load data and split it on training and testing part and save testing part for second job usage. We will use the same [data set](https://github.com/InsightEdge/insightedge-python-demo/blob/master/data/flights_jan_2014.csv) as in Carol McDonald's blog. 
```python

flight_data_file = ...
sc = SparkContext(appName="Flight prediction model training")

text_rdd = sc.textFile(flight_data_file)
splits = text_rdd.randomSplit([0.7, 0.3])
(training_rdd, test_rdd) = (splits[0], splits[1])
test_rdd.coalesce(1, True).saveAsTextFile(...)

```

2. During second job we will convert flight data into LabeledPoint. For this we will store integer representations of origin, destination and carrier in the data grid.
```python

all_flights_rdd = text_rdd.map(lambda r: Utils.parse_flight(r))

carrier_mapping = dict(all_flights_rdd.map(lambda flight: flight.carrier).distinct().zipWithIndex().collect())
origin_mapping = dict(all_flights_rdd.map(lambda flight: flight.origin).distinct().zipWithIndex().collect())
destination_mapping = dict(all_flights_rdd.map(lambda flight: flight.destination).distinct().zipWithIndex().collect())

sqlc = SQLContext(sc)
save_mapping(carrier_mapping, DF_SUFFIX + ".CarrierMap", sqlc)
save_mapping(origin_mapping, DF_SUFFIX + ".OriginMap", sqlc)
save_mapping(destination_mapping, DF_SUFFIX + ".DestinationMap", sqlc)

```

3. Train model and save it to the grid
```python

model = DecisionTree.trainClassifier(training_data, classes_count, categorical_features_info,
                                         impurity, max_depth, max_bins)
Utils.save_model_to_grid(model, sc)

```


#### 'Flight delay prediction' Spark job
Second Spark job will load model from the grid, read data from stream and use the model for prediction. Prediction results are stored in the grid alongside with flight data.
Load model and helper data from grid
Simple Kafka feeder
Open Kafka stream + use function for each rdd
Parse and prepare data  + predict
Save parsed data + prediction to grod


### Showing results

For data
Final data example

![Data example](img/data_example.png)

Correct predictions count VS Incorrect predictions count

![Prediction ratio](img/ratio_predictions.png)

### Next steps

1. Better model
2. Update model logic - Batch update
3. Update model logic - Iterative model
