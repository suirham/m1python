import sqlite3
import os
from flask_app import data
from flask_app import ranking


def connect(database = "database.sqlite"):
  connection = sqlite3.connect(database)
  connection.set_trace_callback(print)
  connection.execute('PRAGMA foreign_keys = 1')
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