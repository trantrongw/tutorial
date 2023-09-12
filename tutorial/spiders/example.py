import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from scrapy.spiders import SitemapSpider
from concurrent.futures import ThreadPoolExecutor

class ExampleSpider(SitemapSpider):
    name = "example"
    sitemap_urls = ['https://online.hsc.com.vn/sitemap.xml',
                    'https://www.hsc.com.vn/sitemap.xml',
                    'https://stockinsight.hsc.com.vn/sitemap_index.xml'
                    ]

    def __init__(self, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        edge_options = Options()
        edge_options.add_argument("--headless")
        self.driver = webdriver.Edge(options=edge_options)
        self.executor = ThreadPoolExecutor(max_workers=4)  # Adjust the number of workers as needed

    def parse(self, response):
        future = self.executor.submit(self._fetch_and_process, response)
        yield future.result()

    def _fetch_and_process(self, response):
        self.driver.get(response.url)
        html_content = self.driver.page_source
        # Your scraping logic here
        item = {
            'datacontent': html_content,
            'start_url': response.request.url,
        }
        return item

    def closed(self, reason):
        self.driver.quit()
        self.executor.shutdown()
