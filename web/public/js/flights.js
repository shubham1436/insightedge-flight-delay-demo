$(function () {
    $.demo = {};
    $.demo.refreshRate = 2000;
    $.demo.submittedLastRowId = 0;
    $.demo.submittedCount = 0;
    $.demo.streamedLastRowId = 0;
    $.demo.streamedCount = 0;
});


if (window.console) {
  console.log("Welcome to your Play application's JavaScript!");
}

function getFlights() {
    var flights = jsRoutes.controllers.FlightEndpoint.getLastFlights($.demo.streamedLastRowId, $.demo.submittedLastRowId);

    $.getJSON(flights.url, function(data) {
        $.each(data, function(index, flight) {
            var tableToInsert = ""
            if (flight.streamed == "1") {
                $.demo.streamedCount += 1;
                tableToInsert = "streamedFlightsTable"
                if (flight.rowId > $.demo.streamedLastRowId) {
                    $.demo.streamedLastRowId = flight.rowId
                }
            } else {
                $.demo.submittedCount += 1
                tableToInsert = "submittedFlightsTable"
                if (flight.rowId > $.demo.submittedLastRowId) {
                    $.demo.submittedLastRowId = flight.rowId
                }
            }
            $('#'+tableToInsert+' tr:last').after('<tr><td>' + flight.rowId + '</td><td>' + flight.streamed + '</td><td>' + flight.origin + '</td><td>' + flight.destination + '</td><td>' + flight.departureDelayMinutes + '</td><td>' + flight.prediction + '</td></tr>');
            $('#submittedCount').text($.demo.submittedCount)
            $('#streamedCount').text($.demo.streamedCount)
        });
        console.log("Last streamed: " + $.demo.streamedLastRowId);
        console.log("Last submitted: " + $.demo.submittedLastRowId);
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