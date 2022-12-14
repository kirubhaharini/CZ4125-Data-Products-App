# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 23:18:31 2022

@author: Kirubha
"""

import streamlit as st
st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

import personalised,general,indiv_book

import sessionstate
import streamlit as st
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
from pymongo import MongoClient
import certifi
    
    
def main():
    state = _get_state() #using sessionstate.py, this allows the app to store and save state variables across pages
    if state.user is None: #initialise
        state.user = False

    if not state.user: #not logged in  
        loginSignup(state)

    else:

        if state.book:
            indiv_book.indiv_book(state)
        else:
            a,b,c = st.columns([1,3,2])
            if (state.user) and (state.user != 'guest'): #logged in already
                personalised.show(state)
                with c: 
                    logout_button = st.button('Logout')
                    if logout_button:
                        state.user = 'guest'
            
            if state.user == 'guest':
                general.show(state)
                with c:
                    login_button = st.button('Login')
                    if login_button:
                        state.user = False
   
    
    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()



def loginSignup(state):

    ca = certifi.where()
    client2 = MongoClient("mongodb+srv://tanchingfhen:978775!Mj@dataproducts.hcjk1ct.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

    user_collection = client2["DP"]["users"]
    usernames = user_collection.distinct('User-ID')
    passwords = user_collection.distinct('password')
    
    forgot_text = st.empty()
    title = st.empty()
    email = st.empty()
    password =  st.empty()
    cola, colb, _ = st.columns(3)
    with cola:
        placeholder = st.empty() #to interchange login&signup button
    with colb:
        forgotpass = st.empty() #checkbox for "forgot password"
    title.title("Book Recommender")
    text_email = email.text_input("Username") #user input
    text_password = password.text_input("Password", type="password") #user input
    

    #Change Login/Signup button depending on the "Already/Don't have an account? Login/Signup" hyperlink
    query_params = st.experimental_get_query_params() #query params that are in the url link
    tabs = ["Login", "Signup"]
    if "tab" in query_params:
        active_tab = query_params["tab"][0]
    else:
        active_tab = "Login"
    if active_tab not in tabs: #default tab is Login-- cntninue as guest?
        active_tab = "Login"  
    non_active_tab = [x for x in tabs if x!=active_tab][0]
    display_text = {"Login": "Already have an account? Login", "Signup":"Don't have an account? Sign up"}
    
    #Here the url in the hyperlink will have the parameter e.g. "?tab=Login" to indicate which page we want
    signup_login_hyperlink = f"""
        <a class="nav-item" href="?tab={non_active_tab}" id="signuploginlink">{display_text[non_active_tab]}</a>
    """
    placeholder_hyperlink = st.empty()
    placeholder_hyperlink.markdown(signup_login_hyperlink, unsafe_allow_html=True)

    guest = st.button("Continue as Guest",key='guestbtn')

    #Functions using firebase signup/login
    def signUp():
        #create users
        while not state.user:
            if (text_email not in usernames):
                user_collection.insert_one({"User-ID": text_email, "password": text_password,'interactions':[]})
                state.user = text_email
            
            else: #if password/email exists
                st.error("Username already exists. Try again!")
                st.stop()
        successful=True
        print("Success .... ")
        st.success("Successfully signed up!")
        email.empty()
        password.empty()
        placeholder.empty()
        placeholder_hyperlink.empty()
        return text_email

    def login():
        while not state.user:
            try:
                user_dict = user_collection.find({"User-ID": text_email})[0] 
                state.user=text_email
            except IndexError as e:
                st.error("Invalid Username/Password. Try again!")
                st.stop()
        successful=True
        print("Success ... ")
        email.empty()
        password.empty()
        placeholder.empty()
        placeholder_hyperlink.empty()
        return text_email

    #Displaying respective buttons depending on the tab 

    if guest:
        #continue as guest
        state.user = 'guest'


    if active_tab == "Login":
        if placeholder.button("Login", key="loginbtn"):
            login() #calling the function
            
    elif active_tab == "Signup":
        if placeholder.button("Sign up", key="signupbutton"):
            signUp() #calling the function


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


if __name__ == "__main__":
    main()
