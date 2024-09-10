import streamlit as st
import pandas as pd

from streamlit_functions import check_password


if check_password():
    st.success('Login success')

    st.write('Hej')

    layers_styles = pd.read_csv('https://raw.githubusercontent.com/Mikkel-schmidt/Klimadata/master/layers_and_styles.csv')
    st.write(layers_styles.head())

    # Create a selectbox for layers
    selected_layer = st.selectbox('Choose a layer', layers_styles['layer_name'].unique())

    # Filter the styles based on selected layer
    filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer]['style']

    # Create a selectbox for styles based on the selected layer
    selected_style = st.selectbox('Choose a style', filtered_styles)

    # Display selected options
    st.write(f'Selected Layer: {selected_layer}')
    st.write(f'Selected Style: {selected_style}')