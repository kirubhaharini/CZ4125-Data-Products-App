import streamlit as st
import pandas as pd
import sessionstate, indiv_book

'''
general UI
'''

def buttonClick(state,isbn):  #on button click - this is the final callback fn
    state.book = isbn


def show(state):
    username = state.user #guest - ignore this

    st.write('general main page')
    st.write(username + ' user')
    
    #######################################################
    ##          WRITE CODE FOR GENERAL UI HERE      ##

        
    #######################################################
   