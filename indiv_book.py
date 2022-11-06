import streamlit as st
import pandas as pd
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
import sessionstate
from pymongo import MongoClient
import certifi

'''
page 2 
'''
@st.cache(suppress_st_warning=True)
def load_data(filename):
    df = pd.read_csv(filename)
    return df

#combine df with mongodb data
@st.cache(suppress_st_warning=True)
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

def indiv_book(state):
    state = _get_state()
    book = state.book

    #get data
    df = load_data('Books.csv')
    final_df = final_data(df,book)

   #Back button, title & image
    back, title, temp = st.columns([1,3,1])
    with back:
    #back button
        if st.button("back"):
            state.book=False
            return
    if not state.book: return #go back to app.py

    with title:
        st.title(final_df['Book-Title'][0])
        st.image(final_df['Image-URL-L'][0])
    with temp:
        pass
    
    ###################### book info here: ######################
    # display other info here 
    # using final_df - only contains 1 row (for the particular book)
    '''
    Useful columns in final df:
    ISBN, Review, Genre, Summary, Book-Title, Book-Author, 
    Year-Of-Publication, Publisher, Image-URL-Lurl
    '''



    #############################################################



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