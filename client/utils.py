from flask import flash, session, redirect, url_for
from functools import wraps

class NotLogged(Exception):
    pass

def auth_required(fn):
    @wraps(fn)
    def outer(*args, **kwargs):
        if session.get('todo_token'):
            try:
                return fn(*args, **kwargs)
            except NotLogged:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    return outer

def get(api, endpoint):
    resp = api.get(endpoint)
    obj = None
    if resp.status == 200:
        obj = resp.data
    elif resp.status == 401:
        flash("You are not logged on the server.", "error")
        raise NotLogged()
    elif resp.status == 403:
        flash("You are not authorized to access this element.", "error")
    elif resp.status == 404:
        flash("Not found on server.", "error")
    else:
        flash('Unable to load data from server.', "error")
    return obj

def add(api, endoint, data):
    resp = api.post(endoint, data=data)
    if resp.status == 401:
        flash("You are not logged on the server.", "error")
        raise NotLogged()
    elif resp.status == 403:
        flash("You are not authorized to access this element.", "error")
    else:
        flash('Add successful', "success")

def edit(api, endpoint, data):
    resp = api.put(endpoint, data=data)
    if resp.status == 401:
        flash("You are not logged on the server.", "error")
        raise NotLogged()
    elif resp.status == 403:
        flash("You are not authorized to access this element.", "error")
    else:
        flash('Successfully Updated the name.', "success")

def delete(api, endpoint, data):
    resp = api.delete(endpoint, data=data)
    if resp.status == 200 or resp.status == 204:
        flash("Successfully deleted the item", "success")
    elif resp.status == 403:
        flash("You are not authorized to access this element.", "error")
    elif resp.status == 401:
        flash("You are not logged on the server.", "error")
        raise NotLogged()
    else:
        flash('Unable to perform this action.', "error")
