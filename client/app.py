from flask import Flask, render_template, g, Markup, request, url_for, redirect, session, flash
from flask_wtf.csrf import CsrfProtect
from flask_bootstrap import Bootstrap
from functools import wraps
from flask_oauthlib.client import OAuth

import config
import forms

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
    return render_template('index.html', lists=lists, listForm=forms.List())

@auth_required
@app.route("/add/", methods=["POST"])
def addList():
    form = forms.List(request.form)
    if request.method == 'POST' and form.validate():
        resp = todo.post('lists/', data={
            'name':  form['name'].data
        })
        if resp.status == 403:
            flash('Your tweet was too long.')
        else:
            flash('Successfully tweeted your tweet (ID: #%s)' % resp.data['id'])
    return redirect(url_for('index'))

@auth_required
@app.route("/delete/<int:pk>")
def deleteList(pk):
    resp = todo.delete('lists/' + str(pk) + "/", data={"id":pk})
    if resp.status == 200:
        flash("Successfully deleted the list")
    elif resp.status == 401:
        flash("You are not authorized to acces this element.")
    else:
        flash('Unable to load list from server.')
    return redirect(url_for('index'))

@app.route("/edit/<int:pk>", methods=["GET", "POST"])
@auth_required
def editList(pk):
    resp = todo.get('lists/' + str(pk) + "/")
    lists = None
    if resp.status == 200:
        lists = resp.data
    elif resp.status == 401:
        flash("You are not authorized to acces this element.")
        return redirect(url_for('index'))
    else:
        flash('Unable to load list from server.')
        return redirect(url_for('index'))
    print(lists)

    form = forms.List(request.form, data=lists)
    if request.method == 'POST' and form.validate():
        resp = todo.put('lists/'+str(pk)+"/", data={
            'name':  form['name'].data
        })
        if resp.status == 401:
            flash("You are not authorized to acces this element.")
        elif resp.status == 403:
            flash('Your tweet was too long.')
        else:
            flash('Successfully Updated the list name.')
        return redirect(url_for('detailList', pk=pk))
    return render_template('edit_list.html', form=form)

@app.route('/<int:pk>')
@auth_required
def detailList(pk):
    resp = todo.get('lists/' + str(pk) + "/")
    lists = None
    if resp.status == 200:
        lists = resp.data
    elif resp.status == 401:
        flash("You are not authorized to access this element.")
    else:
        flash('Unable to load list from server.')
    return render_template('detail_list.html', todoForm=forms.Todo(), list=lists)

@app.route("/todo/add/<int:list_id>", methods=["POST"])
@auth_required
def addTodo(list_id):
    form = forms.Todo(request.form)
    if request.method == 'POST' and form.validate():
        resp = todo.post('todos/', data={
            'todo': form['todo'].data,
            'todo_list' : list_id
        })
        if resp.status == 401:
            flash("You are not authorized to acces this element.")
        elif resp.status == 403:
            flash('Your tweet was too long.')
        else:
            flash('Successfully added your task.')
        print(resp.data)
    return redirect(url_for('detailList', pk=list_id))

@app.route("/todo/delete/<int:list_id>/<int:pk>")
@auth_required
def delTodo(list_id, pk):
    resp = todo.delete('todos/' + str(pk) + "/", data={"id":pk})
    if resp.status == 200:
        flash("Successfully deleted the list")
    elif resp.status == 401:
        flash("You are not authorized to acces this element.")
    else:
        flash('Unable to load list from server.')
    return redirect(url_for('detailList', pk=list_id))

@app.route("/todo/edit/<int:list_id>/<int:pk>", methods=["GET", "POST"])
@auth_required
def editTodo(list_id, pk):
    resp = todo.get('todos/' + str(pk) + "/")
    todos = None
    if resp.status == 200:
        todos = resp.data
    elif resp.status == 401:
        flash("You are not authorized to acces this element.")
        return redirect(url_for('index'))
    else:
        flash('Unable to load todo from server.')
        return redirect(url_for('detailList', pk=list_id))

    form = forms.Todo(request.form, data=todos)
    if request.method == 'POST' and form.validate():
        resp = todo.put('todos/'+str(pk)+"/", data={
            'todo':  form['todo'].data
        })
        if resp.status == 401:
            flash("You are not authorized to acces this element.")
        elif resp.status == 403:
            flash('Your tweet was too long.')
        else:
            flash('Successfully Updated the list name.')
        return redirect(url_for('detailList', pk=list_id))
    return render_template('edit_todo.html', form=form)

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="0.0.0.0", port=8000)
