import scrapy
from scrapy.http import HtmlResponse
from book24.items import Book24Item


class Book24Spider(scrapy.Spider):
    name = 'book_24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/']

    # def parse_last_page(self, response: HtmlResponse):
    #     # last_page_num = 0
    #     last_page_num = response.xpath("//a[class ='pagination__item _link']")
    #     start_urls = []
    #     for n in range(1, 8500):
    #         start_urls.append(f'https://book24.ru/catalog/page-{last_page_num}')

    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__image-link smartLink']//@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        book_link = response.url
        author = response.xpath(
            "//div[@class='product-characteristic__value']/a[@class='product-characteristic-link smartLink']/text()").extract_first()
        name = response.xpath("//h1[@class='product-detail-page__title']/text()").extract()[0]
        price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").extract_first()
        price_old = response.xpath(
            "//div[@class='product-sidebar-price product-sidebar__price-holder']/span[@class='app-price product-sidebar-price__price-old']/text()").extract()[0]
        rating = response.xpath("//span[@class='rating-widget__main-text']/text()").extract_first()

        yield Book24Item(author=author, book_link=response.url, name=name, price=price, price_old=price_old, rating=rating)

