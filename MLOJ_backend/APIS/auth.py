import os
import sys
import json
import time
import click
from flask import Flask, request, abort
from flask import jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource, fields, marshal_with, marshal_with_field, reqparse
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import UserTable, HomeworkTable, UserHomeworkTable
from extensions import db, login_manager
from utils import admin_required

'''
用户登录相关API
'''


# 定义API类
class Login(Resource):
    def post(self):
        if current_user.is_authenticated:
            # TODO
            response = make_response(jsonify(code=32,message = 'already authenticated'))
            return response
        parse = reqparse.RequestParser()
        parse.add_argument('uid', type=int, help='用户名验证不通过', default=201000000)
        parse.add_argument('password', type=str, help='密码验证不通过')
        args = parse.parse_args()

        uid = args.get("uid")
        password = args.get("password")
        try:
            user = UserTable.query.get(uid)
        except Exception:
            print("{} User query: {} failure......".format(
                time.strftime("%Y-%m-%d %H:%M:%S"), uid))
            response = make_response(jsonify(code = 31,message = 'user not found'))
            return response
        else:
            print("{} User query: {} success...".format(
                time.strftime("%Y-%m-%d %H:%M:%S"), uid))
        finally:
            db.session.close()
        if user and user.varify_password(password):
            login_user(user)
            print('current_user : ')
            print(current_user)
            response = jsonify(code = 0,message = 'login success',data ={'user': user.to_json()})
            return response
        else:
            print("{} User query: {} failure...".format(
                time.strftime("%Y-%m-%d %H:%M:%S"), uid))
            print('user is None or password False')
            response = make_response(jsonify(code = 33,message = 'login fail'))
            return response


class Register(Resource):

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('uid', type=int, help='用户id验证不通过', default=201000000)
        parse.add_argument('username',type = str,help='用户名验证不通过')
        parse.add_argument('password', type=str, help='密码验证不通过')
        args = parse.parse_args()

        uid = args.get('uid')
        username = args.get('username')
        password = args.get('password')
        password_hash = generate_password_hash(password)
        try:
            user = UserTable(uid=uid, password_hash=password_hash,username=username)
            db.session.add(user)
            db.session.commit()
        except:
            print("{} User add: {} failure...".format(
                time.strftime("%Y-%m-%d %H:%M:%S"), uid))
            db.session.rollback()
            response = make_response(jsonify(code=34,message = 'user add fail'))
            return response
        else:
            print("{} User add: {} success...".format(
                time.strftime("%Y-%m-%d %H:%M:%S"), uid))
            response = make_response(jsonify(code = 0, message = 'user add success' , data ={'user': user.to_json()}))
            return response
        finally:
            db.session.close()

class GetCurUserAPI(Resource):
    @login_required
    def get(self):
        if current_user.is_authenticated:
            response = make_response(jsonify(code = 0,message = 'get current_user success',data ={'user':current_user.to_json()}))
            return response
        else:
            response = make_response(jsonify(code = 35,message = 'get current_user fail'))
            return response
class GetAllUsersAPI(Resource):

    @admin_required
    def get(self):
        try:
            users = UserTable.query.all();
            response = make_response(jsonify(code = 0,message = 'get users success',data ={'users':[user.to_json() for user in users]}))
            return response
        except:
            response = make_response(jsonify(code = 30,message = 'user error'))
            return response

class Logout(Resource):

    @login_required
    def logout(self):
        logout_user()
        return True
    def get(self):
        if self.logout():
            response = make_response(jsonify(code = 0,message = 'logout success'))
            return response
