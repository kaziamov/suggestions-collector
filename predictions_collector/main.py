import itertools
import json
import os

import requests
from bs4 import BeautifulSoup
from youtubesearchpython import ResultMode, Suggestions

from string import ascii_letters, digits

cyrillic_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

class Collector():

    HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    URL = None

    def __init__(self, query):
        self._language_ = 'en'
        self._region_ = 'EN'
        self.query = query

    def _get_request(self):
        pass

    def collect(self):
        self._get_request()
        return self

    def set_options(self, extend=False, deep=False):
        self.extend = extend
        self.deep = deep
        return self

    def set_ru_region(self):
        self._language_ = 'ru'
        self._region_ = 'RU'
        self.letters = cyrillic_letters + digits
        return self

    def set_en_region(self):
        self._language_ = 'en'
        self._region_ = 'EN'
        self.letters = ascii_letters + digits
        return self

    def save_to_txt(self, filename='result', prefix=None):
        filename = make_clear_name(filename)
        dir = os.path.join(f'{filename}.txt')
        with open(dir, 'w', encoding='utf-8') as new_file:
            new_file.writelines(map(lambda x: f'{x}\n', self.result))


class YoutubeCollector(Collector):

    def __init__(self, query):
        super().__init__(query)

    def _get_request(self):
        suggestions = Suggestions(language = self._language_, region = self._region_)
        self.result = json.loads(suggestions.get(self.query, mode = ResultMode.json))['result']
        return self


class GoogleCollector(Collector):

    URL = 'http://google.com/complete/search?client=chrome&q={}'

    def __init__(self):
        super().__init__()


    def _get_request(self, search_query):
        response = requests.get(GoogleCollector.URL.format(search_query), headers=GoogleCollector.HEADERS)
        return json.loads(response.text)[1]


class Parsing():

    def __init__(self, queries, parsing_methods):
        self.queries = queries
        self._parsing_methods = parsing_methods
        self.collect_values = {}


    def collect(self):
        for query in self.queries:
            self.collect_values.setdefault(query, [])
            for method in self._parsing_methods:
                self.collect_values.extend(method.collect(query))

    def collect_old(self):
        # self.collect_list = itertools.chain.from_iterable(map(self._get_request, self.queries))
        pass

    def reset(self):
        self.queries = {}


collect_methods = [
    YoutubeCollector,
    GoogleCollector
]

def make_deep_collect(action, keyword, sorting=False):
    first_circle = action(keyword)
    second_circle = itertools.chain.from_iterable(map(action, first_circle))
    if sorting:
        return set(sorted(second_circle))
    return set(second_circle)

# def get_google_suggestions(search):
#     URL=f"http://suggestqueries.google.com/complete/search?client=firefox&q={search}"
#     headers = {'User-agent':'Mozilla/5.0'}
#     response = requests.get(URL, headers=headers)
#     result = json.loads(response.content.decode('utf-8'))
#     return result[1]



def get_youtube_tags(url):
    request = requests.get(url)
    html = BeautifulSoup(request.content,"html.parser")
    tags = html.find_all("meta", property="og:video:tag")
    title = html.find('title').text
    return title, [tag['content'] for tag in tags]

def make_clear_name(name):
    return '-'.join(name.replace(' - Youtube', '').split())


def generate_aliases(tags, origin, alias):
    return sorted([tag.replace(origin, alias) for tag in tags if origin in tag].extend(tags))

def load_keywords(filepath='Keywords.txt'):
    with open(filepath, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == '__main__':
    q = 'как в фигма'
    c = YoutubeCollector(query=q)
    c.set_ru_region().set_options(extend=True).collect().save_to_txt()