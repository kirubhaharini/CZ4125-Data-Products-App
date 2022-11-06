import streamlit as st
import pandas as pd
import sessionstate

'''
personalised UI
'''

def show(state):
    username = state.user
    st.write('personalised main page')
    st.write(username)
    
    #######################################################
    ##          WRITE CODE FOR PERSONALISED UI HERE      ##

        
    #######################################################
    

    '''
        #Note: for each button: have a unique key. 
        # if button (for each book) is clicked, set the following:
            bookname = book1
            state.book = bookname
        See below for examples:
    '''
    book1 = 'Book 1'
    personalise = 'personalised'
    book_btn1 = st.button(book1,key=personalise+'book1')
    bookname = None #instead of state.book
    if book_btn1:
        bookname = book1
        state.book = bookname

    book2 = 'Book 2'
    book_btn2 = st.button(book2,key=personalise+'book2')
    if book_btn2:
        bookname = book2
        state.book = bookname
