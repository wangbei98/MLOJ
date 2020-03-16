
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(uid):
	from models import UserTable
	return UserTable.query.get(int(uid))



login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'
