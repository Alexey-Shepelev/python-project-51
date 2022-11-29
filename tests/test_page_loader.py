import pytest
from page_loader.page_loader import make_name
from page_loader import download
import requests_mock
import tempfile
import os


# TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ' \
#        'eiusmod tempor incididunt ut labore et dolore magna aliqua. Urna nec ' \
#        'tincidunt praesent semper feugiat. Lorem ipsum dolor sit amet. ' \
#        'Pellentesque habitant morbi tristique senectus et netus. Est ' \
#        'pellentesque elit ullamcorper dignissim cras tincidunt. Massa eget ' \
#        'egestas purus viverra accumsan in nisl nisi scelerisque. Amet ' \
#        'consectetur adipiscing elit ut aliquam purus sit amet. Dui nunc ' \
#        'mattis enim ut tellus elementum sagittis vitae. In fermentum posuere ' \
#        'urna nec tincidunt praesent. A condimentum vitae sapien pellentesque ' \
#        'habitant morbi. In fermentum posuere urna nec tincidunt praesent ' \
#        'semper. Nulla malesuada pellentesque elit eget gravida. In arcu ' \
#        'cursus euismod quis viverra nibh. '


cases = [
    ('https://page-loader.hexlet.repl.co', 'page-loader-hexlet-repl-co.html', '.html'),
    ('https://test.site.com/test.html', 'test-site-com-test.html', '.html'),
    ('https://test.site.com/testpage', 'test-site-com-testpage_files', '_files')
]


@pytest.mark.parametrize('url,name,ext', cases)
def test_make_name(url, name, ext):
    assert make_name(url, ext) == name


def read(file):
    with open(file) as f:
        return f.read()


def read_bin(file):
    with open(file, 'rb') as f:
        return f.read()


def test_download():
    html_initial = read('tests/fixtures/initial.html')
    html_expected = read('tests/fixtures/expected.html')
    img_initial = read_bin('tests/fixtures/nodejs.png')
    script_initial = read_bin('tests/fixtures/script.js')
    css_initial = read_bin('tests/fixtures/application.css')

    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as m:
            url = cases[0][0]
            filename = cases[0][1]

            img_url = url + '/assets/professions/nodejs.png'
            script_url = url + '/script.js'
            css_url = url + '/assets/application.css'
            link_url = url + '/courses'

            m.get(url, text=html_initial)
            m.get(img_url, content=img_initial)
            m.get(script_url, content=script_initial)
            m.get(css_url, content=css_initial)
            m.get(link_url, text=html_initial)
            download(url, tmp)

            html = read(os.path.join(tmp, filename))
            assert html == html_expected

            img = read_bin(os.path.join(
                tmp,
                'page-loader-hexlet-repl-co_files'
                '/page-loader-hexlet-repl-co-assets-professions-nodejs.png'))
            assert img == img_initial

            script = read_bin(os.path.join(
                tmp,
                'page-loader-hexlet-repl-co_files'
                '/page-loader-hexlet-repl-co-script.js'))
            assert script == script_initial

            css = read_bin(os.path.join(
                tmp,
                'page-loader-hexlet-repl-co_files'
                '/page-loader-hexlet-repl-co-assets-application.css'))
            assert css == css_initial
