$(function () {
    $.demo = {};
    $.demo.refreshRate = 2000;
    $.demo.submittedLastRowId = 0;
    $.demo.submittedCount = 0;
    $.demo.streamedLastRowId = 0;
    $.demo.streamedCount = 0;
    $.demo.debug = true;
});

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
                    row.push('<td class="success center-text">Correct');
                } else {
                    row.push('<td class="warning center-text">Incorrect');
                }
                row.push('</td>');
                row.push('</tr>');
                var combinedRow = row.join("");
                $('#streamedFlightsTable tr:last').after(combinedRow);
            } else {
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
                    row.push('<td class="success center-text">On time');
                } else {
                    row.push('<td class="warning center-text">Delay');
                }
                row.push('</td>');
                row.push('</tr>')
                var combinedRow = row.join("");
                if ($.demo.submittedCount > 0) {
                    $('#submittedFlightsTable tr:first').after(combinedRow);
                } else {
                    $('#submittedFlightsTable tr:last').after(combinedRow);
                }
                $.demo.submittedCount += 1
            }
            $('#submittedCount').text($.demo.submittedCount)
            $('#streamedCount').text($.demo.streamedCount)
        });
        log("Last streamed: " + $.demo.streamedLastRowId);
        log("Last submitted: " + $.demo.submittedLastRowId);
    })

    setTimeout(function() {getFlights();}, $.demo.refreshRate);
}

function submitFlight() {
    var route = jsRoutes.controllers.KafkaEndpoint.submitFlight();
    var flightToSubmit = JSON.stringify({
                                         rowId: $.demo.submittedLastRowId + 1 + "",
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
        success: function(newId) {
            log("Submitted flight row id: " + newId);
        }
    });
    log("Flight was submitted: " + flightToSubmit);
}

function log(msg) {
    if ($.demo.debug) {
        console.log(msg);
    }
}

$(document).ready(getFlights);