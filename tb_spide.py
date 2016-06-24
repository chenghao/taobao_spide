# coding:utf-8
__author__ = "chenghao"
from gevent import monkey

monkey.patch_all()
import gevent
from gevent.pool import Pool
from ghost import Ghost
from lxml.html import fromstring
from conf import logger

pool = Pool(1000)


def main():
	# 童装女 夏季
	urls = [
		"https://s.taobao.com/search?initiative_id=staobaoz_20160623&q=%E7%AB%A5%E8%A3%85%E5%A5%B3+%E5%A4%8F%E5%AD%A3&suggest=0_1&_input_charset=utf-8&wq=%E7%AB%A5%E8%A3%85&suggest_query=%E7%AB%A5%E8%A3%85&source=suggest&bcoffset=-8&ntoffset=-8&p4ppushleft=1%2C48"
	]
	pool.map(build_page, urls)


def build_page(url):
	"""
	构建页数
	:param url:
	:return:
	"""
	for i in xrange(10):
		_url = url + "&s=" + str(i * 44)
		print _url
		pool.spawn(req_url, _url)
		gevent.sleep(10)


def req_url(url):
	"""
	请求url
	:param url:
	:return:
	"""
	try:
		ghost = Ghost()
		with ghost.start() as session:
			page, extra_resources = session.open(url)
			if page.http_status == 200:
				pool.spawn(parse_html, page.content)
	except Exception, e:
		logger.error("请求url异常: " + str(e), exc_info=True)


def parse_html(content):
	"""
	解析html内容
	:param content:
	:return:
	"""
	pass


if __name__ == "__main__":
	main()
