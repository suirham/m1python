from flask_app import data

def goal_difference(goal_for_count, goal_against_count):
  return goal_for_count - goal_against_count


def points(won_match_count, draw_count):
  return draw_count + 3 * won_match_count


def team_wins_match(team_id, match):
  # match0 = {'id' : 123, 'team0' : 1, 'team1' : 3, 'score0' : 3, 'score1' : 5, 'date' : '2048-01-01 00:00:00'}
  # match1 = {'id' : 231, 'team0' : 4, 'team1' : 2, 'score0' : 2, 'score1' : 2, 'date' : '2048-01-01 00:00:00'}
  # match2 = {'id' : 222, 'team0' : 3, 'team1' : 2, 'score0' : 1, 'score1' : 3, 'date' : '2048-01-01 00:00:00'}
  if match['team0'] == team_id or match['team1'] == team_id :
    score = match['score0'] - match['score1']
    # print (score)
    if team_id == match['team0'] and score > 0 or team_id == match['team1'] and score < 0:
      return True
    else:
      return False
  return False


def team_loses_match(team_id, match):
  if match['team0'] == team_id or match['team1'] == team_id :
    score = match['score0'] - match['score1']
    if team_id == match['team0'] and score < 0 or team_id == match['team1'] and score > 0:
      return True
    else:
      return False
  return False


def team_draws_match(team_id, match):
  if match['team0'] == team_id or match['team1'] == team_id :
    score = match['score0'] - match['score1']
    if score == 0 :
      return True
    else:
      return False
  return False


def goal_for_count_during_a_match(team_id, match):
  if match['team0'] == team_id : return match['score0']
  elif match['team1'] == team_id : return match['score1']
  return 0


def goal_against_count_during_a_match(team_id, match):
  if match['team0'] == team_id : return match['score1']
  elif match['team1'] == team_id : return match['score0']
  return 0


def goal_for_count(team_id, matches):
  matches = data.matches()
  total = 0
  x = 0
  for row in data.matches(): 
    if matches[x]['team0'] == team_id : total += goal_for_count_during_a_match(team_id, matches[x])
    elif matches[x]['team1'] == team_id : total += goal_for_count_during_a_match(team_id, matches[x])
    x += 1
  
  return total

def goal_against_count(team_id, matches):
  matches = data.matches()
  total = 0
  x = 0
  for row in data.matches(): 
    if matches[x]['team0'] == team_id : total += goal_against_count_during_a_match(team_id, matches[x])
    elif matches[x]['team1'] == team_id : total += goal_against_count_during_a_match(team_id, matches[x])
    x += 1
  
  return total


def won_match_count(team_id, matches):
  matches = data.matches()
  total = 0
  x = 0
  for row in data.matches(): 
    if matches[x]['team0'] == team_id : total += team_wins_match(team_id, matches[x])
    elif matches[x]['team1'] == team_id : total += team_wins_match(team_id, matches[x])
    x += 1
  
  return total


def lost_match_count(team_id, matches):
  matches = data.matches()
  total = 0
  x = 0
  for row in data.matches(): 
    if matches[x]['team0'] == team_id : total += team_loses_match(team_id, matches[x])
    elif matches[x]['team1'] == team_id : total += team_loses_match(team_id, matches[x])
    x += 1
  
  return total


def draw_count(team_id, matches):
  matches = data.matches()
  total = 0
  x = 0
  for row in data.matches(): 
    if matches[x]['team0'] == team_id : total += team_draws_match(team_id, matches[x])
    elif matches[x]['team1'] == team_id : total += team_draws_match(team_id, matches[x])
    x += 1
  
  return total


def ranking_row(team_id, matches):
  teams = data.teams()
  # for row in matches:
  #   dico. = {}
  match_played_count = 0
  x = 0
  for row in matches:
    if team_id == matches[x]['team0'] or team_id == matches[x]['team1'] : match_played_count += 1
    x += 1
    return {'team_id': teams[team_id], 
            'match_played_count': match_played_count, 
            'won_match_count': won_match_count(team_id, matches), 
            'lost_match_count': lost_match_count(team_id, matches), 
            'draw_count': draw_count(team_id, matches), 
            'goal_for_count': goal_for_count(team_id, matches), 
            'goal_against_count': goal_against_count(team_id, matches), 
            'goal_difference': goal_for_count(team_id, matches) - goal_against_count(team_id, matches), 
            'points': points(won_match_count(team_id, matches), draw_count(team_id, matches)) }


def unsorted_ranking(teams, matches):
  return []


def sorting_key(row):
  return (0, 0, 0)


def sorted_ranking(teams, matches):
  return []