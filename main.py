from typing import Set
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
import re
from PIL import Image

def seconds_to_hms(seconds):
    # convert seconds to hh:mm:ss format
    hours = int(seconds) // 3600
    minutes = (int(seconds) % 3600) // 60
    seconds = int(seconds) % 60
    return f'[{hours:02}:{minutes:02}:{seconds:02}]' \
            f'(https://www.youtube.com/watch?v=tIeHLnjs5U8&t={hours}h{minutes}m{seconds}s)'

def create_timestamps_string(seconds: Set[str]) -> str:
    if not seconds:
        return ''
    timestamps = set(seconds_to_hms(float(sec)) for sec in seconds)
    timestamps_list = list(timestamps)
    timestamps_list.sort()
    timestamps_string = 'relevant timestamps:'
    for i, timestamp in enumerate(timestamps_list):
        timestamps_string += f'\n{i+1}. {timestamp}'
    return timestamps_string

image = Image.open(r'youtube.png')
st.image(image)
st.header('YouTube knowledge assistant')

if (
    'chat_answers_history' not in st.session_state
    and 'user_prompt_history' not in st.session_state
    and 'chat_history' not in st.session_state
):
    st.session_state['chat_answers_history'] = []
    st.session_state['user_prompt_history'] = []
    st.session_state['chat_history'] = []

prompt = st.text_input('Prompt bar', placeholder='Send a message') or st.button(
    'Submit'
)

if prompt:
    with st.spinner('Generating response...'):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state['chat_history']
        )

        timestamps = set(
            [re.search(
                "'start': (.*), 'text'",
                doc.page_content
                ).group(1) for doc in generated_response['source_documents']]
        )

        formatted_response = (
            f"{generated_response['answer']} \n\n {create_timestamps_string(timestamps)}"
        )

        st.session_state.chat_history.append((prompt, generated_response['answer']))
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(formatted_response)

if st.session_state['chat_answers_history']:
    for generated_response, user_query in zip(
        st.session_state['chat_answers_history'],
        st.session_state['user_prompt_history'],
    ):
        message(
            user_query,
            is_user=True,
        )
        message(generated_response)