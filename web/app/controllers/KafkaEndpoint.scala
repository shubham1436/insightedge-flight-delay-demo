package controllers

import java.util.Properties

import kafka.producer.{KeyedMessage, Producer, ProducerConfig}
import model.{FlightEvent, ShortFlight, SubmittedFlight}
import play.api.libs.json._
import play.api.mvc._

object KafkaEndpoint extends Controller {

  implicit val flightsReader = Json.reads[ShortFlight]
  implicit val submittedFlightsReader = Json.reads[SubmittedFlight]

  def submitFlight = Action(parse.json) { request =>
    parseJson(request) { flight: SubmittedFlight =>
      val rowId = flight.rowId.toLong
      val event = FlightEvent(
        rowId,
        flight.dayOfMonth,
        flight.dayOfWeek,
        flight.carrier,
        flight.origin,
        flight.destination,
        flight.scheduledDepartureTime,
        flight.scheduledArrivalTime,
        flight.crsElapsedFlightMinutes
      )
      send(event.toString(), "flights")
      Created(rowId.toString)
    }
  }

  private def parseJson[R](request: Request[JsValue])(block: R => Result)(implicit reads: Reads[R]): Result = {
    request.body.validate[R](reads).fold(
      valid = block,
      invalid = e => {
        val error = e.mkString
        BadRequest(error)
      }
    )
  }

  // hardcoded to simplify the demo code
  lazy val kafkaConfig = {
    val props = new Properties()
    props.put("metadata.broker.list", "localhost:9092")
    props.put("serializer.class", "kafka.serializer.StringEncoder")
    props
  }
  lazy val producer = new Producer[String, String](new ProducerConfig(kafkaConfig))

  private def send(message: String, topic: String) = producer.send(new KeyedMessage[String, String](topic, message))


}