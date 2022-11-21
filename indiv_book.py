import streamlit as st
import pandas as pd
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
import sessionstate
from pymongo import MongoClient
import certifi
import ast
from ast import literal_eval
import plotly.express as px
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

'''
page 2 
'''
@st.cache(suppress_st_warning=True,show_spinner=False)
def load_data(filename):
    df = pd.read_csv(filename)
    return df

@st.cache(suppress_st_warning=True,show_spinner=False)
def plotly_chart(sentiment):
    fig2 = go.Figure(go.Indicator(
        mode = "delta",
        value = sentiment,
        delta = {'reference': 0}, #above 0 : +ve growth
        domain = {'x': [0, 1], 'y': [0, 1]}
        ))
    fig2.update_layout(
    autosize=False,
    width=600,
    height=300,
    margin=dict(
        l=130,
        r=50,
        b=0,
        t=0,
    ),
    )
    return fig2

#combine df with mongodb data
@st.cache(suppress_st_warning=True,show_spinner=False)
def final_data(df,isbn):
    ca = certifi.where()
    client = MongoClient(
        "mongodb+srv://tartiniglia:W.I.T.C.H.@atlascluster.tv8xjir.mongodb.net/?retryWrites=true&w=majority",
        serverSelectionTimeoutMS=5000, tlsCAFile=ca)
    db = client["bookEater"]
    book_collection = db["Books"] 
    try:
        book_data = book_collection.find({"ISBN": isbn})[0]
        temp = pd.DataFrame()
        temp.loc[0,'ISBN'] = book_data['ISBN']
        temp.loc[0,'URL'] = book_data['URL']
        temp.loc[0,'Review'] = str(book_data['Review'])
        temp.loc[0,'Genre'] = str(book_data['Genre'])
        temp.loc[0,'Summary'] = str(book_data['Summary'])
    #get data from mongodb --> convert to df --> then merge with books.csv based on ISBN: 
        book_df = df[df['ISBN']==isbn]
        final_book_data = temp.merge(book_df,on='ISBN',how='outer')
    except:
        final_book_data = book_df
    return final_book_data

@st.cache(suppress_st_warning=True,show_spinner=False)
def get_sentiments(reviews_list):
    sid_obj = SentimentIntensityAnalyzer()
    sentiments = []
    for sentence in reviews_list:
        sentiment_dict = sid_obj.polarity_scores(sentence)
        sentiments.append(sentiment_dict['compound'])
    return round(np.mean(sentiments),1)



def indiv_book(state):
    state = _get_state()
    book = state.book

    #get data
    df = load_data('Books.csv')
    final_df = final_data(df,book)

   #Back button, title & image 
    name = final_df['Book-Title'][0]
    html_str = f""" <h1 style='text-align: center; color: steelblue;'>{name}</h1> """
    st.markdown(html_str, unsafe_allow_html=True)

    back, _ = st.columns(2)
    temp,title, details = st.columns([4,4,6])
    with back:
    #back button
        if st.button("back"):
            state.book=False
            return
    if not state.book: return #go back to app.py

    with title:
        st.image(final_df['Image-URL-L'][0],width=250)
    
    st.text('')
    # temp1, details, temp2 = st.columns([10,6,8])
    with details:
        html_str = f""" <h2 style='color: maroon;'>Book Details</h2> """
        st.markdown(html_str, unsafe_allow_html=True)
        st.text('')
        st.write('ISBN: ',str(final_df['ISBN'][0]))
        st.write('Author: ',str(final_df['Book-Author'][0]))
        st.write('Year Published: ',str(final_df['Year-Of-Publication'][0]))
        st.write('Published By: ',str(final_df['Publisher'][0]))
    
    #reviews
    summary, genres = st.columns(2)
    with summary:
        html_str = f""" <h2 style='text-align: center; color: maroon;'>Summary</h2> """
        st.markdown(html_str, unsafe_allow_html=True)
        st.write('\n'.join(literal_eval(final_df['Summary'][0])))
    with genres:
        html_str = f""" <h2 style='text-align: center; color: maroon;'>Genre(s)</h2> """
        st.markdown(html_str, unsafe_allow_html=True)
        g = literal_eval(final_df['Genre'][0])
        # g = [item for sublist in g for item in sublist]
        st.write(g)
    reviews, general_sentiment = st.columns(2)
    with reviews:
        html_str = f""" <h2 style='text-align: center; color: maroon;'>Top Reviews</h2> """
        st.markdown(html_str, unsafe_allow_html=True)
        reviews_list = literal_eval(final_df['Review'][0])
        reviews_list = [x for x in reviews_list if x != '']
        count = 1
        with st.expander('See Reviews'):
            for review in reviews_list:
                st.write(count)
                st.write(review)
                count+=1
    with general_sentiment:
        html_str = f""" <h2 style='text-align: center; color: maroon;'>Overall Review Sentiment</h2> """
        st.markdown(html_str, unsafe_allow_html=True)
        sentiment = get_sentiments(reviews_list)
        figure = plotly_chart(sentiment)
        st.plotly_chart(figure)

def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_info.session

def _get_state(hash_funcs=None):
    session = _get_session()
    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = sessionstate._SessionState(session, hash_funcs)
    return session._custom_session_state