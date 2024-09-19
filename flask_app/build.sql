DROP TABLE IF EXISTS ranking;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS teams;

CREATE TABLE teams(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE matches(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team0 INTEGER NOT NULL,
    team1 INTEGER NOT NULL,
    score0 INTEGER NOT NULL,
    score1 INTEGER NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (team0) REFERENCES teams(id),
    FOREIGN KEY (team1) REFERENCES teams(id),
    CHECK (team0 != team1),
    UNIQUE (team0, team1)
);

CREATE TABLE ranking(
    rank INTEGER NOT NULL PRIMARY KEY, 
    team_id INTEGER NOT NULL UNIQUE, 
    match_played_count INTEGER NOT NULL, 
    won_match_count INTEGER NOT NULL, 
    lost_match_count INTEGER NOT NULL, 
    draw_count INTEGER NOT NULL, 
    goal_for_count INTEGER NOT NULL, 
    goal_against_count INTEGER NOT NULL, 
    goal_difference INTEGER NOT NULL, 
    points INTEGER NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);
