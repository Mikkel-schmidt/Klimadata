import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim

import streamlit_folium
from streamlit_functions import check_password

st.set_page_config(layout="wide", page_title="Forside")


if check_password():
    st.success('Login success')

    # Opret en geokodningsfunktion ved hjælp af Nominatim
    geolocator = Nominatim(user_agent="Klimadata")

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


    # Definer bounding box for Danmark i EPSG:25832 (omregnet til grader for visning i folium)
    bbox = [[54.5, 8], [58, 15]]  # (latitude, longitude)

    # Opret et folium-kort centreret på Danmark
    m = folium.Map(location=[location.latitude, location.longitude], zoom_start=17, crs='EPSG3857')  # EPSG3857 bruges af standard webkort

    # WMS-serverens URL
    wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

    # Tilføj et tomt baselayer, så ingen WMS-lag er valgt fra starten
    folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m)

    # Tilføj en markør ved den fundne adresse
    folium.Marker([location.latitude, location.longitude], popup=adresse).add_to(m)

    # Loop gennem listen og tilføj hvert lag til kortet som en base layer (kun ét ad gangen)
    for item in layers_and_styles:
        folium.raster_layers.WmsTileLayer(
            url=wms_url,
            name=item['name'],  # Navn der vises i lagvælgeren
            layers=item['layer_name'],  # Navn på WMS-laget
            styles=item['style'],  # Style for WMS-laget
            fmt='image/png',  # Billedformat
            transparent=True,  # Transparent baggrund
            version='1.1.1',  # WMS version
            overlay=True,  # Sæt overlay til False, så det er et baselayer
            control=True,  # Vis kontrolelement for at vælge lag
            show=False,
        ).add_to(m)  # Vi tilføjer lagene til kortet, men de er ikke aktive ved start

    # Tilføj kontrolpanel til at vælge mellem lagene (baselayers)
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    # Hvis du kører det i en Jupyter Notebook, kan du vise kortet direkte med:
    st_folium(m)
