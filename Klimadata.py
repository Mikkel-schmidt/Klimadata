import streamlit as st

from streamlit_functions import check_password


if check_password():
    st.success('Login success')