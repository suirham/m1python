drop table if exists ranking;
drop table if exists matches;
drop table if exists teams;

CREATE TABLE teams(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL
);
create table matches(
id INTEGER PRIMARY KEY AUTOINCREMENT,
team0 integer not null,
team1 integer not null,
score0 integer not null,
score1 integer not null,
date datetime,
foreign key (team0) references teams(id),
foreign key (team1) references teams(id),
check (team0 != team1),
UNIQUE (team0, team1)
);
create table ranking(
rank int primary key,
team_id integer not null unique,
match_played_count integer not null,
won_match_count integer not null,
lost_match_count integer not null,
draw_count integer not null,
goal_for_count integer not null,
goal_against_count integer not null,
goal_difference integer not null,
points integer not null,
foreign key (team_id) references teams(id)
);
