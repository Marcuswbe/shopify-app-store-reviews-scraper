import re
import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["apps.shopify.com"]

    # url comes from "-a url=<reviews-page>" CLI arg
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]

        # Extract the base slug so we can build ?page=N links ourselves
        m = re.match(r"(https://apps\.shopify\.com/[^/]+/reviews)", url)
        if not m:
            raise ValueError("Input URL must look like https://apps.shopify.com/<app>/reviews")
        self.base_reviews_url = m.group(1)

    def parse(self, response):
        containers = response.xpath('//div[@data-merchant-review]')

        # ---- yield each review ------------------------------------------------
        for c in containers:
            _id = c.xpath('./@data-review-content-id').get()
            content = " ".join(
                c.xpath('.//div[@data-truncate-review]//p[@class="tw-break-words"]/text()').getall()
            ).strip()
            rating = len(c.xpath('.//*[@xmlns and path/@d]').getall())
            yield {
                "id": _id,
                "username": c.xpath('.//*[@title]/@title').get(),
                "content": content,
                "rating": rating,
                "date": c.xpath('.//div[@class="tw-text-body-xs tw-text-fg-tertiary"]/text()').get().strip(),
                "country": c.xpath('./div[2]/div[2]/text()').get(),
                "time_using_app": c.xpath('./div[2]/div[3]/text()').get(),
            }

        # ---- build the *next* page URL manually ------------------------------
        # Current page number = ?page=N (default 1)
        current_page = int(response.url.split("page=")[-1]) if "page=" in response.url else 1
        next_page = current_page + 1
        next_url = f"{self.base_reviews_url}?page={next_page}"

        # If this page had reviews, assume the next page exists and follow it.
        # When we finally request a page that contains *zero* review containers,
        # Scrapy will call parse() with containers=[] and we stop naturally.
        if containers:
            yield response.follow(next_url, self.parse)
