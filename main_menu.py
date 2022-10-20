# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 23:18:31 2022

@author: Kirubha
"""

import streamlit as st
import page
st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

state = st.session_state 

page_list = ['Select','Login','2','3','4'] #list of other pages
state.ph = st.empty() #placeholder

state.query_params = st.experimental_get_query_params()
# st.write(state.query_params)

if 'page' not in state: #initilize
    state.page = 'pageSelection' #default url query param for selection
    #st.experimental_set_query_params(page='Selectpage') ##### - if initialized: doesnt work!

if 'page' in state.query_params.keys(): #if url is changed directly
    #if state.query_params["page"][0] != 'Selectpage':
    state.page = state.query_params["page"][0] #?page=NCHS
    # st.write(state.page)
# else:


if state.page == 'pageSelection':  #if mainmenu page
    state.dropdownMenu = state.ph.selectbox('page',page_list,index = 0)#,key='page')
    if (state.dropdownMenu != 'Select'): #if selectbox changed
        state.page = state.dropdownMenu
        state.ph.empty()
        page.page(state)
        st.experimental_set_query_params(page=state.page)

else:  #if url changed directly - (state.page!='pageSelection')
  # #  page.page(state)
      pass