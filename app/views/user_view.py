import json

import flask
from flask_login import login_required

from app import app, db
from app.models import User


@app.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    session = db.session
    queried_user = session.query(User).get(user_id)
    return flask.render_template('user.html',
                                 user=flask.g.user,
                                 queried_user=queried_user)


@app.route('/user/add', methods=['GET'])
@login_required
def add_user_get():
    return flask.render_template('add_user.html',
                                 user=flask.g.user)


@app.route('/user/add', methods=['POST'])
@login_required
def add_user_post():
    session = db.session
    data = flask.request.json
    added_user = User(
        name=data['name'],
        email=data['email'],
    )
    session.add(added_user)
    session.commit()
    return flask.Response(json.dumps({
        'id': added_user.id,
        'name': added_user.name,
        'email': added_user.email,
    }), mimetype=u'application/json')
