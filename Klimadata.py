import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim

from streamlit_functions import check_password

st.set_page_config(layout="wide", page_title="Forside")


if check_password():
    st.success('Login success')

    # Opret en geokodningsfunktion ved hjælp af Nominatim
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Angiv adressen
    adresse = st.text_input("Skriv adresse", value="Kongens Nytorv 34, 1050 København")

    # Geokod adressen (find koordinaterne)
    location = geolocator.geocode(adresse)

    # Tjek om geokodningen lykkedes
    if location:
        # Print latitude og longitude
        st.success('Adresse fundet')
        print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
        
        # Opret et Folium-kort centreret på de fundne koordinater
        m = folium.Map(location=[location.latitude, location.longitude], zoom_start=15, crs='EPSG3857')  # EPSG3857 bruges af standard webkort
        
        # Tilføj en markør ved den fundne adresse
        folium.Marker([location.latitude, location.longitude], popup=adresse).add_to(m)
        
        # Gem kortet som en HTML-fil og vis det
        m.save('adresse_geokodning_kort.html')
        
        # Hvis du kører det i en Jupyter Notebook, kan du vise kortet direkte med:
        m
    else:
        st.write("Kunne ikke finde den angivne adresse.")




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