import os

# 一些全局的配置信息


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

config={
	'RESOURCES_FOLDER':os.path.join(basedir,'backend/resources')
}