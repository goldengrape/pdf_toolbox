import io
import os
from typing import Tuple

import fitz  # PymuPDF
import streamlit as st
import tempfile
import uuid

from PIL import Image, ImageOps
def compress_image(image_data: dict, quality_threshold: int) -> Tuple[str, float]:
    orig_size = len(image_data["image"])

    if orig_size <= quality_threshold:
        return None, 0

    orig_image = Image.open(io.BytesIO(image_data["image"]))
    # 将原始图像转换为灰度图像
    grayscale_image = orig_image.convert("L")
    quality = 75
    new_filename = f"{uuid.uuid4()}_small.jpg"
    # 保存灰度图像
    grayscale_image.save(new_filename, "JPEG", quality=quality)
    new_size = os.path.getsize(new_filename)
    ratio = (orig_size - new_size) / orig_size * 100
    print(f"Image compressed by {ratio:.2f}%")
    return new_filename, ratio

def compress_pdf(input_file, output_file, quality_threshold=512):
    """
    压缩PDF文件中的所有图片

    Args:
        input_file (str): 输入文件名
        output_file (str): 输出文件名
        quality_threshold (int): 质量阈值，仅对超过该阈值的图像进行压缩
    """
    # 打开输入文件
    doc = fitz.open(input_file)
    # 遍历每一页
    for page in doc:
        # 获取页面上所有图像信息列表
        image_list = page.get_images()
        # 遍历每个图像信息
        for image_info in image_list:
            # 提取图像数据字典
            image_data = doc.extract_image(image_info[0])
            # 压缩图像并获取新图片文件名和压缩比例
            new_filename, ratio = compress_image(image_data, quality_threshold)
            # 如果新文件名为None，则跳过替换过程
            if new_filename is None:
                continue
            # 定义一个矩形区域，用于插入新图片
            rect = fitz.Rect(*image_info[1:5])
            # 检查矩形是否有效
            if rect.width > 0 and rect.height > 0:
            # 将新图片插入到当前页面，并覆盖原来的图片
                page.insert_image(rect, filename=new_filename)
            else:
                print(f"Invalid or empty rectangle for image: {image_info}")
            # 删除新图片文件
            os.remove(new_filename)
    # 保存修改后的PDF文件
    doc.save(output_file)
    # 关闭doc对象
    doc.close()



# 创建一个streamlit web app
st.title("PDF Image Compressor")
# 创建一个文件上传器，接受PDF类型的文件，不允许多个文件同时上传
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=False)




# 如果有文件被上传，执行以下操作
if uploaded_file is not None:
    # 获取上传文件的名称和大小（字节）
    input_name = uploaded_file.name
    input_size = uploaded_file.size

    st.write(f"Input file: {input_name}")
    st.write(f"Input size: {input_size} bytes")

    # 使用PymuPDF打开上传文件，并获取页数和页面对象列表
    input_data = io.BytesIO(uploaded_file.read())

    # 将上传的文件内容保存到一个临时文件中
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input_file:
        temp_input_file.write(input_data.getvalue())
        temp_input_file.flush()

    input_doc = fitz.open(temp_input_file.name)
    input_page_count = input_doc.page_count
    st.write(f"page count: {input_page_count}")

    # 压缩PDF文件中的所有图片
    output_file = input_name.replace(".pdf", "_compressed.pdf")
    compress_pdf(temp_input_file.name, output_file)

    # 关闭输入文件
    input_doc.close()

    # 删除临时输入文件
    os.remove(temp_input_file.name)
    # 获取压缩后的文件大小（字节）
    output_size = os.path.getsize(output_file)

    # 在侧边栏显示压缩后的文件信息
    st.sidebar.write(f"Output file: {output_file}")
    st.sidebar.write(f"Output size: {output_size} bytes")

    # 显示压缩后的文件下载链接
    with open(output_file, "rb") as f:
        compressed_pdf = f.read()
    st.download_button(
        label="Download compressed PDF",
        data=compressed_pdf,
        file_name=output_file,
        mime="application/pdf",
    )
