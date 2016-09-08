package controllers

import com.gigaspaces.document.SpaceDocument
import com.j_spaces.core.client.SQLQuery
import model.ShortFlight
import org.openspaces.core.GigaSpaceConfigurer
import org.openspaces.core.space.SpaceProxyConfigurer
import play.api.libs.json._
import play.api.mvc._

object FlightEndpoint extends Controller {

  implicit val orderStatusWrites = new Writes[ShortFlight] {
    override def writes(f: ShortFlight): JsValue = JsString(f.getClass.getSimpleName)
  }

  val flightsWriter = Json.writes[ShortFlight]
  val flightsListWriter = Writes.list[ShortFlight](flightsWriter)

  val grid = {
    val spaceConfigurer = new SpaceProxyConfigurer("insightedge-space").lookupGroups("insightedge").lookupLocators("127.0.0.1:4174")
    new GigaSpaceConfigurer(spaceConfigurer).create()
  }

  def getLastFlights(streamedRowId: String, submittedRowId: String) = Action { implicit request =>
    val streamedQuery = new SQLQuery[SpaceDocument]("FlightWithPrediction", "(row_id > ? AND streamed = ?) OR (row_id > ? AND streamed = ?)")
    streamedQuery.setParameter(1, streamedRowId)
    streamedQuery.setParameter(2, "1")
    streamedQuery.setParameter(3, submittedRowId)
    streamedQuery.setParameter(4, "0")
    val streamedFlights = grid.readMultiple(streamedQuery).map { sd =>
      ShortFlight(
        sd.getProperty[Long]("row_id"),
        sd.getProperty[String]("streamed"),
        sd.getProperty[String]("day_of_month"),
        sd.getProperty[String]("day_of_week"),
        sd.getProperty[String]("carrier"),
        sd.getProperty[String]("origin"),
        sd.getProperty[String]("destination"),
        sd.getProperty[String]("scheduled_departure_time"),
        sd.getProperty[String]("departure_delay_minutes"),
        sd.getProperty[String]("scheduled_arrival_time"),
        sd.getProperty[String]("crs_elapsed_flight_minutes"),
        sd.getProperty[Double]("prediction")
      )
    }.toList

    Ok(Json.toJson(streamedFlights)(flightsListWriter))
  }
}