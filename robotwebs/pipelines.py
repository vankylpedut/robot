# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from robotwebs.items import RobotItemManager


class robotImgDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        open("image_urls.txt", "a").write(request.url + "\n")
        image_guid = request.url.split('/')[-1]
        # times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # image_guid = times + guid
        return 'full/%s' % (image_guid)


# 将数据存储到mysql数据库
from twisted.enterprise import adbapi
import pymysql


class MySQLStorePipeline(object):
    # 数据库参数
    def __init__(self):
        dbargs = dict(
            host='127.0.0.1',
            db='robot',
            user='root',
            passwd='123456',
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8',
            use_unicode=True
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    '''
    The default pipeline invoke function
    '''

    def process_item(self, item, spider):
        # res = self.dbpool.runInteraction(self.insert_into_information, item)
        # res = self.dbpool.runInteraction(self.insert_into_infocontent, item)
        res = self.dbpool.runInteraction(self.insert_into_first_page, item)
        return item

    # 插入的表，此表需要事先建好
    def insert_into_information(self, conn, item):
        url = item[RobotItemManager.LINK]
        title = item[RobotItemManager.TITLE]
        summary = item[RobotItemManager.SUMMARY]
        time = item[RobotItemManager.RELEASE_TIME]
        conn.execute(
            'insert into information(info_link, info_title, info_summary, info_release_time) values(%s,%s,%s,%s)',
            (url, title, summary, time)
        )

    def insert_into_infocontent(self, conn, item):
        conn.execute('select info_id from information where info_link = %s', item[RobotItemManager.LINK])
        result = (conn.fetchone())
        info_id = int(result["info_id"])
        content = item[RobotItemManager.CONTENT]
        content = content[0]
        conn.execute('insert into infocontent(info_id, info_main) values(%s, %s)', (info_id, content))
        # conn.execute('insert into infocontent(info_id, info_main) values(%s)', (info_id))
        pass

    def insert_into_first_page(self, conn, item):
        url = item[RobotItemManager.LINK]
        title = item[RobotItemManager.TITLE]
        summary = item[RobotItemManager.SUMMARY]
        time = item[RobotItemManager.RECORD_TIME]
        conn.execute(
            'insert into information(info_link, info_title, info_summary, info_release_time) values(%s,%s,%s,%s)',
            (url, title, summary, time)
        )

        conn.execute('select info_id from information where info_link = %s', item[RobotItemManager.LINK])
        result = (conn.fetchone())
        info_id = int(result["info_id"])
        content = item[RobotItemManager.CONTENT]
        content = content[0]
        conn.execute('insert into infocontent(info_id, info_main) values(%s, %s)', (info_id, content))
