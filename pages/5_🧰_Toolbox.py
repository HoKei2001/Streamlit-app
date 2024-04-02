import streamlit as st
import fitz  # PyMuPDF
import datetime
import time
import lunardate

st.set_page_config(
    page_title="Toolbox",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="expanded",
)


def pdf2img():
    st.title('Transfer PDF to images (Right click to save the jpg)')
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload PDF file", type=['pdf'])

    if uploaded_file is not None:
        # 读取上传文件的字节流内容
        file_content = uploaded_file.read()

        # 使用 PyMuPDF 将 PDF 转换为图片
        pdf_document = fitz.open(stream=file_content, filetype="pdf")

        # 获取 PDF 文件的总页数
        total_pages = len(pdf_document)

        # 在侧边栏中添加页面范围选择器
        with st.sidebar:
            page_range = st.select_slider("Select pages range", options=list(range(1, total_pages + 1)),
                                          value=(1, total_pages))
            convert_button = st.button("Convert to Images")

        # 当用户点击按钮时，开始转换 PDF 为图片
        if convert_button:
            images = []
            for page_num in range(page_range[0] - 1, page_range[1]):
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # 设置分辨率和缩放比例
                image_bytes = pix.tobytes()
                images.append(image_bytes)
            pdf_document.close()

            # 自动换行显示图片
            cols = st.columns(5)
            rows = len(images) // 5 + (len(images) % 5 > 0)  # 计算需要的行数
            for row_num in range(rows):
                row_images = images[row_num * 5: (row_num + 1) * 5]  # 获取当前行的图片
                for i, (col, image) in enumerate(zip(cols, row_images)):
                    page_num = page_range[0] + row_num * 5 + i  # 计算当前页码
                    col.image(image, caption=f"Page {page_num}", use_column_width=True)


def Xiaoliuren():
    st.title('Chinese magic trick (小六壬)')
    co1, co2 = st.columns([1, 1], gap="large")
    with co1:
        c1, c2 = st.columns([1, 1])
        current_time = datetime.datetime.now()
        d = c1.date_input("Choose the date", current_time.date())
        t = c2.time_input('Choose the time', current_time.time(), step=3600)

        st.sidebar.write(d)
        st.sidebar.write(t)

        lunar_date = lunardate.LunarDate.fromSolarDate(d.year, d.month, d.day)
        st.sidebar.write(lunar_date)

        c21, c22, c23 = st.columns([1, 1, 1], gap="medium")
        liulian = c21.empty()
        liulian.success('### 留连')
        suxi = c22.empty()
        suxi.success('### 速喜')
        chikou = c23.empty()
        chikou.success('### 赤口')

        daan = c21.empty()
        daan.success('### 大安')
        kongwang = c22.empty()
        kongwang.success('### 空亡')
        xiaoji = c23.empty()
        xiaoji.success('### 小吉')

    liuren_dict = {
        0: daan,
        1: liulian,
        2: suxi,
        3: chikou,
        4: xiaoji,
        5: kongwang
    }

    liuren_name_dict = {
        0: '### 大安',
        1: '### 留连',
        2: '### 速喜',
        3: '### 赤口',
        4: '### 小吉',
        5: '### 空亡'
    }
    start = st.sidebar.button("Click Here to start")
    with co2:
        cc1, cc2 = st.columns([1, 2])
    if start:
        i = 0
        while i < lunar_date.month:
            liuren_dict[i % 6].warning(liuren_name_dict[i % 6])
            time.sleep(0.2)
            liuren_dict[i % 6].success(liuren_name_dict[i % 6])
            i = i + 1
        i = i - 1
        cc1.info(f"### 月宫 {lunar_date.month}")
        cc2.info(liuren_name_dict[i % 6])

        time.sleep(0.3)

        while i < lunar_date.month + lunar_date.day:
            liuren_dict[i % 6].warning(liuren_name_dict[i % 6])
            time.sleep(0.2)
            liuren_dict[i % 6].success(liuren_name_dict[i % 6])
            i = i + 1
        i = i - 1
        cc1.info(f"### 日宫 {lunar_date.day}")
        cc2.info(liuren_name_dict[i % 6])

        time.sleep(0.3)

        hour = t.hour
        shichen_dict = {
            0: "子时",
            1: "丑时",
            2: "寅时",
            3: "卯时",
            4: "辰时",
            5: "巳时",
            6: "午时",
            7: "未时",
            8: "申时",
            9: "酉时",
            10: "戌时",
            11: "亥时"
        }
        shichen_index = (hour + 1) // 2 % 12
        shichen = shichen_dict[shichen_index]

        while i < lunar_date.month + lunar_date.day + shichen_index:
            liuren_dict[i % 6].warning(liuren_name_dict[i % 6])
            time.sleep(0.2)
            liuren_dict[i % 6].success(liuren_name_dict[i % 6])
            i = i + 1
        i = i - 1
        cc1.info(f"### 时宫 {shichen_index+1}")
        cc2.info(liuren_name_dict[i % 6])
        st.divider()

page_names_to_funcs = {
    "PDF➡️Picture": pdf2img,
    "Chinese magic trick": Xiaoliuren,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
