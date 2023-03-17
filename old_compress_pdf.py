import io
import os
import uuid
import tempfile
from typing import Tuple
from PIL import Image
import fitz
import streamlit as st

def compress_image(image_data: dict, quality_threshold: int) -> Tuple[str, float]:
    orig_size = len(image_data["image"])

    if orig_size <= quality_threshold:
        return None, 0

    orig_image = Image.open(io.BytesIO(image_data["image"]))
    grayscale_image = orig_image.convert("L")
    quality = 75
    new_filename = f"{uuid.uuid4()}_small.jpg"
    grayscale_image.save(new_filename, "JPEG", quality=quality)
    new_size = os.path.getsize(new_filename)
    ratio = (orig_size - new_size) / orig_size * 100
    print(f"Image compressed by {ratio:.2f}%")
    return new_filename, ratio

def process_page(page, doc, quality_threshold):
    new_page = fitz.open()
    image_list = page.get_images()
    for image_info in image_list:
        image_data = doc.extract_image(image_info[0])
        new_filename, ratio = compress_image(image_data, quality_threshold)
        if new_filename is None:
            continue
        rect = fitz.Rect(*image_info[1:5])
        if rect.width > 0 and rect.height > 0:
            new_page.insert_image(rect, filename=new_filename)
        else:
            print(f"Invalid or empty rectangle for image: {image_info}")
        os.remove(new_filename)
    return new_page


def compress_pdf(input_file, output_file, quality_threshold=512):
    doc = fitz.open(input_file)
    with fitz.open() as new_doc:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            new_page = process_page(page, doc, quality_threshold)

            # Clone the page content and annots
            new_page.show_pdf_page(new_page.rect, doc, page_num)
            for annot in page.annots():
                new_page.add_annot(annot)

            new_doc.insert_page(-1, new_page)
            new_page.close()
        new_doc.save(output_file)
    doc.close()



def main():
    st.title("PDF Image Compressor")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=False)
    if uploaded_file is not None:
        input_name = uploaded_file.name
        input_size = uploaded_file.size
        st.write(f"Input file: {input_name}")
        st.write(f"Input size: {input_size} bytes")
        input_data = io.BytesIO(uploaded_file.read())
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input_file:
            temp_input_file.write(input_data.getvalue())
            temp_input_file.flush()

        input_doc = fitz.open(temp_input_file.name)
        input_page_count = input_doc.page_count
        st.write(f"page count: {input_page_count}")
        output_file = input_name.replace(".pdf", "_compressed.pdf")
        compress_pdf(temp_input_file.name, output_file)
        input_doc.close()
        os.remove(temp_input_file.name)
        output_size = os.path.getsize(output_file)
        st.write(f"Output file: {output_file}")
        st.write(f"Output size: {output_size} bytes")
        with open(output_file, "rb") as f:
            compressed_pdf = f.read()
        st.download_button(
            label="Download compressed PDF",
            data=compressed_pdf,
            file_name=output_file,
            mime="application/pdf",
        )

if __name__ == "__main__":
    main()

