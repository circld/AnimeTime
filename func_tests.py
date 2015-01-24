import unittest as ut
import argparse as ap
from selenium import webdriver
from animetime import Anime, create_parser


class AnimeTimeFunctionality(ut.TestCase):

    def setUp(self):
        self.parser = create_parser()
        self.anime = None

    def tearDown(self):
        self.anime.driver.quit()

    def test_command_line_loads_episode(self):
        # User has some free time and decides she wants to watch some anime.
        # Her friends have said good things about Tokyo Ghoul, so she opens her
        # the console and enters the following command:
        #   >> python animetime.py "tokyo ghoul" 1
        # and it loads the first episode of tokyo ghoul in her browser.
        args = self.parser.parse_args(['tokyo ghoul', '1'])
        self.anime = Anime(args.name)
        self.anime.watch(args.episode)

        self.assertNotEqual(self.anime.driver.current_url, 'about:blank',
                            "No URL passed to browser.")

        # how to test if video loaded correctly, esp if page source not available?



if __name__ == '__main__':
    ut.main()
