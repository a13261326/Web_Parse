import scrapy
from scrapy.http import HtmlResponse
from castorama.items import CastoramaItem
from scrapy.loader import ItemLoader


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1[@class='product-essential__name hide-max-small']/text()")
        loader.add_xpath('price', "//span[@class='price']//text()")
        loader.add_xpath('photos', "//img[contains(@class,'top-slide__img swiper-lazy')]/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath("//h1[@class='product-essential__name hide-max-small']/text()").get()
        # price = response.xpath("//span[@class='price']//text()").get()
        # photos = response.xpath("//img[contains(@class,'top-slide__img swiper-lazy')]/@data-src").getall()
        # url = response.url
        # yield CastoramaItem(name=name, price=price, url=url, photos=photos)
