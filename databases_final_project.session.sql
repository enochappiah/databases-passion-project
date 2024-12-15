use soccer_db;

CREATE TABLE IF NOT EXISTS LEAGUE (
    league_id INT PRIMARY KEY,
    league_name VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS TEAM (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(40) NOT NULL,
    league_id INT NOT NULL REFERENCES LEAGUE(league_id)
);


CREATE TABLE IF NOT EXISTS PLAYER (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(40) NOT NULL,
    birthdate VARCHAR(40),
    height INT,
    player_weight INT
);

CREATE TABLE IF NOT EXISTS PLAYER_ATTRIBUTES (
    attribute_id INT PRIMARY KEY,
    player_id INT NOT NULL REFERENCES PLAYER(player_id),
    overall_rating INT,
    potential INT,
    preferred_foot VARCHAR(6),
    attacking_work_rate VARCHAR(5),
    defensive_work_rate VARCHAR(5),
    crossing INT,
    finishing INT,
    heading_accuracy INT,
    short_passing INT,
    volleys INT,
    dribbling INT,
    curve INT,
    free_kick_accuracy INT,
    long_passing INT,
    ball_control INT,
    acceleration INT,
    sprint_speed INT,
    agility INT,
    reactions INT,
    balance INT,
    shot_power INT,
    jumping INT,
    stamina INT,
    strength INT,
    long_shots INT,
    aggression INT,
    interceptions INT,
    positioning INT,
    vision INT,
    penalties INT,
    marking INT,
    standing_tackle INT,
    sliding_tackle INT,
    gk_diving INT,
    gk_handling INT,
    gk_kicking INT,
    gk_positioning INT,
    gk_reflexes INT
);
gameID,leagueID,season,date,homeTeamID,awayTeamID,homeGoals,awayGoals,homeProbability,drawProbability,awayProbability,homeGoalsHalfTime,awayGoalsHalfTime,B365H,B365D,B365A


CREATE TABLE IF NOT EXISTS GAME (
    game_id INT PRIMARY KEY,
    league_id INT NOT NULL REFERENCES LEAGUE(league_id),
    game_date VARCHAR(40),
    home_team_id INT NOT NULL REFERENCES TEAM(team_id),
    away_team_id INT NOT NULL REFERENCES TEAM(team_id),
    home_goals INT,
    away_goals INT,
    home_probability FLOAT,
    draw_probability FLOAT,
    away_probability FLOAT,
    home_goals_halftime INT,
    away_goals_halftime INT,
    betting_odds_home FLOAT,
    betting_odds_draw FLOAT,
    betting_odds_away FLOAT

);

CREATE TABLE IF NOT EXISTS TEAM_STATS (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    team_id INT NOT NULL REFERENCES TEAM(team_id),
    game_id INT NOT NULL REFERENCES GAME(game_id),
    stat_date VARCHAR(40),
    game_location VARCHAR(1),
    goals INT,
    xG FLOAT,
    shots INT,
    shots_on_target INT,
    fouls INT,
    corners INT,
    yellow_cards INT,
    red_cards INT,
    result VARCHAR(1)
);



CREATE TABLE IF NOT EXISTS SHOTS (
    shot_id INT PRIMARY KEY AUTO_INCREMENT,
    game_id INT NOT NULL REFERENCES GAME(game_id),
    shooter_id INT NOT NULL REFERENCES PLAYER(player_id),
    assister_id INT REFERENCES PLAYER(player_id),
    minute INT,
    situation VARCHAR(30),
    lastAction VARCHAR(30),
    shot_type VARCHAR(30),
    shot_result VARCHAR(30),
    xG FLOAT,
    positionX VARCHAR(30),
    positionY VARCHAR(30)
);


Error Code: 1828. Cannot drop column 'assister_id': needed in a foreign key constraint 'shots_ibfk_3'



-- CREATE TABLE IF NOT EXISTS WINS (
--     team_id INT,
--     league_id INT,
--     wins INT,
--     PRIMARY KEY (team_id, league_id),
--     FOREIGN KEY (team_id) REFERENCES TEAM(team_id),
--     FOREIGN KEY (league_id) REFERENCES LEAGUE(league_id)
-- )


