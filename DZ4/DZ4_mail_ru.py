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
db = client['mail_ru_news']
news = db.news


url = 'https://news.mail.ru/'
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
news_list = list(set(dom.xpath(".//div [@data-logger='news__MainTopNews']//@href")))


for news_link in news_list:
    news_table = {}
    response2 = requests.get(news_link, headers=header)
    dom2 = html.fromstring(response2.text)
    news_title = dom2.xpath("//h1[@class='hdr__inner']/text()")
    news_date = dom2.xpath(".//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    news_parent = dom2.xpath(".//a[@class='link color_gray breadcrumbs__link']//text()")
    news_parent_site = dom2.xpath(".//a[@class='link color_gray breadcrumbs__link']//@href")

    news_table['news_title'] = news_title
    news_table['news_parent'] = news_parent,news_parent_site
    news_table['news_date'] = news_date[0].replace('T', ' ')
    news_table['news_link'] = news_link
    news_table['_id'] = hashlib.md5(str(news_table).encode('utf-8')).hexdigest()

    try:
            news.insert_one(news_table)
    except DuplicateKeyError:
            print(f"Document  {news_table['news_title']} already exist")


result = list(news.find({}))
pprint(result)