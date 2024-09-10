import streamlit as st
import pandas as pd

from streamlit_functions import check_password


if check_password():
    st.success('Login success')

    styles_layers = pd.read_csv('styles_and_layers.csv')
    # Create a selectbox for layers
    selected_layer = st.selectbox('Choose a layer', styles_layers['layer_name'].unique())

    # Filter the styles based on selected layer
    filtered_styles = styles_layers[styles_layers['layer_name'] == selected_layer]['style']

    # Create a selectbox for styles based on the selected layer
    selected_style = st.selectbox('Choose a style', filtered_styles)

    # Display selected options
    st.write(f'Selected Layer: {selected_layer}')
    st.write(f'Selected Style: {selected_style}')