import os
import json
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase
from scrapy.http import HtmlResponse

from shopify_app_store.spiders.reviews import ReviewsSpider


with Betamax.configure() as config:
    cassette_library_dir = 'test/fixtures/cassettes'
    os.makedirs(cassette_library_dir, exist_ok=True)
    config.cassette_library_dir = cassette_library_dir
    config.preserve_exact_body_bytes = True


if 'unittest.util' in __import__('sys').modules:
    # Show full diff in case of failure
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999


class TestReviewsSpider(BetamaxTestCase):
    def setUp(self):
        super().setUp()

        self.maxDiff = None
        process = CrawlerProcess(install_root_handler=False)
        process.crawl(ReviewsSpider)
        self.spider = list(process.crawlers)[0].spider

    def test_parse_id(self):
        mock_response = self.get_mock_response('https://apps.shopify.com/shopify-pos/reviews')
        expected_result = '1431992'

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(result['id'], expected_result)

    def test_parse_username(self):
        mock_response = self.get_mock_response('https://apps.shopify.com/shopify-pos/reviews')
        expected_result = 'Loshen & Crem'

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(result['username'], expected_result)

    def test_parse_content(self):
        mock_response = self.get_mock_response('https://apps.shopify.com/shopify-pos/reviews')
        expected_result = '''I regret having to leave a negative review for Shopify POS. Our experience has been terrible. We needed a system to consolidate our inventory in one place, and despite the bad reviews, we decided to give it a try anyway. Unfortunately, the negative reviews were right. It's disappointing to see a big company like Shopify unable to fix their POS issues. We've lost numerous sales because their hardware wasn't working properly. Now, the system is completely dead, and according to their support, we have to wait 48 hours for a resolution. TERRIBLE.'''

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(result['content'], expected_result)

    def test_parse_rating(self):
        mock_response = self.get_mock_response('https://apps.shopify.com/shopify-pos/reviews')
        expected_result = 1

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(result['rating'], expected_result)

    def test_parse_date(self):
        mock_response = self.get_mock_response('https://apps.shopify.com/shopify-pos/reviews')
        expected_result = 'June 10, 2024'

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(result['date'], expected_result)

    def test_parse_country(self):
        mock_response = self.get_mock_response('https://apps.shopify.com/shopify-pos/reviews')
        expected_result = 'Canada'

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(result['country'], expected_result)

    def test_parse_time_using_app(self):
        mock_response = self.get_mock_response('https://apps.shopify.com/shopify-pos/reviews')
        expected_result = 'Almost 5 years using the app'

        generator = self.spider.parse(mock_response)
        result = next(generator)

        self.assertEqual(result['time_using_app'], expected_result)

    def get_mock_response(self, url):
        response = self.session.get(url)
        scrapy_response = HtmlResponse(body=response.content, url=url)

        return scrapy_response
