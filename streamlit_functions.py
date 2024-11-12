import streamlit as st
import requests
import xml.etree.ElementTree as ET
import math

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

@st.cache_data
def find_laveste_punkt(latitude, longitude):
    # Konvertering fra meter til grader
    lat_offset = 20 / 111320  # Omtrentlig konvertering for breddegrad
    lon_offset = 20 / (111320 * abs(math.cos(math.radians(latitude))))  # Konvertering for længdegrad afhængigt af breddegrad

    # Grid størrelse i grader (4x4 grid for at dække 20x20 meter)
    step_lat = lat_offset / 4
    step_lon = lon_offset / 4

    wms_url = 'https://api.dataforsyningen.dk/dhm?service=WMS&request=GetCapabilities&token=30494b8c7d48e71467a3bca51afaf457'

    laveste_vaerdi = None

    # Iterer gennem grid-punkterne
    for i in range(-2, 3):  # Fra -2 til 2 (5 punkter i alt)
        for j in range(-2, 3):  # Fra -2 til 2 (5 punkter i alt)
            lat = latitude + (i * step_lat)
            lon = longitude + (j * step_lon)

            # Udfør GetFeatureInfo-forespørgsel
            bbox = f"{lon - lon_offset},{lat - lat_offset},{lon + lon_offset},{lat + lat_offset}"
            params = {
                'service': 'WMS',
                'request': 'GetFeatureInfo',
                'version': '1.1.1',
                'layers': 'dhm_havvandpaaland',
                'query_layers': 'dhm_havvandpaaland',
                'styles': 'havvandpaaland_6',
                'bbox': bbox,
                'width': '256',
                'height': '256',
                'x': '128',
                'y': '128',
                'srs': 'EPSG:4326',
                'format': 'image/png',
                'info_format': 'application/vnd.ogc.gml',
                'i': '50',
                'j': '50'
            }

            # Send forespørgslen til WMS-serveren
            response = requests.get(wms_url, params=params)
            if response.status_code != 200:
                continue

            try:
                root = ET.fromstring(response.text)
                value_0_element = root.find('.//value_0')

                if value_0_element is not None and value_0_element.text is not None:
                    value_0 = float(value_0_element.text)
                    # Kontroller om value_0 er en gyldig værdi
                    if value_0 > -1e10 and value_0 < 1e10:  # Filtrer ekstreme værdier fra
                        if laveste_vaerdi is None or value_0 < laveste_vaerdi:
                            laveste_vaerdi = value_0
            except ET.ParseError:
                continue

    if laveste_vaerdi is None:
        raise ValueError("Ingen gyldig værdi fundet inden for 20 meter")

    return laveste_vaerdi

def beregn_vanddybde(value_0, vandstigning):
    if vandstigning < value_0:
        return 0  # Ingen oversvømmelse, vanddybden er 0
    else:
        return vandstigning - value_0