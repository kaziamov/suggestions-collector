import requests
from bs4 import BeautifulSoup

def getYoutubeTags(url):
    request = requests.get(url)
    html = BeautifulSoup(request.content,"html.parser")
    tags = html.find_all("meta", property="og:video:tag")

    for tag in tags:
        print(tag['content'])

url = ''
getYoutubeTags()