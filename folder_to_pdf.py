from typing import List
import os
import pdfkit
import fitz
from utils import get_wkhtmltopdf_path

def get_file_paths(folder_path: str) -> List[str]:
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def convert_to_pdf(file_path: str) -> str:
    pdf_path = os.path.splitext(file_path)[0] + ".pdf"

    options = {
        'quiet': '',
        'page-size': 'Letter',
        'encoding': 'utf-8',
    }
    
    pdfkit.from_file(file_path, pdf_path, options=options, configuration=pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path()))
    return pdf_path

def merge_pdfs(pdf_paths: List[str], output_path: str) -> None:
    pdf_writer = fitz.open()
    for pdf_path in pdf_paths:
        pdf_reader = fitz.open(pdf_path)
        for page_number in range(len(pdf_reader)):
            page = pdf_reader.load_page(page_number)
            pdf_writer.insert_pdf(pdf_reader, from_page=page_number, to_page=page_number)
        pdf_reader.close()
    pdf_writer.save(output_path)
    pdf_writer.close()

def main():
    folder_path = input("请输入文件夹路径：")
    file_paths = get_file_paths(folder_path)
    pdf_paths = []
    for file_path in file_paths:
        if os.path.splitext(file_path)[1] in [".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".txt"]:
            pdf_path = convert_to_pdf(file_path)
            pdf_paths.append(pdf_path)
    output_path = os.path.join(folder_path, "output.pdf")
    merge_pdfs(pdf_paths, output_path)
    print("转换完成！")

if __name__ == "__main__":
    main()
