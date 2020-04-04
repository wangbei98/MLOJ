from flask_login import current_user
from flask import make_response,jsonify
from functools import wraps
from flask import current_app
def admin_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not current_user.is_authenticated:
			# print(current_user.authority)
			return current_app.login_manager.unauthorized()

		if current_user.is_admin == 0:
			return jsonify(code=36,message='permission denied')
		return func(*args, **kwargs)
	return decorated_view


# util 辅助函数

# 为file生成文件名
import hashlib


def generate_dataset_name(hid,ftype,filename):
    return hashlib.md5(
        (str(hid) + '_' + str(ftype) + '_' + filename).encode('utf-8')).hexdigest()

# 为submit生成文件名
def generate_submit_name(hid, uid,filename):
    return hashlib.md5(
        (str(hid) + '_' + str(uid)).encode('utf-8')).hexdigest() + '_ ' + filename