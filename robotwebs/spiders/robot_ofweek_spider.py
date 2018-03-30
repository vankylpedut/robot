import datetime
import re

import scrapy
from scrapy import Selector, Request

from robotwebs.items import RobotOfWeekItem
from robotwebs.settings import IMAGES_STORE
from robotwebs.tool.variable_settings import VariableSettings


class RobotContentSpider(scrapy.Spider):
    name = 'robot'
    allowed_domains = ['robot.ofweek.com']
    bash_url = 'http://robot.ofweek.com/'
    start_urls = ['http://robot.ofweek.com/CATList-8321200-8100-robot.html']
    # # 爬取后面页数的新闻链接
    # pages = []
    start_url = 'http://robot.ofweek.com/CATList-8321200-8100-robot.html'

    def parse(self, response):
        yield Request(url=self.start_url, callback=self.parse_listInfo)

    # 文章列表爬取
    def parse_listInfo(self, response):
        is_request_flag = False  # 下一页是否已经放入待爬列表
        tolerance_value = 2  # 容忍值
        print('文章清单')
        # sel : 页面源代码
        sel = Selector(response)
        articles = sel.xpath(
            '//div [@class="list_model"]//div [contains(@class, "model_right")]')
        for article in articles:
            is_exist = True  # 是否已存在
            is_next_page = False  # 是否爬取下一页
            is_under_deadline = False  # 是否在限期下面,若在，停止循环
            # 解析获取时间
            time = self.parse_info_record_time(article)
            is_exist, is_next_page, is_under_deadline = self.is_time_exist(time)
            # 通过时间判断该文章是否已存进数据库
            if is_exist is not True:
                item = RobotOfWeekItem()
                # url
                url = article.xpath('h3//a/@href').extract_first("")
                item[RobotOfWeekItem.LINK] = url
                print(url)
                # 概述
                item[RobotOfWeekItem.SUMMARY] = article.xpath('p/span/text()').extract_first("")
                # 发布时间
                item[RobotOfWeekItem.RELEASE_TIME] = time
                yield Request(url=url, meta={"item": item}, callback=self.parse_articleInfo)
            if is_next_page and is_request_flag is not True:
                next_page = self.bash_url + (sel.xpath("//div [@class='page']//a[last()]/@href").extract())[0]
                yield Request(url=next_page, callback=self.parse_listInfo)
                is_request_flag = True
            if is_under_deadline:
                tolerance_value -= 1
                if tolerance_value < 0:
                    break

    # 文章页面爬取
    def parse_articleInfo(self, response):
        sel = Selector(response)
        item = response.meta["item"]
        # 标题
        title = sel.xpath('//div [@class="article_left"]/h1/text()').extract()
        item[RobotOfWeekItem.TITLE] = title[0]
        # 导读
        item[RobotOfWeekItem.READING_GUIDANCE] = sel.xpath('//div [@class="simple"]/p').xpath('string(.)').extract()
        # 提取页码
        page_url = response.url
        page = []
        page.append(page_url)
        if page[0][-7] == '_':
            page[0] = int(page[0][-6])
            item['judge'] = 0
        else:
            page[0] = 1
            item['judge'] = 1
        item[RobotOfWeekItem.PAGE] = page

        # 爬取时间
        self.parse_info_record_time2(item, sel)

        # 爬取文章内容
        self.parse_article_cotent(item, sel)

        # 判断正文是否有下一页
        next_page = sel.xpath('//span [@id="nextPage"]/a/@href').extract_first()
        next_page = response.urljoin(next_page)

        if next_page:
            yield Request(url=next_page, meta={"item": item}, callback=self.parse_articleInfo)
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

    # 爬取文章内容
    def parse_article_cotent(self, item, sel):
        item[RobotOfWeekItem.CONTENT] = sel.xpath('//div [@id="articleC"]').extract()
        list_imgs = sel.xpath('//div [@id="articleC"]//img/@src').extract()
        if len(list_imgs) > 0:
            item['image_urls'] = list_imgs
        else:
            item['image_urls'] = []
        for i in range(len(list_imgs)):
            # image_guid为图片文件名称
            image_guid = list_imgs[i].split('/')[-1]
            # image_guid = times + guid
            # image_guid_path为图片文件地址
            image_guid_path = IMAGES_STORE + '/full/' + image_guid
            if list_imgs[i] in item[RobotOfWeekItem.CONTENT][0]:
                item[RobotOfWeekItem.CONTENT][0] = item[RobotOfWeekItem.CONTENT][0].replace(list_imgs[i],
                                                                                            image_guid_path)  # 第二个参数修改为本地地址

    # 爬取二级界面时间
    def parse_info_record_time2(self, item, sel):
        date_str = sel.xpath('//span [@class="sdate"]/text()').extract()
        date_str[0] = date_str[0].replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '')
        time = datetime.datetime.strptime(date_str[0], "%Y-%m-%d %H:%M")
        time = time.strftime("%Y-%m-%d %H:%M")
        # print(time)
        type(time)
        item[RobotOfWeekItem.RELEASE_TIME] = time

    # 爬取一级界面时间
    def parse_info_record_time(self, sel):
        date_str = sel.xpath('div [@class="tag"]//span [@class="date"]/text()').extract()
        matchObj = re.search('\d+-\d+-\d+ \d+:\d+', date_str[len(date_str) - 1])
        strtime = matchObj.group()
        time = datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M")
        return time

    # 判断文章是否以爬取
    def is_time_exist(self, time):
        '''
        通过文章的发布时间判断是否已经存在于数据库
        :param time:
        :return:
        '''
        is_exist = True  # 是否已存在
        is_next_page = False  # 是否爬取下一页
        is_under_deadline = False  # 是否在限期下面
        if VariableSettings.DEADLINE_TIME > time:
            is_under_deadline = True
        elif VariableSettings.TIME_LIST.__contains__(time):
            is_next_page = True
        else:
            is_exist = False
            is_next_page = True
        return is_exist, is_next_page, is_under_deadline
