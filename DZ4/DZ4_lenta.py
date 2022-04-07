# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД
from lxml import html
import requests
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import hashlib
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['lenta_ru_news']
news = db.news

url = 'https://lenta.ru'
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
big_news = dom.xpath(".//div[@class='topnews__first-topic']//@href")
news_list = dom.xpath("//a[@class='card-mini _topnews']//@href")
news_list.append(big_news)


for news_link in news_list:
    if news_link[0] == '/':
        news_link = str(url) + str(news_link)
        news_table = {}
        response2 = requests.get(news_link, headers=header)
        dom2 = html.fromstring(response2.text)
        news_title = dom2.xpath("//h1[@class='topic-body__titles']//text()")
        news_date = dom2.xpath(".//time[@class='topic-header__item topic-header__time']//text()")
        news_parent = dom2.xpath(".//a[@class='topic-header__item topic-header__rubric']/text()")
        news_parent_site = dom2.xpath(".//a[@class='topic-header__item topic-header__rubric']/@href")

        news_table['news_title'] = news_title
        news_table['news_parent'] = news_parent
        news_table['news_parent_site'] = str(url) + str(news_parent_site[0])
        news_table['news_date'] = news_date
        news_table['news_link'] = news_link
        news_table['_id'] = hashlib.md5(str(news_table).encode('utf-8')).hexdigest()

        try:
            news.insert_one(news_table)
        except DuplicateKeyError:
            print(f"Document  {news_table['news_title']} already exist")

result = list(news.find({}))
pprint(result)
