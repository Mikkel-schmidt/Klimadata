import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from streamlit_functions import check_password
import branca.colormap as cm

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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Havvand', 'Skybrud og ekstremregn', 'Flyderetning', 'Gummistøvleindeks', 'Grundvand', 'Vandløb', 'Klimaatlas'])

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


        if st.toggle("Indlæs kort", key="reload_map3"):
            reload_map = True
        else:
            reload_map = False

        if reload_map:
            # Display selected options
            # st.write(f'Valgt lag: {selected_layer_name}')
            # st.write(f'Valgt stil: {selected_style_name}')

            # st.write(f'Valgt lag: {selected_layer_value}')
            # st.write(f'Valgt stil: {selected_style_value}')

            # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
            m3 = folium.Map(location=[latitude, longitude], zoom_start=17, crs='EPSG3857')

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
        selected_style_value = 'Default'

        # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
        selected_layer_value1 = layers_styles[layers_styles['style_name'] == selected_style_name]['layer_value'].iloc[0]

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
            layers=selected_layer_value1,  # Navn på WMS-laget (backend value)
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

    with tab5:

        grundvand_styles = pd.read_csv('https://raw.githubusercontent.com/Mikkel-schmidt/Klimadata/master/Grundvand_model.csv', sep=';')
        # Create a selectbox for layers (frontend-friendly names)
        selected_layer_name = st.selectbox('Vælg et lag', grundvand_styles['layer_name'].unique(), index=2, key="layer_select_grundvand")

        # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
        selected_layer_value = grundvand_styles[grundvand_styles['layer_name'] == selected_layer_name]['layer_value'].iloc[0]

        # Filter stilarterne baseret på valgte lag
        #filtered_styles = layers_styles[layers_styles['layer_name'] == selected_layer_name] 

        # Create a selectbox for styles (frontend-friendly names)
        #selected_style_name = st.selectbox('Vælg et gummistøvleindeks', filtered_styles['style_name'], index=10, key="style_select_gummi")

        # Find den tilsvarende style-værdi (backend value) baseret på valgt stil-navn
        selected_style_value = 'default'

        # Find de tilsvarende lag-værdier (backend values) baseret på valgte lag-navn
        #selected_layer_value1 = layers_styles[layers_styles['style_name'] == selected_style_name]['layer_value'].iloc[0]

        # Display selected options
        # st.write(f'Valgt lag: {selected_layer_name}')
        # st.write(f'Valgt stil: {selected_style_name}')

        # st.write(f'Valgt lag: {selected_layer_value}')
        # st.write(f'Valgt stil: {selected_style_value}')

        # Opret et Folium-kort centreret på den fundne adresse eller fallback-location
        m5 = folium.Map(location=[latitude, longitude], zoom_start=15, crs='EPSG3857')

        # Tilføj en markør ved den fundne adresse, hvis tilgængelig
        if location:
            folium.Marker([latitude, longitude], popup=adresse).add_to(m5)

        # Add a colorbar using branca
        colormap = cm.linear.RdYlBu_10.scale(10, 0)  # Change this to fit your data range
        colormap.caption = 'Grundvandsdybde [m]'  # Caption for the colorbar
        colormap.add_to(m5)

        # WMS-serverens URL
        wms_url = 'https://api.dataforsyningen.dk/hip_dtg_10m_100m?service=WMS&request=GetCapabilities&token=' + st.secrets['token']

        # Tilføj et baselayer
        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m5)
        #folium.TileLayer('Stamen Terrain', name="Stamen Terrain").add_to(m5)  # Terrain map
        #folium.TileLayer('Stamen Toner', name="Stamen Toner").add_to(m5)  # High contrast map for clarity


        # Tilføj WMS-lag med backend-lag og stil værdier
        folium.raster_layers.WmsTileLayer(
            url=wms_url,
            name=f"{selected_layer_name}",  # Navn der vises i lagvælgeren (frontend-friendly)
            layers=selected_layer_value,  # Navn på WMS-laget (backend value)
            styles=selected_style_value,  # Style for WMS-laget (backend value)
            fmt='image/png',  # Billedformat
            transparent=True,  # Transparent baggrund
            version='1.1.1',  # WMS version
            overlay=True,  # Sæt overlay til True
            control=True,  # Vis kontrolelement for at vælge lag
            show=True,
            opacity=0.5  # Adjust opacity (if supported)
        ).add_to(m5)

        # Tilføj kontrolpanel til at vælge mellem lagene
        folium.LayerControl(position='topright', collapsed=False).add_to(m5)

        
        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m5, width=1200, height=700)

    with tab6:
        st.write('Mangler data')

    with tab7:

        # Funktion til at konvertere WKT-geometri, og håndtere ikke-strenge
        def safe_wkt_loads(geom):
            if isinstance(geom, str):  # Tjek om værdien er en streng
                return wkt.loads(geom)
            else:
                return None  # Returner None, hvis geometrien ikke er en streng
    

        df_gdf = pd.read_csv("Klimaatlas_gdf.csv")
        df_gdf['SHAPE_geometry'] = df_gdf['SHAPE_geometry'].apply(safe_wkt_loads)
        gdf = gpd.GeoDataFrame(df_gdf, geometry='SHAPE_geometry', crs="EPSG:25832")
        gdf.to_crs(epsg=4326)
        

        # Opret en dictionary for at kortlægge årstiderne til deres numeriske værdier
        season_mapping = {
            "Hele året": 1,
            "Vinter (Dec.-Jan.-Feb.)": 2,
            "Forår (Marts-April-Maj)": 3,
            "Sommer (Juni-Juli-August)": 4,
            "Efterår (Sept.-Okt.-Nov.)": 5
        }

        # Opret en dictionary for visning af værdier
        value_type_mapping = {
            "Absolut": 1,
            "Ændringer": 2
        }

        # Opret en dictionary for scenarier
        scenarie_mapping = {
            "Mellem CO2-niveau": 1,
            "Højt CO2-niveau": 2,
            "Lavt CO2-niveau": 3
        }

        # Opret en dictionary for perioder
        periode_mapping = {
            "Reference (1981-2010)": 1,
            "Start århundrede (2011-2040)": 2,
            "Midt århundrede (2041-2070)": 3,
            "Slut århundrede (2071-2100)": 4
        }

        # Opret en dictionary for percentil
        percentil_mapping = {
            "10%": 1,
            "50%": 2,
            "90%": 3
        }

        # Selectbox for at vælge årstid
        selected_season = st.selectbox(
            "Vælg årstid:",
            options=list(season_mapping.keys())
        )

        # Selectbox for at vælge visningstype
        selected_value_type = st.selectbox(
            "Vælg visningstype:",
            options=list(value_type_mapping.keys())
        )

        # Selectbox for at vælge scenarie
        selected_scenarie = st.selectbox(
            "Vælg scenarie:",
            options=list(scenarie_mapping.keys())
        )

        # Selectbox for at vælge periode
        selected_periode = st.selectbox(
            "Vælg periode:",
            options=list(periode_mapping.keys())
        )

        # Selectbox for at vælge percentil
        selected_percentil = st.selectbox(
            "Vælg percentil:",
            options=list(percentil_mapping.keys())
        )

        # Få de numeriske værdier for hver selectbox
        selected_season_value = season_mapping[selected_season]
        selected_value_type_value = value_type_mapping[selected_value_type]
        selected_scenarie_value = scenarie_mapping[selected_scenarie]
        selected_periode_value = periode_mapping[selected_periode]
        selected_percentil_value = percentil_mapping[selected_percentil]

        # Vis valgte værdier og deres numeriske feltnavne
        st.write(f"Du har valgt årstiden: {selected_season} (Feltnavn: {selected_season_value})")
        st.write(f"Du har valgt visningstype: {selected_value_type} (Feltnavn: {selected_value_type_value})")
        st.write(f"Du har valgt scenarie: {selected_scenarie} (Feltnavn: {selected_scenarie_value})")
        st.write(f"Du har valgt periode: {selected_periode} (Feltnavn: {selected_periode_value})")
        st.write(f"Du har valgt percentil: {selected_percentil} (Feltnavn: {selected_percentil_value})")

        filtered_gdf = gdf.loc[
            (gdf['aarstid'] == selected_season_value) &
            (gdf['visningafvaerdier'] == selected_value_type_value) &
            (gdf['percentil'] == selected_percentil_value) &
            (gdf['scenarie'] == selected_scenarie_value) &
            (gdf['periode'] == selected_periode_value)
        ]
        st.write(filtered_gdf.head())


        # Opret et nyt folium-kort centreret over Danmark
        m = folium.Map(location=[55.6761, 12.5683], zoom_start=10)

        # Tilføj Choropleth lag for at farve kommunerne efter skybrud
        folium.Choropleth(
            geo_data=filtered_gdf.to_json(),  # GeoDataFrame konverteret til GeoJSON
            name="Skybrud",
            data=filtered_gdf,
            columns=["komnavn", "skybrud"],  # Kolonner for kommune og skybrud
            key_on="feature.properties.komnavn",  # Matcher kommunernes navne i GeoJSON
            fill_color="YlGnBu",  # Farveskala
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Skybrud (mm)"
        ).add_to(m)

        # Tilføj kontrol for lag
        folium.LayerControl().add_to(m)

        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m5, width=1200, height=700)


