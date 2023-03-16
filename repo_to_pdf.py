import os
import tempfile
from git import Repo
import pdfkit
import streamlit as st
import platform
import subprocess
import markdown
from nbconvert import HTMLExporter


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
        html_exporter = HTMLExporter()
        html_exporter.template_name = "lab"
        html_data, _ = html_exporter.from_filename(file_path)
        return html_data
    else:
        return None


def clone_repository(repo_url, temp_dir):
    Repo.clone_from(repo_url, temp_dir)
    st.write("Repository cloned successfully.")


def get_wkhtmltopdf_path():
    if platform.system() == "Windows":
        return r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    else:
        path = subprocess.run(['which', 'wkhtmltopdf'], stdout=subprocess.PIPE)
        return path.stdout.decode('utf-8').strip()


def convert_repo_to_pdf(repo_url):
    temp_dir = tempfile.mkdtemp()
    clone_repository(repo_url, temp_dir)

    st.write("Converting repository content to a single PDF...")

    html_files = [os.path.join(root, file) for root, _, files in os.walk(temp_dir) for file in files if file.endswith((".txt", ".md", ".py", ".html", ".ipynb"))]

    html_contents = [convert_to_html(file_path) for file_path in html_files]

    html_files = [os.path.splitext(file_path)[0] + ".html" for file_path, html_content in zip(html_files, html_contents) if html_content]

    for html_file, html_content in zip(html_files, html_contents):
        if html_content:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

    pdf_options = {
        "quiet": "",
        "enable-local-file-access": None,
        "encoding": "UTF-8",
    }

    pdfkit.from_file(html_files, "output.pdf", options=pdf_options, configuration=pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path()))

    st.write("PDF generated successfully.")
    with open("output.pdf", "rb") as pdf_file:
        st.download_button("Download PDF", pdf_file.read(), "output.pdf", "application/pdf")


st.title("Git Repo to PDF Converter")

repo_url = st.text_input("Enter the Git Repository URL:")
convert_button = st.button("Convert to PDF")

if convert_button and repo_url:
    st.write("Cloning the repository...")
    try:
        convert_repo_to_pdf(repo_url)
    except Exception as e:
        st.error(f"Error: {e}")
