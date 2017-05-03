import React from 'react';

class Header extends React.Component {
	renderRandom() {
		let random;
		if (window.tournament.random_draw) {
			random = 'True';
		} else {
			random = 'False';
		}
		return random;
	}
	render() {
		return (
			<header>
				<h1>
					Tournament
				</h1>
				<p>Date Started: {window.tournament.date_started}</p>
				<p>Random: {this.renderRandom()}</p>
			</header>
		)
	}
};

export default Header;
