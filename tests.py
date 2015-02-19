import unittest as ut
import animetime as at


class TestArgumentParsing(ut.TestCase):

    def setUp(self):
        self.parser = at.create_parser()

    def test_create_parser_creates_name_and_episode_args(self):
        args = self.parser.parse_args(['some_name', '5'])

        self.assertIn('name', args)
        self.assertIn('episode', args)

    def test_passing_no_arguments_raises_error(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])


# Test skeleton for all site-specific classes
class SiteTestBase(object):

    def setUp(self):
        self.episode = None
        self.SiteSuccess = None
        self.SiteFail = None
        self.success_urls = dict()

    def tearDown(self):
        at.stop_browser()

    def test_get_anime_url_success(self):
        self.assertEqual(self.SiteSuccess.get_title(),
                         self.success_urls.get('anime'))

    def test_get_anime_url_fail(self):
        with self.assertRaises(SystemExit):
            self.SiteFail.get_title()

    def test_get_episode_url_success(self):
        self.SiteSuccess.urls['anime'] = self.success_urls.get('anime')
        self.assertEqual(
            self.SiteSuccess.get_episode(),
            self.success_urls.get('episode')
        )

    def test_get_episode_url_fail(self):
        with self.assertRaises(SystemExit):
            self.SiteFail.get_episode()

    def test_get_video_url_success(self):
        self.SiteSuccess.urls['episode'] = self.success_urls.get('episode')
        self.assertIsNotNone(self.SiteSuccess.get_video())

    def test_get_video_url_fail(self):
        with self.assertRaises(SystemExit):
            self.SiteFail.get_video()


class TestAnimeShow(SiteTestBase, ut.TestCase):

    def setUp(self):
        self.episode = 1
        self.SiteSuccess = at.AnimeShow('shigatsu wa kimi no uso', self.episode)
        self.SiteFail = at.AnimeShow('econometrics 101', self.episode)
        self.success_urls = {
            'anime': 'http://animeshow.tv/Shigatsu-wa-Kimi-no-Uso/',
            'episode': 'http://animeshow.tv/Shigatsu-wa-Kimi-no-Uso-episode-1/',
        }
        at.start_browser()


class TestKissAnime(SiteTestBase, ut.TestCase):

    def setUp(self):
        self.episode = 40
        self.SiteSuccess = at.KissAnime('eureka seven', self.episode)
        self.SiteFail = at.KissAnime('econometrics 101', self.episode)
        self.success_urls = {
            'anime': 'http://kissanime.com/Anime/Eureka-Seven',
            'episode': 'http://kissanime.com/Anime/Eureka-Seven/Episode-040?id=5504',
        }
        at.start_browser()


if __name__ == '__main__':
    ut.main()
