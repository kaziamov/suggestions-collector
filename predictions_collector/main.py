import itertools
import json
import os
import aiohttp
import asyncio
import time
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

    def __init__(self, queries):
        self._language_ = 'en'
        self._region_ = 'EN'
        self.queries = queries
        self.result = []
        self.session = requests.Session()

    def _get_request(self):
        pass

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

    def collect(self):
        if self.extend:
            self.extend_queries = self.queries.copy()
            for q in self.queries:
                self.extend_queries.extend([f"{q} {symbol}" for symbol in self.letters])
            self.queries = self.extend_queries
        for qyery in self.queries:
            self._get_request(qyery)
        return self

    async def _async_get_request(self, query):
        return self

    async def async_collect(self):
        # async with aiohttp.ClientSession() as session:
        for q in self.queries:
            task = self._async_get_request(q)
            self.tasks.append(task)

        results = await asyncio.gather(*self.tasks)
        for r in results:
            self.result.append(r)
        print(self.result)
        await self.session.close()
        return self


    def save_to_txt(self):
        # filename = make_clear_name(filename)
        filename = self.queries[0]
        dir = os.path.join(f'{filename}.txt')
        to_save = set(itertools.chain(*self.result))
        to_save = sorted(to_save)
        with open(dir, 'w', encoding='utf-8') as new_file:
            new_file.writelines(map(lambda x: f'{x}\n', to_save))

    # def _get_query_params(self.)


class YoutubeCollector(Collector):

    URL = 'http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&client=firefox&q={}'

    def __init__(self, query):
        super().__init__(query)

    async def _async_get_request(self, query):
        suggestions = Suggestions(language = self._language_, region = self._region_)
        self.result.append(suggestions.get(query, mode = ResultMode.json)['result'])
        return self

    def _get_request(self, query):
        suggestions = Suggestions(language = self._language_, region = self._region_)
        response = self.session.get(YoutubeCollector.URL.format(query))
        # options = {'hl': self.language,
        #     'gl': self.region,
        #     'q': query,
        #     'client': 'youtube',
        #     'gs_ri': 'youtube',
        #     'ds': 'yt',}
        # self.result.append(json.loads(suggestions.get(query, mode = ResultMode.json))['result'])
        result = response.json()
        self.result.append(result[1])
        return self


class GoogleCollector(Collector):

    URL = 'http://google.com/complete/search?client=chrome&q={}'

    def __init__(self):
        super().__init__()


    def _get_request(self, search_query):
        response = self.session.get(GoogleCollector.URL.format(search_query), headers=GoogleCollector.HEADERS)
        result = response.json()
        self.result.append(result[1])
        return self


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
    q = ['как в фигме ']
    c = YoutubeCollector(query=q)
    print(c.queries)
    start = time.perf_counter()
    c.set_ru_region().set_options(extend=True).collect()
    # asyncio.run(c.async_collect())
    print("Time: {}".format(time.perf_counter() - start))
    c.save_to_txt()
    # print(c.queries)