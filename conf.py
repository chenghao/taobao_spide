# coding:utf-8
__author__ = "chenghao"

import logging
import logging.handlers

# mysql配置
mysql_conf = {
	"db": "tb",
	"user": "root",
	"passwd": "123456",
	"host": "localhost",
	"port": 3306
}


def get_logger():
	# 按每天生成日志文件 linux (win是存放在该项目的所在盘下)
	logHandler = logging.handlers.TimedRotatingFileHandler("logs/tb_log", "D", 1)
	# 格式化日志内容
	logFormatter = logging.Formatter('%(asctime)s %(name)-5s %(levelname)-5s %(message)s')
	logHandler.setFormatter(logFormatter)
	# 设置记录器名字
	logger = logging.getLogger('tb_log')
	logger.addHandler(logHandler)
	# 设置日志等级
	logger.setLevel(logging.DEBUG)


logger = get_logger()
