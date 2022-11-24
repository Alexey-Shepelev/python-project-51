import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='Downloading the page from internet and place it into the\
        specified directory (into working directory by default)'
    )
    parser.add_argument('-o', '--output',
                        default=os.getcwd(),
                        help='Directory name')
    parser.add_argument('url',
                        type=str,
                        help='URL address')
    return parser.parse_args()
