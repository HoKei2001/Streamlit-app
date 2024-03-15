import streamlit as st
import fitz  # PyMuPDF
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

page_names_to_funcs = {
    "PDF➡️Picture": pdf2img,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
