import streamlit as st
from repo_to_pdf import main as repo_to_pdf
from merge_pdf import main as merge_pdf
# from compress_pdf import main as compress_pdf

# Create a sidebar with 3 sections: repo_to_pdf, merge_pdf, and compress_pdf
sidebar_selection = st.sidebar.radio("Choose tool", ["Convert Git Repo to PDF", "Merge PDF", "Compress PDF"])

if sidebar_selection == "Convert Git Repo to PDF":
    # Code for repo_to_pdf functionality
    repo_to_pdf()
elif sidebar_selection == "Merge PDF":
    # Code for merge_pdf functionality
    merge_pdf()
elif sidebar_selection == "Compress PDF":
    # Code for compress_pdf functionality
    st.write("to do")