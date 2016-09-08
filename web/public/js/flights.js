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
                if (flight.rowId > $.demo.streamedLastRowId) {
                    $.demo.streamedLastRowId = flight.rowId
                }
                var row = [];
                row.push('<tr>')
                row.push('<td>');     row.push(flight.rowId);                   row.push('</td>');
                row.push('<td>Jan '); row.push(flight.dayOfMonth);              row.push('</td>');
                row.push('<td>');     row.push(flight.carrier);                 row.push('</td>');
                row.push('<td>');     row.push(flight.origin);                  row.push('</td>');
                row.push('<td>');     row.push(flight.destination);             row.push('</td>');
                row.push('<td>');     row.push(flight.scheduledDepartureTime);  row.push('</td>');
                row.push('<td>');     row.push(flight.scheduledArrivalTime);    row.push('</td>');
                row.push('<td>');     row.push(flight.departureDelayMinutes);   row.push('</td>');
                if ((flight.prediction == "0" && flight.departureDelayMinutes <= 40) ||
                    (flight.prediction == "1" && flight.departureDelayMinutes > 40)) {
                    row.push('<td class="success">Correct');
                } else {
                    row.push('<td class="warning">Incorrect');
                }
                row.push('</td>');
                row.push('</tr>')
                var combinedRow = row.join("");
                $('#streamedFlightsTable tr:last').after(combinedRow);
                //$('#streamedFlightsTable tr:last').after('<tr><td>' + flight.rowId + '</td><td>' + flight.streamed + '</td><td>' + flight.origin + '</td><td>' + flight.destination + '</td><td>' + flight.departureDelayMinutes + '</td><td>' + flight.prediction + '</td></tr>');
            } else {
                $.demo.submittedCount += 1
                if (flight.rowId > $.demo.submittedLastRowId) {
                    $.demo.submittedLastRowId = flight.rowId
                }
                var row = [];
                row.push('<tr>')
                row.push('<td>'); row.push(flight.rowId);                   row.push('</td>');
                row.push('<td>'); row.push(flight.dayOfMonth);              row.push('</td>');
                row.push('<td>'); row.push(flight.carrier);                 row.push('</td>');
                row.push('<td>'); row.push(flight.origin);                  row.push('</td>');
                row.push('<td>'); row.push(flight.destination);             row.push('</td>');
                row.push('<td>'); row.push(flight.scheduledDepartureTime);  row.push('</td>');
                row.push('<td>'); row.push(flight.scheduledArrivalTime);    row.push('</td>');
                if (flight.prediction == "0") {
                    row.push('<td class="success">No Delay');
                } else {
                    row.push('<td class="warning">Delay');
                }
                row.push('</td>');
                row.push('</tr>')
                var combinedRow = row.join("");
                $('#submittedFlightsTable tr:last').after(combinedRow);
                //$('#submittedFlightsTable tr:last').after('<tr><td>' + flight.rowId + '</td><td>Jan ' + flight.dayOfMonth + '</td><td>' + flight.carrier + '</td><td>' + flight.origin + '</td><td>' + flight.destination + '</td><td>' + flight.departureDelayMinutes + '</td><td>' + flight.prediction + '</td></tr>');
            }
            $('#submittedCount').text($.demo.submittedCount)
            $('#streamedCount').text($.demo.streamedCount)
        });
        console.log("Last streamed: " + $.demo.streamedLastRowId);
        console.log("Last submitted: " + $.demo.submittedLastRowId);
    })

    setTimeout(function() {getFlights();}, $.demo.refreshRate);
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