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
        selected_layer_name = 'Havvand på Land'
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]
        selected_style_name = st.selectbox('Vælg en havniveaustigning', filtered_styles['style_name'], index=10, key="style_select_hav")
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        m1 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m1)

        wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=' + st.secrets['token']
        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m1)
        folium.raster_layers.WmsTileLayer(
            url=wms_url,
            name=f"{selected_style_name}",
            layers=selected_layer_value,
            styles=selected_style_value,
            fmt='image/png',
            transparent=True,
            version='1.1.1',
            overlay=True,
            control=True,
            show=True,
        ).add_to(m1)

        folium.LayerControl(position='topright', collapsed=False).add_to(m1)
        st_folium(m1, width=1200, height=700)

    with tab2:
        selected_layer_name = 'Skybrud og Ekstremregn'
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]
        selected_style_name = st.selectbox('Vælg en ekstremregnsmængde', filtered_styles['style_name'], index=3, key="style_select_rain")
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        m2 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m2)

        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m2)
        folium.raster_layers.WmsTileLayer(
            url=wms_url,
            name=f"{selected_style_name}",
            layers=selected_layer_value,
            styles=selected_style_value,
            fmt='image/png',
            transparent=True,
            version='1.1.1',
            overlay=True,
            control=True,
            show=True,
        ).add_to(m2)

        folium.LayerControl(position='topright', collapsed=False).add_to(m2)
        st_folium(m2, width=1200, height=700)

    with tab3:
        selected_layer_name = 'Flow ekstremregn'
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]
        selected_style_name = 'Flyderetning af vand'
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        m3 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m3)

        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m3)
        folium.raster_layers.WmsTileLayer(
            url=wms_url,
            name=f"{selected_style_name}",
            layers=selected_layer_value,
            styles=selected_style_value,
            fmt='image/png',
            transparent=True,
            version='1.1.1',
            overlay=True,
            control=True,
            show=True,
        ).add_to(m3)

        folium.LayerControl(position='topright', collapsed=False).add_to(m3)
        st_folium(m3, width=1200, height=700)

    with tab4:
        selected_layer_name = 'Gummistøvleindeks Havvand'
        selected_layer_value = layers_styles[layers_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]
        filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name]
        selected_style_name = st.selectbox('Vælg et gummistøvleindeks', filtered_styles['style_name'], index=10, key="style_select_gummi")
        selected_style_value = filtered_styles[filtered_styles['style_name'] == selected_style_name]['style_value'].iloc[0]

        m4 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m4)

        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m4)
        folium.raster_layers.WmsTileLayer(
            url=wms_url,
            name=f"{selected_style_name}",
            layers=selected_layer_value,
            styles=selected_style_value,
            fmt='image/png',
            transparent=True,
            version='1.1.1',
            overlay=True,
            control=True,
            show=True,
        ).add_to(m4)

        folium.LayerControl(position='topright', collapsed=False).add_to(m4)
        st_folium(m4, width=1200, height=700)



