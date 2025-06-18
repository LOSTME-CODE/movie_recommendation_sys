import streamlit as st
import pickle
import pandas as pd
import requests

# ----- Custom CSS Styling -----
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        [data-testid="stAppViewContainer"] {
            background-color: black;
            text-align: center;
        }  
        [data-testid="stSidebar"] {
            background-color: #1e1e1e;
        }
        .stTextInput, .stSelectbox label {
            color: white !important;
        }

        .stButton>button {
            background-color: black !important;
            color: white !important;
            border-radius: 10px;
            border: 1px solid white;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 22px;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #222 !important;
            color: white !important;
        }

        label[data-testid="stWidgetLabel"] {
            color: white !important;
            font-size: 32px;
            font-weight: bold;
        }

        .poster-img img {
            height: 300px !important;
            width: auto !important;
            display: block;
            margin: auto;
            border-radius: 10px;
            border: 2px solid white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----- Fetch movie poster from API -----
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/200x300?text=No+Image"
    except:
        return "https://via.placeholder.com/200x300?text=No+Image"

# ----- Recommend top 5 similar movies -----
def recommend(movie):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(
            list(enumerate(distances)), reverse=True, key=lambda x: x[1]
        )[1:6]

        recommended_movies = []
        recommended_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_posters
    except IndexError:
        return [], []

# ----- Load Data -----
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# ----- Default state -----
if "show_poster" not in st.session_state:
    st.session_state.show_poster = True

# ----- Title -----
st.markdown(
    """
    <h1 style='
        text-align: center;
        font-size: 47px;
        font-weight: bold;
        color: white;
        margin-bottom: 40px;
        text-shadow: 2px 2px 5px black;
    '>
        🎬 Movie Recommender System
    </h1>
    """,
    unsafe_allow_html=True
)

# ----- Dropdown -----
selected_movie_name = st.selectbox("Select a movie to get recommendations:", movies["title"].values)

# ----- Button Action -----
if st.button("Recommend"):
    st.session_state.show_poster = False
    names, posters = recommend(selected_movie_name)

    if names:
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(
                    f"<div style='text-align: center; padding-bottom: 10px; color: white; font-weight: bold; font-size:20px'>{names[i]}</div>",
                    unsafe_allow_html=True
                )
                st.image(posters[i], width=150)
    else:
        st.warning("No recommendations found. Try another movie.")

# ----- Default Poster -----
if st.session_state.show_poster:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("poster.jpg", caption="Default Poster", width=300)
