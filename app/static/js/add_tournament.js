console.log('loaded add_tournament.js');

$(document).ready(function() {
	var $datePicker = $('#date-started');
	$datePicker.datepicker({
		format: "mm/dd/yyyy"
	});

	$('#submit-tournament').click(function () {
		var dateStarted = $datePicker.val();
		var randomDraw = $('select[name="random"]').val();

		$.ajax({
			type: "POST",
			url: '/tournaments/add',
			data: JSON.stringify({
				date_started: dateStarted,
				random_draw: randomDraw
			}),
			success: function (data) {
				debugger;
				window.href = '/tournaments/' + data.id;
			},
			error: function (data) {
				console.log(data)
			},
			contentType: 'application/json'
		});
	});
});
