#!/usr/bin/env python3
import logging
import datetime

import dateparser

from sqlalchemy.orm import sessionmaker

from kolesa_parser.db import (
    Listing,
    City,
    Region,
    Brand,
    SeriaModel,
    Seria,
    SeriaBrand,
    QueueParser,
    queueParser_push,
    get_session,
    engine,
)

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def time_now():
    return datetime.datetime.now().replace(microsecond=0)


class SaveCarPipeline:
    def open_spider(self, spider):
        self.session = get_session(engine)

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        session = self.session

        if spider.name in ["single-spider"]:
            return item

        # avoid duplicates
        listing = (
            session.query(Listing)
            .filter(Listing.source_id == item["source_id"])
            .first()
        )

        if listing is not None:
            logging.info(f"Item is already present in the database. Skipping...")
            spider.items_no_new += 1
            return item

        listing = Listing()

        listing.url = item["source_url"]
        listing.source_id = item["source_id"]

        # why is this parameter occasionally empty?
        listing.category = item.get("category")

        listing.name = item["title"]
        listing.year = item["year"]
        listing.price = item["price"]

        # заполняем страну-производителя на основании марки
        listing.brand = item["brand"]
        listing.model = item.get("model")

        brand = session.query(Brand).filter(Brand.name.ilike(listing.brand)).first()
        if brand is not None:
            listing.manufacturer = brand.manufacturer.ru

        # заполняем серию на основании марки и модели
        if (listing.model is not None) and (listing.brand is not None):
            seria = (
                session.query(Seria)
                .join(SeriaBrand)
                .join(SeriaModel)
                .filter(
                    SeriaModel.name.ilike(listing.model),
                    SeriaBrand.name.ilike(listing.brand),
                )
                .first()
            )
        else:
            seria = None

        if seria is not None:
            listing.seria = seria.name

        # подбираем подходящий регион в зависимости от города
        listing.city = item.get("city")
        city = session.query(City).filter(City.name.ilike(listing.city)).first()
        if city is not None:
            listing.region = city.region.name

        listing.body = item.get("body")

        if item.get("source_engine_type") == "электрический":
            listing.engine_type = "Электричество"
        else:
            listing.engine_type = item.get("engine_type")

        listing.engine_volume = item.get("engine_volume")
        listing.transmission = (
            "АКПП"
            if item.get("transmission") == "механика"
            else item.get("transmission")
        )
        listing.transmission_description = item.get("transmission")
        listing.customs_cleared = item.get("customs_cleared")
        listing.color = item.get("color")
        listing.rudder = item.get("rudder")
        listing.gearing = item.get("gearing")
        listing.mileage = item.get("mileage")

        listing.description = (
            item.get("description")[:254]
            if item.get("description") is not None
            else None
        )

        listing.exchange_check = item.get("exchange_check")
        listing.complectation = (
            item.get("complectation")[:254]
            if item.get("complectation") is not None
            else None
        )

        # состояние машины
        if item.get("mortgaged_badge") is not None:
            listing.condition = "Аварийная/Не на ходу"
        elif item.get("new_badge") is not None:
            listing.condition = "Новая"
        else:
            listing.condition = "На ходу"

        listing.source_added_at = dateparser.parse(item.get("date_added", ""))

        listing.update_at = time_now()
        listing.create_at = time_now()

        image = item.get("image")

        # картинка на модерация или нет картинки
        if (image is None) or (image.find("Moderation") > 0):
            listing.image = "no image"
            listing.image_check = True
        else:
            listing.image = image
            listing.image_check = False

        listing.images = item.get("images")

        # listing.percent_price = ""
        # listing.avg_price = item["avg_price"]

        # queue parser notification job
        queue = queueParser_push(listing.source_id)

        try:
            session.add(listing)
            session.add(queue)
            session.commit()

            spider.crawler.stats.inc_value("db_added_items")
            spider.items_no_new = 0

        except:
            session.rollback()
            raise

        return item
