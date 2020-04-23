from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask_restful import Api, Resource, fields, marshal_with, marshal_with_field, reqparse


# Models
class UserTable(UserMixin, db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20))
    is_admin = db.Column(db.Integer, default=0)

    def get_id(self):
        return self.uid

    def get_is_admin(self):
        if self.is_admin:
            return True
        else:
            return False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def varify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.uid)


    user_fields = {
        'uid' : fields.Integer,
        'username' : fields.String,
        'is_admin' : fields.Integer
    }
    @marshal_with(user_fields)
    def to_json(self):
        return self

class CoursewareTable(db.Model):
    __tablename__ = 'courseware'
    cwid = db.Column(db.Integer, primary_key=True)
    courseware_name = db.Column(db.String(100))

    def __repr__(self):
        return "<Courseware {}>".format(self.cwid)

    courseware_fields = {
        'cwid': fields.Integer,
        'courseware_name': fields.String
    }

    @marshal_with(courseware_fields)
    def to_json(self):
        return self
class HomeworkTable(db.Model):
    __tablename__ = 'homework'
    hid = db.Column(db.Integer, primary_key=True)
    homeworkname = db.Column(db.String(200))
    htype = db.Column(db.Integer)  # 0 : jupyter , 1: python
    homework_desc = db.Column(db.String(500))
    homework_begin_time = db.Column(db.Integer)
    homework_end_time = db.Column(db.Integer)
    publish_rank = db.Column(db.Integer,default = 0)
    # 建立和 file 的一对多关系
    files = db.relationship('FileTable')

    # 所使用的指标的id
    indexid = db.Column(db.Integer)

    homework_fields = {
        'hid': fields.Integer,
        'htype': fields.Integer,
        'homeworkname': fields.String,
        'homework_desc': fields.String,
        'homework_begin_time': fields.Integer,
        'homework_end_time':fields.Integer,
        'publish_rank':fields.Integer,
        'indexid':fields.Integer,
        'files': fields.List(fields.Nested({
            'fid': fields.Integer,
            'hid': fields.Integer,
            'ftype': fields.Integer,
            'filename': fields.String
        }))
    }

    @marshal_with(homework_fields)
    def to_json(self):
        return self

class FileTable(db.Model):
    __tablename__ = 'file'
    fid = db.Column(db.Integer, primary_key=True)
    hid = db.Column(db.Integer, db.ForeignKey('homework.hid'))
    ftype = db.Column(db.Integer)
    filename = db.Column(db.String(100))

    file_fields = {
        'fid': fields.Integer,
        'hid': fields.Integer,
        'ftype': fields.Integer,
        'filename': fields.String
    }

    @marshal_with(file_fields)
    def to_json(self):
        return self

class UserHomeworkTable(db.Model):
    __tablename__ = 'user_homework'
    hid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer,default = 0)
    is_finished = db.Column(db.Integer, default=0)
    submit_file_name = db.Column(db.String(200))
    submit_time = db.Column(db.Integer)

    user_homework_fields = {
        'hid': fields.Integer,
        'uid': fields.Integer,
        'score': fields.Integer,
        'is_finished': fields.Integer,
        'submit_file_name': fields.String,
        'submit_time': fields.Integer
    }
    @marshal_with(user_homework_fields)
    def to_json(self):
        return self

class EvaluationIndexTable(db.Model):
    __tablename__ = 'evaluation_index'
    indexid = db.Column(db.Integer,primary_key=True)
    micro = db.Column(db.Integer,default = 0)
    macro = db.Column(db.Integer,default = 0)
    f1_score = db.Column(db.Integer,default = 0)
    rmse = db.Column(db.Integer,default = 0)
    r2_score = db.Column(db.Integer,default = 0)

    @staticmethod
    def get_names():
        index = ['micro','macro','f1_score','rmse','r2_score']
        return index

    evaluation_index_fields = {
        'indexid': fields.Integer,
        'micro': fields.Integer,
        'macro': fields.Integer,
        'f1_score': fields.Integer,
        'rmse': fields.String,
        'r2_score': fields.Integer
    }
    @marshal_with(evaluation_index_fields)
    def to_json(self):
        return self
