import streamlit as st
import pandas as pd
import sessionstate
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server

'''
page 2 
'''

def indiv_book(state):
    state = _get_state()
    st.write('indiv book page')
    st.write(state.book)
    



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
