import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    try:
        # API request to get movie details
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=6cf9925dc86fb28bdb254817608400c9&language=en-US')
        data = response.json()

        # If the poster exists, return the valid URL, else return placeholder
        if 'poster_path' in data and data['poster_path'] is not None:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        # Return a placeholder image in case of error
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommendation System")

select_movie_name=st.selectbox('how would you like to connect?',movies['title'].values)
if st.button('Recommend'):
    names,posters=recommend(select_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
