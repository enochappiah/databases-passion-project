import pandas as pd  
import sqlite3
import numpy as np 
import mysql.connector as sql
import os

# Connect to the SQLite database
conn = sqlite3.connect('/Users/enochappiah/school-tings/JHU/senior-year/fall/Databases/final-project/databases-passion-project/database.sqlite')

# Load tables into pandas DataFrames
country = pd.read_sql_query("SELECT * FROM Country", conn)
league = pd.read_sql_query("SELECT * FROM League", conn)
match = pd.read_sql_query("SELECT * FROM Match", conn)
player = pd.read_sql_query("SELECT * FROM Player", conn)
player_attributes = pd.read_sql_query("SELECT * FROM Player_Attributes", conn)
team = pd.read_sql_query("SELECT * FROM Team", conn)
team_attributes = pd.read_sql_query("SELECT * FROM Team_Attributes", conn)

# create csv files for each table
country.to_csv('country.csv', index=False)
league.to_csv('league.csv', index=False)
match.to_csv('match.csv', index=False)
player.to_csv('player.csv', index=False)
player_attributes.to_csv('player_attributes.csv', index=False)
team.to_csv('team.csv', index=False)
team_attributes.to_csv('team_attributes.csv', index=False)



