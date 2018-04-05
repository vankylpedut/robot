import datetime
import time
import re

import scrapy
from scrapy import Selector, Request

from robotwebs import Category
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

    # 启动方法
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
            date = self.parse_info_record_time(article)
            is_exist, is_next_page, is_under_deadline = self.is_time_exist(date)
            # 通过时间判断该文章是否已存进数据库
            if is_exist is not True:  # 判断文章是否已经爬取过
                item = RobotOfWeekItem()
                # url
                url = self.parse_url(article, item)
                # 分类
                self.parse_category(article, item)
                # 概述
                self.parse_summary(article, item)
                # 发布时间
                item[RobotOfWeekItem.RELEASE_TIME] = time
                yield Request(url=url, meta={"item": item}, callback=self.parse_articleInfo)
            if is_next_page and is_request_flag is not True:  # 判断是否爬取下一页
                next_page = self.bash_url + (sel.xpath("//div [@class='page']//a[last()]/@href").extract())[0]
                yield Request(url=next_page, callback=self.parse_listInfo)
                is_request_flag = True
            if is_under_deadline:  # 判断是否已超出了最低期限，只能容忍两次。
                tolerance_value -= 1
                if tolerance_value < 0:
                    break

    # 文章页面爬取
    def parse_articleInfo(self, response):
        sel = Selector(response)
        item = response.meta["item"]
        # 标题
        self.parse_title(sel, item)
        # 导读
        self.parse_reading_guidance(sel, item)
        # 提取页码
        page_url = response.url
        page = [page_url]
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

        # 记录爬取时间
        item[RobotOfWeekItem.RECORD_TIME] = time.localtime(time.time())

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
    def is_time_exist(self, date):
        '''
        通过文章的发布时间判断是否已经存在于数据库
        :param time:
        :return:
        '''
        is_exist = True  # 是否已存在
        is_next_page = False  # 是否爬取下一页
        is_under_deadline = False  # 是否在限期下面
        deadline_time = VariableSettings.DEADLINE_TIME
        if deadline_time > date:
            is_under_deadline = True
        elif VariableSettings.TIME_LIST.__contains__(date):
            is_next_page = True
        else:
            is_exist = False
            is_next_page = True
        return is_exist, is_next_page, is_under_deadline

    # 爬取url
    def parse_url(self, article, item):
        url = article.xpath('h3//a/@href').extract_first("")
        item[RobotOfWeekItem.LINK] = url
        print(url)
        return url

    # 爬取分类
    def parse_category(self, html, item):
        category_name = html.xpath(
            'div [@class="tag"]//span [@class="date"]/a/text()').extract_first("").strip()
        item[RobotOfWeekItem.CATEGORY_NAME] = category_name
        category_dict = VariableSettings.CATEGORY_DICT
        category_id = category_dict.get(category_name)
        if category_id is None:
            category_id = Category.update(category_name)
        item[RobotOfWeekItem.CATEGORY_ID] = category_id
        return category_name

    # 概述
    def parse_summary(self, html, item):
        summary = html.xpath('p/span/text()').extract_first("")
        item[RobotOfWeekItem.SUMMARY] = summary
        return summary

    # 标题
    def parse_title(self, html, item):
        title = html.xpath('//div [@class="article_left"]/h1/text()').extract_first()
        item[RobotOfWeekItem.TITLE] = title
        return title

    # 导读
    def parse_reading_guidance(self, html, item):
        guidance = html.xpath('//div [@class="simple"]/p').xpath('string(.)').extract()
        item[RobotOfWeekItem.READING_GUIDANCE] = guidance
        return guidance
