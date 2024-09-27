import streamlit as st
from main import chat
import time
from db import create_tables

# Initialize database and tables
create_tables()

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_message' not in st.session_state:
    st.session_state.user_message = ""

st.title("LLM Psychiatrist chat")


def parse_groq_stream(stream):
    word = ""
    for chunk in stream:
        for char in chunk:
            if char.isspace():  # Check if the character is a space
                if word:
                    yield word
                    word = ""
            else:
                word += char
    if word:  # Yield the last word if there is no space after it
        yield word


def display_messages():
    for sender, message in st.session_state.messages:
        if sender == 'user':
            st.markdown(
                f"<div style='display: flex; justify-content: flex-end; margin: 10px 0;'>"
                f"<div style='background-color: #007bff; color: white; padding: 10px; border-radius: 10px; max-width: 70%;'>{message}</div>"
                f"</div>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div style='display: flex; justify-content: flex-start; margin: 10px 0;'>"
                f"<div style='background-color: #28a745; color: white; padding: 10px; border-radius: 10px; max-width: 70%;'>{message}</div>"
                f"</div>",
                unsafe_allow_html=True)
            
def hide_sidebar_permanently():
    """ Function to hide the Streamlit sidebar permanently """
    hide_sidebar_style = """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)


def send_message(user_message):

    if user_message:
        st.session_state.messages.append(('user', user_message))

        # Display user message immediately
        # st.markdown(
        #     f"<div style='display: flex; justify-content: flex-end; margin: 10px 0;'>"
        #     f"<div style='background-color: #007bff; color: white; padding: 10px; border-radius: 10px; max-width: 70%;'>{user_message}</div>"
        #     f"</div>",
        #     unsafe_allow_html=True)

        display_messages()

        # Create a container for the bot's response
        bot_response_container = st.empty()
        bot_response = ""

        # Temporary list to hold bot messages during streaming
        temp_bot_response = []

        # Process the conversation stream and update the bot response container
        for word in parse_groq_stream(chat(user_message)):
            bot_response += word + " "
            temp_bot_response.append(word)
            bot_response_container.markdown(
                f"<div style='display: flex; justify-content: flex-start; margin: 10px 0;'>"
                f"<div style='background-color: #28a745; color: white; padding: 10px; border-radius: 10px; max-width: 70%;'>{' '.join(temp_bot_response)}</div>"
                f"</div>",
                unsafe_allow_html=True)
            time.sleep(0.2)  # Simulate streaming delay

        st.session_state.messages.append(('bot', bot_response.strip()))

        # Clear the input box by setting the user message to an empty string
        st.session_state.user_message = ""


user_message = st.chat_input("Type Something Here")

if user_message:
    send_message(user_message)
