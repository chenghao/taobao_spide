# coding:utf-8
__author__ = "chenghao"
from gevent import monkey

monkey.patch_all()
from peewee import Model, PrimaryKeyField, CharField, FloatField, IntegerField
from playhouse.pool import PooledMySQLDatabase
from conf import mysql_conf

database = PooledMySQLDatabase(mysql_conf["db"], max_connections=500, stale_timeout=300,
                               user=mysql_conf["user"], passwd=mysql_conf["passwd"],
                               host=mysql_conf["host"], port=mysql_conf["port"])


class BaseModel(Model):
	pid = PrimaryKeyField(unique=True)  # 主键

	class Meta:
		database = database


class Goods(BaseModel):
	url = CharField(unique=True, max_length=800)  # 商品url
	title = CharField()  # 商品标题
	cover = CharField(max_length=500)  # 商品封面
	price = FloatField()  # 商品价格
	sale_num = IntegerField()  # 卖出人数
	shop_name = CharField(max_length=50)  # 商铺名称
	addr = CharField()  # 地址
	is_tmall = IntegerField()  # 是不是天猫
	same_style_url = CharField(max_length=500)  # 同款url
	similar_url = CharField(max_length=500)  # 相似url
	url_md5 = CharField(32)

	class Meta:
		db_table = "goods"


def exist_by_urlmd5(url_md5):
	result = Goods.select(Goods.pid).where(Goods.url_md5 == url_md5)
	return result.exists()


def save_tb(data):
	Goods.insert(data).execute()


if __name__ == '__main__':
	print exist_by_urlmd5("123")
