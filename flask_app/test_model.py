import pytest
from flask_app import model
from flask_app import data

def test_teams_and_insert_team():
    connection = model.connect(":memory:")
    model.create_database(connection)
    teams = data.teams()
    model.insert_team(connection, teams[4])
    model.insert_team(connection, teams[2])
    assert model.teams(connection) == [teams[2], teams[4]]


def test_matches_and_insert_match():
    connection = model.connect(":memory:")
    model.create_database(connection)
    teams = data.teams()
    matches = data.matches()
    model.insert_team(connection, teams[7])
    model.insert_team(connection, teams[19])
    model.insert_match(connection, matches[194])
    model.insert_match(connection, matches[4])
    assert model.matches(connection) == [matches[4], matches[194]]


def test_fill_database():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.fill_database(connection)
    assert model.teams(connection) == data.teams()
    assert model.matches(connection) == data.matches()


def test_update_ranking():
  connection = model.connect(":memory:")
  model.create_database(connection)
  model.update_ranking(connection)
  model.fill_database(connection)
  model.update_ranking(connection)
  model.update_ranking(connection)
  cursor = connection.execute("SELECT * from ranking ORDER BY rank")
  assert list(cursor) == data.expected_sorted_ranking()


def test_sorted_ranking():
  connection = model.connect(":memory:")
  model.create_database(connection)
  model.fill_database(connection)
  model.update_ranking(connection)
  assert model.sorted_ranking(connection) == data.expected_sorted_ranking_with_name()


def test_team_matches():
  connection = model.connect(":memory:")
  model.create_database(connection)
  model.fill_database(connection)
  assert model.team_matches(connection, 4) == data.expected_team_matches_for_team_4()


def test_team():
   connection = model.connect(":memory:")
   model.create_database(connection)
   model.fill_database(connection)
   teams = data.teams()
   assert model.team(connection, 4) == teams[3]


def test_team_exception():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.fill_database(connection)
    with pytest.raises(Exception) as exception_info:
        model.team(connection, 1000)
    assert str(exception_info.value) == 'Équipe inconnue'


def test_ranking_row():
  connection = model.connect(":memory:")
  model.create_database(connection)
  model.fill_database(connection)
  model.update_ranking(connection)
  for row in data.expected_sorted_ranking_with_name():
      assert model.ranking_row(connection, row['team_id']) == row


def test_ranking_row_exception():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.fill_database(connection)
    model.update_ranking(connection)
    with pytest.raises(Exception) as exception_info:
        model.ranking_row(connection, 1000)
    assert str(exception_info.value) == 'Équipe inconnue'