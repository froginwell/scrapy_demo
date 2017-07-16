# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os


class JokeOfToutiaoPipeline(object):

    def __init__(self):
        joke_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'spiders/joke.txt')
        self.joke_file = open(joke_file_path, 'ab')
        self.count = 0

    def process_item(self, item, spider):
        joke = item['joke']
        self.count += 1
        joke = ''.join(
            [bytes(self.count),
             b'. ',
             joke.encode('utf-8', 'ignore'),
             b'\n\n'])
        self.joke_file.write(joke)

        return item

    def close_spider(self, spider):
        self.joke_file.close()
