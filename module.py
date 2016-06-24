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


class GoodsModel(BaseModel):
	url = CharField(unique=True)  # 商品url
	title = CharField()  # 商品标题
	cover = CharField()  # 商品封面
	price = FloatField()  # 商品价格
	sale_num = IntegerField()  # 卖出人数
	shop_name = CharField(max_length=50)  # 商铺名称
	addr = CharField()  # 地址
	is_tmall = IntegerField()  # 是不是天猫
	same_style_url = CharField()  # 同款url
	similar_url = CharField()  # 相似url
	type = CharField()  # 商品类型
	url_md5 = CharField(32)

	class Meta:
		db_table = "goods"


