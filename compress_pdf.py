import io
import os
from typing import Tuple

import fitz  # PymuPDF
from PIL import Image
import streamlit as st


def compress_image(image_data: dict) -> Tuple[str, float]:
    """
    压缩单个图像，返回新图片文件名和压缩比例

    Args:
        image_data (dict): 图像数据字典

    Returns:
        Tuple[str, float]: 新图片文件名和压缩比例
    """
    # 获取原始图片大小（字节）
    orig_size = len(image_data["image"])
    # 将字节数据转换为PIL.Image对象
    orig_image = Image.open(io.BytesIO(image_data["image"]))
    # 获取原始图片尺寸（宽度、高度）
    orig_width, orig_height = orig_image.size
    # 定义目标图片尺寸（按比例缩小50%）
    target_width = int(orig_width * 0.5)
    target_height = int(orig_height * 0.5)
    target_size = (target_width, target_height)
    # 创建新图片对象并调整尺寸（保持纵横比）
    new_image = Image.new("RGB", target_size)
    new_image.paste(orig_image.resize(target_size))
    # 生成新图片文件名（在原始文件名后加上"_small"）
    new_filename = image_data["name"].replace(".", "_small.")
    # 保存新图片到本地
    new_image.save(new_filename)
    # 获取新图片大小（字节）
    new_size = os.path.getsize(new_filename)
    # 计算压缩比例（百分比）
    ratio = (orig_size - new_size) / orig_size * 100
    # 打印压缩信息
    print(f"Image {image_data['name']} compressed by {ratio:.2f}%")
    return new_filename, ratio


def compress_pdf(input_file, output_file):
    """
    压缩PDF文件中的所有图片

    Args:
        input_file (str): 输入文件名
        output_file (str): 输出文件名
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
            new_filename, ratio = compress_image(image_data)
            # 定义一个矩形区域，用于插入新图片
            rect = fitz.Rect(*image_info[1:5])
            # 将新图片插入到当前页面，并覆盖原来的图片
            page.insert_image(rect, filename=new_filename)
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

    # 在侧边栏显示上传文件的信息
    st.sidebar.write(f"Input file: {input_name}")
    st.sidebar.write(f"Input size: {input_size} bytes")

    # 在主界面显示上传文件的页面预览（前5页）
    st.header("Input file preview")

    # 使用PymuPDF打开上传文件，并获取页数和页面对象列表
    input_data = io.BytesIO(uploaded_file.read())
    input_doc = fitz.open(stream=input_data, filetype="pdf")
    input_page_count = input_doc.page_count
    st.write(f"page count: {input_page_count}")

    input_pages = input_doc[:min(3, input_page_count)]

    # 压缩PDF文件中的所有图片
    output_file = input_name.replace(".pdf", "_compressed.pdf")
    compress_pdf(uploaded_file, output_file)

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
