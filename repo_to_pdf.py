import os
import tempfile
import shutil
from git import Repo
import pdfkit
import streamlit as st
import platform 
import errno
import stat
import subprocess



def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        func(path)
    else:
        raise

st.title("Git Repo to PDF Converter")

repo_url = st.text_input("Enter the Git Repository URL:")
convert_button = st.button("Convert to PDF")

if convert_button and repo_url:
    st.write("Cloning the repository...")

    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(repo_url, temp_dir)

        st.write("Repository cloned successfully.")
        st.write("Converting repository content to a single PDF...")

        file_list = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".txt") or file.endswith(".md") or file.endswith(".py") or file.endswith(".html"):
                    file_list.append(file_path)

        if file_list:
            if platform.system() == "Windows":
                wkhtmltopdf_path=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
            else:
                # /usr/bin/wkhtmltopdf
                wkhtmltopdf_path= subprocess.run(['which', 'wkhtmltopdf'], stdout=subprocess.PIPE)
                wkhtmltopdf_path=wkhtmltopdf_path.stdout.decode('utf-8').strip()

            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    
            pdf_options = {
                "quiet": "",
                "enable-local-file-access": None
            }

            st.write(f"Converting the following files: {file_list}")
            pdfkit.from_file(file_list, "output.pdf", options=pdf_options, configuration=config)
            st.write("PDF generated successfully.")

            with open("output.pdf", "rb") as pdf_file:
                st.download_button("Download PDF", pdf_file.read(), "output.pdf", "application/pdf")
        else:
            st.error("No text or code files found in the repository.")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        shutil.rmtree(temp_dir, onerror=handle_remove_readonly)
