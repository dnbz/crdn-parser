#!/usr/bin/env python3
import scrapy
import logging
import time
import os

from urllib.parse import urlparse
from urllib.parse import parse_qs

from scrapy import signals
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings

from scrapy.downloadermiddlewares.retry import get_retry_request
from kolesa_parser.items import Car
from kolesa_parser.helpers import debug_save
from kolesa_parser.helpers import get_desktop_retry_request
from kolesa_parser.parse_page import parse_page

from kolesa_parser.db import get_session, engine, Job


def get_page(url):
    current_url = urlparse(url)
    query = parse_qs(current_url.query)

    if query is None or query.get("page") is None:
        return 0

    return int(query["page"][0])


class KolesaSpider(scrapy.Spider):
    name = "kolesa-spider"
    BASEURL = "kolesa.kz"

    DOMAIN_NAME = get_project_settings().get("DOMAIN_NAME")
    parser_node = get_project_settings().get("PARSER_NODE")

    page = 1
    max_pages = get_project_settings().get("KOLESA_MAX_PAGES")

    items_no_new = 0
    stop_items = float("inf")

    def __init__(self, page=None, stop=None, *args, **kwargs):
        super(KolesaSpider, self).__init__(*args, **kwargs)

        self.session = get_session(engine)

        if page is not None:
            self.start_urls = [page]
        else:
            self.start_urls = self.get_job_urls()

        if stop is not None:
            self.max_pages = int(stop)

        # stopping if certain number of items were already in db
        page_stop = get_project_settings().get("PAGE_STOP_NO_NEW")
        if page_stop is not None:
            page_size = get_project_settings().get("PAGE_SIZE")
            self.stop_items = int(page_stop) * page_size

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KolesaSpider, cls).from_crawler(crawler, *args, **kwargs)

        # Запуск функции open_spider при инициализации
        crawler.signals.connect(spider.open_spider, signal=signals.spider_opened)

        return spider

    def open_spider(self):
        # количество карточек из списков
        self.crawler.stats.set_value("total_card_items", 0)
        self.crawler.stats.set_value("db_added_items", 0)

    def get_job_urls(self):
        query = self.session.query(Job)
        if self.parser_node is not None:
            query = query.filter(Job.server == self.parser_node)
        job_urls = [job.base_url for job in query.all()]

        logging.info(f"Jobs urls: {job_urls}")

        return job_urls

    def parse(self, response):
        car_cards = response.xpath(
            "//div[@class='a-list__item']/div[contains(@class, 'a-card') and not(contains(@class, 'item-banner'))]"
        )
        self.crawler.stats.inc_value("total_card_items", len(car_cards))

        for card in car_cards:

            date = card.xpath(
                ".//span[contains(@class, 'a-card__param--date')]/text()"
            ).get()

            link = card.xpath(".//a[@class='a-card__link']/@href").get()

            title = card.xpath(".//a[@class='a-card__link']/text()").get()

            index_card_data = {
                "card_link": link,
                "card_date": date,
                "card_title": title,
            }

            yield response.follow(
                link,
                callback=self.handle_page,
                cb_kwargs=index_card_data,
                meta={"dont_redirect": True},
            )

        yield self.paginate(response)

    def handle_page(self, response, **kwargs):
        return parse_page(response, **kwargs)

    def paginate(self, response):

        current_page = get_page(response.url)
        if current_page > self.max_pages:
            logging.info(f"Stopping on page {self.max_pages}. Skipping...")
            return
            # raise CloseSpider(f"stop on page {self.max_pages}")
        elif self.items_no_new > self.stop_items:
            logging.info(
                f"Parsed {self.items_no_new} without new items written to DB. Skipping..."
            )
            return

        next_page_link = response.xpath("//a[contains(@class,'next_page')]/@href").get()

        if next_page_link is None:
            # next_page_link = re.sub(r"page=\d+", f"page={self.page}", response.url)
            logging.warning(
                f"Can't parse next page. Current page {response.url}. Skipping..."
            )
        else:
            return response.follow(
                next_page_link, self.parse, meta={"dont_redirect": True}
            )
