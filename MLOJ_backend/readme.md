readme.md


## 运行

```
cd 进 MLOJ_backend
pipenv install (下载所需的所有依赖)
pipenv shell （进入pipenv的shell环境）
flask run (运行)
```


## 后端目录结构

```
MLOJ_backend
	|
	| -- APIS （API设计）
		  | -- admin.py  管理员操作
		  | -- auth.py 用户登入等出相关
		  | -- user.py  普通用户操作
	|
	| -- .flaskenv (flask 配置文件)
	| 
	| -- app.py (项目入口文件)
	|
	| -- extensions.py 定义一些扩展工具 
	|
	| -- models.py  定义数据库类
	|
	| -- Pipfile/Pipfile.lock 虚拟环境下载的依赖包信息 
```