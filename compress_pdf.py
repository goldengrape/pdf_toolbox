import streamlit as st
import pikepdf
import zlib
from PIL import Image
import tempfile


def compress_image(image):
    grayscale = image.convert('L').resize((image.width // 10, image.height // 10), Image.ANTIALIAS)
    compressed_data = zlib.compress(grayscale.tobytes())
    return compressed_data

def compress_pdf(file):
    pdf_data = file.getvalue()
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(pdf_data)
        tf.flush()
        with pikepdf.open(tf.name) as pdf:
            for page in pdf.pages:
                for image_name in page.images.keys():
                    try:
                        image = pikepdf.Image(page.images[image_name])
                        rawimage = image.obj
                        pillowimage = image.as_pil_image()
                        compressed_data = compress_image(pillowimage)
                        rawimage.write(compressed_data, filter=pikepdf.Name("/FlateDecode"))
                        rawimage.ColorSpace = pikepdf.Name("/DeviceGray")
                    except:
                        continue
        with open(tf.name, 'rb') as f:
            pdf_bytes = f.read()
    return pdf_bytes

def main():
    st.set_page_config(page_title="PDF压缩工具")
    st.title("PDF压缩工具")
    file = st.file_uploader("请选择要压缩的PDF文件", type="pdf")
    if file is not None:
        compressed_pdf = compress_pdf(file)
        st.download_button(
            label="Download compressed PDF",
            data=compressed_pdf,
            file_name="compressed.pdf",
            mime="application/pdf"
        )
        st.success("PDF压缩完成！")

if __name__ == '__main__':
    main()
