# -*- coding: utf-8 -*-

# Scrapy settings for robotwebs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from calendar import calendar

import time

BOT_NAME = 'robotwebs'

SPIDER_MODULES = ['robotwebs.spiders']
NEWSPIDER_MODULE = 'robotwebs.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'robotwebs (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'robotwebs.middlewares.RobotwebsSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'robotwebs.middlewares.RobotwebsDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipeline
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy.pipelines.images.ImagesPipeline': 300,
    'robotwebs.pipelines.robotImgDownloadPipeline': 300,
    'robotwebs.pipeline.robot_ofweek_pipeline.RobotOfweekPipeline': 300,
}
# IMAGES_EXPIRES = 90
DOWNLOAD_DELAY = 0.25
# IMAGES_URL_FILED = "image_url"
# start MySQL database configure setting
MYSQL_HOST = 'localhost'
MYSQL_DB = 'robot'
MYSQL_USER = 'root'
# MYSQL_PASSWORD = '123456'
MYSQL_PASSWORD = 'Rdcrdc2016'
MYSQL_PORT = 3306
MYSQL_CHARSET = 'utf-8'
# end of MySQL database configure setting


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# ??????????????????
# LOG_FILE = "log/mySpider" + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) + ".log"
# LOG_LEVEL = "INFO"

# ???????????????????????????????????????????????????????????????
IS_FORCE = True  # ????????????????????????????????????
DEADLINE_IS_TODAY = True  # DEADLINE_TIME ??????????????????
DEADLINE_TIME = '2018-3-29 09:00'  # ???????????????????????????,??????????????????????????????????????????
DATETIME_FORMAT = '%Y-%m-%d %H:%M'  # ????????????

# ????????????
IMAGES_STORE = '/usr/local/img'  # Linux
# IMAGES_STORE = 'E:/img'  # windows
# IMAGES_STORE = 'img'  # ????????????
