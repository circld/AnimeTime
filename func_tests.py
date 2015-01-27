import unittest as ut
import animetime as at


class AnimeTimeFunctionality(ut.TestCase):

    def setUp(self):
        self.parser = at.create_parser()
        at.start_browser()

    def tearDown(self):
        at.stop_browser()

    # TODO: update test so that it actually tests this (program tries kiss first)
    def test_command_line_loads_episode_only_on_animeshow(self):
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

    def test_command_line_loads_episode_only_on_kiss(self):
        # User decides to finish watching the series Eureka Seven,
        # which is not available on all sites. She types:
        #   >> python animetime.py "eureka seven" 40
        args = self.parser.parse_args(['eureka seven', '40'])
        eureka7 = at.Anime(args.name)
        eureka7.watch(args.episode)

        self.assertNotEqual(at.driver.current_url, 'about:blank',
                            "No URL passed to browser.")

    def test_still_to_implement(self):
        self.fail('What about anime movies!? What about info/rating?')


if __name__ == '__main__':
    ut.main()
