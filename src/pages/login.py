import streamlit as st
from db import create_tables, get_db_connection  
import time


class LoginPage:
    def __init__(self):
        self.username = ""
        self.password = ""

    def hide_sidebar_permanently(self):
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

    def authenticate_user(self):
        """ Authenticate the user with the provided username and password. """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (self.username, self.password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def display(self):
        """ Display the login page """
        st.title("Welcome to Mindify")
        self.hide_sidebar_permanently()

        self.username = st.text_input("Username")
        self.password = st.text_input("Password", type="password")

        if st.button("Log in"):
            if self.authenticate_user():
                st.session_state.logged_in = True
                st.success("Logged in successfully!")
                time.sleep(0.5)  # Simulate a small delay
                st.switch_page("pages/interface.py")  # Switch to the search graph page
            else:
                st.error("Incorrect username or password")

        if st.button("Sign Up"):
            st.switch_page("pages/signup.py")  # Switch to signup page



if __name__ == "__main__":
    st.set_page_config(page_title="Mindify", page_icon="🧠")

    login_page = LoginPage()
    login_page.display()