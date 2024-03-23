import streamlit as st
import func

st.set_page_config(
    page_title="Overlap",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Make sure you get the api of nougat server
if "NOUGAT_API" not in st.session_state:
    st.session_state["NOUGAT_API"] = ""
api = st.session_state["NOUGAT_API"]

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
api_key = st.session_state["OPENAI_API_KEY"]

if api == "" or api_key == "":
    st.warning("Please check your api keys in Settings")
    st.sidebar.success("❌ Nougat")
    st.sidebar.success("❌ Openai")
    video_file = open('../video/demonstration.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

else:
    uploaded_file1 = st.sidebar.file_uploader("Upload Paper A", type="pdf")
    uploaded_file2 = st.sidebar.file_uploader("Upload Paper B", type="pdf")
    st.sidebar.success("✅ Nougat")
    st.sidebar.success("✅ Openai")
    st.title("Identify Papers Overlapping Contributions 🔎📑")
    st.divider()
    main_body = st.empty()
    with main_body.container():
        c1, c2, c3 = st.columns([1, 1, 1], gap="large")
        c1.info("### Paper A")
        c1.info("##### - Aim \n ##### - Method \n ##### - Formulas \n ##### - Conclusion")
        with c2:
            st.info("### Paper B")
            st.info("##### - Aim \n ##### - Method \n ##### - Formulas \n ##### - Conclusion")
        with c3:
            st.success("### Comparison")
            st.success("##### - Aim \n ##### - Method \n ##### - Formulas \n ##### - Conclusion")
        tip_space = st.empty()
        tip_space.write("## 👈 Just upload your files and try!")

    if uploaded_file1 is not None:
        with c1:
            st.info(f"{uploaded_file1.name}")
            st.success("✅ Successfully uploaded")
        tip_space.write("## 👈 Continue to upload two papers!")
    if uploaded_file2 is not None:
        with c2:
            st.info(f"{uploaded_file2.name}")
            st.success("✅ Successfully uploaded")
        tip_space.write("## 👈 Continue to upload two papers!")

    # main processing
    if uploaded_file1 is not None and uploaded_file2 is not None:
        tip_space.empty()
        with st.spinner('Wait for processing A...'):
            re1 = func.nougat_api(uploaded_file1, api)
            if re1.status_code == 200:
                c1.success("✅ File A processing Done")
            else:
                c1.error("Processing Failed")

        with st.spinner('Wait for processing B...'):
            re2 = func.nougat_api(uploaded_file2, api)
            if re1.status_code == 200:
                c2.success("✅ File B processing Done")
            else:
                c2.error("Processing Failed")

        st.markdown("<h1 style='text-align:center'>⏬Slide down⏬</h1>", unsafe_allow_html=True)
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.info("### Paper A")
            col1_space = st.empty()
            with col1_space.container():
                with st.spinner('Wait for analysis...'):
                    analysis1 = func.paper_analysis(api_key, re1.json())
                    st.markdown(analysis1)
        with col2:
            st.info("### Paper B")
            col2_space = st.empty()
            with col2_space.container():
                with st.spinner('Wait for analysis...'):
                    analysis2 = func.paper_analysis(api_key, re2.json())
                    st.markdown(analysis2)

        with col3:
            st.success("### Comparison")
            col3_space = st.empty()
            with col3_space.container():
                with st.spinner('Wait for comparing...'):
                    compare = func.paper_compare(api_key, analysis1,analysis2)
                    st.markdown(compare)
            button3 = st.button("💡 Regenerate")
            if button3:
                with col3_space.container():
                    with st.spinner('Wait for comparing...'):
                        compare = func.paper_compare(api_key, analysis1, analysis2)
                        st.markdown(compare)
