import sqlite3
import os
from flask_app import data
from flask_app import ranking


def dictionary_factory(cursor, row):
  dictionary = {}
  for index in range(len(cursor.description)):
    column_name = cursor.description[index][0]
    dictionary[column_name] = row[index]
  return dictionary


def connect(database = "database.sqlite"):
  connection = sqlite3.connect(database)
  connection.set_trace_callback(print)
  connection.execute('PRAGMA foreign_keys = 1')
  connection.row_factory = dictionary_factory
  return connection


def read_build_script():
  path = os.path.join(os.path.dirname(__file__), 'build.sql')
  file = open(path)
  script = file.read()
  file.close()
  return script


def create_database(connection):
  script = read_build_script()
  connection.executescript(script)
  connection.commit()


def insert_team(connection, team):
  sql = 'INSERT INTO teams (id, name) VALUES (:id, :name)'
  connection.execute(sql, team)  
  connection.commit()


def insert_match(connection, match):
    sql = '''INSERT INTO matches (id, team0, team1, score0, score1, date) 
             VALUES (:id, :team0, :team1, :score0, :score1, :date)'''
    connection.execute(sql, match) 
    connection.commit()


def teams(connection):
  sql = 'SELECT * FROM teams ORDER BY id'
  cursor = connection.execute(sql)
  return cursor.fetchall()


def matches(connection):
    sql = 'SELECT * FROM matches ORDER BY id'
    cursor = connection.execute(sql)
    return cursor.fetchall()


def fill_database(connection):
  teams = data.teams()
  for team in teams:
    insert_team(connection, team)
  matches = data.matches()
  for match in matches:
    insert_match(connection, match)


def update_ranking(connection):
  sql = "DELETE FROM ranking"
  connection.execute(sql)
  teams_ = teams(connection)
  matches_ = matches(connection)
  ranking_ = ranking.sorted_ranking(teams_, matches_)
  sql = '''INSERT INTO ranking(rank, team_id, match_played_count, 
                                won_match_count, lost_match_count, draw_count, 
                                goal_for_count, goal_against_count, 
                                goal_difference, points)
            VALUES (:rank, :team_id, :match_played_count, 
                    :won_match_count, :lost_match_count, :draw_count, 
                    :goal_for_count, :goal_against_count, 
                    :goal_difference, :points)'''
  connection.executemany(sql, ranking_)
  # for row in ranking_: connection.execute(sql, row)
  connection.commit()


def sorted_ranking(connection):
  sql = '''SELECT ranking.*, teams.name FROM ranking 
           JOIN teams ON ranking.team_id = teams.id
           ORDER BY rank'''
  cursor = connection.execute(sql)
  return cursor.fetchall()


def team_matches(connection, team_id):
  sql = '''
    SELECT matches.*, t0.name AS name0, t1.name AS name1 FROM matches
    JOIN teams AS t0 ON matches.team0 = t0.id
    JOIN teams AS t1 ON matches.team1 = t1.id
    WHERE matches.team0 = :team_id OR matches.team1 = :team_id
    ORDER BY date
  '''
  cursor = connection.execute(sql, {'team_id': team_id})
  return cursor.fetchall()


def team(connection, team_id):
  sql = '''
    SELECT * FROM teams
    WHERE id = :team_id
  '''
  cursor = connection.execute(sql, {'team_id': team_id})
  teams = cursor.fetchall()
  if len(teams)==0:
    raise Exception('Équipe inconnue')
  return teams[0]