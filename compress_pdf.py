import io
import tempfile
import shutil
import streamlit as st
import fitz  # pymupdf


def compress_pdf(input_file, output_file, quality=50):
    # 打开现有的PDF文档
    doc = fitz.open(stream=input_file.getvalue(), filetype="pdf")

    # 创建一个新的PDF文档
    new_doc = fitz.open()

    # 遍历所有页面
    for page in doc:
        # 在新文档中创建一个新的空白页面
        temp_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)

        # 复制除了图片以外的内容到临时页面
        temp_page.insert_textbox(temp_page.rect, page.get_text())

        # 遍历所有图像并进行压缩
        for img in page.get_images(full=True):
            try:
                # st.write(img)
                img_data = img[5].get_raw_data("jpeg")
                new_img = fitz.Pixmap(fitz.csRGB, img[0].width, img[0].height, img_data)
                new_img.writeJPG("temp.jpg", quality=quality)
                new_pixmap = fitz.Pixmap("temp.jpg")
                temp_page.insert_image(img[1], pixmap=new_pixmap)
            except:
                # st.write("Error while compressing image.")
                pass
    # 保存压缩后的PDF文档
    new_doc.save(output_file)
    new_doc.close()
    doc.close()

def main():
    st.title("PDF压缩工具")

    # 上传文件
    uploaded_file = st.file_uploader("请选择要压缩的PDF文件", type="pdf")

    if uploaded_file is not None:
        # 显示上传文件信息
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)

        # 压缩质量滑块控件
        quality = st.slider("请选择压缩质量（1-100）", min_value=1, max_value=100, value=50)

        # 压缩PDF文件
        output_file = "compressed.pdf"
        compress_pdf(uploaded_file, output_file, quality=quality)

        # 下载压缩后的PDF文件
        with open(output_file, "rb") as f:
            st.download_button("下载压缩后的PDF文件", f.read(), file_name=output_file)

if __name__ == "__main__":
    main()
