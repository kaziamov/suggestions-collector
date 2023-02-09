from bs4 import BeautifulSoup
import requests

def make_deep_collect(action, keyword, sorting=False):
    first_circle = action(keyword)
    second_circle = itertools.chain.from_iterable(map(action, first_circle))
    if sorting:
        return set(sorted(second_circle))
    return set(second_circle)


def get_youtube_tags(url):
    request = requests.get(url)
    html = BeautifulSoup(request.content, "html.parser")
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
