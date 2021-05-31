from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from itemloaders import ItemLoader
import logging

from scrapy.crawler import CrawlerProcess


class News(Item):
    """Clase que hereda de Item, que modela la noticia de  la pagina a Scrapear"""
    id = Field()
    title = Field()
    # content = Field()


class AljazeeraSpider(Spider):
    name = "AljazeeraSpider"
    custom_settings = {
        'USER_AGENT': 'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18',
        'LOG_LEVEL': logging.WARNING,
        'FEEDS': {
            'news.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'overwrite': True
            }
        }
    }
    start_urls = [
        'https://www.aljazeera.com/news/2019/01/latin-america-2019-stories-watch-190102132047518.html']

    def parse(self, response):
        sel = Selector(response)
        list_of_news = sel.xpath(
            '//div[contains(@class, "wysiwyg--all-content")]/h2[not(strong)]')
        # ?print(list_of_news.getall())
        i = 0
        for title in list_of_news:
            item = ItemLoader(News(), title)
            item.add_xpath("title", "./text()")
            item.add_value("id", i)
            i += 1
            yield item.load_item()


def main():
    process = CrawlerProcess()
    process.crawl(AljazeeraSpider)
    process.start()


if __name__ == "__main__":
    main()
