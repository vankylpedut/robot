# -*- coding: utf-8 -*-

# Define your item pipeline here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from robotwebs.items import RobotOfWeekItem


class robotImgDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item[RobotOfWeekItem.IMAGE_URLS]:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        open("img\image_urls.txt", "a").write(request.url + "\n")
        image_guid = request.url.split('/')[-1]
        return 'robot/%s' % image_guid
