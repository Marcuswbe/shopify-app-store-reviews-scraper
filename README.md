# Shopify App Store Reviews Scraper

## Installation

### Setup
1. Clone the repository 
```
git clone https://github.com/XavierZambrano/shopify-app-store-reviews-scraper.git
```
2. Create a virtual environment and activate it
3. Install the requirements
```bash
pip install -r requirements.txt
```

## Usage
To run the scraper, use the following command: (replace the url with the desired app store url)
```
scrapy crawl reviews -a url=https://apps.shopify.com/shopify-pos/reviews -O results.csv
```
For more information about scrapy crawl arguments, check the [Scrapy documentation](https://docs.scrapy.org/en/latest/topics/commands.html#std-command-crawl).

Example result: [results.csv](assets/results.csv)


## Notes
- The tests are very basic and can be broken easily. It will require update manually the expected results.