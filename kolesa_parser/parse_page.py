#!/usr/bin/env python3
import os
import logging

from scrapy.loader import ItemLoader


from kolesa_parser.items import Car
from kolesa_parser.debug_save import debug_save
from kolesa_parser.settings import BASEURL


def parse_page(response, card_link=None, card_date=None, card_title=None):
    # debug save when page isn't loaded properly
    if (
        not response.xpath("//h1[@class='offer__title']/span[@itemprop='brand']").get()
    ) and card_link is not None:

        item_id = os.path.basename(card_link)
        logging.error(
            f"Page isn't loaded properly. Saving it to file debug/{item_id}.html. Url: {response.url}"
        )

        debug_save(response.body, item_id)

    item = Car()

    il = ItemLoader(item, response=response)

    # данные из карточки в списках
    if card_link is not None:
        il.add_value("source_url", f"{BASEURL}{card_link}")
        il.add_value("source_id", os.path.basename(card_link))
    if card_title is not None:
        il.add_value("title", card_title)
    if card_date is not None:
        il.add_value("date_added", card_date)

    # определяем готов ли пользователь меняться по поиску ключевых слов в описании
    description = response.xpath(
        "//div[@class='offer__description']/div[last()][@class='text']/p/text()"
    ).get()
    il.add_value("description", description)

    il.add_value("exchange_check", check_exchange(description))

    # il.add_xpath("title", "//h1[@class='offer__title']/span")
    il.add_xpath(
        "category", "//div[@class='offer__breadcrumps']//a[@itemprop='url']/text()"
    )
    il.add_xpath("brand", "//span[@itemprop='brand']/text()")
    il.add_xpath("city", "//dt[@title='Город']/../dd/text()")
    il.add_xpath("body", "//dt[@title='Кузов']/../dd/text()")
    il.add_xpath("rudder", "//dt[@title='Руль']/../dd/text()")
    il.add_xpath("color", "//dt[@title='Цвет']/../dd/text()")
    il.add_xpath(
        "customs_cleared", "//dt[@title='Растаможен в Казахстане']/../dd/text()"
    )
    il.add_xpath("mileage", "//dt[@title='Пробег']/../dd/text()")

    il.add_xpath("transmission", "//dt[@title='Коробка передач']/../dd/text()")
    il.add_xpath("gearing", "//dt[@title='Привод']/../dd/text()")

    il.add_xpath("engine_type", "//dt[@title='Объем двигателя, л']/../dd/text()")
    il.add_xpath("engine_volume", "//dt[@title='Объем двигателя, л']/../dd/text()")

    il.add_xpath("model", "//span[@itemprop='name']/text()")
    il.add_xpath("year", "//span[@class='year']/text()")
    il.add_xpath("price", "//div[@class='offer__price']/text()")

    il.add_xpath(
        "complectation",
        "//div[@class='offer__description']/div[1][@class='text']/p/text()",
    )

    il.add_xpath("image", "//button[@class='gallery__main js__gallery-main']//img/@src")

    il.add_xpath(
        "images", "//ul[contains(@class, 'gallery__thumbs-list')]//button/@data-href"
    )

    il.add_xpath("new_badge", "//span[contains(@class, 'a-labels__item--new')]/text()")

    il.add_xpath(
        "mortgaged_badge",
        "//div[contains(@class, 'offer__parameters-mortgaged')]/text()",
    )

    return il.load_item()


def check_exchange(description: str | None) -> bool:
    if not description:
        return False

    description = description.lower()
    EXCHANGE_KEYWORDS = ["обмен", "меняю"]
    NO_EXCHANGE_KEYWORDS = [
        "не меняю",
        "без обмен",
        "нет обмен",
        "обмена нет",
        "обмен жок",
        "обмен жоқ"
        "обмена жок",
        "обмен не предлагать",
        "обмены не предлагать",
        "обмен не интересует",
        "обмены не интересуют",
    ]

    for keyword in NO_EXCHANGE_KEYWORDS:
        if description.find(keyword) != -1:
            return False

    for keyword in EXCHANGE_KEYWORDS:
        if description.find(keyword) != -1:
            return True

    return False
