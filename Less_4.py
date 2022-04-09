from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

url = 'https://lenta.ru/'
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)


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

    news.append(news_info)

pprint(news)


client = MongoClient('127.0.0.1', 27017)  # соединение
mongodb = client['news']  # база
newsdb = mongodb.newsdb  # коллекция

for newsi in news:
    try:
        newsi['_id'] = newsi['link']
        newsdb.insert_one(newsi)
    except Exception as e:
        print('Ошибка при сохранении новости в базу:')
        print(e)


