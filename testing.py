from collections import namedtuple

import requests
from bs4 import BeautifulSoup

urlNews = namedtuple('urlNews', 'origin url depth_1 depth_2')


def generate_url(name):
    return f'https://www.{name.lower()}.pl'


def create_soup(url):
    response = requests.get(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    return BeautifulSoup(response.content, "html.parser")


class Scraper:

    url_list = (
        urlNews(
            origin='onet',
            url=generate_url('onet'),
            depth_1=('div', {'class': 'hpLiveColumn'}),
            depth_2=('span', {'class': 'title'})
        ),
        urlNews(
            origin='wp',
            url=generate_url('wp'),
            depth_1=('div', {'class', 'sc-1010b23-0 jmZodu'}),
            depth_2=('div', {'class': 'sc-1k2mbc5-1'})
        ),
        urlNews(
            origin='interia',
            url=generate_url('interia'),
            depth_1=('section', {'id', 'facts'}),
            depth_2='a'
        ),
        urlNews(
            origin='polsatnews',
            url=generate_url('polsatnews'),
            depth_1=('div', {'id': 'sg_slider'}),
            depth_2='img'
        )
    )

    def get_news(self):
        for data in self.url_list:
            origin, url, depth_1, depth_2 = data
            frame = create_soup(url).find_all(*depth_1)[0]

            if isinstance(depth_2, tuple):
                headers = frame.find_all(*depth_2)
            else:
                headers = frame.find_all(depth_2)



class WP:

    @staticmethod
    def download_news():
        soup = create_soup(generate_url('wp'))
        hs = soup.find_all('div', {'class', 'sc-1010b23-0 jmZodu'})
        headers = hs[0].find_all('div', {'class': 'sc-1k2mbc5-1'})
        print(list(h.text for h in headers))

        news = soup.find_all('div', {'class': 'njuxue-2 fhXiuI'})[0]
        for div in news.find_all('div'):
            try:
                if div['data-st-area'] == 'Wiadomosci':
                    pass
            except TypeError:
                pass