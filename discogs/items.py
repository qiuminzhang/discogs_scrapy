# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class DiscogsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    # this crawler extracts first three
    # the last three are extracted by other crawler

    album = Field()
    artist = Field()
    genre = Field()
    url = Field()

    # release_year = Field()
    image_url = Field()

    image = Field()

