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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7= st.tabs(['Havvand', 'Ekstremregn og skybrud', 'Flyderetning', 'Gummistøvleindeks', 'Grundvand', 'Vandløb', 'Klimaatlas'])

    ############################# TAB 1 ###############################################################################

    # Hent lag og stilarter fra filen
    layers_styles = pd.read_csv('https://raw.githubusercontent.com/Mikkel-schmidt/Klimadata/master/layers_and_styles.csv', sep=';')
    #st.write(layers_styles)

    # Create a selectbox for layers (frontend-friendly names)
    selected_layer_name = tab1.selectbox('Vælg et lag', layers_styles['layer_name'].unique(), index=2, key="layer_select")

    # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
    selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]

    # Filter stilarterne baseret på valgte lag
    filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]

    # Create a selectbox for styles (frontend-friendly names)
    selected_style_name = tab1.selectbox('Vælg en stil', filtered_styles['style_name'], index=0, key="style_select")

    # Find den tilsvarende style-værdi (backend value) baseret på valgt stil-navn
    selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

    # Display selected options
    tab1.write(f'Valgt lag: {selected_layer_name}')
    tab1.write(f'Valgt stil: {selected_style_name}')

    tab1.write(f'Valgt lag: {selected_layer_value}')
    tab1.write(f'Valgt stil: {selected_style_value}')

    # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
    m = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

    # Tilføj en markør ved den fundne adresse, hvis tilgængelig
    if location:
        folium.Marker([latitude, longitude], popup=adresse).add_to(m)

    # WMS-serverens URL
    wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

    # Tilføj et baselayer
    folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m)

    # Tilføj WMS-lag med backend-lag og stil værdier
    folium.raster_layers.WmsTileLayer(
        url=wms_url,
        name=f"{selected_style_name}",  # Navn der vises i lagvælgeren (frontend-friendly)
        layers=selected_layer_value,  # Navn på WMS-laget (backend value)
        styles=selected_style_value,  # Style for WMS-laget (backend value)
        fmt='image/png',  # Billedformat
        transparent=True,  # Transparent baggrund
        version='1.1.1',  # WMS version
        overlay=True,  # Sæt overlay til True
        control=True,  # Vis kontrolelement for at vælge lag
        show=True,
    ).add_to(m)

    # Tilføj kontrolpanel til at vælge mellem lagene
    folium.LayerControl(position='topright', collapsed=False).add_to(m)

    with tab1:
        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m, width=1200, height=700)
