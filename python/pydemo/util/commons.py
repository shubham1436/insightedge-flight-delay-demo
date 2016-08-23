from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors


IE_FORMAT = "org.apache.spark.sql.insightedge"
DF_SUFFIX = "org.insightedge.pythondemo"


class Flight(object):
    def __init__(self, day_of_month, day_of_week, carrier, tail_number, flight_number, origin_id, origin, destination_id, destination, scheduled_departure_time, actual_departure_time,
                 departure_delay_minutes, scheduled_arrival_time, actual_arrival_time, arrival_delay_minutes, crs_elapsed_flight_minutes, distance):
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.carrier = carrier
        self.tail_number = tail_number
        self.flight_number = flight_number
        self.origin_id = origin_id
        self.origin = origin
        self.destination_id = destination_id
        self.destination = destination
        self.scheduled_departure_time = scheduled_departure_time
        self.actual_departure_time = actual_departure_time
        self.departure_delay_minutes = departure_delay_minutes
        self.scheduled_arrival_time = scheduled_arrival_time
        self.actual_arrival_time = actual_arrival_time
        self.arrival_delay_minutes = arrival_delay_minutes
        self.crs_elapsed_flight_minutes = crs_elapsed_flight_minutes
        self.distance = distance

class Utils(object):
    @staticmethod
    def parse_flight(data):
        line = data.split(',')
        return Flight(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16])

    @staticmethod
    def create_labeled_point(flight, carrier_mapping, origin_mapping, destination_mapping):
        day_of_month = int(flight.day_of_month) - 1
        day_of_week = int(flight.day_of_week) - 1
        scheduled_departure_time = int(flight.scheduled_departure_time)
        scheduled_arrival_time = int(flight.scheduled_arrival_time)
        carrier = carrier_mapping[flight.carrier]
        crs_elapsed_flight_minutes = float(flight.crs_elapsed_flight_minutes)
        origin = origin_mapping[flight.origin]
        destination = destination_mapping[flight.destination]
        if int(flight.departure_delay_minutes) > 40:
            delayed = 1.0
        else:
            delayed = 0.0

        return LabeledPoint(delayed, Vectors.dense(day_of_month, day_of_week, scheduled_departure_time, scheduled_arrival_time, carrier, crs_elapsed_flight_minutes, origin, destination))

    @staticmethod
    def save_model_to_grid(model, sc):
        python_context = sc._jvm.java.lang.Thread.currentThread().getContextClassLoader().loadClass("org.insightedge.pythondemo.PythonInsightEdgeSparkContext").newInstance()
        python_context.init(sc._jsc)
        python_context.saveMlInstance(DF_SUFFIX + ".DecisionTreeFlightModel", model._java_model)


    @staticmethod
    def load_model_from_grid(sc):
        python_context = sc._jvm.java.lang.Thread.currentThread().getContextClassLoader().loadClass("org.insightedge.pythondemo.PythonInsightEdgeSparkContext").newInstance()
        python_context.init(sc._jsc)
        return python_context.loadMlInstance(DF_SUFFIX + ".DecisionTreeFlightModel", "org.apache.spark.mllib.tree.model.DecisionTreeModel")
