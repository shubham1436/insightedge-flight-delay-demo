package model

import com.gigaspaces.document.SpaceDocument

/**
  * @author Danylo_Hurin.
  */
case class ShortFlight(
                        rowId: Long,
                        streamed: String,
                        dayOfMonth: String,
                        dayOfWeek: String,
                        carrier: String,
                        origin: String,
                        destination: String,
                        scheduledDepartureTime: String,
                        departureDelayMinutes: String,
                        scheduledArrivalTime: String,
                        crsElapsedFlightMinutes: String,
                        prediction: Double
                      )

//
//object ShortFlight {
//
//  def apply(sd: SpaceDocument): ShortFlight = {
//    ShortFlight(
//      sd.getProperty[String]("number"),
//      sd.getProperty[String]("streamed"),
//      sd.getProperty[String]("day_of_month"),
//      sd.getProperty[String]("day_of_week"),
//      sd.getProperty[String]("carrier"),
//      sd.getProperty[String]("origin"),
//      sd.getProperty[String]("destination"),
//      sd.getProperty[String]("scheduled_departure_time"),
//      sd.getProperty[String]("departure_delay_minutes"),
//      sd.getProperty[String]("scheduled_arrival_time"),
//      sd.getProperty[String]("crs_elapsed_flight_minutes"),
//      sd.getProperty[String]("prediction")
//    )
//  }
//}