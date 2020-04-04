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
from utils import admin_required,generate_dataset_name,generate_submit_name
from sqlalchemy import and_
# 获取配置文件中定义的资源目录
RESOURCES_FOLDER = config['RESOURCES_FOLDER']
COURSEWARES_FOLDER = config['COURSEWARES_FOLDER']
SUBMITS_FOLDER = config['SUBMITS_FOLDER']

'''
资源操作相关API
'''

# /api/courseware?cwid=xxx
class CoursewareAPI(Resource):
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
                response = make_response(jsonify(code=0,message='OK',data = {'courseware':filenode.to_json()}))
                return response
            except:
                response = make_response(jsonify(code=12,message='node already exist , add fail'))
                return response
    def get(self):
        try:
            # file_nodes = FileNode.query.filter_by(user_id=cur_uid)
            file_nodes = CoursewareTable.query.all()
            response = make_response(jsonify(code = 0,data={'coursewares':[file.to_json() for file in file_nodes]}))
            return response
        except :
            response = make_response(jsonify(code=10,message='database error'))
            return response

# /api/homeworks
class HomeworksAPI(Resource):
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
        return jsonify(code=0, message='OK', data={'homeworks':  [ homework.to_json() for homework in homework_li]})
    # 新建课程
    @admin_required
    def post(self):
        # 新建解释器对象，用来获取request中的对象
        parse = reqparse.RequestParser()
        # 检查request中的htype，如果为int，则加入到parse对象中，如果不为int，返回‘错误的htype’
        parse.add_argument('type', type=int, help='错误的htype', default='1')
        # 检查request中的homeworkname，str类型不为空
        parse.add_argument("homeworkname", type=str, required=True, help='homeworkname cannot be blank!')
        # 检查request中的desc，str类型不为空
        parse.add_argument("desc", type=str, required=True, help='homework_desc cannot be blank!')
        parse.add_argument('publish_rank',type =int,required=True,help = 'public_rank cannot be blank')
        parse.add_argument('end_time',type = int,required=True,help='end time cannot be blank')
        # 将parse对象中的参数读取到args中
        args = parse.parse_args()
        # new
        homework = HomeworkTable(htype=args.get('type'), homeworkname=args.get(
            'homeworkname'), homework_desc=args.get('desc'), homework_begin_time=int(time.time()),homework_end_time=int(time.time())+args.get('end_time')*24*3600 )

        try:
            db.session.add(homework)
            db.session.commit()
        except:
            # 如果插入失败，则返回错误
            return jsonify(code=27, message='insert fail')

        return jsonify(code=0, message="OK", data={'homework':  homework.to_json()})

# /api/homework?hid=xxx
class HomeworkAPI(Resource):
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
            # 从数据库中读取指定course对象
            homework = HomeworkTable.query.get(hid)
        except:
            # 如果获取失败，则返回错误
            return jsonify(code=11, message='node not exist, query fail')

        if homework == None:
            return jsonify(code=11, message='node not exist, query fail')
        # 返回得到的homework对象，这里的homework是model对象，不可序列化，所以不能直接放入返回的json里面
        return jsonify(code=0, message='OK', data={'homework':  homework.to_json()})
    # 修改某作业
    @admin_required
    def put(self):
        # 新建解析器对象，用来获取request中的参数
        parse = reqparse.RequestParser()
        # 检查request中的hid，如果为int，则加入到parse对象中，如果不为int，返回‘错误的hid’
        parse.add_argument('hid', type=int, help='错误的hid', default='1')
        parse.add_argument("homeworkname", type=str, required=True, help='homeworkname cannot be blank!')
        parse.add_argument("desc", type=str, required=True, help='homeworkdesc cannot be blank!')
        parse.add_argument('publish_rank',type =int,required=True,help = 'public_rank cannot be blank')
        parse.add_argument('end_time',type = int,required=True,help='end time cannot be blank')
        # 将parse对象中的参数读取到args中
        args = parse.parse_args()
        # 获取args中的hid
        hid = args.get('hid')
        homeworkname = args.get('homeworkname')
        desc = args.get('desc')
        publish_rank = args.get('publish_rank')
        end_time = args.get('end_time')
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
                homework_end_time = homework.homework_begin_time + end_time * 24 * 3600
                homework.homeworkname = homeworkname
                homework.homework_desc = desc
                homework.publish_rank = publish_rank
                homework.homework_end_time = homework_end_time
            except:
                # 如果修改失败，则返回错误
                return jsonify(code=27, message='modify fail')

            try:
                db.session.commit()
            except:
                return jsonify(code=26, message='modify fail')

        return jsonify(code=0, message='OK', data={'homework':  homework.to_json()})
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
                response = make_response(jsonify(code=0,message='OK',data = {'file':filenode.to_json()}))
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
            response = make_response(jsonify(code = 0,data={'files':[ file.to_json() for file in file_nodes]}))
            return response
        except :
            response = make_response(jsonify(code=10,message='database error'))
            return response

# /api/homework/submit?hid=xxx
# 学生提交的作业
class SubmitAPI(Resource):
    @login_required
    # 学生查看自己提交的作业
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type=int,required=True,help='hid cannot be blank')
        args = parse.parse_args()
        hid = args.get('hid')
        uid = current_user.uid
        try:
            print(hid)
            print(uid)
            user_homework = UserHomeworkTable.query.filter(and_(UserHomeworkTable.hid==hid,UserHomeworkTable.uid==uid)).first()
        except:
            response = make_response(jsonify(code=10,message='database error'))
            return response
        if user_homework is None:
            print('node is none')
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        filename = user_homework.submit_file_name
        actual_filename = generate_submit_name(hid,uid,filename)
        target_file = os.path.join(os.path.expanduser(SUBMITS_FOLDER), actual_filename)
        if os.path.exists(target_file):
            return send_file(target_file,as_attachment=False,attachment_filename=filename,cache_timeout=3600)
        else:
            response = make_response(jsonify(code='22',message='file not exist'))
            return response
    # 删除数据集
    # 某学生上传某作业
    @login_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type=int,required=True,help='hid cannot be blank')
        parse.add_argument('file',type = FileStorage,location='files')
        args = parse.parse_args()
        hid = args.get('hid')
        file = args.get('file')
        uid = current_user.uid
        print(hid)
        print(uid)
        try:
            user_homework = UserHomeworkTable.query.filter(and_(UserHomeworkTable.hid==hid,UserHomeworkTable.uid==uid)).first()
        except:
            response = make_response(jsonify(code=10,message='database error'))
            return response
        # 已存在，删掉原来的文件
        if user_homework:
            print('node exists')
            old_filename = user_homework.submit_file_name
            old_actual_filename = generate_submit_name(hid,uid,old_filename)
            old_target_file = os.path.join(os.path.expanduser(SUBMITS_FOLDER), old_actual_filename)
            if os.path.exists(old_target_file):
                print('file exists')
                os.remove(old_target_file)
            # 修改文件名
            filename = file.filename
            if '\"' in filename:
                filename = filename[:-1]
            try:
                user_homework.submit_file_name = filename
                db.session.add(user_homework)
                db.session.commit()
            except:
                response = make_response(jsonify(code=10,message='database error'))
                return response
            # 存储新文件
            try:
                actual_filename = generate_submit_name(hid,uid,filename)
                target_file = os.path.join(os.path.expanduser(SUBMITS_FOLDER), actual_filename)
                file.save(target_file)
                response = make_response(jsonify(code=0,message='OK'))
                return response
            except:
                response = make_response(jsonify(code=10,message='database error'))
                return response

        # 文件不存在，需要新建
        else:
            filename = file.filename
            if '\"' in filename:
                filename = filename[:-1]
            print(filename)
            try:
                user_homework = UserHomeworkTable(hid=hid,uid=uid,is_finished=1,submit_file_name=filename,submit_time=int(time.time()))
                db.session.add(user_homework)
                db.session.commit()
            except:
                response = make_response(jsonify(code=10,message='database error'))
                return response
            try:
                actual_filename = generate_submit_name(hid,uid,filename)
                target_file = os.path.join(os.path.expanduser(SUBMITS_FOLDER), actual_filename)
                file.save(target_file)
                response = make_response(jsonify(code=0,message='OK'))
                return response
            except:
                response = make_response(jsonify(code=10,message='database error'))
                return response
# /api/homework/score?hid=xxx
class ScoreAPI(Resource):

    # 学生 get某学生的某作业的分数
    @login_required
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type = int,required=True,help='hid cannot be blank')
        args = parse.parse_args()

        hid = args.get('hid')
        uid = current_user.uid
        try:
            user_homework = UserHomeworkTable.query.filter(and_(UserHomeworkTable.hid==hid,UserHomeworkTable.uid==uid)).first()
        except:
            response = make_response(jsonify(code=10,message='database error'))
            return response
        if user_homework is None:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        response = make_response(jsonify(code=0, message = 'OK',data = { 'score' : user_homework.score}))
        return response
    # 打分
    @admin_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type = int,required=True,help='hid cannot be blank')
        parse.add_argument('uid',type=int,required=True,help='uid cannot be blank')
        parse.add_argument('score',type=int,required=True,help='score cannot be blank')
        args = parse.parse_args()
        hid = args.get('hid')
        uid = args.get('uid')
        score = args.get('score')
        try:
            user_homework = UserHomeworkTable.query.filter(and_(UserHomeworkTable.hid==hid,UserHomeworkTable.uid==uid)).first()
        except:
            response = make_response(jsonify(code=10,message='database error'))
            return response
        if user_homework is None:
            response = make_response(jsonify(code=11,message='node not exist, query fail'))
            return response
        # TODO
        try:
            user_homework.score =score
            db.session.commit()
            response = make_response(jsonify(code=0,message='OK',data={'user-homework':user_homework.to_json()}))
            return response
        except:
            response = make_response(jsonify(code=10,message='database error'))
            return response
# 获取某作业下的所有学生完成情况
# /api/homework/students?hid=xxx

class StudentsAPI(Resource):
    @admin_required
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('hid',type=int)
        args = parse.parse_args()
        hid = args.get('hid')
        try:
            user_homeworks = UserHomeworkTable.query.filter_by(hid=hid).all()
            response = make_response(jsonify(code=0,message='OK',data={ 'users':[user_homework.to_json() for user_homework in user_homeworks] }))
            return response
        except:
            response = make_response(jsonify(code=10,message='database error'))
            return response


