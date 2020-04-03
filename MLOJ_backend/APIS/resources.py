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
from werkzeug.datastructures import FileStorage
from models import CoursewareTable,FileTable
from flask import make_response
from flask import send_file
from utils import admin_required
# 获取配置文件中定义的资源目录
RESOURCES_FOLDER = config['RESOURCES_FOLDER']
COURSEWARES_FOLDER = config['COURSEWARES_FOLDER']

'''
资源操作相关API
'''

# /api/courseware?cwid=xxx
class CoursewareAPI(Resource):
    courseware_fields = {
        'cwid': fields.Integer,
        'courseware_name': fields.String
    }

    @marshal_with(courseware_fields)
    def serialize_courseware(self, courseware):
        return courseware

    # 下载课件
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('cwid',type=int,help='错误的cwid',default='0')
        args = parse.parse_args()
        # 获取当前文件夹id
        file_id = args.get('cwid')
        try:
            file_node = CoursewareTable.query.get(file_id)
        except:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        if file_node is None:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        filename = file_node.courseware_name
        target_file = os.path.join(os.path.expanduser(COURSEWARES_FOLDER), filename)
        if os.path.exists(target_file):

            # print(filename)
            # print(target_file)
            return send_file(target_file,as_attachment=True,attachment_filename=filename,cache_timeout=3600)
            # return send_from_directory(UPLOAD_FOLDER,actual_filename,as_attachment=True)
            # response =  Response(stream_with_context(self.generate(target_file)),content_type='application/octet-stream')
            # response.headers["Content-disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
            # return response
        else:
            response = make_response(jsonify(code='22',message='file not exist'))
            return response
    @admin_required
    def delete(self):
        parse = reqparse.RequestParser()
        parse.add_argument('cwid',type=int,help='错误的cwid',default='0')
        args = parse.parse_args()
        # 获取当前文件夹id
        file_id = args.get('cwid')

        try:
            file_node = CoursewareTable.query.get(file_id)
        except:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        if file_node is None:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        try:
            filename = file_node.courseware_name
            target_file = os.path.join(os.path.expanduser(COURSEWARES_FOLDER), filename)
            # 本地删除
            if os.path.exists(target_file):
                os.remove(target_file)
            # 修改数据库中的文件名
            db.session.delete(file_node)
            db.session.commit()
            response = make_response(jsonify(code = 0,message='OK'))
            return response
        except:
            response = make_response(jsonify(code=20,message='file error'))
            return response

class CoursewaresAPI(Resource):
    courseware_fields = {
        'cwid': fields.Integer,
        'courseware_name': fields.String
    }

    @marshal_with(courseware_fields)
    def serialize_courseware(self, courseware):
        return courseware

    # 上传课件
    @admin_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location='files')
        args = parse.parse_args()

        f = args['file']

        if f:
            filename = f.filename
            if '\"' in filename:
                filename = filename[:-1]
            target_file = os.path.join(os.path.expanduser(COURSEWARES_FOLDER), filename)
            if os.path.exists(target_file):
                response = make_response(jsonify(code=21,message='file already exist, save fail'))
                return response
            try:
                print(target_file)
                # 保存文件
                f.save(target_file)
                print('saved')
                print(filename)
                filenode = CoursewareTable(courseware_name=filename)
                db.session.add(filenode)
                db.session.commit()
                response = make_response(jsonify(code=0,message='OK',data = {'courseware':self.serialize_courseware(filenode)}))
                return response
            except:
                response = make_response(jsonify(code=12,message='node already exist , add fail'))
                return response
    def get(self):
        try:
            # file_nodes = FileNode.query.filter_by(user_id=cur_uid)
            file_nodes = CoursewareTable.query.all()
            response = make_response(jsonify(code = 0,data={'coursewares':[ self.serialize_courseware(file) for file in file_nodes]}))
            return response
        except :
            response = make_response(jsonify(code=10,message='database error'))
            return response

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
        # 获取
        try:
            # 从数据获取全部数据存到list
            homework_li = HomeworkTable.query.all()
        except:
            # 获取失败，返回错误
            return jsonify(code=11, message='query fail')

        if homework_li is None:
            return jsonify(code=11, message='query fail')
        # 返回得到的homework对象，这里的homework是model对象，不可序列化，所以不能直接放入返回的json里面
        # 需要把homework中的各个字段对应放到一个dict里面，这个功能上面封装成了serialize_course函数
        return jsonify(code=0, message='OK', data={'homeworks':  self.serialize_homework(homework_li)})
    # 新建课程
    @admin_required
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
        homework = HomeworkTable(htype=args.get('type'), homeworkname=args.get(
            'homeworkname'), homework_desc=args.get('desc'), homework_begin_time=int(time.time()))

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
        # 新建解析器对象，用来获取request中的参数
        parse = reqparse.RequestParser()
        # 检查request中的hid，如果为int，则加入到parse对象中，如果不为int，返回‘错误的hid’
        parse.add_argument('hid', type=int, help='错误的hid', default='1')
        # 将parse对象中的参数读取到args中
        args = parse.parse_args()
        # 获取args中的hid
        hid = args.get('hid')  # 现在算是成功把request中的cid存入到hid变量里了

        try:
            # 从数据库中读取指定course对抗
            homework = HomeworkTable.query.get(hid)
        except:
            # 如果获取失败，则返回错误
            return jsonify(code=11, message='node not exist, query fail')

        if homework == None:
            return jsonify(code=11, message='node not exist, query fail')
        # 返回得到的homework对象，这里的homework是model对象，不可序列化，所以不能直接放入返回的json里面
        # 需要把homework中的各个字段对应放到一个dict里面，这个功能上面封装成了serialize_course函数
        return jsonify(code=0, message='OK', data={'homework':  self.serialize_homework(homework)})
    # 修改某作业
    @admin_required
    def put(self):
        # 新建解析器对象，用来获取request中的参数
        parse = reqparse.RequestParser()
        # 检查request中的hid，如果为int，则加入到parse对象中，如果不为int，返回‘错误的hid’
        parse.add_argument('hid', type=int, help='错误的hid', default='1')
        parse.add_argument(
            "homeworkname", type=str, required=True, help='homeworkname cannot be blank!')
        parse.add_argument(
            "desc", type=str, required=True, help='homeworkdesc cannot be blank!')
        # 将parse对象中的参数读取到args中
        args = parse.parse_args()
        # 获取args中的hid
        hid = args.get('hid')  # 现在算是成功把request中的hid存入到hid变量里了

        try:
            # 从数据库中读取指定course记录
            homework = HomeworkTable.query.get(hid)
        except:
            # 如果获取失败，则返回错误
            return jsonify(code=26, message='modify fail')

        # 当前数据库节点不存在
        if homework == None:
            return jsonify(code=26, message='modify fail')
        # 当前数据库节点存在，修改
        else:
            try:
                homework.homeworkname = args.get("homeworkname")
                homework.homework_desc = args.get("desc")
                homework.htype = 1
                print(homework.homeworkname)
            except:
                # 如果修改失败，则返回错误
                return jsonify(code=27, message='modify fail')

            try:
                db.session.commit()
            except:
                return jsonify(code=26, message='modify fail')

        return jsonify(code=0, message='OK', data={'homework':  self.serialize_homework(homework)})
    # 删除某作业
    def deleteFiles(self,hid):
        try:
            files = FileTable.query.filter_by(hid=hid).all();
        except:
            response = make_response(jsonify(code = 10,message='database error'))
            return response
        if files == None:
            return
        for file in files:
            db.session.delete(file)
        db.session.commit()
    @admin_required
    def delete(self):
        # 新建解析器对象，用来获取request中的参数
        parse = reqparse.RequestParser()
        # 检查request中的hid，如果为int，则加入到parse对象中，如果不为int，返回‘错误的hid’
        parse.add_argument('hid', type=int, help='错误的hid', default='1')
        # 将parse对象中的参数读取到args中
        args = parse.parse_args()
        # 获取args中的cid
        hid = args.get('hid')  # 现在算是成功把request中的hid存入到hid变量里了

        try:
            # 从数据库中读取指定course记录
            homework = HomeworkTable.query.get(hid)
        except:
            # 如果获取失败，则返回错误
            return jsonify(code=25, message='delete fail')

        # 当前数据库节点不存在
        if homework == None:
            return jsonify(code=25, message='delete fail')
        # 当前数据库节点存在
        else:
            try:
                self.deleteFiles(homework.hid)
                db.session.delete(homework)
                db.session.commit()
            except:
                return jsonify(code=25, message='delete fail')

        return jsonify(code=0, message='OK')

# /api/homework/dataset?fid=xxx
class DatasetAPI(Resource):
    file_fields = {
        'fid': fields.Integer,
        'hid': fields.Integer,
        'ftype': fields.Integer,
        'filename': fields.String
    }

    @marshal_with(file_fields)
    def serialize_file(self, file):
        return file
    # 下载数据集
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('fid',type = int)
        args = parse.parse_args()

        fid = args.get('fid')
        try:
            file_node = FileTable.query.get(fid)
        except:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        if file_node is None:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        hid = file_node.hid
        ftype = file_node.ftype
        filename = file_node.filename
        actual_filename = generate_dataset_name(hid,ftype,filename)
        target_file = os.path.join(os.path.expanduser(RESOURCES_FOLDER), actual_filename)
        if os.path.exists(target_file):
            return send_file(target_file,as_attachment=True,attachment_filename=filename,cache_timeout=3600)
        else:
            response = make_response(jsonify(code='22',message='file not exist'))
            return response
    # 删除数据集
    @admin_required
    def delete(self):
        parse = reqparse.RequestParser()
        parse.add_argument('fie',type=int,help='错误的fid',default='0')
        args = parse.parse_args()
        # 获取当前文件夹id
        fid = args.get('fid')

        if current_user.is_admin == 1:
            try:
                file_node = FileTable.query.get(fid)
            except:
                response = make_response(jsonify(code=11,message='node not exist, query fail'))
                return response
            if file_node is None:
                response = make_response(jsonify(code=11,message='node not exist, query fail'))
                return response
            try:
                hid = file_node.hid
                ftype = file_node.ftype
                filename = file_node.filename
                actual_filename = generate_dataset_name(hid,ftype,filename)
                target_file = os.path.join(os.path.expanduser(COURSEWARES_FOLDER), actual_filename)
                # 本地删除
                if os.path.exists(target_file):
                    os.remove(target_file)
                # 修改数据库中的文件名
                db.session.delete(file_node)
                db.session.commit()
                response = make_response(jsonify(code = 0,message='OK'))
                return response
            except:
                response = make_response(jsonify(code=20,message='file error'))
                return response
        else:
            response = make_response(jsonify(code=36,message='permission denied'))
            return response

# /api/homework/datasets
class DatasetsAPI(Resource):
    file_fields = {
        'fid': fields.Integer,
        'hid': fields.Integer,
        'ftype': fields.Integer,
        'filename': fields.String
    }

    @marshal_with(file_fields)
    def serialize_file(self, file):
        return file

    # 上传数据集
    @admin_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type = int)
        parse.add_argument('ftype',type=str)
        parse.add_argument('file', type=FileStorage, location='files')
        args = parse.parse_args()

        hid = args.get('hid')
        ftype = args.get('ftype')
        f = args['file']

        if f:
            filename = f.filename
            if '\"' in filename:
                filename = filename[:-1]
            actual_filename = generate_dataset_name(hid,ftype,filename)
            target_file = os.path.join(os.path.expanduser(RESOURCES_FOLDER), actual_filename)
            if os.path.exists(target_file):
                response = make_response(jsonify(code=21,message='file already exist, save fail'))
                return response
            try:
                # 保存文件
                f.save(target_file)
                filenode = FileTable(hid = hid,ftype = ftype,filename = filename)
                db.session.add(filenode)
                db.session.commit()
                response = make_response(jsonify(code=0,message='OK',data = {'file':self.serialize_file(filenode)}))
                return response
            except:
                response = make_response(jsonify(code=12,message='node already exist , add fail'))
                return response

    # 获取hid对应数据集
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type = int)
        args = parse.parse_args()

        hid = args.get('hid')

        try:
            print(current_user.is_admin)
            if current_user.is_admin == 1:
                print('in if')
                file_nodes = FileTable.query.filter_by(hid = hid).all()
            else:
                print('in else')
                file_nodes = FileTable.query.filter(FileTable.ftype.in_([0,1])).all()
                print('after query')
            response = make_response(jsonify(code = 0,data={'files':[ self.serialize_file(file) for file in file_nodes]}))
            return response
        except :
            response = make_response(jsonify(code=10,message='database error'))
            return response

# /api/homework/submit?uid=xxx&hid=xxx
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
    def serialize_user_homework(self, user_homework):
        return user_homework
    # 获取某学生的某作业
    @admin_required
    def get(self):
        pass
    # 某学生上传某作业
    @login_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type=int)
        parse.add_argument('file',type=FileStorage,location='files')
        args = parse.parse_args()

        hid = args.get('hid')
        uid = current_user.uid
        f = args['file']

        if f:
            filename = f.filename
            if '\"' in filename:
                filename = filename[:-1]
            actual_filename = generate_submit_name(hid,uid,filename)
            target_file = os.path.join(os.path.expanduser(RESOURCES_FOLDER), actual_filename)
            if os.path.exists(target_file):
                response = make_response(jsonify(code=21,message='file already exist, save fail'))
                return response
            try:
                # 保存文件
                print('in try')
                f.save(target_file)
                print('after save')
                userhomework_node = UserHomeworkTable(hid = hid,uid = uid,submit_file_name = filename,submit_time = int(time.time()))
                print('after create node')
                db.session.add(userhomework_node)
                db.session.commit()
                response = make_response(jsonify(code=0,message='OK',data = {'file':self.serialize_user_homework(userhomework_node)}))
                return response
            except:
                response = make_response(jsonify(code=12,message='node already exist , add fail'))
                return response

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
    def serialize_user_homework(self, user_homework):
        return user_homework
    # get某学生的某作业的分数
    @login_required
    def get(self):
        pass
    # 打分
    @admin_required
    def post(self):
        pass

# 获取某作业下的所有学生完成情况
# /api/homework/students?hid=xxx
class StudentsAPI(Resource):
    user_homework_fields = {
        'hid': fields.Integer,
        'uid': fields.Integer,
        'score': fields.Integer,
        'is_finished': fields.Integer,
        'submit_file_name': fields.String,
        'submit_time': fields.Integer
    }

    @marshal_with(user_homework_fields)
    def serialize_user_homework(self, user_homework):
        return user_homework

    @admin_required
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type=int)
        args = parse.parse_args()

        hid = args.get('hid')
        try:
            user_homeworks = UserHomeworkTable.query.filter_by(hid = hid).all()
            response = make_response(jsonify(code=0,message='OK',data={ 'users':[self.serialize_user_homework(user_homework) for user_homework in user_homeworks] }))
            return response
        except:
            response = make_response(jsonify(code=10,message='database error'))
            return response

# util 辅助函数

# 为file生成文件名
import hashlib


def generate_dataset_name(hid,ftype,filename):
    return hashlib.md5(
        (str(hid) + '_' + str(ftype) + '_' + filename).encode('utf-8')).hexdigest()

# 为submit生成文件名
import hashlib


def generate_submit_name(hid, uid,filename):
    return hashlib.md5(
        (str(hid) + '_' + str(uid) + '_' + filename).encode('utf-8')).hexdigest()
