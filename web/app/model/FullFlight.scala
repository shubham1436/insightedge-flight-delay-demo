package model

import com.gigaspaces.document.SpaceDocument


case class FullFlight(
                       number: String,
                       streamed: String,
                       dayOfMonth: String,
                       dayOfWeek: String,
                       carrier: String,
                       tailNumber: String,
                       flightNumber: String,
                       originId: String,
                       origin: String,
                       destinationId: String,
                       destination: String,
                       scheduledDepartureTime: String,
                       actualDepartureTime: String,
                       departureDelayMinutes: String,
                       scheduledArrivalTime: String,
                       actualArrivalTime: String,
                       arrivalDelayMinutes: String,
                       crsElapsedFlightMinutes: String,
                       distance: String,
                       prediction: String
                     )

object FullFlight {
  def apply(sd: SpaceDocument): FullFlight = {
    FullFlight(
      sd.getProperty[String]("number"),
      sd.getProperty[String]("streamed"),
      sd.getProperty[String]("day_of_month"),
      sd.getProperty[String]("day_of_week"),
      sd.getProperty[String]("carrier"),
      sd.getProperty[String]("tail_number"),
      sd.getProperty[String]("flight_number"),
      sd.getProperty[String]("origin"),
      sd.getProperty[String]("origin_id"),
      sd.getProperty[String]("destination_id"),
      sd.getProperty[String]("destination"),
      sd.getProperty[String]("scheduled_departure_time"),
      sd.getProperty[String]("actual_departure_time"),
      sd.getProperty[String]("departure_delay_minutes"),
      sd.getProperty[String]("scheduled_arrival_time"),
      sd.getProperty[String]("actual_arrival_time"),
      sd.getProperty[String]("arrival_delay_minutes"),
      sd.getProperty[String]("crs_elapsed_flight_minutes"),
      sd.getProperty[String]("distance"),
      sd.getProperty[String]("prediction")
    )
  }
}