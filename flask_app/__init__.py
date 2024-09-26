import os
from flask import Flask, render_template
from flask_app import model


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    connection = model.connect()
    ranking = model.sorted_ranking(connection)
    return render_template('ranking.html', ranking=ranking)


@app.route('/team/<int:team_id>', methods=['GET'])
def team(team_id):
    return 'Team {0}'.format(team_id)