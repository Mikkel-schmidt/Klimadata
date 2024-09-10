import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from streamlit_functions import check_password

st.set_page_config(layout="wide", page_title="Forside")

# Function to create map based on selected layer and style
def create_map(latitude, longitude, selected_layer, selected_style):
    # Create a Folium map centered at the address or fallback location
    m = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

    # Add a marker at the found address if available
    if location:
        folium.Marker([latitude, longitude], popup=adresse).add_to(m)

    # WMS server URL with token
    wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

    # Add the selected WMS layer and style
    folium.raster_layers.WmsTileLayer(
        url=wms_url,
        name=f"{selected_layer} {selected_style}",
        layers=selected_layer,
        styles=selected_style,
        fmt='image/png',
        transparent=True,
        version='1.1.1',
        overlay=True,
        control=True,
        show=True,
    ).add_to(m)

    # Add layer control
    folium.LayerControl(position='topright', collapsed=True).add_to(m)
    
    return m

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

    # Track selected layer and style changes in session state
    if 'selected_layer' not in st.session_state:
        st.session_state['selected_layer'] = layers_styles['layer_name'].unique()[0]

    if 'selected_style' not in st.session_state:
        st.session_state['selected_style'] = layers_styles[layers_styles['layer_name'] == st.session_state['selected_layer']]['style'].iloc[0]

    # Create a selectbox for layers
    selected_layer = st.selectbox(
        'Choose a layer',
        layers_styles['layer_name'].unique(),
        index=list(layers_styles['layer_name'].unique()).index(st.session_state['selected_layer']),
        key="layer_select"
    )

    # Filter the styles based on the selected layer
    filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer]['style']

    # Create a selectbox for styles based on the selected layer
    selected_style = st.selectbox(
        'Choose a style',
        filtered_styles,
        index=list(filtered_styles).index(st.session_state['selected_style']),
        key="style_select"
    )

    # Update session state
    st.session_state['selected_layer'] = selected_layer
    st.session_state['selected_style'] = selected_style

    # Force re-creation of the map each time either the layer or style changes
    m = create_map(latitude, longitude, selected_layer, selected_style)

    # Display the updated map
    st_folium(m, width=1200, height=700)
