from time import process_time
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
    content = Field()


class AljazeeraSpider(Spider):
    name = "AljazeeraSpider"
    custom_settings = {
        'USER_AGENT': 'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18',
        'LOG_LEVEL': logging.WARNING,
        'FEEDS': {
            'news.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'overwrite': True,
                'fields': ['id', 'title', 'content'],
            }
        }
    }
    start_urls = [
        'https://www.aljazeera.com/news/2019/01/latin-america-2019-stories-watch-190102132047518.html']

    def parse(self, response):
        sel = Selector(response)
        list_of_elements = sel.xpath(
            '//div[contains(@class, "wysiwyg--all-content")]//child::*')
        # ?print(list_of_elements.getall())

        dic = {}
        flag_h2 = False
        for element in list_of_elements:
            if len(element.re('<h2>')) > 0:
                title = element.xpath('./text()').getall()
                if(len(title) > 0):
                    title = title[0]
                    content = dic.get(title, "")
                    flag_h2 = True
                else:
                    break

            elif len(element.re('<p>')) > 0:
                p = "".join(element.xpath('.//text()').getall())
                if flag_h2:
                    content += p
                    dic[title] = content
        # ?print(dic)
        i = 0
        for key, value in dic.items():
            item = ItemLoader(News())
            item.add_value("id", i)
            item.add_value("title", key)
            item.add_value("content", value)
            i += 1
            yield item.load_item()


def main():
    process = CrawlerProcess()
    process.crawl(AljazeeraSpider)
    process.start()


if __name__ == "__main__":
    main()
