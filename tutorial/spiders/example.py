import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from scrapy.spiders import SitemapSpider

class ExampleSpider(SitemapSpider):
    name = "example"
    sitemap_urls = ['https://online.hsc.com.vn/sitemap.xml']  # Note: Changed from start_urls to sitemap_urls

    def __init__(self, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)  # Call superclass's __init__
        edge_options = Options()
        edge_options.add_argument("--headless")
        self.driver = webdriver.Edge(options=edge_options)

    def parse(self, response):
        self.driver.get(response.url)
        html_content = self.driver.page_source
        # Your scraping logic here
        item = {
            'datacontent': html_content,
            'start_url': response.request.url,
        }
        yield item

    def closed(self, reason):
        self.driver.quit()
