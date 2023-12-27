import streamlit as st
from PIL import Image
import base64
import pickle
import pandas as pd
import requests
movues_list=pickle.load(open("/home/nitin/Documents/movies_dict.pkl",'rb'))
movies=pd.DataFrame(movues_list)
similarity=pickle.load(open("/home/nitin/Documents/similarty.pkl",'rb'))


def  background_image():
    # Function to convert image file to a base64 string
    def get_base64_of_image(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    # Function to set a background image
    def set_background_image(path):
        base64_string = get_base64_of_image(path)
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{base64_string}");
                background-size: cover;
                background-position: center center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True)
    # Use a local path or URL to an image
    background_image_path = "/Movie_Recommender_System_Project/movies.jpg"
    # Set the background image
    set_background_image(background_image_path)
    # Your Streamlit application code goes below
    st.title("Movie Recommendation System")
background_image()  
#NOTE - <><><><><><><><<><<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<>>>>>>>>>>>>>>
def fetch_poster(move_id):
    api_key="8265bd1679663a7ea12ac168da84d2e8"
    res=requests.get("https://api.themoviedb.org/3/movie/"+str(move_id)+"?api_key="+api_key+"&language=en-US")
    data=res.json()
    return  "https://image.tmdb.org/t/p/w500/"+data['poster_path']
#NOTE -  ========Recommend function=============================================
def recommend(movies_nameas):
    movie_index=movies[movies['title']==movies_nameas].index[0]
    distances=similarity[movie_index]
   
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    # print(movies_list)
    recommend_movies=[]
    recommend_movies_psoters=[]
    for i in movies_list:
        recommend_movies.append(movies.iloc[i[0]].title)
        #!SECTION =fetch the poster from poster  key => 8265bd1679663a7ea12ac168da84d2e8
        recommend_movies_psoters.append(fetch_poster(movies.iloc[i[0]].movie_id))

        
    return recommend_movies,recommend_movies_psoters
        
#NOTE - =======================================================================
def info_fetch(recommend_movies,movies):
    l=[]
    for i in recommend_movies:
        movies['overview'] = movies['overview'].str.replace('1\nName: count, dtype: int64', '')
        ls=movies[movies['title']==i]
        l.append(ls['overview'].value_counts().idxmax())
        

    print(l)
    return l
#NOTE - ===============================================================

select_movies_nameas = st.selectbox(
    'How wud you like to be contacted?',
    movies['title'].values,
     placeholder="Select  Movie Name...",
      index=None,
    )
st.markdown(
            """<div style="position: fixed; bottom: 10px; right: 10px; text-align: right; font-style: italic;">
            Develop By Nitin kumar
            </div>""",
            unsafe_allow_html=True)
if st.button('Recommend'):
    if select_movies_nameas is not None:
        recommend_movies,recommend_movies_psoters=recommend(select_movies_nameas)
        info_list=info_fetch(recommend_movies,movies)
        col1, col2,col3,col4,col5 = st.columns(5)
        for i in range(len(recommend_movies)):
            with col1:
                st.write(recommend_movies[i])
                st.image(recommend_movies_psoters[i])
                st.info(info_list[i], icon="ℹ️")
                

            with col2:
                st.write(recommend_movies[i+1])
                st.image(recommend_movies_psoters[i+1])
                st.info(info_list[i+1], icon="ℹ️")
            with col3:
                st.write(recommend_movies[i+2])
                st.image(recommend_movies_psoters[i+2])
                st.info(info_list[i+2], icon="ℹ️")
                
            with col4:
                st.write(recommend_movies[i+3])
                st.image(recommend_movies_psoters[i+3])
                st.info(info_list[i+3], icon="ℹ️")
            with col5:
                st.write(recommend_movies[i+4])
                st.image(recommend_movies_psoters[i+4])
                st.info(info_list[i+4], icon="ℹ️")
            break       
        else:
            st.error('No Recommendation Found')
#NOTE - ===============================================================================


