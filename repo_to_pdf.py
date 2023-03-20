import os
import tempfile
from git import Repo
import pdfkit
import streamlit as st
import platform
import subprocess
import markdown
from nbconvert import HTMLExporter
import nbformat
import shutil
import time 
from utils import get_wkhtmltopdf_path

def remove_unsupported_output(notebook):
    """Remove unsupported output types from notebook cells."""
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = [output for output in cell.outputs if not (output.output_type == 'display_data' and "application/vnd.jupyter.widget-state+json" in output.data)]

    return notebook

def convert_to_html(file_path):
    ext = os.path.splitext(file_path)[1]
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if ext in (".md", ".markdown"):
        return markdown.markdown(content)
    elif ext in (".txt", ".py"):
        return f"<pre>{content}</pre>"
    elif ext == ".html":
        return content
    elif ext == ".ipynb":
        notebook = nbformat.reads(content, as_version=4)
        notebook = remove_unsupported_output(notebook)
        
        html_exporter = HTMLExporter()
        html_exporter.template_name = "lab"
        html_data, _ = html_exporter.from_notebook_node(notebook)
        return html_data
    else:
        return None



def clone_repository(repo_url, temp_dir):
    Repo.clone_from(repo_url, temp_dir)
    st.write("Repository cloned successfully.")




def create_html_files(temp_dir, html_files, html_contents):
    for html_file, html_content in zip(html_files, html_contents):
        if html_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)


def generate_pdf_from_html_files(html_files, pdf_file_name):
    pdf_options = {
        "quiet": "",
        "enable-local-file-access": None,
        "encoding": "UTF-8",
    }

    pdfkit.from_file(html_files, pdf_file_name, options=pdf_options, configuration=pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path()))

    st.write("PDF generated successfully.")
    with open(pdf_file_name, "rb") as pdf_file:
        download_button=st.download_button("Download PDF", pdf_file.read(), pdf_file_name, "application/pdf")
        return download_button



def remove_temp_dir(temp_dir):
    """Remove temporary directory and its contents."""
    try:
        shutil.rmtree(temp_dir)
        st.write(f"Temporary directory {temp_dir} removed successfully.")
    except Exception as e:
        st.write(f"Error while removing temporary directory {temp_dir}: {e}")


def convert_repo_to_pdf(repo_url):
    temp_dir = tempfile.mkdtemp()
    clone_repository(repo_url, temp_dir)

    st.write("Converting repository content to a single PDF...")

    html_files = [os.path.join(root, file) for root, _, files in os.walk(temp_dir) for file in files if file.endswith((".txt", ".md", ".py", ".html", ".ipynb"))]

    html_contents = [convert_to_html(file_path) for file_path in html_files]

    html_files = [os.path.splitext(file_path)[0] + ".html" for file_path, html_content in zip(html_files, html_contents) if html_content]

    create_html_files(temp_dir, html_files, html_contents)

    # generate_pdf_from_html_files(html_files)
    repo_name = os.path.basename(repo_url)
    pdf_file_name = repo_name + ".pdf"
    downloaded=generate_pdf_from_html_files(html_files, pdf_file_name)
    if downloaded:
        time.sleep(5)
        remove_temp_dir(temp_dir)


def main():
    st.title("Git Repo to PDF Converter")

    repo_url = st.text_input("Enter the Git Repository URL:")
    convert_button = st.button("Convert to PDF")

    if convert_button and repo_url:
        st.write("Cloning the repository...")
        try:
            convert_repo_to_pdf(repo_url)
        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
