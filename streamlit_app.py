import streamlit as st

st.set_page_config(
    page_title="HoKei's page",
    page_icon="🐸",
    layout="wide",
    initial_sidebar_state="expanded",
)

col1, gap, col2 = st.columns([5, 0.2, 3],gap="large")
with col1:
    st.title("👋 Welcome to my page !")
    st.divider()
    st.subheader(" -🍬 About Nougat")
    st.write("Nougat is a tool which can transfer your PDF paper/article into markdown form. It can works well with "
             "latex formulas")
    st.subheader(" -🤖 About Chatbot")
    st.write("Chatbot can chat with models")
    st.subheader(" -🔎 About Overlap")
    st.write("Overlap Nougat is a tool can compare two articles with their topics, aims, methods and also formulas. "
             "It can works really well to identify overlapping contributions between different papers")
with col2:
    st.image('bgpic.png')
    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<h5 style='text-align: center;'>😺HoKei</h1>", unsafe_allow_html=True)
    c2.markdown("<h5 style='text-align: center;'>👨‍🎓Student</h1>", unsafe_allow_html=True)
    c3.markdown("<h5 style='text-align: center;'>📐EE</h1>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<h6 style='text-align: center;'>@e1143543@u.nus.edu</h6>", unsafe_allow_html=True)
    st.info("")

