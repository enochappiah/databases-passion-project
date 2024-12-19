import pandas as pd  
import sqlite3
import numpy as np 
import mysql.connector
import os



def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('/Users/ahmedhashi/databases-passion-project/database.sqlite')

    # # Load tables into pandas DataFrames
    # country_scope: list = [1729, 4769, 7809, 10257, 21518] # England, France, Germany, Italy, Spain

    # math_country = pd.read_sql_query("SELECT * FROM Country WHERE id IN (1729, 4769, 7809, 10257, 21518)", conn)
    # math_league = pd.read_sql_query("SELECT * FROM League WHERE id IN (1729, 4769, 7809, 10257, 21518)", conn)
    # math_match = pd.read_sql_query("SELECT * FROM Match WHERE country_id IN (1729, 4769, 7809, 10257, 21518)", conn)
    math_player = pd.read_sql_query("SELECT * FROM Player", conn)
    math_player_attributes = pd.read_sql_query("SELECT * FROM Player_Attributes", conn)
    # math_team = pd.read_sql_query("SELECT * FROM Team", conn)
    # math_team_attributes = pd.read_sql_query("SELECT * FROM Team_Attributes", conn)

    conn.close()



    # drop rows where the column date is less than 2014 and more than 2016

    # MATCH TABLE
    # math_match = math_match[math_match['date'] >= '2014-01-01']
    # math_match = math_match[math_match['date'] <= '2016-12-31']

    # skip_column_names = ["home_player_X1", "home_player_X2", "home_player_X3", "home_player_X4", "home_player_X5", 
    #     "home_player_X6", "home_player_X7", "home_player_X8", "home_player_X9", "home_player_X10", 
    #     "home_player_X11", "away_player_X1", "away_player_X2", "away_player_X3", "away_player_X4", 
    #     "away_player_X5", "away_player_X6", "away_player_X7", "away_player_X8", "away_player_X9", 
    #     "away_player_X10", "away_player_X11", "home_player_Y1", "home_player_Y2", "home_player_Y3", 
    #     "home_player_Y4", "home_player_Y5", "home_player_Y6", "home_player_Y7", "home_player_Y8", 
    #     "home_player_Y9", "home_player_Y10", "home_player_Y11", "away_player_Y1", "away_player_Y2", 
    #     "away_player_Y3", "away_player_Y4", "away_player_Y5", "away_player_Y6", "away_player_Y7", 
    #     "away_player_Y8", "away_player_Y9", "away_player_Y10", "away_player_Y11", "B365H", "B365D", "B365A", "BWH", "BWD", "BWA", 
    #     "IWH", "IWD", "IWA", "LBH", "LBD", "LBA", 
    #     "PSH", "PSD", "PSA", "WHH", "WHD", "WHA", 
    #     "SJH", "SJD", "SJA", "VCH", "VCD", "VCA", 
    #     "GBH", "GBD", "GBA", "BSH", "BSD", "BSA", "goal", "shoton", "shotoff", "foulcommit", "card", "cross", "corner", "possession"]

    # # remove these columns from the match table
    # math_match = math_match.drop(columns=skip_column_names)




    # PLAYER_ATTRIBUTES TABLE
    math_player_attributes = math_player_attributes[math_player_attributes['date'] >= '2014-01-01']
    math_player_attributes = math_player_attributes[math_player_attributes['date'] <= '2016-12-31']


    # # TEAM_ATTRIBUTES TABLE
    # math_team_attributes = math_team_attributes[math_team_attributes['date'] >= '2014-01-01']
    # math_team_attributes = math_team_attributes[math_team_attributes['date'] <= '2016-12-31']

    # get the max overall rating for each player
    math_player_attributes = math_player_attributes.sort_values('overall_rating', ascending=False).drop_duplicates('player_api_id')

    # merge the player_attributes table with the player table to get players from 2014-2016
    math_player = pd.merge(math_player, math_player_attributes, on="player_api_id", how="inner")
    #print(math_player)

    # # create csv files for each table
    # math_country.to_csv('MATHIEN_DATASET/country.csv', index=False)
    # math_league.to_csv('MATHIEN_DATASET/league.csv', index=False)
    # math_match.to_csv('MATHIEN_DATASET/match.csv', index=False)
    math_player.to_csv('MATHIEN_DATASET/player_merged.csv', index=False)
    math_player_attributes.to_csv('MATHIEN_DATASET/player_attributes.csv', index=False)
    # math_team.to_csv('MATHIEN_DATASET/team.csv', index=False)
    # math_team_attributes.to_csv('MATHIEN_DATASET/team_attributes.csv', index=False)


    # clean up MATHEIN _Dataset  - specfically player_attributes to only include the entry of a player's highest overall rating season
    # clean up the datasets to not include data that does not overlap (OVERLAP IS 2014 -2016) 


    #TECHNIKA DATASET CLEANUP
    unwanted_columns = ["deep","ppda"]
    tech_team_stats = pd.read_csv('TECHNIKA_DATASET/new_teamstats.csv')
    # tech_team_stats = pd.read_csv('TECHNIKA_DATASET/teamstats.csv')
    # if 'deep' in tech_team_stats.columns:
    #     tech_team_stats = tech_team_stats.drop(columns=unwanted_columns)
    # tech_team_stats = tech_team_stats[tech_team_stats['date'] >= '2014-01-01']
    # tech_team_stats = tech_team_stats[tech_team_stats['date'] <= '2016-12-31']
    # tech_team_stats = tech_team_stats.dropna()
    # tech_team_stats.to_csv('TECHNIKA_DATASET/new_teamstats.csv', index=False)

    unwanted_columns = ["BWH","BWD","BWA","IWH","IWD","IWA","PSH","PSD","PSA","WHH","WHD","WHA","VCH","VCD","VCA","PSCH","PSCD","PSCA"]
    # tech_games = pd.read_csv('TECHNIKA_DATASET/games.csv')
    # if not os.path.exists('TECHNIKA_DATASET/new_games.csv'): 
        
    #     tech_games = tech_games[tech_games['date'] >= '2014-01-01']
    #     tech_games = tech_games[tech_games['date'] <= '2016-12-31']
    #     #remove any rows with missing values
    #     tech_games = tech_games.dropna()
    #     tech_games.to_csv('TECHNIKA_DATASET/new_games.csv', index=False)
    # else:
    #     tech_games = pd.read_csv('TECHNIKA_DATASET/new_games.csv')

    if os.path.exists('TECHNIKA_DATASET/new_games.csv'):
        tech_games = pd.read_csv('TECHNIKA_DATASET/new_games.csv')
    else:
        tech_games = pd.read_csv('TECHNIKA_DATASET/games.csv')
        if 'BWH' in tech_games.columns:
            tech_games = tech_games.drop(columns=unwanted_columns)
        tech_games = tech_games[tech_games['date'] >= '2014-01-01']
        tech_games = tech_games[tech_games['date'] <= '2016-12-31']
        tech_games = tech_games.dropna()
        tech_games.to_csv('TECHNIKA_DATASET/new_games.csv', index=False)

    # math_player = pd.merge(math_player, math_player_attributes["player_api_id"], on="player_api_id", how="inner")

    tech_appearances = pd.read_csv('TECHNIKA_DATASET/appearances.csv')
    tech_appearances = tech_appearances[tech_appearances['gameID'].isin(tech_games['gameID'])]
    player_ids = tech_appearances['playerID']
    tech_appearances.to_csv('TECHNIKA_DATASET/new_appearances.csv', index=False)


    tech_shots = pd.read_csv('TECHNIKA_DATASET/shots.csv')
    tech_shots = tech_shots[tech_shots['gameID'].isin(tech_games['gameID'])]
    # tech_shots = tech_shots[tech_shots['shooterID'].isin(player_ids)]
    tech_shots.to_csv('TECHNIKA_DATASET/new_shots.csv', index=False, na_rep='NULL')

    # #No need to rerun this code

    # test_player = pd.read_csv('MATHIEN_DATASET/player.csv')
    # test_player_attrs = pd.read_csv('MATHIEN_DATASET/player_attributes.csv')

    # test_player_attrs = test_player_attrs[test_player_attrs['date'] >= '2014-01-01']
    # test_player_attrs = test_player_attrs[test_player_attrs['date'] <= '2016-12-31']

    # Joining Players (Technika) and Player_Attributes (Mathien)
    # tech_player = pd.read_csv('TECHNIKA_DATASET/Cleaned_Player_Dataset_2.csv')
    # tech_player = tech_player.drop(tech_player.columns[0], axis=1)
    # tech_player = tech_player[tech_player['playerID'].isin(player_ids)]
    # tech_player.to_csv('TECHNIKA_DATASET/new_players.csv', index=False)

    tech_player_2 = pd.read_csv('TECHNIKA_DATASET/new_players.csv')

    #math_player = math_player[math_player['player_name'].isin(math_player['player_name'])]
    tech_player_3 = pd.merge(tech_player_2, math_player, left_on="name",right_on="player_name", how="inner")
    columns_to_drop = ['id_x','player_api_id','player_name','player_fifa_api_id_x','id_y','player_fifa_api_id_y','date']
    tech_player_3 = tech_player_3.drop(columns=columns_to_drop, errors='ignore').drop_duplicates(subset='playerID', keep='first')
    tech_player_3.to_csv('TECHNIKA_DATASET/cleaned_players_w_attributes.csv', index=False)

    player_ids_2 = tech_player_3['playerID']
    player_ids_2 = player_ids_2.to_list()
    # print(player_ids_2.pop())
    # player_ids_2.append('NULL')

    



    conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='nettspend',
    database='soccer_db'
    )

    cur = conn.cursor()


    


    tech_league = pd.read_csv('TECHNIKA_DATASET/leagues.csv')
    tech_teams = pd.read_csv('TECHNIKA_DATASET/teams.csv')
    # insert_leagues(cur, tech_league)
    # insert_teams(cur, tech_teams)
    # insert_games(cur, tech_games)
    # insert_teamstats(cur, tech_team_stats)

    # print(tech_shots)

    # tech_player = tech_player[tech_player['playerID'].isin(player_ids)]

    df_tech_shots = pd.read_csv('TECHNIKA_DATASET/new_shots.csv', keep_default_na=False)
    print(df_tech_shots['assisterID'][1], type(df_tech_shots['assisterID'][1]))
    print("playerids2 type", type(player_ids_2[1]))
    # compare assiterID (which is a string and .0) to player_ids which is a int
    print(str(player_ids_2[1]) + ".0")
    print(type(df_tech_shots['shooterID'][1]))
    df_tech_shots = df_tech_shots[df_tech_shots['shooterID'].isin(player_ids_2)]

    new_player_ids = convert(player_ids_2)
    new_player_ids.append('NULL')

    #print(df_tech_shots)
    # df_tech_shots = df_tech_shots[df_tech_shots['assisterID'].isin(player_ids_2)]
    # print(player_ids_2.size)
    # df_tech_shots_filtered = filter_tech_shots(df_tech_shots, player_ids_2)
    # print(df_tech_shots_filtered)
    # insert_shots(cur, df_tech_shots, new_player_ids)

    insert_attributes(cur, tech_player_3)

    # insert_players(cur, tech_player_3)

    conn.commit()
    conn.close()

def convert(player_ids):
    new_player_ids = []
    for p_id in player_ids:
        new_player_ids.append(str(p_id) + ".0")
    return new_player_ids


def filter_tech_shots(df, player_ids_2):
    filteredrows = []

    for _, row in df.iterrows():
        shooter_valid = row['shooterID'] in player_ids_2
        assister_valid = row['assisterID'] in player_ids_2 or row['assisterID'] == 'NULL'
        #print(assister_valid)

        if shooter_valid and assister_valid:
            filteredrows.append(row)

    return pd.DataFrame(filteredrows)
    

def insert_shots(cur, df: pd.DataFrame, players_id):
    #df = df.where(pd.notnull(df["assisterID"]), "NA")
    for _, row in df.iterrows():
        # if pd.isna(row["assisterID"]) and pd.isna(row["lastAction"]):
        #     cur.execute("INSERT INTO SHOTS (game_id, shooter_id, minute, situation, shot_type, shot_result, xG, positionX, positionY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['shooterID'], row['minute'], row['situation'], row['shotType'], row['shotResult'], row['xGoal'], row['positionX'], row['positionY']))
        # if pd.isna(row["assisterID"]):
        #     cur.execute("INSERT INTO SHOTS (game_id, shooter_id, minute, situation, lastAction, shot_type, shot_result, xG, positionX, positionY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['shooterID'], row['minute'], row['situation'], row['lastAction'], row['shotType'], row['shotResult'], row['xGoal'], row['positionX'], row['positionY']))
        # if pd.isna(row["lastAction"]):
        #     cur.execute("INSERT INTO SHOTS (game_id, shooter_id, assister_id, minute, situation, shot_type, shot_result, xG, positionX, positionY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['shooter_id'],row["assisterID"], row['minute'], row['situation'], row['shotType'], row['shotResult'], row['xGoal'], row['positionX'], row['positionY']))
        if row['assisterID'] not in players_id:
            continue
        elif row['assisterID'] == 'NULL':
            cur.execute("INSERT INTO SHOTS (game_id, shooter_id, assister_id, minute, situation, lastAction, shot_type, shot_result, xG, positionX, positionY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['shooterID'], None, row['minute'], row['situation'], row['lastAction'] if row["lastAction"] != "NULL" else None, row['shotType'], row['shotResult'], row['xGoal'], row['positionX'], row['positionY']))
        else:
            cur.execute("INSERT INTO SHOTS (game_id, shooter_id, assister_id, minute, situation, lastAction, shot_type, shot_result, xG, positionX, positionY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['shooterID'], row["assisterID"], row['minute'], row['situation'], row['lastAction'] if row["lastAction"] != "NULL" else None, row['shotType'], row['shotResult'], row['xGoal'], row['positionX'], row['positionY']))

        # if row['assisterID'] in players_id:
        #     if row['assisterID'] == 'NULL':
        #         cur.execute("INSERT INTO SHOTS (game_id, shooter_id, assister_id, minute, situation, lastAction, shot_type, shot_result, xG, positionX, positionY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['shooterID'], None, row['minute'], row['situation'], row['lastAction'] if row["lastAction"] != "NULL" else None, row['shotType'], row['shotResult'], row['xGoal'], row['positionX'], row['positionY']))
        #         continue
        #     cur.execute("INSERT INTO SHOTS (game_id, shooter_id, assister_id, minute, situation, lastAction, shot_type, shot_result, xG, positionX, positionY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['shooterID'], row["assisterID"], row['minute'], row['situation'], row['lastAction'] if row["lastAction"] != "NULL" else None, row['shotType'], row['shotResult'], row['xGoal'], row['positionX'], row['positionY']))
        # else:
        #     continue

def insert_games(cur, df: pd.DataFrame):
    for _, row in df.iterrows():
        cur.execute("INSERT INTO GAME (game_id, league_id, game_date, home_team_id, away_team_id, home_goals, away_goals, home_probability, draw_probability, away_probability, home_goals_halftime, away_goals_halftime, betting_odds_home, betting_odds_draw, betting_odds_away) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row['gameID'], row['leagueID'], row['date'], row["homeTeamID"], row["awayTeamID"], row["homeGoals"], row["awayGoals"], row["homeProbability"], row["drawProbability"], row["awayProbability"], row["homeGoalsHalfTime"], row["awayGoalsHalfTime"], row["B365H"], row["B365D"], row["B365A"]))


def insert_teams(cur, df: pd.DataFrame):
    for _, row in df.iterrows():
        cur.execute("INSERT INTO TEAM (team_id, team_name, league_id) VALUES (%s, %s, %s)", (row['teamID'], row['name'], row["leagueID"]))


def insert_leagues(cur, df: pd.DataFrame):
    for _, row in df.iterrows():
        cur.execute("INSERT INTO LEAGUE (league_id, league_name) VALUES (%s, %s)", (row['leagueID'], row['name']))
        
def insert_teamstats(cur, df: pd.DataFrame):
    for _, row in df.iterrows():
        cur.execute("INSERT INTO TEAM_STATS (team_id, game_id, stat_date, game_location, goals, xG, shots, shots_on_target, fouls, corners, yellow_cards, red_cards, result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row["teamID"], row["gameID"], row["date"], row["location"], row["goals"], row["xGoals"], row["shots"], row["shotsOnTarget"], row["fouls"], row["corners"], row["yellowCards"], row["redCards"], row["result"]))
    

def insert_players(cur, df: pd.DataFrame):
    for _, row in df.iterrows():
        cur.execute("INSERT INTO PLAYER (player_id, player_name, birthdate, height, player_weight) VALUES (%s, %s, %s, %s, %s)", (row['playerID'], row['name'], row['birthday'], row['height'], row['weight']))

def insert_attributes(cur, df: pd.DataFrame):
    for _, row in df.iterrows():
        # Assuming `row` is a dictionary containing keys that match the column names in PLAYER_ATTRIBUTES
        cur.execute("""
            INSERT INTO PLAYER_ATTRIBUTES (
                player_id, overall_rating, potential, preferred_foot,
                attacking_work_rate, defensive_work_rate, crossing, finishing,
                heading_accuracy, short_passing, volleys, dribbling, curve,
                free_kick_accuracy, long_passing, ball_control, acceleration,
                sprint_speed, agility, reactions, balance, shot_power, jumping,
                stamina, strength, long_shots, aggression, interceptions,
                positioning, vision, penalties, marking, standing_tackle,
                sliding_tackle, gk_diving, gk_handling, gk_kicking,
                gk_positioning, gk_reflexes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['playerID'], row['overall_rating'], row['potential'],
            row['preferred_foot'], row['attacking_work_rate'], row['defensive_work_rate'],
            row['crossing'], row['finishing'], row['heading_accuracy'],
            row['short_passing'], row['volleys'], row['dribbling'], row['curve'],
            row['free_kick_accuracy'], row['long_passing'], row['ball_control'],
            row['acceleration'], row['sprint_speed'], row['agility'], row['reactions'],
            row['balance'], row['shot_power'], row['jumping'], row['stamina'],
            row['strength'], row['long_shots'], row['aggression'], row['interceptions'],
            row['positioning'], row['vision'], row['penalties'], row['marking'],
            row['standing_tackle'], row['sliding_tackle'], row['gk_diving'],
            row['gk_handling'], row['gk_kicking'], row['gk_positioning'], row['gk_reflexes']
        ))






if __name__ == "__main__":
    main()



