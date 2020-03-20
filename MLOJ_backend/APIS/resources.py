import os
import sys
import json
import time
import click
from flask import Flask,request,abort
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api,Resource,fields,marshal_with,marshal_with_field,reqparse
from flask_login import LoginManager,UserMixin,login_user, logout_user, current_user, login_required
from models import UserTable,CourseTable,HomeworkTable,UserHomeworkTable
from extensions import db,login_manager
from settings import config
# 获取配置文件中定义的资源目录
RESOURCES_FOLDER = config['RESOURCES_FOLDER']

'''
资源操作相关API
'''

# /api/courses
class CourcesAPI(Resource):
	# 获取所有课程信息
	def get(self):
		pass
	# 新建一个课程
	def post(self):
		pass


# /api/course?cid=xxx
class CourseAPI(Resource):

	# 获取某课程
	def get(self):
		pass
	# 修改某课程
	def put(self):
		pass
	# 删除某课程
	def delete(self):
		pass

# /api/courseware?cid=xxx
class CoursewareAPI(Resource):
	# 下载课件
	def get(self):
		pass
	# 上传课件
	def post(self):
		pass

	def delete(self):
		pass
# /api/course/homeworks?cid=xxx
class HomeworksAPI(Resource):
	# 获取所有作业信息
	def get(self):
		pass
	# 新建课程
	def post(self):
		pass

# /api/course/homework?hid=xxx
class HomeworkAPI(Resource):

	# 获取某作业
	def get(self):
		pass
	# 修改某作业
	def put(self):
		pass
	# 删除某作业
	def delete(self):
		pass

# /api/course/homework/datasets?hid=xxx
class DatasetAPI(Resource):

	def get(self):
		pass

	def post(self):
		pass

	def delete(self):
		pass
# /api/user/course/homework?uid=xxx&hid=xxx
# 学生提交的作业
class StudentHomeworkAPI(Resource):
	# 获取某学生的某作业
	def get(self):
		pass
	# 某学生上传某作业
	def post(self):
		pass
# /api/course/homework/score?uid=xxx&hid=xxx
class ScoreAPI(Resource):
	# get某学生的某作业的分数
	def get(self):
		pass
	# 打分
	def post(self):
		pass



