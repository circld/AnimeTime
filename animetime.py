# TODO: minimize FF windows (if sticking with selenium)
# http://stackoverflow.com/questions/2791489/how-do-i-take-out-the-focus-or-minimize-a-window-with-python

from sys import argv
from os.path import dirname, join
import argparse as ap
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from re import search, sub
from urllib2 import unquote
from inspect import isclass


driver = None
profile_path = None
script_location = dirname(argv[0])

# load Firefox default profile into memory
with open(join(script_location, 'profile_path.txt'), 'r') as pp:
    profile_path = pp.readlines()[0].strip()
    pp.close()


def start_browser():
    global driver
    profile = webdriver.FirefoxProfile(profile_path)
    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(5)
    return driver


def stop_browser():
    global driver
    driver.quit()


def create_parser():
    parser = ap.ArgumentParser(
        description=
        """
        Watch anime from the command line.\n\n
        Example usage:\n
        >>> python animetime.py 'juuni kokuki' 2
        """
    )
    parser.add_argument(
        'name', type=str,
        help='Name of anime (enclose multiple words with quotes)'
    )
    parser.add_argument(
        'episode', type=int,
        help='Episode number to watch'
    )
    return parser


class Site(object):
    """
    general class specific website classes will subclass
    """

    def __init__(self, anime, episode):
        self.anime = anime.title()
        self.episode = int(episode)
        self.urls = {'anime': None, 'episode': None, 'video': None}


    def get_anime(self):
        pass

    def get_episode(self):
        pass

    def get_video(self):
        pass


class AnimeShow(Site):

    def get_anime(self):
        driver.get('http://www.animeshow.tv')
        search_box = driver.find_element_by_class_name('search')
        search_box.send_keys(self.anime)
        sleep(1)
        try:
            results = driver.find_element_by_css_selector(
                "div[class='menu-search-result'] > ol > li > a"
            )
            results.click()
            self.urls['anime'] = driver.current_url
            return self.urls['anime']
        except NoSuchElementException:
            raise SystemExit(
                '{0}: Could not find {1} URL.'.format(self.__class__,
                                                      self.anime)
            )

    def get_episode(self):
        if self.urls['anime'] is None:
            self.get_anime()
        if driver.current_url != self.urls['anime']:
            driver.get(self.urls['anime'])

        loc_id = 'episode-list-entry'
        episodes = driver.find_elements_by_css_selector(
            "table[id='{0}-tbl'] a".format(loc_id)
        )
        links = [
            (a.get_attribute('title'), a.get_attribute('href'))
            for a in episodes
            if search('Episode %d$' % self.episode, a.get_attribute('title'))
        ]
        try:
            self.urls['episode'] = links[0][1]
            return self.urls['episode']
        except (IndexError, TypeError):
            raise SystemExit(
                '{0}: Could not find {1} episode {2} URL.'.format(
                    self.__class__, self.anime, self.episode
                )
            )

    def get_video(self, direct_link=None):
        if not direct_link:
            if self.urls['episode'] is None:
                self.get_episode()
            if driver.current_url != self.urls['episode']:
                driver.get(self.urls['episode'])

        mirrors = driver.find_elements_by_css_selector(
            "div[id='episode-mirrors'] > ul a"
        )
        hd_url = None

        try:
            hd_url = [a.get_attribute('href')
                            for a in mirrors
                            if search(' HD$', a.text)][0]
        except (IndexError, TypeError, NameError):
            pass

        # recursive get_video call to grab HD vid link
        if direct_link is None and hd_url is not None:
            driver.get(hd_url)
            return self.get_video(hd_url)
        else:
            try:
                embed_vid = driver.find_element_by_css_selector(
                    "div[id='embbed-video'] > IFRAME"
                )
                self.urls['video'] = embed_vid.get_attribute('SRC')

                driver.get(self.urls['video'])
                return self.urls['video']
            except:
                raise SystemExit(
                    '{0}: Could not find {1} episode {2} video URL {3}.'.format(
                        self.__class__, self.anime, self.episode, direct_link
                    )
                )


class KissAnime(Site):

    def get_anime(self):
        driver.get('http://www.kissanime.com')
        search_box = driver.find_element_by_css_selector(
            "input[id='keyword']"
        )
        search_box.send_keys(self.anime)
        sleep(1)
        try:
            results = driver.find_elements_by_css_selector(
                "div[id='result_box'] > a"
            )
            if len([r for r in results]) > 1:
                search_box.send_keys(' (sub)')
                sleep(1)
                results = driver.find_elements_by_css_selector(
                    "div[id='result_box'] > a"
                )
            results[0].click()
            self.urls['anime'] = driver.current_url
            return self.urls['anime']
        except (NoSuchElementException, AttributeError, IndexError):
            raise SystemExit(
                '{0}: Could not find {1} URL.'.format(self.__class__,
                                                      self.anime)
            )

    def get_episode(self):
        if self.urls['anime'] is None:
            self.get_anime()
        if driver.current_url != self.urls['anime']:
            driver.get(self.urls['anime'])

        episodes = driver.find_elements_by_css_selector(
            "table[class='listing'] a"
        )
        links = [
            (a.text, a.get_attribute('href'))
            for a in episodes
            if search('\D(00){0,2}%d$' % self.episode, a.text)
        ]
        try:
            self.urls['episode'] = links[0][1]
            return self.urls['episode']
        except (IndexError, TypeError):
            raise SystemExit(
                '{0}: Could not find {1} episode {2} URL.'.format(
                    self.__class__, self.anime, self.episode
                )
            )

    def get_video(self):
        if self.urls['episode'] is None:
            self.get_episode()
        if driver.current_url != self.urls['episode']:
            driver.get(self.urls['episode'])

        try:
            raw_link = search(
                "fmt_stream_map.*?';",
                driver.page_source
            ).group()
            raw_link = sub('fmt_stream.*?(?=https)', '', unquote(raw_link))
            link = sub('(?<=lh1).*[=]lh1', '', raw_link)

            self.urls['video'] = link
            driver.get(self.urls['video'])
            return self.urls['video']
        except:
            raise SystemExit(
                '{0}: Could not find {1} episode {2} video URL.'.format(
                    self.__class__, self.anime, self.episode
                )
            )

class Anime(object):

    def __init__(self, name):
        self.name = name

    def watch(self, episode):
        # grab all Site subclasses
        sources = [
            site_class for name, site_class in globals().items()
            if isclass(site_class) and name != 'Site'
            and issubclass(site_class, Site)
        ]
        # try to load video from the first site that works
        for site in sources:
            try:
                site(self.name, episode).get_video()
                break
            except SystemExit:
                pass


def main():

    start_browser()

    parser = create_parser()
    args = parser.parse_args()

    this_anime = Anime(args.name)
    this_anime.watch(args.episode)


if __name__ == '__main__':

    main()
