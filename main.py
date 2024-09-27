from flask_app.ranking import *
from flask_app import data, ranking
from flask_app import model  

connection = model.connect()

# model.create_database(connection)

# model.insert_teams(connection, {'id': 2, 'name': 'Marseille'})
# model.insert_teams(connection, {'id': 7, 'name': 'Strasbourg'})

model.insert_match(connection, {'id': 1, 'team0': 7, 'team1': 2, 'score0': 4, 'score1': 9, 'date': ''})

# model.teams(connection)