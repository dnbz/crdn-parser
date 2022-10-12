#!/usr/bin/env python3
import scrapy
from scrapy.http.request import Request
import re2 as re

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from kolesa_parser.items import Car
from kolesa_parser.settings import BASEURL
from kolesa_parser.parse_page import parse_page
from twisted.internet.error import TimeoutError

URL = "https://kolesa.kz/a/show/142573607"


class KolesaDetailSpider(scrapy.Spider):
    name = "single-spider"
    start_urls = [URL]

    def __init__(self, detail=None, *args, **kwargs):
        super(KolesaDetailSpider, self).__init__(*args, **kwargs)

        if detail is not None:
            self.start_urls = [detail]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            callback=parse_page,
            meta={'proxy': None}
        )

    def exception_is_ban(self, request, exception):
        return isinstance(exception, TimeoutError)

    def parse(self, response):
        data = {}

        # data['city'] = response.xpath("//dt[@title='Город']/../dd/text()").get()
        category = response.xpath(
            "//div[@class='offer__breadcrumps']//a[@itemprop='url']/text()"
        ).getall()

        engine = response.xpath("//dt[@title='Объем двигателя, л']/../dd/text()").get()

        data["engine_type"] = "".join(re.findall("[а-я]+", engine))
        data["engine_volume"] = "".join(re.findall(r"[0-9\.]+", engine))

        data["category"] = "/".join(category)

        # print(data)
        return data
