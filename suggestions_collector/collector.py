import asyncio
import aiohttp
import time
import requests
import json

class Collector:
    ENDPOINT = 'http://google.com/complete/search?client=chrome&q={}'
    HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    def __init__(self, search_query) -> None:
        self.search_query = search_query
        self.predictions = []
        self._tasks = []
        self.results = []


    def set_settings(self, language='en', deep=False, extend=False):
        self.language = language
        self.deep = deep
        self.extend = extend
        return self

    async def _create_get_task(self, session, prediction):
        async with session.get(Collector.ENDPOINT.format(prediction)) as request:
            if request.status == 200:
                return await request.json()[1]


    async def _get_tasks(self, session, predictions):
        new_tasks = []
        for prediction in predictions:
            task = asyncio.create_task(session, prediction)
            new_tasks.append(task)
        responses = await asyncio.gather(*new_tasks)
        return responses

    async def collect_keywords(self):
        async with aiohttp.ClientSession(headers=Collector.HEADERS) as session:
            response = requests.get(Collector.ENDPOINT.format(self.search_query))
            predictions = json.loads(response.text)[1]
            print(predictions)
            async for p in predictions:
                task = asyncio.create_task(session.get(Collector.ENDPOINT.format(p), ssl=False), name=p)
            # tasks = self._get_tasks(session=session, predictions=predictions)
            # self.responses = await asyncio.gather(*tasks)
            # for resp in self.responses:
            #     self.results.append(await resp.json()[1])
        return self


    def collect(self):
        asyncio.run(self.collect_keywords())


        # await self._session.close()


if __name__ == "__main__":
    c = Collector(['how blockchain'])
    start = time.perf_counter()
    c.set_settings().collect()
    end = time.perf_counter()
    print(c.results)
    print('Time result is {}'.format(end - start))
