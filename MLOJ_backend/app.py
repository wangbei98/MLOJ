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

# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import SignatureExpired, BadSignature

app = Flask(__name__)
# restful api
api = Api(app)
login = LoginManager(app)
# login.login_view = 'login'

# SQLite URI compatiblec
WIN = sys.platform.startswith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = 'sqlite:////'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'UserTable.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
	"""Initialize the database."""
	if drop:
		db.drop_all()
		click.echo('Drop tables')
	db.create_all()
	# 在数据库中存储一个默认根目录 root  id = 0
	admin = UserTable(user_id=123456,password_hash = generate_password_hash('123456'),is_admin=True)
	db.session.add(admin)
	db.session.commit()
	click.echo('Initialized database.')


# handlers
# @app.error_handler
# def unauthorized():
# 	error_info = '{}'.format('Invalid credentials')
# 	print('api.auth.unauthorized.error_info = ' + error_info)
# 	response = jsonify({'error': error_info})
# 	response.status_code = 403

# 	print('api.auth.unauthorized.response = ' + str(response))

# 	return response
@app.shell_context_processor
def make_shell_context():
	return dict(db=db, UserTable=UserTable)


@login.user_loader
def load_user(id):
	return UserTable.query.get(int(id))

# Models
class UserTable(UserMixin,db.Model):
	__tablename__ = 'UserTable'
	user_id = db.Column(db.Integer,primary_key=True)
	password_hash = db.Column(db.String(100), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	def get_id(self):
		return self.user_id
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
		return "<User {}>".format(self.user_id)
class ScoresTable(db.Model):
	__tablename__ = 'ScoresTable'
	user_id = db.Column(db.Integer,primary_key=True)
	course_id = db.Column(db.Integer)
	score = db.Column(db.Integer)
	def __repr__(self):
		return "<User {}> , < Course {}> , <Score {}>".format(self.user_id,self.course_id,self.score)
class CourseTable(db.Model):
	__tablename__ = 'CourseTable'
	course_id = db.Column(db.Integer,primary_key=True)
	course_name = db.Column(db.String(100))
	def __repr__(self):
		return "<Course {}>".format(self.user_id)
# apis
class Login(Resource):
	def post(self):
		if current_user.is_authenticated:
			# TODO
			return jsonify('already authenticated')
		parse = reqparse.RequestParser()
		parse.add_argument('user_id',type=int,help='用户名验证不通过',default=201000000)
		parse.add_argument('password',type=str,help='密码验证不通过')
		args = parse.parse_args()

		user_id = args.get("user_id")
		password = args.get("password")
		try:
			user = UserTable.query.get(user_id)
		except Exception:
			print("{} User query: {} failure......".format(time.strftime("%Y-%m-%d %H:%M:%S"),user_id))
			return jsonify('user not found')
		else:
			print("{} User query: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id))
		finally:
			db.session.close()
		if user and user.varify_password(password):
			login_user(user)
			print(current_user)
			return jsonify('login success')
		else:
			print('in if')
			print("{} User query: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id))
			print('user is None or password False')
			return jsonify('login fail')
		
class Register(Resource):
	def post(self):
		parse = reqparse.RequestParser()
		parse.add_argument('user_id',type=int,help='用户名验证不通过',default=201000000)
		parse.add_argument('password',type=str,help='密码验证不通过')
		args = parse.parse_args()

		user_id = args.get('user_id')
		password = args.get('password')
		password_hash = generate_password_hash(password)
		try:
			user = UserTable(user_id = user_id,password_hash =password_hash)
			db.session.add(user)
			db.session.commit()
		except:
			print("{} User add: {} failure...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id))
			db.session.rollback()
			return jsonify('user add fail')
		else:
			print("{} User add: {} success...".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id))
			return jsonify('user add success')
		finally:
			db.session.close()
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Register, '/register', endpoint='register')

class LoginOut(Resource):
	@login_required
	def get():
	    logout_user()
	    flash("已退出登录")
	    return jsonify('loginout success')
api.add_resource(LoginOut,'/loginout',endpoint='loginout')

