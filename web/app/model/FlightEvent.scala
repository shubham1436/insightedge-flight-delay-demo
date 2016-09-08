package model

/**
  * @author Danylo_Hurin.
  */
case class FlightEvent(
                       rowId: Long,
                       dayOfMonth: String,
                       dayOfWeek: String,
                       carrier: String,
                       origin: String,
                       destination: String,
                       scheduledDepartureTime: String,
                       scheduledArrivalTime: String,
                       crsElapsedFlightMinutes: String
                      ) {
  override def toString: String = {
    s"$rowId," +
      s"0," + //streamed
      s"$dayOfMonth," +
      s"$dayOfWeek," +
      s"$carrier," +
      s"," + //tailNumber
      s"," + //flightNumber
      s"," + //originId
      s"$origin," +
      s"," + //desctinationId
      s"$destination," +
      s"$scheduledDepartureTime," +
      s"," + //actual_departure_time
      s"-1," + //departure_delay_minutes
      s"$scheduledArrivalTime," +
      s"," + //actual_arrival_time
      s"," + //arrival_delay_minutes
      s"$crsElapsedFlightMinutes," +
      s"" //distance
  }

}
