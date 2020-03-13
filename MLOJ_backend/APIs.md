



## 公共部分
* 首页： http://localhost:5000/index
	* method : GET

* 资料：http://localhost:5000/resourses
	* method : GET
* 登录：http://localhost:5000/login
	* method : GET
* 注册：http://localhost:5000/register
	* method : GET

## 学生端

* 课程页面(所有课程)： http://localhost:5000/courses
	* method : GET
	* response:
	```python
		data{
			course:[1,2,3]   # cid的数组
		}
	```

* 课程xxx：http://localhost:5000/course?cid=xxx
	* method : GET
	* body: ''
	* response:
	```python
		data{
			intro: '课程简介',
			courseware:'下载链接'
			homework:[1,2,3]   # hid的数组
		}
	```

* 作业xxx：http://localhost:5000/homework?hid=xxx
	* method: GET
	* body: 
	* response:
	```python
		data{
			intro:'作业介绍',
			'dataset':'数据集下载链接',
		}
	```
* 作业上传：http://localhost:5000/upload?hid=xxx
	* method: POST
	* body: 
	```python
		data{
			file:'file'
		}
	```

 

## 教师端

* 新建课程：http://localhost:5000/newCourse
	* method:GET  跳转到新建课程的表单
* 新建课程：http://localhost:5000/newCourse
	* method:POST
	* body:
		{
			coursename:'xxx'
		}
* 课件上传：http://localhost:5000/uploadCourseware?cid=1
	* method POST:
	* body:
		{
			file:'file'
		}
* 新建作业：http://localhost:5000/newHomeword?cid=1
	* GET  跳转到新建作业的表单
* 新建作业
	* POST
	* body
		{
			homeworkname:'xxx',
			homeworktype: 0/1
		}

* 数据集上传：http://localhost:5000/uploadDataSet?cid=1
	* method POST:
	* body:
		{
			file:'file'
		}
* 批改作业：http://localhost:5000/pingfen?hid=1&uid=201672048
	* GET  去批改页面
	* body:
		```
			homeworkname:'xxx',
			type: 0/1
		```
* 批改作业： http://localhost:5000/pingfen?hid=1&uid=201672048
	* POST 提交分数
	* body
		{
			grade:''
		}


## 后端架构：

```
MLOJ_backend
|
|-- app.py
|
|-- files
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









