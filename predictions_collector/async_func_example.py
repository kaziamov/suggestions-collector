import time
import asyncio

def get_number():
    counter = 0
    while True:
        yield counter
        counter += 1

numbers = get_number()

async def counter_async():
    print('Hello')

# task = asyncio.create_task(counter_async())
asyncio.run()