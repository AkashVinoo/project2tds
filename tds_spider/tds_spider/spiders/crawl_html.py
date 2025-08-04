import scrapy
from urllib.parse import urljoin


class CrawlHtmlSpider(scrapy.Spider):
    name = "crawl_html"
    allowed_domains = ["sanand0.github.io"]
    start_urls = ["https://sanand0.github.io/tdsdata/wikipedia/"]

    def __init__(self):
        self.matching_files = []

    def parse(self, response):
        # Extract all links
        for href in response.css('a::attr(href)').getall():
            if href in ('../', './'):
                continue
            full_url = urljoin(response.url, href)
            if href.endswith('/'):
                # Recurse into subdirectory
                yield scrapy.Request(full_url, callback=self.parse)
            elif href.endswith('.html'):
                filename = href.split('/')[-1]
                first_letter = filename[0].upper()
                if 'J' <= first_letter <= 'W':
                    self.matching_files.append(full_url)
                    self.logger.info(f"MATCH: {full_url}")

    def closed(self, reason):
        print(f"\nNumber of HTML files starting with letters J through W (inclusive): {len(self.matching_files)}")
        if self.matching_files:
            print("\nMatching files:")
            for url in self.matching_files:
                print(url)
        else:
            print("\nNo matching files found.")
