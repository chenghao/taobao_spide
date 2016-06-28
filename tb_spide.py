# coding:utf-8
__author__ = "chenghao"
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from gevent import monkey

monkey.patch_all()
import gevent
from gevent.pool import Pool
import lxml.etree as etree
from conf import logger
import re, hashlib
from module import *
from selenium import webdriver


class TBSpide():
	def __init__(self):
		self.pool = Pool(1000)

	def import_firefox(self):
		self.browser = webdriver.Firefox()

	def import_chrome(self):
		self.browser = webdriver.Chrome(executable_path="/home/chenghao/script/chromedriver")

	def import_phantomJS(self):
		self.browser = webdriver.PhantomJS(executable_path="/home/chenghao/script/phantomjs")

	def get_url(self):
		urls = [
			"https://s.taobao.com/search?initiative_id=staobaoz_20160625&q=童装女 夏季&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest"
		]
		self.pool.map(self.load_page, urls)
		self.close()

	def load_page(self, url):
		"""
		构建页数
		:param url:
		:return:
		"""
		for i in xrange(10):
			_url = url + "&s=" + str(i * 44)
			print _url
			self.pool.spawn(self.req_url, _url)
			gevent.sleep(25)

	def req_url(self, url):
		"""
		请求url
		:param url:
		:return:
		"""
		try:
			self.browser.get(url)
			content = self.browser.page_source
			self.pool.spawn(self.parse_html, content.decode('utf-8', 'ignore'))
		except Exception, e:
			logger.error("请求url异常: " + str(e), exc_info=True)

	def parse_html(self, content):
		"""
		解析html内容
		:param content:
		:return:
		"""
		if len(content) > 400:
			html = etree.HTML(content)
			items = html.xpath(u'//*[@id="mainsrp-itemlist"]//div[@class="items g-clearfix"]/div')
			self.pool.map(self.get_field, items)

	def get_field(self, item):
		"""
		获取字段
		:param item:
		:return:
		"""
		try:
			div = item.xpath(u'div[@class="pic-box J_MouseEneterLeave J_PicBox"]//*')[0]
			url = div.xpath(u'div[@class="pic"]//a')[0].attrib.get("href")  # url地址
			url = self.is_startswith(url)
			url_md5 = hashlib.md5(url).hexdigest()
			bo = exist_by_urlmd5(url_md5)
			if bo is False:  # 数据库中不存在才新增
				img = div.xpath(u'div[@class="pic"]//img')[0].attrib
				cover = img.get("src") if img.get("src") else img.get("data-src")  # 封面
				cover = self.is_startswith(cover)
				similars = div.xpath(u'div[@class="similars"]//a')
				if similars:
					same_style_url = similars[0].attrib.get("href")  # 同款url
					if same_style_url is None:
						same_style_url = ""
					else:
						same_style_url = "https://s.taobao.com" + same_style_url

					if len(similars) > 1:
						similar_url = similars[1].attrib.get("href")
						if similar_url is None:
							similar_url = ""
						else:
							similar_url = "https://s.taobao.com" + similar_url  # 相似url
					else:
						similar_url = ""
				else:
					same_style_url = ""
					similar_url = ""

				div = item.xpath(u'div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]/div')
				price = div[0].xpath(u'div[@class="price g_price g_price-highlight"]/strong')[0].text  # 商品价格
				sale_num = div[0].xpath(u'div[@class="deal-cnt"]')[0].text
				if sale_num is None:
					sale_num = 0
				else:
					sale_num = "".join([s for s in sale_num if s.isdigit()])  # 商品购买人数
				title_a = etree.tounicode(div[1].xpath(u'a')[0])  # 商品名称
				p = re.compile('<[^>]+>')  # 去掉html标签， 只留字符
				title = p.sub("", title_a).strip()
				shop_name = div[2].xpath(u'div/a/span')[1].text  # 商铺名称
				addr = div[2].xpath(u'div')[1].text  # 商铺地址
				tianmao = div[3].xpath(u'div/ul/li//span[@class="icon-service-tianmao"]')
				is_tmall = 1 if tianmao else 0  # 是否天猫商店

				data = {"url": url, "title": title, "cover": cover, "price": price, "sale_num": sale_num,
				        "shop_name": shop_name, "addr": addr, "is_tmall": is_tmall, "url_md5": url_md5,
				        "same_style_url": same_style_url, "similar_url": similar_url}
				self.pool.spawn(self.save, data)
		except Exception, e:
			logger.error("获取字段异常: " + str(e), exc_info=True)

	def save(self, data):
		"""
		保存数据库
		:param data:
		:return:
		"""
		try:
			save_tb(data)
		except Exception, e:
			logger.error("保存到数据库异常: " + str(e), exc_info=True)

	def is_startswith(self, s):
		if s.startswith("http") is False:
			return "https:" + s;
		else:
			return s

	def close(self):
		self.browser.quit()


if __name__ == "__main__":
	import time
	s = time.time()
	tb = TBSpide()
	#tb.import_firefox()
	#tb.import_chrome()
	tb.import_phantomJS()
	tb.get_url()
	e = time.time()
	print e - s