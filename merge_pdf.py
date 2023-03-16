import os
import fitz  # PyMuPDF的别名
import glob
import base64
import streamlit as st
import time
import tempfile  # 添加这一行


def save_uploaded_files(uploaded_files, temp_dir):
    """
    保存上传的PDF文件到临时目录。
    """
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())


def merge_pdfs(pdf_dir, out_dir):
    """
    合并多个pdf文件为一个pdf文件，并返回合并后的文件名和内容。
    """
    doc = fitz.open()

    for file_path in glob.glob(pdf_dir + "*.pdf"):
        doc.insert_pdf(fitz.open(file_path))

    merged_file_name = "merged_" + str(int(time.time())) + ".pdf"
    merged_file_path = os.path.join(out_dir, merged_file_name)
    doc.save(merged_file_path)

    with open(merged_file_path, "rb") as f:
        merged_file_content = f.read()

    return merged_file_name, merged_file_content


def main():
    st.title("PDF合成器")
    st.write("这是一个简单的web app，可以将多个PDF文件合成为一个PDF文件。")

    uploaded_files = st.file_uploader(
        "请上传要合成的PDF文件（可多选）", type="pdf", accept_multiple_files=True
    )

    if len(uploaded_files) >= 2:
        temp_dir = tempfile.mkdtemp()

        save_uploaded_files(uploaded_files, temp_dir)

        merged_file_name, merged_file_content = merge_pdfs(
            temp_dir + "/", temp_dir + "/"
        )

        st.success("成功合成了以下PDF文件：")
        st.write([file.name for file in uploaded_files])
        st.write(f"合成后的PDF文件名为：{merged_file_name}")
        st.download_button(
            "点击下载合成后的PDF文件",
            merged_file_content,
            merged_file_name,
            "application/pdf",
        )

    else:
        st.warning("请至少上传两个PDF文件。")


if __name__ == "__main__":
    main()
