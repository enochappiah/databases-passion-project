DELIMITER //
CREATE PROCEDURE MostGamesPlayed()



CREATE PROCEDURE MostTeams

CREATE PROCEDURE HigherThanAttribute(IN Threshold INTEGER, Attribute_Name VARCHAR(15))

CREATE PROCEDURE LowestAvgRating

CREATE PROCEDURE HighestAvgRating

CREATE PROCEDURE HighestAvgBettingOdds()



CREATE PROCEDURE HighestAvgBettingOdds()
BEGIN
    -- Find the team with the highest average betting odds
    SELECT 
        t.team_name AS TeamName,
        AVG(odds.AvgOdds) AS HighestAvgBettingOdds
    FROM 
        TEAM t
    JOIN (
        -- Subquery to calculate average betting odds for each team
        SELECT 
            home_team_id AS team_id,
            (betting_odds_home + betting_odds_draw + betting_odds_away) / 3 AS AvgOdds
        FROM 
            GAME
        UNION ALL
        SELECT 
            away_team_id AS team_id,
            (betting_odds_home + betting_odds_draw + betting_odds_away) / 3 AS AvgOdds
        FROM 
            GAME
    ) odds ON t.team_id = odds.team_id
    GROUP BY 
        t.team_id, t.team_name
    ORDER BY 
        HighestAvgBettingOdds DESC
    LIMIT 1;
END //

DELIMITER ;

--CALL HighestAvgBettingOdds()


DELIMITER //
CREATE PROCEDURE LowestAvgBettingOdds()
BEGIN
    -- Find the team with the lowest average betting odds
    SELECT 
        t.team_name AS TeamName,
        AVG(odds.AvgOdds) AS LowestAvgBettingOdds
    FROM 
        TEAM t
    JOIN (
        -- Subquery to calculate average betting odds for each team
        SELECT 
            home_team_id AS team_id,
            (betting_odds_home + betting_odds_draw + betting_odds_away) / 3 AS AvgOdds
        FROM 
            GAME
        UNION ALL
        SELECT 
            away_team_id AS team_id,
            (betting_odds_home + betting_odds_draw + betting_odds_away) / 3 AS AvgOdds
        FROM 
            GAME
    ) odds ON t.team_id = odds.team_id
    GROUP BY 
        t.team_id, t.team_name
    ORDER BY 
        LowestAvgBettingOdds ASC
    LIMIT 1;
END //

DELIMITER ;

--CALL LowestAvgBettingOdds()


CREATE PROCEDURE GameWithHighestxG()
BEGIN
    -- Find the game with the highest xG and its details
    SELECT 
        g.game_id,
        g.game_date,
        ht.team_name AS HomeTeam,
        at.team_name AS AwayTeam,
        g.home_goals,
        g.away_goals,
        g.betting_odds_home,
        g.betting_odds_draw,
        g.betting_odds_away,
        ts.team_id AS WinningTeamID,
        IF(ts.game_location = 'H', ht.team_name, at.team_name) AS WinningTeam,
        IF(ts.game_location = 'H', at.team_name, ht.team_name) AS LosingTeam,
        MAX(ts.xG) AS HighestxG
    FROM 
        GAME g
    JOIN 
        TEAM_STATS ts ON g.game_id = ts.game_id
    JOIN 
        TEAM ht ON g.home_team_id = ht.team_id
    JOIN 
        TEAM at ON g.away_team_id = at.team_id
    WHERE 
        ts.result = 'W' -- Filter for the winning team in the game
    GROUP BY 
        g.game_id, g.game_date, ht.team_name, at.team_name,
        g.home_goals, g.away_goals, g.betting_odds_home, 
        g.betting_odds_draw, g.betting_odds_away, ts.team_id, ts.game_location
    ORDER BY 
        HighestxG DESC
    LIMIT 1;
END

CREATE PROCEDURE HigherThanAttribute(IN Threshold INTEGER, Attribute_Name VARCHAR(15))
BEGIN
    SELECT P.player_name FROM PLAYER P, PLAYER_ATTRIBUTES PA WHERE P.player_id = PA.player_id AND PA.Attribute_Name > Threshold;
END


CREATE PROCEDURE HighestWinRatio()
BEGIN
    SELECT 
        T.team_id,
        T.team_name,
        COALESCE(SUM(CASE WHEN TS.result = 'W' THEN 1 ELSE 0 END), 0) AS wins,
        COALESCE(SUM(CASE WHEN TS.result = 'L' THEN 1 ELSE 0 END), 0) AS losses,
        CASE 
            WHEN COALESCE(SUM(CASE WHEN TS.result = 'L' THEN 1 ELSE 0 END), 0) = 0 THEN NULL
            ELSE 
                COALESCE(SUM(CASE WHEN TS.result = 'W' THEN 1 ELSE 0 END), 0) 
                / COALESCE(SUM(CASE WHEN TS.result = 'L' THEN 1 ELSE 0 END), 1) 
        END AS win_loss_ratio
        FROM 
            TEAM_STATS TS
        JOIN 
            TEAM T ON TS.team_id = T.team_id
        GROUP BY 
            T.team_id, T.team_name
        ORDER BY 
            win_loss_ratio DESC
        LIMIT 1;

END

CREATE PROCEDURE PlayersWithMostGoals()
BEGIN
    -- Find the player(s) with the most recorded goals
    SELECT 
        p.player_name AS PlayerName,
        COUNT(s.shot_id) AS Goals
    FROM 
        PLAYER p
    JOIN 
        SHOTS s ON p.player_id = s.shooter_id
    WHERE 
        s.shot_result = 'Goal' -- Filter for successful goals
    GROUP BY 
        p.player_id, p.player_name
    HAVING 
        Goals = (
            SELECT 
                MAX(GoalCount) 
            FROM 
                (SELECT 
                    COUNT(s1.shot_id) AS GoalCount
                 FROM 
                    SHOTS s1
                 WHERE 
                    s1.shot_result = 'Goal'
                 GROUP BY 
                    s1.shooter_id) GoalCounts
        );
END