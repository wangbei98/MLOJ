

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


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


class CoursewareTable(db.Model):
    __tablename__ = 'courseware'
    cwid = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))

    def __repr__(self):
        return "<Courseware {}>".format(self.cwid)


class HomeworkTable(db.Model):
    __tablename__ = 'homework'
    hid = db.Column(db.Integer, primary_key=True)
    homeworkname = db.Column(db.String(200))
    htype = db.Column(db.Integer)  # 0 : jupyter , 1: python
    homework_desc = db.Column(db.String(500))
    homework_begin_time = db.Column(db.Integer)

    # 建立和 file 的一对多关系
    files = db.relationship('FileTable')


class FileTable(db.Model):
    __tablename__ = 'file'
    fid = db.Column(db.Integer, primary_key=True)
    hid = db.Column(db.Integer, db.ForeignKey('homework.hid'))
    ftype = db.Column(db.String(20))
    filename = db.Column(db.String(100))


class UserHomeworkTable(db.Model):
    __tablename__ = 'user_homework'
    hid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    is_finished = db.Column(db.Integer, default=0)
    submit_file_name = db.Column(db.String(100))
    submit_time = db.Column(db.Integer)
