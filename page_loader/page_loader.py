import requests
from urllib.parse import urlparse, urljoin
import os.path
import re
from bs4 import BeautifulSoup


def covert_url_to_name(url):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    path = os.path.splitext(parsed_url.path)[0]
    name = re.sub(r'\W', '-', netloc + path)
    return name


def make_name(url, ext):
    name = covert_url_to_name(url)
    return name + ext


def download_bin_files(data, path_, dir_, url, tag, attr):
    # tag_list = data.find_all(tag)
    netloc = urlparse(url).netloc
    for tag in data.find_all(tag):
        link = tag[attr]
        link_netloc = urlparse(link).netloc
        if not link_netloc or netloc == link_netloc:
            if not link_netloc:
                link = urljoin(url, link)
            converted_link = make_name(covert_url_to_name(link),
                                       os.path.splitext(link)[1])
            local_path = os.path.join(path_, converted_link)
            tag[attr] = os.path.join(dir_, converted_link)
            resp = requests.get(link).content
            with open(local_path, 'wb+') as f:
                f.write(resp)


def download(url, directory=os.getcwd()):
    resp = requests.get(url).text
    dir_name = make_name(url, '_files')
    dir_path = os.path.join(directory, dir_name)
    html_file_name = make_name(url, '.html')
    html_file_path = os.path.join(directory, html_file_name)

    # if not os.path.exists(dir_path):
    os.makedirs(dir_path, exist_ok=True)

    soup = BeautifulSoup(resp, 'html.parser')
    download_bin_files(soup, dir_path, dir_name, url, 'img', 'src')

    with open(html_file_path, 'w+') as f:
        f.write(soup.prettify())

    return html_file_path
