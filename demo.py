#1、网页分析

# 全部城市的连接
# https://www.fang.com/SoufunFamily.htm

# 所有城市的新房的url连接
#  例：安庆：https://anqing.fang.com/   全部房
#     安庆：https://anqing.newhouse.fang.com/house/s/ 新房

#所有城市的二手房的url连接
#  例：安庆：https://anqing.fang.com/   全部房
#     安庆：https://anqing.esf.fang.com/ 二手房

#北京市是个例外
# 北京新房连接：http://newhouse.fang.com/house/s/
# 而精二手房连接： http://esf.fang.com/

# 2、准备
# settings.py文件  机器人协议 默认请求头
# middlewares.py文件中 编写随即请求头 以及 ip代理 并在settings.py中打开Download_Middleware

# 3、代码设计
# 首先获取到所有省份以及城市的名称和url
# 然后构建所有城市的新房以及二手房的url
# 然后分别 yield scrapy.Request(url = newhouse_url/esf_url,callback = '')

# 然后定义items
# 然后根据items分别对新房和二手房进行页面分析以及数据提取

#然后将所有item yield到pipeline中

#然后获取下一页的url

# 然后yield scrapy.Request(url = response.urljoin(next_url),callback='',meta='')

#然后编写pipeline 并在settings.py文件中打开pipeline