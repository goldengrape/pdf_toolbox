# 导入所需的库
import os
import fitz # PyMuPDF的别名
import glob
import base64
import streamlit as st
import time 
import tempfile  # 添加这一行


# 定义一个函数，用于合并多个pdf文件为一个pdf文件，并返回合并后的文件名和内容
def merge_pdfs(pdf_dir, out_dir):
    # 创建一个空的文档对象，用于合并pdf文件
    doc = fitz.open()
    # 遍历指定目录下的所有pdf文件，并将它们添加到文档对象中
    for file_path in glob.glob(pdf_dir + "*.pdf"):
        doc.insert_pdf(fitz.open(file_path))
    # 生成合并后的文件名，使用当前时间戳作为唯一标识符
    merged_file_name = "merged_" + str(int(time.time())) + ".pdf"
    # 将合并后的文件保存到指定目录下，并返回文件名和内容
    merged_file_path = os.path.join(out_dir, merged_file_name)
    doc.save(merged_file_path)
    with open(merged_file_path, "rb") as f:
        merged_file_content = f.read()
    return merged_file_name, merged_file_content

# 定义一个函数，用于将pdf文件内容转换为base64编码，并嵌入到html中显示在web app上
def display_pdf(file_name, file_content):
    # 将pdf文件内容转换为base64编码，并拼接成html格式的字符串
    encoded_pdf = base64.b64encode(file_content).decode()
    pdf_display = f'<embed src="data:application/pdf;base64,{encoded_pdf}" width="700" height="1000" type="application/pdf">'
    # 使用streamlit的markdown组件显示html字符串，并设置unsafe_allow_html参数为True，允许渲染html标签
    st.markdown(pdf_display, unsafe_allow_html=True)

# 设置web app的标题和说明文字
st.title("PDF合成器")
st.write("这是一个简单的web app，可以将多个PDF文件合成为一个PDF文件。")

# 使用streamlit的file_uploader组件创建一个上传框，允许用户上传多个PDF文件，并设置accept_multiple_files参数为True，表示接受多个文件上传。
uploaded_files = st.file_uploader("请上传要合成的PDF文件（可多选）", type="pdf", accept_multiple_files=True)

# 如果用户已经上传了至少两个PDF文件，则执行以下操作：
if len(uploaded_files) >= 2:
    # 创建一个临时目录，用于存放上传的PDF文    # 件和合成后的PDF文件。
    temp_dir = tempfile.mkdtemp()
    
    # 遍历上传的PDF文件列表，并将每个PDF文件保存到临时目录下。
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
    
    # 调用merge_pdfs函数，传入临时目录作为参数，得到合成后的PDF文件名和内容。
    merged_file_name, merged_file_content = merge_pdfs(temp_dir + "/", temp_dir + "/")
    
     # 使用streamlit的success组件显示成功信息，并显示合成后的PDF文件名。
    st.success("成功合成了以下PDF文件：")
    st.write([file.name for file in uploaded_files])
    st.write(f"合成后的PDF文件名为：{merged_file_name}")
     
    # 调用display_pdf函数，传入合成后的PDF文件名和内容，将其显示在web app上。
    display_pdf(merged_file_name, merged_file_content)
     
# 如果用户没有上传至少两个PDF文件，则显示提示信息。
else:
    st.warning("请至少上传两个PDF文件。")