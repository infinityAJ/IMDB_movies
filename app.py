import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import base64

menu_items = [
    'Home',
    'Analyze by Genre',
    'Analyze by Year',
    'Analyze by Runtime',
    'Analyze Raw Data'
    ]

df = pd.read_csv("IMDB-Movie-Data.csv")
st.sidebar.header('Data Analytics of IMDB movies')
st.sidebar.image('movies-camera.png', width=100)

menu = st.sidebar.selectbox("Check other analytics",menu_items)

genre_list = list(set(','.join(list(df.Genre)).split(',')))

if menu == 'Home':
    image = 'movies-disk.png'
    msg = '''Hey there,<br>
this is my project 'IMDB movie data Analytics'.<br>
I aim to describe and visualize the movie data from 2006-2016.'''
    st.title("Welcome to my Project.")
    st.markdown(f"""
        <div style='display: grid; grid-template-columns: 3fr 1fr; column-gap: 1em; padding-top: 12px;'>
            <p style="font-size: 20px;">{msg}</p>
            <img style="width: 200px;" src="data:image/png;base64,{base64.b64encode(open(image, "rb").read()).decode()}"></img>
        </div>
""", unsafe_allow_html = True)
    st.header('Dataset used in the project')
    st.write('  ')
    st.write(df)
    st.markdown(f"""
<hr>
<div style="display: grid; grid-template-columns: 1fr 1fr;">
<h3>Rows: 1000</h3>
<h3>Columns: 13</h3>
</div><hr>
""", unsafe_allow_html= True)
    st.header("Sumarry of DataSet")
    st.write("  ")
    st.write(df.describe())
    for i in df.columns:
        d_type = 'String of Characters' if type(df[i].iloc[0] == str) else 'Numerical'
        st.markdown(f"""
<h2>{i}</h2>
<div style="display: grid; grid-template-columns: 1fr 1fr;">
<h3>Unique Values:  {len(df[i].unique())}</h3>
<h3>Type of Data:  {d_type}</h3>
</div><hr>
""", unsafe_allow_html= True)

if menu == menu_items[1]:
    st.title('Analyze by Genre')
    genre_rev = []
    genre_rate = []
    genre_vote = []
    mov_count = []
    for i in genre_list:
        temp = df[[i in j for j in df.Genre]]
        genre_rev.append(temp['Revenue (Millions)'].sum())
        genre_rate.append(temp['Rating'].sum()/len(temp['Rating']))
        genre_vote.append(temp['Votes'].sum())
        mov_count.append(len(temp))
    st.header('Which Genre has highest number of movies?')
    fig = px.pie(names=genre_list, values=mov_count)
    st.plotly_chart(fig)
    st.write('Maximum movies have Genre \'Drama\'')
    bar_data = pd.DataFrame({'Genre':genre_list, 'Total Revenue':genre_rev, 'Total Votes':genre_vote, 'Average Rating':genre_rate})
    fig1 = px.bar(bar_data, x='Genre', y='Total Revenue')
    st.header('Checking Revenue by Genre')
    st.plotly_chart(fig1)
    st.write('Adventure Genre has highest total Revenue.')
    st.header('Rating according to Genre')
    fig2 = px.bar(bar_data, x='Genre', y='Average Rating')
    st.plotly_chart(fig2)
    st.write('War Genre has highest average rating.')
    st.header('Total Votes by Genre')
    fig3 = px.bar(bar_data, x='Genre', y='Total Votes')
    st.plotly_chart(fig3)
    st.write('Drama Genre has the most Total Votes.')

if menu == menu_items[2]:
    year_count = df.groupby('Year').count()
    st.title("Analyzing movie count by years")
    fig1 = px.bar(year_count, x=year_count.index, y='Title')
    st.plotly_chart(fig1)
    st.write("According to the plot, maximum number of movies were made in 2016")
    year_sum = df.groupby('Year').sum()
    st.title("Revenue Growth in respect to Years.")
    fig2 = px.line(year_sum, x=year_count.index, y='Revenue (Millions)')
    st.plotly_chart(fig2)
    st.write("Revenue of Movies were much more in 2016 then 2006.")

if menu == menu_items[3]:
    rundf = df.groupby('Runtime (Minutes)').count()
    st.title("Analyzing by Runtime")
    st.header('Movies Count by Runtime')
    fig1 = px.bar(rundf, x=rundf.index, y='Title')
    st.plotly_chart(fig1)
    st.write('This plot tells us that most movies have a runtime of 108 minutes.')

def raw_data():
    if genre == 'All':
        movies = df
    else:
        movies = df[[genre in i for i in df.Genre]]
    sortc = st.selectbox("sort by...", "Title,Rating,Votes,Year,Revenue (Millions),Runtime (Minutes)".split(','))
    if sortc == 'Title':
        movies = movies.sort_values(by=[sortc])
    else:
        movies = movies.sort_values(by=[sortc], ascending=False)

    for x in range(movies.shape[0]):
        i = movies.iloc[x]
        st.markdown(f"""
    <div style='border-bottom: 1px solid white;'>
        <h2>{x+1}. {i.Title}</h2>
        <p style='font-size:0.8em;'>{i.Description}</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr;">
            <div>
                <b>Genre: {i.Genre}</b>
                <h4 style='margin: 2px;'>Rating: {i.Rating}/10</h4>
                <h4 style='margin: 2px;'>Year: {i.Year}</h4>
            </div>
            <div>
                <b>Votes: {i.Votes}</b>
                <h4 style='margin: 2px;'>Revenue: {i['Revenue (Millions)']}M</h4>
                <h4 style='margin: 2px;'>Length: {i['Runtime (Minutes)']}Minutes</h4>
            </div>
        </div>
    </div>"""
                    , unsafe_allow_html = True)

if menu == menu_items[3]:
    genres = ['All'] + genre_list
    genre = st.sidebar.selectbox("choose a Genre", genres)
    raw_data()
