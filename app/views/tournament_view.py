import random
from datetime import datetime
import json

import flask
import requests
from flask_login import login_required

from app import app, db
from app.libs.tournament_lib import make_tournament
from app.models import Tournament, User, TournamentPlayer
from config import Challonge


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
    queried_tournament = session.query(Tournament).get(tournament_id)
    tournament_player_users = session.query(User).join(
        TournamentPlayer,
        TournamentPlayer.user_id == User.id
    ).filter(
        TournamentPlayer.tournament_id == tournament_id
    ).all()
    tournament_player_user_dicts = [user.dict for user in tournament_player_users]

    return flask.render_template('tournaments/tournament.html',
                                 user=flask.g.user,
                                 tournament_players=json.dumps(tournament_player_user_dicts),
                                 tournament=queried_tournament)


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


@app.route('/tournaments/ch/list', methods=['GET'])
def ch_tournament_get():
    ch_tournaments = requests.get(
        '{}?api_key={}'.format(Challonge.URL, Challonge.API_KEY)
    )

    return flask.Response(ch_tournaments.text, mimetype=u'application/json')


@app.route('/tournaments/ch/add', methods=['POST'])
@login_required
def ch_add_tournament_post():
    session = db.session

    data = flask.request.json

    posted_tournament_response = requests.post(
        url='{}.json'.format(Challonge.URL),
        json={
            'api_key': Challonge.API_KEY,
            'tournament': {
                'name': 'experimental 1',
                'private': True,
                'show_rounds': True,
                'url': 'cratejoy_darts_{}'.format(random.randint(1, 100000))
            }
        }
    )
    json_posted_tournament = json.loads(posted_tournament_response.text)
    tournament_id = json_posted_tournament['tournament']['id']

    users = session.query(User).filter(
        User.id.in_([int(id) for id in data['player_ids']])
    ).all()

    participant_dicts = []
    for seed, user in enumerate(users):
        participant_dicts.append({
            'name': user.name,
            'seed': seed + 1
        })

    add_players_to_tourney = requests.post(
        url='{}/{}/participants/bulk_add.json'.format(Challonge.URL, tournament_id),
        json={
            'api_key': Challonge.API_KEY,
            'participants':  participant_dicts
        }

    )

    start_tournament = requests.post(
        url='{}/{}/start.json'.format(Challonge.URL, tournament_id),
        json={
            'api_key': Challonge.API_KEY
        }
    )

    return flask.Response('s', mimetype=u'application/json')
