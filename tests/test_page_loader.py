import pytest
from page_loader.page_loader import make_filename
from page_loader import download
import requests_mock
import tempfile
import os


TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ' \
       'eiusmod tempor incididunt ut labore et dolore magna aliqua. Urna nec ' \
       'tincidunt praesent semper feugiat. Lorem ipsum dolor sit amet. ' \
       'Pellentesque habitant morbi tristique senectus et netus. Est ' \
       'pellentesque elit ullamcorper dignissim cras tincidunt. Massa eget ' \
       'egestas purus viverra accumsan in nisl nisi scelerisque. Amet ' \
       'consectetur adipiscing elit ut aliquam purus sit amet. Dui nunc ' \
       'mattis enim ut tellus elementum sagittis vitae. In fermentum posuere ' \
       'urna nec tincidunt praesent. A condimentum vitae sapien pellentesque ' \
       'habitant morbi. In fermentum posuere urna nec tincidunt praesent ' \
       'semper. Nulla malesuada pellentesque elit eget gravida. In arcu ' \
       'cursus euismod quis viverra nibh. '


cases = [
    ('https://test.site.com/testpage', 'test-site-com-testpage.html'),
    ('https://test.site.com/testpage.html', 'test-site-com-testpage.html'),
    ('https://test.site.com/testpage.test', 'test-site-com-testpage-test.html')
]

def read_file(file):
    with open(file) as f:
        return f.read()


def test_download():
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as m:
            url = cases[0][0]
            filename = cases[0][1]
            m.get(url, text=TEXT)
            download(url, tmp)
            result = read_file(os.path.join(tmp, filename))
            assert result == TEXT


@pytest.mark.parametrize('url,filename', cases)
def test_make_filename(url, filename):
    assert make_filename(url) == filename
