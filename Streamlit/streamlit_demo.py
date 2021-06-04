import streamlit as st
import pandas as pd 


st.title('Sales Report')

q1_sales = {
    'Jan' : 100,
    'Feb' : 120,
    'Mar' : 300
}

q2_sales = {
    'April' : 400,
    'May': 410,
    'June': 500
}

Section = st.sidebar.radio('Which Section?', ('Text','Charts','Widgets'))
if Section == 'Text':
    q1_df = pd.DataFrame(q1_sales.items(), columns=['Month', 'Amount'])
    q2_df = pd.DataFrame(q2_sales.items(), columns=['Month', 'Amount'])
    st.table(q2_df)
    st.dataframe(q2_df)

elif Section == 'Charts':
    st.bar_chart([q1_sales.values(),q2_sales.values()])

elif Section == 'Widgets':
    st.write(st.slider('Which Quarters', 1,4, (1,2)))
    st.multiselect('Choose quarter',['Q1','Q2','Q3','Q4'])

