BOT_NAME = 'fangtianxia'

SPIDER_MODULES = ['fangtianxia.spiders']
NEWSPIDER_MODULE = 'fangtianxia.spiders'

ROBOTSTXT_OBEY = False

import random
DOWNLOAD_DELAY = random.uniform(1,2)

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

DOWNLOADER_MIDDLEWARES = {
   'fangtianxia.middlewares.UseragentDownloadMiddleware': 543,
   # 'fangtianxia.middlewares.IpProxyDownloadMiddleware': 542,
}

# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'fangtianxia.pipelines.FangtianxiaPipeline': 300,
}

#scrapy_redis相关配置
#确保request存储到redis中
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#确保所有爬虫共享相同的去重指纹
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#设置redis为item_pipeline
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline':300
# }

#在redis中保持scrapy_redis用到的队列，不会清理redis中的队列，从而可以实现暂停和恢复的功能
SCHEDULER_PERSIST = True

#设置连接redis信息
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379