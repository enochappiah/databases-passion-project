use soccer_db;

CREATE TABLE IF NOT EXISTS TEAM (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(40) NOT NULL,
    team_city VARCHAR(40) NOT NULL,
    team_country VARCHAR(40) NOT NULL -- Added team_country
)

CREATE TABLE IF NOT EXISTS LEAGUE (
    league_id INT PRIMARY KEY,
    league_name VARCHAR(40) NOT NULL,
    league_country VARCHAR(40) NOT NULL
)

-- CREATE TABLE IF NOT EXISTS WINS (
--     team_id INT,
--     league_id INT,
--     wins INT,
--     PRIMARY KEY (team_id, league_id),
--     FOREIGN KEY (team_id) REFERENCES TEAM(team_id),
--     FOREIGN KEY (league_id) REFERENCES LEAGUE(league_id)
-- )


