import re

import datetime
import scrapy
from scrapy import Selector, Request


from robotwebs.items import RobotcontentItem
from robotwebs.settings import IMAGES_STORE


class RobotContentSpider(scrapy.Spider):
    name = 'robot'
    allowed_domains = ['robot.ofweek.com']
    start_urls = ['http://robot.ofweek.com/CATList-8321200-8100-robot.html']
    # pages = []
    # start_url = 'http://robot.ofweek.com/CATList-8321200-8100-robot.html'
    # pages.append(start_url)
    # for i in range(2, 3):
    #     newspage = "http://robot.ofweek.com/CATList-8321200-8100-robot-%s.html" % i
    #     pages.append(newspage)
    # start_urls = pages

    def parse(self, response):
        # sel : 页面源代码
        sel = Selector(response)

        articles = sel.xpath('//div [@class="list_model"]//h3')
        for eacharticle in articles:
            articleUrl = eacharticle.xpath('a/@href').extract_first("")
            # print(articleUrl)
            yield Request(url=articleUrl, callback=self.parse_articleInfo)

    def parse_articleInfo(self, response):
        sel = Selector(response)
        item = RobotcontentItem()
        item['title'] = sel.xpath('//div [@class="article_left"]/h1/text()').extract()
        item['simple'] = sel.xpath('//div [@class="simple"]/p').xpath('string(.)').extract()
        #提取页码
        page_url = response.url
        page = []
        page.append(page_url)
        if page[0][-7] == '_':
            page[0] = int(page[0][-6])
            item['judge'] = 0
        else:
            page[0] = 1
            item['judge'] = 1
        item['page'] = page

        #爬取时间
        date_str = sel.xpath('//span [@class="sdate"]/text()').extract()
        date_str[0] = date_str[0].replace('\r', '').replace('\n', '').replace('\t', '').replace('  ','')
        time = datetime.datetime.strptime(date_str[0], "%Y-%m-%d %H:%M")
        time = time.strftime("%Y-%m-%d %H:%M")
        # print(time)
        type(time)
        item['time'] = time

        #爬去文章内容
        item['content'] = sel.xpath('//div [@id="articleC"]').extract()
        list_imgs = sel.xpath('//div [@id="articleC"]//img/@src').extract()
        if len(list_imgs) > 0:
            item['image_urls'] = list_imgs
        else:
            item['image_urls'] = []
        for i in range(len(list_imgs)):
            #image_guid为图片文件名称
            image_guid = list_imgs[i].split('/')[-1]
            # image_guid = times + guid
            #image_guid_path为图片文件地址
            image_guid_path = IMAGES_STORE+'/full/'+image_guid
            if list_imgs[i] in item['content'][0]:
                item['content'][0] = item['content'][0].replace(list_imgs[i], image_guid_path)#第二个参数修改为本地地址


        next_page = sel.xpath('//span [@id="nextPage"]/a/@href').extract_first()
        next_page = response.urljoin(next_page)

        if next_page:
            yield Request(next_page, callback=self.parse_articleInfo)
        yield item


        # item = RobotcontentItem()
        # item['url'] = sel.xpath(urlSetting.URL_XPATH).extract()
        # item['title'] = sel.xpath(TITLE_XPATH).extract()
        # item['url'] = sel.xpath(URL_XPATH).extract()
        # item['abstract'] = sel.xpath(ABSTRACT_XPATH).extract()
        # item['image_urls'] = response.xpath('//img/@src').extract()
        # 抓取图片不成功是因为有的图片url没有http前缀，无法解析
        # yield item
        # yield scrapy.Request(url=item['url'], callback=self.parse)
        # for i in range(len(item['url'])):
        #     yield scrapy.Request(url=item['url'][i], callback=self.parse)
