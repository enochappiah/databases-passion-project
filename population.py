import pandas as pd  
import sqlite3
import numpy as np 
import mysql.connector as sql
import os

# Connect to the SQLite database
conn = sqlite3.connect('/Users/enochappiah/school-tings/JHU/senior-year/fall/Databases/final-project/databases-passion-project/database.sqlite')

# Load tables into pandas DataFrames
country_scope: list = [1729, 4769, 7809, 10257, 21518] # England, France, Germany, Italy, Spain

math_country = pd.read_sql_query("SELECT * FROM Country WHERE id IN (1729, 4769, 7809, 10257, 21518)", conn)
math_league = pd.read_sql_query("SELECT * FROM League WHERE id IN (1729, 4769, 7809, 10257, 21518)", conn)
math_match = pd.read_sql_query("SELECT * FROM Match WHERE country_id IN (1729, 4769, 7809, 10257, 21518)", conn)
math_player = pd.read_sql_query("SELECT * FROM Player", conn)
math_player_attributes = pd.read_sql_query("SELECT * FROM Player_Attributes", conn)
math_team = pd.read_sql_query("SELECT * FROM Team", conn)
math_team_attributes = pd.read_sql_query("SELECT * FROM Team_Attributes", conn)



# drop rows where the column date is less than 2014 and more than 2016

# MATCH TABLE
math_match = math_match[math_match['date'] >= '2014-01-01']
math_match = math_match[math_match['date'] <= '2016-12-31']

skip_column_names = ["home_player_X1", "home_player_X2", "home_player_X3", "home_player_X4", "home_player_X5", 
    "home_player_X6", "home_player_X7", "home_player_X8", "home_player_X9", "home_player_X10", 
    "home_player_X11", "away_player_X1", "away_player_X2", "away_player_X3", "away_player_X4", 
    "away_player_X5", "away_player_X6", "away_player_X7", "away_player_X8", "away_player_X9", 
    "away_player_X10", "away_player_X11", "home_player_Y1", "home_player_Y2", "home_player_Y3", 
    "home_player_Y4", "home_player_Y5", "home_player_Y6", "home_player_Y7", "home_player_Y8", 
    "home_player_Y9", "home_player_Y10", "home_player_Y11", "away_player_Y1", "away_player_Y2", 
    "away_player_Y3", "away_player_Y4", "away_player_Y5", "away_player_Y6", "away_player_Y7", 
    "away_player_Y8", "away_player_Y9", "away_player_Y10", "away_player_Y11", "B365H", "B365D", "B365A", "BWH", "BWD", "BWA", 
    "IWH", "IWD", "IWA", "LBH", "LBD", "LBA", 
    "PSH", "PSD", "PSA", "WHH", "WHD", "WHA", 
    "SJH", "SJD", "SJA", "VCH", "VCD", "VCA", 
    "GBH", "GBD", "GBA", "BSH", "BSD", "BSA", "goal", "shoton", "shotoff", "foulcommit", "card", "cross", "corner", "possession"]

# remove these columns from the match table
math_match = math_match.drop(columns=skip_column_names)




# PLAYER_ATTRIBUTES TABLE
math_player_attributes = math_player_attributes[math_player_attributes['date'] >= '2014-01-01']
math_player_attributes = math_player_attributes[math_player_attributes['date'] <= '2016-12-31']


# TEAM_ATTRIBUTES TABLE
math_team_attributes = math_team_attributes[math_team_attributes['date'] >= '2014-01-01']
math_team_attributes = math_team_attributes[math_team_attributes['date'] <= '2016-12-31']

# get the max overall rating for each player
math_player_attributes = math_player_attributes.sort_values('overall_rating', ascending=False).drop_duplicates('player_api_id')

# merge the player_attributes table with the player table to get players from 2014-2016
math_player = pd.merge(math_player, math_player_attributes["player_api_id"], on="player_api_id", how="inner")

# create csv files for each table
math_country.to_csv('MATHIEN_DATASET/country.csv', index=False)
math_league.to_csv('MATHIEN_DATASET/league.csv', index=False)
math_match.to_csv('MATHIEN_DATASET/match.csv', index=False)
math_player.to_csv('MATHIEN_DATASET/player.csv', index=False)
math_player_attributes.to_csv('MATHIEN_DATASET/player_attributes.csv', index=False)
math_team.to_csv('MATHIEN_DATASET/team.csv', index=False)
math_team_attributes.to_csv('MATHIEN_DATASET/team_attributes.csv', index=False)


# clean up MATHEIN _Dataset  - specfically player_attributes to only include the entry of a player's highest overall rating season
# clean up the datasets to not include data that does not overlap (OVERLAP IS 2014 -2016) 


#TECHNIKA DATASET CLEANUP
unwanted_columns = ["deep","ppda"]
tech_team_stats = pd.read_csv('TECHNIKA_DATASET/teamstats.csv')
if 'deep' in tech_team_stats.columns:
    tech_team_stats = tech_team_stats.drop(columns=unwanted_columns)
tech_team_stats = tech_team_stats[tech_team_stats['date'] >= '2014-01-01']
tech_team_stats = tech_team_stats[tech_team_stats['date'] <= '2016-12-31']
tech_team_stats.to_csv('TECHNIKA_DATASET/new_teamstats.csv', index=False)

unwanted_columns = ["BWH","BWD","BWA","IWH","IWD","IWA","PSH","PSD","PSA","WHH","WHD","WHA","VCH","VCD","VCA","PSCH","PSCD","PSCA"]
tech_games = pd.read_csv('TECHNIKA_DATASET/games.csv')
if 'BWH' in tech_games.columns:
    tech_games = tech_games.drop(columns=unwanted_columns)
tech_games = tech_games[tech_games['date'] >= '2014-01-01']
tech_games = tech_games[tech_games['date'] <= '2016-12-31']
game_ids = tech_games['gameID']
tech_games.to_csv('TECHNIKA_DATASET/new_games.csv', index=False)

# math_player = pd.merge(math_player, math_player_attributes["player_api_id"], on="player_api_id", how="inner")

tech_appearances = pd.read_csv('TECHNIKA_DATASET/appearances.csv')
tech_appearances = tech_appearances[tech_appearances['gameID'].isin(game_ids)]
player_ids = tech_appearances['playerID']
tech_appearances.to_csv('TECHNIKA_DATASET/new_appearances.csv', index=False)


tech_shots = pd.read_csv('TECHNIKA_DATASET/shots.csv')
tech_shots = tech_shots[tech_shots['gameID'].isin(game_ids)]
tech_shots.to_csv('TECHNIKA_DATASET/new_shots.csv', index=False)

tech_player = pd.read_csv('TECHNIKA_DATASET/new_players.csv',encoding='ISO-8859-1', encoding_errors='ignore')
tech_player = tech_player[tech_player['playerID'].isin(player_ids)]
tech_player.to_csv('TECHNIKA_DATASET/new_players.csv', index=False)







