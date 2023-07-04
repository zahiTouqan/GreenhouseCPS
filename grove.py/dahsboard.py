# This is a sample Python script.
import pandas as pd
import plotly.express as px

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import ssl
import certifi
from urllib.request import urlopen

request = "https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv"
urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
#read in the file
movies_data = pd.read_csv(urlopen(request, context=ssl.create_default_context(cafile=certifi.where())))
movies_data.info()
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()
year_list = movies_data['year'].unique().tolist()
new_score_rating = st.slider(label="Choose a value:",
                             min_value=1.0,
                             max_value=10.0,
                             value=(3.0, 4.0))
score_info = (movies_data['score'].between(*new_score_rating))
new_genre_list = st.multiselect('Choose Genre:',
                                        genre_list, default = ['Animation',\
                                         'Horror',  'Fantasy', 'Romance'])
year = st.selectbox('Choose a Year',
    year_list, 0)
new_genre_year = (movies_data['genre'].isin(new_genre_list)) \
& (movies_data['year'] == year)
col1, col2 = st.columns(2)
with col1:
    st.write("""#### Lists of movies filtered by year and Genre """)
    dataframe_genre_year = movies_data[new_genre_year]\
    .groupby(['name',  'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width = 400)

with col2:
    st.write("""#### User score of movies and their genre """)
    rating_count_year = movies_data[score_info]\
    .groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'genre', y = 'score')
    st.plotly_chart(figpx)

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
