#!/usr/bin/env python3
import scrapy
import re2 as re

from itemloaders.processors import Join, MapCompose, TakeFirst, Identity
from scrapy.utils.project import get_project_settings

from w3lib.html import remove_tags


def compose_title(value):
    return re.sub(" +", " ", value).strip()


def get_img_size(value):
    img_size = get_project_settings().get("KOLESA_IMG_SIZE")
    return re.sub(r"full\.", f"{img_size}.", value)


def get_numeric(value):
    if value is None:
        return

    return "".join(re.findall(r"\d+", value))


def compose_category(value):
    return "/".join(value)


def get_engine_volume(value):
    return "".join(re.findall(r"[0-9\.]+", value))


def get_engine_type(value):
    return "".join(re.findall("[а-я]+", value))


def strip_query_params(value):
    return value.split("?")[0]


class Car(scrapy.Item):
    source_url = scrapy.Field(
        output_processor=TakeFirst(),
    )
    source_id = scrapy.Field(
        input_processor=MapCompose(strip_query_params),
        output_processor=TakeFirst(),
    )
    city = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    body = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    rudder = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    color = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    customs_cleared = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    transmission = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    gearing = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    engine_type = scrapy.Field(
        input_processor=MapCompose(get_engine_type, str.strip),
        output_processor=TakeFirst(),
    )
    engine_volume = scrapy.Field(
        input_processor=MapCompose(get_engine_volume, str.strip),
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        # input_processor=MapCompose(remove_tags, compose_title),
        # output_processor=Join(),
        output_processor=TakeFirst(),
    )
    mortgaged_badge = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    new_badge = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    complectation = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst(),
    )
    exchange_check = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )
    brand = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    model = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    condition = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(get_numeric),
        output_processor=TakeFirst(),
    )
    mileage = scrapy.Field(
        input_processor=MapCompose(get_numeric),
        output_processor=TakeFirst(),
    )
    # avg_price = scrapy.Field(
    #     input_processor=MapCompose(get_numeric),
    #     output_processor=TakeFirst(),
    # )
    year = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    image = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
    category = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join(separator="/"),
    )
    images = scrapy.Field(
        input_processor=MapCompose(get_img_size, str.strip),
    )
    date_added = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst(),
    )
