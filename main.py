# hw9 part 2

import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from hw8.seeds import autors_add, quotes_add


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class DataPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        if 'quote' in adapter.keys():
            self.quotes.append(dict(adapter))
        

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=4)
        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=4)


class QuotesSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"ITEM_PIPELINES": {DataPipline: 300}}

    def parse(self, response, *args):
        for q in response.xpath("/html//div[@class='quote']"):
            tags = q.xpath("div[@class='tags']/a/text()").extract()
            author = q.xpath("span/small/text()").get().strip()
            quote= q.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, quote=quote)
            yield response.follow(url=self.start_urls[0] + q.xpath('span/a/@href').get(),
                                  callback=self.parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response, *args):
        author = response.xpath('/html//div[@class="author-details"]')
        fullname = author.xpath('h3[@class="author-title"]/text()').get().strip().replace("-"," ")
        born_date = author.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        born_location = author.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        description = author.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()

    print("---adding authors to DB---")
    with open("authors.json", encoding='utf-8') as file:
        autors_add(json.load(file))

    print("---adding qoutes to DB---")
    with open("quotes.json", encoding='utf-8') as file:
        quotes_add(json.load(file))


