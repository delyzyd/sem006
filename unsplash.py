import scrapy
from ..items import UnsplashImageItem

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash'
    allowed_domains = ['unsplash.com']
    start_urls = ['https://unsplash.com/']

    def parse(self, response):
        # Найти ссылки на страницы категорий
        category_links = response.css('a[href*="collections/"]::attr(href)').getall()
        for link in category_links:
            yield response.follow(link, self.parse_category)

    def parse_category(self, response):
        # Найти ссылки на отдельные фотографии
        photo_links = response.css('a[href*="/photos/"]::attr(href)').getall()
        for link in photo_links:
            yield response.follow(link, self.parse_photo)
        
        # Пагинация
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_category)

    def parse_photo(self, response):
        item = UnsplashImageItem()
        item['image_url'] = response.css('img::attr(src)').get()
        item['name'] = response.css('h1::text').get()
        item['category'] = response.css('a[data-test="breadcrumb-link"]::text').get()
        yield item
