import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import folium
from folium.raster_layers import WmsTileLayer
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import branca.colormap as cm

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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Havvand', 'Skybrud og ekstremregn', 'Flyderetning', 'Gummistøvleindeks', 'Grundvand', 'Vandløb', 'Klimaatlas'])

    # Hent lag og stilarter fra filen
    layers_styles = pd.read_csv('https://raw.githubusercontent.com/Mikkel-schmidt/Klimadata/master/layers_and_styles.csv', sep=';')
    #st.write(layers_styles)

    with tab1: ############# HAVVAND #######################
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

    with tab2: ############# EKSTREMREGN ###################
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

        st.toggle('Vis kloakoplande', key='Kloakoplande')
        

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

        if st.session_state['Kloakoplande'] == True:
            # Tilføj WMS-lag dynamisk baseret på listen over lag
            folium.raster_layers.WmsTileLayer(
                url='https://geoserver.plandata.dk/geoserver/ows',
                name='Kloakoplande',
                layers='pdk:theme_pdk_kloakopland_vedtaget_v',
                styles='kloakopland_vedtaget',  # Leave empty to test
                fmt='image/png',
                transparent=True,
                version='1.1.1',
                overlay=True,
                control=True,
                opacity=0.5
            ).add_to(m2)

            # URL for signaturforklaringen (legend)
            legend_url = 'https://geoserver.plandata.dk/geoserver/wms?REQUEST=GetLegendGraphic&SERVICE=WMS&VERSION=1.1.1&FORMAT=image/png&LAYER=pdk:theme_pdk_kloakopland_vedtaget_v&STYLE=kloakopland_vedtaget'

            # Tilføj HTML/CSS til legenden i nederste højre hjørne ved hjælp af st.components.v1.html
            legend_html = f'''
            <div style="
            position: fixed;
            bottom: 0px;
            left: 0px;
            z-index: 9999;
            background-color: white;
            border:2px solid grey;
            padding: 0px;
            ">
            <img src="{legend_url}" alt="Legend" style="width: 200px;">
            </div>
            '''



        # Tilføj kontrolpanel til at vælge mellem lagene
        folium.LayerControl(position='topright', collapsed=False).add_to(m2)

        col1, col2 = st.columns([3,1])
        with col1:
            # Vis kortet i Streamlit og opdater det dynamisk
            st_folium(m2, width='100%', height=700)
        with col2:
            # Tilføj signaturforklaringen til kortet som en HTML-element
            st.components.v1.html(legend_html, height=250)

    with tab3: ############# FLOW ##########################

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

    with tab4: ############# GUMMISTØVLE ###################
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

    with tab5: ############# GRUNDVAND #####################

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

    with tab6: ############# VANDLØB #######################
        # Data fra https://oversvommelse.kyst.dk/planperioder/planperiode-2016-2021/plantrin-1/vandloebsoversvoemmelser

        valgt_haendelse = st.selectbox('Vælg et hændelsesinterval:', ['20-års hændelse', '100-års hændelse', '1000-års hændelse'])

        # Create a map centered on Denmark
        m6 = folium.Map(location=[latitude, longitude], zoom_start=12, crs='EPSG3857')

        if valgt_haendelse == '20-års hændelse': haendelse = 'OSD_20aars_40cm'
        elif valgt_haendelse == '1000-års hændelse': haendelse = 'OSD_100aars_40cm'
        elif valgt_haendelse == '1000-års hændelse': haendelse = 'OSD_1000aars_40cm_vandlob'
        else: haendelse = 'OSD_20aars_40cm'

        # WMS server URL
        wms_url = f'https://gis.nst.dk/server/services/ekstern/{haendelse}/MapServer/WMSServer'

        # Tilføj et baselayer
        folium.TileLayer('CartoDB positron', name="CartoDB Positron").add_to(m6)

        # Add Mosaic Layer (0)
        WmsTileLayer(
            url=wms_url,
            name=valgt_haendelse,
            layers='0',  # Layer ID for Mosaic Layer
            styles='default',
            fmt='image/png',
            transparent=True,
            version='1.1.1',
            control=True,
            show=True
        ).add_to(m6)

        # Add Layer Control
        folium.LayerControl().add_to(m6)

        # Display the map
        st_folium(m6, width=1200, height=700)

    with tab7:

        # Funktion til at konvertere WKT-geometri, og håndtere ikke-strenge
        def safe_wkt_loads(geom):
            if isinstance(geom, str):  # Tjek om værdien er en streng
                return wkt.loads(geom)
            else:
                return None  # Returner None, hvis geometrien ikke er en streng
    
        if 'Klimaatlas_gdf' not in st.session_state:
            df_gdf = pd.read_csv("Klimaatlas_gdf.csv")
            df_gdf = df_gdf.loc[df_gdf['percentil'] == 2]
            df_gdf['SHAPE_geometry'] = df_gdf['SHAPE_geometry'].apply(safe_wkt_loads)
            st.session_state['Klimaatlas_gdf'] = df_gdf
        
        
        c0, c1, c2, c3, c4 = st.columns(5)
        c0.subheader('Filtre:')

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
            "Lavt CO2-niveau": 3,
            "Mellem CO2-niveau": 1,
            "Højt CO2-niveau": 2
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
        selected_season = c2.selectbox(
            "Vælg årstid:",
            options=list(season_mapping.keys())
        )

        # Selectbox for at vælge visningstype
        selected_value_type = c3.selectbox(
            "Vælg visningstype:",
            options=list(value_type_mapping.keys())
        )

        # Selectbox for at vælge scenarie
        selected_scenarie = c1.selectbox(
            "Vælg scenarie:",
            options=list(scenarie_mapping.keys()), 
            index=2
        )

        # Selectbox for at vælge periode
        selected_periode = c4.selectbox(
            "Vælg periode:",
            options=list(periode_mapping.keys()), 
            index=3
        )

        # # Selectbox for at vælge percentil
        # selected_percentil = c5.selectbox(
        #     "Vælg percentil:",
        #     options=list(percentil_mapping.keys())
        # )

        # Få de numeriske værdier for hver selectbox
        selected_season_value = season_mapping[selected_season]
        selected_value_type_value = value_type_mapping[selected_value_type]
        selected_scenarie_value = scenarie_mapping[selected_scenarie]
        selected_periode_value = periode_mapping[selected_periode]
        # selected_percentil_value = percentil_mapping[selected_percentil]

        
        # Vis valgte værdier og deres numeriske feltnavne
        # c1.write(f"Du har valgt årstiden: {selected_season} (Feltnavn: {selected_season_value})")
        # c2.write(f"Du har valgt visningstype: {selected_value_type} (Feltnavn: {selected_value_type_value})")
        # c3.write(f"Du har valgt scenarie: {selected_scenarie} (Feltnavn: {selected_scenarie_value})")
        # c4.write(f"Du har valgt periode: {selected_periode} (Feltnavn: {selected_periode_value})")
        # c5.write(f"Du har valgt percentil: {selected_percentil} (Feltnavn: {selected_percentil_value})")

        # Dictionary der mapper tekniske navne til mere letforståelige navne
        klimavariabler = {
            'doegn2aarsh': "2-årshændelse døgnnedbør",
            'doegn5aarsh': "5-årshændelse døgnnedbør",
            'doegn10aarsh': "10-årshændelse døgnnedbør",
            'doegn20aarsh': "20-årshændelse døgnnedbør",
            'doegn50aarsh': "50-årshændelse døgnnedbør",
            'doegn100aarsh': "100-årshændelse døgnnedbør",
            'doegn10mm': "Døgn med over 10 mm nedbør",
            'doegn20mm': "Døgn med over 20 mm nedbør",
            'gennemsnitsnedboer': "Gennemsnitsnedbør",
            'maksimal5doegn': "Maksimal 5-døgnsnedbør",
            'maksimal14doegn': "Maksimal 14-døgnsnedbør",
            'maksimaldoegn': "Maksimal døgnnedbør",
            'skybrud': "Skybrud",
            'time2aarsh': "2-årshændelse timenedbør",
            'time5aarsh': "5-årshændelse timenedbør",
            'time10aarsh': "10-årshændelse timenedbør",
            'time20aarsh': "20-årshændelse timenedbør",
            'time50aarsh': "50-årshændelse timenedbør",
            'time100aarsh': "100-årshændelse timenedbør",
            'toerredage': "Antal tørre dage",
            'toerreperiode': "Længste tørre periode"
        }

        c00, c01 = st.columns([1,4])
        c00.subheader('Klimavariabel:')

        # Opret en selectbox til valg af klimavariabel
        valgt_variabel = c01.selectbox(
            "Vælg en klimavariabel:",
            options=list(klimavariabler.keys()),  # Vis de tekniske navne som options
            format_func=lambda x: klimavariabler[x]  # Viser de letforståelige navne
        )

        with st.spinner('Anvender filtre...'):
            df_gdf = st.session_state['Klimaatlas_gdf']
            filtered_gdf = df_gdf.loc[
                (df_gdf['aarstid'] == selected_season_value) &
                (df_gdf['visningafvaerdier'] == selected_value_type_value) &
                # (st.session_state['Klimaatlas_gdf']['percentil'] == selected_percentil_value) &
                (df_gdf['scenarie'] == selected_scenarie_value) &
                (df_gdf['periode'] == selected_periode_value)
            ]
            gdf = gpd.GeoDataFrame(filtered_gdf, geometry='SHAPE_geometry', crs="EPSG:25832")
            gdf.to_crs(epsg=4326)
        #st.write(gdf.head()) 


        # Opret et nyt folium-kort centreret over Danmark
        m7 = folium.Map(location=[55.6761, 12.5683], zoom_start=10)

        # Tilføj Choropleth lag for at farve kommunerne efter skybrud
        folium.Choropleth(
            geo_data=gdf.to_json(),  # GeoDataFrame konverteret til GeoJSON
            name=valgt_variabel,
            data=gdf,
            columns=["komnavn", valgt_variabel],  # Kolonner for kommune og skybrud
            key_on="feature.properties.komnavn",  # Matcher kommunernes navne i GeoJSON
            fill_color="YlGnBu",  # Farveskala
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=valgt_variabel
        ).add_to(m7)

        # Tilføj kontrol for lag
        folium.LayerControl().add_to(m7)
        
        # Vis kortet i Streamlit og opdater det dynamisk
        st_folium(m7, width=1200, height=700)


