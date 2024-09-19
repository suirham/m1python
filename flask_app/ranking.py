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
  for row in matches:
    r01 = team_id
    r03 = won_match_count(team_id, matches)
    r04 = lost_match_count(team_id, matches)
    r05 = draw_count(team_id, matches)
    r06 = goal_for_count(team_id, matches)
    r07 = goal_against_count(team_id, matches)
    r08 = goal_for_count(team_id, matches) - goal_against_count(team_id, matches)
    r09 = points(won_match_count(team_id, matches), draw_count(team_id, matches))
    r02 = r03 + r04 + r05
    result = {'team_id': r01, 
            'match_played_count': r02, 
            'won_match_count': r03, 
            'lost_match_count': r04, 
            'draw_count': r05, 
            'goal_for_count': r06, 
            'goal_against_count': r07, 
            'goal_difference': r08, 
            'points': r09}
    return result
    


def unsorted_ranking(teams, matches):
  result = []
  for team in teams:
    row = ranking_row(team['id'], matches)
    result.append(row)
  return result


def sorting_key(row):
  return (row['points'], row['goal_difference'], row['goal_for_count'])


def sorted_ranking(teams, matches):
  ranking = unsorted_ranking(teams, matches)
  ranking = sorted(ranking, key=sorting_key, reverse=True)
  rank = 1
  for row in ranking:
    row['rank'] = rank
    rank += 1
  return ranking

# def sorted_ranking_with_names(teams, ranking):
#   result = []
#   for row in ranking:
    
#   return result