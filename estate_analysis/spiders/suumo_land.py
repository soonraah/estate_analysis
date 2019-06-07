# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider


class SuumoLandSpider(Spider):
    name = 'suumo_land'
    allowed_domains = ['suumo.jp']
    start_urls = ['']

    def parse(self, response):
        bukken_urls = response.xpath('//div[@id="js-bukkenList"]/div/div['
                                       '@class="property_unit-content"]/div/h2/a/@href').getall()
        for url in bukken_urls:
            gaiyo_url = url.split('?')[0] + 'bukkengaiyo/'
            abs_url = 'https://suumo.jp/' + gaiyo_url
            yield scrapy.Request(abs_url, callback=self._parse_bukkengaiyo)

    def _parse_bukkengaiyo(self, response):
        tbody = response.xpath('//*[@id="mainContents"]/div/table/tbody')[0]

        return dict(
            url=response.url,
            place=self._extract_table_value(tbody, "所在地"),
            traffic=self._extract_table_value(tbody, "交通"),
            selling_lot=self._extract_table_value(tbody, "販売区画数"),
            total_lot=self._extract_table_value(tbody, "総区画数"),
            price=self._extract_table_value(tbody, "価格"),
            frequent_price_range=self._extract_table_value(tbody, "最多価格帯"),
            private_road=self._extract_table_value(tbody, "私道負担・道路"),
            expenses=self._extract_table_value(tbody, "諸費用"),
            land_area=self._extract_table_value(tbody, "土地面積"),
            building_coverage_and_floor_space_ratio=self._extract_table_value(tbody, "建ぺい率・容積率"),
            land_condition=self._extract_table_value(tbody, "土地状況"),
            creation_completion_time=self._extract_table_value(tbody, "造成完了時期"),

            # ToDo: 他の要素の追加
        )

    @staticmethod
    def _extract_table_value(tbody, name):
        value = tbody.xpath('./tr/th/div[text()="{}"]/parent::th/following-sibling::td[1]/text()'.format(name)).extract_first()
        return None if value == '-' else value.strip()
