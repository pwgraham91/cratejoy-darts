import flask
from flask_login import login_required

from app import app


@app.route('/user', methods=['GET'])
@login_required
def user():
    return flask.render_template('user.html',
                                 user=flask.g.user)


@app.route('/user/add', methods=['GET'])
@login_required
def add_user():
    return flask.render_template('add_user.html',
                                 user=flask.g.user)
