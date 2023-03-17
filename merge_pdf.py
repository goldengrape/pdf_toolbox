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
    st.title("PDF merge")
    st.write("This is a simple web app that can merge multiple PDF files into one PDF file.")

    uploaded_files = st.file_uploader(
        "Please upload the PDF files to be merged (multiple selection allowed)", type="pdf", accept_multiple_files=True
    )

    if len(uploaded_files) >= 2:
        temp_dir = tempfile.mkdtemp()

        save_uploaded_files(uploaded_files, temp_dir)

        merged_file_name, merged_file_content = merge_pdfs(
            temp_dir + "/", temp_dir + "/"
        )

        st.success("Successfully merged the following PDF files:")
        st.write([file.name for file in uploaded_files])
        st.write(f"The merged PDF file name is: {merged_file_name}")
        st.download_button(
            "Click to download the merged PDF file",
            merged_file_content,
            merged_file_name,
            "application/pdf",
        )

    else:
        st.warning("Please upload at least two PDF files.")


if __name__ == "__main__":
    main()
