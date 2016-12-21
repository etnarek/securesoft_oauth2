from flask import Flask, render_template, g, Markup, request, url_for, redirect, session, flash
from flask_wtf.csrf import CsrfProtect
from flask_bootstrap import Bootstrap
from functools import wraps
from flask_oauthlib.client import OAuth

import config

app = Flask(__name__)
app.secret_key = config.SECRET
csfr = CsrfProtect(app)
Bootstrap(app)

oauth = OAuth()
todo = oauth.remote_app(
    'todo',
    base_url=config.SERVER_URL,
    request_token_url=None,
    access_token_url=config.SERVER_URL + config.TOKEN_URL,
    authorize_url=config.SERVER_URL + config.AUTHORIZATION_URL,
    consumer_key=config.OAUTH_ID,
    consumer_secret=config.OAUTH_SECRET
)
oauth.init_app(app)


def auth_required(fn):
    @wraps(fn)
    def outer(*args, **kwargs):
        if session.get('todo_token'):
            return fn(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return outer

@todo.tokengetter
def get_todo_teken(token=None):
    return session.get('todo_token')


@app.route('/login')
def login():
    return "We are going to connect you with" + config.SERVER_URL + "\n clik here to continue: <a href=/log>login</a>"

@app.route('/log')
def log():
    return todo.authorize(callback="http://127.0.0.1:5000"+url_for('oauth_authorized', next=None))


@app.route('/oauth-authorized')
@todo.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['todo_token'] = (
        resp['access_token'],
        resp['refresh_token']
    )

    flash('You were signed in.')
    return redirect(next_url)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
@auth_required
def index():
    resp = todo.get('lists/')
    if resp.status == 200:
        lists = resp.data
    else:
        lists = None
        flash('Unable to load lists from server.')
    return str(lists)

def addList():
    pass

def deleteList():
    pass

def editList():
    pass

def detailList():
    pass

def addTodo():
    pass

def delTodo():
    pass

def editTodo():
    pass

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="0.0.0.0", port=8000)
