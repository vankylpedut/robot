from scrapy.cmdline import execute

# 注意！第二行中代码中的前两个参数是不变的，第三个参数请使用自己的spider的名字。
execute(['scrapy', 'crawl', 'robot'])