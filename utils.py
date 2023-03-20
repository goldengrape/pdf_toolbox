import platform
import subprocess

def get_wkhtmltopdf_path():
    if platform.system() == "Windows":
        path= r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    else:
        path = subprocess.run(['which', 'wkhtmltopdf'], stdout=subprocess.PIPE)
        path= path.stdout.decode('utf-8').strip()
    return path 