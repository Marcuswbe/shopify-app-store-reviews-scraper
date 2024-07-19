import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["apps.shopify.com"]
    start_urls = ["https://apps.shopify.com"]

    def parse(self, response):
        pass
