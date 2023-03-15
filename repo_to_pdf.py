import os
import tempfile
import shutil
from git import Repo
import pdfkit
import streamlit as st

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
            pdf_options = {
                "quiet": "",
                "enable-local-file-access": None
            }
            
            pdfkit.from_file(file_list, "output.pdf", options=pdf_options)
            st.write("PDF generated successfully.")
            
            with open("output.pdf", "rb") as pdf_file:
                st.download_button("Download PDF", pdf_file.read(), "output.pdf", "application/pdf")
        else:
            st.error("No text or code files found in the repository.")
    
    except Exception as e:
        st.error(f"Error: {e}")
    
    finally:
        shutil.rmtree(temp_dir)
