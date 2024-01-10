import streamlit as st
from streamlit_extras.switch_page_button import switch_page

name = ""
password = ""

st.set_page_config(
     initial_sidebar_state="collapsed" 
)

# Create an empty container
placeholder = st.empty()

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your Information")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Start")

if submit and name != "" and password != "":
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    st.session_state.id = name+password
    switch_page("chat")
elif submit and name != "" or password != "":
    st.error("Login failed")
