# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from robotwebs import settings
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

host = settings.MYSQL_HOST
user = settings.MYSQL_USER
psd = settings.MYSQL_PASSWORD
db = settings.MYSQL_DB
port = 3306
use_unicode = True
charset = settings.MYSQL_CHARSET


class MySQLStorePipeline(object):

    @staticmethod
    def get_connection():
        return pymysql.connect(host=host, user=user, passwd=psd, db=db, port=port, use_unicode=True, charset="utf8")

    '''
    The default pipeline invoke function
    '''
    def process_item(self, item, spider):
        conn = MySQLStorePipeline.get_connection()
        self.insert_into_information(conn, item)
        self.insert_into_infocontent(conn, item)
        conn.close()
        return item

    # 插入的表，此表需要事先建好
    def insert_into_information(self, conn, item):
        url = item[RobotItemManager.LINK]
        title = item[RobotItemManager.TITLE]
        summary = item[RobotItemManager.SUMMARY]
        time = item[RobotItemManager.RECORD_TIME]
        cursor = conn.cursor()
        cursor.execute(
            'insert into information(info_link, info_title, info_summary, info_release_time) values(%s,%s,%s,%s)',
            (url, title, summary, time)
        )
        conn.commit()

    def insert_into_infocontent(self, conn, item):
        cursor = conn.cursor()
        cursor.execute('select info_id from information where info_link = %s', item[RobotItemManager.LINK])
        result = (cursor.fetchone())
        info_id = int(result[0])
        content = item[RobotItemManager.CONTENT]
        content = content[0]
        cursor.execute('insert into infocontent(info_id, info_main) values(%s, %s)', (info_id, content))
        # conn.execute('insert into infocontent(info_id, info_main) values(%s)', (info_id))
        conn.commit()
        pass
