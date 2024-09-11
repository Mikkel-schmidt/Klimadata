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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7= st.tabs(['Havvand', 'Skybrud og ekstremregn', 'Flyderetning', 'Gummistøvleindeks', 'Grundvand', 'Vandløb', 'Klimaatlas'])

    # Hent lag og stilarter fra filen
    layers_styles = pd.read_csv('https://raw.githubusercontent.com/Mikkel-schmidt/Klimadata/master/layers_and_styles.csv', sep=';')
    #st.write(layers_styles)

    with tab1:
        # Create a selectbox for layers (frontend-friendly names)
        selected_layer_name = 'Havvand på Land' #= tab1.selectbox('Vælg et lag', layers_styles['layer_name'].unique(), index=2, key="layer_select")

        # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]

        # Filter stilarterne baseret på valgte lag
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]

        # Create a selectbox for styles (frontend-friendly names)
        selected_style_name = st.selectbox('Vælg en havniveaustigning', filtered_styles['style_name'], index=10, key="style_select_hav")

        # Find den tilsvarende style-værdi (backend value) baseret på valgt stil-navn
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        # Display selected options
        # st.write(f'Valgt lag: {selected_layer_name}')
        # st.write(f'Valgt stil: {selected_style_name}')

        # st.write(f'Valgt lag: {selected_layer_value}')
        # st.write(f'Valgt stil: {selected_style_value}')

        # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
        m1 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

        # Tilføj en markør ved den fundne adresse, hvis tilgængelig
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m1)

        # WMS-serverens URL
        wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

        # Tilføj et baselayer
        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m1)

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
        ).add_to(m1)

        # Tilføj kontrolpanel til at vælge mellem lagene
        folium.LayerControl(position='topright', collapsed=False).add_to(m1)

        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m1, width=1200, height=700)

    with tab2:
        # Create a selectbox for layers (frontend-friendly names)
        selected_layer_name = 'Skybrud og Ekstremregn' #= tab1.selectbox('Vælg et lag', layers_styles['layer_name'].unique(), index=2, key="layer_select")

        # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]

        # Filter stilarterne baseret på valgte lag
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]

        # Create a selectbox for styles (frontend-friendly names)
        selected_style_name = st.selectbox('Vælg en ekstremregnsmængde', filtered_styles['style_name'], index=3, key="style_select_rain")

        # Find den tilsvarende style-værdi (backend value) baseret på valgt stil-navn
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        # Display selected options
        # st.write(f'Valgt lag: {selected_layer_name}')
        # st.write(f'Valgt stil: {selected_style_name}')

        # st.write(f'Valgt lag: {selected_layer_value}')
        # st.write(f'Valgt stil: {selected_style_value}')

        # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
        m2 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

        # Tilføj en markør ved den fundne adresse, hvis tilgængelig
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m2)

        # WMS-serverens URL
        wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

        # Tilføj et baselayer
        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m2)

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
        ).add_to(m2)

        # Tilføj kontrolpanel til at vælge mellem lagene
        folium.LayerControl(position='topright', collapsed=False).add_to(m2)

        
        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m2, width=1200, height=700)

    with tab3:
        # Create a selectbox for layers (frontend-friendly names)
        selected_layer_name = 'Flow ekstremregn' #= tab1.selectbox('Vælg et lag', layers_styles['layer_name'].unique(), index=2, key="layer_select")

        # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]

        # Filter stilarterne baseret på valgte lag
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]

        # Create a selectbox for styles (frontend-friendly names)
        selected_style_name = 'Flyderetning af vand'#st.selectbox('Vælg en ekstremregnsmængde', filtered_styles['style_name'], index=0, key="style_select_rain")

        # Find den tilsvarende style-værdi (backend value) baseret på valgt stil-navn
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        # Display selected options
        # st.write(f'Valgt lag: {selected_layer_name}')
        # st.write(f'Valgt stil: {selected_style_name}')

        # st.write(f'Valgt lag: {selected_layer_value}')
        # st.write(f'Valgt stil: {selected_style_value}')

        # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
        m3 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

        # Tilføj en markør ved den fundne adresse, hvis tilgængelig
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m3)

        # WMS-serverens URL
        wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

        # Tilføj et baselayer
        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m3)

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
        ).add_to(m3)

        # Tilføj kontrolpanel til at vælge mellem lagene
        folium.LayerControl(position='topright', collapsed=False).add_to(m3)

        
        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m3, width=1200, height=700)

    with tab4:
        # Create a selectbox for layers (frontend-friendly names)
        selected_layer_name = 'Gummistøvleindeks Havvand' #= tab1.selectbox('Vælg et lag', layers_styles['layer_name'].unique(), index=2, key="layer_select")

        # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]

        # Filter stilarterne baseret på valgte lag
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]

        # Create a selectbox for styles (frontend-friendly names)
        selected_style_name = st.selectbox('Vælg et gummistøvleindeks', filtered_styles['style_name'], index=10, key="style_select_gummi")

        # Find den tilsvarende style-værdi (backend value) baseret på valgt stil-navn
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        # Display selected options
        # st.write(f'Valgt lag: {selected_layer_name}')
        # st.write(f'Valgt stil: {selected_style_name}')

        # st.write(f'Valgt lag: {selected_layer_value}')
        # st.write(f'Valgt stil: {selected_style_value}')

        # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
        m4 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

        # Tilføj en markør ved den fundne adresse, hvis tilgængelig
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m4)

        # WMS-serverens URL
        wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

        # Tilføj et baselayer
        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m4)

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
        ).add_to(m4)

        # Tilføj kontrolpanel til at vælge mellem lagene
        folium.LayerControl(position='topright', collapsed=False).add_to(m4)

        
        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m4, width=1200, height=700)



