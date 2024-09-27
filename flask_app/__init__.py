import os
from flask import Flask, render_template, request, redirect
from flask_app import model
import datetime
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SelectField, PasswordField, DateField, TimeField, IntegerField, EmailField, validators

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/', methods=['GET'])
def home():
    connection = model.connect()
    ranking = model.sorted_ranking(connection)
    return render_template('ranking.html', ranking=ranking)


@app.route('/team/<int:team_id>', methods=['GET'])
def team(team_id):
    connection = model.connect()
    matches = model.team_matches(connection, team_id)
    ranking_row = model.ranking_row(connection, team_id)
    return render_template('team.html', matches=matches, ranking_row=ranking_row)

class TeamForm(FlaskForm):
  team_name = StringField('team_name', validators=[validators.DataRequired()])

@app.route('/team/create', methods=['GET', 'POST'])
def team_create():
    form = TeamForm()
    if form.validate_on_submit():
        return form.team_name.data
    return render_template('team_edit.html')