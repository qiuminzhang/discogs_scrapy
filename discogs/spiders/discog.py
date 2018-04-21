# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from discogs.items import DiscogsItem
import os
import urllib.request

# cd C:\Users\qyao7\PycharmProjects\discogs
# scrapy crawl discog -s LOG_FILE=scrapy.log


class DiscogSpider(scrapy.Spider):
    name = 'discog'
    allowed_domains = ['www.discogs.com']

    base_url = 'https://www.discogs.com/search/?limit=250&genre_exact={0}&page={1}'
    host_url = 'https://www.discogs.com'
    # 'Rock', 'Pop' - 4520
    # genres = ['Electronic', 'Folk%2C+World%2C+%26+Country', 'Jazz', 'Funk+%2F+Soul', 'Hip+Hop', 'Reggae',
    #           'Latin', 'Blues', 'Stage+%26+Screen', 'Classical', 'Non-Music', 'Children%27s', 'Brass+%26+Military']
    genres = ['Pop']
    pns = range(1, 41)
    items = []

    def start_requests(self):
        urls = [self.base_url.format(genre, pn) for genre in self.genres for pn in self.pns]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def download_pic(self, genre, image_url):
        first_name = image_url[-18:]
        path = '''Q:\discogsimages\\''' + genre + '\_' + genre + '_' + first_name
        path = path.replace('/', '_')
        if not os.path.exists(path):
            urllib.request.urlretrieve(image_url, path)
        else:
            print("this pic already exists, no more download")
            pass

    def parse(self, response):
        """
        get album_url, album_name, genre
        :param response:
        """
        url = response.url
        genre = re.search('genre_exact=(.*?)&page=', url).group(1)
        album_name = response.xpath('''//*[@id="search_results"]/div/h4/a/text()''').extract()
        links = response.xpath('''//*[@id="search_results"]/div/h4/a/@href''').extract()

        for (album, link) in zip(album_name, links):
            item = DiscogsItem(genre=genre, album=album, url=self.host_url+link)
            self.items.append(item)

        for item in self.items:
            yield Request(item['url'], self.parse_info, meta={'item': item})
            # yield item

    def parse_info(self, response):
        """
        get artist and image_url
        :param response:
        :return:
        """
        item = response.meta['item']
        url = response.url
        artist = response.xpath('''//*[@id="profile_title"]/span[1]/span/a/text()''').extract_first()
        item['artist'] = artist
        image_url = response.xpath('''//*[@property="og:image"]/@content''').extract_first()
        item['image_url'] = image_url
        print('step 2')
        yield item
        # Save image to local file Q:\discogsimages
        self.download_pic(item['genre'], image_url)

        # yield Request(item['image_url'], self.parse_image_url, meta={'item': item})

    # def parse_image_url(self, response):
    #     print('Hi there')
    #     item = response.meta['item']
    #     yield item








