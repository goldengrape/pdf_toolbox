import os
import platform
import tempfile
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfkit
import streamlit as st

def fetch_html(url):
    response = requests.get(url)
    return response.text

def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    return links

def crawl_links_recursively(url, depth):
    if depth == 0:
        return {url}
    html = fetch_html(url)
    links = extract_links(html, url)
    child_links = set()
    for link in links:
        child_links |= crawl_links_recursively(link, depth - 1)
    return {url} | child_links

def save_to_pdf(url_list, output_file):
    options = {
        'quiet': '',
        'page-size': 'Letter',
        # 'margin-top': '0.75in',
        # 'margin-right': '0.75in',
        # 'margin-bottom': '0.75in',
        # 'margin-left': '0.75in',
        'encoding': 'utf-8',
        # 'custom-header': [('Accept-Encoding', 'gzip')]
    }

    pdfkit.from_url(url_list, output_file, options=options, configuration=pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path()))

def display_app():
    st.title("网站内容下载器")
    url_input = st.text_input("请输入网站 URL：", "")
    depth_input = st.slider("请选择爬取深度（0 为只下载主页）：", 0, 5, 0)
    download_button = st.button("下载内容")

    return url_input, depth_input, download_button

def get_wkhtmltopdf_path():
    if platform.system() == "Windows":
        return r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    else:
        path = subprocess.run(['which', 'wkhtmltopdf'], stdout=subprocess.PIPE)
        return path.stdout.decode('utf-8').strip()

def main():
    url_input, depth_input, download_button = display_app()

    if download_button:
        file_path, message = process(url_input, depth_input)
        st.write(message)
        if file_path:
            with open(file_path, "rb") as f:
                pdf_data = f.read()
                st.download_button(
                    label="下载 PDF",
                    data=pdf_data,
                    file_name='website_content.pdf',
                    mime='application/pdf',
                )
            os.remove(file_path)

def process(url, depth):
    if not url:
        return None, "请输入一个有效的 URL"

    try:
        links = crawl_links_recursively(url, depth)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            save_to_pdf(list(links), tmp.name)

        return tmp.name, f"下载已准备好！共找到 {len(links)} 个链接"
    except Exception as e:
        return None, f"发生错误，请确保输入的 URL 是有效的。错误信息：{e}"

if __name__ == "__main__":
    main()
