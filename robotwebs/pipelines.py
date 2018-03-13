# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline



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

#将数据存储到mysql数据库
from twisted.enterprise import adbapi
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


class MySQLStorePipeline(object):
    #数据库参数
    def __init__(self):
        dbargs = dict(
             host = '127.0.0.1',
             db = 'robot',
             user = 'root',
             passwd = '123456',
             cursorclass = MySQLdb.cursors.DictCursor,
             charset = 'utf8',
             use_unicode = True
            )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)


    '''
    The default pipeline invoke function
    '''
    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table, item)
        # title = item['title']
        # item['title'] = set(title)
        # time = item['time']
        # item['time'] = set(time)
        return item
    #插入的表，此表需要事先建好
    def insert_into_table(self,conn,item):

        # conn.execute('insert into infocontent(infoId,infomain,InfoPage) values((select max(infoId) from infomation),%s,%s');
        conn.execute('insert into information(InfoTitle, InfoSummary,InfoRecordTime) values(%s,%s,%s)', (
            item['title'],
            item['simple'],
            item['time'])
            )

