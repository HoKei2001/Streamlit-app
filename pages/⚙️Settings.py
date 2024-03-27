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
with st.expander("See how to get OpenAI API key"):
    st.write("1. Go to https://platform.openai.com/account/api-keys.")
    st.write("2. Click on the '+ Create new secret key' button.")
    st.write("3. Enter an identifier name (optional) and click on the 'Create secret key' button.")
    st.write("4. Copy the API key to be used in this tutorial (the key shown below was already revoked):")
    st.image('img/openai.png')
st.title("Serp API key Settings")

serp_api_key = st.text_input("Serp API key", value=st.session_state["SERPAPI_API_KEY"], max_chars=None, key=None,
                             type='password')

st.title("Nougat server API Settings")

nougat_api = st.text_input("Nougat API path", value=st.session_state["NOUGAT_API"], max_chars=None, key=None)
with st.expander("See how to get Nougat API path"):
    st.write("### Way 1: \n Directly use this server we provide (our server may not run 7*24)")
    st.code("https://mature-garfish-emerging.ngrok-free.app")
    st.write("Note that if this server does not work do try other ways")
    st.write("### Way 2: \n Run your own server on local GPU")
    st.write("Follow https://github.com/facebookresearch/nougat")
    st.write("Note, on Windows: If you want to utilize a GPU, make sure you first install the correct PyTorch version. Follow instructions hereNOTE to use https://pytorch.org/get-started/locally/")
    st.write("### Way 3: \n Use Huggingface endpoint of Nougat-base")
    st.write("Visit https://huggingface.co/facebook/nougat-base")

saved = st.button("Save")

if saved:
    st.session_state["OPENAI_API_KEY"] = openai_api_key
    st.session_state["SERPAPI_API_KEY"] = serp_api_key
    st.session_state["NOUGAT_API"] = nougat_api

