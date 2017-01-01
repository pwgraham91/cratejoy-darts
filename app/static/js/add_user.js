console.log('loaded add_user.js');

define([
	'jQuery'
], function(jquery) {
	$('#submit-user').click(function () {
		var name = $('input[name="username"]').val();
		var email = $('input[name="email"]').val();

		$.ajax({
			type: "POST",
			url: '/user/add',
			data: JSON.stringify({
				name: name,
				email: email
			}),
			success: function (data) {
				window.location.href = '/user/' + data.id;
			},
			error: function (data) {
				console.log(data)
			},
			contentType: 'application/json'
		});
	});
});
