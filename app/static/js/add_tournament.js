console.log('loaded add_tournament.js');

define([
	'jQuery',
	'bootstrap',
	'bootstrapDatepicker'
], function(
	jquery,
	bootstrap,
    bootstrapDatepicker
) {
	var $datePicker = $('#date-started');
	$datePicker.datepicker({
		format: "mm/dd/yyyy",
		autoclose: true
	});

	$('#submit-tournament').click(function () {
		var dateStarted = $datePicker.val();
		var randomDraw = $('select[name="random"]').val();
		var checkedPlayers = $('input[name="players"]:checked');

		var checkedPlayerIds = _.map(checkedPlayers, function (playerInput) {
			return playerInput.value;
		});

		$.ajax({
			type: "POST",
			url: '/tournaments/add',
			data: JSON.stringify({
				date_started: dateStarted,
				random_draw: randomDraw,
				player_ids: checkedPlayerIds
			}),
			success: function (data) {
				window.location.href = '/tournaments/' + data.id;
			},
			error: function (data) {
				console.log(data)
			},
			contentType: 'application/json'
		});
	});
});
