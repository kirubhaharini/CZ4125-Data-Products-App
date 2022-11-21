import streamlit as st
import pandas as pd
import sessionstate, indiv_book

'''
general UI
'''
import streamlit as st
import pandas as pd
import pipeline
from pipeline import *
import pymongo
from pymongo import MongoClient
import certifi
from PIL import Image
import requests
import time
from collections import Counter
from streamlit_tags import st_tags, st_tags_sidebar

showWarningOnDirectExecution = False
import json, requests, urllib, io
from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder import CrossEncoder
from rake_nltk import Rake

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


genre_embedding_model = SentenceTransformer('whaleloops/phrase-bert')
ranking_model = CrossEncoder('cross-encoder/stsb-TinyBERT-L-4')
keyword_model = Rake()

df = load_data('Books.csv')

#########################
@st.cache(suppress_st_warning=True)
def filter_by_genre(genres):
    isbn_list = []
    for book in book_collection.find():
        genre_list = [g.lower() for g in book['Genre']]
        for gen in genres:
            if gen in genre_list:
                isbn_list.append(book['ISBN'])
                break
    isbn_list = list(set(isbn_list))
    filtered_df = df[df['ISBN'].isin(isbn_list)].reset_index(drop=True)
    return filtered_df

@st.cache(suppress_st_warning=True)
def get_popular_reads():
    pop_ls = []
    for user in user_collection.find():
        pop_ls.append(user['interactions'])
        
    flat_list = [item for sublist in pop_ls for item in sublist]
    isbn_list = []
    for item in Counter(flat_list).most_common(15):
        isbn = item[0]
        isbn_list.append(isbn)
    
    filtered_df = df[df['ISBN'].isin(isbn_list)].reset_index(drop=True)
    return filtered_df

@st.cache(suppress_st_warning=True)
def convert_docs_to_df(docs):
    return_df = pd.DataFrame()
    for doc in docs:
        temp = pd.DataFrame()
        isbn = doc['ISBN']
        temp.loc[0,'ISBN'] = doc['ISBN']
        temp.loc[0,'URL'] = doc['URL']
        temp.loc[0,'Review'] = str(doc['Review'])
        temp.loc[0,'Genre'] = str(doc['Genre'])
        temp.loc[0,'Summary'] = str(doc['Summary'])
        book_df = df[df['ISBN']==isbn]
        final_book_data = temp.merge(book_df,on='ISBN',how='outer') #
        return_df = pd.concat([return_df,final_book_data]).reset_index(drop=True)
    return return_df

# @st.cache(suppress_st_warning=True)
def get_query_results(query):
    results, desired_genres = semanticSearch(
            query = query, 
            book_collection = book_collection, 
            genre_collection = full_genre_collection, 
            genre_embedder = genre_embedding_model, 
            ranking_model = ranking_model, 
            keyword_model = keyword_model,
            stage_one_limit = 200, 
            stage_two_limit = 3, 
            )
    return [results, desired_genres]
###########################

def buttonClick(state,isbn):  #on button click - this is the final callback fn
    state.book = isbn


def show(state):
    username = state.user #guest - can ignore this

    html_str = f""" <h1 style='text-align: center; color: steelblue;'>Book Recommendation App</h1> """
    st.markdown(html_str, unsafe_allow_html=True)
    user_id = username
    st.write('Welcome, ',str(username)+ ' user!')
    
    for col in df.columns:
        df[col] = df[col].astype(str)

    search_bar = st.container()
    search_results = st.container()
    pop_reads = st.container()

    genres = st_tags_sidebar(
        label='Filter by Genre:',
        suggestions=full_genre_collection.find_one()['genre'],
        maxtags=4,
        key='2')


    with search_bar:
        query = st.text_input('Search for your books here')
    

    #initialize variables
    filter = False
    desired_genres = []
    new_df = pd.DataFrame()

    if genres:
        filter = True
        genre_df = filter_by_genre(genres)
        desired_genres = genres
        new_df = pd.concat([genre_df,new_df]).drop_duplicates(subset='ISBN')

    if query:
        filter = True
        output = get_query_results(query)
        results = output[0]
        output_genres = output[1]
        output_genres = [item for sublist in output_genres for item in sublist]
        desired_genres += output_genres
        query_df = convert_docs_to_df(results)
        new_df = pd.concat([query_df,new_df]).drop_duplicates(subset='ISBN')
    
    if len(desired_genres)>0:
        desired_genres = list(set(desired_genres))
        
    if filter:
        new_df = new_df.drop_duplicates(subset='ISBN').reset_index(drop=True)
        new_df = new_df[:5] #show top 5 results
        with search_results:
            st.header('Search Results')
            st.write('Displaying books from related genres: ',', '.join(desired_genres))
            col1, col2, col3 = st.columns(3)
            with col1: 
                for i in range(int(len(new_df)/3)+1):
                    if len(new_df.loc[i,'Book-Title']) > 25:
                        title = new_df.loc[i,'Book-Title'][:25] + '...'
                    else:
                        title = new_df.loc[i,'Book-Title']
                    url = new_df.loc[i,'Image-URL-L']
                    st.image(url,width=160)
                    title_button = st.button(title, key=new_df.loc[i,'ISBN']+str(i)+'result')
                    if title_button:
                        buttonClick(state,new_df.loc[i,'ISBN'])
                    st.write('\n\n')

            with col2:
                for i in range(int(len(new_df)/3)+1,int(len(new_df)/3)*2+1):
                    if len(new_df.loc[i,'Book-Title']) > 25:
                        title = new_df.loc[i,'Book-Title'][:25] + '...'
                    else:
                        title = new_df.loc[i,'Book-Title']
                    url = new_df.loc[i,'Image-URL-L']
                    st.image(url,width=160)
                    title_button = st.button(title, key=new_df.loc[i,'ISBN']+str(i)+'result')
                    if title_button:
                        buttonClick(state,new_df.loc[i,'ISBN'])
                    st.write('\n\n')

            with col3:
                for i in range(int(len(new_df)/3)*2+1,len(new_df)):
                    if len(new_df.loc[i,'Book-Title']) > 25:
                        title = new_df.loc[i,'Book-Title'][:25] + '...'
                    else:
                        title = new_df.loc[i,'Book-Title']
                    url = new_df.loc[i,'Image-URL-L']
                    st.image(url,width=160)
                    title_button = st.button(title, key=new_df.loc[i,'ISBN']+str(i)+'result')
                    if title_button:
                        buttonClick(state,new_df.loc[i,'ISBN'])
                    st.write('\n\n')
        
    with pop_reads:
        st.header('Popular Reads')

        #based on user interactions -- get most pop
        pop_df = get_popular_reads()
        col1, col2, col3 = st.columns(3)

        with col1: #replace df w new_df
            for i in range(0, 13, 3):
                if len(pop_df['Book-Title'][i]) > 25:
                    title = pop_df['Book-Title'][i][:25] + '...'
                else:
                    title = pop_df['Book-Title'][i]
                url = pop_df['Image-URL-L'][i]
                st.image(url,width=160)
                title_button = st.button(title, key=pop_df['ISBN'][i]+str(i))
                if title_button:
                    buttonClick(state,pop_df['ISBN'][i])
                st.write('\n\n')

        with col2:
            for i in range(1, 13, 3):
                if len(pop_df['Book-Title'][i]) > 25:
                    title = pop_df['Book-Title'][i][:25] + '...'
                else:
                    title = pop_df['Book-Title'][i]
                url = pop_df['Image-URL-L'][i]
                st.image(url,width=140)
                title_button = st.button(title, key=pop_df['ISBN'][i]+str(i))
                if title_button:
                    buttonClick(state,pop_df['ISBN'][i])
                st.write('\n\n')

        with col3:
            for i in range(2, 13, 3):
                if len(pop_df['Book-Title'][i]) > 25:
                    title = pop_df['Book-Title'][i][:25] + '...'
                else:
                    title = pop_df['Book-Title'][i]
                url = pop_df['Image-URL-L'][i]
                st.image(url,width=140)
                title_button = st.button(title, key=pop_df['ISBN'][i]+str(i))
                if title_button:
                    buttonClick(state,pop_df['ISBN'][i])
                st.write('\n\n')

        
    #######################################################
   