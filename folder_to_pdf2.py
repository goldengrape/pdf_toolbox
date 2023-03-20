import os
import tempfile
import pdfkit
import shutil
import time 
from repo_to_pdf import clone_repository, convert_to_html, create_html_files, generate_pdf_from_html_files, remove_temp_dir
from utils import get_wkhtmltopdf_path


def generate_pdf_from_html_files(html_files, pdf_file_name):
    pdf_options = {
        "quiet": "",
        "enable-local-file-access": None,
        "encoding": "UTF-8",
    }

    pdfkit.from_file(html_files, pdf_file_name, options=pdf_options, configuration=pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path()))

    # st.write("PDF generated successfully.")
    # with open(pdf_file_name, "rb") as pdf_file:
    #     download_button=st.download_button("Download PDF", pdf_file.read(), pdf_file_name, "application/pdf")
    #     return download_button
    return pdf_file_name
        
def convert_folder_to_pdf(folder_path):
    # st.write("Converting folder content to a single PDF...")
    html_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith((".txt", ".md", ".py", ".html", ".ipynb"))]
    html_contents = [convert_to_html(file_path) for file_path in html_files]
    html_files = [os.path.splitext(file_path)[0] + ".html" for file_path, html_content in zip(html_files, html_contents) if html_content]
    create_html_files(folder_path, html_files, html_contents)
    pdf_file_name = os.path.basename(folder_path) + ".pdf"
    downloaded=generate_pdf_from_html_files(html_files, pdf_file_name)
    if downloaded:
        time.sleep(5)
        # remove_temp_dir(folder_path)
        print(downloaded)

# Continue the main execution of the script
if __name__ == "__main__":
    folder_path='C:\\Users\\goldengrape\\Documents\\Code\\Optometric_Design_pdf'
    convert_folder_to_pdf(folder_path)