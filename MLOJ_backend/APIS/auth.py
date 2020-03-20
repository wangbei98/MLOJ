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


'''
用户登录相关API
'''


# 定义API类
class Login(Resource):
	def post(self):
		if current_user.is_authenticated:
			# TODO
			return jsonify('already authenticated')
		parse = reqparse.RequestParser()
		parse.add_argument('uid',type=int,help='用户名验证不通过',default=201000000)
		parse.add_argument('password',type=str,help='密码验证不通过')
		args = parse.parse_args()

		uid = args.get("uid")
		password = args.get("password")
		try:
			user = UserTable.query.get(uid)
		except Exception:
			print("{} User query: {} failure......".format(time.strftime("%Y-%m-%d %H:%M:%S"),uid))
			return jsonify('user not found')
		else:
			print("{} User query: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), uid))
		finally:
			db.session.close()
		if user and user.varify_password(password):
			login_user(user)
			print('current_user : ')
			print(current_user)
			return jsonify('login success')
		else:
			print('in if')
			print("{} User query: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), uid))
			print('user is None or password False')
			return jsonify('login fail')
		
class Register(Resource):
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument('uid',type=int,help='用户名验证不通过',default=201000000)
		parse.add_argument('password',type=str,help='密码验证不通过')
		args = parse.parse_args()

		uid = args.get('uid')
		password = args.get('password')
		password_hash = generate_password_hash(password)
		try:
			user = UserTable(uid = uid,password_hash =password_hash)
			db.session.add(user)
			db.session.commit()
		except:
			print("{} User add: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), uid))
			db.session.rollback()
			return jsonify('user add fail')
		else:
			print("{} User add: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), uid))
			return jsonify('user add success')
		finally:
			db.session.close()

class Logout(Resource):
	@login_required
	def logout(self):
		print(current_user)
		print("已退出登录")
		logout_user()
		print(current_user.is_authenticated)
		return True
	def get(self):
	    if self.logout():
	    	return jsonify('logout success')
