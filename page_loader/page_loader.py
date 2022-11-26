import requests
from urllib.parse import urlparse
import os.path
import re


def covert_url_to_name(url):
    # url = url if os.path.splitext(url)[1] != '.html' \
    #     else os.path.splitext(url)[0]
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    path = os.path.splitext(parsed_url.path)[0]
    name = re.sub(r'\W', '-', netloc + path)
    return name


def make_filename(url, ext='html'):
    name = covert_url_to_name(url)
    return name + '.' + ext


def download(url, directory):
    resp = requests.get(url)
    file_name = make_filename(url)
    full_file_path = os.path.join(directory, file_name)

    if not os.path.exists(directory):
        os.mkdir(directory)

    with open(full_file_path, 'w+') as f:
        f.write(resp.text)
    return full_file_path
