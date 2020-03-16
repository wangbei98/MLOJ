[TOC]


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
	|
	| -- files 文件目录
		  |
		  | -- courseware:
		  			|
		  			| -- 课程xxx
		  			|		｜ xxx.zip
		  			| -- 课程xxx
		  					｜ xxx.zip
		  | -- datasets:
		  			|
		  			| -- 课程xxx
		  			|		｜ xxx.zip
		  			| -- 课程xxx
		  					｜ xxx.zip
		  | -- homework:
		  			| -- hid-xxx
		  					| -- 201672048
		  							｜ xxx.html
		  							｜ xxx.py
		  					| -- 201672049
		  							｜ xxx.html
		  							｜ xxx.py
		  					| -- 201672050
		  							｜ xxx.html
		  							｜ xxx.py
		  					| -- 201672051
		  			| -- hid-xxx
		  					| -- 201672048
		  					| -- 201672049
		  					| -- 201672050
	  					| -- 201672051
```

## API设计

### 设计资源端点

* 用户登录/注册/登出
* 获取用户信息
* 获取所有课程
* 新建课程
* 删除课程
* 获取课程信息
* 修改课程信息
* 上传课件
* 下载课件
* 新建作业
* 删除作业
* 获取作业信息
* 修改作业信息
* 上传数据集
* 下载数据集
* 上传作业
* 批改作业

#### 图例：

* <u>下划线</u>：学生可以用
* *斜体*：老师可以用
* **加粗**：都可以用

| 资源       | URL                                        | 实现方法/对应功能                                            |
| ---------- | ------------------------------------------ | ------------------------------------------------------------ |
| 当前用户   | /api/user                                  | 学生：GET(获取当前用户的信息)                                |
| 单个课程   | /api/course?cid=xxx                        | 学生&老师：GET获取xxx课程的信息，<br>老师：PUT(coursename=xxx,desc=xxx)修改xxx课程，<br>老师：DELETE  删除xxx课程 |
| 所有课程   | /api/courses                               | 学生&老师：GET获取所有课程<br/>老师：POST(coursename=xxx,desc=xxxx)新建一个课程 |
| 课件       | /api/courseware?cid=xxx                    | 学生&老师：GET下载课程xxx对应的课件<br/>老师：POST(file=xxx) 上传 |
| 单个作业题 | /api/course/homework?hid=xxx               | 学生&老师：GET 获取<br/>老师：PUT (homeworkname=xxx,homeworkdesc=xxx,type=1)修改<br/>老师：DELETE 删除 |
| 所有作业题 | /api/course/homeworks?cid=xxx              | 学生&老师：GET 获取xxx作业题的信息<br/>老师：POST(homeworkname=xxx,homeworkdesc=xxx,type=x)为cid为xxx的课程新建作业题，作业题类型为x |
| 数据集     | /api/course/homework/datasets?hid=xxx      | 学生&老师：GET 获取xxx作业题对应的数据集<br/>老师：POST(file=xx)为xxx上传数据集<br/>老师：DELETE删除数据集 |
| 作业       | /api/user/course/homework?uid=xxx&hid=xxx  | 学生&老师：GET获取xxx学生的xxx作业信息<br/>学生：POST(file=xxx) 这个学生提交这次作业的答案 |
| 分数       | /api/course/homework/score?uid=xxx&hid=xxx | 老师：POST(score=xxxx) 为这个人的这个作业打分                |