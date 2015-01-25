import unittest as ut
import animetime as at


class AnimeTimeFunctionality(ut.TestCase):

    def setUp(self):
        self.parser = at.create_parser()
        at.start_browser()

    def tearDown(self):
        at.stop_browser()

    def test_command_line_loads_episode(self):
        # User has some free time and decides she wants to watch some anime.
        # Her friends have said good things about Tokyo Ghoul, so she opens her
        # the console and enters the following command:
        #   >> python animetime.py "tokyo ghoul" 1
        # and it loads the first episode of tokyo ghoul in her browser.
        args = self.parser.parse_args(['tokyo ghoul', '1'])
        tokyo_ghoul = at.Anime(args.name)
        tokyo_ghoul.watch(args.episode)

        self.assertNotEqual(at.driver.current_url, 'about:blank',
                            "No URL passed to browser.")

        # how to test if video loaded correctly, esp if page source not available?

        self.fail('What about if not on AnimeShow? What about info/rating?')


if __name__ == '__main__':
    ut.main()
