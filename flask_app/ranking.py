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
  result = 0
  for match in matches:
    result += goal_for_count_during_a_match(team_id, match)
  return result


def goal_against_count(team_id, matches):
  result = 0
  for match in matches:
    result += goal_against_count_during_a_match(team_id, match)
  return result


def won_match_count(team_id, matches):
  result = 0
  for match in matches:
    result += team_wins_match(team_id, match)
  return result


def lost_match_count(team_id, matches):
  result = 0
  for match in matches:
    result += team_loses_match(team_id, match)
  return result


def draw_count(team_id, matches):
  result = 0
  for match in matches:
    result += team_draws_match(team_id, match)
  return result


def ranking_row(team_id, matches):
  won_match_count_ = won_match_count(team_id, matches)
  lost_match_count_ = lost_match_count(team_id, matches)
  draw_count_ = draw_count(team_id, matches)
  match_played_count_ = won_match_count_ + lost_match_count_ + draw_count_
  goal_for_count_ = goal_for_count(team_id, matches)
  goal_against_count_ = goal_against_count(team_id, matches)
  goal_difference_ = goal_difference(goal_for_count_, goal_against_count_)
  points_ = points(won_match_count_, draw_count_)
  return {'team_id': team_id, 
          'match_played_count': match_played_count_,
          'won_match_count': won_match_count_, 
          'lost_match_count': lost_match_count_, 
          'draw_count': draw_count_, 
          'goal_for_count': goal_for_count_, 
          'goal_against_count': goal_against_count_, 
          'goal_difference': goal_difference_, 
          'points': points_}


def unsorted_ranking(teams, matches):
  return []


def sorting_key(row):
  return (0, 0, 0)


def sorted_ranking(teams, matches):
  return []