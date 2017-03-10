from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors


IE_FORMAT = "org.apache.spark.sql.insightedge"


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

class Weather(object):
    def __init__(self, airport_id, year, month, day, time, timezone, skycondition, visibility, weather_type, dry_bulb_farenheit, dry_bulb_celsius, wet_bulb_farenheit, wet_bulb_celsius, dew_point_farenheit, dew_point_celsius, 
    relative_humidity, wind_speed, wind_direction, value_for_wind_character, station_pressure, pressure_tendency, pressure_change, sea_level_pressure, record_type, hourly_precip, altimeter):
        self.airport_id = airport_id
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.timezone = timezone
        self.skycondition = skycondition
        self.visibility = visibility
        self.weather_type = weather_type
        self.dry_bulb_farenheit = dry_bulb_farenheit
        self.dry_bulb_celsius = dry_bulb_celsius
        self.wet_bulb_farenheit = wet_bulb_farenheit
        self.wet_bulb_celsius = wet_bulb_celsius
        self.dew_point_farenheit = dew_point_farenheit
        self.dew_point_celsius = dew_point_celsius
        self.relative_humidity = relative_humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.value_for_wind_character = value_for_wind_character
        self.station_pressure = station_pressure
        self.pressure_tendency = pressure_tendency
        self.pressure_change = pressure_change
        self.sea_level_pressure = sea_level_pressure
        self.record_type = record_type
        self.hourly_precip = hourly_precip
        self.altimeter = altimeter


class GridFlight(Flight):
    def __init__(self, row_id, streamed, day_of_month, day_of_week, carrier, tail_number, flight_number, origin_id, origin, destination_id, destination, scheduled_departure_time, actual_departure_time,
                 departure_delay_minutes, scheduled_arrival_time, actual_arrival_time, arrival_delay_minutes, crs_elapsed_flight_minutes, distance, wind_speed):
        Flight.__init__(self, day_of_month, day_of_week, carrier, tail_number, flight_number, origin_id, origin, destination_id, destination, scheduled_departure_time, actual_departure_time,
                                     departure_delay_minutes, scheduled_arrival_time, actual_arrival_time, arrival_delay_minutes, crs_elapsed_flight_minutes, distance)
        self.row_id = row_id
        self.streamed = streamed
        self.wind_speed = wind_speed


class Utils(object):
    @staticmethod
    def parse_flight(data):
        line = data.split(',')
        return Flight(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16])

    @staticmethod
    def parse_weather(data):
        line = data.split(',')
        return Flight(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19], line[20], line[21], line[22], line[23], line[24], line[25])

    @staticmethod
    def parse_grid_flight(data):
        line = data.split(',')
        return GridFlight(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19])

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
        wind_speed = flight.wind_speed
        if int(flight.departure_delay_minutes) > 40:
            delayed = 1.0
        else:
            delayed = 0.0

        return LabeledPoint(delayed, Vectors.dense(day_of_month, day_of_week, scheduled_departure_time, scheduled_arrival_time, carrier, crs_elapsed_flight_minutes, origin, destination, wind_speed))

    @staticmethod
    def save_model_to_grid(model, name, sc):
        python_context = sc._jvm.java.lang.Thread.currentThread().getContextClassLoader().loadClass("org.insightedge.pythondemo.PythonInsightEdgeSparkContext").newInstance()
        python_context.init(sc._jsc)
        python_context.saveMlInstance(name, model._java_model)


    @staticmethod
    def load_model_from_grid(name, sc):
        python_context = sc._jvm.java.lang.Thread.currentThread().getContextClassLoader().loadClass("org.insightedge.pythondemo.PythonInsightEdgeSparkContext").newInstance()
        python_context.init(sc._jsc)
        return python_context.loadMlInstance(name, "org.apache.spark.mllib.tree.model.DecisionTreeModel")
