package model

/**
  * @author Danylo_Hurin.
  */
case class SubmittedFlight(
                            rowId: String,
                            dayOfMonth: String,
                            dayOfWeek: String,
                            carrier: String,
                            origin: String,
                            destination: String,
                            scheduledDepartureTime: String,
                            scheduledArrivalTime: String,
                            crsElapsedFlightMinutes: String
                          )
