from flask_login import current_user
from flask import make_response,jsonify
from functools import wraps
from flask import current_app
from models import UserHomeworkTable,FileTable
from sqlalchemy import and_
from settings import config

RESOURCES_FOLDER = config['RESOURCES_FOLDER']


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




import pandas as pd


def get_micro_precision_score(ans_path,res_path):
    ans_data = pd.read_csv(ans_path).iloc[:,-1]
    res_data = pd.read_csv(res_path).iloc[:,-1]
    from sklearn.metrics import precision_score
    precision_score =  precision_score(ans_data, res_data, average="micro")
    return round(precision_score*10,1)

def get_macro_precision_score(ans_path,res_path):
    ans_data = pd.read_csv(ans_path).iloc[:,-1]
    res_data = pd.read_csv(res_path).iloc[:,-1]
    from sklearn.metrics import precision_score
    precision_score =  precision_score(ans_data, res_data, average="macro")
    return round(precision_score*10,1)

def get_f1_score(ans_path,res_path):
    ans_data = pd.read_csv(ans_path).iloc[:,-1]
    res_data = pd.read_csv(res_path).iloc[:,-1]
    from sklearn.metrics import f1_score
    f1_s = f1_score(ans_data,res_data)
    return round(f1_s*10,1)
def get_rmse(ans_path,res_path):
    ans_data = pd.read_csv(ans_path).iloc[:,-1]
    res_data = pd.read_csv(res_path).iloc[:,-1]
    import numpy as np
    rmse = np.sqrt(np.mean(np.square(ans_data-res_data)))
    return round((1-rmse)*10,1)
def get_r2_score(ans_path,res_path):
    ans_data = pd.read_csv(ans_path).iloc[:,-1]
    res_data = pd.read_csv(res_path).iloc[:,-1]
    from sklearn.metrics import r2_score
    r2_score = r2_score(ans_data,res_data)
    return round(r2_score*10,1)


# def get_score(ans_path,res_path,evaluate_standard):
# 	if evaluate_standard == 'micro' :
# 		score = get_micro_precision_score(ans_path,res_path)
# 		return round(score*10,1)
# 	elif evaluate_standard == 'macro':
# 		score = get_macro_precision_score(ans_path,res_path)
# 		return round(score*10,1)
# 	elif evaluate_standard == 'f1_score':
# 		score = get_f1_score(ans_path,res_path)
# 		return round(score*10,1)
# 	elif evaluate_standard == 'rmse':
# 		score = get_rmse(ans_path,res_path)
# 		return round((1-score)*10,1)
# 	elif evaluate_standard == 'r2_score':
# 		score = get_r2_score(ans_path,res_path)
# 		return round(score*10,1)


## 获取某个作业对应的答案的路径
def get_answer_path(hid):
	try:
		file = FileTable.query.filter(and_(FileTable.hid==hid,FileTable.ftype==-1)).first()
	except:
		return ''
	if file is None:
		return ''
	filename = file.filename
	ftype = file.ftype
	actual_filename = generate_dataset_name(hid,ftype,filename)
	target_file = os.path.join(os.path.expanduser(RESOURCES_FOLDER), actual_filename)
	return target_file

if __name__ == '__main__':
    res_path = 'test/res.csv'
    ans_path = 'test/ans.csv'
    
    print(get_score(ans_path,res_path,'micro'))
    print(get_score(ans_path,res_path,'macro'))
    # print(get_score(ans_path,res_path,'f1_score'))
    print(get_score(ans_path,res_path,'rmse'))
    print(get_score(ans_path,res_path,'r2_score'))



