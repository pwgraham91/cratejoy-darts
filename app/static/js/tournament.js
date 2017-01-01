console.log('loaded tournament.js');

define([
	'jQuery',
	'/static/js/tournament_builder.js'
], function(
	jquery,
	tournamentBuilder
) {
	var gamesByRound = window.gamesByRound;
	console.log(tournamentBuilder({}));
});