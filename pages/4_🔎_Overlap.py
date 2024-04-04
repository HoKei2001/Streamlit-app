import streamlit as st
import func

st.set_page_config(
    page_title="Overlap",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


def compare2():
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
        video_file = open('video/demonstration.mp4', 'rb')
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


def compare3():
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
        video_file = open('video/demonstration.mp4', 'rb')
        video_bytes = video_file.read()
    else:
        uploaded_file1 = st.sidebar.file_uploader("Upload Paper A (main)", type="pdf")
        uploaded_file2 = st.sidebar.file_uploader("Upload Paper B", type="pdf")
        uploaded_file3 = st.sidebar.file_uploader("Upload Paper C", type="pdf")
        st.sidebar.success("✅ Nougat")
        st.sidebar.success("✅ Openai")
        st.title("Identify Papers Overlapping Contributions 🔎📑")
        st.divider()
        main_body = st.empty()
        with main_body.container():
            c1, c2, c3 = st.columns([1, 1, 1], gap="large")
            c1.success("### A B ")
            c1.success("##### - Comparison")
            c2.info("### Paper A (Main to analysis)")
            c2.info("##### - Aim \n ##### - Method \n ##### - Formulas \n ##### - Conclusion")
            c3.success("### A C")
            c3.success("##### - Comparison ")
            c1.info("### Paper B")
            c1.info("##### - Aim \n ##### - Method \n ##### - Formulas \n ##### - Conclusion")
            c2.warning("### Conclusion")
            c2.warning("##### - Comparison")
            c3.info("### Paper C")
            c3.info("##### - Aim \n ##### - Method \n ##### - Formulas \n ##### - Conclusion")
            tip_space = st.empty()
            tip_space.write("## 👈 Just upload your files and try!")

        if uploaded_file1 is not None:
            with c1:
                st.info(f"{uploaded_file1.name}")
                st.success("✅ Successfully uploaded")
            tip_space.write("## 👈 Continue to upload 3 papers!")
        if uploaded_file2 is not None:
            with c2:
                st.info(f"{uploaded_file2.name}")
                st.success("✅ Successfully uploaded")
            tip_space.write("## 👈 Continue to upload 3 papers!")
        if uploaded_file3 is not None:
            with c3:
                st.info(f"{uploaded_file3.name}")
                st.success("✅ Successfully uploaded")
            tip_space.write("## 👈 Continue to upload 3 papers!")

        # main processing
        if uploaded_file1 is not None and uploaded_file2 is not None and uploaded_file3 is not None:
            tip_space.empty()
            with st.spinner('Wait for processing A...'):
                re1 = func.nougat_api(uploaded_file1, api)
                if re1.status_code == 200:
                    c1.success("✅ File A processing Done")
                else:
                    c1.error("Processing Failed")

            with st.spinner('Wait for processing B...'):
                re2 = func.nougat_api(uploaded_file2, api)
                if re2.status_code == 200:
                    c2.success("✅ File B processing Done")
                else:
                    c2.error("Processing Failed")

            with st.spinner('Wait for processing C...'):
                re3 = func.nougat_api(uploaded_file3, api)
                if re3.status_code == 200:
                    c3.success("✅ File C processing Done")
                else:
                    c3.error("Processing Failed")

            st.markdown("<h1 style='text-align:center'>⏬Slide down⏬</h1>", unsafe_allow_html=True)
            st.divider()
            st.success("### Comparison")
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
                st.info("### Paper C")
                col3_space = st.empty()
                with col3_space.container():
                    with st.spinner('Wait for analysis...'):
                        analysis3 = func.paper_analysis(api_key, re3.json())
                        st.markdown(analysis3)

            with col1:
                st.success("### A B Comparison")
                col11_space = st.empty()
                with col11_space.container():
                    with st.spinner('Wait for comparing...'):
                        compare12 = func.paper_compare(api_key, analysis1, analysis2)
                        st.markdown(compare12)
            with col2:
                st.success("### A C Comparison")
                col22_space = st.empty()
                with col22_space.container():
                    with st.spinner('Wait for comparing...'):
                        compare13 = func.paper_compare(api_key, analysis1, analysis3)
                        st.markdown(compare13)
            with col3:
                st.success("### Conclusion")
                col33_space = st.empty()
                with col33_space.container():
                    with st.spinner('Wait for comparing...'):
                        compare123 = func.paper_compare3(api_key, analysis1, compare12, compare13)
                        st.markdown(compare123)

page_names_to_funcs = {
    "2 Papers": compare2,
    "3 Papers": compare3,
}

demo_name = st.sidebar.selectbox("Choose paper numbers", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
