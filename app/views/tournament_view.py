from datetime import datetime
import json

import flask
from flask_login import login_required

from app import app, db
from app.libs.tournament_lib import make_tournament
from app.models import Tournament


@app.route('/tournaments', methods=['GET'])
def tournaments():
    session = db.session
    all_tournaments = session.query(Tournament).order_by(Tournament.date_started.desc()).all()
    return flask.render_template('tournaments/tournaments.html',
                                 user=flask.g.user,
                                 tournaments=all_tournaments)


@app.route('/tournaments/add', methods=['GET'])
@login_required
def add_tournament_get():
    return flask.render_template('tournaments/add_tournament.html',
                                 user=flask.g.user)


@app.route('/tournaments/<int:tournament_id>', methods=['GET'])
@login_required
def tournament_get(tournament_id):
    session = db.session
    queried_tournament = session.query(Tournament).get(tournament_id)
    return flask.render_template('tournaments/tournament.html',
                                 user=flask.g.user,
                                 tournament=queried_tournament)


@app.route('/tournaments/add', methods=['POST'])
@login_required
def add_tournament_post():
    session = db.session

    data = flask.request.json

    added_tournament = make_tournament(session, datetime.strptime(data['date_started'], '%m/%d/%Y'),
                                       data['random_draw'], [])

    session.commit()
    return flask.Response(json.dumps({
        'id': added_tournament.id,
        'random_draw': added_tournament.random_draw,
    }), mimetype=u'application/json')
