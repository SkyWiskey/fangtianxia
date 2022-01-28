# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewhouseItem(scrapy.Item):
    #省份
    province = scrapy.Field()
    #城市
    city_name = scrapy.Field()
    #小区名
    name = scrapy.Field()
    #价格
    price = scrapy.Field()
    #几居 是个列表
    rooms = scrapy.Field()
    #面积
    area = scrapy.Field()
    #地址
    address = scrapy.Field()
    #行政区
    district = scrapy.Field()
    #是否在售
    sale = scrapy.Field()
    #详情url
    origin_url = scrapy.Field()


class EsfItem(scrapy.Item):
    #省份
    province = scrapy.Field()
    #城市
    city_name = scrapy.Field()
    #小区
    name = scrapy.Field()
    #总价
    price = scrapy.Field()
    #单价
    unit = scrapy.Field()
    #几室几厅
    rooms = scrapy.Field()
    #面积
    area = scrapy.Field()
    #楼层
    floor = scrapy.Field()
    #朝向
    toward = scrapy.Field()
    #建筑年份
    year = scrapy.Field()
    #地址
    address = scrapy.Field()
    #详情url
    origin_url = scrapy.Field()
