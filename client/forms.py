from flask_wtf import Form
from wtforms import TextField, SubmitField, validators

class Todo(Form):
    todo = TextField("Text", [validators.Length(min=2, max=254)])
    submit = SubmitField("Envoyer")

class List(Form):
    name = TextField("Text", [validators.Length(min=2, max=254)])
    submit = SubmitField("Envoyer")
