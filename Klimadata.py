import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
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
        st.success('Adresse fundet')
        latitude, longitude = location.latitude, location.longitude
    else:
        st.write("Kunne ikke finde den angivne adresse.")
        latitude, longitude = 56, 10  # Fallback to Denmark's center if location is not found

    st.header('Klimadata')

    # Hent lag og stilarter fra filen
    layers_styles = pd.read_csv('https://raw.githubusercontent.com/Mikkel-schmidt/Klimadata/master/layers_and_styles.csv')

    # Create a selectbox for layers
    selected_layer = st.selectbox('Choose a layer', layers_styles['layer_name'].unique(), key="layer_select")

    # Filter the styles based on selected layer
    filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer]['style']

    # Create a selectbox for styles based on the selected layer
    selected_style = st.selectbox('Choose a style', filtered_styles, key="style_select")

    # Display selected options
    st.write(f'Selected Layer: {selected_layer}')
    st.write(f'Selected Style: {selected_style}')


    # If the selected layer or style has changed, trigger a rerun
    if st.session_state['selected_layer'] != selected_layer or st.session_state['selected_style'] != selected_style:
        # Update session state
        st.session_state['selected_layer'] = selected_layer
        st.session_state['selected_style'] = selected_style
        st.rerun()  # Trigger full app rerun

    # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
    m = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

    # Tilføj en markør ved den fundne adresse, hvis tilgængelig
    if location:
        folium.Marker([latitude, longitude], popup=adresse).add_to(m)

    # WMS-serverens URL
    wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

    # Tilføj et baselayer
    folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m)

    # Tilføj WMS-lag med valgt lag og stil
    folium.raster_layers.WmsTileLayer(
        url=wms_url,
        name=f"{selected_layer} {selected_style}",  # Navn der vises i lagvælgeren
        layers=selected_layer,  # Navn på WMS-laget
        styles=selected_style,  # Style for WMS-laget
        fmt='image/png',  # Billedformat
        transparent=True,  # Transparent baggrund
        version='1.1.1',  # WMS version
        overlay=True,  # Sæt overlay til True
        control=True,  # Vis kontrolelement for at vælge lag
        show=True,
    ).add_to(m)

    # Tilføj kontrolpanel til at vælge mellem lagene
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    # Vis kortet i Streamlit og opdater det dynamisk
    st_folium(m, width=1200, height=700)
