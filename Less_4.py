from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

url = 'https://lenta.ru/'
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

client = MongoClient('127.0.0.1', 27017)
db = client['news']
newsdb = db.newsdb

news_list = dom.xpath("//a[contains(@class,'_topnews')]")
news = []
for newsi in news_list:
    news_info = {}
    title = newsi.xpath(".//h3[@class='card-big__title']/text() | "".//span[contains(@class,'card-mini__title')]/text()")
    link = newsi.xpath("./@href")
    time = newsi.xpath(".//time/text()")
    sourse = 'https://lenta.ru/'

    news_info['title'] = title
    news_info['link'] = link
    news_info['time'] = time
    news_info['sourse'] = sourse

    try:
        newsdb.insert_one(news_info)
    except DuplicateKeyError:
        print(f"Document  {news_info['title']} already exist")

    result = list(newsdb.find({}))
    pprint(result)