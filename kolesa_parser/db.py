#!/usr/bin/env python3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.session import object_session
from scrapy.utils.project import get_project_settings
import datetime


def db_connect():
    engine = create_engine(
        get_project_settings().get("CONNECTION_STRING"),
        connect_args={"connect_timeout": 5},
    )
    return engine


def get_session(engine):
    session = sessionmaker(bind=engine)()
    return session


engine = db_connect()
Base = automap_base()


class Listing(Base):
    __tablename__ = "offer"

    def as_dict(obj):
        data = obj.__dict__
        data.pop("_sa_instance_state")
        return data


class Region(Base):
    __tablename__ = "region"
    cities = relationship("City", back_populates="region")


class City(Base):
    __tablename__ = "city"
    region_id = Column(Integer, ForeignKey("region.id"))
    region = relationship("Region", back_populates="cities")


class Manufacturer(Base):
    __tablename__ = "manufacturer"
    brands = relationship("Brand", back_populates="manufacturer")


class Brand(Base):
    __tablename__ = "brand"
    manufacturer_id = Column(Integer, ForeignKey("manufacturer.id"))
    manufacturer = relationship("Manufacturer", back_populates="brands")


class SeriaBrand(Base):
    __tablename__ = "seria_brand"
    serias = relationship("Seria", back_populates="brand")


class Seria(Base):
    __tablename__ = "seria"
    seria_brand_id = Column(Integer, ForeignKey("seria_brand.id"))
    brand = relationship("SeriaBrand", back_populates="serias")

    models = relationship("SeriaModel", back_populates="seria")


class SeriaModel(Base):
    __tablename__ = "seria_model"
    seria_id = Column(Integer, ForeignKey("seria.id"))
    seria = relationship("Seria", back_populates="models")


class Job(Base):
    __tablename__ = "job"


class QueueParser(Base):
    __tablename__ = "queue"


def timestamp_now():
    return datetime.datetime.timestamp(datetime.datetime.now().replace(microsecond=0))


def queueParser_push(offer_id):
    q = QueueParser()
    q.channel = "parser"
    q.ttr = 300
    q.delay = 0
    q.priority = 1024
    q.pushed_at = timestamp_now()

    job_str = f'O:23:"common\\jobs\\OfferSearch":1:{{s:8:"offer_id";i:{offer_id};}}'
    q.job = bytes(job_str, 'utf-8')

    return q


Base.prepare(engine, reflect=True, generate_relationship=lambda *args, **kwargs: None)
