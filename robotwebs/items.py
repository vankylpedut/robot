# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class RobotOfWeekItem(scrapy.Item):
    # url = scrapy.Field()
    # title = scrapy.Field()
    # content = scrapy.Field()
    # simple = scrapy.Field()
    # time = scrapy.Field()
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
    # image_paths = scrapy.Field()
    # page = scrapy.Field()
    # judge = scrapy.Field()  #0是不插information，1是插information

    # 命名必须对齐数据库字段名
    info_link = scrapy.Field()  # 连接
    info_title = scrapy.Field()  # 标题
    info_main = scrapy.Field()  # 正文
    reading_guidance = scrapy.Field()  # 导读
    info_summary = scrapy.Field()  # 梗概
    info_release_time = scrapy.Field()  # 记录时间
    image_urls = scrapy.Field()  #
    images = scrapy.Field()  #
    image_paths = scrapy.Field()  #
    page = scrapy.Field()  # 页数
    judge = scrapy.Field()  # 0是不插information，1是插information
    # 命名必须对齐RobotcontentItem字段名
    ITEM = 'item'
    LINK = 'info_link'
    TITLE = 'info_title'
    CONTENT = 'info_main'
    READING_GUIDANCE = 'reading_guidance'
    RELEASE_TIME = 'info_release_time'
    SUMMARY = 'info_summary'
    PAGE = 'page'
    JUDGE = 'judge'
