import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml

'''
page 1 - Login 
'''

def one(state):
    names = ['groupA','groupB']
    usernames = ['groupA','groupB']
    passwords = ['groupA','groupB']
    hashed_passwords = stauth.hasher(passwords).generate()
    authenticator = stauth.authenticate(names,usernames,hashed_passwords,
        'some_cookie_name','some_signature_key',cookie_expiry_days=30)
    name, authentication_status = authenticator.login('Login','main')



    if authentication_status:
       # st.write('Logged in as *%s*' % (name))
        #st.title('Some content')
        pass
    elif authentication_status == False:
        st.error('Username/password is incorrect')
