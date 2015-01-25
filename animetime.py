# TODO: minimize FF windows (if stick with selenium)
# http://stackoverflow.com/questions/2791489/how-do-i-take-out-the-focus-or-minimize-a-window-with-python

import argparse as ap
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from re import search

driver = None


def start_browser():
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    return driver


def stop_browser():
    global driver
    driver.quit()


def create_parser():
    # TODO: add program description & help text
    parser = ap.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('episode')
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


class Anime(object):

    def __init__(self, name):
        self.name = name

    def watch(self, episode):
        AnimeShow(self.name, episode).get_video()


def main():

    start_browser()

    parser = create_parser()
    args = parser.parse_args()

    this_anime = Anime(args.name)
    this_anime.watch(args.episode)


if __name__ == '__main__':

    main()