import sqlite3
import os
from flask_app import *

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

  
def insert_teams(connection, team):
    sql = 'insert into teams (id, name) values (:id, :name)'
    connection.execute(sql, team)
    connection.commit()

def insert_match(connection, match):
   sql = 'insert into matches (id, team0, team1, score0, score1, date) values (:id, :team0, :team1, :score0, :score1, :date)'
   connection.execute(sql, match)
   connection.commit()

def teams(connection):
   sql = 'select * from teams'
   cursor = connection.execute(sql)
   return cursor.fetchall()

def matches(connection):
   sql = 'select * from matches'
   cursor = connection.execute(sql)
   return cursor.fetchall()