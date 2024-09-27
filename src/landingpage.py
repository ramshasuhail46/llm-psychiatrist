import streamlit as st


st.set_page_config(page_title="Mindify", page_icon="🧠")

from db import create_tables

# Initialize database and tables
create_tables()

if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "access_page" not in st.session_state:
    st.session_state.access_page = None

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

hide_sidebar_permanently()

def check_login_and_redirect(page):
    """Function to check if user is logged in and reroute to the respective page"""
    if st.session_state.logged_in:
        st.switch_page("pages/interface.py")  # Rerun the app to the respective page if logged in
    else:
        st.session_state.show_signup = False  # Ensure user is redirected to login
        st.error("Please log in to access this page.")
        st.switch_page("pages/login.py")  

        

# Set page title
st.title("Mindify: Your Own AI Powered Psychiatrist")

st.header("About Mindify")
st.write("""
Welcome to Mindify, where midify employs zero-shot prompting with state-of-the-art LLMs (e.g., GPT or LLaMA) to simulate psychiatric consultations. Implements carefully crafted prompts to elicit empathetic responses and psychological insights without domain-specific fine-tuning. Features robust content filtering, ethical guidelines enforcement, and a conversational interface designed to handle mental health discussions sensitively.
""")

st.subheader("Key Features:")
st.write("""
- **Zero-Shot Prompting:** Zero-Shot Prompting: Utilizes advanced LLMs (e.g., GPT, LLaMA) to conduct psychiatric consultations without the need for domain-specific fine-tuning, ensuring flexibility and adaptability.
- **Empathetic Responses:** Implements carefully crafted prompts that elicit compassionate and insightful responses, promoting a supportive user experience.
- **Psychological Insights:** Provides valuable psychological insights based on user inputs, helping individuals reflect on their thoughts and feelings.
- **Robust Content Filtering:** Ensures a safe environment by implementing rigorous content filtering mechanisms, preventing harmful or inappropriate interactions.
- **Ethical Guidelines Enforcement:**  Adheres to strict ethical guidelines to promote responsible AI use, safeguarding user wellbeing and privacy.
- **Conversational Interface:** Features an intuitive and user-friendly chat interface designed to facilitate sensitive discussions about mental health.
""")

if st.button("Try the Demo"):
        check_login_and_redirect("demo") 

# Footer
st.write("Thank you for visiting Mindify!")
