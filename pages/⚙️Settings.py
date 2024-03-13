import streamlit as st

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
if "SERPAPI_API_KEY" not in st.session_state:
    st.session_state["SERPAPI_API_KEY"] = ""
if "NOUGAT_API" not in st.session_state:
    st.session_state["NOUGAT_API"] = ""



st.set_page_config(page_title="Setting", layout="wide")

st.title("OpenAI API key Settings")

openai_api_key = st.text_input("OpenAI API Key", value=st.session_state["OPENAI_API_KEY"], max_chars=None, key=None,
                               type='password')

st.title("Serp API key Settings")

serp_api_key = st.text_input("Serp API key", value=st.session_state["SERPAPI_API_KEY"], max_chars=None, key=None,
                             type='password')

st.title("Nougat server API Settings")

nougat_api = st.text_input("Nougat API path", value=st.session_state["NOUGAT_API"], max_chars=None, key=None)


saved = st.button("Save")

if saved:
    st.session_state["OPENAI_API_KEY"] = openai_api_key
    st.session_state["SERPAPI_API_KEY"] = serp_api_key
    st.session_state["NOUGAT_API"] = nougat_api

