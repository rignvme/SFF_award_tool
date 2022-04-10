import scrapy


class AwardsSpider(scrapy.Spider):
    name = 'awards'
    allowed_domains = ['test.com']
    start_urls = ['http://www.sfadb.com/World_Fantasy_Awards_2021']

    def parse(self, response):

        title = response.css('li::text').extract()

        return({"A": title})

