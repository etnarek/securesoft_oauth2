from flask import Flask, render_template, g, Markup, request, url_for, redirect, session, flash
from flask_wtf.csrf import CsrfProtect
from flask_bootstrap import Bootstrap
from flask_oauthlib.client import OAuth
from datetime import timedelta
from urllib.parse import urljoin

import config
import forms
import utils

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

@todo.tokengetter
def get_todo_teken(token=None):
    return session.get('todo_token')


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/log')
def log():
    return todo.authorize(callback=urljoin(config.SERVER_NAME, url_for('oauth_authorized', next=None)))


@app.route('/oauth-authorized')
@todo.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=35000)
    session['todo_token'] = (
        resp['access_token'],
        resp['refresh_token']
    )

    flash('You are signed in.')
    return redirect(next_url)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
@utils.auth_required
def index():
    lists = utils.get(todo, "lists/")
    return render_template('index.html', lists=lists, listForm=forms.List())

@utils.auth_required
@app.route("/add/", methods=["POST"])
def addList():
    form = forms.List(request.form)
    if request.method == 'POST' and form.validate():
        utils.add(
            todo,
            "lists/",
            {'name':  form['name'].data}
        )
    return redirect(url_for('index'))

@utils.auth_required
@app.route("/delete/<int:pk>", methods=["POST"])
def deleteList(pk):
    utils.delete(todo, "lists/%d/" % pk, {"id":pk})
    return redirect(url_for('index'))

@app.route("/edit/<int:pk>", methods=["GET", "POST"])
@utils.auth_required
def editList(pk):
    lists = utils.get(todo, "lists/%d/" % pk)
    if lists is None:
        return redirect(url_for('index'))

    form = forms.List(request.form, data=lists)
    if request.method == 'POST' and form.validate():
        utils.edit(
            todo,
            "lists/%d/" % pk,
            {"name": form["name"].data}
        )
        return redirect(url_for('detailList', pk=pk))
    return render_template('edit_list.html', form=form)

@app.route('/<int:pk>')
@utils.auth_required
def detailList(pk):
    lists = utils.get(todo, "lists/%d/" % pk)
    if lists:
        return render_template('detail_list.html', todoForm=forms.Todo(), list=lists)
    else:
        return redirect(url_for("index"))

@app.route("/todo/add/<int:list_id>", methods=["POST"])
@utils.auth_required
def addTodo(list_id):
    form = forms.Todo(request.form)
    if request.method == 'POST' and form.validate():
        utils.add(
            todo,
            "todos/",
            {'todo': form['todo'].data, 'todo_list' : list_id}
        )
    return redirect(url_for('detailList', pk=list_id))

@app.route("/todo/delete/<int:list_id>/<int:pk>", methods=["POST"])
@utils.auth_required
def delTodo(list_id, pk):
    utils.delete(todo, "todos/%d/" % pk, {"id":pk})
    return redirect(url_for('detailList', pk=list_id))

@app.route("/todo/edit/<int:list_id>/<int:pk>", methods=["GET", "POST"])
@utils.auth_required
def editTodo(list_id, pk):
    todos = utils.get(todo, "todos/%d/" % pk)
    if todos is None:
        return redirect(url_for('index'))

    form = forms.Todo(request.form, data=todos)
    if request.method == 'POST' and form.validate():
        utils.edit(
            todo,
            "todos/%d/" % pk,
            {'todo':  form['todo'].data}
        )
        return redirect(url_for('detailList', pk=list_id))
    return render_template('edit_todo.html', form=form)

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="127.0.0.1", port=3032)
