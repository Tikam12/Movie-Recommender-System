import streamlit as st
import requests
import base64
import pandas as pd
import random

st.set_page_config(layout="wide")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:21]:  # Fetching 20 posters
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Add CSS for background image
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('./image-asset.jpeg')

try:
    movies = pd.read_pickle('movies (1).pkl')
except Exception as e:
    print("Error:", e)

try:
    similarity = pd.read_pickle('similarity (1).pkl')
except Exception as e:
    print("Error:", e)

movie_list = movies['title'].values

if 'selected_movie' not in st.session_state or st.session_state.selected_movie is None:
    st.session_state.selected_movie = random.choice(movie_list)

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    index=movie_list.tolist().index(st.session_state.selected_movie)
)

if st.button('Show Recommendation') or 'is_first_load' not in st.session_state:
    st.session_state.is_first_load = False
    st.session_state.selected_movie = selected_movie
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    rows = 4
    cols = 5
    for i in range(rows):
        cols_list = st.columns(cols)
        for j in range(cols):
            index = i * cols + j
            if index < len(recommended_movie_names):
                with cols_list[j]:
                    st.text(recommended_movie_names[index])
                    st.image(recommended_movie_posters[index])
