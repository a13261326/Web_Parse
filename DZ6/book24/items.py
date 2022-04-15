# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Book24Item(scrapy.Item):
    name = scrapy.Field()
    book_link = scrapy.Field()
    price = scrapy.Field()
    price_old = scrapy.Field()
    rating = scrapy.Field()
    author= scrapy.Field()
    _id = scrapy.Field()