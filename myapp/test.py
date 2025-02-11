import os
import requests
from zipfile import ZipFile
 
def download_and_read_files(url):
    # Get the temporary directory from the environment variable
    temp_dir = os.getenv('TEMP_FOLDER')
    if not temp_dir:
        raise EnvironmentError("TEMP_FOLDER environment variable is not set")
 
    # Download the file
    response = requests.get(url)
    zip_path = os.path.join(temp_dir, 'files.zip')
 
    with open(zip_path, 'wb') as file:
        file.write(response.content)
 
    # Extract the zip file
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
 
    # Read the text of all files
    text_content = ""
    for root, dirs, files in os.walk(temp_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content += f"--- {file_path} ---\n"
                    text_content += file.read() + "\n"
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text_content += f"--- {file_path} ---\n"
                    text_content += file.read() + "\n"
 
    return text_content
 
def read_single_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()
 
#header
header = "As a senior programmer, given a project in [PROGRAMMING LANGUAGE] with [VERSION OF LIBRARIES]. How could resolve the next error [ERROR_COMPILE] to generete a success compile?\n\n"
 
# Example log
single_file_path = "C:/Users/beltrac1/Downloads/msbuild (3) 1.log"
single_file_content = read_single_file(single_file_path)
 
# Example git
url = 'https://github.com/cristobal987/gpu-prices-api-mex/archive/refs/heads/main.zip'
text = download_and_read_files(url)
 
print(text + single_file_content)
 