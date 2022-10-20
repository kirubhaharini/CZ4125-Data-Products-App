import one,two,three #ADD pageS HERE
import streamlit as st
   
def page(state):
  
    title = state.page 
    
    st.markdown(f"""<h1 style='text-align: left; color: black;'>{title}</h1>""", unsafe_allow_html=True)

    #leave a gap
    st.write(' ')

    if state.page == 'Login':
        one.one(state)
    elif state.page == '2':
        two.two(state)
    elif state.page == '3':
        three.three(state)


    # #back button

    # state.back = st.button('Select page')
    # if state.back:
    #     state.check = st.write('okok')
    #     state.dropdownMenu='Select' #reset
    #     state.check2 = st.write('ok')
    #     return #temp_trial.main()
   # if not state.activated: return #temp_trial.main() #go back to app.py