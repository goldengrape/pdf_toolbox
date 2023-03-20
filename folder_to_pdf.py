from typing import List
import os
import pdfkit
import fitz
from repo_to_pdf import convert_to_html, remove_unsupported_output
from utils import get_wkhtmltopdf_path

def get_file_paths(folder_path: str) -> List[str]:
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def convert_to_pdf(file_path: str) -> str:
    file_type = os.path.splitext(file_path)[1]
    html=convert_to_html(file_path)
    pdf_path = file_path+".pdf"
    options = {'quiet': '','page-size': 'Letter','encoding': 'utf-8',}
    pdfkit.from_string(html, pdf_path, options=options, configuration=pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path()))
    return pdf_path

def merge_pdfs(pdf_paths: List[str], output_path: str) -> None:
    pdf_document = fitz.open()
    for pdf_path in pdf_paths:
        pdf_document.insert_pdf(fitz.open(pdf_path))
        os.remove(pdf_path)
    pdf_document.save(output_path)
    pdf_document.close()

def main():
    folder_path = input("请输入文件夹路径：")
    file_paths = get_file_paths(folder_path)
    pdf_paths = []
    for file_path in file_paths:
        if os.path.splitext(file_path)[1] in [".ipynb", ".md", ".txt", ".py"]:
            pdf_path = convert_to_pdf(file_path)
            pdf_paths.append(pdf_path)
    merge_pdfs(pdf_paths, os.path.join(folder_path, "output.pdf"))
    print("PDF文件已生成！")
if __name__=="__main__":
    main()
