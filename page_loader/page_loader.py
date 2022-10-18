import requests
from urllib.parse import urlparse
import os.path
import re


def make_filename(url):
    ext = '.html'
    url = url if os.path.splitext(url)[1] != ext else os.path.splitext(url)[0]
    parsed_url = urlparse(url)
    name = '-'.join(
        re.split(r'[^a-zA-Z0-9]', parsed_url.netloc + parsed_url.path))
    return name + '.html'


def download(url, directory):
    resp = requests.get(url)
    file_name = make_filename(url)
    full_file_path = os.path.join(directory, file_name)
    with open(full_file_path, 'w+') as f:
        f.write(resp.text)
    return full_file_path
