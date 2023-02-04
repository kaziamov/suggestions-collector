import asyncio
import itertools
import json
import os

import aiohttp
from bs4 import BeautifulSoup
from youtubesearchpython import ResultMode, Suggestions

class Collector():
    HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    URL = None

    def __init__(self):
        self._language_ = 'en'
        self._region_ = 'EN'

    async def _get_request(self, search_query):
        pass

    async def collect(self, search_query):
        return await self._get_request(search_query)

    def set_ru_region(self):
        self._language_ = 'ru'
        self._region_ = 'RU'

    def set_en_region(self):
        self._language_ = 'en'
        self._region_ = 'EN'

    async def save_to_txt(self, filename, lines, prefix=None):
        filename = make_clear_name(filename)
        dir = os.path.join(f'{filename}.txt')
        async with aiofiles.open(dir, 'w', encoding='utf-8') as new_file:
            await new_file.writelines(map(lambda x: f'{x}\n', lines))
