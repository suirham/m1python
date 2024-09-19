from flask_app.ranking import *
from flask_app import data, ranking
from flask_app import model  

connection = model.connect()

model.create_database(connection)

model.insert_teams(connection, {'id':4, 'name': 'Marseille'})

model.teams(connection)