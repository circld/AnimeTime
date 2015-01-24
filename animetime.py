import argparse as ap
from selenium import webdriver


class Anime(object):

    def __init__(self, name):
        self.name = name
        self.driver = None

    def watch(self, episode):
        self.driver = webdriver.Firefox()


def create_parser():
    parser = ap.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('episode')
    return parser
