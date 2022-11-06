import streamlit as st
import pandas as pd
import sessionstate, indiv_book

'''
general UI
'''

def show(state):
    username = state.user #guest - ignore this

    st.write('general main page')
    st.write(username)
    
    #######################################################
    ##          WRITE CODE FOR GENERAL UI HERE      ##

        
    #######################################################

    '''
        #Note: for each button: have a unique key. 
        # if button (for each book) is clicked, set the following:
            bookname = book1
            state.book = bookname
        See below for examples:
    '''
    book1 = 'Book 1'
    general = 'general'
    book_btn1 = st.button(book1,key=general+'book1')
    bookname = None #instead of state.book
    if book_btn1:
        bookname = book1
        state.book = bookname

    book2 = 'Book 2'
    book_btn2 = st.button(book2,key=general+'book2')
    if book_btn2:
        bookname = book2
        state.book = bookname
   