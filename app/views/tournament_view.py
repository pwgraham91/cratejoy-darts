from datetime import datetime
import json

import flask
from flask_login import login_required

from app import app, db
from app.libs.tournament_lib import make_tournament
from app.models import Tournament, User, Game
from app.views.handlers import game_handler


@app.route('/tournaments', methods=['GET'])
def tournaments():
    session = db.session
    all_tournaments = session.query(Tournament).order_by(Tournament.date_started.desc()).all()
    return flask.render_template('tournaments/tournaments.html',
                                 user=flask.g.user,
                                 tournaments=all_tournaments)


@app.route('/tournaments/<int:tournament_id>', methods=['GET'])
@login_required
def tournament_get(tournament_id):
    session = db.session
    tournament_games = session.query(Game).filter(
        Game.tournament_id == int(tournament_id)
    ).order_by(
        Game.round.desc(),
        Game.position.asc()
    ).all()

    if len(tournament_games) > 0:
        games_by_round = game_handler.get_games_by_round(tournament_games)
    else:
        return 'no games in this tournament'

    return flask.render_template('tournaments/tournament.html',
                                 user=flask.g.user,
                                 games_by_round=json.dumps(games_by_round))


@app.route('/tournaments/add', methods=['GET'])
@login_required
def add_tournament_get():
    session = db.session
    players = session.query(User).all()
    return flask.render_template('tournaments/add_tournament.html',
                                 user=flask.g.user,
                                 players=players)


@app.route('/tournaments/add', methods=['POST'])
@login_required
def add_tournament_post():
    session = db.session

    data = flask.request.json

    added_tournament = make_tournament(session, datetime.strptime(data['date_started'], '%m/%d/%Y'),
                                       data['random_draw'], data['player_ids'])

    session.commit()
    return flask.Response(json.dumps({
        'id': added_tournament.id,
        'random_draw': added_tournament.random_draw,
    }), mimetype=u'application/json')
