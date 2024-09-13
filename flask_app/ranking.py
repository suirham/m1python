def goal_difference(goal_for_count, goal_against_count):
  return goal_for_count - goal_against_count


def points(won_match_count, draw_count):
  return 3*won_match_count + draw_count


def team_wins_match(team_id, match):
  return (match['team0'] == team_id and match['score0'] > match['score1']) \
      or (match['team1'] == team_id and match['score1'] > match['score0'])


def team_loses_match(team_id, match):
  return (match['team0'] == team_id and match['score0'] < match['score1']) \
      or (match['team1'] == team_id and match['score1'] < match['score0'])


def team_draws_match(team_id, match):
  return (match['team0'] == team_id or match['team1'] == team_id) \
     and (match['score0'] == match['score1'])


def goal_for_count_during_a_match(team_id, match):
  return match['score0'] if match['team0'] == team_id \
    else match['score1'] if match['team1'] == team_id \
    else 0


def goal_against_count_during_a_match(team_id, match):
  return match['score1'] if match['team0'] == team_id \
    else match['score0'] if match['team1'] == team_id \
    else 0


def goal_for_count(team_id, matches):
  return 0


def goal_against_count(team_id, matches):
  return 0


def won_match_count(team_id, matches):
  return 0


def lost_match_count(team_id, matches):
  return 0


def draw_count(team_id, matches):
  return 0


def ranking_row(team_id, matches):
  return {}


def unsorted_ranking(teams, matches):
  return []


def sorting_key(row):
  return (0, 0, 0)


def sorted_ranking(teams, matches):
  return []