from openai import OpenAI
from sqlalchemy.exc import ProgrammingError
import streamlit as st
import json

conn = st.connection('mysql', type='sql')

system_prompt = """
You are a SQL expert who can translate natural language into SQL queries. The queries that you generate should strictly be applied on the following schema:

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
    attribute_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT NOT NULL REFERENCES PLAYER(player_id),
    overall_rating INT,
    potential INT,
    preferred_foot VARCHAR(10),
    attacking_work_rate VARCHAR(10),
    defensive_work_rate VARCHAR(10),
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

You will be translating the natural language query into the most relevant stored procedures listed here:
- HighestAvgBettingOdds(): Returns top 5 teams across Europe with highest average betting odds across all seasons recorded in database. This procedure takes no arguments. 
- LowestAvgBettingOdds(): Returns top 5 teams across Europe with lowest average betting odds across all seasons recorded in database. This procedure takes no arguments.
- GameWithHighestxG(): Returns single game with the highest recorded xG across all seasons recorded in database. This procedure takes no arguments. 
- HighestWinRatio(): Returns single team across Europe with the highest win ratio across all seasons recorded in database. This procedures takes no arguments. 
- LowestWinRatio(): Returns single team across Europe with the lowest win ratio across all seasons recorded in database. This procedures takes no arguments. 

If there is a relevant stored procedure that can be called, create a JSON object with a "procedure" field (e.g. {"procedure": "CALL HighestAvgBettingOdds()"}. If there is NOT a relevant stored procedure to be called, generate a valid SQL SELECT database query based on the database schema provided, and create a JSON object with a "query" field (e.g. {"query": "SELECT..."}. Make sure to NOT violate the rules of the database schema, such as referencing table and/or attribute names that do not exist. If you are unable to find an equivalent stored procedure or generate a valid query without violating database schema, then create a JSON object with an "error" field. 
"""

with st.sidebar:
    # Fill in with your own API key
    openai_api_key = ""

st.title("Databases Final Project")
st.caption("Give a query and receive a corresponding output")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How may I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model="gpt-4o", messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
        ]
    )

    msg = response.choices[0].message.content

    if 'json' in msg:
        msg = msg[7:]
        msg = msg[:-3]

    print(msg)

    msg_dict = json.loads(msg)

    print(msg_dict)


    st.chat_message("assistant").write(msg)

    
    if "query" in msg_dict:
        try:
            query = msg_dict["query"]
            df = conn.query(query, ttl=600)
            if not df.empty:
                st.session_state.messages.append({"role": "assistant", "content": df})
                st.code(msg, language='sql')
                st.dataframe(df, hide_index=True)
        except ProgrammingError as e:
            # print(f"ProgrammingError: {e}")
            st.chat_message("assistant").write("Error occurred when processsing that query. Try a different query as that specific one may not be supported at this time.")
    elif "procedure" in msg_dict:
        try:
            procedure = msg_dict["procedure"]
            df = conn.query(procedure, ttl=600)
            if not df.empty:
                st.session_state.messages.append({"role": "assistant", "content": df})
                st.code(msg, language='sql')
                st.dataframe(df, hide_index=True)
        except ProgrammingError as e:
            # print(f"ProgrammingError: {e}")
            st.chat_message("assistant").write("Error occurred when processsing that query. Try a different query as that specific one may not be supported at this time.")
    else:
        print("Error from OpenAI API", msg_dict["error"])
        st.chat_message("assistant").write(msg_dict["error"])