import streamlit as st
from streamlit_extras.row import row
st.set_page_config(
    page_title="HoKei's page",
    page_icon="🐸",
    layout="wide",
    initial_sidebar_state="expanded",
)

col1, col2 = st.columns([2, 1],gap="large")
with col1:
    st.title("👋 Welcome to HoKei's page !")
    st.info(" ")

with col2:
    st.image('bgpic.png')
    c1, c2, c3 = st.columns(3)
    c1.metric("Temperature", "70 °F", "1.2 °F")
    c2.metric("Wind", "9 mph", "-8%")
    c3.metric("Humidity", "86%", "4%")

    st.write(": HoKei")
    st.write("Student")
    st.info("")
