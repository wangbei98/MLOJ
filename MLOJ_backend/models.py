

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


# Models
class UserTable(UserMixin,db.Model):
	__tablename__ = 'UserTable'
	uid = db.Column(db.Integer,primary_key=True)
	password_hash = db.Column(db.String(200), nullable=False)
	username = db.Column(db.String(20))
	is_admin = db.Column(db.Boolean, default=False)
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
	def password(self,password):
		self.password_hash = generate_password_hash(password)
	def varify_password(self,password):
		return check_password_hash(self.password_hash,password)
	def __repr__(self):
		return "<User {}>".format(self.uid)

class CourseTable(db.Model):
	__tablename__ = 'CourseTable'
	cid = db.Column(db.Integer,primary_key=True)
	course_name = db.Column(db.String(100))
	course_desc = db.Column(db.String(500))
	course_begin_time = db.Column(db.DateTime)
	courseware_url = db.Column(db.String(100))
	def __repr__(self):
		return "<Course {}>".format(self.uid)

# 用户课程表
# class ScoresTable(db.Model):
# 	__tablename__ = 'ScoresTable'
# 	uid = db.Column(db.Integer,primary_key=True)
# 	cid = db.Column(db.Integer)
# 	score = db.Column(db.Integer)
# 	def __repr__(self):
# 		return "<User {}> , < Course {}> , <Score {}>".format(self.uid,self.cid,self.score)


class HomeworkTable(db.Model):
	__tablename__ = 'HomeworkTable'
	hid = db.Column(db.Integer,primary_key=True)
	cid = db.Column(db.Integer)
	homework_type = db.Column(db.Integer) # 0 : jupyter , 1: python
	homework_desc = db.Column(db.String(500))
	homework_train_data_url = db.Column(db.String(100))
	homework_test_data_url = db.Column(db.String(100))
	homework_begin_time = db.Column(db.DateTime)

class UserHomeworkTable(db.Model):
	__tablename__ = 'UserHomeworkTable'
	hid = db.Column(db.Integer,primary_key=True)
	uid = db.Column(db.Integer,primary_key=True)
	homework_score = db.Column(db.Integer)


