#!/usr/bin/env python
from page_loader import download
from page_loader.cli import parse_args


def main():
    url, directory = parse_args().url, parse_args().output
    print(download(url, directory))


if __name__ == '__main__':
    main()
