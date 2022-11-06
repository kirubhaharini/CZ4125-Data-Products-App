import streamlit as st
import pandas as pd
import sessionstate

'''
personalised UI
'''
import streamlit as st
import pandas as pd
import pipeline
import pymongo
from pymongo import MongoClient
import certifi
from PIL import Image
import requests
import time
from streamlit_tags import st_tags, st_tags_sidebar

showWarningOnDirectExecution = False
import json, requests, urllib, io


@st.cache(suppress_st_warning=True)
def load_data(filename):
    df = pd.read_csv(filename)
    return df

ca = certifi.where()
client = MongoClient(
    "mongodb+srv://tartiniglia:W.I.T.C.H.@atlascluster.tv8xjir.mongodb.net/?retryWrites=true&w=majority",
    serverSelectionTimeoutMS=5000, tlsCAFile=ca)
db = client["bookEater"]
book_collection = db["Books"]  # Tiviatis is making new Book collection
full_genre_collection = db["full_genre"]  # this is used for the semanticSearch pipeline
ca = certifi.where()
client2 = MongoClient(
    "mongodb+srv://tanchingfhen:978775!Mj@dataproducts.hcjk1ct.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca)
user_collection = client2["DP"]["users"]
df = load_data('data/Books.csv')


def buttonClick(isbn):
    inter = user_collection.find({"User-ID": '276725'})[0]['interactions']
    inter.append(isbn)
    inter = list(set(inter))

def show(state):
    username = state.user
    st.write('personalised main page')
    st.write(username)

    for col in df.columns:
        df[col] = df[col].astype(str)

    header = st.container()
    pop_reads = st.container()

    keyword = st_tags_sidebar(
        label='Genre:',
        value=full_genre_collection.find_one()['genre'],
        suggestions=full_genre_collection.find_one()['genre'],
        maxtags=4,
        key='2')

    st.sidebar.write(keyword)

    # =============================================================================
    # with st.sidebar:
    #     with st.echo():
    #         st.write("This code will be printed to the sidebar.")
    #
    #     option = st.multiselect(
    #     'Genre',
    #     full_genre_collection.find_one()['genre'])
    # =============================================================================

    # =============================================================================
    #     options = st.multiselect(
    #     'What are your favorite colors',
    #     ['Green', 'Yellow', 'Red', 'Blue'],
    #     ['Yellow', 'Red'])
    #
    #     st.write('You selected:', options)
    # =============================================================================

    # =============================================================================
    #     with st.spinner("Loading..."):
    #         time.sleep(5)
    #     st.success("Done!")
    # =============================================================================

    with header:
        app_name, none, login = st.columns(3)
        # taking book name as input
        with app_name:
            st.header('Book Rec App')
        # taking multiple fiels to get similarity
        with login:
            st.button('Login')
        # =============================================================================
        #         feat = st.selectbox("Select Mode : ",['Book_title', 'Rating', 'Price'])
        #         if st.button('Search'):
        #             tk = 1
        # =============================================================================

        search = st.text_input('Search for your books here')

    user_id = username

    with pop_reads:
        st.header('Popular Reads')

        col1, col2, col3 = st.columns(3)

        with col1:
            # st.write('Where You\'ll Find Me: And Other...')
            for i in range(0, 13, 3):
                if len(df['Book-Title'][i]) > 25:
                    title = df['Book-Title'][i][:25] + '...'
                else:
                    title = df['Book-Title'][i]
                im = Image.open(requests.get(df['Image-URL-L'][i], stream=True).raw)
                new_image = im.resize((180, 200))
                st.image(new_image)
                title_button = st.button(title, key=df['ISBN'][i])
                if title_button:
                    buttonClick(df['ISBN'][i])

                st.write('\n\n')

        with col2:
            for i in range(1, 13, 3):
                if len(df['Book-Title'][i]) > 25:
                    st.write(df['Book-Title'][i][:25] + '...')
                else:
                    st.write(df['Book-Title'][i])
                im = Image.open(requests.get(df['Image-URL-L'][i], stream=True).raw)
                new_image = im.resize((180, 200))
                st.image(new_image)
                st.write('\n\n')

        with col3:
            for i in range(2, 13, 3):
                if len(df['Book-Title'][i]) > 25:
                    st.write(df['Book-Title'][i][:25] + '...')
                else:
                    st.write(df['Book-Title'][i])
                im = Image.open(requests.get(df['Image-URL-L'][i], stream=True).raw)
                new_image = im.resize((180, 200))
                st.image(new_image)
                st.write('\n\n')



    
