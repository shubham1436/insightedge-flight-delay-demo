$(function () {
    $.demo = {};
    $.demo.refreshRate = 2000;
    $.demo.submittedLastRowId = 0;
    $.demo.streamedLastRowId = 0;
});


if (window.console) {
  console.log("Welcome to your Play application's JavaScript!");
}

function getFlights() {
    var flights = jsRoutes.controllers.FlightEndpoint.getLastFlights($.demo.streamedLastRowId, $.demo.submittedLastRowId);
//    flights.ajax({
//        success: function(result) {
//            var res = result;
//            $("#streamedFlightsDiv").append("<div>" + res + "</div>");
//        },
//        failure: function(err) {
//            var errorText = 'There was an error';
//            $("#streamedFlightsSpan").text(errorText);
//        }
//    });

    $.getJSON(flights.url, function(data) {
        $.each(data, function(index, flight) {
//            $("#streamedFlightsDiv").append("<div>" + index + "</div>");
//            $("#streamedFlightsDiv").append("<div>" + flight.number + flight.streamed + flight.carrier + "</div>");
            var tableToInsert = ""
            if (flight.streamed == "1") {
                tableToInsert = "streamedFlightsTable"
                if (flight.rowId > $.demo.streamedLastRowId) {
                    $.demo.streamedLastRowId = flight.rowId
                }
            } else {
                tableToInsert = "submittedFlightsTable"
                if (flight.rowId > $.demo.streamedLastRowId) {
                    $.demo.submittedLastRowId = flight.rowId
                }
            }
            $('#'+tableToInsert+' tr:last').after('<tr><td>' + flight.rowId + '</td><td>' + flight.streamed + '</td><td>' + flight.origin + '</td><td>' + flight.destination + '</td><td>' + flight.departureDelayMinutes + '</td><td>' + flight.prediction + '</td></tr>');
        });
//        console.log("Last streamed: " + $.demo.streamedLastRowId);
//        console.log("Last submitted: " + $.demo.submittedLastRowId);
    })

    setTimeout(function() {getFlights();}, 2000);
}

function submitFlight() {
    var route = jsRoutes.controllers.KafkaEndpoint.submitFlight();
    var flightToSubmit = JSON.stringify({
                                         dayOfMonth: $('#mday').val(),
                                         dayOfWeek: $('#wday').val(),
                                         carrier: $('#carrier').val(),
                                         origin: $('#origin').val(),
                                         destination: $('#destination').val(),
                                         scheduledDepartureTime: $('#departureTime').val(),
                                         scheduledArrivalTime: $('#arrivalTime').val(),
                                         crsElapsedFlightMinutes: $('#crsFlightTime').val()
                                        });
    $.ajax({
        url: route.url,
        type: route.type,
        data: flightToSubmit,
        contentType: "application/json",
        success: function(newId) {console.log("Flight row id: " + newId);}
    });
    console.log("Flight was submitted: " + flightToSubmit);
}


$(document).ready(getFlights);