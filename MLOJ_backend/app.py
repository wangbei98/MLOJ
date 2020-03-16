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
from APIS.auth import Login,Register,Logout

# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import SignatureExpired, BadSignature

# SQLite URI compatiblec
WIN = sys.platform.startswith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'MLOJ.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# restful api
api = Api(app)

db.init_app(app)
login_manager.init_app(app)
# login.login_view = 'login'

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
	"""Initialize the database."""
	if drop:
		db.drop_all()
		click.echo('Drop tables')
	db.create_all()
	# 在数据库中存储一个默认根目录 root  id = 0
	admin = UserTable(uid=123456,password_hash = generate_password_hash('123456'),is_admin=True)
	db.session.add(admin)
	db.session.commit()
	click.echo('Initialized database.')

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, UserTable=UserTable,CourseTable = CourseTable,HomeworkTable = HomeworkTable,UserHomeworkTable = UserHomeworkTable)


api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Logout,'/logout',endpoint='logout')

