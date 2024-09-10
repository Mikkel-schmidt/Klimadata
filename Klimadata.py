import streamlit as st

# Tilgå kode gemt i st.secrets
kode = st.secrets["code"]

# Brug koden i din app
st.title('Brug af hemmelig kode i Streamlit')

if kode == "din_hemmelige_kode_her":
    st.write("Koden er korrekt!")
else:
    st.write("Forkert kode!")