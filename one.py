import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml

'''
page 1 - Login 
'''

def one(state):
    with open('config.yaml') as file:
        config = yaml.full_load(file)
    
    #passwords = ['userA','userB']
    #hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        #authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
        st.title('Some content')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

    # if st.session_state["authentication_status"]:
    #     authenticator.logout('Logout', 'main')
    #     st.write(f'Welcome *{st.session_state["name"]}*')
    #     st.title('Some content')
    #     if st.session_state['name'] == 'userA':
    #         st.title('user A logging in')
    #         # NDA.NDA()
    #     elif st.session_state['name'] == 'userB':
    #         st.title('user B logging in')
    #         # BSA.BSA()
    # elif st.session_state["authentication_status"] == False:
    #     st.error('Username/password is incorrect')
    # elif st.session_state["authentication_status"] == None:
    #     st.warning('Please enter your username and password')


'''
    if authentication_status:
    # st.write('Logged in as *%s*' % (name))
        st.title('welcome')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    #elif authentication_status == None:
    #   st.warning('Please enter your username and password')


    if st.session_state['authentication_status']:
    # st.write('Welcome *%s*' % (st.session_state['name']))
        if st.session_state['name'] == 'userA':
            st.title('user A logging in')
            # NDA.NDA()
        elif st.session_state['name'] == 'userB':
            st.title('user B logging in')
            # BSA.BSA()
    elif st.session_state['authentication_status'] == False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] == None:
        st.warning('Please enter your username and password')


'''