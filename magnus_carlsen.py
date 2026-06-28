import streamlit as st
import pandas as pd
import chess.pgn
from converter.pgn_data import PGNData
from Openix import ChessOpeningsLibrary
import datetime
import io
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('dark_background')


st.title('Search a player\'s games between two dates!')




start_date=st.date_input(label="Start Date",value='1866-01-01', min_value=datetime.date(year=1865, month=12, day=31), max_value=datetime.date(year=2022, month=12, day=31))
end_date=st.date_input(label='End date',value='2021-01-01', max_value=datetime.date(year=2022, month=12, day=31))

start_date=pd.Timestamp(start_date)
end_date=pd.Timestamp(end_date)




game_info_df=pd.read_csv("chess_wc_history_game_info.csv")
#game_moves_df=pd.read_csv("chess_wc_history_moves.csv")
eco_codes_df=pd.read_csv("eco_codes.csv")


#https://stackoverflow.com/questions/37504672/pandas-dataframe-return-first-word-in-string-for-column
game_info_df.winner=game_info_df.winner.str.split(',').str[0]
game_info_df.white=game_info_df.white.str.split(',').str[0]
game_info_df.black=game_info_df.black.str.split(',').str[0]

#https://stackoverflow.com/questions/49110156/finding-unique-combinations-of-columns-from-a-dataframe
game_and_eco=game_info_df[['game_id','eco']].drop_duplicates()

#https://stackoverflow.com/questions/53106428/pandas-merge-returning-only-null-values
game_and_eco_and_name=game_and_eco.merge(eco_codes_df)

games_without_draws=game_info_df[game_info_df.winner!='draw']

#https://stackoverflow.com/questions/43401903/python-order-dataframe-alphabetically
games_without_draws=games_without_draws.sort_values('winner')

players_name=st.selectbox(label="Select player",options=games_without_draws['winner'].unique().tolist())

game_info_df['date_played']=pd.to_datetime(game_info_df['date_played'],format='%Y.%m.%d',errors='coerce')
#game_info_df['date_played']=game_info_df['date_played'].dt.date



player_games=game_info_df[(game_info_df['white']==players_name)|(game_info_df['black']==players_name)]

#for move in range(len(game_moves_df))
#games_requested=player_games[player_games['date_played'].between(start_date,end_date)]
games_requested=player_games[(player_games['date_played']>=start_date)&(player_games['date_played']<=end_date)]



#let's get the number of wins

won_games=len(games_requested[games_requested['winner']==players_name])
drawn_games=len(games_requested[games_requested['winner']=='draw'])
lost_games=len(games_requested[(games_requested['winner']!=players_name)&(games_requested['winner']!='draw')])
total_games=len(games_requested)


winner_countplot=sns.countplot(data=games_requested,x='winner')
#https://stackoverflow.com/questions/26540035/rotate-label-text-in-seaborn
#stackoverflow.com/questions/20335290/matplotlib-plot-set-x-ticks
plt.xticks(rotation=30)
#https://discuss.streamlit.io/t/code-to-create-chart-with-seaborn-objects/36491
st.pyplot(winner_countplot.figure)

st.write(f"Number of games won: {won_games}")
st.write(f"Number of games drawn: {drawn_games}")
st.write(f"Number of games lost: {lost_games}")

st.write(f"Total games: {total_games}")

games_selected_and_openings=games_requested.merge(game_and_eco_and_name)
#games_selected_and_opening_names=pd.concat([games_selected_and_openings,eco_codes_df])

#https://stackoverflow.com/questions/48590268/pandas-get-the-most-frequent-values-of-a-column
top_5_openings=games_selected_and_openings['eco_name'].value_counts()[:5].index.to_list()



st.write("Top 5 openings for selected games:")
st.dataframe(top_5_openings)

plt.figure()
opening_countplot=sns.countplot(data=games_selected_and_openings,x='eco_name')
#https://stackoverflow.com/questions/26540035/rotate-label-text-in-seaborn
#stackoverflow.com/questions/20335290/matplotlib-plot-set-x-ticks
plt.xticks(rotation=90)
plt.figure(figsize=(12,12))
#https://discuss.streamlit.io/t/code-to-create-chart-with-seaborn-objects/36491
st.pyplot(opening_countplot.figure)




st.write('Debugging stuff')
st.dataframe(game_info_df)
st.dataframe(player_games)
st.dataframe(eco_codes_df)


st.dataframe(eco_codes_df)

