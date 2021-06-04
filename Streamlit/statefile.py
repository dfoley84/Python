import json
import os

import streamlit as st
from streamlit.report_thread import get_report_ctx

state = get_report_ctx().session_id + '.json'
if not os.path.isfile(state):
    with open(state, 'w') as f:
        json.dump({'clicks': 0,
                   'text': ''}, f)

with open(state) as f:
    d = json.load(f)
    counter = d['clicks']
    text = d['text']

page = st.sidebar.radio(label='Select page',
                        options=['First', 'Second'])

if page == 'First':
    if st.button('Click me'):
        counter += 1
    st.write(f'The button was clicked {counter} times')
elif page == 'Second':
    text = st.text_area('Message',
                        value=text)

with open(state, 'w') as f:
    json.dump({'clicks': counter,
               'text': text}, f)
