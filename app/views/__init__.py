import flask
from flask import g
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user, logout_user

from app import app, oid
from app.forms import LoginForm


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flask.session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# rearch to move this at some point
import app.handlers.auth_handler  # needs to be at bottom
