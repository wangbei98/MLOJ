import os
import sys
import json
import time
import click
from flask import Flask, request, abort
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource, fields, marshal_with, marshal_with_field, reqparse
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import UserTable, HomeworkTable, UserHomeworkTable
from extensions import db, login_manager
from settings import config
# 获取配置文件中定义的资源目录
RESOURCES_FOLDER = config['RESOURCES_FOLDER']

'''
资源操作相关API
'''

# /api/courseware?cwid=xxx


class CoursewareAPI(Resource):
    courseware_fields = {
        'cwid': fields.Integer,
        'course_name': fields.String
    }

    @marshal_with(courseware_fields)
    def serialize_courseware(self, courseware):
        return courseware

    # 下载课件
    def get(self):
        pass
    # 上传课件

    def post(self):
        pass

    def delete(self):
        pass

# /app_template_filter()

# /api/homeworks
class HomeworksAPI(Resource):
    homework_fields = {
        'hid': fields.Integer,
        'htype': fields.Integer,
        'homeworkname': fields.String,
        'homework_desc': fields.String,
        'homework_begin_time': fields.Integer,
        'files': fields.List(fields.Nested({
            'hid': fields.Integer,
            'htype': fields.Integer,
            'homeworkname': fields.String,
            'homework_desc': fields.String,
            'homework_begin_time': fields.Integer
        }))
    }

    @marshal_with(homework_fields)
    def serialize_homework(self, homework):
        return homework
    # 获取所有作业信息

    def get(self):
        pass
    # 新建课程

    def post(self):
        # 新建解释器对象，用来获取request中的对象
        parse = reqparse.RequestParser()
        # 检查request中的htype，如果为int，则加入到parse对象中，如果不为int，返回‘错误的htype’
        parse.add_argument('type', type=int, help='错误的htype', default='1')
        # 检查request中的homeworkname，str类型不为空
        parse.add_argument(
            "homeworkname", type=str, required=True, help='homeworkname cannot be blank!')
        # 检查request中的desc，str类型不为空
        parse.add_argument(
            "desc", type=str, required=True, help='homework_desc cannot be blank!')
        # 将parse对象中的参数读取到args中
        args = parse.parse_args()
        # new
        homework = HomeworkTable(htype=args.get('type'),homeworkname=args.get('homeworkname'),
                                 homework_desc=args.get('desc'),homework_begin_time = int(time.time()))

        try:
            db.session.add(homework)
            db.session.commit()
        except:
            # 如果插入失败，则返回错误
            return jsonify(code=27, message='insert fail')

        return jsonify(code=0, message="OK", data={'homework':  self.serialize_homework(homework)})

# /api/homework?hid=xxx


class HomeworkAPI(Resource):
    homework_fields = {
        'hid': fields.Integer,
        'htype': fields.Integer,
        'homeworkname': fields.String,
        'homework_desc': fields.String,
        'homework_begin_time': fields.Integer,
        'files': fields.List(fields.Nested({
            'hid': fields.Integer,
            'htype': fields.Integer,
            'homeworkname': fields.String,
            'homework_desc': fields.String,
            'homework_begin_time': fields.Integer
        }))
    }

    @marshal_with(homework_fields)
    def serialize_homework(self, homework):
        return homework

    # 获取某作业
    def get(self):
        pass
    # 修改某作业

    def put(self):
        pass
    # 删除某作业

    def delete(self):
        pass

# /api/homework/datasets?hid=xxx&type=xxx


class DatasetAPI(Resource):
    file_fields = {
        'fid': fields.Integer,
        'hid': fields.Integer,
        'ftype': fields.String,
        'filename': fields.String
    }

    @marshal_with(file_fields)
    def serialize_file(self, file):
        return file

    def get(self):
        # TODO ：验证用户身份，不允许学生下载 standard 文件
        pass

    def post(self):
        pass

    def delete(self):
        pass

# /api/user/course/homework?uid=xxx&hid=xxx
# 学生提交的作业


class StudentHomeworkAPI(Resource):
    user_homework_fields = {
        'hid': fields.Integer,
        'uid': fields.Integer,
        'score': fields.Integer,
        'is_finished': fields.Integer,
        'submit_file_name': fields.String,
        'submit_time': fields.Integer
    }

    @marshal_with(user_homework_fields)
    def serialize_file(self, user_homework):
        return user_homework
    # 获取某学生的某作业

    def get(self):
        pass
    # 某学生上传某作业

    def post(self):
        pass

# /api/homework/score?uid=xxx&hid=xxx


class ScoreAPI(Resource):
    user_homework_fields = {
        'hid': fields.Integer,
        'uid': fields.Integer,
        'score': fields.Integer,
        'is_finished': fields.Integer,
        'submit_file_name': fields.String,
        'submit_time': fields.Integer
    }

    @marshal_with(user_homework_fields)
    def serialize_file(self, user_homework):
        return user_homework
    # get某学生的某作业的分数

    def get(self):
        pass
    # 打分

    def post(self):
        pass


# util 辅助函数

# 为file生成文件名
import hashlib


def generate_file_name(fid, hid):
    return hashlib.md5(
        (str(fid) + '_' + str(hid)).encode('utf-8')).hexdigest()

# 为submit生成文件名
import hashlib


def generate_file_name(hid, uid):
    return hashlib.md5(
        (str(hid) + '_' + str(uid)).encode('utf-8')).hexdigest()
