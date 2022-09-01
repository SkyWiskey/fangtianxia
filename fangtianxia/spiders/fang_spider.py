import scrapy
import re

from ..items import NewhouseItem,EsfItem
from scrapy_redis.spiders import RedisSpider


class FangSpiderSpider(RedisSpider):
    name = 'fang_spider'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fangtianxia:start_urls"

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub('\s','',province_text)
            #如果这一行有省份名称，则属于一个新的省份，如果没有，则还是属于上一个省份的城市
            if province_text:
                province = province_text
            #不爬取海外城市
            if province_text == "其它":
                continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city_name = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                # 构建新房的连接
                scheme = city_url.split('//')[0]
                domain = city_url.split('//')[1]
                #北京是个例外 需要单独判断
                if city_name == "北京":
                    newhouse_url = 'http://newhouse.fang.com/house/s/'
                    esf_url = 'http://esf1.fang.com/default.aspx'
                else:
                    newhouse_url = scheme + '//' + 'newhouse.' + domain +'house/s/'
                    # 构架二手房连接
                    esf_url = scheme + '//' +'esf.' + domain

                # 请求每个城市新房的连接 进行信息提取
                yield scrapy.Request(url = newhouse_url,callback=self.parse_newhouse,
                                     meta={'info':(province,city_name)}) #meta可以传递参数
                # 请求每个城市二手房的连接 进行信息提取
                yield scrapy.Request(url = esf_url,callback=self.parse_esf,
                                     meta={'info':(province,city_name)})

    #解析新房房源信息
    def parse_newhouse(self,response):
        province,city_name = response.meta.get('info')
        houses = response.xpath("//div[@class='nl_con clearfix']/ul/li[not(@style)]")
        for house in houses:
            #小区名
            name = house.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            #价格
            price_text = ''.join(house.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r'\s|广告','',price_text)
            #几居室
            rooms = house.xpath(".//div[@class='house_type clearfix']/a/text()").getall()
            rooms = list(filter(lambda x:x.endswith("居"),rooms))
            #面积
            area_text = house.xpath(".//div[@class='house_type clearfix']/text()[last()]").get().strip()
            area = area_text.replace('—','')
            #地址
            address = house.xpath(".//div[@class='address']/a/@title").get().strip()
            #行政区
            district_text = ''.join(house.xpath(".//div[@class='address']/a//text()").getall())
            district = re.search('.*\[(.+)\].*',district_text).group(1)
            #是否在售
            sale = house.xpath(".//div[@class='fangyuan']/span/text()").get().strip()
            #详情url
            origin_url = house.xpath(".//div[@class='nlcd_name']/a/@href").get().strip()
            item = NewhouseItem(province = province,city_name = city_name,name = name,
                                price = price,district = district,sale = sale,rooms = rooms,
                                area = area,address = address,origin_url = origin_url)
            yield item

        #获取翻页
        next_url = response.xpath("//a[@class='next'][last()]/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,
                                 meta={'info':(province,city_name)})

    #解析二手房房源信息
    def parse_esf(self,response):
        province,city_name = response.meta.get('info')
        item = EsfItem(province = province,city_name = city_name)
        houses = response.xpath("//dl[@class='clearfix'][not(@data-bgcomare)]")
        for house in houses:
            #小区名
            name = house.xpath(".//p[@class='add_shop']/a/@title").get().strip()
            item['name'] = name
            #总价
            price_text = ''.join(house.xpath(".//dd[@class='price_right']/span[@class='red']//text()").getall())
            price = re.sub(r'\s','',price_text)
            item['price'] = price
            #单价
            unit = house.xpath(".//dd[@class='price_right']/span[2]/text()").get().strip()
            item['unit'] = unit
            #几室几厅 面积 楼层 朝向 年份
            infos_text = house.xpath(".//p[@class='tel_shop']//text()").getall()
            infos = list(map(lambda x:re.sub(r'\s','',x),infos_text))
            for info in infos:
                if '室' in info:
                    item['rooms'] = info
                elif '㎡' in info:
                    item['area'] = info
                elif '层' or '栋' in info:
                    item['floor'] = info
                elif '向' in info:
                    item['toward'] = info
                elif "年建" in info:
                    item['year'] = info
            #地址
            address = house.xpath(".//p[@class='add_shop']/span/text()").get()
            item['address'] = address
            #详情url
            origin_url = house.xpath("h4[@class='clearfix']/a/@href").get()
            item['origin_url'] = response.urljoin(origin_url)

            yield item
        #获取翻页
        next_url = response.xpath("//div[@class='page_al']/p[position() < last()][last()]/a/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_esf,
                                 meta={'info':(province,city_name)})



