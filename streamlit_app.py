import streamlit as st
from repo_to_pdf import main as repo_to_pdf
from merge_pdf import main as merge_pdf
from webscraper_to_pdf import main as webscraper_to_pdf
# from compress_pdf import main as compress_pdf

choice={
    "Convert Git Repo to PDF": repo_to_pdf,
    "Convert WebSite to PDF": webscraper_to_pdf,
    "Merge PDF": merge_pdf,
    # "Compress PDF": None,
}

sidebar_selection = st.sidebar.radio("Choose tool", 
    list(choice.keys()))

choice[sidebar_selection]()