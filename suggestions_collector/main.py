import itertools
import os
import time
# import requests
import grequests
from string import ascii_letters, digits

cyrillic_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


class Collector():

    def __init__(self, queries):
        self._language_ = 'en'
        self._region_ = 'EN'
        self.queries = queries
        self.result = []
        self.session = grequests.Session()
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

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
                self.extend_queries.extend(
                    [f"{q} {symbol}" for symbol in self.letters])
            self.queries = self.extend_queries
        for qyery in self.queries:
            self._get_request(qyery)
        if self.deep:
            self.collect
        return self

    def _get_request(self, query):
        response = self.session.get(self.url.format(query))
        result = response.json()
        self.result.append(result[1])
        return self

    def save_to_txt(self):
        filename = self.queries[0]
        dir = os.path.join(f'{filename}.txt')
        to_save = set(itertools.chain(*self.result))
        to_save = sorted(to_save)
        with open(dir, 'w', encoding='utf-8') as new_file:
            new_file.writelines(map(lambda x: f'{x}\n', to_save))


class YoutubeCollector(Collector):

    def __init__(self, queries):
        super().__init__(queries)
        self.url = 'http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&client=firefox&q={}'


class GoogleCollector(Collector):

    def __init__(self, queries):
        super().__init__(queries)
        self.url = 'http://google.com/complete/search?client=chrome&q={}'


if __name__ == '__main__':
    q = ['как в фигме ']
    c = GoogleCollector(queries=q)
    print(c.queries)
    start = time.perf_counter()
    c.set_ru_region().set_options(extend=True).collect()
    print("Time: {}".format(time.perf_counter() - start))
    c.save_to_txt()
