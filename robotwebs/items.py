# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class RobotOfWeekItem(scrapy.Item):
    # 命名必须对齐数据库字段名
    info_link = scrapy.Field()  # 连接
    info_title = scrapy.Field()  # 标题
    info_main = scrapy.Field()  # 正文
    reading_guidance = scrapy.Field()  # 导读
    info_summary = scrapy.Field()  # 梗概
    info_release_time = scrapy.Field()  # 文章发布的时间
    info_record_time = scrapy.Field()  # 爬取的时间
    image_urls = scrapy.Field()  #
    images = scrapy.Field()  #
    image_paths = scrapy.Field()  #
    page = scrapy.Field()  # 页数
    judge = scrapy.Field()  # 0是不插information，1是插information
    info_category_name = scrapy.Field()  # 类别
    info_category_id = scrapy.Field()  # 类别id
    info_source = scrapy.Field()  # 来源
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
    CATEGORY_NAME = 'info_category_name'
    CATEGORY_ID = 'info_category_id'
    RECORD_TIME = 'info_record_time'
    SOURCE = 'info_source'
    IMAGE_URLS = 'image_urls'
    IMAGES = 'images'
    IMAGE_PATHS = 'image_paths'
