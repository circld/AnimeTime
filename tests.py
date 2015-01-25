import unittest as ut
import animetime as at


class TestArgumentParsing(ut.TestCase):

    def setUp(self):
        self.parser = at.create_parser()

    def test_create_parser_creates_name_and_episode_args(self):
        args = self.parser.parse_args(['some_name', 'some_episode'])

        self.assertIn('name', args)
        self.assertIn('episode', args)

    def test_passing_no_arguments_raises_error(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])


# TODO: once AnimeShow class & test case working, generalize test structure & subclass
class TestAnimeShow(ut.TestCase):

    def setUp(self):
        self.episode = 1
        self.SiteSuccess = at.AnimeShow('shigatsu wa kimi no uso', self.episode)
        self.SiteFail = at.AnimeShow('econometrics 101', self.episode)
        at.start_browser()

    def tearDown(self):
        at.stop_browser()

    def test_AnimeShow_get_anime_url_success(self):
        self.assertEqual(self.SiteSuccess.get_anime(),
                         'http://animeshow.tv/Shigatsu-wa-Kimi-no-Uso/')

    def test_AnimeShow_get_anime_url_fail(self):
        with self.assertRaises(SystemExit):
            self.SiteFail.get_anime()

    def test_AnimeShow_get_episode_url_success(self):
        self.SiteSuccess.urls['anime'] = 'http://animeshow.tv/Shigatsu-wa-Kimi-no-Uso/'
        self.assertEqual(
            self.SiteSuccess.get_episode(),
            'http://animeshow.tv/Shigatsu-wa-Kimi-no-Uso-episode-1/'
        )

    def test_AnimeShow_get_episode_url_fail(self):
        with self.assertRaises(SystemExit):
            self.SiteFail.get_episode()

    def test_AnimeShow_get_video_url_success(self):
        self.SiteSuccess.urls['episode'] = 'http://animeshow.tv/Shigatsu-wa-Kimi-no-Uso-episode-1/'
        self.assertIsNotNone(self.SiteSuccess.get_video())

    def test_AnimeShow_get_video_url_fail(self):
        with self.assertRaises(SystemExit):
            self.SiteFail.get_video()


if __name__ == '__main__':
    ut.main()
