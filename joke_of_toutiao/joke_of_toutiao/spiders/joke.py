# -*- coding: utf-8 -*-
import json
import random
import time

import scrapy
from joke_of_toutiao.items import JokeOfToutiaoItem


class JokeSpider(scrapy.Spider):
    name = 'joke'
    start_urls = [
        'http://www.toutiao.com/api/article/feed/?category=essay_joke&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A12529565B53C57&cp=596B730C45272E1',
    ]
    url_template = 'http://www.toutiao.com/api/article/feed/?category=essay_joke&utm_source=toutiao&widen=1&max_behot_time={max_behot_time}&max_behot_time_tmp={max_behot_time}&tadrequire=true&as=A115C9B66B93F7E&cp=596BF3EF171EDE1'

    def parse(self, response):
        json_data = json.loads(response.text)
        jokes = json_data.get('data', [])
        for joke in jokes:
            joke = joke['group']['content']
            joke_item = JokeOfToutiaoItem()
            joke_item['joke'] = joke
            yield joke_item

        # 请求下一批数据
        if json_data.get('has_more', False):
            max_behot_time = json_data['next']['max_behot_time']
            url = self.url_template.format(max_behot_time=max_behot_time)
            req = scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=False)
            time.sleep(10 + 10 * random.random())
            yield req
