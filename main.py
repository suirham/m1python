from flask_app.ranking import *
from flask_app import data

match0 = {'id' : 123, 'team0' : 1, 'team1' : 3, 'score0' : 3, 'score1' : 5, 'date' : '2048-01-01 00:00:00'}
match1 = {'id' : 231, 'team0' : 4, 'team1' : 2, 'score0' : 2, 'score1' : 2, 'date' : '2048-01-01 00:00:00'}
match2 = {'id' : 222, 'team0' : 3, 'team1' : 2, 'score0' : 1, 'score1' : 3, 'date' : '2048-01-01 00:00:00'}
for row in data.expected_sorted_ranking():
    print (goal_for_count(row['team_id'], data.matches()))