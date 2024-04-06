import streamlit as st

st.set_page_config(
    page_title="Toolbox",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="expanded",
)

def cpp1():
    col1,col2=st.columns([3,1])
    with col1:
        with open("blogpages/cpp1.md", "r", encoding="utf-8") as file:
            markdown_text = file.read()
        st.markdown(markdown_text)
    with col2:
        st.page_link("https://www.bilibili.com/video/BV1iQ4y1s7Qj/?share_source=copy_web&vd_source=cda810cbb5e85ca277470d72cd78e5c0", label="Click to Reference video", icon="📺")
        video_file = open('video/streamlit-streamlit_app-2024-04-04-19-04-99.webm', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

def SVM():
    with open("blogpages/SVM/SVM.md", "r", encoding="utf-8") as file:
        markdown_text = file.read()
    st.markdown(markdown_text)



page_names_to_funcs = {
    "01 First try with cpp": cpp1,
    "02 SVM notes":  SVM,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
