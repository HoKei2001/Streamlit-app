import streamlit as st
import func

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Make sure you get the api of nougat server
if "NOUGAT_API" not in st.session_state:
    st.session_state["NOUGAT_API"] = ""
api = st.session_state["NOUGAT_API"]

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
api_key = st.session_state["OPENAI_API_KEY"]

col1, col2 = st.columns([1, 2])
with col1:
    st.title("PDF ➡️ Markdown")
    st.caption("Your nougat server")
    if api == "" or api_key == "":
        st.warning("Please set your api keys in setting pages!")
    else:
        st.code(api)

uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

with col2:
    tab1, tab2 = st.tabs(["Markdown", "Code"])
    with tab1:
        with st.container(height=650):
            show_space = st.empty()
            with show_space.container():
                st.markdown("""
                    <style>
                    .vertical-center {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 500px;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.markdown(
                    '<div class="vertical-center"><h1><i>Upload your <font color="blue">PDF</font> file </i>😎</h1>'
                    '<h1><i>Get the <font color="green">Markdown</font> here !</i></h1></div>', unsafe_allow_html=True)
    with tab2:
        with st.container(height=650):
            code_space = st.empty()
            with code_space.container():
                st.markdown("""
                    <style>
                    .vertical-center {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 500px;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.markdown(
                    '<div class="vertical-center"><h1><i>Upload your <font color="blue">PDF</font> file </i>😎</h1>'
                    '<h1><i>Get the <font color="green">Markdown Code</font> here !</i></h1></div>', unsafe_allow_html=True)

if uploaded_file is not None:
    if api != "":
        with show_space.container():
            st.markdown("""
                <style>
                .vertical-center {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 500px;
                }
                </style>
            """, unsafe_allow_html=True)
            with st.spinner(" "):
                st.markdown(
                    '<div class="vertical-center"><h1><i>Processing <font color="blue">on</font> </i></h1>'
                    '<h1>Please wait a minute!</h1></div>', unsafe_allow_html=True)
                try:
                    markdown = func.nougat_api(uploaded_file, api).json()
                    with col1:
                        with st.container(height=452):
                            if api_key == "":
                                st.write(
                                    "You need to fill the OPENAI API KEY to get a table of content! Please complete it in "
                                    "Settings pages.")
                            else:
                                with st.spinner("LOADING TABLE OF CONTENT"):
                                    st.write(func.get_list(markdown, api_key))
                except Exception as e:
                    markdown = f"Server Denied: {e}"
                    st.warning(markdown)
        show_space.markdown(markdown)
        code_space.code(markdown)

    else:
        st.toast("Please set your api keys in setting pages!")
