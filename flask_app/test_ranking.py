from flask_app import ranking

match0 = {'id' : 123, 'team0' : 1, 'team1' : 3, 'score0' : 3, 'score1' : 5, 'date' : '2048-01-01 00:00:00'}
match1 = {'id' : 231, 'team0' : 4, 'team1' : 2, 'score0' : 2, 'score1' : 2, 'date' : '2048-01-01 00:00:00'}
match2 = {'id' : 222, 'team0' : 3, 'team1' : 2, 'score0' : 1, 'score1' : 3, 'date' : '2048-01-01 00:00:00'}


def test_goal_difference():
  assert ranking.goal_difference(2, 3) == -1
  assert ranking.goal_difference(0, 0) == 0
  assert ranking.goal_difference(4, 1) == 3


def test_points():
  assert ranking.points(1, 0) == 3
  assert ranking.points(0, 1) == 1
  assert ranking.points(0, 0) == 0
  assert ranking.points(3, 2) == 11


def test_team_wins_match():
  assert not ranking.team_wins_match(1, match0)
  assert ranking.team_wins_match(3, match0)
  assert not ranking.team_wins_match(4, match1)
  assert not ranking.team_wins_match(2, match1)
  assert not ranking.team_wins_match(3, match2)
  assert ranking.team_wins_match(2, match2)
  assert not ranking.team_wins_match(4, match0)


def test_team_loses_match():
  assert ranking.team_loses_match(1, match0)
  assert not ranking.team_loses_match(3, match0)
  assert not ranking.team_loses_match(4, match1)
  assert not ranking.team_loses_match(2, match1)
  assert ranking.team_loses_match(3, match2)
  assert not ranking.team_loses_match(2, match2)
  assert not ranking.team_loses_match(4, match0)


def test_team_draws_match():
  assert not ranking.team_draws_match(1, match0)
  assert not ranking.team_draws_match(3, match0)
  assert ranking.team_draws_match(4, match1)
  assert ranking.team_draws_match(2, match1)
  assert not ranking.team_draws_match(6, match1)
  assert not ranking.team_draws_match(3, match2)
  assert not ranking.team_draws_match(2, match2)
  assert not ranking.team_draws_match(4, match0)


def test_goal_for_count_during_a_match():
  assert ranking.goal_for_count_during_a_match(1, match0) == 3
  assert ranking.goal_for_count_during_a_match(3, match0) == 5
  assert ranking.goal_for_count_during_a_match(4, match1) == 2
  assert ranking.goal_for_count_during_a_match(2, match1) == 2
  assert ranking.goal_for_count_during_a_match(6, match1) == 0
  assert ranking.goal_for_count_during_a_match(3, match2) == 1
  assert ranking.goal_for_count_during_a_match(2, match2) == 3
  assert ranking.goal_for_count_during_a_match(4, match0) == 0


def test_goal_against_during_a_match():
    assert ranking.goal_against_count_during_a_match(1, match0) == 5
    assert ranking.goal_against_count_during_a_match(3, match0) == 3
    assert ranking.goal_against_count_during_a_match(4, match1) == 2
    assert ranking.goal_against_count_during_a_match(2, match1) == 2
    assert ranking.goal_against_count_during_a_match(6, match1) == 0
    assert ranking.goal_against_count_during_a_match(3, match2) == 3
    assert ranking.goal_against_count_during_a_match(2, match2) == 1
    assert ranking.goal_against_count_during_a_match(4, match0) == 0